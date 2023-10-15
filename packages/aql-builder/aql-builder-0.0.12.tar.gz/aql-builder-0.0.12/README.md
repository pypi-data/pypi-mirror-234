[![pipeline status](https://foss.heptapod.net/aquapenguin/aql-builder/badges/branch/default/pipeline.svg)](https://foss.heptapod.net/aquapenguin/aql-builder/-/pipelines)
[![coverage report](https://foss.heptapod.net/aquapenguin/aql-builder/badges/branch/default/coverage.svg)](https://foss.heptapod.net/aquapenguin/aql-builder/-/commits/branch/default)
[![Latest Release](https://foss.heptapod.net/aquapenguin/aql-builder/-/badges/release.svg)](https://foss.heptapod.net/aquapenguin/aql-builder/-/releases)
[![Python version](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![ArangoDB version](https://img.shields.io/badge/ArangoDB-3.8%2B-%23DDDF72)](https://www.arangodb.com/docs/stable/aql/)


# ArangoDB AQL builder

Python AQL builder for [ArangoDB](https://www.arangodb.com), a scalable multi-model
database natively supporting documents, graphs and search.

## Requirements

- Python version 3.7+

## Installation

```shell
pip install aql-builder --upgrade
```

## Getting Started

Here are simple usage examples:

```python
>>> from aql_builder import AQLBuilder as AB
>>> 
>>> AB.for_('my').in_('mycollection').return_('my._key').to_aql()
'FOR my IN mycollection RETURN my._key'
>>> 
>>> AB.for_('u').in_('users').replace('u').in_('backup').to_aql()
'FOR u IN users REPLACE u IN backup'
>>> 
>>> AB.for_('u').in_('users')
...     .filter(
...         AB.ref('u.active').eq(True)
...         .and_(AB.ref('u.age').gte(35))
...         .and_(AB.ref('u.age').lte(37))
...     )
...     .remove('u').in_('users')
...     .to_aql()
'FOR u IN users FILTER (((u.active == true) && (u.age >= 35)) && (u.age <= 37)) REMOVE u IN users'
>>> 
```

Working with query parameters:

```python
>>> from aql_builder import AQLBuilder as AB
>>> 
>>> AB.for_('user').in_('@@users').filter(AB.ref('user.age').gte('@min_age')).return_('user._key').to_aql()
'FOR user IN @@users FILTER (user.age >= @min_age) RETURN user._key'
>>> 
```

Working with graph:

```python
>>> from aql_builder import AQLBuilder as AB
>>> 
>>> AB.for_('v').in_graph(
...         graph='knowsGraph',
...         direction='OUTBOUND',
...         start_vertex=AB.str('users/1'),
...         min_depth=1,
...         max_depth=3
...     )
...     .return_('v._key')
...     .to_aql()
'FOR v IN 1..3 OUTBOUND "users/1" GRAPH "knowsGraph" RETURN v._key'
>>> 
```

More complex examples:

```python
>>> from aql_builder import AQLBuilder as AB
>>> 
>>> AB.for_('i').in_(AB.range(1, 1000))
...     .insert({
...         'id': AB(100000).add('i'),
...         'age': AB(18).add(AB.FLOOR(AB.RAND().times(25))),
...         'name': AB.CONCAT('test', AB.TO_STRING('i')),
...         'active': False,
...         'gender': (
...             AB.ref('i').mod(2).eq(0).then('"male"').else_('"female"')
...         )
...     }).into('users')
...     .to_aql()
'FOR i IN 1..1000 INSERT '
'{"id": (100000 + i), '
'"age": (18 + FLOOR((RAND() * 25))), '
'"name": CONCAT(test, TO_STRING(i)), '
'"active": false, '
'"gender": (((i % 2) == 0) ? "male" : "female")} '
'INTO users'
>>> 
>>> 
>>> AB.for_('u').in_('users')
...     .filter(AB.ref('u.active').eq(True))
...     .collect({
...         'ageGroup': AB.FLOOR(AB.ref('u.age').div(5)).times(5),
...         'gender': 'u.gender'
...     }).into('group')
...     .sort('ageGroup', 'DESC')
...     .return_({
...         'ageGroup': 'ageGroup',
...         'gender': 'gender'
...     })
...     .to_aql()
'FOR u IN users '
'FILTER (u.active == true) '
'COLLECT ageGroup = (FLOOR((u.age / 5)) * 5), gender = u.gender INTO group '
'SORT ageGroup DESC '
'RETURN {"ageGroup": ageGroup, "gender": gender}'
>>> 
```

## Acknowledgements

AQL builder is a free software project hosted at https://foss.heptapod.net. Thanks
to the support of [Clever Cloud](https://clever-cloud.com),
[Octobus](https://octobus.net) and the sponsors of the [heptapod project](https://heptapod.net/).