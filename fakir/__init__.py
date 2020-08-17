# fakir: a library for fast faking

#  Copyright 2020 Derrick W. Turk / terminus data science, LLC

#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at

#      http://www.apache.org/licenses/LICENSE-2.0

#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from random import Random
from copy import deepcopy
import operator

from typing import cast, Any, Callable, Dict, Generic, List, Optional, Tuple
from typing import TypeVar, Union

_T = TypeVar('_T', covariant=True)
_U = TypeVar('_U', covariant=True)

class Fakir(Generic[_T]):
    '''"abstract" base class for generators of fake values of a given type
    
    provides default implementations for core generation functionality and a
    full suite of "lifted" operator overloads, including:
    `__lt__`, `__le__`, `__eq__`, `__ne__`, `__ge__`, `__gt__`, `__add__`,
    `__sub__`, `__mul__`, `__floordiv__`, `__truediv__`, `__mod__`,
    `__matmul__`, `__pow__`, `__or__`, `__xor__`, `__and__`, `__getitem__`,
    `__contains__` `__lshift__`, `__rshift__`, `__concat__`, `__inv__`,
    `__abs__`, `__neg__`, and `__bool__`
    '''

    # default implementation is a memoized call to self.generate1 
    def _generate(self, r: Random, cache: Dict[int, Any]) -> _T:
        '''the core generation method, which should generate a value
        given a random.Random instance, and respect the by-object-id cache

        the default implementation calls generate1 to populate the cache
        if needed

        client code (including custom subclasses of Fakir) should almost never
        need to override this
        '''
        self_id = id(self)
        if self_id in cache:
            return cast(_T, cache[self_id])
        val = self.generate1(r)
        cache[self_id] = val
        return val

    def generate(self, r: Random) -> _T:
        '''generate a value given a random.Random instance
        
        the primary generation method called from client code: produce a new,
        independent draw from the generator'''
        return self._generate(r, dict())

    def generate1(self, r: Random) -> _T:
        '''generate a value given a random.Random instance, without using
        the cache
          
        this method is primarily a hook for subclasses to easily provide
        a valid _generate method using the default implementation from Fakir
        '''
        raise NotImplementedError

    def map(self, f: Callable[[_T], _U]) -> 'Fakir[_U]':
        '''lift a unary function over a Fakir'''
        return LiftFakir(f, self)

    def bind(self, f: Callable[[_T], 'Fakir[_U]']) -> 'Fakir[_U]':
        '''"monadic" bind - chain a Fakir to a computation which produces
        a resulting Fakir using the value drawn from the first Fakir'''
        return BindFakir(self, f)

    # an independent draw from the same distribution
    def iid(self) -> 'Fakir[_T]':
        '''"clone" a Fakir, allowing for an independent draw from the same
        distribution'''
        return deepcopy(self)

    def __lt__(self, other: 'Fakir[Any]') -> 'Fakir[Any]':
        '''a "lifted" less-than operator over Fakir objects'''
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
        return self.map(operator.inv)

    def __abs__(self) -> 'Fakir[Any]':
        return self.map(operator.abs) # type: ignore

    def __neg__(self) -> 'Fakir[Any]':
        return self.map(operator.neg)

    def __bool__(self) -> 'Fakir[bool]':
        return self.map(operator.truth)

    @staticmethod
    def lift(fn: Callable[..., _U], *args: 'Fakir[Any]') -> 'Fakir[_U]':
        '''"lift" an n-ary function over values to a function over Fakir
        objects of the corresponding types'''
        return LiftFakir(fn, *args)

    @staticmethod
    def liftList(fn: Callable[[List[Any]], _U],
            *args: 'Fakir[Any]') -> 'Fakir[_U]':
        '''"lift" an function over (heterogeneous) lists of values to a
        function over Fakir objects of the corresponding types'''
        return LiftFakir(lambda *args: fn(list(args)), *args)

class ConstFakir(Fakir[_T]):
    '''a Fakir which always generates a constant value (corresponds to
    monadic "return")'''

    def __init__(self, val: _T):
        self._val = val

    def _generate(self, r: Random, cache: Dict[int, Any]) -> _T:
        return self._val

class FnFakir(Fakir[_T]):
    '''a Fakir defined by a custom _generate method'''

    def __init__(self, fn: Callable[[Random, Dict[int, Any]], _T]):
        self._fn = fn

    def _generate(self, r: Random, cache: Dict[int, Any]) -> _T:
        return self._fn(r, cache)

class Fn1Fakir(Fakir[_T]):
    '''a Fakir defined by a custom generate1 method, used to wrap any function
    which can generate a value given a random.Random object'''

    def __init__(self, fn: Callable[[Random], _T]):
        self._fn = fn

    def generate1(self, r: Random) -> _T:
        return self._fn(r)

class LiftFakir(Fakir[_T]):
    '''a Fakir representing a lifted function over other Fakir objects'''

    def __init__(self, fn: Callable[..., _T], *args: Fakir[Any]):
        self._fn = fn
        self._args = args

    def _generate(self, r: Random, cache: Dict[int, Any]) -> _T:
        return self._fn(*(arg._generate(r, cache) for arg in self._args))

class BindFakir(Fakir[_U]):
    '''a Fakir representing a monadic bind over another Fakir object'''

    def __init__(self, fakir: Fakir[_T], fn: Callable[[_T], Fakir[_U]]):
            self._fakir = fakir
            self._fn = fn

    def _generate(self, r: Random, cache: Dict[int, Any]) -> _U:
        return self._fn(self._fakir._generate(r, cache))._generate(r, cache)

class ChoiceFakir(Fakir[_T]):
    '''a Fakir defined by a list of values from which to choose at random'''

    def __init__(self, choices: List[_T]):
        self._choices = choices

    def generate1(self, r: Random) -> _T:
        return r.choice(self._choices)

class BootstrapFakir(Fakir[List[_T]]):
    '''a Fakir defined by a list of values from which to sample lists at random
    with replacement'''

    def __init__(self, choices: List[_T], count: int):
        self._choices = choices
        self._count = count

    def generate1(self, r: Random) -> List[_T]:
        return r.choices(self._choices, k=self._count)

class PermuteFakir(Fakir[List[_T]]):
    '''a Fakir defined by a list of values from which to sample lists at random
    without replacement'''

    def __init__(self, choices: List[_T], choose: Optional[int] = None):
        self._choices = choices
        if choose is None:
            self._choose = len(self._choices)
        else:
            if not 0 <= choose <= len(self._choices):
                raise ValueError('sample larger than population or is negative')
            self._choose = choose

    def generate1(self, r: Random) -> List[_T]:
        return r.sample(self._choices, self._choose)

_V = TypeVar('_V') # needs invariant type parameter
def fixed(val: _V) -> Fakir[_V]:
    '''construct a Fakir which generates a fixed value'''
    return ConstFakir(val)

def rng_fn(fn: Callable[[Random], _T]) -> Fakir[_T]:
    '''construct a Fakir from a generating function on random.Random objects'''
    return Fn1Fakir(fn)

def choice(choices: List[_T]) -> Fakir[_T]:
    '''construct a Fakir which chooses uniformly at random from a list'''
    return ChoiceFakir(choices)

def bootstrap(choices: List[_T], count: int) -> Fakir[List[_T]]:
    '''construct a Fakir which chooses samples with replacement from a list'''
    return BootstrapFakir(choices, count)

def permute(choices: List[_T], choose: Optional[int] = None) -> Fakir[List[_T]]:
    '''construct a Fakir which generates permutations of a list'''
    return PermuteFakir(choices, choose)

def uniform(a: float, b: float) -> Fakir[float]:
    '''construct a Fakir which generates values from a uniform
    distribution on [a, b]'''
    return Fn1Fakir(lambda r: r.uniform(a, b))

def uniform1() -> Fakir[float]:
    '''construct a Fakir which generates values from a uniform
    distribution on [0, 1)'''
    return Fn1Fakir(Random.random)

def normal(mu: float, sigma: float) -> Fakir[float]:
    '''construct a Fakir which generates values from a normal distribution
    centered on mu with standard deviation sigma'''
    return Fn1Fakir(lambda r: r.normalvariate(mu, sigma))

def truncated_normal(mu: float, sigma: float, a: Optional[float] = None,
        b: Optional[float] = None) -> Fakir[float]:
    '''construct a Fakir which generates values from a truncated normal
    distribution centered on mu with standard deviation sigma, (optionally)
    bounded from below and above by a and b
    
    uses inefficient but reliable rejection sampling'''
    def tnorm(r: Random) -> float:
        while True:
            val = r.normalvariate(mu, sigma)
            if (a is None or val >= a) and (b is None or val <= b):
                return val
    return Fn1Fakir(tnorm)

def lognormal(mu: float, sigma: float) -> Fakir[float]:
    '''construct a Fakir which generates values whose natural logarithms are
    taken from a normal distribution centered on mu with standard
    deviation sigma'''
    return Fn1Fakir(lambda r: r.lognormvariate(mu, sigma))

def triangular(low: float, high: float, mode: float) -> Fakir[float]:
    '''construct a Fakir which generates values from a triangular distribution
    between low and high, with given mode'''
    return Fn1Fakir(lambda r: r.triangular(low, high, mode))

def beta(alpha: float, beta: float) -> Fakir[float]:
    '''construct a Fakir which generates values from a beta distribution
    with given alpha and beta'''
    return Fn1Fakir(lambda r: r.betavariate(alpha, beta))

def exponential(lambda_: float) -> Fakir[float]:
    '''construct a Fakir which generates values from an exponential distribution
    with given lambda'''
    return Fn1Fakir(lambda r: r.expovariate(lambda_))

def gamma(alpha: float, beta: float) -> Fakir[float]:
    '''construct a Fakir which generates values from a gamma distribution
    with given alpha and beta'''
    return Fn1Fakir(lambda r: r.gammavariate(alpha, beta))

def pareto(alpha: float) -> Fakir[float]:
    '''construct a Fakir which generates values from a Pareto distribution
    with given alpha'''
    return Fn1Fakir(lambda r: r.paretovariate(alpha))

def weibull(alpha: float, beta: float) -> Fakir[float]:
    '''construct a Fakir which generates values from a Weibull distribution
    with given alpha and beta'''
    return Fn1Fakir(lambda r: r.weibullvariate(alpha, beta))

def tupled(*args: Fakir[Any]) -> Fakir[Tuple[Any, ...]]:
    '''construct a Fakir which generates tuples of samples from each argument
    Fakir object'''
    return Fakir.liftList(tuple, *args)

def listed(*args: Fakir[Any]) -> Fakir[List[Any]]:
    '''construct a Fakir which generates lists of samples from each argument
    Fakir object'''
    return Fakir.liftList(lambda xs: xs, *args)

def repeat(fakir: Fakir[_T], count: int) -> Fakir[List[_T]]:
    '''construct a Fakir which generates lists of independent identically
    distributed samples from the same underlying Fakir'''
    return listed(*(fakir.iid() for _ in range(count)))

def ifelse(cond: Fakir[bool], ifTrue: Fakir[_T], ifFalse: Fakir[_U]
        ) -> Fakir[Union[_T, _U]]:
    '''construct a Fakir which generates values from one of two Fakir
    objects, depending on the truthiness of the value generated by the cond
    Fakir object'''
    def ifElse(cond: bool) -> Fakir[Union[_T, _U]]:
        if cond:
            return ifTrue.iid()
        return ifFalse.iid()
    return cond.bind(ifElse)

# just for documentation...
__pdoc__ = {
        'Fakir._generate': True,
}

__all__ = [
    'Fakir', 'ConstFakir', 'FnFakir', 'Fn1Fakir', 'LiftFakir', 'BindFakir',
    'ChoiceFakir', 'BootstrapFakir', 'PermuteFakir',
    'fixed', 'rng_fn', 'choice', 'bootstrap', 'permute', 'uniform', 'uniform1',
    'normal', 'truncated_normal', 'lognormal', 'triangular', 'beta',
    'exponential', 'gamma', 'pareto', 'weibull', 'tupled', 'listed', 'repeat',
    'ifelse'
]
