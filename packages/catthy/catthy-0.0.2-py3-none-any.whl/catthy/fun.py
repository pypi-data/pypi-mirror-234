from __future__ import annotations
from typing import Generic, TypeVar, Callable, List, Tuple, Set, Dict, NamedTuple, Deque, ChainMap, Counter, OrderedDict, DefaultDict
from collections import deque, ChainMap, Counter, OrderedDict
from abc import ABC, abstractmethod, abstractclassmethod

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

K = TypeVar('K')
V = TypeVar('V')
K_1 = TypeVar('K_1')
V_1 = TypeVar('V_1')

MapFunction = Callable[[A], B]
DictMapFunction = Callable[[K,V], Tuple[K_1, V_1]]

class EnhancedContainer(Generic[A]):
    @classmethod
    def of(cls, *xs) -> EnhancedContainer[A]:
        return cls(xs)
    
class NaiveHashable:
    def __hash__(self):
        return hash(str(self))
    
class FunctionCastable:
    def cast(self, f: Callable) -> FunctionCastable:
        self = type(self)(f(self))
        return self

class Functor(ABC, Generic[A]):
    @abstractmethod
    def map(self, f: MapFunction[A, B]) -> Functor[B]: ...

class DefaultFunctor(Generic[A]):
    def map(self, f: MapFunction[A, B]) -> DefaultFunctor[B]:
        self = type(self)(f(x) for x in self)
        return self
    
class DefaultFunctorDict(Generic[A]):
    def map(self, f: DictMapFunction[K,V, K_1,V_1]) -> DefaultFunctorDict[K_1, V_1]:
        self = type(self)({f(k,v) for k,v in self.items()})
        return self

class Applicative(Functor, ABC, Generic[A]):
    @abstractclassmethod
    def of(cls, *xs) -> Applicative[A]: ... # pure

class DefaultApplicative(EnhancedContainer, Functor): ...


# Concrete Functors ===================================================== #

class FList(List[A], DefaultFunctor): ...

class FTuple(Tuple[A], DefaultFunctor): ...

class FSet(Set[A], DefaultFunctor): ...

class FDeque(Deque[A], DefaultFunctor): ...
    
class FDict(Dict[K,V], DefaultFunctorDict): ...

class FOrderedDict(OrderedDict[K,V], DefaultFunctorDict): ...

# Concrete Applicatives ================================================= #

class AList(FList[A], DefaultApplicative): ...

class ATuple(FTuple[A], DefaultApplicative): ...

class ASet(FSet[A], DefaultApplicative): ...

class ADeque(FDeque[A], DefaultApplicative): ...

# =

from functools import _initial_missing, wraps, reduce as foldl
from typing import Any, Iterable

def reverse(binary_operation: Callable[[A,B], Any]) -> Callable[[B,A], Any]:
    return wraps(binary_operation)(lambda a, b: binary_operation(b, a))

# foldr = foldl(reverse(binary_operation), sequence, initial)
def foldr(binary_operation: Callable[[A,B], B], sequence: Iterable, initial=_initial_missing) -> B:
    it = iter(sequence)

    if initial is _initial_missing:
        try:
            value = next(it)
        except StopIteration:
            raise TypeError(
                "foldr() of empty iterable with no initial value") from None
    else:
        value = initial

    for element in it:
        value = binary_operation(element, value)

    return value