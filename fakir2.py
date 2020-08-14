from random import Random
from copy import deepcopy
from abc import ABC
import operator

from typing import cast
from typing import Any, Callable, Dict, Generic, List, Optional, Tuple, TypeVar

_T = TypeVar('_T')
_U = TypeVar('_U')

class Fakir(ABC, Generic[_T]):
    # default implementation is a memoized call to self.generate1 
    def _generate(self, r: Random, cache: Dict[int, Any]) -> _T:
        self_id = id(self)
        if self_id in cache:
            return cast(_T, cache[self_id])
        val = self.generate1(r)
        cache[self_id] = val
        return val

    def generate(self, r: Random) -> _T:
        return self._generate(r, dict())

    def generate1(self, r: Random) -> _T:
        raise NotImplementedError

    def fmap(self, f: Callable[[_T], _U]) -> 'Fakir[_U]':
        return FnFakir(lambda r, cache: f(self._generate(r, cache)))

    def bind(self, f: Callable[[_T], 'Fakir[_U]']) -> 'Fakir[_U]':
        return FnFakir(
          lambda r, cache: f(self._generate(r, cache))._generate(r, cache))

    # an independent draw from the same distribution
    def clone(self) -> 'Fakir[_T]':
        return deepcopy(self)

    def __lt__(self, other: 'Fakir[Any]') -> 'Fakir[Any]':
        return Fakir.lift(operator.lt, self, other)

    def __le__(self, other: 'Fakir[Any]') -> 'Fakir[Any]':
        return Fakir.lift(operator.le, self, other)

    # I don't care about the LSP here
    def __eq__(self, other: 'Fakir[Any]') -> 'Fakir[Any]': # type: ignore
        return Fakir.lift(operator.eq, self, other)

    # or here
    def __ne__(self, other: 'Fakir[Any]') -> 'Fakir[Any]': # type: ignore
        return Fakir.lift(operator.ne, self, other)

    def __ge__(self, other: 'Fakir[Any]') -> 'Fakir[Any]':
        return Fakir.lift(operator.ge, self, other)

    def __gt__(self, other: 'Fakir[Any]') -> 'Fakir[Any]':
        return Fakir.lift(operator.gt, self, other)

    def __add__(self, other: 'Fakir[Any]') -> 'Fakir[Any]':
        return Fakir.lift(operator.add, self, other)

    def __sub__(self, other: 'Fakir[Any]') -> 'Fakir[Any]':
        return Fakir.lift(operator.sub, self, other)

    def __mul__(self, other: 'Fakir[Any]') -> 'Fakir[Any]':
        return Fakir.lift(operator.mul, self, other)

    def __floordiv__(self, other: 'Fakir[Any]') -> 'Fakir[Any]':
        return Fakir.lift(operator.floordiv, self, other)

    def __truediv__(self, other: 'Fakir[Any]') -> 'Fakir[Any]':
        return Fakir.lift(operator.truediv, self, other)

    def __mod__(self, other: 'Fakir[Any]') -> 'Fakir[Any]':
        return Fakir.lift(operator.mod, self, other)

    def __matmul__(self, other: 'Fakir[Any]') -> 'Fakir[Any]':
        return Fakir.lift(operator.matmul, self, other)

    def __pow__(self, other: 'Fakir[Any]') -> 'Fakir[Any]':
        return Fakir.lift(operator.pow, self, other)

    def __or__(self, other: 'Fakir[Any]') -> 'Fakir[Any]':
        return Fakir.lift(operator.or_, self, other)

    def __xor__(self, other: 'Fakir[Any]') -> 'Fakir[Any]':
        return Fakir.lift(operator.xor, self, other)

    def __and__(self, other: 'Fakir[Any]') -> 'Fakir[Any]':
        return Fakir.lift(operator.and_, self, other)

    def __getitem__(self, other: 'Fakir[Any]') -> 'Fakir[Any]':
        return Fakir.lift(operator.getitem, self, other)

    def __contains__(self, other: 'Fakir[Any]') -> 'Fakir[Any]':
        return Fakir.lift(operator.contains, self, other)

    def __lshift__(self, other: 'Fakir[Any]') -> 'Fakir[Any]':
        return Fakir.lift(operator.lshift, self, other)

    def __rshift__(self, other: 'Fakir[Any]') -> 'Fakir[Any]':
        return Fakir.lift(operator.rshift, self, other)

    def __concat__(self, other: 'Fakir[Any]') -> 'Fakir[Any]':
        return Fakir.lift(operator.concat, self, other)

    def __inv__(self) -> 'Fakir[Any]':
        return self.fmap(operator.inv)

    def __abs__(self) -> 'Fakir[Any]':
        return self.fmap(operator.abs) # type: ignore

    def __neg__(self) -> 'Fakir[Any]':
        return self.fmap(operator.neg)

    def __bool__(self) -> 'Fakir[bool]':
        return self.fmap(operator.truth)

    @staticmethod
    def lift(fn: Callable[..., _U], *args: 'Fakir[Any]') -> 'Fakir[_U]':
        return FnFakir(
          lambda r, cache: fn(*(arg._generate(r, cache) for arg in args)))

    @staticmethod
    def liftList(fn: Callable[[List[Any]], _U],
            *args: 'Fakir[Any]') -> 'Fakir[_U]':
        return FnFakir(
          lambda r, cache: fn([arg._generate(r, cache) for arg in args]))

class ConstFakir(Fakir[_T]):
    def __init__(self, val: _T):
        self._val = val

    def _generate(self, r: Random, cache: Dict[int, Any]) -> _T:
        return self._val

class FnFakir(Fakir[_T]):
    def __init__(self, fn: Callable[[Random, Dict[int, Any]], _T]):
        self._fn = fn

    def _generate(self, r: Random, cache: Dict[int, Any]) -> _T:
        return self._fn(r, cache)

class Fn1Fakir(Fakir[_T]):
    def __init__(self, fn: Callable[[Random], _T]):
        self._fn = fn

    def generate1(self, r: Random) -> _T:
        return self._fn(r)

class ChoiceFakir(Fakir[_T]):
    def __init__(self, choices: List[_T]):
        self._choices = choices

    def generate1(self, r: Random) -> _T:
        return r.choice(self._choices)

class BootstrapFakir(Fakir[List[_T]]):
    def __init__(self, choices: List[_T], count: int):
        self._choices = choices
        self._count = count

    def generate1(self, r: Random) -> List[_T]:
        return r.choices(self._choices, k=self._count)

class PermuteFakir(Fakir[List[_T]]):
    def __init__(self, choices: List[_T], choose: Optional[int] = None):
        self._choices = choices
        if choose is None:
            self._choose = len(self._choices)
        else:
            self._choose = choose

    def generate1(self, r: Random) -> List[_T]:
        return r.sample(self._choices, self._choose)

def fixed(val: _T) -> Fakir[_T]:
    return ConstFakir(val)

def rng_fn(fn: Callable[[Random], _T]) -> Fakir[_T]:
    return Fn1Fakir(fn)

def choice(choices: List[_T]) -> Fakir[_T]:
    return ChoiceFakir(choices)

def bootstrap(choices: List[_T], count: int) -> Fakir[List[_T]]:
    return BootstrapFakir(choices, count)

def permute(choices: List[_T], choose: Optional[int] = None) -> Fakir[List[_T]]:
    return PermuteFakir(choices, choose)

def uniform(a: float, b: float) -> Fakir[float]:
    return Fn1Fakir(lambda r: r.uniform(a, b))

def normal(mu: float, sigma: float) -> Fakir[float]:
    return Fn1Fakir(lambda r: r.normalvariate(mu, sigma))

def lognormal(mu: float, sigma: float) -> Fakir[float]:
    return Fn1Fakir(lambda r: r.lognormvariate(mu, sigma))

def tupled(*args: Fakir[Any]) -> Fakir[Tuple[Any, ...]]:
    return Fakir.liftList(tuple, *args)

def listed(*args: Fakir[Any]) -> Fakir[List[Any]]:
    return Fakir.liftList(lambda xs: xs, *args)

# start with an empty cache for each repetition
def repeat(fakir: Fakir[_T], count: int) -> Fakir[List[_T]]:
    return FnFakir(
      lambda r, _: [fakir.generate(r) for _ in range(count)])

def ifelse(cond: Fakir[bool], ifTrue: Fakir[_T], ifFalse: Fakir[_T]
        ) -> Fakir[_T]:
    return cond.bind(lambda c: ifTrue if c else ifFalse)