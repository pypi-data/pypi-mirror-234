from collections import defaultdict
from itertools import chain
from typing import Callable, Dict, Iterable, Iterator, Set, Tuple, Type, TypeVar, Union

from typing_extensions import Self

from tdm.abstract.datamodel import EnsureIdentifiable, Identifiable, and_filter
from tdm.helper import unfold_union
from ._container import TypedIdsContainer
from ._state import pack_view_state, unpack_view_state
from ._types import get_base_type
from ._view import AbstractView, object_view, restore_object

_I = TypeVar('_I', bound=Identifiable)
_Base = TypeVar('_Base', bound=EnsureIdentifiable)


class ViewContainer(object):
    __slots__ = (
        '_id2view', '_dependencies', '_containers'
    )

    def __setstate__(self, state):
        d, s = state
        if d is not None:
            self.__dict__.update(d)
        s['_id2view'] = unpack_view_state(s['_id2view'])
        for component in chain.from_iterable(getattr(cls, '__slots__', ()) for cls in type(self).mro()):
            setattr(self, component, s.get(component, None))

    def __getstate__(self):
        result = {component: getattr(self, component, None) for component in
                  chain.from_iterable(getattr(cls, '__slots__', ()) for cls in type(self).mro())}
        result['_id2view'] = pack_view_state(result.get('_id2view', {}))
        d = self.__dict__ if hasattr(self, '__dict__') else None
        return d, result

    def __init__(
            self,
            id2view: Dict[str, Union[EnsureIdentifiable, AbstractView]],
            dependencies: Dict[str, Set[Tuple[str, Type[EnsureIdentifiable]]]],
            containers: Dict[Type[EnsureIdentifiable], TypedIdsContainer],
    ):
        self._id2view = id2view
        self._dependencies = dependencies
        self._containers = containers

    def _replace(self, **kwargs) -> Self:
        return type(self)(
            **{
                'id2view': self._id2view,
                'dependencies': self._dependencies,
                'containers': self._containers,
                **kwargs
            }
        )

    def id2element(self, base_type: Type[_Base]) -> Dict[str, _Base]:
        return {i: restore_object(self._id2view[i], self._id2view) for i, _ in self._containers[base_type]}

    def elements(self, base_type: Type[_Base]) -> Dict[Type[_Base], Iterable[_Base]]:
        return {
            t: {restore_object(self._id2view[i], self._id2view) for i in ids}
            for t, ids in self._containers[base_type].type2ids.items()
        }

    def get_element(self, base_type: Type[EnsureIdentifiable], id_: str) -> _I:
        if id_ not in self._containers[base_type]:
            raise KeyError
        return restore_object(self._id2view[id_], self._id2view)

    def get_elements(
            self, base_type: Type[EnsureIdentifiable], type_: Type[_I],
            filter_: Union[Callable[[_I], bool], Iterable[Callable[[_I], bool]]]
    ) -> Iterator[_I]:
        if isinstance(filter_, Iterable):
            filter_ = and_filter(*filter_)

        type_ = unfold_union(type_)
        if not all(issubclass(t, base_type) for t in type_):
            raise ValueError

        for t, ids in self._containers[base_type].type2ids.items():
            if not issubclass(t, type_):
                continue
            yield from filter(filter_, (restore_object(self._id2view[id_], self._id2view) for id_ in ids))

    def related_elements(
            self, base_type: Type[EnsureIdentifiable], obj: Union[Identifiable, str], type_: Type[_I],
            filter_: Union[Callable[[_I], bool], Iterable[Callable[[_I], bool]]]
    ) -> Iterator[_I]:
        if isinstance(obj, Identifiable):
            obj = obj.id
        if not isinstance(obj, str):
            raise ValueError

        if isinstance(filter_, Iterable):
            filter_ = and_filter(*filter_)

        type_ = unfold_union(type_)
        if not all(issubclass(t, base_type) for t in type_):
            raise ValueError

        for element_id, element_type in self._dependencies.get(obj, tuple()):
            if not issubclass(element_type, base_type):
                continue
            view = self._id2view[element_id]
            if not issubclass(view.orig_type(), type_):
                continue
            fact = restore_object(view, self._id2view)
            if filter_(fact):
                yield fact

    def with_elements(self, elements: Iterable[EnsureIdentifiable], *, update: bool = False) -> Self:
        containers: Dict[Type[EnsureIdentifiable], TypedIdsContainer] = dict(self._containers)
        id2view = dict(self._id2view)
        dependencies = defaultdict(set, self._dependencies)
        updated = set()

        elements = self._order_dependencies(set(elements), update)

        for element_type, element, element_view in elements:
            assert isinstance(element_view, AbstractView)
            container = containers[element_type]
            if element.id in container:
                try:
                    id2view[element.id].validate_update(element_view)
                except ValueError as e:
                    raise ValueError(f"Couldn't update element {element}") from e
            elif element.id in id2view:
                raise ValueError(f"Element {element} identifiers collision: document already "
                                 f"contains {id2view[element.id].orig_type()} with same id")
            if isinstance(element_view, AbstractView):
                for dep in element_view.__depends_on__:
                    if dep not in updated:
                        dependencies[dep] = set(dependencies[dep])
                        updated.add(dep)
                    dependencies[dep].add((element.id, element_type))
            id2view[element.id] = element_view
            containers[element_type] = containers[element_type].with_ids([(element.id, type(element))])

        return self._replace(
            id2view=id2view,
            dependencies=dependencies,
            containers=containers
        )

    def without_elements(self, ids: Iterable[str], *, cascade: bool = False) -> Self:
        ids = set(self._id2view.keys()).intersection(map(_to_id, ids))  # ignore excess ids
        if not cascade:
            # check no hang links
            for id_ in ids:
                for dep, _ in self._dependencies.get(id_, ()):
                    if dep not in ids:
                        raise ValueError(f"Couldn't remove element {id_} as it depends on element {dep}")
        remove_from_containers = defaultdict(set)
        id2view = dict(self._id2view)
        dependencies = dict(self._dependencies)
        updated = set()
        remove = defaultdict(set)
        removed_ids = set()
        for id_ in ids:
            remove[get_base_type(id2view[id_].orig_type())].add(id_)
        while remove:
            to_remove = defaultdict(set)
            for base_type, ids in remove.items():
                for id_ in ids:
                    if id_ in removed_ids:
                        continue
                    removed_ids.add(id_)
                    for dep_id, dep_type in dependencies.get(id_, ()):
                        to_remove[dep_type].add(dep_id)
                    view = id2view.pop(id_)
                    dependencies.pop(id_, None)
                    remove_from_containers[base_type].add(id_)
                    if not isinstance(view, AbstractView):
                        continue
                    for dep in view.__depends_on__:
                        if dep not in dependencies:
                            continue
                        if dep not in updated:
                            dependencies[dep] = set(dependencies[dep])
                            updated.add(dep)
                        dependencies[dep].discard((id_, base_type))
                        if not dependencies[dep]:
                            dependencies.pop(dep)
            remove = to_remove

        containers = dict(self._containers)
        for base_type, ids in remove_from_containers.items():
            containers[base_type] = containers[base_type].without_ids(ids)

        return self._replace(id2view=id2view, dependencies=dependencies, containers=containers)

    def _order_dependencies(
            self, elements: Set[EnsureIdentifiable], update: bool = False
    ) -> Iterable[Tuple[Type[EnsureIdentifiable], EnsureIdentifiable, AbstractView]]:
        result = []
        visited = set()
        while elements:
            to_process = set()
            for element in map(self._transform_element, elements):
                visited.add(element)
                view = object_view(element)

                result.append((get_base_type(element), element, view))

                if not isinstance(view, AbstractView):
                    continue  # no dependencies

                dependencies = view.get_dependencies(element)
                dependencies.difference_update(elements)  # will be processed next steps
                dependencies.difference_update(visited)
                if update:
                    to_process.update(dependencies)  # add to queue
                else:
                    self._validate_elements(dependencies)
            elements = to_process
        return result[::-1]

    def _transform_element(self, element: _Base) -> _Base:
        return element

    def _validate_elements(self, elements: Set[EnsureIdentifiable]) -> None:
        for element in elements:
            if element.id not in self._id2view:
                raise ValueError(f"document contains no {element}")
            view = self._id2view[element.id]
            element_type = type(element)
            view_type = view.orig_type() if isinstance(view, AbstractView) else type(view)
            if not issubclass(element_type, view_type) or not issubclass(view_type, element_type):
                raise ValueError(f"Type mismatch for {element}. Expected: {view_type}, actual: {element_type}")


def _to_id(obj: Union[str, EnsureIdentifiable]) -> str:
    return obj if isinstance(obj, str) else obj.id
