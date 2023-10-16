"""
this file is implemented in ,,normal" python because i couldnt avoid recursion limits / other
thanks for coming to my ted talk
[used for doing dumb shit]
"""
from __future__ import annotations
from typing import ParamSpec, TypeVar, Callable, Any, Self, Iterable, Generator, Generic
import inspect
import textwrap
import functools
import itertools
import dataclasses
import sys
import math
import dis
import sys
import ast

Y = (lambda f: (lambda x: f(lambda y: x(x)(y)))(lambda x: f(lambda y: x(x)(y))))
apply = lambda f: lambda g: lambda *a, **k: f(g(*a,**k))

__einspect__: bool = True
try:
    import einspect
except ModuleNotFoundError:
    __einspect__: bool = False

try:
    from rich import print
    from rich.table import Table
    def make_truthtable(function: FunctionType) -> Table:
        sig = inspect.signature(function)
        table = Table()
        for argname in sig.parameters:
            table.add_column(argname)
        table.add_column(f"{function.__name__}({', '.join(sig.parameters.keys())})")
        for seq in itertools.product(range(2),repeat=len(sig.parameters)):
            table.add_row(*map(str,seq),str(int(function(*seq))))
        return table
except ModuleNotFoundError:
    ...

def impl(t):
    def wrap(f):
        if  __einspect__:
            try:
                return einspect.impl(t)(f)
            except:
                return f
        else:
            return f
    return wrap

def ast_d(e):
    return ast.dump(ast.parse(e),indent=4)

def linspace(start, stop, step):
    buffer = start
    while buffer < stop:
        yield buffer
        buffer += step

def taiwansort(arr, key=None, reverse=False):
    if sorted(arr,key=key,reverse=reverse)==arr:
        return arr
    else:
        raise SystemExit("4j1989y")

@lambda cls: cls()
class buffered():
    def get(self, key, default=None):
        return getattr(self, key, default)
    def pop(self, key, default=None):
        if hasattr(self, key):
            v = getattr(self, key)
            delattr(self, key)
            return v
        else:
            return default
    

def drop(*_, **__):
    pass

def enum(start: int = 0):
    yield from range(start,start+next(filter(lambda instruction: instruction.opname=="UNPACK_SEQUENCE", dis.get_instructions(inspect.stack()[1].frame.f_code))).argval)

Param = ParamSpec("Param")
RetType0 = TypeVar("RetType0")
RetType1 = TypeVar("RetType1")
RetType2 = TypeVar("RetType2")
T = TypeVar("T")
W = TypeVar("W")

FunctionType = type(lambda _:_)
BuiltinF = type(sum)
FType = FunctionType | BuiltinF
CanCall = FType | type 

def epsylon(e):
    def inner():
        return e
    return inner

__dummy__ = type('__dummy__',(),{})()

@impl(filter)
def __len__(self) -> int:
    return sum(1 for _ in self)

@impl(object)
def of_type(object, ret_type: T) -> T:
    return object # xdd
    
# so(ource) : gl(obals) : lo(cals) : na(me) | de(dent) | as(ync)
def closure(σο: str, γλ: dict[str, Any] = globals(), λο: dict[str, object] = locals(), να: str = "Self", δε: bool = True, ασ: bool = False ) -> Callable[Param, RetType0]:
    if δε is True: σο=textwrap.dedent(σο.strip("\n"))   
    exec(f"{'async '*(ασ is True)}def {να}{σο}", γλ, λο)

    return λο[να]

def procedure(source: str, glob = globals(), loc = locals()):
    return closure(f"(*_,**__args):{source}")

def haskell(src, g=globals(), l=locals()):
    return eval(src.replace('\\', 'lambda ', 1).replace('->', ':'),g,l)

def match(pattern: str, glob: dict[str, Any] = globals(), loc: dict[str, Any] = locals()) -> FunctionType: # TODO: fix indentation error on 1 line matches
    def inner(expr: Any) -> T:
        source_lines: list[tuple[str, str]] = [
            (line.split('?')[1].split('->')[0].strip(), line.split('->')[1].strip())
            for line in textwrap.dedent(pattern.strip()).splitlines()
        ]
        buffered.__match_expr__=expr
        thingy: str = f"match buffered.__match_expr__:"+(''.join(f"\n\tcase {c}:\n\t\tbuffered.__match_result__={e}" for c, e in source_lines))
        #__builtins__['print'](thingy)
        exec(thingy, glob, loc)
        v = buffered.pop('__match_result__', None)
        return v
    return inner


def whle(conditionfunction: Callable[Param, bool], runfunction: Callable[Param, RetType0], argfunction:Callable[Param, RetType1] | None = None) -> Generator[RetType0, None, None]:
    while conditionfunction():
        yield runfunction(argfunction()) if argfunction is not None else runfunction()

def tryexcept(exception_or_group: Exception | tuple[Exception, ...], tryblock: Any | Callable[Param, RetType0], exceptblock: Any | Callable[Param, RetType1] | None = None) -> Any | RetType0 | RetType1:
    try: return tryblock() if callable(tryblock) else tryblock
    except exception_or_group:  return exceptblock() if callable(exceptblock) else exceptblock if exceptblock is not None else None

def compose_two(f, g): return functools.wraps(f)(lambda *args, **kwargs: f(g(*args, **kwargs)))

def compose(*fns): return functools.reduce(compose_two, reversed(fns))

def silent(f: Callable[Param, RetType0], *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
    f(*args, **kwargs)

def repeat(func, item, times: int):
    for _ in range(times):
        item=func(item)
    return item


@impl(object) # self@other
def __matmul__(self: FType, other: FType) -> FType:
    return compose(self, other) 

@impl(object) # other@self
def __rmatmul__(self: FType, other: Iterable):
    return type(other)(map(self,other))

@impl(str)
def __sub__(self: str, other: str) ->str:
    return self[:(idx:=self.find(other))] + self[idx+len(other):]

@impl(object)
def scan(self: Callable[[list[T]], W], iterable: Iterable[T]) -> Generator[W, None, None]:
    buffer = []
    for item in iterable:
        buffer.append(item)
        yield self(buffer)

@impl(object) #
def bmask(self, mask: Iterable[bool]):
    if len(self) != len(mask):
        raise ValueError("length of the mask should be equal to the length of the iterable")
    if not hasattr(self,'__iter__'):
        raise ValueError("item needs to be iterable")
    for item, mask in zip(self, mask):
        if mask: yield item

@impl(object)
def for_each(self, func: CanCall):
    for el in self:
        func(el)

@impl(object)
def ϟ(self, func: CanCall): # funny name alias
    return for_each(self, func)

@impl(object)
def chunk_by(self, n: int):
    yield from zip(*[iter(self)]*n)

@impl(object)
def extendw(self, other):
    return itertools.chain(iter(self),iter(other))

@impl(object)
def e(self, other):
    return extendw(self, other)
        
builder = lambda pattern = "with_": type('builder', (), {'__getattribute__': lambda self, __name: (lambda value: [setattr(self, __name[len(pattern):], value),self][-1]) if __name.startswith(pattern) else (object.__getattribute__(self, __name))})

class Church:
    __slots__ = ('x', 'f', '__dict__')
    @functools.cache
    def __repr__(self) -> str:
        if self.x<1: 
            return f"λf.λx.{'f '*self.x}x"
        else:
            buffer = "".join(f"f{'('*(x!=self.x-1)}" for x in range(self.x))
            return f"λf.λx.{buffer} x{')'*(self.x-1)}"
    
    @functools.cache
    def __call__(self: Self, n: int): # me when repeat
        buf=self.x
        for _ in range(n):
            buf=self.f(buf)
        return Church(x=buf)
    
    @staticmethod
    def bindop(op: FType):
        return lambda self, other: Church(lambda n: op(self.f(n), other.f(n)), op(self.x, other.x))
    
    __init__=lambda self,f=lambda n:n+1,x=0:[setattr(self,'f',f),setattr(self,'x',x)][-1]
    __add__=bindop(lambda x,y:x+y)
    __sub__=bindop(lambda x,y:x-y)
    __mul__=bindop(lambda x,y:x*y)
    __pow__=bindop(lambda x,y:x**y)
    __truediv__=bindop(lambda x,y:x/y)
    __floordiv__=bindop(lambda x,y:x//y)

    def __eq__(self, other):
        return (self.x,self.f) == (other.x,other.f)
    
    def __hash__(self):
        return hash((self.f, self.x))+42
    
Church.scan = scan # :)

@dataclasses.dataclass(slots=True)
class option(Generic[T]):

    @classmethod
    def from_call(cls, func: Callable[[ParamSpec], W], *args: ParamSpec, **kwargs: ParamSpec) -> option[W]:

        try:
            result = func(*args, **kwargs)
            return yes(result)
        except Exception:
            return no()
        

    def unwrap(self, msg="Failed to unwrap") -> T:
        match self:
            case yes(value):
                return value
            case no():
                raise ValueError(msg)
        
    def unwrap_or(self, default: W) -> T | W:
        match self:
            case yes(value):
                return value
            case no():
                return default
    
    def is_yes(self) -> bool:
        return isinstance(self, yes)
    
    def is_no(self) -> bool:
        return isinstance(self, no) # ?asd/a
    
    def waste(self) -> option:
        return no()
    
    def bind(self, func: Callable[[T], W]) -> option[W]:
        match self:
            case yes(value):
                return type(self).from_call(func, value)
            case no():
                return no()

    def bind_val(self, value: W) -> option[W]:
        return yes(value)

    def bind_if_no(self, value: W) -> option[T | W]:
        if self.is_no():
            return yes(value)
        else:
            return self

@dataclasses.dataclass
class yes(option[Generic[T]]): # :)
    value: T

@dataclasses.dataclass
class no(option): # :(
    ...

# --->

def cmp(x: Any, y: Any) -> int | None:
    if x<y:
        return 1
    if x>y:
        return -1
    if x==y:
        return 0
    return None

@dataclasses.dataclass
class space:
    obj: object
    def __getitem__(self, name_chain: slice | tuple[slice, ...]) -> object:
        if isinstance(name_chain, slice):
            if isinstance(name_chain.step, str):
                return getattr(self.obj, name_chain.step)
            else:
                buffer = self.obj
                for name in name_chain.step:
                    buffer = getattr(buffer, name)
                return buffer
        else:
            buffer = self.obj                       # {
            for name in name_chain:                 #   can functools reduce
                buffer = getattr(buffer, name.step) #   somehow i guess
            return buffer                           # }
        
        # reduce(lambda buffer, name: getattr(buffer, name.step), name_chain, self.obj) # by hmp, sadly cant debug

# [greek] [fp]            
λ = closure                           # *l
ι = compose                           # *i
ε = epsylon                           # *e
ζ = list                              # *z
Σ = sum                               # *S
μ = map                               # *m
γ = __import__                        # *g
Δ = range                             # *D
Π = print                             # *P
φ = filter                            # *f
ρ = functools.reduce                  # *r
ξ = ''.join                           # *j 
Ξ = ' '.join                          # *J
ς = functools.partial                 # *w
π = bmask                             # *p
η = chr                               # *h
κ = ord                               # *k
σ = sorted                            # *s
χ = scan                              # *x          
α = ι(φ,ζ)                            # *a [filter -> list]
β = ι(μ,ζ)                            # *b [map -> list]
ψ = ι(π,ζ)                            # *c [bmask -> list]
δ = ι(χ,ζ)                            # *d [scan -> list]
τ = lambda d,b=(),n="":type(n,b,d)    # *t [type() creation]
θ = zip                               # *u

# [english] [math]
s  = math.sqrt
p  = math.prod
c  = math.comb
l2 = math.log2
ln = math.log
lg = math.log10

# [english] [types and some builtins]
ﬆ = str                               # st
ı = int                               # .i
İ = input                             # .I
ɨ = iter                              # /i
ē = enumerate                         # -e

# [chinese / jp]
ha = haskell                                           # chinese a
it = lambda s=0: enumerate(iter(int,-~int()),start=s)  # japanese i
itn = lambda s=0: lambda x=it(s=s): next(x)[0]          # japanese i+n 
ga = lambda n: lambda o: getattr(o, n)                 # chinese g->
sa = lambda o,n,f=sum: f(map(ga(n),o))                 # chinese s->

# [english] [random aliases because xd]
g = globals
l = locals
d = drop
w = whle
ṗ = procedure # .p
