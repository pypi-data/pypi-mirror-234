import cloudpickle
import sys
from ...proto import worker_pb2
from ..constants import MAX_OUTPUT_SIZE
from ..serializer import add_type_converters


def get_single_output(output, handler):
    """
    This function gets the output from a user function, and returns it in a GRPC response.

    The output is checked for size, and is serialized and postprocessed. We then return it,
    upon which it will be sent over GRPC to the client.

    :param output: The output from the user's code
    :type output: Any
    :param handler: The handler to run postprocessing on the output
    :type handler: Handler
    """

    handler.postprocess(output)
    output = add_type_converters(output)
    o = cloudpickle.dumps(output)
    if sys.getsizeof(o) > MAX_OUTPUT_SIZE:
        raise Exception(
            f"Output size too large, must be less than f{MAX_OUTPUT_SIZE} bytes. Current size: {sys.getsizeof(o)} bytes"
        )
    return worker_pb2.PredictionResponse(
        data=o, status=worker_pb2.Status.STATUS_SUCCEEDED, stop=True
    )
