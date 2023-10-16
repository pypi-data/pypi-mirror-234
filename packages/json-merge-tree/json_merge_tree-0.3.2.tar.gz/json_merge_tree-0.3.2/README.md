# json-merge-tree

JSON Merge Tree (built on top of [`jsonmerge`](https://github.com/avian2/jsonmerge)) merges JSON objects in a hierarchy, 
allowing customization of how objects are merged.

The hierarchy is defined by the caller's `parents` module, which specifies a function for each resource type that 
returns the parent ID and another function to get its parents (unless it's the top level).

It relies on a SQLAlchemy `Table` containing the fields `id` (UUID), `resource_id` (UUID), `resource_type` (string), `slug` (string), 
and a field that stores the JSON object you want to merge.

## Installation

Install this package, e.g., `pip install json-merge-tree`.
```

## merge_tree

Main entrypoint for merging JSON objects in a table up a hierarchy defined by `parents`.

### Example
```python
from json_merge_tree import merge_tree

import widget_service.parents
from widget_service.db import widgets

# Merge widgets of all the requested resource's ancestors and return the result
merged_json = merge_tree(
    table=widgets, 
    id='228135fb-6a3d-4551-93db-17ed1bbe466a', 
    type='brand', 
    json_field='widget', 
    parents=widget_service.parents, 
    slugs=None, 
    debug='annotate'
)
```

## merge

Generic function to merge two JSON objects together. Largely the same as 
[`jsonmerge.Merger.merge`](https://github.com/avian2/jsonmerge/blob/master/jsonmerge/__init__.py#L299) 
but with the added ability to customize how objects are merged with the annotations below.


## Merge key annotations

You can append the annotation listed below to a key at any level to customize how its value affects the merged json.

### `--` Unset
Unset this key in the merged json. The value of this key does not matter - you can set it to `null`.

- **E.g. 1**
```json
{
  "colors": {
    "content": "#000000", 
    "section--": null
  }
}
```
merged into  
```json
{
  "colors": {
    "section": "#000001"
  }
}
``` 
results in  
```json
{
  "colors": {
    "content": "#000000"
  }
}
``` 

***

- **E.g. 2**
```json
{
  "styles": {
    "h1--": null, 
    "h2": {
      "fontSize": 3
    }
  }
}
``` 
merged into  
```json
{
  "styles": {
    "h1": {
      "fontWeight": "heading"
    }
  }
}
``` 
results in  
```json
{
  "styles": {
    "h2": {
      "fontSize": 3
    }
  }
}
```

### `!` Replace
Replace this key's value with this value.

- **E.g. 1**
```json
{
  "colors": {
      "content": "#000000", 
      "section!": "#000002"
  }
}
```
merged into
```json
{
  "colors": {
    "section": "#000001"
  }
}
``` 
results in 
```json
{
  "colors": {
    "content": "#000000", 
    "section": "#000002"
  }
}
``` 

***

- **E.g. 2**
```json
{
  "styles": {
    "h1!": {
      "fontFamily": "heading",
      "fontSize": 5
    }
  }
}
``` 
merged into  
```json
{
  "styles": {
    "h1": {
      "fontWeight": "heading"
    }
  }
}
```
results in  
```json
{
  "styles": {
    "h1": {
      "fontFamily": "heading",
      "fontSize": 5
    }
  }
}
```

## Slugs

Slugs are kind of a weird feature – and getting weirder as we use them to solve more use cases.

Originally, A slug was a named json object scoped *under* a resource in the hierarchy to be merged. In our case, a custom-page theme merged under one of the resources in our resource hierarchy.

The use of slugs has been extended to included named json object mixins *not* associated with any one resource at the bottom of the hierarchy, but scoped to a resource at any level. For example, a site wants to have a "dark" theme that could be applied to any page within the site.

When merging, the library first merges the json objects without slugs, *then* merges json objects with slugs at each level. Multiple slugs can be included when merging.
