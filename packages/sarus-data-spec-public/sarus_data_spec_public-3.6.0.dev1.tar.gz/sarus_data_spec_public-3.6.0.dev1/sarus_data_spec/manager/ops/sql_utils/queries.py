from collections import defaultdict
import typing as t

from sarus_sql import ast_utils, rename_tables, translator

from sarus_data_spec.path import Path
import sarus_data_spec.type as sdt
import sarus_data_spec.typing as st


def rename_and_compose_queries(
    query_or_dict: t.Union[str, t.Dict[str, t.Any]],
    curr_path: t.List[str],
    queries_transform: t.Optional[t.Dict[str, str]],
    table_map: t.Dict[Path, t.Tuple[str, ...]],
) -> t.Union[str, t.Dict[str, t.Any]]:
    """Composition is done by first updating the table names
    in the leaves of queries_or_dict and then composing with
    all the queries in queries_transform
    """
    if isinstance(query_or_dict, str):
        # type ignore because issue of typing in sarus_sql
        updated_query = rename_tables.rename_tables(query_or_dict, table_map)  # type: ignore # noqa : E501
        if queries_transform is not None:
            updated_query = ast_utils.compose_query(
                queries_transform, updated_query
            )
        return updated_query
    else:
        new_queries = {}
        for name, sub_queries_or_dict in query_or_dict.items():
            new_queries[name] = rename_and_compose_queries(
                query_or_dict=sub_queries_or_dict,
                curr_path=[*curr_path, name],
                queries_transform=queries_transform,
                table_map=table_map,
            )
        return new_queries


def flatten_queries_dict(
    queries: t.Dict[str, t.Any]
) -> t.Dict[t.Tuple[str, ...], str]:
    """Transform nested dict in linear dict where each
    key is the tuple of the nesting path"""

    final_dict: t.Dict[t.Tuple[str, ...], str] = {}

    def update_dict(
        curr_path: t.List[str],
        dict_to_update: t.Dict[t.Tuple[str, ...], t.Any],
        query_or_dict: t.Union[t.Dict[str, t.Any], t.Any],
    ) -> None:
        if isinstance(query_or_dict, dict):
            for name, sub_query in query_or_dict.items():
                update_dict(
                    curr_path=[*curr_path, name],
                    dict_to_update=dict_to_update,
                    query_or_dict=sub_query,
                )
        else:
            dict_to_update[tuple(curr_path)] = t.cast(str, query_or_dict)
        return

    for name, query_or_dict in queries.items():
        update_dict(
            query_or_dict=query_or_dict,
            curr_path=[name],
            dict_to_update=final_dict,
        )

    return final_dict


def rename_and_translate_query(
    old_query: str,
    dialect: st.SQLDialect,
    destination_dialect: st.SQLDialect,
    table_mapping: t.Dict[st.Path, t.Tuple[str]],
    extended_table_mapping: t.Optional[t.List[str]],
) -> str:
    """Converts to postgres, parses query and then
    reconverts if needed"""

    # Translate to postgres
    new_query = str(
        translator.translate_to_postgres(
            ast_utils.parse_query(old_query),
            dialect,
        )
    )
    # Rename tables
    new_query = rename_tables.rename_tables(
        query_str=new_query,
        table_mapping=t.cast(
            t.Dict[st.Path, t.Tuple[str, ...]], table_mapping
        ),
        extended_table_mapping=extended_table_mapping,
    )
    if destination_dialect != st.SQLDialect.POSTGRES:
        new_query = str(
            translator.translate_to_dialect(
                ast_utils.parse_query(new_query),
                destination_dialect,
            )
        )
    return new_query


def nest_queries(
    queries: t.Dict[t.Tuple[str, ...], str]
) -> t.Dict[str, t.Any]:
    """It transform the dict of queries according to the tuple keys:
    if queries = {
            ('a','b'):'q',
            ('a','c'):'q'
    }
    the results woulf be: {a: {b: 'q', c: 'q'}

    if queries = {
            ('a','b'):'q',
            ('e','c'):'q'
    }
    the results woulf be: {a: {b: 'q'}, e: {c: 'q'}}
    """
    intermediate: t.Dict[str, t.Dict[t.Tuple[str, ...], t.Any]] = defaultdict(
        dict
    )
    final: t.Dict[str, t.Any] = {}
    for query_path, query in queries.items():
        if len(query_path) == 1:
            final[query_path[0]] = query
        else:
            intermediate[query_path[0]][query_path[1:]] = query

    for name, subdict in intermediate.items():
        final[name] = nest_queries(subdict)

    return final


def nested_dict_of_types(
    types: t.Dict[t.Tuple[str, ...], st.Type]
) -> t.Dict[str, t.Any]:
    """Similar to nest_queries but values are sarus types instead of strings"""
    intermediate: t.Dict[str, t.Dict[t.Tuple[str, ...], t.Any]] = defaultdict(
        dict
    )
    final: t.Dict[str, t.Any] = {}
    for type_path, type in types.items():
        if len(type_path) == 1:
            final[type_path[0]] = type
        else:
            intermediate[type_path[0]][type_path[1:]] = type

    for name, subdict in intermediate.items():
        final[name] = nested_dict_of_types(subdict)

    return final


def nested_unions_from_nested_dict_of_types(
    nested_types: t.Dict[str, t.Any]
) -> t.Dict[str, st.Type]:
    """create unions out of nested_types"""
    fields: t.Dict[str, st.Type] = {}
    for path_string, type_or_dict in nested_types.items():
        if isinstance(type_or_dict, dict):
            fields[path_string] = sdt.Union(
                nested_unions_from_nested_dict_of_types(type_or_dict)
            )
        else:
            fields[path_string] = type_or_dict
    return fields
