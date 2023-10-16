import json
import math
import re
from math import inf
from numbers import Number
from typing import Optional

from .assumptions import builtins as functions
from .assumptions import keywords, keywords_not_reserved
from .errors import AqlError

# pylint: disable=too-many-lines


def _seems_arango_collection(obj):
	# Introspect the object to avoid having an external dependency.
	# Do not use hasattr() because it return always True
	# on others expressions, due to the wrapper for the
	# functions on the AQLBuilder.
	attrs = set(dir(obj))
	return "statuses" in attrs and "delete_index" in attrs and "name" in attrs


def flat_list(*args):
	vals = []
	for arg in args:
		if isinstance(arg, (list, tuple)):
			vals.extend(flat_list(*arg))
		else:
			vals.append(arg)
	return vals


def is_quoted_string(string):
	return string and len(string) >= 2 and string[0] == '"' and string[-1] == '"'


def wrap_aql(expr):
	if isinstance(expr, (_Operation, _ReturnExpression, _PartialStatement)):
		return f"({expr.to_aql()})"
	return expr.to_aql()


def is_valid_number(value):
	return isinstance(value, Number) and value != inf and value != -inf


def cast_number(number):
	if math.floor(number) == number:
		return IntegerLiteral(number)
	return NumberLiteral(number)


def cast_boolean(boolean):
	return BooleanLiteral(boolean)


def cast_string(string):
	if NumberLiteral.match(string):
		return auto_cast_token(float(string))
	if is_quoted_string(string):
		return StringLiteral(json.loads(string))
	match = RangeExpression.match(string)
	if match:
		return RangeExpression(match.group(1), match.group(2))
	if Identifier.match(string):
		return Identifier(string)
	return SimpleReference(string)


def cast_object(obj):
	if _seems_arango_collection(obj):
		return Identifier(obj.name)
	if isinstance(obj, list):
		return ListLiteral(obj)
	return ObjectLiteral(obj)


def auto_cast_token(token):
	if token is None:
		return NullLiteral(token)
	if isinstance(token, (_Expression, _PartialStatement)):
		return token
	if isinstance(token, bool):
		return cast_boolean(token)
	if isinstance(token, Number):
		return cast_number(token)
	if isinstance(token, str):
		return cast_string(token)
	if isinstance(token, (list, dict)) or _seems_arango_collection(token):
		return cast_object(token)
	raise AqlError(f"Invalid AQL value: ({type(token)}) {token}")


class _Definitions:

	__slots__ = ["_dfns"]

	def __init__(self, dfns):
		if isinstance(dfns, _Definitions):
			dfns = dfns._dfns
		if dfns is None or not isinstance(dfns, (list, dict)):
			raise AqlError("Expected definitions to be a list or a dict")
		self._dfns = []
		if isinstance(dfns, list):
			i = 0
			for dfn in dfns:
				if not isinstance(dfn, list) or len(dfn) != 2:
					raise AqlError(f"Expected definitions[{i}] to be a tuple")
				self._dfns.append([Identifier(dfn[0]), auto_cast_token(dfn[1])])
		else:
			for dfn_key, dfn_val in dfns.items():
				self._dfns.append([Identifier(dfn_key), auto_cast_token(dfn_val)])

	def to_aql(self):
		return ", ".join(
			[f"{dfn[0].to_aql()} = {wrap_aql(dfn[1])}" for dfn in self._dfns]
		)


class _Expression():
	_pattern: Optional[re.Pattern] = None

	def __getattribute__(self, name):
		return object.__getattribute__(self, name)

	def __getattr__(self, name):

		def wrapper(*args):
			return FunctionCall(name, *args)

		return wrapper

	@classmethod
	def match(cls, value):
		if cls._pattern:
			return cls._pattern.match(value)
		return None

	def range(self, max_):
		return RangeExpression(self, max_)

	def get(self, *keys):
		return PropertyAccess(self, keys)

	def and_(self, *values):
		return NAryOperation("&&", flat_list(self, values))

	def or_(self, *values):
		return NAryOperation("||", flat_list(self, values))

	def add(self, *values):
		return NAryOperation("+", flat_list(self, values))

	def plus(self, *values):
		return self.add(*values)

	def sub(self, *values):
		return NAryOperation("-", flat_list(self, values))

	def minus(self, *values):
		return self.sub(*values)

	def mul(self, *values):
		return NAryOperation("*", flat_list(self, values))

	def times(self, *values):
		return self.mul(*values)

	def div(self, *values):
		return NAryOperation("/", flat_list(self, values))

	def mod(self, *values):
		return NAryOperation("%", flat_list(self, values))

	def eq(self, value):  # pylint: disable=invalid-name
		return BinaryOperation("==", self, value)

	def gt(self, value):  # pylint: disable=invalid-name
		return BinaryOperation(">", self, value)

	def gte(self, value):
		return BinaryOperation(">=", self, value)

	def lt(self, value):  # pylint: disable=invalid-name
		return BinaryOperation("<", self, value)

	def lte(self, value):
		return BinaryOperation("<=", self, value)

	def neq(self, value):
		return BinaryOperation("!=", self, value)

	def not_(self):
		return UnaryOperation("!", self)

	def neg(self):
		return UnaryOperation("-", self)

	def in_(self, value):
		return BinaryOperation("in", self, value)

	def not_in(self, value):
		return BinaryOperation("not in", self, value)

	def then(self, value):
		return _PartialTernaryOperation("?", ":", self, value)


class _PartialTernaryOperation:

	__slots__ = ["_operator1", "_operator2", "_value1", "_value2"]

	def __init__(self, operator1, operator2, value1, value2):
		self._operator1 = operator1
		self._operator2 = operator2
		self._value1 = value1
		self._value2 = value2

	def else_(self, value):
		return TernaryOperation(
			self._operator1, self._operator2, self._value1, self._value2, value
		)

	def otherwise(self, value):
		return self.else_(value)


class Literal(_Expression):

	def __len__(self):
		if hasattr(self, "_value"):
			return len(self._value)
		return super().__len__()  # pragma: no cover


class NullLiteral(Literal):

	__slots__ = ["_value"]

	def __init__(self, value=None):
		super().__init__()
		if isinstance(value, NullLiteral):
			value = value._value
		if value is not None:
			raise AqlError(f"Expected value to be null: {repr(value)}")
		self._value = value

	def to_aql(self):
		return "null"


class BooleanLiteral(Literal):

	__slots__ = ["_value"]

	def __init__(self, value):
		super().__init__()
		if isinstance(value, BooleanLiteral):
			value = value._value
		self._value = bool(value)

	def to_aql(self):
		return str(self._value).lower()


class NumberLiteral(Literal):
	_pattern = re.compile(r"^[-+]?[0-9]+(\.[0-9]+)?$")

	__slots__ = ["_value"]

	def __init__(self, value):
		super().__init__()
		if isinstance(value, (NumberLiteral, IntegerLiteral)):
			value = value._value
		if not is_valid_number(value):
			raise AqlError(f"Expected value to be a finite number: {repr(value)}")
		self._value = float(value)

	def to_aql(self):
		return str(self._value)


class IntegerLiteral(Literal):

	__slots__ = ["_value"]

	def __init__(self, value):
		super().__init__()
		if isinstance(value, (NumberLiteral, IntegerLiteral)):
			value = value._value
		if not is_valid_number(value) or math.floor(value) != value:
			raise AqlError(f"Expected value to be a finite integer: {repr(value)}")
		self._value = int(value)

	def to_aql(self):
		return str(self._value)


class StringLiteral(Literal):

	__slots__ = ["_value"]

	def __init__(self, value):
		super().__init__()
		if isinstance(value, StringLiteral):
			value = value._value
		if hasattr(value, "to_aql"):
			value = value.to_aql()
		self._value = str(value)

	def to_aql(self):
		return json.dumps(self._value)


class ListLiteral(Literal):

	__slots__ = ["_value"]

	def __init__(self, value):
		super().__init__()
		if isinstance(value, ListLiteral):
			value = value._value
		if value is None or not isinstance(value, list):
			raise AqlError(f"Expected value to be an array: {repr(value)}")
		self._value = [auto_cast_token(val) for val in value]

	def to_aql(self):
		return f"[{', '.join([wrap_aql(val) for val in self._value])}]"


class ObjectLiteral(Literal):

	__slots__ = ["_value"]

	def __init__(self, value):
		super().__init__()
		if isinstance(value, ObjectLiteral):
			value = value._value
		if value is None or not isinstance(value, dict):
			raise AqlError(f"Expected value to be an object: {repr(value)}")
		self._value = {}
		for key, val in value.items():
			if not is_quoted_string(key) and not Identifier.match(key):
				try:
					if key != str(int(key)):
						key = json.dumps(key)
				except ValueError:
					pass
			self._value[key.replace('"', '\\"')] = auto_cast_token(val)

	def to_aql(self):
		# return '{%s}' % ', '.join(['"%s": %s' % (key, wrap_aql(val)) for key, val in self._value.items()])
		aql = ", ".join(
			[f'"{key}": {wrap_aql(val)}' for key, val in self._value.items()]
		)
		return f"{{{aql}}}"


class RawExpression(_Expression):

	__slots__ = ["_value"]

	def __init__(self, value):
		super().__init__()
		if isinstance(value, RawExpression):
			value = value._value
		self._value = value

	def to_aql(self):
		return str(self._value)


class RangeExpression(_Expression):
	_pattern = re.compile(r"^([0-9]+)\.\.([0-9]+)$")

	__slots__ = ["_begin", "_end"]

	def __init__(self, begin, end):
		super().__init__()
		self._begin = auto_cast_token(begin)
		self._end = auto_cast_token(end)

	def to_aql(self):
		return f"{wrap_aql(self._begin)}..{wrap_aql(self._end)}"


class PropertyAccess(_Expression):
	_pattern = re.compile(r"^[_a-z][_0-9a-z]*$")

	__slots__ = ["_obj", "_keys"]

	def __init__(self, obj, keys):
		super().__init__()
		self._obj = auto_cast_token(obj)
		self._keys = [auto_cast_token(key) for key in keys]

	def to_aql(self):
		keys = "".join([f"[{wrap_aql(val)}]" for val in self._keys])
		return f"{wrap_aql(self._obj)}{keys}"


class Keyword(_Expression):
	_pattern = re.compile(r"^[_a-z][_0-9a-z]*$", flags=re.RegexFlag.IGNORECASE)

	__slots__ = ["_value"]

	def __init__(self, value):
		super().__init__()
		if isinstance(value, Keyword):
			value = value._value
		if value is None or not isinstance(value, str):
			raise AqlError(f"Expected value to be a string: {repr(value)}")
		if not self.match(value):
			raise AqlError(f"Not a valid keyword: {value}")
		self._value = value

	def to_aql(self):
		return str(self._value).upper()


class Identifier(_Expression):
	_pattern = re.compile(r"^[_@a-z][-_@0-9a-z]*$", flags=re.RegexFlag.IGNORECASE)

	__slots__ = ["_value"]

	def __init__(self, value):
		super().__init__()
		if _seems_arango_collection(value):
			value = value.name
		if isinstance(value, Identifier):
			value = value._value
		if value is None or not isinstance(value, str):
			raise AqlError(f"Expected value to be a string: {repr(value)}")
		if not self.match(value):
			raise AqlError(f"Not a valid identifier: {value}")
		self._value = value

	def to_aql(self):
		value = str(self._value)
		valuelower = value.lower()
		if (valuelower in keywords or "-" in value) and \
				valuelower not in keywords_not_reserved:
			return f"`{value}`"
		return value


class SimpleReference(_Expression):
	_pattern = re.compile(
		r"^([_@a-z][-_@0-9a-z]*|`[_@a-z][-_@0-9a-z]*`)"
		r"(\.[_@a-z][-_@0-9a-z]*|\.`[_@a-z][-_@0-9a-z]*`|\[\*\])*$",
		flags=re.RegexFlag.IGNORECASE
	)

	__slots__ = ["_value"]

	def __init__(self, value):
		super().__init__()
		if _seems_arango_collection(value):
			value = value.name
		if isinstance(value, SimpleReference):
			value = value._value
		if value is None or not isinstance(value, str):
			raise AqlError(f"Expected value to be a string: {repr(value)}")
		if not self.match(value):
			raise AqlError(f"Not a valid simple reference: {value}")
		self._value = value

	def to_aql(self):
		value = str(self._value)
		return ".".join(
			[
				"`%s`" % token  # pylint: disable=consider-using-f-string
				if token[0] != "`" and (token.lower() in keywords or "-" in token)
				else token
				for token in value.split(".")
			]
		)


class _Operation(_Expression):

	__slots__ = ["_operator1"]

	def __init__(self, operator):
		super().__init__()
		if operator is None or not isinstance(operator, str):
			raise AqlError(f"Expected operator to be a string: {repr(operator)}")
		self._operator1 = operator


class UnaryOperation(_Operation):

	__slots__ = ["_value1"]

	def __init__(self, operator, value):
		super().__init__(operator)
		self._value1 = auto_cast_token(value)

	def to_aql(self):
		return f"{self._operator1}{wrap_aql(self._value1)}"


class BinaryOperation(UnaryOperation):

	__slots__ = ["_value2"]

	def __init__(self, operator, value1, value2):
		super().__init__(operator, value1)
		self._value2 = auto_cast_token(value2)

	def to_aql(self):
		return f"{wrap_aql(self._value1)} {self._operator1} {wrap_aql(self._value2)}"


class TernaryOperation(BinaryOperation):

	__slots__ = ["_operator2", "_value3"]

	def __init__(self, operator1, operator2, value1, value2, value3):
		super().__init__(operator1, value1, value2)
		if operator2 is None or not isinstance(operator2, str):
			raise AqlError(f"Expected operator 2 to be a string: {repr(operator2)}")
		self._operator2 = operator2
		self._value3 = auto_cast_token(value3)

	def to_aql(self):
		return "%s %s %s %s %s" % (# pylint: disable=consider-using-f-string
			wrap_aql(self._value1),
			self._operator1,
			wrap_aql(self._value2),
			self._operator2,
			wrap_aql(self._value3),
		)


class NAryOperation(_Operation):

	__slots__ = ["_values"]

	def __init__(self, operator, values):
		super().__init__(operator)
		self._values = [auto_cast_token(value) for value in values]

	def to_aql(self):
		return f" {self._operator1} ".join([wrap_aql(val) for val in self._values])


class FunctionCall(_Expression):
	_pattern = re.compile(r"^[_a-z][_0-9a-z]*(::[_a-z][_0-9a-z]*)*$", flags=re.RegexFlag.IGNORECASE)

	__slots__ = ["_function_name", "_args"]

	def __init__(self, function_name, *args):
		super().__init__()
		if function_name is None or not isinstance(function_name, str):
			raise AqlError("Expected function name to be a string: " + function_name)
		if not self.match(function_name):
			raise AqlError("Not a valid simple reference: " + function_name)
		if function_name not in functions:
			raise AqlError("Not a valid function: " + function_name)
		arg_def_len = functions[function_name]
		if isinstance(arg_def_len, list) and len(arg_def_len) == 1 and isinstance(arg_def_len[0], list):
			arg_def_len = arg_def_len[0]
		if isinstance(arg_def_len, int):
			arg_def_len = [arg_def_len]
		arg_def_len = flat_list(arg_def_len)
		arg_len = len(args)
		arg_len_min = min(arg_def_len)
		arg_len_max = max(arg_def_len)
		if arg_len < arg_len_min:
			raise AqlError("Not enough arguments: at least " + str(arg_len_min))
		if arg_len > arg_len_max:
			raise AqlError("Too many arguments: at most " + str(arg_len_max))
		self._function_name = function_name
		self._args = [auto_cast_token(token) for token in args] if args else []

	def to_aql(self):
		return f"{self._function_name}({', '.join([wrap_aql(arg) for arg in self._args])})"


class _ReturnExpression(_Expression):

	__slots__ = ["_prev", "_value", "_distinct"]

	def __init__(self, prev, value, distinct):
		super().__init__()
		self._prev = prev
		self._value = auto_cast_token(value)
		self._distinct = distinct

	def to_aql(self):
		aql = []
		if self._prev:
			aql.append(self._prev.to_aql())
		aql.append("RETURN")
		if self._distinct:
			aql.append("DISTINCT")
		aql.append(wrap_aql(self._value))
		return " ".join(aql)


class _PartialForExpression:

	__slots__ = ["_prev", "_varnames"]

	def __init__(self, prev, *varnames):
		self._prev = prev
		self._varnames = varnames

	def in_(self, expr):
		return ForExpression(self._prev, self._varnames, expr)

	def in_graph(self,
		graph=None,
		edges=None,
		direction=None,
		pathtype=None,
		start_vertex=None,
		target_vertex=None,
		min_depth=None,
		max_depth=None,
		prune_expr=None
	):
		expr = _PartialInGraphExpression(
			graph=graph,
			edges=edges,
			direction=direction,
			pathtype=pathtype,
			start_vertex=start_vertex,
			target_vertex=target_vertex,
			min_depth=min_depth,
			max_depth=max_depth,
			prune_expr=prune_expr
		)
		return self.in_(expr)


class _PartialInGraphExpression:
	direction_keywords = ["OUTBOUND", "INBOUND", "ANY"]
	pathtype_keywords = ["SHORTEST_PATH", "ALL_SHORTEST_PATHS", "K_SHORTEST_PATHS", "K_PATHS"]

	__slots__ = [
		"_graph",
		"_edges",
		"_direction",
		"_pathtype",
		"_start_vertex",
		"_target_vertex",
		"_min_depth",
		"_max_depth",
		"_prune_expr"
	]

	def __init__(self,
		graph=None,
		edges=None,
		direction=None,
		pathtype=None,
		start_vertex=None,
		target_vertex=None,
		min_depth=None,
		max_depth=None,
		prune_expr=None
	):
		if graph is not None and edges is not None:
			raise AqlError("Expected only one of the attributes graph and edges")
		if graph is not None and not isinstance(graph, str):
			raise AqlError(f"Expected graph to be a string: {repr(graph)}")
		if edges is not None and isinstance(edges, str):
			edges = (edges,)
		if direction is None:
			raise AqlError("Expected direction to be defined")
		if not (isinstance(direction, str) and direction.upper() in self.direction_keywords):
			raise AqlError(f"Expected direction to be one of: {self.direction_keywords}")
		if pathtype is not None and not (isinstance(pathtype, str) and pathtype.upper() in self.pathtype_keywords):
			raise AqlError(f"Expected pathtype to be one of: {self.pathtype_keywords}")
		if start_vertex is None:
			raise AqlError("Expected start_vertex to be define")
		if pathtype is not None and target_vertex is None:
			raise AqlError("Expected target_vertex to be define for this pathtype")
		if pathtype is None and target_vertex is not None:
			raise AqlError("Expected pathtype to be define with the target_vertex")
		if pathtype is not None and prune_expr is not None:
			raise AqlError("Attributes pathtype and prune_expr can not be both defined.")

		self._graph = None if graph is None else StringLiteral(graph)
		self._edges = None
		if edges:
			self._edges = []
			allow_keyword = True
			for i, edge in enumerate(list(edges)):
				if not allow_keyword and edge:
					if isinstance(edge, Keyword) or (
						isinstance(edge, str) and edge.upper() in self.direction_keywords
					):
						raise AqlError(
							f"Unexpected direction keyword {edge.toString()} at offset {i}"
						)
				if isinstance(edge, str) and edge.upper() in self.direction_keywords:
					allow_keyword = False
					self._edges.append(Keyword(edge))
				else:
					allow_keyword = True
					self._edges.append(auto_cast_token(edge))

		self._direction = direction.upper()
		self._pathtype = None if pathtype is None else pathtype.upper()
		self._start_vertex = auto_cast_token(start_vertex)
		self._target_vertex = None if target_vertex is None else auto_cast_token(target_vertex)
		self._min_depth = None if min_depth is None else auto_cast_token(min_depth)
		self._max_depth = None if max_depth is None else auto_cast_token(max_depth)
		self._prune_expr = None if prune_expr is None else auto_cast_token(prune_expr)

	def _edges_to_aql(self):
		edges = []
		keyword = None
		for edge in self._edges:
			if isinstance(edge, Keyword):
				keyword = edge.to_aql()
			else:
				tmpl = (f"{keyword} " if keyword else "") + "%s"
				edges.append(tmpl % wrap_aql(edge))
				keyword = None
		return ", ".join(edges)

	def to_aql(self):
		aql = []

		# can only specify min/max depth with traversal and k_paths
		if self._min_depth is not None and self._pathtype in (None, "K_PATHS"):
			depth = wrap_aql(self._min_depth)
			if self._max_depth is not None:
				depth += ".."
				depth += wrap_aql(self._max_depth)
			aql.append(depth)

		aql.append(self._direction)
		if self._pathtype:
			aql.append(self._pathtype)

		aql.append(wrap_aql(self._start_vertex))
		# can only specify a target with a pathtype define (not traversal)
		if self._target_vertex and self._pathtype:
			aql.append("TO")
			aql.append(wrap_aql(self._target_vertex))

		if self._graph:
			aql.append("GRAPH")
			aql.append(wrap_aql(self._graph))
		else:
			aql.append(self._edges_to_aql())

		if self._prune_expr is not None and self._pathtype is None:
			aql.append("PRUNE")
			aql.append(wrap_aql(self._prune_expr))
		return " ".join(aql)


class _PartialRemoveExpression:

	__slots__ = ["_prev", "_expr"]

	def __init__(self, prev, expr):
		self._prev = prev
		self._expr = expr

	def in_(self, collection):
		return RemoveExpression(self._prev, self._expr, collection)

	def into(self, collection):
		return self.in_(collection)


class _PartialUpsertExpression:

	__slots__ = ["_prev", "_upsert_expr"]

	def __init__(self, prev, upsert_expr):
		self._prev = prev
		self._upsert_expr = upsert_expr

	def insert(self, insert_expr):
		return _PartialUpsertInsertExpression(
			self._prev, self._upsert_expr, insert_expr
		)


class _PartialUpsertInsertExpression:

	__slots__ = ["_prev", "_upsert_expr", "_insert_expr"]

	def __init__(self, prev, upsert_expr, insert_expr):
		self._prev = prev
		self._upsert_expr = upsert_expr
		self._insert_expr = insert_expr

	def _update_or_replace(self, replace, update_or_replace_expr):
		return _PartialUpsertInExpression(
			self._prev,
			self._upsert_expr,
			self._insert_expr,
			replace,
			update_or_replace_expr,
		)

	def update(self, update_expr):
		return self._update_or_replace(False, update_expr)

	def replace(self, replace_expr):
		return self._update_or_replace(True, replace_expr)


class _PartialUpsertInExpression:

	__slots__ = [
		"_prev",
		"_upsert_expr",
		"_insert_expr",
		"_replace",
		"_update_or_replace_expr",
	]

	def __init__(self, prev, upsert_expr, insert_expr, replace, update_or_replace_expr):
		self._prev = prev
		self._upsert_expr = upsert_expr
		self._insert_expr = insert_expr
		self._replace = replace
		self._update_or_replace_expr = update_or_replace_expr

	def in_(self, collection):
		return UpsertExpression(
			self._prev,
			self._upsert_expr,
			self._insert_expr,
			self._replace,
			self._update_or_replace_expr,
			collection,
		)

	def into(self, collection):
		return self.in_(collection)


class _PartialInsertExpression:

	__slots__ = ["_prev", "_expr"]

	def __init__(self, prev, expr):
		self._prev = prev
		self._expr = expr

	def in_(self, collection):
		return InsertExpression(self._prev, self._expr, collection)

	def into(self, collection):
		return self.in_(collection)


class _PartialUpdateExpression:

	__slots__ = ["_prev", "_expr"]

	def __init__(self, prev, expr):
		self._prev = prev
		self._expr = expr

	def with_(self, with_expr):
		return _PartialUpdateInExpression(self._prev, self._expr, with_expr)

	def in_(self, collection):
		return UpdateExpression(self._prev, self._expr, None, collection)

	def into(self, collection):
		return self.in_(collection)


class _PartialUpdateInExpression:

	__slots__ = ["_prev", "_expr", "_with_expr"]

	def __init__(self, prev, expr, with_expr):
		self._prev = prev
		self._expr = expr
		self._with_expr = with_expr

	def in_(self, collection):
		return UpdateExpression(self._prev, self._expr, self._with_expr, collection)

	def into(self, collection):
		return self.in_(collection)


class _PartialReplaceExpression:

	__slots__ = ["_prev", "_expr"]

	def __init__(self, prev, expr):
		self._prev = prev
		self._expr = expr

	def with_(self, with_expr):
		return _PartialReplaceInExpression(self._prev, self._expr, with_expr)

	def in_(self, collection):
		return ReplaceExpression(self._prev, self._expr, None, collection)

	def into(self, collection):
		return self.in_(collection)


class _PartialReplaceInExpression:

	__slots__ = ["_prev", "_expr", "_with_expr"]

	def __init__(self, prev, expr, with_expr):
		self._prev = prev
		self._expr = expr
		self._with_expr = with_expr

	def in_(self, collection):
		return ReplaceExpression(self._prev, self._expr, self._with_expr, collection)

	def into(self, collection):
		return self.in_(collection)


class _PartialWindowExpression:

	__slots__ = ["_prev", "_range_expr", "_options"]

	def __init__(
		self,
		prev,
		range_expr=None,
		options=None,
	):
		self._prev = prev
		self._range_expr = range_expr
		self._options = options

	def range_(self, range_expr):
		return _PartialWindowExpression(
			self._prev,
			range_expr=range_expr,
			options=self._options
		)

	def options(self, options):
		return _PartialWindowExpression(
			self._prev,
			range_expr=self._range_expr,
			options=options
		)

	def aggregate(self, aggregate_dfns):
		return WindowExpression(
			self._prev,
			range_expr=self._range_expr,
			options=self._options,
			aggregate_dfns=aggregate_dfns
		)


class _PartialStatement:

	def __getattribute__(self, name):
		return super().__getattribute__(name)

	def __getattr__(self, name):

		def wrapper(*args):
			return FunctionCall(name, *args)

		return wrapper

	def _prev_aql(self):
		if getattr(self, "_prev", None) is not None:
			return self._prev.to_aql()
		return ""  # pragma: no cover

	def for_(self, *varnames):
		return _PartialForExpression(self, *varnames)

	def filter(self, expr):
		return FilterExpression(self, expr)

	def search(self, expr):
		return SearchExpression(self, expr)

	def let(self, varname, expr):
		dfns = varname if expr is None else [[varname, expr]]
		return LetExpression(self, dfns)

	def collect(self, varname, expr=None):
		dfns = varname if expr is None else [[varname, expr]]
		return CollectExpression(self, dfns)

	def collect_with_count_into(self, varname):
		return CollectWithCountIntoExpression(self, None, varname)

	def window(self):
		return _PartialWindowExpression(self)

	def sort(self, *args):
		return SortExpression(self, *args)

	def limit(self, offset, count=None):
		return LimitExpression(self, offset, count)

	def remove(self, expr):
		return _PartialRemoveExpression(self, expr)

	def return_(self, value):
		return _ReturnExpression(self, value, False)

	def return_distinct(self, value):
		return _ReturnExpression(self, value, True)

	def upsert(self, upsert_expr):
		return _PartialUpsertExpression(self, upsert_expr)

	def insert(self, expr):
		return _PartialInsertExpression(self, expr)

	def update(self, expr):
		return _PartialUpdateExpression(self, expr)

	def replace(self, expr):
		return _PartialReplaceExpression(self, expr)


class WithExpression(_PartialStatement):
	__slots__ = ["_collections"]

	def __init__(self, *collections):
		self._collections = []
		if not collections:
			raise AqlError(f"Expected with list not to be empty: {collections}")
		for collection in collections:
			self._collections.append(auto_cast_token(collection))

	def for_(self, *varnames):
		return _PartialForExpression(self, *varnames)

	def to_aql(self):
		aql = []
		collections = []
		for collection in self._collections:
			collections.append(wrap_aql(collection))
		aql.append("WITH")
		aql.append(", ".join(collections))
		return " ".join(aql)


class ForExpression(_PartialStatement):

	__slots__ = ["_prev", "_varnames", "_expr", "_options"]

	def __init__(self, prev, varnames, expr, options=None):
		self._prev = prev
		self._varnames = []
		if not varnames:
			raise AqlError(f"Expected for list of varnames not to be empty: {varnames}")
		for varname in varnames:
			self._varnames.append(Identifier(varname))
		self._expr = expr if isinstance(expr, _PartialInGraphExpression) else auto_cast_token(expr)
		if options is None:
			options = {}
		self._options = ObjectLiteral(options)

	def options(self, options):
		return ForExpression(
			self._prev,
			self._varnames,
			self._expr,
			options=options
		)

	def to_aql(self):
		aql = []
		varnames = []
		for varname in self._varnames:
			varnames.append(wrap_aql(varname))
		if self._prev:
			aql.append(self._prev_aql())
		aql.append("FOR")
		aql.append(", ".join(varnames))
		aql.append("IN")
		aql.append(wrap_aql(self._expr))
		if self._options:
			aql.append("OPTIONS")
			aql.append(wrap_aql(self._options))
		return " ".join(aql)


class FilterExpression(_PartialStatement):

	__slots__ = ["_prev", "_expr"]

	def __init__(self, prev, expr):
		self._prev = prev
		self._expr = auto_cast_token(expr)

	def to_aql(self):
		aql = []
		if self._prev:
			aql.append(self._prev_aql())
		aql.append("FILTER")
		aql.append(wrap_aql(self._expr))
		return " ".join(aql)


class SearchExpression(_PartialStatement):

	__slots__ = ["_prev", "_expr", "_options"]

	def __init__(self, prev, expr, options=None):
		self._prev = prev
		self._expr = auto_cast_token(expr)
		if options is None:
			options = {}
		self._options = ObjectLiteral(options)

	def options(self, options):
		return SearchExpression(
			self._prev,
			self._expr,
			options=options
		)

	def to_aql(self):
		aql = []
		if self._prev:
			aql.append(self._prev_aql())
		aql.append("SEARCH")
		aql.append(wrap_aql(self._expr))
		if self._options:
			aql.append("OPTIONS")
			aql.append(wrap_aql(self._options))
		return " ".join(aql)


class LetExpression(_PartialStatement):

	__slots__ = ["_prev", "_dfns"]

	def __init__(self, prev, dfns):
		self._prev = prev
		self._dfns = _Definitions(dfns)

	def to_aql(self):
		aql = []
		if self._prev:
			aql.append(self._prev_aql())
		aql.append("LET")
		aql.append(wrap_aql(self._dfns))
		return " ".join(aql)


class CollectExpression(_PartialStatement):

	__slots__ = [
		"_prev",
		"_dfns",
		"_varname",
		"_aggregate_dfns",
		"_into_expr",
		"_keep_names",
		"_options",
	]

	def __init__(
		self,
		prev,
		dfns,
		varname=None,
		aggregate_dfns=None,
		into_expr=None,
		keep_names=None,
		options=None,
	):
		self._prev = prev
		self._dfns = None if dfns is None else _Definitions(dfns)
		self._varname = Identifier(varname) if varname else None
		self._aggregate_dfns = (
			None if aggregate_dfns is None else _Definitions(aggregate_dfns)
		)
		self._into_expr = into_expr
		self._keep_names = [Identifier(val) for val in keep_names] if keep_names else []
		if options is None:
			options = {}
		self._options = ObjectLiteral(options)

	def aggregate(self, aggregate_dfns):
		return CollectExpression(
			self._prev,
			self._dfns,
			varname=self._varname,
			aggregate_dfns=aggregate_dfns,
			into_expr=self._into_expr,
			keep_names=self._keep_names,
			options=self._options,
		)

	def into(self, varname, into_expr=None):
		return CollectExpression(
			self._prev,
			self._dfns,
			varname=varname,
			aggregate_dfns=self._aggregate_dfns,
			into_expr=into_expr,
			keep_names=self._keep_names,
			options=self._options,
		)

	def keep(self, *keep_names):
		return CollectExpression(
			self._prev,
			self._dfns,
			varname=self._varname,
			aggregate_dfns=self._aggregate_dfns,
			into_expr=self._into_expr,
			keep_names=keep_names,
			options=self._options,
		)

	def options(self, options):
		return CollectExpression(
			self._prev,
			self._dfns,
			varname=self._varname,
			aggregate_dfns=self._aggregate_dfns,
			into_expr=self._into_expr,
			keep_names=self._keep_names,
			options=options,
		)

	def with_count_into(self, varname):
		return CollectWithCountIntoExpression(
			self._prev, self._dfns, varname, options=self._options
		)

	def to_aql(self):
		aql = []
		if self._prev:
			aql.append(self._prev_aql())
		aql.append("COLLECT")
		if self._dfns:
			aql.append(wrap_aql(self._dfns))
		if self._aggregate_dfns is not None:
			aql.append("AGGREGATE")
			aql.append(wrap_aql(self._aggregate_dfns))
		if self._varname:
			aql.append("INTO")
			aql.append(wrap_aql(self._varname))
			if self._into_expr:
				aql.append("=")
				aql.append(wrap_aql(self._into_expr))
			elif self._keep_names:
				aql.append("KEEP")
				aql.append(", ".join([wrap_aql(keep) for keep in self._keep_names]))
		if self._options:
			aql.append("OPTIONS")
			aql.append(wrap_aql(self._options))
		return " ".join(aql)


class CollectWithCountIntoExpression(_PartialStatement):

	__slots__ = ["_prev", "_dfns", "_varname", "_options"]

	def __init__(self, prev, dfns, varname, options=None):
		self._prev = prev
		self._dfns = None if dfns is None else _Definitions(dfns)
		self._varname = Identifier(varname)
		if options is None:
			options = {}
		self._options = ObjectLiteral(options)

	def options(self, options):
		return CollectWithCountIntoExpression(
			self._prev, self._dfns, self._varname, options=options
		)

	def to_aql(self):
		aql = []
		if self._prev:
			aql.append(self._prev_aql())
		aql.append("COLLECT")
		if self._dfns:
			aql.append(wrap_aql(self._dfns))
		aql.append("WITH COUNT INTO")
		aql.append(wrap_aql(self._varname))
		if self._options:
			aql.append("OPTIONS")
			aql.append(wrap_aql(self._options))
		return " ".join(aql)


class WindowExpression(_PartialStatement):

	__slots__ = [
		"_prev",
		"_range_expr",
		"_options",
		"_aggregate_dfns",
	]

	def __init__(
		self,
		prev,
		range_expr=None,
		options=None,
		aggregate_dfns=None,
	):
		self._prev = prev
		self._range_expr = range_expr
		if options is None:
			options = {}
		self._options = ObjectLiteral(options)
		self._aggregate_dfns = (
			None if aggregate_dfns is None else _Definitions(aggregate_dfns)
		)

	def to_aql(self):
		aql = []
		if self._prev:
			aql.append(self._prev_aql())
		aql.append("WINDOW")
		if self._range_expr:
			aql.append(wrap_aql(self._range_expr))
			aql.append("WITH")
		if self._options:
			aql.append(wrap_aql(self._options))
		aql.append("AGGREGATE")
		aql.append(wrap_aql(self._aggregate_dfns))
		return " ".join(aql)


class SortExpression(_PartialStatement):
	keywords = ["ASC", "DESC"]

	__slots__ = ["_prev", "_args"]

	def __init__(self, prev, *args):
		self._prev = prev
		self._args = []
		if not args:
			raise AqlError(f"Expected sort list not to be empty: {args}")
		allow_keyword = False
		for i, arg in enumerate(list(args)):
			if not allow_keyword and arg:
				if isinstance(arg, Keyword) or (
					isinstance(arg, str) and arg.upper() in self.keywords
				):
					raise AqlError(f"Unexpected keyword {arg.toString()} at offset {i}")
			if isinstance(arg, str) and arg.upper() in self.keywords:
				allow_keyword = False
				self._args.append(Keyword(arg))
			else:
				allow_keyword = True
				self._args.append(auto_cast_token(arg))

	def to_aql(self):
		aql = []
		args = []
		j = 0
		for arg in self._args:
			if isinstance(arg, Keyword):
				args[j - 1] = args[j - 1] + f" {arg.to_aql()}"
			else:
				args.append(wrap_aql(arg))
				j += 1
		if self._prev:
			aql.append(self._prev_aql())
		aql.append("SORT")
		aql.append(", ".join(args))
		return " ".join(aql)


class LimitExpression(_PartialStatement):

	__slots__ = ["_prev", "_offset", "_count"]

	def __init__(self, prev, offset, count=None):
		self._prev = prev
		if count is None:
			count = offset
			offset = None
		self._offset = None if offset is None else auto_cast_token(offset)
		self._count = auto_cast_token(count)

	def to_aql(self):
		aql = []
		if self._prev:
			aql.append(self._prev_aql())
		aql.append("LIMIT")
		if self._offset is not None:
			aql.append(f"{wrap_aql(self._offset)},")
		aql.append(wrap_aql(self._count))
		return " ".join(aql)


class RemoveExpression(_PartialStatement):

	__slots__ = ["_prev", "_expr", "_collection", "_options"]

	def __init__(self, prev, expr, collection, options=None):
		self._prev = prev
		self._expr = auto_cast_token(expr)
		self._collection = Identifier(collection)
		if options is None:
			options = {}
		self._options = ObjectLiteral(options)

	def options(self, options):
		return RemoveExpression(
			self._prev, self._expr, self._collection, options=options
		)

	def to_aql(self):
		aql = []
		if self._prev:
			aql.append(self._prev_aql())
		aql.append("REMOVE")
		aql.append(wrap_aql(self._expr))
		aql.append("IN")
		aql.append(wrap_aql(self._collection))
		if self._options:
			aql.append("OPTIONS")
			aql.append(wrap_aql(self._options))
		return " ".join(aql)


class UpsertExpression(_PartialStatement):

	__slots__ = [
		"_prev",
		"_upsert_expr",
		"_insert_expr",
		"_replace",
		"_update_or_replace_expr",
		"_collection",
		"_options",
	]

	def __init__(
		self,
		prev,
		upsert_expr,
		insert_expr,
		replace,
		update_or_replace_expr,
		collection,
		options=None,
	):
		self._prev = prev
		self._upsert_expr = auto_cast_token(upsert_expr)
		self._insert_expr = auto_cast_token(insert_expr)
		self._replace = replace
		self._update_or_replace_expr = auto_cast_token(update_or_replace_expr)
		self._collection = Identifier(collection)
		if options is None:
			options = {}
		self._options = ObjectLiteral(options)

	def options(self, options):
		return UpsertExpression(
			self._prev,
			self._upsert_expr,
			self._insert_expr,
			self._replace,
			self._update_or_replace_expr,
			self._collection,
			options=options,
		)

	def return_new(self, return_expr=None):
		if return_expr is None:
			return self.return_("NEW")
		return self.return_(return_expr)

	def return_old(self, return_expr=None):
		if return_expr is None:
			return self.return_("OLD")
		return self.return_(return_expr)

	def to_aql(self):
		aql = []
		if self._prev:
			aql.append(self._prev_aql())
		aql.append("UPSERT")
		aql.append(wrap_aql(self._upsert_expr))
		aql.append("INSERT")
		aql.append(wrap_aql(self._insert_expr))
		aql.append("REPLACE" if self._replace else "UPDATE")
		aql.append(wrap_aql(self._update_or_replace_expr))
		aql.append("IN")
		aql.append(wrap_aql(self._collection))
		if self._options:
			aql.append("OPTIONS")
			aql.append(wrap_aql(self._options))
		return " ".join(aql)


class InsertExpression(_PartialStatement):

	__slots__ = ["_prev", "_expr", "_collection", "_options"]

	def __init__(self, prev, expr, collection, options=None):
		self._prev = prev
		self._expr = auto_cast_token(expr)
		self._collection = Identifier(collection)
		if options is None:
			options = {}
		self._options = ObjectLiteral(options)

	def options(self, options):
		return InsertExpression(
			self._prev, self._expr, self._collection, options=options
		)

	def return_new(self, return_expr=None):
		if return_expr is None:
			return self.return_("NEW")
		return self.return_(return_expr)

	def to_aql(self):
		aql = []
		if self._prev:
			aql.append(self._prev_aql())
		aql.append("INSERT")
		aql.append(wrap_aql(self._expr))
		aql.append("INTO")
		aql.append(wrap_aql(self._collection))
		if self._options:
			aql.append("OPTIONS")
			aql.append(wrap_aql(self._options))
		return " ".join(aql)


class UpdateExpression(_PartialStatement):

	__slots__ = ["_prev", "_expr", "_with_expr", "_collection", "_options"]

	def __init__(self, prev, expr, with_expr, collection, options=None):
		self._prev = prev
		self._expr = auto_cast_token(expr)
		self._with_expr = None if with_expr is None else auto_cast_token(with_expr)
		self._collection = Identifier(collection)
		if options is None:
			options = {}
		self._options = ObjectLiteral(options)

	def options(self, options):
		return UpdateExpression(
			self._prev, self._expr, self._with_expr, self._collection, options=options
		)

	def return_new(self, return_expr=None):
		if return_expr is None:
			return self.return_("NEW")
		return self.return_(return_expr)

	def return_old(self, return_expr=None):
		if return_expr is None:
			return self.return_("OLD")
		return self.return_(return_expr)

	def to_aql(self):
		aql = []
		if self._prev:
			aql.append(self._prev_aql())
		aql.append("UPDATE")
		aql.append(wrap_aql(self._expr))
		if self._with_expr:
			aql.append("WITH")
			aql.append(wrap_aql(self._with_expr))
		aql.append("IN")
		aql.append(wrap_aql(self._collection))
		if self._options:
			aql.append("OPTIONS")
			aql.append(wrap_aql(self._options))
		return " ".join(aql)


class ReplaceExpression(_PartialStatement):

	__slots__ = ["_prev", "_expr", "_with_expr", "_collection", "_options"]

	def __init__(self, prev, expr, with_expr, collection, options=None):
		self._prev = prev
		self._expr = auto_cast_token(expr)
		self._with_expr = None if with_expr is None else auto_cast_token(with_expr)
		self._collection = Identifier(collection)
		if options is None:
			options = {}
		self._options = ObjectLiteral(options)

	def options(self, options):
		return ReplaceExpression(
			self._prev, self._expr, self._with_expr, self._collection, options=options
		)

	def return_new(self, return_expr=None):
		if return_expr is None:
			return self.return_("NEW")
		return self.return_(return_expr)

	def return_old(self, return_expr=None):
		if return_expr is None:
			return self.return_("OLD")
		return self.return_(return_expr)

	def to_aql(self):
		aql = []
		if self._prev:
			aql.append(self._prev_aql())
		aql.append("REPLACE")
		aql.append(wrap_aql(self._expr))
		if self._with_expr:
			aql.append("WITH")
			aql.append(wrap_aql(self._with_expr))
		aql.append("IN")
		aql.append(wrap_aql(self._collection))
		if self._options:
			aql.append("OPTIONS")
			aql.append(wrap_aql(self._options))
		return " ".join(aql)
