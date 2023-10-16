import logging
import typing as t

import numpy as np
import pandas as pd

from sarus_data_spec.constants import MAX_MAX_MULT
from sarus_data_spec.dataspec_validator.signature import SarusBoundSignature
from sarus_data_spec.protobuf.utilities import unwrap
import sarus_data_spec.typing as st

from ..external_op import ExternalOpImplementation

logger = logging.getLogger(__name__)

try:
    from sarus_statistics.ops.bounds.op import BoundOp
    from sarus_statistics.ops.corr.op import CorrOp
    from sarus_statistics.ops.histograms.op import CountOp, HistogramOp
    from sarus_statistics.ops.max_multiplicity.op import MaxMultiplicityOp
    from sarus_statistics.ops.mean.op import MeanOp
    from sarus_statistics.ops.median.op import MedianOp
    from sarus_statistics.ops.std.op import StdOp
    from sarus_statistics.ops.sum.op import SumOp
    from sarus_statistics.protobuf.multiplicity_pb2 import (
        MultiplicityParameters,
    )
except ModuleNotFoundError as e_pandas_dp:
    if "sarus_statistics" not in str(e_pandas_dp):
        raise

try:
    from sarus_differential_privacy.query import ComposedPrivateQuery
except ModuleNotFoundError as e_pandas_dp:
    if "sarus_differential_privacy" not in str(e_pandas_dp):
        raise

try:
    from sarus_query_builder.builders.bounds_builder import (
        simple_bounds_builder,
    )
    from sarus_query_builder.builders.composed_builder import (
        simple_composed_builder,
    )
    from sarus_query_builder.builders.corr_builder import (
        corr_builder as simple_corr_builder,
    )
    from sarus_query_builder.builders.max_multiplicity_builder import (
        simple_max_multiplicity_builder,
    )
    from sarus_query_builder.builders.mean_builder import mean_builder
    from sarus_query_builder.builders.median_builder import median_builder
    from sarus_query_builder.builders.standard_mechanisms_builder import (
        laplace_builder,
    )
    from sarus_query_builder.builders.std_builder import std_builder
    from sarus_query_builder.builders.sum_builder import sum_builder
    from sarus_query_builder.core.core import OptimizableQueryBuilder
    from sarus_query_builder.protobuf.query_pb2 import GenericTask, Query
except ModuleNotFoundError as e_pandas_dp:
    if "sarus_query_builder" not in str(e_pandas_dp):
        raise


DEFAULT_MAX_MAX_MULT = 1
NUMERIC_TYPES = ('integer', 'float', 'boolean')


class pd_shape_dp(ExternalOpImplementation):
    _transform_id = "pandas.PD_SHAPE_DP"
    _non_dp_equivalent_id = "pandas.PD_SHAPE"

    def is_dp(self, signature: SarusBoundSignature) -> bool:
        return True

    async def private_queries_and_task(
        self, signature: SarusBoundSignature
    ) -> t.Tuple[t.List[st.PrivateQuery], st.Task]:
        """Return the PrivateQueries summarizing DP characteristics."""
        parent_ds = signature["this"].static_value()
        epsilon, delta = await get_budget(signature)

        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_max_mult = int(
            parent_schema.properties().get(MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT)
        )

        builder = simple_composed_builder(
            parent_ds,
            [
                simple_max_multiplicity_builder(
                    parent_ds,
                    Query(
                        max_multiplicity=Query.MaxMultiplicity(
                            max_max_multiplicity=max_max_mult
                        )
                    ),
                ),
                laplace_builder(
                    parent_ds,
                    Query(laplace_mechanism=Query.LaplaceMechanism()),
                ),
            ],
        )
        tasks = builder.build_query(
            builder.target([(epsilon, delta)], (0, epsilon))
        )
        query = builder.private_query(tasks)
        composed_query = t.cast(ComposedPrivateQuery, query)
        return list(composed_query.all_subqueries()), tasks

    async def call_dp(self, signature: SarusBoundSignature) -> t.Any:
        """Implementation of DP shape.

        A DP implementation receives additional arguments compared to a
        standard external implementation:
            - `budget`: a list of sp.Scalar.PrivacyParams.Point
                object containing each an epsilon and a delta values
            - `seed`: an integer used to parametrize random number generators
            - `pe`: the protected entity used by `sarus_statistics` primitives
        """
        # Evaluate arguments
        parent_ds = signature.static_kwargs()["this"]
        (dataframe, budget, seed) = await signature.collect_args()

        # Get QB task parametrization
        _, tasks = await self.private_queries_and_task(signature)

        epsilon = budget[0].epsilon
        shape = dataframe.shape

        # Compute DP value
        tasks = [unwrap(subtask) for subtask in tasks.subtasks]
        max_mult_task, shape_task = t.cast(
            MultiplicityParameters, tasks[0]
        ), t.cast(GenericTask, tasks[1])
        random_generator = np.random.default_rng(abs(seed))
        max_mul = MaxMultiplicityOp(
            parent_ds,
            epsilon,  # parameter for quantiles
            max_mult_task.noise_user_count,
            max_mult_task.noise_multiplicity,
            max_mult_task.max_max_multiplicity,
        ).value(random_generator)

        n_rows = CountOp(
            parent_ds,
            noise=shape_task.parameters['noise'],
        ).value(None, max_mul, random_generator)

        dp_shape = (n_rows, *shape[1:])
        return dp_shape


class pd_sum_dp(ExternalOpImplementation):
    _transform_id = "pandas.PD_SUM_DP"
    _non_dp_equivalent_id = "pandas.PD_SUM"

    def is_dp(self, signature: SarusBoundSignature) -> bool:
        """`axis = 0` and `numeric_only` is `True`"""
        if signature["this"].python_type() == str(pd.Series):
            return True

        axis = signature["axis"].static_value()
        numeric_only = signature["numeric_only"].static_value()
        return (axis == 0) and (numeric_only is True)

    async def private_queries_and_task(
        self, signature: SarusBoundSignature
    ) -> t.Tuple[t.List[st.PrivateQuery], st.Task]:
        parent_ds = signature["this"].static_value()
        epsilon, delta = await get_budget(signature)

        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_max_mult = int(
            parent_schema.properties().get(MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT)
        )
        n_cols = len(parent_schema.data_type().children())

        max_mult_builder: OptimizableQueryBuilder = (
            simple_max_multiplicity_builder(
                parent_ds,
                Query(
                    max_multiplicity=Query.MaxMultiplicity(
                        max_max_multiplicity=max_max_mult
                    )
                ),
            )
        )

        column_bounds_sum_builder: OptimizableQueryBuilder = (
            simple_composed_builder(
                parent_ds,
                [
                    simple_bounds_builder(
                        parent_ds, Query(bounds=Query.Bounds())
                    ),
                    sum_builder(parent_ds, Query(sum=Query.Sum())),
                ],
            )
        )

        builder = simple_composed_builder(
            parent_ds,
            [max_mult_builder] + n_cols * [column_bounds_sum_builder],
        )
        tasks = builder.build_query(
            builder.target([(epsilon, delta)], (0, epsilon))
        )
        query = builder.private_query(tasks)
        composed_query = t.cast(ComposedPrivateQuery, query)
        return list(composed_query.all_subqueries()), tasks

    async def call_dp(self, signature: SarusBoundSignature) -> t.Any:
        # Evaluate arguments
        parent_ds: st.Dataset = signature["this"].static_value()
        dataframe: pd.DataFrame = await parent_ds.async_to(pd.DataFrame)
        budget_value = await signature["budget"].collect()
        seed_value = await signature["seed"].collect()
        skipna = await signature["skipna"].collect()

        _, tasks = await self.private_queries_and_task(signature)

        epsilon = budget_value[0].epsilon
        # Compute DP value
        tasks = [unwrap(subtask) for subtask in tasks.subtasks]
        max_mult_task, sum_tasks = tasks[0], tasks[1:]
        random_generator = np.random.default_rng(abs(seed_value))
        max_mul = MaxMultiplicityOp(
            parent_ds,
            epsilon,  # parameter for quantiles
            max_mult_task.noise_user_count,
            max_mult_task.noise_multiplicity,
            max_mult_task.max_max_multiplicity,
        ).value(random_generator)

        sum_dp_dict = {}
        for index, column_name in enumerate(dataframe.columns):
            subtasks = [unwrap(task) for task in sum_tasks[index].subtasks]
            bounds_parameters, sum_parameters = t.cast(
                GenericTask, subtasks[0]
            ), t.cast(GenericTask, subtasks[1])
            column_type = (
                parent_ds.schema()
                .data_type()
                .children()[column_name]
                .protobuf()
            )
            if column_type.WhichOneof('type') == 'optional':
                if not skipna:
                    sum_dp_dict[column_name] = np.nan
                    continue
                column_type = column_type.optional.type
            if column_type.WhichOneof('type') not in NUMERIC_TYPES:
                continue

            # TODO parent_ds doesn't have a size
            # if parent_ds.size().children()[column_name].size() < min_count:
            #     sum_dp_dict[column_name] = np.nan
            #     continue

            bounds = BoundOp(
                parent_ds,
                bounds_parameters.parameters['noise'],
            ).value(column_name, max_mul, random_generator)
            sum_op = SumOp(
                parent_ds,
                sum_parameters.parameters['noise'],
            )
            sum_dp_dict[column_name] = sum_op.value(
                column_name, max_mul, bounds, random_generator
            )

        if signature["this"].python_type() == str(pd.DataFrame):
            sum_dp = pd.Series(sum_dp_dict)
        else:
            sum_dp = list(sum_dp_dict.values()).pop()

        return sum_dp


class pd_mean_dp(ExternalOpImplementation):
    _transform_id = "pandas.PD_MEAN_DP"
    _non_dp_equivalent_id = "pandas.PD_MEAN"

    def is_dp(self, signature: SarusBoundSignature) -> bool:
        """`axis = 0` and `numeric_only` is `True`"""
        if signature["this"].python_type() == str(pd.Series):
            return True

        axis = signature["axis"].static_value()
        numeric_only = signature["numeric_only"].static_value()
        return (axis == 0) and (numeric_only is True)

    async def private_queries_and_task(
        self, signature: SarusBoundSignature
    ) -> t.Tuple[t.List[st.PrivateQuery], st.Task]:
        parent_ds = signature["this"].static_value()
        epsilon, delta = await get_budget(signature)

        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_max_mult = int(
            parent_schema.properties().get(MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT)
        )
        n_cols = len(parent_schema.data_type().children())

        max_mult_builder: OptimizableQueryBuilder = (
            simple_max_multiplicity_builder(
                parent_ds,
                Query(
                    max_multiplicity=Query.MaxMultiplicity(
                        max_max_multiplicity=max_max_mult
                    )
                ),
            )
        )
        column_bounds_mean_builder: OptimizableQueryBuilder = (
            simple_composed_builder(
                parent_ds,
                [
                    simple_bounds_builder(
                        parent_ds, Query(bounds=Query.Bounds())
                    ),
                    mean_builder(parent_ds, Query(mean=Query.Mean())),
                ],
            )
        )
        builder = simple_composed_builder(
            parent_ds,
            [max_mult_builder] + n_cols * [column_bounds_mean_builder],
        )
        tasks = builder.build_query(
            builder.target([(epsilon, delta)], (0, epsilon))
        )
        query = builder.private_query(tasks)
        composed_query = t.cast(ComposedPrivateQuery, query)
        return list(composed_query.all_subqueries()), tasks

    async def call_dp(self, signature: SarusBoundSignature) -> t.Any:
        # Evaluate arguments
        parent_ds: st.Dataset = signature["this"].static_value()
        dataframe: pd.DataFrame = await parent_ds.async_to(pd.DataFrame)
        budget_value = await signature["budget"].collect()
        seed_value = await signature["seed"].collect()
        skipna = await signature["skipna"].collect()
        pe = (await signature.admin_data()).to_pandas()

        _, tasks = await self.private_queries_and_task(signature)

        tasks = [unwrap(subtask) for subtask in tasks.subtasks]
        max_mult_task, mean_tasks = tasks[0], tasks[1:]

        # Compute DP value
        random_generator = np.random.default_rng(abs(seed_value))
        epsilon = budget_value[0].epsilon
        max_mul = MaxMultiplicityOp(
            parent_ds,
            epsilon,  # parameter for quantiles
            max_mult_task.noise_user_count,
            max_mult_task.noise_multiplicity,
            max_mult_task.max_max_multiplicity,
        ).value(random_generator)

        mean_dp_dict = {}
        for index, column_name in enumerate(dataframe.columns):
            df = dataframe[[column_name]].join(pe)
            subtasks = [unwrap(task) for task in mean_tasks[index].subtasks]
            bounds_parameters, mean_parameters = t.cast(
                GenericTask, subtasks[0]
            ), t.cast(GenericTask, subtasks[1])
            column_type = (
                parent_ds.schema()
                .data_type()
                .children()[column_name]
                .protobuf()
            )
            if column_type.WhichOneof('type') == 'optional':
                if not skipna:
                    mean_dp_dict[column_name] = np.nan
                    continue
                column_type = column_type.optional.type
                df = df.dropna()
            if column_type.WhichOneof('type') not in NUMERIC_TYPES:
                continue

            bounds = BoundOp(
                parent_ds,
                bounds_parameters.parameters['noise'],
            ).value(column_name, max_mul, random_generator)
            mean_op = MeanOp(
                parent_ds,
                mean_parameters.parameters['noise'],
            )
            mean_dp_dict[column_name] = mean_op.value(
                column_name, max_mul, bounds, random_generator
            )

        if signature["this"].python_type() == str(pd.DataFrame):
            mean_dp = pd.Series(mean_dp_dict)
        else:
            mean_dp = list(mean_dp_dict.values()).pop()

        return mean_dp


class pd_median_dp(ExternalOpImplementation):
    _transform_id = "pandas.PD_MEDIAN_DP"
    _non_dp_equivalent_id = "pandas.PD_MEDIAN"

    def is_dp(self, signature: SarusBoundSignature) -> bool:
        """`axis = 0` and `numeric_only` is `True`"""
        if signature["this"].python_type() == str(pd.Series):
            return True

        axis = signature["axis"].static_value()
        numeric_only = signature["numeric_only"].static_value()
        return axis == 0 and numeric_only is True

    async def private_queries_and_task(
        self, signature: SarusBoundSignature
    ) -> t.Tuple[t.List[st.PrivateQuery], st.Task]:
        parent_ds = signature["this"].static_value()
        epsilon, delta = await get_budget(signature)

        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_max_mult = int(
            parent_schema.properties().get(MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT)
        )
        n_cols = len(parent_schema.data_type().children())

        max_mult_builder: OptimizableQueryBuilder = (
            simple_max_multiplicity_builder(
                parent_ds,
                Query(
                    max_multiplicity=Query.MaxMultiplicity(
                        max_max_multiplicity=max_max_mult
                    )
                ),
            )
        )
        column_bounds_median_builder: OptimizableQueryBuilder = (
            simple_composed_builder(
                parent_ds,
                [
                    simple_bounds_builder(
                        parent_ds, Query(bounds=Query.Bounds())
                    ),
                    median_builder(parent_ds, Query(median=Query.Median())),
                ],
            )
        )

        builder = simple_composed_builder(
            parent_ds,
            [max_mult_builder] + n_cols * [column_bounds_median_builder],
        )
        tasks = builder.build_query(
            builder.target([(epsilon, delta)], (0, epsilon))
        )
        query = builder.private_query(tasks)
        composed_query = t.cast(ComposedPrivateQuery, query)
        return list(composed_query.all_subqueries()), tasks

    async def call_dp(self, signature: SarusBoundSignature) -> t.Any:
        # Evaluate arguments
        parent_ds: st.Dataset = signature["this"].static_value()
        dataframe: pd.DataFrame = await parent_ds.async_to(pd.DataFrame)
        budget_value = await signature["budget"].collect()
        seed_value = await signature["seed"].collect()
        skipna = await signature["skipna"].collect()
        pe = (await signature.admin_data()).to_pandas()

        _, tasks = await self.private_queries_and_task(signature)
        tasks = [unwrap(subtask) for subtask in tasks.subtasks]
        max_mult_task, median_tasks = tasks[0], tasks[1:]

        random_generator = np.random.default_rng(abs(seed_value))
        epsilon = budget_value[0].epsilon

        # Compute DP value
        max_mul = MaxMultiplicityOp(
            parent_ds,
            epsilon,  # parameter for quantiles
            max_mult_task.noise_user_count,
            max_mult_task.noise_multiplicity,
            max_mult_task.max_max_multiplicity,
        ).value(random_generator)

        median_dp_dict = {}
        for index, column_name in enumerate(dataframe.columns):
            df = dataframe[[column_name]].join(pe)
            subtasks = [unwrap(task) for task in median_tasks[index].subtasks]
            bounds_parameters, median_parameters = t.cast(
                GenericTask, subtasks[0]
            ), t.cast(GenericTask, subtasks[1])
            column_type = (
                parent_ds.schema()
                .data_type()
                .children()[column_name]
                .protobuf()
            )
            if column_type.WhichOneof('type') == 'optional':
                if not skipna:
                    median_dp_dict[column_name] = np.nan
                    continue
                column_type = column_type.optional.type
                df = df.dropna()
            if column_type.WhichOneof('type') not in NUMERIC_TYPES:
                continue

            bounds = BoundOp(
                parent_ds,
                bounds_parameters.parameters['noise'],
            ).value(column_name, max_mul, random_generator)
            median_op = MedianOp(
                parent_ds,
                median_parameters.parameters['noise'],
            )
            median_dp_dict[column_name] = median_op.value(
                column_name, max_mul, bounds, random_generator
            )

        if signature["this"].python_type() == str(pd.DataFrame):
            median_dp = pd.Series(median_dp_dict)
        else:
            median_dp = list(median_dp_dict.values()).pop()

        return median_dp


class pd_std_dp(ExternalOpImplementation):
    _transform_id = "pandas.PD_STD_DP"
    _non_dp_equivalent_id = "pandas.PD_STD"

    def is_dp(self, signature: SarusBoundSignature) -> bool:
        """`axis = 0` and `numeric_only` is `True`"""
        if signature["this"].python_type() == str(pd.Series):
            return True

        axis = signature["axis"].static_value()
        numeric_only = signature["numeric_only"].static_value()
        return axis == 0 and numeric_only is True

    async def private_queries_and_task(
        self, signature: SarusBoundSignature
    ) -> t.Tuple[t.List[st.PrivateQuery], st.Task]:
        parent_ds = signature["this"].static_value()
        epsilon, delta = await get_budget(signature)

        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_max_mult = int(
            parent_schema.properties().get(MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT)
        )
        n_cols = len(parent_schema.data_type().children())

        max_mult_builder: OptimizableQueryBuilder = (
            simple_max_multiplicity_builder(
                parent_ds,
                Query(
                    max_multiplicity=Query.MaxMultiplicity(
                        max_max_multiplicity=max_max_mult
                    )
                ),
            )
        )
        column_bounds_std_builder: OptimizableQueryBuilder = (
            simple_composed_builder(
                parent_ds,
                [
                    simple_bounds_builder(
                        parent_ds, Query(bounds=Query.Bounds())
                    ),
                    std_builder(parent_ds, Query(std=Query.Std())),
                ],
            )
        )

        builder = simple_composed_builder(
            parent_ds,
            [max_mult_builder] + n_cols * [column_bounds_std_builder],
        )
        tasks = builder.build_query(
            builder.target([(epsilon, delta)], (0, epsilon))
        )
        query = builder.private_query(tasks)
        composed_query = t.cast(ComposedPrivateQuery, query)
        return list(composed_query.all_subqueries()), tasks

    async def call_dp(self, signature: SarusBoundSignature) -> t.Any:
        # Evaluate arguments
        parent_ds: st.Dataset = signature["this"].static_value()
        dataframe: pd.DataFrame = await parent_ds.async_to(pd.DataFrame)
        budget_value = await signature["budget"].collect()
        seed_value = await signature["seed"].collect()
        skipna = await signature["skipna"].collect()
        pe = (await signature.admin_data()).to_pandas()

        _, tasks = await self.private_queries_and_task(signature)
        tasks = [unwrap(subtask) for subtask in tasks.subtasks]
        max_mult_task, std_tasks = tasks[0], tasks[1:]

        epsilon = budget_value[0].epsilon
        random_generator = np.random.default_rng(abs(seed_value))

        # Compute DP value
        max_mul = MaxMultiplicityOp(
            parent_ds,
            epsilon,  # parameter for quantiles
            max_mult_task.noise_user_count,
            max_mult_task.noise_multiplicity,
            max_mult_task.max_max_multiplicity,
        ).value(random_generator)

        std_dp_dict = {}
        for index, column_name in enumerate(dataframe.columns):
            df = dataframe[[column_name]].join(pe)
            subtasks = [unwrap(task) for task in std_tasks[index].subtasks]
            bounds_parameters, std_parameters = t.cast(
                GenericTask, subtasks[0]
            ), t.cast(GenericTask, subtasks[1])
            column_type = (
                parent_ds.schema()
                .data_type()
                .children()[column_name]
                .protobuf()
            )
            if column_type.WhichOneof('type') == 'optional':
                if not skipna:
                    std_dp_dict[column_name] = np.nan
                    continue
                column_type = column_type.optional.type
                df = df.dropna()
            if column_type.WhichOneof('type') not in NUMERIC_TYPES:
                continue

            bounds = BoundOp(
                parent_ds,
                bounds_parameters.parameters['noise'],
            ).value(column_name, max_mul, random_generator)
            std_op = StdOp(
                parent_ds,
                std_parameters.parameters['noise_mean'],
                std_parameters.parameters['noise_square'],
                std_parameters.parameters['noise_count'],
            )
            std_dp_dict[column_name] = std_op.value(
                column_name, max_mul, bounds, random_generator
            )

        if signature["this"].python_type() == str(pd.DataFrame):
            std_dp = pd.Series(std_dp_dict)
        else:
            std_dp = list(std_dp_dict.values()).pop()

        return std_dp


class pd_count_dp(ExternalOpImplementation):
    _transform_id = "pandas.PD_COUNT_DP"
    _non_dp_equivalent_id = "pandas.PD_COUNT"

    def is_dp(self, signature: SarusBoundSignature) -> bool:
        """`axis = 0` and `numeric_only` is `True`"""
        axis = signature["axis"].static_value()
        return bool(axis == 0)

    async def private_queries_and_task(
        self, signature: SarusBoundSignature
    ) -> t.Tuple[t.List[st.PrivateQuery], st.Task]:
        parent_ds = signature["this"].static_value()
        epsilon, delta = await get_budget(signature)

        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_max_mult = int(
            parent_schema.properties().get(MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT)
        )
        n_cols = len(parent_schema.data_type().children())

        max_mult_builder: OptimizableQueryBuilder = (
            simple_max_multiplicity_builder(
                parent_ds,
                Query(
                    max_multiplicity=Query.MaxMultiplicity(
                        max_max_multiplicity=max_max_mult
                    )
                ),
            )
        )
        column_counts_builder = laplace_builder(
            parent_ds, Query(laplace_mechanism=Query.LaplaceMechanism())
        )
        builders_list: t.List[OptimizableQueryBuilder] = [max_mult_builder]
        builders_list.extend(n_cols * [column_counts_builder])
        builder = simple_composed_builder(parent_ds, builders_list)
        tasks = builder.build_query(
            builder.target([(epsilon, delta)], (0, epsilon))
        )
        query = builder.private_query(tasks)
        composed_query = t.cast(ComposedPrivateQuery, query)
        return list(composed_query.all_subqueries()), tasks

    async def call_dp(self, signature: SarusBoundSignature) -> t.Any:
        # Evaluate arguments
        parent_ds: st.Dataset = signature["this"].static_value()
        dataframe: pd.DataFrame = await parent_ds.async_to(pd.DataFrame)
        budget_value = await signature["budget"].collect()
        seed_value = await signature["seed"].collect()

        _, tasks = await self.private_queries_and_task(signature)
        tasks = [unwrap(subtask) for subtask in tasks.subtasks]
        max_mult_task, shape_task = tasks[0], tasks[1:]

        epsilon = budget_value[0].epsilon
        random_generator = np.random.default_rng(abs(seed_value))

        # Compute DP value
        max_mul = MaxMultiplicityOp(
            parent_ds,
            epsilon,  # parameter for quantiles
            max_mult_task.noise_user_count,
            max_mult_task.noise_multiplicity,
            max_mult_task.max_max_multiplicity,
        ).value(random_generator)

        count_dp_dict = {}
        for index, column_name in enumerate(dataframe.columns):
            count_parameters = shape_task[index]
            count_dp_dict[column_name] = CountOp(
                parent_ds,
                count_parameters.parameters['noise'],
            ).value(column_name, max_mul, random_generator)

        if signature["this"].python_type() == str(pd.DataFrame):
            count_dp = pd.Series(count_dp_dict)
        else:
            count_dp = list(count_dp_dict.values()).pop()
        return count_dp


class pd_value_counts_dp(ExternalOpImplementation):
    _transform_id: str = "pandas.PD_VALUE_COUNTS_DP"
    _non_dp_equivalent_id = "pandas.PD_VALUE_COUNTS"

    def is_dp(self, signature: SarusBoundSignature) -> bool:
        return signature["this"].python_type() == str(pd.Series)

    async def private_queries_and_task(
        self, signature: SarusBoundSignature
    ) -> t.Tuple[t.List[st.PrivateQuery], st.Task]:
        """Return the PrivateQueries summarizing DP characteristics."""
        parent_ds = signature["this"].static_value()
        epsilon, delta = await get_budget(signature)

        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_max_mult = int(
            parent_schema.properties().get(MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT)
        )
        n_cols = len(parent_schema.data_type().children())

        max_mult_builder: OptimizableQueryBuilder = (
            simple_max_multiplicity_builder(
                parent_ds,
                Query(
                    max_multiplicity=Query.MaxMultiplicity(
                        max_max_multiplicity=max_max_mult
                    )
                ),
            )
        )
        column_counts_builder = laplace_builder(
            parent_ds, Query(laplace_mechanism=Query.LaplaceMechanism())
        )
        builders_list: t.List[OptimizableQueryBuilder] = [max_mult_builder]
        builders_list.extend(n_cols * [column_counts_builder])
        builder = simple_composed_builder(parent_ds, builders_list)
        tasks = builder.build_query(
            builder.target([(epsilon, delta)], (0, epsilon))
        )
        query = builder.private_query(tasks)
        composed_query = t.cast(ComposedPrivateQuery, query)
        return list(composed_query.all_subqueries()), tasks

    async def call_dp(self, signature: SarusBoundSignature) -> t.Any:
        """Implementation of DP shape.

        A DP implementation receives additional arguments compared to a
        standard external implementation:
            - `budget`: a list of sp.Scalar.PrivacyParams.Point
                object containing each an epsilon and a delta values
            - `seed`: an integer used to parametrize random number generators
            - `pe`: the protected entity used by `sarus_statistics` primitives
        """
        parent_ds: st.Dataset = signature["this"].static_value()
        dataframe: pd.DataFrame = await parent_ds.async_to(pd.DataFrame)
        budget_value = await signature["budget"].collect()
        seed_value = await signature["seed"].collect()
        sort = await signature["sort"].collect()
        ascending = await signature["ascending"].collect()
        normalize = await signature["normalize"].collect()
        dropna = await signature["dropna"].collect()

        _, tasks = await self.private_queries_and_task(signature)
        tasks = [unwrap(subtask) for subtask in tasks.subtasks]
        max_mult_task, shape_task = tasks[0], tasks[1:]

        epsilon = budget_value[0].epsilon
        random_generator = np.random.default_rng(abs(seed_value))

        # Compute DP value
        max_mul = MaxMultiplicityOp(
            parent_ds,
            epsilon,  # parameter for quantiles
            max_mult_task.noise_user_count,
            max_mult_task.noise_multiplicity,
            max_mult_task.max_max_multiplicity,
        ).value(random_generator)

        count_dp_dict = {}
        for index, column_name in enumerate(dataframe.columns):
            count_parameters = shape_task[index]

            histogram = t.cast(
                t.Dict[str, float],
                HistogramOp(
                    parent_ds,
                    noise=count_parameters.parameters['noise'],
                    sort=sort,
                    ascending=ascending,
                    normalize=normalize,
                    dropna=dropna,
                ).value(column_name, max_mul, random_generator),
            )
            count_dp_dict[column_name] = {
                key: round(count) for key, count in histogram.items()
            }

        # for now only on series
        count_dp = pd.Series(list(count_dp_dict.values())[0])
        return count_dp


class pd_corr_dp(ExternalOpImplementation):
    _transform_id = "pandas.PD_CORR_DP"
    _non_dp_equivalent_id = "pandas.PD_CORR"

    def is_dp(self, signature: SarusBoundSignature) -> bool:
        """
        `numeric_only` is `True`
        DataFrame
        `method = Pearson`
        `min_periods = 1`
        """
        method = signature["method"].static_value()
        min_periods = signature["min_periods"].static_value()
        is_dataframe = bool(
            signature["this"].python_type() == str(pd.DataFrame)
        )
        return is_dataframe and (min_periods == 1) and (method == 'pearson')

    async def private_queries_and_task(
        self, signature: SarusBoundSignature
    ) -> t.Tuple[t.List[st.PrivateQuery], st.Task]:
        parent_ds = signature["this"].static_value()
        epsilon, delta = await get_budget(signature)

        parent_schema = await parent_ds.manager().async_schema(parent_ds)
        max_max_mult = int(
            parent_schema.properties().get(MAX_MAX_MULT, DEFAULT_MAX_MAX_MULT)
        )

        max_mult_builder: OptimizableQueryBuilder = (
            simple_max_multiplicity_builder(
                parent_ds,
                Query(
                    max_multiplicity=Query.MaxMultiplicity(
                        max_max_multiplicity=max_max_mult
                    )
                ),
            )
        )

        corr_builder: OptimizableQueryBuilder = simple_corr_builder(
            parent_ds, Query(covariance=Query.Covariance())
        )

        builder = simple_composed_builder(
            parent_ds,
            [max_mult_builder, corr_builder],
        )
        tasks = builder.build_query(
            builder.target([(epsilon, delta)], (0, epsilon))
        )
        query = t.cast(ComposedPrivateQuery, builder.private_query(tasks))
        return list(query.all_subqueries()), tasks

    async def call_dp(self, signature: SarusBoundSignature) -> t.Any:
        # Evaluate arguments
        parent_ds: st.Dataset = signature["this"].static_value()
        budget_value = await signature["budget"].collect()
        seed_value = await signature["seed"].collect()

        _, tasks = await self.private_queries_and_task(signature)

        epsilon = budget_value[0].epsilon
        # Compute DP value
        tasks = [unwrap(subtask) for subtask in tasks.subtasks]
        max_mult_task, corr_task = tasks[0], tasks[1]
        random_generator = np.random.default_rng(abs(seed_value))

        max_mul = MaxMultiplicityOp(
            parent_ds,
            epsilon,  # parameter for quantiles
            max_mult_task.noise_user_count,
            max_mult_task.noise_multiplicity,
            max_mult_task.max_max_multiplicity,
        ).value(random_generator)

        corr_dp = CorrOp(
            parent_ds,
            corr_task.parameters['epsilon'],
            corr_task.parameters['dims'],
        ).value(max_mul, random_generator=random_generator)

        return corr_dp


async def get_budget(signature: SarusBoundSignature) -> t.Tuple[float, float]:
    """Retrieve (epsilon, delta) from signature"""
    budget = await signature["budget"].collect()
    if len(budget) != 1:
        raise NotImplementedError(
            "The PrivacyParams contains more than 1 point in the privacy "
            "profile."
        )

    epsilon = budget[0].epsilon
    delta = budget[0].delta
    if epsilon == 0.0:
        raise ValueError("`epsilon` should be greater than 0.")

    return epsilon, delta
