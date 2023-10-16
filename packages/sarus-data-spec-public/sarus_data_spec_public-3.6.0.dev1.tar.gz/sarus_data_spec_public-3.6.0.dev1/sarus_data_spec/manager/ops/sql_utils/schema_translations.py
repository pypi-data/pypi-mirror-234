"""Utils for translating sarus schema into other sql related schemas e.g.
sqlalchemy metadata.
"""
from enum import Enum
import typing as t
import warnings

from sarus_data_spec.constants import DATA
from sarus_data_spec.manager.async_utils import sync
import sarus_data_spec.typing as st

try:
    import sqlalchemy as sa
except ModuleNotFoundError:
    warnings.warn("Sqlalchemy not installed, cannot send sql queries")

try:
    from google.cloud import bigquery

except ImportError:
    warnings.warn(
        'Google API Python client and related libraries are not installed,'
        ' cannot push dataset to bigquery'
    )
    big_query_schema_field = t.Any
else:
    big_query_schema_field = bigquery.SchemaField  # type:ignore


def to_sqlalchemy_metadata(
    _type: st.Type,
    table: sa.Table,
    col_name: t.Optional[str] = None,
    nullable: bool = False,
    primary_keys: t.Optional[t.List[str]] = None,
    foreign_keys: t.Optional[t.Dict[str, str]] = None,
    administrative_cols: t.Optional[t.Dict[str, st.Type]] = None,
) -> None:
    # TODO check that if columns have a dot are quoted by sqlalchemy
    # if not we can force them to be always quoted
    """Visitor to create sqlalchemy metadata from a sarus type"""

    if administrative_cols is None:
        administrative_cols = {}
    if primary_keys is None:
        primary_keys = []
    if foreign_keys is None:
        foreign_keys = {}

    class ToSAMetaData(st.TypeVisitor):
        def Text(
            self,
            encoding: str,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert col_name
            table.append_column(
                sa.Column(
                    col_name, sa.types.Text, nullable=nullable, quote=True
                )
            )

        def Float(
            self,
            min: float,
            max: float,
            base: st.FloatBase,
            possible_values: t.Iterable[float],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert col_name
            table.append_column(
                sa.Column(
                    col_name, sa.types.Float, nullable=nullable, quote=True
                )
            )

        def Struct(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            for fieldname, fieldtype in fields.items():
                to_sqlalchemy_metadata(
                    fieldtype, table, col_name=fieldname, nullable=False
                )
            assert administrative_cols is not None
            for fieldname, fieldtype in administrative_cols.items():
                to_sqlalchemy_metadata(
                    fieldtype, table, col_name=fieldname, nullable=False
                )

            if primary_keys:
                table.append_constraint(
                    sa.PrimaryKeyConstraint(
                        *primary_keys, name=f'{table.name}_pks'
                    )
                )

            if foreign_keys:
                for key, value in foreign_keys.items():
                    table.append_constraint(
                        sa.ForeignKeyConstraint(
                            [key],
                            [value],
                        )
                    )

        def Union(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise ValueError()

        def Optional(
            self,
            type: st.Type,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert col_name
            to_sqlalchemy_metadata(
                type, table, col_name=col_name, nullable=True
            )

        def Datetime(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DatetimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert col_name
            table.append_column(
                sa.Column(
                    col_name, sa.types.DateTime, nullable=nullable, quote=True
                )
            )

        def Date(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DateBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert col_name
            table.append_column(
                sa.Column(
                    col_name, sa.types.Date, nullable=nullable, quote=True
                )
            )

        def Time(
            self,
            format: str,
            min: str,
            max: str,
            base: st.TimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert col_name
            table.append_column(
                sa.Column(
                    col_name, sa.types.Time, nullable=nullable, quote=True
                )
            )

        def Duration(
            self,
            unit: str,
            min: int,
            max: int,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert col_name
            table.append_column(
                sa.Column(
                    col_name, sa.types.Interval, nullable=nullable, quote=True
                )
            )

        def Array(
            self,
            type: st.Type,
            shape: t.Tuple[int, ...],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError()

        def Boolean(
            self,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert col_name
            table.append_column(
                sa.Column(
                    col_name, sa.types.Boolean, nullable=nullable, quote=True
                )
            )

        def Unit(
            self,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert col_name
            table.append_column(
                sa.Column(col_name, sa.types.String, nullable=True, quote=True)
            )

        def Bytes(
            self,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert col_name
            table.append_column(
                sa.Column(
                    col_name,
                    sa.types.LargeBinary,
                    nullable=nullable,
                    quote=True,
                )
            )

        def Constrained(
            self,
            type: st.Type,
            constraint: st.Predicate,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError()

        def Null(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            assert col_name
            table.append_column(
                sa.Column(
                    col_name, sa.types.NullType, nullable=nullable, quote=True
                )
            )

        def Enum(
            self,
            name: str,
            name_values: t.Sequence[t.Tuple[str, int]],
            ordered: bool,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert col_name
            enum = Enum(name, name_values)  # type: ignore
            table.append_column(
                sa.Column(
                    col_name,
                    sa.types.Enum(enum),
                    nullable=nullable,
                    quote=True,
                )
            )

        def Hypothesis(
            self,
            *types: t.Tuple[st.Type, float],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError()

        def Id(
            self,
            unique: bool,
            reference: t.Optional[st.Path] = None,
            base: t.Optional[st.IdBase] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert col_name
            if base:
                if base == st.IdBase.STRING:
                    table.append_column(
                        sa.Column(
                            col_name,
                            sa.types.String(450),
                            nullable=nullable,
                            quote=True,
                        )
                    )
                elif base == st.IdBase.BYTES:
                    table.append_column(
                        sa.Column(
                            col_name,
                            sa.types.BINARY,
                            nullable=nullable,
                            quote=True,
                        )
                    )
                else:
                    table.append_column(
                        sa.Column(
                            col_name,
                            sa.types.Integer,
                            nullable=nullable,
                            quote=True,
                        )
                    )

        def Integer(
            self,
            min: int,
            max: int,
            base: st.IntegerBase,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert col_name
            if base in [st.IntegerBase.INT8, st.IntegerBase.INT16]:
                table.append_column(
                    sa.Column(
                        col_name,
                        sa.types.SmallInteger,
                        nullable=nullable,
                        quote=True,
                    )
                )
            elif base == st.IntegerBase.INT32:
                table.append_column(
                    sa.Column(
                        col_name,
                        sa.types.Integer,
                        nullable=nullable,
                        quote=True,
                    )
                )
            else:
                table.append_column(
                    sa.Column(
                        col_name,
                        sa.types.BigInteger,
                        nullable=nullable,
                        quote=True,
                    )
                )

        def List(
            self,
            type: st.Type,
            max_size: int,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError()

    visitor = ToSAMetaData()
    _type.accept(visitor)


# https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#TableFieldSchema.FIELDS.mode
class BQFieldType(Enum):
    """big query column constraint"""

    # it accepts null
    NULLABLE = 'NULLABLE'
    # id donesn't accept null values
    REQUIRED = 'REQUIRED'
    # not used for the moment
    REPEATED = 'REPEATED'


def to_bq_schema(
    _type: st.Type,
    bq_schema: t.Dict[str, big_query_schema_field],
    col_name: t.Optional[str] = None,
    typemode: t.Optional[str] = None,
) -> None:
    """Visitor that associate to each column a bigquery.SchemaField
    containing the wanted column type.
    """

    class ToBQSchema(st.TypeVisitor):
        def Text(
            self,
            encoding: str,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert col_name
            assert typemode
            bq_schema[col_name] = bigquery.SchemaField(
                col_name, "STRING", mode=typemode
            )

        def Float(
            self,
            min: float,
            max: float,
            base: st.FloatBase,
            possible_values: t.Iterable[float],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert col_name
            assert typemode
            bq_schema[col_name] = bigquery.SchemaField(
                col_name, "FLOAT64", mode=typemode
            )

        def Struct(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            for fieldname, fieldtype in fields.items():
                to_bq_schema(
                    fieldtype,
                    bq_schema,
                    col_name=fieldname,
                    typemode=BQFieldType.REQUIRED.value,
                )

        def Union(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise ValueError()

        def Optional(
            self,
            type: st.Type,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert col_name
            to_bq_schema(
                type,
                bq_schema,
                col_name=col_name,
                typemode=BQFieldType.NULLABLE.value,
            )

        def Datetime(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DatetimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert col_name
            assert typemode
            bq_schema[col_name] = bigquery.SchemaField(
                col_name, "DATETIME", mode=typemode
            )

        def Date(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DateBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert col_name
            assert typemode
            bq_schema[col_name] = bigquery.SchemaField(
                col_name, "DATE", mode=typemode
            )

        def Time(
            self,
            format: str,
            min: str,
            max: str,
            base: st.TimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert col_name
            assert typemode
            bq_schema[col_name] = bigquery.SchemaField(
                col_name, "TIME", mode=typemode
            )

        def Duration(
            self,
            unit: str,
            min: int,
            max: int,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError()

        def Array(
            self,
            type: st.Type,
            shape: t.Tuple[int, ...],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError()

        def Boolean(
            self,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert col_name
            assert typemode
            bq_schema[col_name] = bigquery.SchemaField(
                col_name, "BOOL", mode=typemode
            )

        def Unit(
            self,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            # Since big query has no type Null
            # We are considering as a nullable string
            assert col_name
            assert typemode
            bq_schema[col_name] = bigquery.SchemaField(
                col_name, "STRING", mode=BQFieldType.NULLABLE.value
            )

        def Bytes(
            self,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert col_name
            assert typemode
            bq_schema[col_name] = bigquery.SchemaField(
                col_name, "BYTES", mode=typemode
            )

        def Constrained(
            self,
            type: st.Type,
            constraint: st.Predicate,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError()

        def Null(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            # treated in the same way as in Unit
            assert col_name
            assert typemode
            bq_schema[col_name] = bigquery.SchemaField(
                col_name, "STRING", mode=BQFieldType.NULLABLE.value
            )

        def Enum(
            self,
            name: str,
            name_values: t.Sequence[t.Tuple[str, int]],
            ordered: bool,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert col_name
            assert typemode
            bq_schema[col_name] = bigquery.SchemaField(
                col_name, bigquery.enums.SqlTypeNames.STRING, mode=typemode
            )

        def Hypothesis(
            self,
            *types: t.Tuple[st.Type, float],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError()

        def Id(
            self,
            unique: bool,
            reference: t.Optional[st.Path] = None,
            base: t.Optional[st.IdBase] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert col_name
            assert typemode
            if base:
                if base == st.IdBase.STRING:
                    bq_schema[col_name] = bigquery.SchemaField(
                        col_name, "STRING", mode=typemode
                    )
                elif base == st.IdBase.BYTES:
                    bq_schema[col_name] = bigquery.SchemaField(
                        col_name, "BYTES", mode=typemode
                    )
                else:
                    bq_schema[col_name] = bigquery.SchemaField(
                        col_name, "INTEGER", mode=typemode
                    )

        def Integer(
            self,
            min: int,
            max: int,
            base: st.IntegerBase,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            assert col_name
            assert typemode
            bq_schema[col_name] = bigquery.SchemaField(
                col_name, "INT64", mode=typemode
            )

        def List(
            self,
            type: st.Type,
            max_size: int,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError()

    visitor = ToBQSchema()
    _type.accept(visitor)


async def async_sa_metadata_from_dataset(dataset: st.Dataset) -> sa.MetaData:
    metadata = sa.MetaData()
    manager = dataset.manager()
    schema = await manager.async_schema(dataset)
    tables = schema.tables()
    schema_type = schema.type()
    if schema_type.has_admin_columns():
        additional_cols = schema_type.children()
        additional_cols.pop(DATA)

    else:
        additional_cols = {}
    for table_path in tables:
        explicit_table_path = table_path.to_strings_list()[0]
        qualified_tablename = (
            explicit_table_path[1:]
            if explicit_table_path[0] == DATA
            else explicit_table_path
        )
        table_type = schema.data_type().sub_types(table_path)[0]
        table_name = ".".join([f'"{name}"' for name in qualified_tablename])
        # we create a fully qualified name for the table
        # it also needs to be quoted in order to deal with dots in names
        # with allows that tables in the rendered queries are fully
        # qualified to avoid amibous names.
        sa_tabmetadata = sa.Table(table_name, metadata, quote=False)
        to_sqlalchemy_metadata(
            table_type, sa_tabmetadata, administrative_cols=additional_cols
        )
    return metadata


def sa_metadata_from_dataset(dataset: st.Dataset) -> t.Any:
    return sync(async_sa_metadata_from_dataset(dataset))
