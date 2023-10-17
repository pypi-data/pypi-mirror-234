import inspect
import json
from warnings import warn
from six.moves import cStringIO
import sys
import ast

from .dolphindb_lexical import dolphindb_function_name_set

def parse_py_code_to_dolphindb_code(input, isfile=False):
    """
    parse python code to dolphindb code
    code may contain part of python base function, some numpy or pandas function
    :param input: input maybe source code file, code str, fucntion name
    :param isfile: if input is file, isfile must be set to True, or it will be process as code str
    :return: str the dolphidb code
    Example:
    1.input is source code
        >>> source = "lambda x : x+1"
        >>> parse_py_code_to_dolphindb_code(source)
    2.input is file
        >>> source = "code.py"
        >>> parse_py_code_to_dolphindb_code(source, isfile=True)
    3.input is function name. The code below must be in a code file
        def add(a, b):
            return a+b
        parse_py_code_to_dolphindb_code(add)
    """
    if isfile:
        f = open(input, "r")
        source = f.read()
        f.close()
    elif isinstance(input, str):
        source = input
    elif callable(input): 
        source = get_python_function_source(input)
    else:
        raise NotImplementedError("dolphindb parse does not support the input type!")
    tree = compile(source, "", "exec", ast.PyCF_ONLY_AST, dont_inherit=True)
    v = cStringIO()
    DolphindbParser(tree, file=v)
    return v.getvalue()

def get_python_function_source(functionName):
    """
    get python function source code by function name.
    This function can process the function defined in other function that with
    :param functionName:
    :return: str type source code
    """
    result = inspect.getsourcelines(functionName)
    source_lines = result[0]
    if not source_lines:
        return ""
    whitespaceNum = len(source_lines[0]) - len(source_lines[0].lstrip())
    if 0 == whitespaceNum:
        return inspect.getsource(functionName)
    source = ""
    for str in source_lines:
        if len(str) - len(str.lstrip()) >= whitespaceNum:
            source += str[whitespaceNum:]
        else:
            source += str
    return source
# Large float and imaginary literals get turned into infinities in the AST.
# We unparse those infinities to INFSTR.
INFSTR = "1e" + repr(sys.float_info.max_10_exp + 1)


def interleave(inter, f, seq):
    """Call f on each item in seq, calling inter() in between.
    """
    seq = iter(seq)
    try:
        f(next(seq))
    except StopIteration:
        pass
    else:
        for x in seq:
            inter()
            f(x)


class DolphindbParser:
    """Methods in this class recursively traverse an AST and
    output source code for the abstract syntax; original formatting
    is disregarded. """

    def __init__(self, tree, file=sys.stdout):
        """Unparser(tree, file=sys.stdout) -> None.
         Print the source for tree to file."""
        self.pre_name = ""
        self._numpy_name = {"numpy", }
        # numpy function called by numpy.(or by other numpy alias name)
        self._numpy_lib_flag = False
        self._name_module_flag = False
        self._pandas_name = {"pandas", }
        self._pandas_lib_flag = False
        self._pd_struct_init_flag = False
        self.f = file
        self._indent = 0
        self.dispatch(tree)
        print("", file=self.f)
        self.f.flush()

    def fill(self, text=""):
        "Indent a piece of text, according to the current indentation level"
        self.f.write("\n" + "    " * self._indent + text)

    def write(self, text):
        "Append a piece of text to the current line."
        self.f.write(text)

    def enter(self):
        "Print ':', and increase the indentation."
        self.write("{")
        self._indent += 1

    def leave(self):
        "Decrease the indentation level."
        self._indent -= 1
        self.f.write("\n" + "    " * self._indent + "}")

    def dispatch(self, tree):
        "Dispatcher function, dispatching tree type T to method _T."
        self._name_module_flag = False
        if isinstance(tree, list):
            for t in tree:
                self.dispatch(t)
            return
        meth = getattr(self, "_" + tree.__class__.__name__)
        meth(tree)

    ############### Unparsing methods ######################
    # There should be one method per concrete grammar type #
    # Constructors should be grouped by sum type. Ideally, #
    # this would follow the order in the grammar, but      #
    # currently doesn't.                                   #
    ########################################################

    def _Module(self, tree):
        for stmt in tree.body:
            self.dispatch(stmt)

    def _Interactive(self, tree):
        for stmt in tree.body:
            self.dispatch(stmt)

    def _Expression(self, tree):
        self.dispatch(tree.body)

    # stmt
    def _Expr(self, tree):
        self.fill()
        self.dispatch(tree.value)

    def _NamedExpr(self, tree):
        self.write("(")
        self.dispatch(tree.target)
        self.write(" := ")
        self.dispatch(tree.value)
        self.write(")")

    def _Import(self, t):
        """
        when python convert to dolphindb, we should tranverse some numpy and pandas fuction  to dolphindb function
        """
        interleave(lambda: self.write(", "), self.dispatch, t.names)

    def _ImportFrom(self, t):
        """
        from * import *
        we should process the "from numpy import add as ad", to process function convert
        """
        interleave(lambda: self.write(""), self.dispatch, t.names)

    def _Assign(self, t):
        """
        a = 5, keep the same but the type Y = [ [ int(x1+x2 < 1) ] for (x1, x2) in X ]
        may be we can support this in future
        """
        self.fill()
        for target in t.targets:
            self.dispatch(target)
            self.write(" = ")
        self.dispatch(t.value)

    def _AugAssign(self, t):
        """
        a += 5, keep the same
        """
        self.fill()
        self.dispatch(t.target)
        self.write(" " + self.binop[t.op.__class__.__name__] + "= ")
        self.dispatch(t.value)

    def _AnnAssign(self, t):
        self.fill()
        if not t.simple and isinstance(t.target, ast.Name):
            self.write('(')
        self.dispatch(t.target)
        if not t.simple and isinstance(t.target, ast.Name):
            self.write(')')
        self.write(": ")
        self.dispatch(t.annotation)
        if t.value:
            self.write(" = ")
            self.dispatch(t.value)

    def _Return(self, t):
        """
        dolphindb support multi return, so we can just use the return statement
        """
        self.fill("return")
        if t.value:
            self.write(" ")
            self.dispatch(t.value)

    def _Pass(self, t):
        """
        pass
        dolphindb support the empty function. do nothing.
        """
        pass

    def _Break(self, t):
        self.fill("break")

    def _Continue(self, t):
        self.fill("continue")

    def _Delete(self, t):
        """
        del
        dolphindb do not support the del with undef.
        """
        self.fill("undef `")
        interleave(lambda: self.write(", `"), self.dispatch, t.targets)

    def _Assert(self, t):
        """
        assert
        dolphindb support assert. but this is for test.
        """
        pass

    def _Exec(self, t):
        """
        exec
        this is for python 2.x, so ignore it.
        """
        raise NotImplementedError("dolphindb does not support exec function!")

    def _Print(self, t):
        """
        print
        this is for python 2.x
        """
        self.fill("print ")
        do_comma = False
        if t.dest:
            self.write(">>")
            self.dispatch(t.dest)
            do_comma = True
        for e in t.values:
            if do_comma:
                self.write(", ")
            else:
                do_comma = True
            self.dispatch(e)
        if not t.nl:
            self.write(",")

    def _Global(self, t):
        """
        del
        dolphindb do not support the del function. do nothing.
        """
        raise NotImplementedError("dolphindb does not support global variable!")

    def _Nonlocal(self, t):
        """
        del
        dolphindb do not support the nolocal. do nothing.
        """
        raise NotImplementedError("dolphindb does not support nolocal!")

    def _Await(self, t):
        """
        del
        dolphindb do not support the del function. do nothing.
        """
        raise NotImplementedError("dolphindb does not support await function!")

    def _Yield(self, t):
        raise NotImplementedError("dolphindb does not support yield function!")

    def _YieldFrom(self, t):
        raise NotImplementedError("dolphindb does not support yield from function!")

    def _Raise(self, t):
        self.fill("throw")
        if not t.exc:
            assert not t.cause
            return
        self.write(" ")
        self.dispatch(t.exc)
        if t.cause:
            # dolphindb do not support raise from
            print("WARNNING: dolphindb do not support raise from")

    def _Try(self, t):
        self.fill("try")
        self.enter()
        self.dispatch(t.body)
        self.leave()
        for ex in t.handlers:
            self.dispatch(ex)
        if t.orelse:
            raise NotImplementedError("dolphindb does not support try...else!")
        if t.finalbody:
            raise NotImplementedError("dolphindb does not support try...finally!")

    def _TryExcept(self, t):
        self.fill("try")
        self.enter()
        self.dispatch(t.body)
        self.leave()

        for ex in t.handlers:
            self.dispatch(ex)
        if t.orelse:
            raise NotImplementedError("dolphindb does not support try...else!")

    def _TryFinally(self, t):
        raise NotImplementedError("dolphindb does not support try...finally!")

    def _ExceptHandler(self, t):
        self.fill("catch(")
        # dolphindb do not support exception type
        if t.name:
            self.write(t.name)
        else:
            self.write("ex")
        self.write(")")

        self.enter()
        self.dispatch(t.body)
        self.leave()

    def _ClassDef(self, t):
        raise NotImplementedError("dolphindb does not support class type!")

    def _FunctionDef(self, t):
        self.__FunctionDef_helper(t, "def")

    def _AsyncFunctionDef(self, t):
        raise NotImplementedError("dolphindb does not support async def!")

    def __FunctionDef_helper(self, t, fill_suffix):
        self.write("\n")
        for deco in t.decorator_list:
            raise NotImplementedError("dolphindb does not support decorator!")
        if t.name in dolphindb_function_name_set:
            raise NotImplementedError("dolphindb does not allowed to overwrite existing built-in functions ", t.name)

        def_str = fill_suffix + " " + t.name + "("
        self.fill(def_str)
        self.dispatch(t.args)
        self.write(")")
        if getattr(t, "returns", False):
            raise NotImplementedError("dolphindb does not support -> for return!")

        self.enter()
        self.dispatch(t.body)
        self.leave()

    def _For(self, t):
        self.__For_helper("for ", t)

    def _AsyncFor(self, t):
        raise NotImplementedError("dolphindb does not support async for!")

    def __For_helper(self, fill, t):
        self.fill(fill)
        self.write(" ( ")
        self.dispatch(t.target)
        self.write(" in ")
        self.dispatch(t.iter)
        self.write(" ) ")
        self.enter()
        self.dispatch(t.body)
        self.leave()
        if t.orelse:
            raise NotImplementedError("dolphindb does not support for else!")

    def _test_condition(self, test):
        self.write(" ( ")
        self.dispatch(test)
        self.write(" ) ")

    def _If(self, t):
        self.fill("if ")
        self.write('(')
        self.dispatch(t.test)
        self.write(')')
        self.enter()
        self.dispatch(t.body)
        self.leave()
        # collapse nested ifs into equivalent elifs.
        while (t.orelse and len(t.orelse) == 1 and
               isinstance(t.orelse[0], ast.If)):
            t = t.orelse[0]
            self.fill("else if ")
            self._test_condition(t.test)
            self.enter()
            self.dispatch(t.body)
            self.leave()
        # final else
        if t.orelse:
            self.fill("else")
            self.enter()
            self.dispatch(t.orelse)
            self.leave()

    def _While(self, t):
        self.fill("do")
        self.enter()
        self.fill("if(!")
        self._test_condition(t.test)
        self.write("){\n\t\t\tbreak\n\t\t}\n")
        self.dispatch(t.body)
        self.leave()
        self.write("while ")
        self._test_condition(t.test)
        if t.orelse:
            self.fill("if(!")
            self._test_condition(t.test)
            self.write(")")
            self.enter()
            self.dispatch(t.orelse)
            self.leave()

    def _generic_With(self, t, async_=False):
        raise NotImplementedError("dolphindb does not support for with!")

    def _With(self, t):
        self._generic_With(t)

    def _AsyncWith(self, t):
        self._generic_With(t, async_=True)

    # expr
    def _Bytes(self, t):
        self.write(repr(t.s))

    def _Str(self, tree):
        if len(tree.s) > 0:
            self.write(json.dumps(tree.s))
        else:
            self.write('""')

    def _JoinedStr(self, t):
        raise NotImplementedError("dolphindb can not  convert joined str !")

    def _FormattedValue(self, t):
        raise NotImplementedError("dolphindb can not  convert formatted value!")

    def _fstring_JoinedStr(self, t, write):
        raise NotImplementedError("dolphindb can not  convert joined str!")

    def _fstring_Str(self, t, write):
        raise NotImplementedError("dolphindb can not  convert joined str")

    def _fstring_Constant(self, t, write):
        raise NotImplementedError("dolphindb can not  convert formatted expression!")

    def _fstring_FormattedValue(self, t, write):
        raise NotImplementedError("dolphindb can not  convert formatted expression!")

    constant_dict = {
        'nan': 'NULL',
        'NAN': 'NULL',
        'NZERO': '0',
        'PZERO': '0',
    }

    def _Name(self, t):
        if t.id in self._numpy_name:
            self._numpy_lib_flag = True
            return
        attr = self.constant_dict.get(t.id)
        if attr:
            t.id = attr
        if t.id in self._pandas_name:
            self._pandas_lib_flag = True
            return
        self._name_module_flag = True
        # numpy or pandas function
        attr = self.numpy_pandas_to_dolphindb_dict.get(t.id)
        if attr:
            t.id = attr
        self.write(t.id)
        self.pre_name = t.id

    def _NameConstant(self, t):
        value = ""
        # if value is bool, change to lowercase
        if isinstance(t.value, bool):
            value = str(t.value).lower()
        else:
            value = repr(t.value)
        # process None to NULL
        if t.value is None:
            value = 'NULL'
        self.write(value)

    def _Repr(self, t):
        raise NotImplementedError("dolphindb does not support repr!")

    def _write_constant(self, value):
        if isinstance(value, (float, complex)):
            # Substitute overflowing decimal literal for AST infinities.
            self.write(repr(value).replace("inf", INFSTR))
        else:
            self.write(repr(value))

    def _Constant(self, t):
        value = t.value
        if isinstance(value, tuple):
            self.write("(")
            if len(value) == 1:
                self._write_constant(value[0])
                self.write(",")
            else:
                interleave(lambda: self.write(", "), self._write_constant, value)
            self.write(")")
        elif value is Ellipsis:  # instead of `...` for Py2 compatibility
            raise NotImplementedError("dolphindb does not support ellipsis value!")
        else:
            raise NotImplementedError("dolphindb does not support u kind value!")

    def _Num(self, t):
        repr_n = repr(t.n)
        self.write(repr_n.replace("inf", INFSTR))

    def _List(self, t):
        self.write("[")
        interleave(lambda: self.write(", "), self.dispatch, t.elts)
        self.write("]")

    def _ListComp(self, t):
        self.write("[")
        self.write("]\n")
        name = self.pre_name
        for gen in t.generators:
            self.dispatch(gen)
        self.write('\t')
        self.write(name)
        self.write('.append!(')
        self.dispatch(t.elt)
        self.write(")\n\t}\n}\n")

    def _GeneratorExp(self, t):
        raise NotImplementedError("dolphindb does not support generator!")

    def _SetComp(self, t):
        name = self.pre_name
        self.write("set([0])\n")
        self.write(name)
        self.write(".clear!()\n")
        for gen in t.generators:
            self.dispatch(gen)
        self.write('\t')
        self.write(name)
        self.write(".append(")
        self.dispatch(t.elt)
        self.write(")")
        self.write("\n}")

    def _DictComp(self, t):
        raise NotImplementedError("dolphindb does not support dict init by generator!")

    def _comprehension(self, t):
        if getattr(t, 'is_async', False):
            raise NotImplementedError("dolphindb does not support async!")
        else:
            self.write(" for(")
        self.dispatch(t.target)
        self.write(" in ")
        self.dispatch(t.iter)
        self.write("){\n")
        for if_clause in t.ifs:
            self.write(" if ")
            self.dispatch(if_clause)
            self.write("\n\t")

    def _IfExp(self, t):
        name = self.pre_name
        self.dispatch(t.body)
        self.write("\n")
        self.write(" if ")
        self.write("(!")
        self.dispatch(t.test)
        self.write("){\n\t")
        self.write(name)
        self.write(" = ")
        self.dispatch(t.orelse)
        self.write("\n}\n")

    def _Set(self, t):
        assert (t.elts)  # should be at least one element
        self.write("{")
        interleave(lambda: self.write(", "), self.dispatch, t.elts)
        self.write("}")

    def _Dict(self, t):
        def write_table_item(item):
            k, v = item
            self.dispatch(v)
            self.write(' as ')
            self.dispatch(k)

        if self._pd_struct_init_flag:
            interleave(lambda: self.write(", "), write_table_item, zip(t.keys, t.values))
            return

        self.write("dict(")

        def write_item(item):
            self.dispatch(item)

        self.write('[')
        interleave(lambda: self.write(", "), write_item, t.keys)
        self.write('],[')
        interleave(lambda: self.write(", "), write_item, t.values)
        self.write(']')
        self.write(")")

    def _Tuple(self, t):
        self.write("[")
        if len(t.elts) == 1:
            elt = t.elts[0]
            self.dispatch(elt)
            self.write(",")
        else:
            interleave(lambda: self.write(", "), self.dispatch, t.elts)
        self.write("]")

    unop = {"Invert": "!", "Not": "!", "UAdd": "+", "USub": "-"}

    def _UnaryOp(self, t):
        self.write("(")
        self.write(self.unop[t.op.__class__.__name__])
        self.write(" ")
        self.dispatch(t.operand)
        self.write(")")

    binop = {"Add": "+", "Sub": "-", "Mult": "*", "MatMult": "@", "Div": "\\", "Mod": "%",
             "LShift": "<<", "RShift": ">>", "BitOr": "|", "BitXor": "^", "BitAnd": "&",
             "FloorDiv": "/", "Pow": "pow"}

    def _BinOp(self, t):
        self.write("(")
        self.dispatch(t.left)
        self.write(" " + self.binop[t.op.__class__.__name__] + " ")
        self.dispatch(t.right)
        self.write(")")

    cmpops = {"Eq": "==", "NotEq": "!=", "Lt": "<", "LtE": "<=", "Gt": ">", "GtE": ">=",
              "Is": "==", "IsNot": "!=", "In": "in", "NotIn": "not in"}

    def _Compare(self, t):
        self.write("(")
        self.dispatch(t.left)
        for o, e in zip(t.ops, t.comparators):
            self.write(" " + self.cmpops[o.__class__.__name__] + " ")
            self.dispatch(e)
        self.write(")")

    boolops = {ast.And: 'and', ast.Or: 'or'}

    def _BoolOp(self, t):
        self.write("(")
        s = " %s " % self.boolops[t.op.__class__]
        interleave(lambda: self.write(s), self.dispatch, t.values)
        self.write(")")

    numpy_pandas_to_dolphindb_dict = {
        'pi': 'pi',
        'e': 'e',
        'nan': 'NULL',
        'NAN': 'NULL',
        'NZERO': '0',
        'PZERO': '0',
        'array': ' ',
        # operator by ndarray
        'bitwise_and': "bitAnd",
        'bitwise_or': "bitOr",
        'bitwise_not': "bitNot",
        'logical_xor': "bitXor",
        'isnull': "isNull",
        'notnull': "isNull",  # will add ! before the func
        'isna': "isNull",
        'notna': "isValid",
        # operator by np
        "subtract": "sub",
        "multiply": "mul",
        "divide": "ratio",
        "true_divide": "ratio",
        "negative": "neg",
        "power": "pow",
        "mod": "mod",
        "fmod": "mod",
        "left_shift": "lshift",
        "right_shift": "rshift",
        "absolute": "abs",
        "rint": "round",
        "bitwise_xor": "bitXor",
        "invert": "bitwise_not",
        "greater": "gt",
        "greater_equal": "ge",
        "less": "lt",
        "less_equal": "le",
        "not_equal": "ne",
        "equal": "eq",
        "logical_and": "and",
        "logical_or": "or",
        "logical_not": "invert",
        "floor_divide": "div",
        "amin": "min",
        "amax": "max",
        "min": "min",
        "max": "max",
        "quantile": "quantile",
        "median": "med",
        "mean": "mean",
        "std": "std",
        "var": "var",
        "nanquantile": "quantile",
        "nanmedian": "med",
        "nanmean": "mean",
        "nanstd": "std",
        "nanvar": "var",
        "corrcoef": "corr",
        "correlate": "corr",
        "maximum": "max",
        "minimum": "min",
        "fmax": "max",
        "fmin": "min",
        # stats operator
        'sin': "sin",
        'cos': "cos",
        'tan': "tan",
        'arcsin': "asin",
        'arccos': "acos",
        'arctan': "atan",
        'exp': "exp",
        'log': "log",
        'floor': "floor",
        'ceil': "ceil",
        'sqrt': "sqrt",
        'ffill': "ffill",
        'bfill': "bfill",
        'abs': "abs",
        'cumsum': "cumsum",
        'cummax': "cummax",
        'cummin': "cummin",
        'cumprod': "cumprod",
        'nancumsum': "cumsum",
        'nancummax': "cummax",
        'nancummin': "cummin",
        'nancumprod': "cumprod",
        'pct_change': "percentChange",
        'any': "any",
        'all': "all",
        'count': "count",
        'sum': "sum",
        'sum2': "sum2",
        'prod': "prod",
        'product': 'prod',
        'mean': "mean",
        'median': "median",
        'mode': "mode",
        'min': "min",
        'max': "max",
        'nanmin': "min",
        'nanmax': "max",
        'std': "std",
        'var': "var",
        'sem': "sem",
        'first': "first",
        'last': "last",
        'mad': "mad",
        'nunique': "nunique",
        'wavg': "wavg",
        'wsum': "wsum",
        'sinh': "sinh",
        'cosh': "cosh",
        'tanh': "tanh",
        'arcsinh': "arcsinh",
        'arccosh': "arccosh",
        'arctanh': "arctanh",
        'deg2rad': "deg2rad",
        'rad2deg': "rad2deg",
        'transpose': "transpose",
        'dot': 'dot',
        'sort': 'sort!',
        # pandas func
        'read_csv': 'ploadText',
        'groupby': 'groupby',
        'rename': 'rename!',
        'DataFrame': 'table',
        'Series': 'table',
        # python builtin functions
        'float': 'double',
        'str': 'string'
    }

    python_to_dolphindb_operator_dict = {
        '__neg__': 'neg',
        '__add__': "add",
        '__sub__': "sub",
        '__mul__': "mul",
        '__div__': "ratio",
        '__truediv__': "ratio",
        '__floordiv__': "div",
        '__mod__': "mod",
        '__pow__': "pow",
        '__lshift__': "lshift",
        '__rshift__': "rshift",
        # logical operator
        '__lt__': 'lt',
        '__gt__': 'gt',
        '__le__': 'le',
        '__ge__': 'ge',
        '__eq__': 'eq',
        '__ne__': 'ne',
        '__and__': "and",  # logical_and
        '__or__': "or",  # logical_or
        '__xor__': "bitXor",  # bitwise_xor
        '__invert__': "not",  # logical_not
        '__bool__': 'bool',
        'sort': 'sort!',
        '__len__': 'size',
        'diagonal': 'diag',
        'append': 'append!',
        'empty': 'size() == 0',
        # for pandas
        'div': 'ratio',
        'truediv': 'ratio',
        'floordiv': 'div',
        'divide': 'ratio',
        'multiply': 'mul',
        'product': 'prod',
        'pct_change': "percentChange",
        'subtract': 'sub',
        'isnull': 'isNull',
        'isna': 'isNull',
        'notna': 'isNull',
        'notnull': 'isNull',
        'hasnans': 'hasNull',
        'kurt': 'kurtosis',
    }

    unsupport_func = {
        'T', '__array__', '__array_finalize__', '__array_function__', '__array_interface__',
        '__array_prepare__', '__array_priority__', '__array_struct__', '__array_ufunc__',
        '__array_wrap__',
        '__class__', '__complex__', '__contains__', '__copy__', '__deepcopy__', '__delattr__',
        '__delitem__', '__dir__', '__divmod__', '__doc__', '__float__', '__format__',
        '__getattribute__', '__getitem__', '__hash__', '__iadd__', ', ', '__iand__', ', ',
        '__ifloordiv__', '__ilshift__', ', ', '__imatmul__', '__imod__', ', ', '__imul__', ', ',
        '__index__', '__init__', '__init_subclass__', ', ', '__int__', ',  ', '__ior__', '__ipow__',
        '__irshift__', '__isub__', '__iter__', '__itruediv__', '__ixor__',
        '__matmul__', '__new__', '__pos__', '__radd__',
        '__rand__', '__rdivmod__', '__reduce__', '__reduce_ex__', '__repr__',
        '__rfloordiv__', '__rmatmul__', '__rmod__', '__rmul__', '__ror__', '__rpow__',
        '__rrshift__', '__rsub__', '__rtruediv__',
        '__rxor__', '__setattr__', '__setitem__', '__setstate__', '__sizeof__', '__str__',
        '__subclasshook__', 'argmax', 'data', 'log10', 'log2', 'log1p'
                                                                'dtype', 'dump', 'dumps', 'flags', 'flat',
        'getfield', 'imag', 'item', 'itemset',
        'itemsize', 'nbytes', 'ndim', 'newbyteorder', 'nonzero', 'partition', 'ptp', 'put', 'ravel',
        'real', 'resize', 'searchsorted', 'setfield', 'setflags', 'squeeze',
        'strides', 'swapaxes', 'take', 'tobytes', 'tofile', 'tolist', 'tostring', 'trace', 'view',
        # for pandas
        'to_numpy', 'to_pandas', 'join', 'merge', 'merge_window',
        'drop', 'rename', 'add_prefix', 'add_suffix', 'agg', 'aggregate', 'align', 'apply', 'argmin',
        'argsort',
        'as_blocks', 'as_matrix', 'asfreq', 'asobject', 'asof', 'astype', 'at', 'at_time', 'autocorr',
        'axes', 'base', 'between', 'between_time', 'blocks', 'cat', 'clip', 'clip_lower', 'clip_upper',
        'combine', 'combine_first', 'compound', 'compress', 'copy', 'corr', 'cov', 'describe', 'diff',
        'divmod', 'drop_duplicates', 'droplevel', 'dropna', 'dt', 'dtypes', 'duplicated', 'ewm',
        'expanding', 'explode', 'factorize', 'fillna', 'filter', 'first_valid_index', 'from_array',
        'ftype', 'ftypes', 'get', 'get_dtype_counts', 'get_ftype_counts', 'get_value', 'get_values',
        'head', 'hist', 'iat', 'idxmax', 'idxmin', 'iloc', 'index', 'infer_objects',
        'is_copy', 'is_monotonic', 'is_monotonic_decreasing', 'is_monotonic_increasing',
        'is_unique', 'isin', 'items', 'iteritems', 'ix', 'keys', 'last_valid_index',
        'loc', 'map', 'mask', 'memory_usage', 'nlargest', 'nsmallest', 'pipe', 'plot', 'pop', 'radd',
        'rdiv', 'rdivmod', 'reindex', 'reindex_like', 'rename_axis', 'reorder_levels', 'repeat',
        'replace', 'resample', 'reset_index', 'rfloordiv', 'rmod', 'rmul', 'rolling',
        'rpow', 'rsub', 'rtruediv', 'set_axis', 'set_value', 'shift',
        'slice_shift', 'sort_index', 'sort_values', 'sparse', 'str', 'swaplevel', 'tail', 'to_clipboard',
        'to_csv', 'to_dense', 'to_dict', 'to_excel', 'to_frame', 'to_hdf', 'to_json', 'to_latex',
        'to_list', 'to_msgpack', 'to_period', 'to_pickle', 'to_sparse', 'to_sql', 'to_string',
        'to_timestamp',
        'to_xarray', 'transform', 'tshift', 'tz_convert', 'tz_localize', 'unique', 'unstack', 'update',
        'valid', 'value_counts', 'values', 'where', 'xs',
        # from pandas DataFrame
        'applymap', 'assign', 'boxplot', 'columns', 'corrwith', 'count', 'equals', 'eval', 'from_dict',
        'from_records', 'groupby', 'info', 'insert', 'iterrows', 'itertuples', 'lookup', 'melt',
        'nunique', 'pivot_table', 'query', 'select_dtypes', 'set_index', 'stack', 'style',
        'to_feather', 'to_gbq', 'to_html', 'to_parquet', 'to_records', 'to_stata', 'truncate',
    }
    invert_set = [
        'notna',
        'notnull'
    ]

    def _Attribute(self, t):
        if t.attr in self.invert_set:
            self.write('!')

        self.dispatch(t.value)
        if self._numpy_lib_flag or self._pandas_lib_flag:
            self._numpy_lib_flag = False
            self._pandas_lib_flag = False
            if t.attr == "DataFrame" or t.attr == "Series":
                self._pd_struct_init_flag = True
            attr = self.numpy_pandas_to_dolphindb_dict.get(t.attr)
            if attr:
                self.write(attr)
            else:
                raise NotImplementedError("dolphindb does not support function", t.attr)
            return

        # numpy imported, so should process x.sum etc.
        attr = self.python_to_dolphindb_operator_dict.get(t.attr)
        if attr:
            t.attr = attr
        if t.attr in self.unsupport_func:
            raise NotImplementedError("dolphindb does not support numpy function", t.attr)
        self.write(".")
        self.write(t.attr)
        if t.attr == 'shape':
            self.write('()')

    def _Call(self, t):
        func_id = getattr(t.func, "id", None)
        if func_id:
            attr = getattr(t.func, "attr", None)
            if attr == "DataFrame" or attr == "Series":
                self._pd_struct_init_flag = True
            if t.func.id == 'len':
                t.func.id = 'size'
            elif t.func.id == 'sorted':
                t.func.id = 'sort'
            elif t.func.id == 'sort':
                t.func.id = 'sort!'
            else:
                alias_func = self.alias_dict.get(func_id)
                if func_id in self.alias_set:
                    attr = self.numpy_pandas_to_dolphindb_dict.get(func_id)
                    if attr:
                        t.func.id = attr
                elif alias_func:
                    t.func.id = alias_func
            if t.func.id == "DataFrame" or t.func.id == "Series":
                self._pd_struct_init_flag = True
            # range does not contain the stop, but seq contains
            # elif t.func.id == 'range':
            #     t.func.id='seq'
        self.dispatch(t.func)
        self.write("(")
        comma = False
        for e in t.args:
            if comma:
                self.write(", ")
            else:
                comma = True
            self.dispatch(e)

        for e in t.keywords:
            if comma:
                self.write(", ")
            else:
                comma = True
            self.dispatch(e)
        if sys.version_info[:2] < (3, 5):
            if t.starargs:
                warn("dolphindb does not support *args!")
            if t.kwargs:
                warn("dolphindb does not support **kwargs!")
        self.write(")")
        # revert the init flag
        self._pd_struct_init_flag = False

    def _Subscript(self, t):
        self.dispatch(t.value)
        self.write("[")
        self.dispatch(t.slice)
        self.write("]")

    def _Starred(self, t):
        # self.write("*")
        raise NotImplementedError("dolphindb does not support operator Starred(...)!")

    # slice
    def _Ellipsis(self, t):
        # self.write("...")
        raise NotImplementedError("dolphindb does not support operator Ellipsis(...)!")

    def _Index(self, t):
        self.dispatch(t.value)

    def _Slice(self, t):
        if t.lower:
            self.dispatch(t.lower)
        self.write(":")
        if t.upper:
            self.dispatch(t.upper)
        if t.step:
            raise NotImplementedError("dolphindb does not support slice step!")

    def _ExtSlice(self, t):
        interleave(lambda: self.write(', '), self.dispatch, t.dims)

    # argument
    def _arg(self, t):
        self.write(t.arg)
        if t.annotation:
            raise NotImplementedError("dolphindb does not support operator annotation!")

    # others
    def _arguments(self, t):
        first = True
        # normal arguments
        all_args = getattr(t, 'posonlyargs', []) + t.args
        defaults = [None] * (len(all_args) - len(t.defaults)) + t.defaults
        for index, elements in enumerate(zip(all_args, defaults), 1):
            a, d = elements
            if first:
                first = False
            else:
                self.write(", ")
            self.dispatch(a)
            # quantile
            if d:
                raise NotImplementedError("dolphindb does not support key word argument!")
            if index == len(getattr(t, 'posonlyargs', ())):
                self.write(", /")

        # varargs, or bare '*' if no varargs but keyword-only arguments present
        if t.vararg or getattr(t, "kwonlyargs", False):
            raise NotImplementedError("dolphindb does not support argument *args!")

        # keyword-only arguments
        if getattr(t, "kwonlyargs", False):
            raise NotImplementedError("dolphindb does not support keyword argument!")

        # kwargs
        if t.kwarg:
            raise NotImplementedError("dolphindb does not support argument **kwargs!")

    def _keyword(self, t):
        self.write(t.arg)
        self.write("=")
        self.dispatch(t.value)

    def _Lambda(self, t):
        self.write("def (")
        self.dispatch(t.args)
        self.write(") :")
        self.dispatch(t.body)

    alias_dict = dict()
    alias_set = set()

    def _alias(self, t):
        if t.name == "numpy":
            if t.asname:
                self._numpy_name.add(t.asname)
                self._numpy_lib_import_flag = True
                # print(self._numpy_name)
        elif t.name == "pandas":
            if t.asname:
                self._pandas_name.add(t.asname)

        self.alias_set.add(t.name)
        if t.asname:
            self.alias_dict[t.asname] = t.name
        # print(self.alias_set)
        # print(self.alias_dict)

    def _withitem(self, t):
        raise NotImplementedError("dolphindb does not support with as!")
