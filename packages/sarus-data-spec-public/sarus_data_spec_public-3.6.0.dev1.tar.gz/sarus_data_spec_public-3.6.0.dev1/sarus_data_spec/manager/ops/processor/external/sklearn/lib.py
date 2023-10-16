from typing import Any, Optional, Union

import numpy.typing as npt

from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusSignature,
    SarusSignatureValue,
)

from ..external_op import ExternalOpImplementation

try:
    from scipy.sparse import spmatrix
    from sklearn.base import BaseEstimator
except ModuleNotFoundError:
    BaseEstimator = Any
    spmatrix = Any


class sk_fit(ExternalOpImplementation):
    _transform_id = "sklearn.SK_FIT"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=BaseEstimator,
        ),
        SarusParameter(
            name="X",
            annotation=Union[npt.ArrayLike, spmatrix],
        ),
        SarusParameter(
            name="y",
            annotation=Optional[Union[npt.ArrayLike, spmatrix]],
            default=None,
        ),
        SarusParameter(
            name="sample_weight",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        if kwargs["sample_weight"] is None:
            del kwargs["sample_weight"]
        fitted_model = this.fit(**kwargs)
        return fitted_model


class sk_fit_y(ExternalOpImplementation):
    _transform_id = "sklearn.SK_FIT_Y"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=BaseEstimator,
        ),
        SarusParameter(
            name="y",
            annotation=Union[npt.ArrayLike, spmatrix],
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        fitted_model = this.fit(**kwargs)
        return fitted_model


class sk_predict(ExternalOpImplementation):
    _transform_id = "sklearn.SK_PREDICT"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=BaseEstimator,
        ),
        SarusParameter(
            name="X",
            annotation=Union[npt.ArrayLike, spmatrix],
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.predict(**kwargs)


class sk_predict_callable(ExternalOpImplementation):
    _transform_id = "sklearn.SK_PREDICT_CALLABLE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=BaseEstimator,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.predict


class sk_predict_log_proba(ExternalOpImplementation):
    _transform_id = "sklearn.SK_PREDICT_LOG_PROBA"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=BaseEstimator,
        ),
        SarusParameter(
            name="X",
            annotation=Union[npt.ArrayLike, spmatrix],
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.predict_log_proba(**kwargs)


class sk_predict_log_proba_callable(ExternalOpImplementation):
    _transform_id = "sklearn.SK_PREDICT_LOG_PROBA_CALLABLE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=BaseEstimator,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.predict_log_proba


class sk_predict_proba(ExternalOpImplementation):
    _transform_id = "sklearn.SK_PREDICT_PROBA"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=BaseEstimator,
        ),
        SarusParameter(
            name="X",
            annotation=Union[npt.ArrayLike, spmatrix],
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.predict_proba(**kwargs)


class sk_predict_proba_callable(ExternalOpImplementation):
    _transform_id = "sklearn.SK_PREDICT_PROBA_CALLABLE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=BaseEstimator,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this,) = signature.collect_args()
        return this.predict_proba


class sk_transform(ExternalOpImplementation):
    _transform_id = "sklearn.SK_TRANSFORM"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=BaseEstimator,
        ),
        SarusParameter(
            name="X",
            annotation=Union[npt.ArrayLike, spmatrix],
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        (this, X) = signature.collect_args()
        return this.transform(X)


class sk_inverse_transform(ExternalOpImplementation):
    _transform_id = "sklearn.SK_INVERSE_TRANSFORM"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=BaseEstimator,
        ),
        SarusParameter(
            name="X",
            annotation=Union[npt.ArrayLike, spmatrix],
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, X = signature.collect_args()
        return this.inverse_transform(X)


class sk_score(ExternalOpImplementation):
    _transform_id = "sklearn.SK_SCORE"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=BaseEstimator,
        ),
        SarusParameter(
            name="X",
            annotation=Union[npt.ArrayLike, spmatrix],
        ),
        SarusParameter(
            name="y",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
        SarusParameter(
            name="sample_weight",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.score(**kwargs)


class sk_fit_transform(ExternalOpImplementation):
    _transform_id = "sklearn.SK_LABEL_ENCODER_FIT_TRANSFORM"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=BaseEstimator,
        ),
        SarusParameter(
            name="X",
            annotation=Union[npt.ArrayLike, spmatrix],
        ),
        SarusParameter(
            name="y",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.fit_transform(**kwargs)


class sk_split(ExternalOpImplementation):
    _transform_id = "sklearn.SK_SPLIT"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=BaseEstimator,
        ),
        SarusParameter(
            name="X",
            annotation=Union[npt.ArrayLike, spmatrix],
        ),
        SarusParameter(
            name="y",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
        SarusParameter(
            name="groups",
            annotation=Optional[npt.ArrayLike],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.split(**kwargs)


class sk_get_n_splits(ExternalOpImplementation):
    _transform_id = "sklearn.SK_GET_N_SPLITS"
    _signature = SarusSignature(
        SarusParameter(
            name="this",
            annotation=BaseEstimator,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        this, kwargs = signature.collect_kwargs_method()
        return this.get_n_splits(**kwargs)
