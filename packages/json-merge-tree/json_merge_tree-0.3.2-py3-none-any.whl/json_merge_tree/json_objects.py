import json
from functools import reduce
from types import ModuleType
from typing import Any, Callable, Iterable, Optional, Tuple
from uuid import UUID

from sqlalchemy import Table, func
from sqlalchemy.sql import select

from json_merge_tree.merged import merge

Ancestors = Iterable[Tuple[UUID, Optional[Callable]]]


def merge_tree(
        db: Any,
        table: Table,
        id: UUID,
        type: str,
        json_field: str,
        parents: ModuleType,
        slugs: Optional[Iterable[str]] = None,
        filters: Optional[tuple] = None,
        debug: Optional[str] = None
) -> dict:
    """Take a resource ID and return the merged json object for that page.

    The merged json object is any json saved for that resource, merged into any resources saved
    for its ancestor resources, all the way up the hierarchy.
    """
    # Get a generator that will yield the IDs of a resource's immediate ancestors
    parent_getter = getattr(parents, type, None)

    # Get a generator that will yield the json objects of all the requested resource's ancestors
    json_objects = get_json_objects(db, table, id, json_field, parent_getter, slugs, filters, debug)

    # Merge those json objects and return the result
    return reduce(merge, json_objects, {})


def get_json_objects(
    db: Any,
    table: Table,
    resource_id: UUID,
    json_field: str,
    parent_getter: Optional[Callable[[UUID], Ancestors]],
    slugs: Optional[Iterable[str]] = None,
    filters: Optional[tuple] = None,
    debug: Optional[str] = None
) -> Iterable[dict]:
    """Take a resource ID and return all its ancestors' resources.

     Recurses up the hierarchy using "parent getters" to get the IDs of each resource's immediate
     ancestors, then on the way back down yields any resources defined for those resources, starting
     at the top.
    """
    c = table.columns
    # These filters will be used to get the resource record here, and also the slug records later
    query_filters: tuple = (c.resource_id == resource_id,)
    if filters is not None:
        query_filters = query_filters + filters
    query = select([table]).where(*query_filters)
    record = get_resource_record(db, query.where(c.slug.is_(None)).order_by(c.created_at))

    if parent_getter is not None and getattr(record, 'inherits', True):
        # If this resource isn't the top of the hierarchy, recurse upwards...
        for parent_id, grandparent_getter in parent_getter(resource_id):
            # ...with the parent's ID and a generator of that resource's immediate ancestors
            yield from get_json_objects(db, table, parent_id, json_field, grandparent_getter, slugs,
                                        filters, debug)

    # As the recursion unwinds, yield any json objects for each resource:
    # its own, and any slugs under it
    if record:
        yield record_json(record, json_field, debug)
    if slugs:
        for slug_record in get_slug_records(db, query, c, slugs):
            yield record_json(slug_record, json_field, debug)


def get_resource_record(db, query):
    return db.execute(query).first()


def get_slug_records(db, query, c, slugs):
    order = func.array_position(slugs, c.slug)
    return db.execute(query.where(c.slug.in_(slugs)).order_by(order))


def record_json(
        record: Any,
        json_field: str,
        debug: Optional[str] = None
) -> dict:
    hook = None
    if debug:
        def add_debug_info(d):
            from_dicts = {
                k + '-from' if debug == 'annotate' else k: from_dict(record, json_field)
                for k, v in d.items()
                if not isinstance(v, dict)
            }
            d.update(from_dicts)
            return d
        hook = add_debug_info
    return json.loads(getattr(record, json_field), object_hook=hook)


def from_dict(
        record: Any,
        json_field: str
) -> dict:
    return {
        'id': record.resource_id,
        f'{json_field}_id': record.id,
        'type': record.resource_type,
        'slug': record.slug or None
    }
