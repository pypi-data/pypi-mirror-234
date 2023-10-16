from __future__ import annotations

import enum
import typing as t

import typing_extensions as te
from rithm.fraction import Fraction

from rene import (Location,
                  Relation,
                  hints)
from rene._clipping import (intersect_polygon_with_multipolygon,
                            intersect_polygon_with_multisegmental,
                            intersect_polygon_with_polygon,
                            intersect_polygon_with_segment,
                            subtract_multipolygon_from_polygon,
                            subtract_polygon_from_polygon,
                            symmetric_subtract_multipolygon_from_polygon,
                            symmetric_subtract_polygon_from_polygon,
                            unite_polygon_with_multipolygon,
                            unite_polygon_with_polygon)
from rene._context import Context
from rene._relating import polygon
from rene._utils import locate_point_in_region


@te.final
class Polygon:
    @property
    def border(self) -> hints.Contour[Fraction]:
        return self._border

    @property
    def bounding_box(self) -> hints.Box[Fraction]:
        return self._border.bounding_box

    @property
    def holes(self) -> t.Sequence[hints.Contour[Fraction]]:
        return _PolygonHoles(self._holes, _TOKEN)

    def locate(self, point: hints.Point[Fraction], /) -> Location:
        location_without_holes = locate_point_in_region(self._border, point)
        if location_without_holes is Location.INTERIOR:
            for hole in self._holes:
                location_in_hole = locate_point_in_region(hole, point)
                if location_in_hole is Location.INTERIOR:
                    return Location.EXTERIOR
                elif location_in_hole is Location.BOUNDARY:
                    return Location.BOUNDARY
        return location_without_holes

    def relate_to(self, other: hints.Compound[Fraction], /) -> Relation:
        if isinstance(other, self._context.contour_cls):
            return polygon.relate_to_contour(self, other)
        elif isinstance(other, self._context.multisegment_cls):
            return polygon.relate_to_multisegment(self, other)
        elif isinstance(other, self._context.segment_cls):
            return polygon.relate_to_segment(self, other)
        elif isinstance(other, self._context.empty_cls):
            return Relation.DISJOINT
        elif isinstance(other, self._context.multipolygon_cls):
            return polygon.relate_to_multipolygon(self, other)
        elif isinstance(other, self._context.polygon_cls):
            return polygon.relate_to_polygon(self, other)
        else:
            raise TypeError(f'Unsupported type: {type(other)!r}.')

    _context: t.ClassVar[Context[Fraction]]
    _border: hints.Contour[Fraction]
    _holes: t.Sequence[hints.Contour[Fraction]]

    __module__ = 'rene.exact'
    __slots__ = '_border', '_holes'

    def __init_subclass__(cls, /, **_kwargs: t.Any) -> t.NoReturn:
        raise TypeError(f'type {cls.__qualname__!r} '
                        'is not an acceptable base type')

    def __new__(cls,
                border: hints.Contour[Fraction],
                holes: t.Sequence[hints.Contour[Fraction]],
                /) -> te.Self:
        self = super().__new__(cls)
        self._border, self._holes = border, tuple(holes)
        return self

    @t.overload
    def __and__(
            self, other: hints.Empty[Fraction], /
    ) -> hints.Empty[Fraction]:
        ...

    @t.overload
    def __and__(
            self,
            other: t.Union[
                hints.Multipolygon[Fraction], hints.Polygon[Fraction]
            ],
            /
    ) -> t.Union[
        hints.Empty[Fraction], hints.Multipolygon[Fraction],
        hints.Polygon[Fraction]
    ]:
        ...

    @t.overload
    def __and__(self, other: t.Any, /) -> t.Any:
        ...

    def __and__(self, other: t.Any, /) -> t.Any:
        return (
            intersect_polygon_with_multipolygon(
                    self, other, self._context.contour_cls,
                    self._context.empty_cls, self._context.multipolygon_cls,
                    self._context.polygon_cls, self._context.segment_cls
            )
            if isinstance(other, self._context.multipolygon_cls)
            else (
                intersect_polygon_with_polygon(
                        self, other, self._context.contour_cls,
                        self._context.empty_cls,
                        self._context.multipolygon_cls,
                        self._context.polygon_cls, self._context.segment_cls
                )
                if isinstance(other, self._context.polygon_cls)
                else (
                    intersect_polygon_with_multisegmental(
                            self, other, self._context.empty_cls,
                            self._context.multisegment_cls,
                            self._context.segment_cls
                    )
                    if isinstance(other, (self._context.contour_cls,
                                          self._context.multisegment_cls))
                    else (
                        intersect_polygon_with_segment(
                                self, other, self._context.empty_cls,
                                self._context.multisegment_cls,
                                self._context.segment_cls
                        )
                        if isinstance(other, self._context.segment_cls)
                        else (other
                              if isinstance(other, self._context.empty_cls)
                              else NotImplemented)
                    )
                )
            )
        )

    def __contains__(self, point: hints.Point[Fraction], /) -> bool:
        return self.locate(point) is not Location.EXTERIOR

    @t.overload
    def __eq__(self, other: te.Self, /) -> bool:
        ...

    @t.overload
    def __eq__(self, other: t.Any, /) -> t.Any:
        ...

    def __eq__(self, other: t.Any, /) -> t.Any:
        return ((self._border == other.border
                 and len(self._holes) == len(other.holes)
                 and frozenset(self._holes) == frozenset(other.holes))
                if isinstance(other, self._context.polygon_cls)
                else NotImplemented)

    def __hash__(self) -> int:
        return hash((self._border, frozenset(self._holes)))

    @t.overload
    def __or__(self, other: hints.Empty[Fraction], /) -> te.Self:
        ...

    @t.overload
    def __or__(
            self,
            other: t.Union[
                hints.Multipolygon[Fraction], hints.Polygon[Fraction]
            ],
            /
    ) -> t.Union[hints.Multipolygon[Fraction], hints.Polygon[Fraction]]:
        ...

    @t.overload
    def __or__(self, other: t.Any, /) -> t.Any:
        ...

    def __or__(self, other: t.Any, /) -> t.Any:
        return (
            unite_polygon_with_multipolygon(
                    self, other, self._context.contour_cls,
                    self._context.multipolygon_cls,
                    self._context.polygon_cls, self._context.segment_cls
            )
            if isinstance(other, self._context.multipolygon_cls)
            else
            (
                unite_polygon_with_polygon(
                        self, other, self._context.contour_cls,
                        self._context.multipolygon_cls,
                        self._context.polygon_cls,
                        self._context.segment_cls
                )
                if isinstance(other, Polygon)
                else (self
                      if isinstance(other, self._context.empty_cls)
                      else NotImplemented)
            )
        )

    def __repr__(self) -> str:
        return (f'{type(self).__qualname__}({self._border!r}, [{{}}])'
                .format(', '.join(map(repr, self._holes))))

    def __str__(self) -> str:
        return (f'{type(self).__qualname__}({self._border}, [{{}}])'
                .format(', '.join(map(str, self._holes))))

    @t.overload
    def __sub__(self, other: hints.Empty[Fraction], /) -> te.Self:
        ...

    @t.overload
    def __sub__(
            self,
            other: t.Union[
                hints.Multipolygon[Fraction], hints.Polygon[Fraction]
            ],
            /
    ) -> t.Union[
        hints.Empty[Fraction], hints.Multipolygon[Fraction],
        hints.Polygon[Fraction]
    ]:
        ...

    @t.overload
    def __sub__(self, other: t.Any, /) -> t.Any:
        ...

    def __sub__(self, other: t.Any, /) -> t.Any:
        return (
            subtract_multipolygon_from_polygon(
                    self, other, self._context.contour_cls,
                    self._context.empty_cls, self._context.multipolygon_cls,
                    self._context.polygon_cls, self._context.segment_cls
            )
            if isinstance(other, self._context.multipolygon_cls)
            else (
                subtract_polygon_from_polygon(
                        self, other, self._context.contour_cls,
                        self._context.empty_cls,
                        self._context.multipolygon_cls,
                        self._context.polygon_cls, self._context.segment_cls
                )
                if isinstance(other, self._context.polygon_cls)
                else (self
                      if isinstance(other, self._context.empty_cls)
                      else NotImplemented)
            )
        )

    @t.overload
    def __xor__(self, other: hints.Empty[Fraction], /) -> te.Self:
        ...

    @t.overload
    def __xor__(
            self,
            other: t.Union[
                hints.Multipolygon[Fraction], hints.Polygon[Fraction]
            ],
            /
    ) -> t.Union[
        hints.Empty[Fraction], hints.Multipolygon[Fraction],
        hints.Polygon[Fraction]
    ]:
        ...

    @t.overload
    def __xor__(self, other: t.Any, /) -> t.Any:
        ...

    def __xor__(self, other: t.Any, /) -> t.Any:
        return (
            symmetric_subtract_multipolygon_from_polygon(
                    self, other, self._context.contour_cls,
                    self._context.empty_cls,
                    self._context.multipolygon_cls,
                    self._context.polygon_cls, self._context.segment_cls
            )

            if isinstance(other, self._context.multipolygon_cls)
            else (
                symmetric_subtract_polygon_from_polygon(
                        self, other, self._context.contour_cls,
                        self._context.empty_cls,
                        self._context.multipolygon_cls,
                        self._context.polygon_cls,
                        self._context.segment_cls
                )
                if isinstance(other, self._context.polygon_cls)
                else (self
                      if isinstance(other, self._context.empty_cls)
                      else NotImplemented)
            )
        )


class _Token(enum.Enum):
    VALUE = object()


_TOKEN = _Token.VALUE


@te.final
class _PolygonHoles(t.Sequence[hints.Contour[Fraction]]):
    def count(self, contour: hints.Contour[Fraction], /) -> int:
        return self._holes.count(contour)

    def index(self,
              contour: hints.Contour[Fraction],
              start: int = 0,
              stop: t.Optional[int] = None,
              /) -> int:
        return self._holes.index(contour, start,
                                 *(() if stop is None else (stop,)))

    _holes: t.Sequence[hints.Contour[Fraction]]

    __module__ = 'rene.exact'
    __slots__ = '_holes',

    def __init_subclass__(cls, /, **_kwargs: t.Any) -> t.NoReturn:
        raise TypeError(f'type {cls.__qualname__!r} '
                        'is not an acceptable base type')

    def __new__(cls,
                holes: t.Sequence[hints.Contour[Fraction]],
                token: _Token,
                /) -> te.Self:
        if token is not _TOKEN:
            raise ValueError(f'{cls.__qualname__!r} is internal '
                             'and its instances should not be instantiated '
                             'outside of the library.')
        self = super().__new__(cls)
        self._holes = holes
        return self

    @t.overload
    def __eq__(self, other: te.Self, /) -> bool:
        ...

    @t.overload
    def __eq__(self, other: t.Any, /) -> t.Any:
        ...

    def __eq__(self, other: t.Any, /) -> t.Any:
        return (self._holes == other._holes
                if isinstance(other, _PolygonHoles)
                else NotImplemented)

    @t.overload
    def __getitem__(self, item: int) -> hints.Contour[Fraction]:
        ...

    @t.overload
    def __getitem__(self, item: slice) -> te.Self:
        ...

    def __getitem__(
            self, item: t.Union[int, slice]
    ) -> t.Union[hints.Contour[Fraction], te.Self]:
        return (_PolygonHoles(self._holes[item], _TOKEN)
                if type(item) is slice
                else self._holes[item])

    def __hash__(self) -> int:
        return hash(self._holes)

    def __len__(self) -> int:
        return len(self._holes)
