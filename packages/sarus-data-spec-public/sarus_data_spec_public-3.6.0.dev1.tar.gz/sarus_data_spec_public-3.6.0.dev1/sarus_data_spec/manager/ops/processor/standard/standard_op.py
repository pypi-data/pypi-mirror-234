import hashlib
import logging
import typing as t
import warnings

import pyarrow as pa

from sarus_data_spec.dataset import Dataset
from sarus_data_spec.manager.ops.base import (
    DatasetImplementation,
    DatasetStaticChecker,
    DataspecStaticChecker,
    ScalarImplementation,
    _ensure_batch_correct,
)

try:
    from sarus_data_spec.manager.ops.sql_utils.table_mapping import (
        name_encoder,
        table_mapping,
    )
except ModuleNotFoundError:
    warnings.warn('table_mapping not found. Cannot send sql queries.')
try:
    from sarus_data_spec.manager.ops.sql_utils.queries import (
        rename_and_compose_queries,
    )
except ModuleNotFoundError:
    warnings.warn('Queries composition not available.')
from sarus_data_spec.scalar import Scalar
import sarus_data_spec.typing as st

logger = logging.getLogger(__name__)


class StandardDatasetStaticChecker(DatasetStaticChecker):
    def parent(self, kind: str = 'dataset') -> t.Union[st.Dataset, st.Scalar]:
        return parent(self.dataset, kind=kind)

    async def parent_schema(self) -> st.Schema:
        parent = self.parent(kind='dataset')
        assert isinstance(parent, Dataset)
        return await parent.manager().async_schema(parent)

    async def parent_marginals(self) -> st.Marginals:
        parent = self.parent(kind='dataset')
        assert isinstance(parent, Dataset)
        return await parent.manager().async_marginals(parent)

    def pep_token(self, public_context: t.Collection[str]) -> t.Optional[str]:
        """By default we implement that the transform inherits the PEP status
        but changes the PEP token."""
        parent_token = self.parent().pep_token()
        if parent_token is None:
            return None

        transform = self.dataset.transform()
        h = hashlib.md5()
        h.update(parent_token.encode("ascii"))
        h.update(transform.protobuf().SerializeToString())

        return h.hexdigest()


class StandardDatasetImplementation(DatasetImplementation):
    """Object that executes first routing among ops between
    transformed/source and processor
    """

    def parents(self) -> t.List[t.Union[st.DataSpec, st.Transform]]:
        return parents(self.dataset)

    def parent(self, kind: str = 'dataset') -> t.Union[st.Dataset, st.Scalar]:
        return parent(self.dataset, kind=kind)

    async def parent_to_arrow(
        self, batch_size: int = 10000
    ) -> t.AsyncIterator[pa.RecordBatch]:
        parent = self.parent(kind='dataset')
        assert isinstance(parent, Dataset)
        parent_iterator = await parent.manager().async_to_arrow(
            parent, batch_size=batch_size
        )
        return await self.decoupled_async_iter(parent_iterator)

    async def parent_schema(self) -> st.Schema:
        parent = self.parent(kind='dataset')
        assert isinstance(parent, Dataset)
        return await parent.manager().async_schema(parent)

    async def parent_value(self) -> t.Any:
        parent = self.parent(kind='scalar')
        assert isinstance(parent, Scalar)
        return await parent.manager().async_value(parent)

    async def parent_size(self) -> st.Size:
        parent = self.parent(kind='dataset')
        assert isinstance(parent, Dataset)
        return await parent.manager().async_size(parent)

    async def parent_multiplicity(self) -> st.Multiplicity:
        parent = self.parent(kind='dataset')
        assert isinstance(parent, Dataset)
        return await parent.manager().async_multiplicity(parent)

    async def parent_bounds(self) -> st.Bounds:
        parent = self.parent(kind='dataset')
        assert isinstance(parent, Dataset)
        return await parent.manager().async_bounds(parent)

    async def parent_marginals(self) -> st.Marginals:
        parent = self.parent(kind='dataset')
        assert isinstance(parent, Dataset)
        return await parent.manager().async_marginals(parent)

    async def ensure_batch_correct(
        self,
        async_iterator: t.AsyncIterator[pa.RecordBatch],
        func_to_apply: t.Callable,
        batch_size: int,
    ) -> t.AsyncIterator[pa.RecordBatch]:
        """Method that executes func_to_apply on each batch
        of the async_iterator but rather than directly returning
        the result, it accumulates them and returns them progressively
        so that each new batch has batch_size."""

        return _ensure_batch_correct(async_iterator, func_to_apply, batch_size)

    async def sql_implementation(
        self,
    ) -> t.Optional[t.Dict[t.Tuple[str, ...], str]]:
        """Returns a dict of queries equivalent to the current transform.
        If the the transform does not change the schema, then return None"""
        raise NotImplementedError(
            "No SQL implementation for dataset issued from"
            f" {self.dataset.transform().spec()} transform."
        )

    async def sql(
        self,
        query: t.Union[str, t.Dict[str, t.Any]],
        dialect: t.Optional[st.SQLDialect] = None,
        batch_size: int = 10000,
        result_type: t.Optional[st.Type] = None,
    ) -> t.AsyncIterator[pa.RecordBatch]:
        """It rewrites and/or composes the query and sends it to the parent."""
        queries_transform = await self.sql_implementation()
        current_schema = await self.dataset.manager().async_schema(
            self.dataset
        )
        parent_schema = await self.parent_schema()
        if (
            queries_transform is None
            and current_schema.name() == parent_schema.name()
        ):
            parent_query = query
        else:
            table_map = {}
            if queries_transform is not None:
                table_map = table_mapping(
                    tables=current_schema.tables(),
                    sarus_schema_name=current_schema.name(),
                    encoded_name_length=10,
                    encoder_prefix_name=self.dataset.uuid(),
                )
            updated_queries_transform = (
                {
                    name_encoder(
                        names=(self.dataset.uuid(), *tab_name),
                        length=10,
                    ): query_str
                    for tab_name, query_str in queries_transform.items()
                }
                if queries_transform is not None
                else None
            )

            parent_query = rename_and_compose_queries(
                query_or_dict=query,
                curr_path=[],
                queries_transform=updated_queries_transform,
                table_map=table_map,
            )

        parent_ds = t.cast(st.Dataset, self.parent(kind='dataset'))
        logger.debug(
            f"query {parent_query} sent to the "
            f"parent dataset {parent_ds.uuid()}"
        )
        return await parent_ds.manager().async_sql(
            dataset=parent_ds,
            query=parent_query,
            dialect=dialect,
            batch_size=batch_size,
            result_type=result_type,
        )


class StandardScalarStaticChecker(DataspecStaticChecker):
    ...


class StandardScalarImplementation(ScalarImplementation):
    def parent(self, kind: str = 'dataset') -> st.DataSpec:
        return parent(self.scalar, kind=kind)

    def parents(self) -> t.List[t.Union[st.DataSpec, st.Transform]]:
        return parents(self.scalar)

    async def parent_to_arrow(
        self, batch_size: int = 10000
    ) -> t.AsyncIterator[pa.RecordBatch]:
        parent = self.parent(kind='dataset')
        assert isinstance(parent, Dataset)
        parent_iterator = await parent.manager().async_to_arrow(
            parent, batch_size=batch_size
        )
        return await self.decoupled_async_iter(parent_iterator)

    async def parent_schema(self) -> st.Schema:
        parent = self.parent(kind='dataset')
        assert isinstance(parent, Dataset)
        return await parent.manager().async_schema(parent)

    async def parent_value(self) -> t.Any:
        parent = self.parent(kind='scalar')
        assert isinstance(parent, Scalar)
        return await parent.manager().async_value(parent)


def parent(dataspec: st.DataSpec, kind: str) -> t.Union[st.Dataset, st.Scalar]:
    pars = parents(dataspec)
    if kind == 'dataset':
        parent: t.Union[t.List[Scalar], t.List[Dataset]] = [
            element for element in pars if isinstance(element, Dataset)
        ]
    else:
        parent = [element for element in pars if isinstance(element, Scalar)]
    assert len(parent) == 1
    return parent[0]


def parents(
    dataspec: st.DataSpec,
) -> t.List[t.Union[st.DataSpec, st.Transform]]:
    parents_args, parents_kwargs = dataspec.parents()
    parents_args.extend(parents_kwargs.values())
    return parents_args
