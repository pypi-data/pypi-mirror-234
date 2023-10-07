# This file was automatically generated by SWIG (http://www.swig.org).
# Version 4.0.2
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError("Python 2.7 or later required")

# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _CorePythonSwig
else:
    import _CorePythonSwig

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "thisown":
            self.this.own(value)
        elif name == "this":
            set(self, name, value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


SHARED_PTR_DISOWN = _CorePythonSwig.SHARED_PTR_DISOWN
class SwigPyIterator(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _CorePythonSwig.delete_SwigPyIterator

    def value(self):
        return _CorePythonSwig.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _CorePythonSwig.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _CorePythonSwig.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _CorePythonSwig.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _CorePythonSwig.SwigPyIterator_equal(self, x)

    def copy(self):
        return _CorePythonSwig.SwigPyIterator_copy(self)

    def next(self):
        return _CorePythonSwig.SwigPyIterator_next(self)

    def __next__(self):
        return _CorePythonSwig.SwigPyIterator___next__(self)

    def previous(self):
        return _CorePythonSwig.SwigPyIterator_previous(self)

    def advance(self, n):
        return _CorePythonSwig.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _CorePythonSwig.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _CorePythonSwig.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _CorePythonSwig.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _CorePythonSwig.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _CorePythonSwig.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _CorePythonSwig.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _CorePythonSwig:
_CorePythonSwig.SwigPyIterator_swigregister(SwigPyIterator)

class Token(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr
    type = property(_CorePythonSwig.Token_type_get, _CorePythonSwig.Token_type_set)
    lexeme = property(_CorePythonSwig.Token_lexeme_get, _CorePythonSwig.Token_lexeme_set)
    line = property(_CorePythonSwig.Token_line_get, _CorePythonSwig.Token_line_set)
    column = property(_CorePythonSwig.Token_column_get, _CorePythonSwig.Token_column_set)

    def __init__(self, *args):
        _CorePythonSwig.Token_swiginit(self, _CorePythonSwig.new_Token(*args))

    @staticmethod
    def Uninitialized():
        return _CorePythonSwig.Token_Uninitialized()

    @staticmethod
    def Invalid():
        return _CorePythonSwig.Token_Invalid()

    @staticmethod
    def Identifier(lexeme):
        return _CorePythonSwig.Token_Identifier(lexeme)

    @staticmethod
    def _None():
        return _CorePythonSwig.Token__None()

    def __eq__(self, other):
        return _CorePythonSwig.Token___eq__(self, other)
    __swig_destroy__ = _CorePythonSwig.delete_Token

# Register Token in _CorePythonSwig:
_CorePythonSwig.Token_swigregister(Token)

def Token_Uninitialized():
    return _CorePythonSwig.Token_Uninitialized()

def Token_Invalid():
    return _CorePythonSwig.Token_Invalid()

def Token_Identifier(lexeme):
    return _CorePythonSwig.Token_Identifier(lexeme)

def Token__None():
    return _CorePythonSwig.Token__None()

NodeType_Document = _CorePythonSwig.NodeType_Document
NodeType_ModelDeclaration = _CorePythonSwig.NodeType_ModelDeclaration
NodeType_VarDeclaration = _CorePythonSwig.NodeType_VarDeclaration
NodeType_VarAssignment = _CorePythonSwig.NodeType_VarAssignment
NodeType_BinaryOp = _CorePythonSwig.NodeType_BinaryOp
NodeType_ModelInitializer = _CorePythonSwig.NodeType_ModelInitializer
NodeType_MethodDeclaration = _CorePythonSwig.NodeType_MethodDeclaration
NodeType_Parameter = _CorePythonSwig.NodeType_Parameter
NodeType_Array = _CorePythonSwig.NodeType_Array
NodeType_ArrayType = _CorePythonSwig.NodeType_ArrayType
NodeType_Constant = _CorePythonSwig.NodeType_Constant
NodeType_Call = _CorePythonSwig.NodeType_Call
NodeType_MemberAccess = _CorePythonSwig.NodeType_MemberAccess
NodeType_PrimitiveType = _CorePythonSwig.NodeType_PrimitiveType
NodeType_Unary = _CorePythonSwig.NodeType_Unary
NodeType_Indexing = _CorePythonSwig.NodeType_Indexing
NodeType_OperatorOverload = _CorePythonSwig.NodeType_OperatorOverload
NodeType_Annotation = _CorePythonSwig.NodeType_Annotation
class Node(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr

    def getNodeType(self):
        return _CorePythonSwig.Node_getNodeType(self)

    def isValid(self):
        return _CorePythonSwig.Node_isValid(self)

    def setValid(self, valid):
        return _CorePythonSwig.Node_setValid(self, valid)

    def isDocument(self):
        return _CorePythonSwig.Node_isDocument(self)

    def isModelDeclaration(self):
        return _CorePythonSwig.Node_isModelDeclaration(self)

    def isVarDeclaration(self):
        return _CorePythonSwig.Node_isVarDeclaration(self)

    def isVarAssignment(self):
        return _CorePythonSwig.Node_isVarAssignment(self)

    def isMethodDeclaration(self):
        return _CorePythonSwig.Node_isMethodDeclaration(self)

    def isParameter(self):
        return _CorePythonSwig.Node_isParameter(self)

    def isConstant(self):
        return _CorePythonSwig.Node_isConstant(self)

    def isBinaryOp(self):
        return _CorePythonSwig.Node_isBinaryOp(self)

    def isModelInitializer(self):
        return _CorePythonSwig.Node_isModelInitializer(self)

    def isArray(self):
        return _CorePythonSwig.Node_isArray(self)

    def isArrayType(self):
        return _CorePythonSwig.Node_isArrayType(self)

    def isUnary(self):
        return _CorePythonSwig.Node_isUnary(self)

    def isMemberAccess(self):
        return _CorePythonSwig.Node_isMemberAccess(self)

    def isCall(self):
        return _CorePythonSwig.Node_isCall(self)

    def isPrimitiveType(self):
        return _CorePythonSwig.Node_isPrimitiveType(self)

    def isType(self):
        return _CorePythonSwig.Node_isType(self)

    def isIndexing(self):
        return _CorePythonSwig.Node_isIndexing(self)

    def isOperatorOverload(self):
        return _CorePythonSwig.Node_isOperatorOverload(self)

    def isAnnotation(self):
        return _CorePythonSwig.Node_isAnnotation(self)

    def asDocument(self):
        return _CorePythonSwig.Node_asDocument(self)

    def asModelDeclaration(self):
        return _CorePythonSwig.Node_asModelDeclaration(self)

    def asVarDeclaration(self):
        return _CorePythonSwig.Node_asVarDeclaration(self)

    def asVarAssignment(self):
        return _CorePythonSwig.Node_asVarAssignment(self)

    def asMethodDeclaration(self):
        return _CorePythonSwig.Node_asMethodDeclaration(self)

    def asParameter(self):
        return _CorePythonSwig.Node_asParameter(self)

    def asConstant(self):
        return _CorePythonSwig.Node_asConstant(self)

    def asBinaryOp(self):
        return _CorePythonSwig.Node_asBinaryOp(self)

    def asModelInitializer(self):
        return _CorePythonSwig.Node_asModelInitializer(self)

    def asUnary(self):
        return _CorePythonSwig.Node_asUnary(self)

    def asArray(self):
        return _CorePythonSwig.Node_asArray(self)

    def asArrayType(self):
        return _CorePythonSwig.Node_asArrayType(self)

    def asMemberAccess(self):
        return _CorePythonSwig.Node_asMemberAccess(self)

    def asCall(self):
        return _CorePythonSwig.Node_asCall(self)

    def asPrimitiveType(self):
        return _CorePythonSwig.Node_asPrimitiveType(self)

    def asType(self):
        return _CorePythonSwig.Node_asType(self)

    def asIndexing(self):
        return _CorePythonSwig.Node_asIndexing(self)

    def asOperatorOverload(self):
        return _CorePythonSwig.Node_asOperatorOverload(self)

    def asAnnotation(self):
        return _CorePythonSwig.Node_asAnnotation(self)

    def accept(self, visitor):
        return _CorePythonSwig.Node_accept(self, visitor)
    __swig_destroy__ = _CorePythonSwig.delete_Node

    @staticmethod
    def segmentsAsString(segments):
        return _CorePythonSwig.Node_segmentsAsString(segments)

# Register Node in _CorePythonSwig:
_CorePythonSwig.Node_swigregister(Node)

def Node_segmentsAsString(segments):
    return _CorePythonSwig.Node_segmentsAsString(segments)

class ModelDeclaration(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr

    @staticmethod
    def create(qualifier_token, name_token, parent_segments, annotations, members):
        return _CorePythonSwig.ModelDeclaration_create(qualifier_token, name_token, parent_segments, annotations, members)

    def asModelDeclaration(self):
        return _CorePythonSwig.ModelDeclaration_asModelDeclaration(self)

    def asType(self):
        return _CorePythonSwig.ModelDeclaration_asType(self)

    def accept(self, visitor):
        return _CorePythonSwig.ModelDeclaration_accept(self, visitor)

    def isAssignableTo(self, other):
        return _CorePythonSwig.ModelDeclaration_isAssignableTo(self, other)

    def toString(self):
        return _CorePythonSwig.ModelDeclaration_toString(self)

    def toKey(self):
        return _CorePythonSwig.ModelDeclaration_toKey(self)

    def getQualifierToken(self):
        return _CorePythonSwig.ModelDeclaration_getQualifierToken(self)

    def isConst(self):
        return _CorePythonSwig.ModelDeclaration_isConst(self)

    def getNameToken(self):
        return _CorePythonSwig.ModelDeclaration_getNameToken(self)

    def getName(self):
        return _CorePythonSwig.ModelDeclaration_getName(self)

    def getNameWithNamespace(self, separator):
        return _CorePythonSwig.ModelDeclaration_getNameWithNamespace(self, separator)

    def getNameWithNamespaceSkipFirst(self, separator):
        return _CorePythonSwig.ModelDeclaration_getNameWithNamespaceSkipFirst(self, separator)

    def extendsSegmentsAsString(self):
        return _CorePythonSwig.ModelDeclaration_extendsSegmentsAsString(self)

    def getExtendsSegments(self):
        return _CorePythonSwig.ModelDeclaration_getExtendsSegments(self)

    def getExtends(self):
        return _CorePythonSwig.ModelDeclaration_getExtends(self)

    def setExtends(self, extends):
        return _CorePythonSwig.ModelDeclaration_setExtends(self, extends)

    def appendToAnnotations(self, annotation):
        return _CorePythonSwig.ModelDeclaration_appendToAnnotations(self, annotation)

    def getAnnotations(self):
        return _CorePythonSwig.ModelDeclaration_getAnnotations(self)

    def findAnnotations(self, name):
        return _CorePythonSwig.ModelDeclaration_findAnnotations(self, name)

    def appendToMembers(self, member):
        return _CorePythonSwig.ModelDeclaration_appendToMembers(self, member)

    def getMembers(self):
        return _CorePythonSwig.ModelDeclaration_getMembers(self)

    def getOuterMembers(self):
        return _CorePythonSwig.ModelDeclaration_getOuterMembers(self)

    def removeMember(self, member):
        return _CorePythonSwig.ModelDeclaration_removeMember(self, member)

    def removeInvalidMembers(self):
        return _CorePythonSwig.ModelDeclaration_removeInvalidMembers(self)

    def findMembers(self, name):
        return _CorePythonSwig.ModelDeclaration_findMembers(self, name)

    def findFirstMemberOfType(self, name, type):
        return _CorePythonSwig.ModelDeclaration_findFirstMemberOfType(self, name, type)

    def findFirstMemberExcludeType(self, name, type):
        return _CorePythonSwig.ModelDeclaration_findFirstMemberExcludeType(self, name, type)

    def findFirstMember(self, name):
        return _CorePythonSwig.ModelDeclaration_findFirstMember(self, name)

    def countMembers(self):
        return _CorePythonSwig.ModelDeclaration_countMembers(self)

    def getOwningDocument(self):
        return _CorePythonSwig.ModelDeclaration_getOwningDocument(self)

    def setOwningDocument(self, owning_document):
        return _CorePythonSwig.ModelDeclaration_setOwningDocument(self, owning_document)

    def getSourceIdOrDefault(self):
        return _CorePythonSwig.ModelDeclaration_getSourceIdOrDefault(self)

    def getTopologicalSort(self):
        return _CorePythonSwig.ModelDeclaration_getTopologicalSort(self)

    def setTopologicalSort(self, topological_sort):
        return _CorePythonSwig.ModelDeclaration_setTopologicalSort(self, topological_sort)
    __swig_destroy__ = _CorePythonSwig.delete_ModelDeclaration

# Register ModelDeclaration in _CorePythonSwig:
_CorePythonSwig.ModelDeclaration_swigregister(ModelDeclaration)

def ModelDeclaration_create(qualifier_token, name_token, parent_segments, annotations, members):
    return _CorePythonSwig.ModelDeclaration_create(qualifier_token, name_token, parent_segments, annotations, members)

AnyType_Int = _CorePythonSwig.AnyType_Int
AnyType_Real = _CorePythonSwig.AnyType_Real
AnyType_Bool = _CorePythonSwig.AnyType_Bool
AnyType_String = _CorePythonSwig.AnyType_String
AnyType_Object = _CorePythonSwig.AnyType_Object
AnyType_Array = _CorePythonSwig.AnyType_Array
AnyType_Undefined = _CorePythonSwig.AnyType_Undefined
class Any(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        _CorePythonSwig.Any_swiginit(self, _CorePythonSwig.new_Any(*args))

    def __eq__(self, rhs):
        return _CorePythonSwig.Any___eq__(self, rhs)

    def __ne__(self, rhs):
        return _CorePythonSwig.Any___ne__(self, rhs)

    @staticmethod
    def fromString(value):
        return _CorePythonSwig.Any_fromString(value)

    @staticmethod
    def fromArray(value):
        return _CorePythonSwig.Any_fromArray(value)

    @staticmethod
    def fromObject(value):
        return _CorePythonSwig.Any_fromObject(value)

    def typeAsString(self):
        return _CorePythonSwig.Any_typeAsString(self)

    @staticmethod
    def typeToString(t):
        return _CorePythonSwig.Any_typeToString(t)

    def getType(self):
        return _CorePythonSwig.Any_getType(self)

    def isReal(self):
        return _CorePythonSwig.Any_isReal(self)

    def isInt(self):
        return _CorePythonSwig.Any_isInt(self)

    def isBool(self):
        return _CorePythonSwig.Any_isBool(self)

    def isString(self):
        return _CorePythonSwig.Any_isString(self)

    def isObject(self):
        return _CorePythonSwig.Any_isObject(self)

    def isArray(self):
        return _CorePythonSwig.Any_isArray(self)

    def isUndefined(self):
        return _CorePythonSwig.Any_isUndefined(self)

    def asReal(self):
        return _CorePythonSwig.Any_asReal(self)

    def asInt(self):
        return _CorePythonSwig.Any_asInt(self)

    def asBool(self):
        return _CorePythonSwig.Any_asBool(self)

    def asString(self):
        return _CorePythonSwig.Any_asString(self)

    def asObject(self):
        return _CorePythonSwig.Any_asObject(self)

    def asArray(self):
        return _CorePythonSwig.Any_asArray(self)
    __swig_destroy__ = _CorePythonSwig.delete_Any

# Register Any in _CorePythonSwig:
_CorePythonSwig.Any_swigregister(Any)

def Any_fromString(value):
    return _CorePythonSwig.Any_fromString(value)

def Any_fromArray(value):
    return _CorePythonSwig.Any_fromArray(value)

def Any_fromObject(value):
    return _CorePythonSwig.Any_fromObject(value)

def Any_typeToString(t):
    return _CorePythonSwig.Any_typeToString(t)

class Object(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        _CorePythonSwig.Object_swiginit(self, _CorePythonSwig.new_Object(*args))
    __swig_destroy__ = _CorePythonSwig.delete_Object

    def onInit(self):
        return _CorePythonSwig.Object_onInit(self)

    def setDynamic(self, key, value):
        return _CorePythonSwig.Object_setDynamic(self, key, value)

    def extractObjectFieldsTo(self, output):
        return _CorePythonSwig.Object_extractObjectFieldsTo(self, output)

    def extractEntriesTo(self, output):
        return _CorePythonSwig.Object_extractEntriesTo(self, output)

    def getDynamic(self, key):
        return _CorePythonSwig.Object_getDynamic(self, key)

    def callDynamic(self, key, args):
        return _CorePythonSwig.Object_callDynamic(self, key, args)

    def getName(self):
        return _CorePythonSwig.Object_getName(self)

    def triggerOnInit(self):
        return _CorePythonSwig.Object_triggerOnInit(self)

    def getType(self):
        return _CorePythonSwig.Object_getType(self)

    def getTypeList(self):
        return _CorePythonSwig.Object_getTypeList(self)

    def getOwner(self):
        return _CorePythonSwig.Object_getOwner(self)

# Register Object in _CorePythonSwig:
_CorePythonSwig.Object_swigregister(Object)

class EvaluatorContext(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def registerFactory(self, className, createMethod):
        return _CorePythonSwig.EvaluatorContext_registerFactory(self, className, createMethod)

    def registerStaticMethod(self, key, static_method):
        return _CorePythonSwig.EvaluatorContext_registerStaticMethod(self, key, static_method)

    def registerBinaryOperatorMethod(self, key, bin_op_method):
        return _CorePythonSwig.EvaluatorContext_registerBinaryOperatorMethod(self, key, bin_op_method)

    def registerUnaryOperatorMethod(self, key, unary_op_method):
        return _CorePythonSwig.EvaluatorContext_registerUnaryOperatorMethod(self, key, unary_op_method)

    def lookup(self, className):
        return _CorePythonSwig.EvaluatorContext_lookup(self, className)

    def callStaticMethod(self, key, args):
        return _CorePythonSwig.EvaluatorContext_callStaticMethod(self, key, args)

    def callBinaryOperator(self, key, lhs, rhs):
        return _CorePythonSwig.EvaluatorContext_callBinaryOperator(self, key, lhs, rhs)

    def callUnaryOperator(self, key, operand):
        return _CorePythonSwig.EvaluatorContext_callUnaryOperator(self, key, operand)

    def __init__(self):
        _CorePythonSwig.EvaluatorContext_swiginit(self, _CorePythonSwig.new_EvaluatorContext())
    __swig_destroy__ = _CorePythonSwig.delete_EvaluatorContext

# Register EvaluatorContext in _CorePythonSwig:
_CorePythonSwig.EvaluatorContext_swigregister(EvaluatorContext)

class TokenVector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def iterator(self):
        return _CorePythonSwig.TokenVector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _CorePythonSwig.TokenVector___nonzero__(self)

    def __bool__(self):
        return _CorePythonSwig.TokenVector___bool__(self)

    def __len__(self):
        return _CorePythonSwig.TokenVector___len__(self)

    def __getslice__(self, i, j):
        return _CorePythonSwig.TokenVector___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _CorePythonSwig.TokenVector___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _CorePythonSwig.TokenVector___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _CorePythonSwig.TokenVector___delitem__(self, *args)

    def __getitem__(self, *args):
        return _CorePythonSwig.TokenVector___getitem__(self, *args)

    def __setitem__(self, *args):
        return _CorePythonSwig.TokenVector___setitem__(self, *args)

    def pop(self):
        return _CorePythonSwig.TokenVector_pop(self)

    def append(self, x):
        return _CorePythonSwig.TokenVector_append(self, x)

    def empty(self):
        return _CorePythonSwig.TokenVector_empty(self)

    def size(self):
        return _CorePythonSwig.TokenVector_size(self)

    def swap(self, v):
        return _CorePythonSwig.TokenVector_swap(self, v)

    def begin(self):
        return _CorePythonSwig.TokenVector_begin(self)

    def end(self):
        return _CorePythonSwig.TokenVector_end(self)

    def rbegin(self):
        return _CorePythonSwig.TokenVector_rbegin(self)

    def rend(self):
        return _CorePythonSwig.TokenVector_rend(self)

    def clear(self):
        return _CorePythonSwig.TokenVector_clear(self)

    def get_allocator(self):
        return _CorePythonSwig.TokenVector_get_allocator(self)

    def pop_back(self):
        return _CorePythonSwig.TokenVector_pop_back(self)

    def erase(self, *args):
        return _CorePythonSwig.TokenVector_erase(self, *args)

    def __init__(self, *args):
        _CorePythonSwig.TokenVector_swiginit(self, _CorePythonSwig.new_TokenVector(*args))

    def push_back(self, x):
        return _CorePythonSwig.TokenVector_push_back(self, x)

    def front(self):
        return _CorePythonSwig.TokenVector_front(self)

    def back(self):
        return _CorePythonSwig.TokenVector_back(self)

    def assign(self, n, x):
        return _CorePythonSwig.TokenVector_assign(self, n, x)

    def resize(self, *args):
        return _CorePythonSwig.TokenVector_resize(self, *args)

    def insert(self, *args):
        return _CorePythonSwig.TokenVector_insert(self, *args)

    def reserve(self, n):
        return _CorePythonSwig.TokenVector_reserve(self, n)

    def capacity(self):
        return _CorePythonSwig.TokenVector_capacity(self)
    __swig_destroy__ = _CorePythonSwig.delete_TokenVector

# Register TokenVector in _CorePythonSwig:
_CorePythonSwig.TokenVector_swigregister(TokenVector)

class ObjectVector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def iterator(self):
        return _CorePythonSwig.ObjectVector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _CorePythonSwig.ObjectVector___nonzero__(self)

    def __bool__(self):
        return _CorePythonSwig.ObjectVector___bool__(self)

    def __len__(self):
        return _CorePythonSwig.ObjectVector___len__(self)

    def __getslice__(self, i, j):
        return _CorePythonSwig.ObjectVector___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _CorePythonSwig.ObjectVector___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _CorePythonSwig.ObjectVector___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _CorePythonSwig.ObjectVector___delitem__(self, *args)

    def __getitem__(self, *args):
        return _CorePythonSwig.ObjectVector___getitem__(self, *args)

    def __setitem__(self, *args):
        return _CorePythonSwig.ObjectVector___setitem__(self, *args)

    def pop(self):
        return _CorePythonSwig.ObjectVector_pop(self)

    def append(self, x):
        return _CorePythonSwig.ObjectVector_append(self, x)

    def empty(self):
        return _CorePythonSwig.ObjectVector_empty(self)

    def size(self):
        return _CorePythonSwig.ObjectVector_size(self)

    def swap(self, v):
        return _CorePythonSwig.ObjectVector_swap(self, v)

    def begin(self):
        return _CorePythonSwig.ObjectVector_begin(self)

    def end(self):
        return _CorePythonSwig.ObjectVector_end(self)

    def rbegin(self):
        return _CorePythonSwig.ObjectVector_rbegin(self)

    def rend(self):
        return _CorePythonSwig.ObjectVector_rend(self)

    def clear(self):
        return _CorePythonSwig.ObjectVector_clear(self)

    def get_allocator(self):
        return _CorePythonSwig.ObjectVector_get_allocator(self)

    def pop_back(self):
        return _CorePythonSwig.ObjectVector_pop_back(self)

    def erase(self, *args):
        return _CorePythonSwig.ObjectVector_erase(self, *args)

    def __init__(self, *args):
        _CorePythonSwig.ObjectVector_swiginit(self, _CorePythonSwig.new_ObjectVector(*args))

    def push_back(self, x):
        return _CorePythonSwig.ObjectVector_push_back(self, x)

    def front(self):
        return _CorePythonSwig.ObjectVector_front(self)

    def back(self):
        return _CorePythonSwig.ObjectVector_back(self)

    def assign(self, n, x):
        return _CorePythonSwig.ObjectVector_assign(self, n, x)

    def resize(self, *args):
        return _CorePythonSwig.ObjectVector_resize(self, *args)

    def insert(self, *args):
        return _CorePythonSwig.ObjectVector_insert(self, *args)

    def reserve(self, n):
        return _CorePythonSwig.ObjectVector_reserve(self, n)

    def capacity(self):
        return _CorePythonSwig.ObjectVector_capacity(self)
    __swig_destroy__ = _CorePythonSwig.delete_ObjectVector

# Register ObjectVector in _CorePythonSwig:
_CorePythonSwig.ObjectVector_swigregister(ObjectVector)

class AnyVector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def iterator(self):
        return _CorePythonSwig.AnyVector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _CorePythonSwig.AnyVector___nonzero__(self)

    def __bool__(self):
        return _CorePythonSwig.AnyVector___bool__(self)

    def __len__(self):
        return _CorePythonSwig.AnyVector___len__(self)

    def __getslice__(self, i, j):
        return _CorePythonSwig.AnyVector___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _CorePythonSwig.AnyVector___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _CorePythonSwig.AnyVector___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _CorePythonSwig.AnyVector___delitem__(self, *args)

    def __getitem__(self, *args):
        return _CorePythonSwig.AnyVector___getitem__(self, *args)

    def __setitem__(self, *args):
        return _CorePythonSwig.AnyVector___setitem__(self, *args)

    def pop(self):
        return _CorePythonSwig.AnyVector_pop(self)

    def append(self, x):
        return _CorePythonSwig.AnyVector_append(self, x)

    def empty(self):
        return _CorePythonSwig.AnyVector_empty(self)

    def size(self):
        return _CorePythonSwig.AnyVector_size(self)

    def swap(self, v):
        return _CorePythonSwig.AnyVector_swap(self, v)

    def begin(self):
        return _CorePythonSwig.AnyVector_begin(self)

    def end(self):
        return _CorePythonSwig.AnyVector_end(self)

    def rbegin(self):
        return _CorePythonSwig.AnyVector_rbegin(self)

    def rend(self):
        return _CorePythonSwig.AnyVector_rend(self)

    def clear(self):
        return _CorePythonSwig.AnyVector_clear(self)

    def get_allocator(self):
        return _CorePythonSwig.AnyVector_get_allocator(self)

    def pop_back(self):
        return _CorePythonSwig.AnyVector_pop_back(self)

    def erase(self, *args):
        return _CorePythonSwig.AnyVector_erase(self, *args)

    def __init__(self, *args):
        _CorePythonSwig.AnyVector_swiginit(self, _CorePythonSwig.new_AnyVector(*args))

    def push_back(self, x):
        return _CorePythonSwig.AnyVector_push_back(self, x)

    def front(self):
        return _CorePythonSwig.AnyVector_front(self)

    def back(self):
        return _CorePythonSwig.AnyVector_back(self)

    def assign(self, n, x):
        return _CorePythonSwig.AnyVector_assign(self, n, x)

    def resize(self, *args):
        return _CorePythonSwig.AnyVector_resize(self, *args)

    def insert(self, *args):
        return _CorePythonSwig.AnyVector_insert(self, *args)

    def reserve(self, n):
        return _CorePythonSwig.AnyVector_reserve(self, n)

    def capacity(self):
        return _CorePythonSwig.AnyVector_capacity(self)
    __swig_destroy__ = _CorePythonSwig.delete_AnyVector

# Register AnyVector in _CorePythonSwig:
_CorePythonSwig.AnyVector_swigregister(AnyVector)

class StringVector(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def iterator(self):
        return _CorePythonSwig.StringVector_iterator(self)
    def __iter__(self):
        return self.iterator()

    def __nonzero__(self):
        return _CorePythonSwig.StringVector___nonzero__(self)

    def __bool__(self):
        return _CorePythonSwig.StringVector___bool__(self)

    def __len__(self):
        return _CorePythonSwig.StringVector___len__(self)

    def __getslice__(self, i, j):
        return _CorePythonSwig.StringVector___getslice__(self, i, j)

    def __setslice__(self, *args):
        return _CorePythonSwig.StringVector___setslice__(self, *args)

    def __delslice__(self, i, j):
        return _CorePythonSwig.StringVector___delslice__(self, i, j)

    def __delitem__(self, *args):
        return _CorePythonSwig.StringVector___delitem__(self, *args)

    def __getitem__(self, *args):
        return _CorePythonSwig.StringVector___getitem__(self, *args)

    def __setitem__(self, *args):
        return _CorePythonSwig.StringVector___setitem__(self, *args)

    def pop(self):
        return _CorePythonSwig.StringVector_pop(self)

    def append(self, x):
        return _CorePythonSwig.StringVector_append(self, x)

    def empty(self):
        return _CorePythonSwig.StringVector_empty(self)

    def size(self):
        return _CorePythonSwig.StringVector_size(self)

    def swap(self, v):
        return _CorePythonSwig.StringVector_swap(self, v)

    def begin(self):
        return _CorePythonSwig.StringVector_begin(self)

    def end(self):
        return _CorePythonSwig.StringVector_end(self)

    def rbegin(self):
        return _CorePythonSwig.StringVector_rbegin(self)

    def rend(self):
        return _CorePythonSwig.StringVector_rend(self)

    def clear(self):
        return _CorePythonSwig.StringVector_clear(self)

    def get_allocator(self):
        return _CorePythonSwig.StringVector_get_allocator(self)

    def pop_back(self):
        return _CorePythonSwig.StringVector_pop_back(self)

    def erase(self, *args):
        return _CorePythonSwig.StringVector_erase(self, *args)

    def __init__(self, *args):
        _CorePythonSwig.StringVector_swiginit(self, _CorePythonSwig.new_StringVector(*args))

    def push_back(self, x):
        return _CorePythonSwig.StringVector_push_back(self, x)

    def front(self):
        return _CorePythonSwig.StringVector_front(self)

    def back(self):
        return _CorePythonSwig.StringVector_back(self)

    def assign(self, n, x):
        return _CorePythonSwig.StringVector_assign(self, n, x)

    def resize(self, *args):
        return _CorePythonSwig.StringVector_resize(self, *args)

    def insert(self, *args):
        return _CorePythonSwig.StringVector_insert(self, *args)

    def reserve(self, n):
        return _CorePythonSwig.StringVector_reserve(self, n)

    def capacity(self):
        return _CorePythonSwig.StringVector_capacity(self)
    __swig_destroy__ = _CorePythonSwig.delete_StringVector

# Register StringVector in _CorePythonSwig:
_CorePythonSwig.StringVector_swigregister(StringVector)



