import typing as t
from numbers import Rational

import typing_extensions as te
from rithm.fraction import Fraction
from rithm.integer import Int

_Coordinate = t.Union[Fraction, Int, Rational, float, int]


@te.final
class Point:
    @property
    def x(self) -> Fraction:
        return self._x

    @property
    def y(self) -> Fraction:
        return self._y

    _x: Fraction
    _y: Fraction

    __module__ = 'rene.exact'
    __slots__ = '_x', '_y'

    def __init_subclass__(cls, /, **_kwargs: t.Any) -> t.NoReturn:
        raise TypeError(f'type {cls.__qualname__!r} '
                        'is not an acceptable base type')

    def __new__(cls, x: _Coordinate, y: _Coordinate, /) -> te.Self:
        self = super().__new__(cls)
        self._x, self._y = Fraction(x), Fraction(y)
        return self

    @t.overload
    def __eq__(self, other: te.Self, /) -> bool:
        ...

    @t.overload
    def __eq__(self, other: t.Any, /) -> t.Any:
        ...

    def __eq__(self, other: t.Any, /) -> t.Any:
        return (self._x == other._x and self._y == other._y
                if isinstance(other, Point)
                else NotImplemented)

    @t.overload
    def __ge__(self, other: te.Self, /) -> bool:
        ...

    @t.overload
    def __ge__(self, other: t.Any, /) -> t.Any:
        ...

    def __ge__(self, other: t.Any, /) -> t.Any:
        return (self._x > other._x
                or self._x == other._x and self._y >= other._y
                if isinstance(other, Point)
                else NotImplemented)

    @t.overload
    def __gt__(self, other: te.Self, /) -> bool:
        ...

    @t.overload
    def __gt__(self, other: t.Any, /) -> t.Any:
        ...

    def __gt__(self, other: t.Any, /) -> t.Any:
        return (self._x > other._x
                or self._x == other._x and self._y > other._y
                if isinstance(other, Point)
                else NotImplemented)

    def __hash__(self) -> int:
        return hash((self._x, self._y))

    @t.overload
    def __le__(self, other: te.Self, /) -> bool:
        ...

    @t.overload
    def __le__(self, other: t.Any, /) -> t.Any:
        ...

    def __le__(self, other: t.Any, /) -> t.Any:
        return (self._x < other._x
                or self._x == other._x and self._y <= other._y
                if isinstance(other, Point)
                else NotImplemented)

    @t.overload
    def __lt__(self, other: te.Self, /) -> bool:
        ...

    @t.overload
    def __lt__(self, other: t.Any, /) -> t.Any:
        ...

    def __lt__(self, other: t.Any, /) -> t.Any:
        return (self._x < other._x
                or self._x == other._x and self._y < other._y
                if isinstance(other, Point)
                else NotImplemented)

    def __repr__(self) -> str:
        return f'{type(self).__qualname__}({self._x!r}, {self._y!r})'

    def __str__(self) -> str:
        return f'{type(self).__qualname__}({self._x}, {self._y})'
