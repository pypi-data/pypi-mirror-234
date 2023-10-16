import typing as t
import warnings

import pyarrow as pa

from sarus_data_spec.attribute import attach_properties
from sarus_data_spec.bounds import bounds as bounds_builder
from sarus_data_spec.marginals import marginals as marginals_builder
from sarus_data_spec.multiplicity import multiplicity as multiplicity_builder
from sarus_data_spec.size import size as size_builder
import sarus_data_spec.typing as st

try:
    from sarus_synthetic_data.synthetic_generator.generator import (
        SyntheticGenerator,
    )

except ModuleNotFoundError:
    warnings.warn(
        'sarus-synthetic-data Module not found, synthetic data operations not '
        'available '
    )

from sarus_data_spec.constants import (
    DATASET_SLUGNAME,
    SYNTHETIC_MODEL,
    SYNTHETIC_TASK,
    TRAIN_CORRELATIONS,
)
from sarus_data_spec.dataset import Dataset

try:
    from sarus_data_spec.manager.ops.source.query_builder import (
        synthetic_parameters,
    )
except ModuleNotFoundError:
    warnings.warn(
        "synthetic_parameters not found, "
        "synthetic data operations not available "
    )
from sarus_data_spec.scalar import Scalar
from sarus_data_spec.schema import schema

from .standard_op import (
    StandardDatasetImplementation,
    StandardDatasetStaticChecker,
    StandardScalarImplementation,
    StandardScalarStaticChecker,
)

MAX_SIZE = 1e6  # TODO: in sarus_data_spec.constants ?


def convert_array_to_table(
    schema_type: st.Type, arrow_data: pa.array
) -> pa.Array:
    """Given a PyArrow array, returns a correctly-defined Table."""

    class ArrayToTable(st.TypeVisitor):
        """Handles both configuration: a dataset as a Struct or as an Union."""

        result = None

        def Struct(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            names = list(fields.keys())
            self.result = pa.Table.from_arrays(
                arrays=arrow_data.flatten(), names=names
            )

        def Union(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            names = list(fields.keys())
            arrs = arrow_data.flatten()
            schema = pa.schema(
                [
                    pa.field(name, type=arr.type)
                    for arr, name in zip(arrs[:-1], names)
                ]
            )
            schema = schema.append(
                pa.field('field_selected', type=pa.string(), nullable=False)
            )
            self.result = pa.Table.from_arrays(
                arrays=arrow_data.flatten(), schema=schema
            )

        def Null(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            raise NotImplementedError

        def Unit(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            raise NotImplementedError

        def Boolean(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            raise NotImplementedError

        def Id(
            self,
            unique: bool,
            reference: t.Optional[st.Path] = None,
            base: t.Optional[st.IdBase] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Integer(
            self,
            min: int,
            max: int,
            base: st.IntegerBase,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Enum(
            self,
            name: str,
            name_values: t.Sequence[t.Tuple[str, int]],
            ordered: bool,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Float(
            self,
            min: float,
            max: float,
            base: st.FloatBase,
            possible_values: t.Iterable[float],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Text(
            self,
            encoding: str,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Bytes(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            raise NotImplementedError

        def Optional(
            self,
            type: st.Type,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def List(
            self,
            type: st.Type,
            max_size: int,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Array(
            self,
            type: st.Type,
            shape: t.Tuple[int, ...],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Datetime(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DatetimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Time(
            self,
            format: str,
            min: str,
            max: str,
            base: st.TimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Date(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DateBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Duration(
            self,
            unit: str,
            min: int,
            max: int,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Constrained(
            self,
            type: st.Type,
            constraint: st.Predicate,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Hypothesis(
            self,
            *types: t.Tuple[st.Type, float],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

    visitor = ArrayToTable()
    schema_type.accept(visitor)
    return visitor.result


async def async_iter_arrow(
    iterator: t.Iterator[pa.RecordBatch],
) -> t.AsyncIterator[pa.RecordBatch]:
    """Async generator from the synthetic data iterator."""
    for batch in iterator:
        yield batch
    return


class SyntheticStaticChecker(StandardDatasetStaticChecker):
    def pep_token(self, public_context: t.Collection[str]) -> t.Optional[str]:
        # TODO add pep token when the synthetic data is actually protected
        return None

    async def schema(self) -> st.Schema:
        parent_schema = await self.parent_schema()
        return schema(
            self.dataset,
            schema_type=parent_schema.data_type(),
            properties=parent_schema.properties(),
            name=self.dataset.properties().get(DATASET_SLUGNAME, None),
        )


class Synthetic(StandardDatasetImplementation):
    """Create a Synthetic op class for is_pep."""

    async def to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        dataset = self.dataset
        parents, parents_dict = dataset.parents()

        # Forcing the marginals to be computed first
        parent = t.cast(Dataset, parents[0])
        _ = await parent.manager().async_marginals(parent)

        # Budget
        budget_param = parents_dict['sd_budget']
        budget = t.cast(
            t.Tuple[float, float],
            await dataset.manager().async_value(t.cast(Scalar, budget_param)),
        )

        # Model
        correlations_scalar = t.cast(Scalar, parents_dict['synthetic_model'])
        train_correlations = t.cast(
            bool, await dataset.manager().async_value(correlations_scalar)
        )

        # Generator params
        generator_params = await synthetic_parameters(
            dataset,
            sd_budget=budget,
            task=SYNTHETIC_TASK,
            train_correlations=train_correlations,
        )
        # Links computation
        _ = await self.dataset.manager().async_links(self.dataset)
        # compute
        generator = SyntheticGenerator(dataset, generator_params.generator)
        dataset_schema = await dataset.manager().async_schema(dataset)
        datatype = dataset_schema.type()
        generator.train()
        sample = generator.sample()
        table = convert_array_to_table(datatype, sample)
        return async_iter_arrow(table.to_batches(max_chunksize=batch_size))

    async def size(self) -> st.Size:
        parent_size = await self.parent_size()
        return size_builder(self.dataset, parent_size.statistics())

    async def multiplicity(self) -> st.Multiplicity:
        parent_multiplicity = await self.parent_multiplicity()
        return multiplicity_builder(
            self.dataset, parent_multiplicity.statistics()
        )

    async def bounds(self) -> st.Bounds:
        parent_bounds = await self.parent_bounds()
        return bounds_builder(self.dataset, parent_bounds.statistics())

    async def marginals(self) -> st.Marginals:
        parent_marginals = await self.parent_marginals()
        return marginals_builder(self.dataset, parent_marginals.statistics())


class SamplingRatiosStaticChecker(StandardScalarStaticChecker):
    ...


class SamplingRatios(StandardScalarImplementation):
    """Computes the sampling ratios for the SD
    of the dataspec given the total budget"""

    async def value(self) -> t.Any:
        dataset = t.cast(st.Dataset, self.parent())
        out = {}
        for table_path in (await self.parent_schema()).tables():
            sizes = await dataset.manager().async_size(dataset)
            assert sizes
            stat = sizes.statistics().nodes_statistics(table_path)[0]
            out[table_path] = min(1, MAX_SIZE / stat.size())
        return out


class SyntheticModelStaticChecker(StandardScalarStaticChecker):
    ...


class SyntheticModel(StandardScalarImplementation):
    """Computes the synthetic model to use"""

    async def value(self) -> t.Any:
        attribute = self.scalar.attribute(name=SYNTHETIC_MODEL)
        if attribute is None:
            attach_properties(
                self.scalar,
                name=SYNTHETIC_MODEL,
                properties={TRAIN_CORRELATIONS: str(True)},
            )
            return True
        return attribute.properties()[TRAIN_CORRELATIONS] == str(True)
