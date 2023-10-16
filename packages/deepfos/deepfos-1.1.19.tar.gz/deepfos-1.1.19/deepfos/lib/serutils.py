from __future__ import annotations

import datetime
import decimal
import functools
import uuid

import edgedb
from edgedb.introspect import introspect_object as intro
from edgedb.datatypes import datatypes


@functools.singledispatch
def serialize(o):
    raise TypeError(f'无法序列化类型: {type(o)}')


@functools.singledispatch
def deserialize(o):
    raise TypeError(f'无法反序列化类型: {type(o)}')


@deserialize.register
def to_object(o: dict):
    _id = o.pop('id', None)
    ordered_attr = sorted(o.keys())
    obj_cls = datatypes.create_object_factory(
        id='property' if _id else 'implicit',
        ** {k: 'link' if isinstance(o[k], dict) else 'property' for k in ordered_attr}
    )
    return obj_cls(
        uuid.UUID(_id) if _id else None,
        *[deserialize(o[k]) for k in ordered_attr]
    )


@deserialize.register
def to_set(o: list):
    return [deserialize(ele) for ele in o]


@deserialize.register(int)
@deserialize.register(float)
@deserialize.register(str)
@deserialize.register(bytes)
@deserialize.register(bool)
@deserialize.register(type(None))
def to_scalar(o):
    return o


@serialize.register
def _tuple(o: edgedb.Tuple):
    return [serialize(el) for el in o]


@serialize.register
def _namedtuple(o: edgedb.NamedTuple):
    return {attr: serialize(getattr(o, attr)) for attr in dir(o)}


@serialize.register
def _linkset(o: edgedb.LinkSet):
    return [serialize(el) for el in o]


@serialize.register
def _link(o: edgedb.Link):
    ret = {}

    for lprop in dir(o):
        if lprop in {'source', 'target'}:
            continue
        ret[f'@{lprop}'] = serialize(getattr(o, lprop))

    ret.update(_object(o.target))
    return ret


@serialize.register
def _object(o: edgedb.Object):
    ret = {}

    implicited = [desc.name for desc in intro(o).pointers if desc.implicit]
    has_implicit = len(implicited) > 0

    for attr in dir(o):
        if has_implicit and attr in implicited:
            continue

        try:
            link = o[attr]
        except (KeyError, TypeError):
            link = None

        if link:
            ret[attr] = serialize(link)
        else:
            ret[attr] = serialize(getattr(o, attr))

    return ret


@serialize.register(edgedb.Set)
@serialize.register(edgedb.Array)
def _set(o):
    return [serialize(el) for el in o]


@serialize.register(uuid.UUID)
def _stringify(o):
    return str(o)


@serialize.register(int)
@serialize.register(float)
@serialize.register(str)
@serialize.register(bytes)
@serialize.register(bool)
@serialize.register(type(None))
@serialize.register(decimal.Decimal)
@serialize.register(datetime.timedelta)
@serialize.register(edgedb.RelativeDuration)
def _scalar(o):
    return o


@serialize.register
def _datetime(o: datetime.datetime):
    return o.isoformat()


@serialize.register
def _date(o: datetime.date):
    return o.isoformat()


@serialize.register
def _time(o: datetime.time):
    return o.isoformat()


@serialize.register
def _enum(o: edgedb.EnumValue):
    return str(o)
