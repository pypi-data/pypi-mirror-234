import pyarrow as pa

import sarus_data_spec.typing as st


def convert_record_batch(
    record_batch: pa.RecordBatch, _type: st.Type
) -> pa.Array:
    if str(_type.protobuf().WhichOneof('type')) not in ['struct', 'union']:
        return record_batch.column(0)
    record_schema = record_batch.schema
    fields = [record_schema.field(i) for i in range(len(record_schema.types))]
    return pa.StructArray.from_arrays(record_batch.columns, fields=fields)
