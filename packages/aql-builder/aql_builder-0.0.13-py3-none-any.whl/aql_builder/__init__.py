from aql_builder import types

# pylint: disable=protected-access

__version__ = '0.0.13'


class _AQLBuilderMeta(type):

	def __call__(cls, obj=None):
		return types.auto_cast_token(obj)

	def __getattribute__(cls, name):
		return super().__getattribute__(name)

	def __getattr__(cls, name):
		def wrapper(*args):
			try:
				return getattr(types._PartialStatement, name)(None, *args)
			except AttributeError:
				try:
					return getattr(types._Expression, name)(None, *args)
				except AttributeError:
					return types.FunctionCall(name, *args)

		return wrapper


class AQLBuilder(types._Expression, types._PartialStatement, metaclass=_AQLBuilderMeta):
	# pylint: disable=arguments-differ

	@staticmethod
	def if_(cond, then, otherwise):
		return types.auto_cast_token(cond).then(then).else_(otherwise)

	@staticmethod
	def null(value=None):
		return types.NullLiteral(value)

	@staticmethod
	def bool(value):
		return types.BooleanLiteral(value)

	@staticmethod
	def num(value):
		return types.NumberLiteral(value)

	@staticmethod
	def int(value):
		return types.IntegerLiteral(value)

	@staticmethod
	def str(value):
		return types.StringLiteral(value)

	@staticmethod
	def list(value):
		return types.ListLiteral(value)

	@staticmethod
	def obj(value):
		return types.ObjectLiteral(value)

	@staticmethod
	def ref(value):
		if isinstance(value, str) and types.Identifier.match(value):
			return types.Identifier(value)
		return types.SimpleReference(value)

	@staticmethod
	def expr(value):
		return types.RawExpression(value)

	@staticmethod
	def with_(*collections):
		return types.WithExpression(*collections)

	@staticmethod
	def for_(*varnames):
		return types._PartialStatement.for_(None, *varnames)

	@staticmethod
	def filter(expr):
		return types.FilterExpression(None, expr)

	@staticmethod
	def search(expr):
		return types.SearchExpression(None, expr)

	@staticmethod
	def let(varname, expr):
		dfns = varname if expr is None else [[varname, expr]]
		return types.LetExpression(None, dfns)

	@staticmethod
	def collect(varname=None, expr=None):
		dfns = varname if expr is None else [[varname, expr]]
		return types.CollectExpression(None, dfns)

	@staticmethod
	def collect_with_count_into(varname):
		return types.CollectWithCountIntoExpression(None, None, varname)

	@staticmethod
	def window():
		return types._PartialWindowExpression(None)

	@staticmethod
	def sort(*args):
		return types.SortExpression(None, *args)

	@staticmethod
	def limit(x, y=None):
		return types.LimitExpression(None, x, y)

	@staticmethod
	def remove(expr):
		return types._PartialRemoveExpression(None, expr)

	@staticmethod
	def return_(value):
		return types._ReturnExpression(None, value, False)

	@staticmethod
	def return_distinct(value):
		return types._ReturnExpression(None, value, True)

	@staticmethod
	def upsert(upsert_expr):
		return types._PartialUpsertExpression(None, upsert_expr)

	@staticmethod
	def insert(expr):
		return types._PartialInsertExpression(None, expr)

	@staticmethod
	def update(expr):
		return types._PartialUpdateExpression(None, expr)

	@staticmethod
	def replace(expr):
		return types._PartialReplaceExpression(None, expr)
