# AUTO GENERATED FILE - DO NOT EDIT

export reacttable

"""
    reacttable(;kwargs...)

A ReactTable component.

Keyword arguments:
- `id` (String; required)
- `rows` (required): . rows has the following type: Array of lists containing elements 'id', 'date', 'text', 'stance', 'sentiment', 'num_replies', 'replies'.
Those elements have the following types:
  - `id` (String; required)
  - `date` (String; required)
  - `text` (String; required)
  - `stance` (String; required)
  - `sentiment` (String; required)
  - `num_replies` (Real; required)
  - `replies` (optional): . replies has the following type: Array of lists containing elements 'id', 'date', 'text', 'stance', 'sentiment', 'num_replies', 'replies'.
Those elements have the following types:
  - `id` (String; required)
  - `date` (String; required)
  - `text` (String; required)
  - `stance` (String; required)
  - `sentiment` (String; required)
  - `num_replies` (Real; required)
  - `replies` (Array; optional)ss
"""
function reacttable(; kwargs...)
        available_props = Symbol[:id, :rows]
        wild_props = Symbol[]
        return Component("reacttable", "ReactTable", "collapsible_table", available_props, wild_props; kwargs...)
end

