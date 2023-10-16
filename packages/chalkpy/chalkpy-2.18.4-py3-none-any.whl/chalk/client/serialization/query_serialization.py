from io import BytesIO
from typing import Any, List, Optional

from chalk.client.models import OnlineQueryManyRequest
from chalk.features import ensure_feature

MAGIC_STR: bytes = "chalk".encode("utf-8")
MULTI_QUERY_MAGIC_STR: bytes = "chal1".encode("utf-8")


def _write_query_to_buffer(dest: BytesIO, request: OnlineQueryManyRequest, compression: Optional[str] = None) -> None:
    """
    Advances pointer for `dest`
    """
    # called from guarded locations

    import pyarrow
    import pyarrow.feather as feather

    encoded_inputs = request.inputs

    schema = pyarrow.schema(
        [pyarrow.field(k, type=ensure_feature(k).converter.pyarrow_dtype) for k in encoded_inputs.keys()]
    )

    data = pyarrow.Table.from_pydict(encoded_inputs, schema=schema)

    header = request.copy(exclude={"inputs"}).json()
    header_bytes = header.encode("utf-8")
    # Header
    dest.write(len(header_bytes).to_bytes(8, byteorder="big"))
    dest.write(header_bytes)

    # Fill in a placeholder for the body length
    body_length_position = dest.tell()
    dest.write((0).to_bytes(8, byteorder="big"))
    body_start_position = dest.tell()

    # Write the body
    pyarrow.feather.write_feather(data, dest=dest, compression=compression)
    end_of_body = dest.tell()

    # Backfill the body length
    dest.seek(body_length_position)
    dest.write((end_of_body - body_start_position).to_bytes(8, byteorder="big"))

    # Leave the cursor ready to write
    dest.seek(end_of_body)


def _decode_multi_query_responses(body: bytes) -> List[Any]:
    import pyarrow
    import pyarrow.feather as feather

    response: List[pyarrow.Table] = []

    INT64_BYTE_COUNT = 8

    buffer = BytesIO(body)

    while buffer.tell() < len(body) - 1:
        body_length = int.from_bytes(buffer.read(INT64_BYTE_COUNT), byteorder="big")
        body_buffer = BytesIO(buffer.read(body_length))
        parsed_body = pyarrow.feather.read_table(body_buffer)
        response.append(parsed_body)

    return response
