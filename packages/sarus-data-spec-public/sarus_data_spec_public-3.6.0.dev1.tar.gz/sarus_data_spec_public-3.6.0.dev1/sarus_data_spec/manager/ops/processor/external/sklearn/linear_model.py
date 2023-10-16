from typing import Any, Optional

from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusSignature,
    SarusSignatureValue,
)

from ..external_op import ExternalOpImplementation

try:
    from sklearn import linear_model
except ModuleNotFoundError:
    pass  # error message in typing.py


class sk_linear_regression(ExternalOpImplementation):
    _transform_id = "sklearn.SK_LINEAR_REGRESSION"
    _signature = SarusSignature(
        SarusParameter(
            name="fit_intercept",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="copy_X",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="n_jobs",
            annotation=Optional[int],
            default=None,
            predicate=lambda x: x is None,
        ),
        SarusParameter(
            name="positive",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return linear_model.LinearRegression(**kwargs)
