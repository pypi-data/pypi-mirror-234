import typing as t

from sarus_data_spec.manager.ops.processor.standard.standard_op import (  # noqa: E501
    StandardScalarImplementation,
    StandardScalarStaticChecker,
)
from sarus_data_spec.typing import Scalar


class ErrorEstimationStaticChecker(StandardScalarStaticChecker):
    ...


class ErrorEstimation(StandardScalarImplementation):
    """Computes the budget via standard rule
    depending on the number of columns of the
    parent dataspec"""

    async def value(self) -> t.Any:
        dataspecs = self.parents()

        true_value = await t.cast(Scalar, dataspecs[0]).async_value()
        dp_values = []
        for dataspec in dataspecs[1:]:
            dp_value = await t.cast(Scalar, dataspec).async_value()
            dp_values.append(abs(dp_value - true_value))

        return max(dp_values)
