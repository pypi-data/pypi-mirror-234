from dotty_dict import dotty
from jsonmerge import Merger, strategies
from jsonmerge.jsonvalue import JSONValue
from jsonmerge.strategies import Strategy


def merge(base: dict, head: dict) -> dict:
    """Create an instance of jsonmerge Merger class and call merge function"""
    strategies = {
        "objectMerge": JsonMergeTreeObjectMerge(),
        "unsetKey": UnsetKey()
    }
    return Merger({}, strategies=strategies).merge(base, head)


class JsonMergeTreeObjectMerge(strategies.ObjectMerge):
    """Merge strategy that allows customizing how objects are merged.

    1) Allow overwriting a scalar with an object.
    We may need to merge a json document that has an object property onto one that has a scalar in
    the same place, which ObjectMerge doesn't allow.

    2) Allow keys with special denotations to use custom merge strategies.
    """
    def merge(self, walk, base, head, schema, **kwargs):
        # Allow overwriting a scalar with an object.
        if not base.is_undef() and not walk.is_type(base, "object"):
            return head

        # Build a dictionary of special keys to handle
        keys_to_change = {}
        for k, _ in head.items():  # JSONValue "dict"
            # `--` denotation indicates this key should be removed from the object
            if k.endswith('--'):
                new_key = k[:-2]
                keys_to_change[k] = {'new_key': new_key, 'merge_strategy': 'unsetKey'}
            # `!` denotation indicates this key should overwrite the parent's value
            if k.endswith('!'):
                new_key = k[:-1]
                keys_to_change[k] = {'new_key': new_key, 'merge_strategy': 'overwrite'}

        # Handle special keys by updating the schema with the given merge strategy
        for k, v in keys_to_change.items():
            # Rename the key in head to remove the special characters
            head.val[v['new_key']] = head.val[k]
            del head.val[k]

            # Update the current schema
            curr_props = {v['new_key']: {'mergeStrategy': v['merge_strategy']}}
            if schema.val and 'properties' in schema.val:
                curr_props.update(schema['properties'].val)
            schema = JSONValue({'properties': curr_props},
                               ref=str.replace(head.ref, '/', '/properties/'))

            # Normally, the schema would be loaded when the merger was set,
            # so we need to update the store with the new schema
            dot_schema = dotty(walk.resolver.store[''])
            schema_ref = build_schema_ref(head.ref)
            dot_schema[schema_ref] = curr_props

        return super(JsonMergeTreeObjectMerge, self).merge(walk, base, head, schema, **kwargs)


def build_schema_ref(head_ref: str) -> str:
    """Build reference for a schema based on the head reference

    A schema follows the same nested structure as the head document, except that each set of keys is
    nested under a `properties` key.

    Ex1. '#' returns 'properties'
    Ex2. '#/nested_remove_key' returns 'properties.nested_remove_key.properties'
    Ex3. '#/double_nested_remove_key/nested' returns
    'properties.double_nested_remove_key.properties.nested.properties'
    """
    parts = str.replace(head_ref[2:], '/', '/properties/').split('/') if len(head_ref) > 2 else []
    parts.append('properties')
    if len(parts) > 1:
        parts.insert(0, 'properties')
    return '.'.join(parts)


class UnsetKey(Strategy):
    """Merge strategy that allows unsetting a key."""
    def merge(self, walk, base, head, *args, **kwargs):
        return JSONValue(undef=True)
