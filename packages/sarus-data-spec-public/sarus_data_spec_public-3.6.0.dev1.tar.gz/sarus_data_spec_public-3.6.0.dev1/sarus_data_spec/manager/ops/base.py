from __future__ import annotations

import typing as t

import numpy as np
import pyarrow as pa

from sarus_data_spec.manager.async_utils import decoupled_async_iter
import sarus_data_spec.dataspec_validator.typing as sdvt
import sarus_data_spec.typing as st


class DataspecStaticChecker:
    def __init__(self, dataspec: st.DataSpec):
        self.dataspec = dataspec

    def is_dp_applicable(self, public_context: t.Collection[str]) -> bool:
        """Statically check if a DP transform is applicable in this position.

        This verification is common to all dataspecs and is true if:
            - the dataspec is transformed and its transform has an equivalent
            DP transform
            - the DP transform's required PEP arguments are PEP and aligned
            (i.e. same PEP token)
            - other dataspecs arguments are public
        """
        return False

    def is_dp(self) -> bool:
        """Checks if the transform is DP and compatible with the arguments."""
        return False

    def dp_transform(self) -> t.Optional[st.Transform]:
        """Return the dataspec's DP equivalent transform if existing."""
        return None

    def dp_equivalent(self) -> t.Optional[st.Transform]:
        """Return the dataspec's DP equivalent transform if existing."""
        raise NotImplementedError

    async def private_queries(self) -> t.List[st.PrivateQuery]:
        """Return the PrivateQueries summarizing DP characteristics."""
        if self.is_dp():
            raise NotImplementedError
        else:
            return []


class DatasetStaticChecker(DataspecStaticChecker):
    def __init__(self, dataset: st.Dataset):
        super().__init__(dataset)
        self.dataset = dataset

    async def schema(self) -> st.Schema:
        """Computes the schema of the dataspec"""
        raise NotImplementedError

    def pep_token(self, public_context: t.Collection[str]) -> t.Optional[str]:
        """Return a token if the output is PEP."""
        raise NotImplementedError

    def pep_kind(self) -> sdvt.PEPKind:
        raise NotImplementedError


class DatasetImplementation:
    def __init__(self, dataset: st.Dataset):
        self.dataset = dataset

    async def to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        raise NotImplementedError

    async def size(self) -> st.Size:
        raise NotImplementedError

    async def multiplicity(self) -> st.Multiplicity:
        raise NotImplementedError

    async def bounds(self) -> st.Bounds:
        raise NotImplementedError

    async def marginals(self) -> st.Marginals:
        raise NotImplementedError

    async def sql(
        self,
        query: t.Union[str, t.Dict[str, t.Any]],
        dialect: t.Optional[st.SQLDialect] = None,
        batch_size: int = 10000,
        result_type: t.Optional[st.Type] = None,
    ) -> t.AsyncIterator[pa.RecordBatch]:
        """It composes the query and it sends it to the parent."""
        raise NotImplementedError

    @staticmethod
    async def decoupled_async_iter(
        source: t.AsyncIterator[pa.RecordBatch], buffer_size: int = 100
    ) -> t.AsyncIterator[pa.RecordBatch]:
        return decoupled_async_iter(source=source, buffer_size=buffer_size)


class ScalarImplementation:
    def __init__(self, scalar: st.Scalar):
        self.scalar = scalar

    async def value(self) -> t.Any:
        raise NotImplementedError

    @staticmethod
    async def decoupled_async_iter(
        source: t.AsyncIterator[pa.RecordBatch], buffer_size: int = 100
    ) -> t.AsyncIterator[pa.RecordBatch]:
        return decoupled_async_iter(source=source, buffer_size=buffer_size)


async def _ensure_batch_correct(
    async_iterator: t.Union[
        t.AsyncIterator[pa.RecordBatch], t.AsyncIterator[pa.Array]
    ],
    func_to_apply: t.Callable,
    batch_size: int,
) -> t.AsyncIterator[pa.RecordBatch]:
    """Method that executes func_to_apply on each batch
    of the async_iterator but rather than directly returning
    the result, it accumulates them and returns them progressively
    so that each new batch has batch_size."""

    global_array = None
    async for batch in async_iterator:
        new_array = await func_to_apply(batch)
        if len(new_array) == batch_size and global_array is None:
            yield pa.RecordBatch.from_struct_array(
                new_array.take(
                    np.linspace(0, batch_size - 1, batch_size, dtype=int)
                )
            )
        elif global_array is not None:
            global_array = pa.concat_arrays([global_array, new_array])
            if len(global_array) < batch_size:
                continue
            else:
                # here cannot use array.slice because there
                # is a bug in the columns being copied
                # when we switch to record batch
                yield pa.RecordBatch.from_struct_array(
                    global_array.take(
                        np.linspace(0, batch_size - 1, batch_size, dtype=int)
                    )
                )
                global_array = global_array.take(
                    np.linspace(
                        batch_size,
                        len(global_array) - 1,
                        len(global_array) - batch_size,
                        dtype=int,
                    )
                )

        else:
            # initialize global_array
            global_array = new_array
            continue
    # handle remaining array: split it in

    if global_array is not None and len(global_array) > 0:
        while len(global_array) > 0:
            min_val = min(batch_size, len(global_array))
            indices = np.linspace(
                0, len(global_array) - 1, len(global_array), dtype=int
            )
            yield pa.RecordBatch.from_struct_array(
                global_array.take(indices[:min_val])
            )
            global_array = global_array.take(indices[min_val:])
