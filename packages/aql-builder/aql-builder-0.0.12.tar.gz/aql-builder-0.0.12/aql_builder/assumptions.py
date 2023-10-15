from math import inf

keywords = set([
	"aggregate",
	"all",
	"and",
	"any",
	"asc",
	"collect",
	"desc",
	"distinct",
	"false",
	"filter",
	"for",
	"graph",
	"in",
	"inbound",
	"insert",
	"into",
	"k_paths",
	"k_shortest_paths",
	"let",
	"like"
	"limit",
	"none",
	"not",
	"null",
	"or",
	"outbound",
	"remove",
	"replace",
	"return",
	"shortest_path",
	"sort",
	"true",
	"update",
	"upsert",
	"window",
	"with",
])

# not reserved but contextual keywords
keywords_not_reserved = set([
	"keep",
	"count",
	"options",
	"prune",
	"search",
	"to",
	"current",
	"new",
	"old",
])

builtins = {
	# Conversion
	"TO_BOOL": 1,
	"TO_NUMBER": 1,
	"TO_STRING": 1,
	"TO_LIST": 1,
	"TO_ARRAY": 1,
	"IPV4_FROM_NUMBER": 1,
	"IPV4_TO_NUMBER": 1,
	"TO_BASE64": 1,
	"TO_HEX": 1,

	# Type checks
	"IS_NULL": 1,
	"IS_BOOL": 1,
	"IS_NUMBER": 1,
	"IS_STRING": 1,
	"IS_ARRAY": 1,
	"IS_LIST": 1,
	"IS_OBJECT": 1,
	"IS_DOCUMENT": 1,
	"IS_DATESTRING": 1,
	"IS_IPV4": 1,
	"IS_KEY": 1,
	"TYPENAME": 1,

	# String functions
	"CHAR_LENGTH": 1,
	"CONCAT": [[1, inf]],
	"CONCAT_SEPARATOR": [[2, inf]],
	"CONTAINS": [2, 3],
	"COUNT": 1,
	"CRC32": 1,
	"ENCODE_URI_COMPONENT": 1,
	"FIND_FIRST": [2, 3, 4],
	"FIND_LAST": [2, 3, 4],
	"FNV64": 1,
	"JSON_PARSE": 1,
	"JSON_STRINGIFY": 1,
	"LEFT": 2,
	"LENGTH": 1,
	"LEVENSHTEIN_DISTANCE": 2,
	"LIKE": [2, 3],
	"LOWER": 1,
	"LTRIM": [1, 2],
	"MD5": 1,
	"NGRAM_POSITIONAL_SIMILARITY": 3,
	"NGRAM_SIMILARITY": 3,
	"RANDOM_TOKEN": 1,
	"REGEX_MATCHES": [2, 3],
	"REGEX_SPLIT": [2, 3, 4],
	"REGEX_TEST": [2, 3],
	"REGEX_REPLACE": [3, 4],
	"REVERSE": 1,
	"RIGHT": 2,
	"RTRIM": [1, 2],
	"SHA1": 1,
	"SHA512": 1,
	"SOUNDEX": 1,
	"SPLIT": [1, 2, 3],
	"STARTS_WITH": [2, 3],
	"SUBSTITUTE": [2, 3, 4],
	"SUBSTRING": [2, 3],
	"TOKENS": 2,
	"TRIM": [1, 2],
	"UPPER": 1,
	"UUID": 0,

	# Numeric functions
	"ABS": 1,
	"ACOS": 1,
	"ASIN": 1,
	"ATAN": 1,
	"ATAN2": 2,
	"AVERAGE": 1,
	"AVG": 1,
	"CEIL": 1,
	"COS": 1,
	"DEGREES": 1,
	"EXP": 1,
	"EXP2": 1,
	"FLOOR": 1,
	"LOG": 1,
	"LOG2": 1,
	"LOG10": 1,
	"MAX": 1,
	"MEDIAN": 1,
	"MIN": 1,
	"PERCENTILE": [2, 3],
	"PI": 0,
	"POW": 2,
	"PRODUCT": 1,
	"RADIANS": 1,
	"RAND": 0,
	"RANGE": [2, 3],
	"ROUND": 1,
	"SIN": 1,
	"SQRT": 1,
	"STDDEV_POPULATION": 1,
	"STDDEV_SAMPLE": 1,
	"STDDEV": 1,
	"SUM": 1,
	"TAN": 1,
	"VARIANCE_POPULATION": 1,
	"VARIANCE_SAMPLE": 1,
	"VARIANCE": 1,

	# Bit functions
	"BIT_AND": [1, 2],
	"BIT_CONSTRUCT": 1,
	"BIT_DECONSTRUCT": 1,
	"BIT_FROM_STRING": 1,
	"BIT_NEGATE": 2,
	"BIT_OR": [1, 2],
	"BIT_POPCOUNT": 1,
	"BIT_SHIFT_LEFT": 3,
	"BIT_SHIFT_RIGHT": 3,
	"BIT_TEST": 2,
	"BIT_TO_STRING": 2,
	"BIT_XOR": [1, 2],

	# Date functions
	"DATE_NOW": 0,
	"DATE_ISO8601": [1, [3, 7]],
	"DATE_TIMESTAMP": [1, [3, 7]],
	"DATE_DAYOFWEEK": 1,
	"DATE_YEAR": 1,
	"DATE_MONTH": 1,
	"DATE_DAY": 1,
	"DATE_HOUR": 1,
	"DATE_MINUTE": 1,
	"DATE_SECOND": 1,
	"DATE_MILLISECOND": 1,
	"DATE_DAYOFYEAR": 1,
	"DATE_ISOWEEK": 1,
	"DATE_LEAPYEAR": 1,
	"DATE_QUARTER": 1,
	"DATE_DAYS_IN_MONTH": 1,
	"DATE_TRUNC": 2,
	"DATE_ROUND": 3,
	"DATE_FORMAT": 2,
	"DATE_ADD": [2, 3],
	"DATE_SUBTRACT": [2, 3],
	"DATE_DIFF": [3, 4],
	"DATE_COMPARE": [3, 4],

	# List functions
	"APPEND": [2, 3],
	"CONTAINS_ARRAY": [2, 3],
	# "COUNT": 1,# in strings
	"COUNT_DISTINCT": 1,
	"COUNT_UNIQUE": 1,
	"FIRST": 1,
	"FLATTEN": [1, 2],
	"INTERLEAVE": [[2, inf]],
	"INTERSECTION": [[2, inf]],
	"JACCARD": 2,
	"LAST": 1,
	# "LENGTH": 1,# in strings
	"MINUS": [[2, inf]],
	"NTH": 2,
	"OUTERSECTION": [[2, inf]],
	"POP": 1,
	"POSITION": [2, 3],
	"PUSH": [2, 3],
	"REMOVE_NTH": 2,
	"REPLACE_NTH": [3, 4],
	"REMOVE_VALUE": [2, 3],
	"REMOVE_VALUES": 2,
	# "REVERSE": 1, # in strings
	"SHIFT": 1,
	"SLICE": [2, 3],
	"SORTED": 1,
	"SORTED_UNIQUE": 1,
	"UNION": [[2, inf]],
	"UNION_DISTINCT": [[2, inf]],
	"UNIQUE": 1,
	"UNSHIFT": [2, 3],

	# Document functions
	"ATTRIBUTES": [1, 2, 3],
	# "COUNT": 1,# in strings
	"HAS": 2,
	"IS_SAME_COLLECTION": 2,
	"KEEP": [[2, inf]],
	# "LENGTH": 1,# in strings
	"MATCHES": [2, 3],
	"MERGE": [[2, inf]],
	"MERGE_RECURSIVE": [[2, inf]],
	"PARSE_IDENTIFIER": 1,
	"TRANSLATE": [2, 3],
	"UNSET": [[2, inf]],
	"UNSET_RECURSIVE": [[2, inf]],
	"VALUES": [1, 2],
	"ZIP": 2,

	# Geo functions
	"DISTANCE": 4,
	"GEO_CONTAINS": 2,
	"GEO_DISTANCE": [2, 3],
	"GEO_AREA": [1, 2],
	"GEO_EQUALS": 2,
	"GEO_INTERSECTS": 2,
	"GEO_IN_RANGE": [4, 6],
	"IS_IN_POLYGON": [2, 3],
	"GEO_LINESTRING": 1,
	"GEO_MULTILINESTRING": 1,
	"GEO_MULTIPOINT": 1,
	"GEO_POINT": 2,
	"GEO_POLYGON": 1,
	"GEO_MULTIPOLYGON": 1,

	"NEAR": [4, 5],  # Deprecated from 3.4.0
	"WITHIN": [4, 5],  # Deprecated from 3.4.0
	"WITHIN_RECTANGLE": 5,  # Deprecated from 3.4.0

	# Fulltext functions
	"FULLTEXT": [3, 4],

	# ArangoSearch functions
	"ANALYZER": 2,
	"BOOST": 2,
	"EXISTS": [1, 2, 3],
	"IN_RANGE": 5,
	"MIN_MATCH": [[2, inf]],
	"NGRAM_MATCH": [3, 4],
	"PHRASE": [[2, inf]],
	# "TOKENS": 2, # in strings
	# "STARTS_WITH": [2, 3], # in strings
	"LEVENSHTEIN_MATCH": [3, 6],
	# "LIKE": [2, 3], # in strings
	"BM25": [1, 3],
	"TFIDF": [1, 2],

	# Control flow functions
	"NOT_NULL": [[1, inf]],
	"FIRST_LIST": [[1, inf]],
	"FIRST_DOCUMENT": [[1, inf]],

	# Database functions
	"CHECK_DOCUMENT": 1,
	"COLLECTION_COUNT": 1,
	"COLLECTIONS": 0,
	# "COUNT": 1,# in strings
	"CURRENT_USER": 0,
	"DECODE_REV": 1,
	"DOCUMENT": [1, 2],
	# "LENGTH": 1, # in strings

	# Hash functions
	"HASH": 1,

	# Function calling
	"APPLY": [[1, inf]],
	"CALL": [[1, inf]],

	# Other functions
	"ASSERT": 2,
	"WARN": 2,
	# "IN_RANGE": 5, # in search
	"PREGEL_RESULT": [1, 2],

	# Miscellaneous functions
	"SKIPLIST": [[2, 4]],
}

deprecatedBuiltins = set([
	"NEAR",  # Deprecated from 3.4.0
	"WITHIN",  # Deprecated from 3.4.0
	"WITHIN_RECTANGLE",  # Deprecated from 3.4.0
	"SKIPLIST",
])
