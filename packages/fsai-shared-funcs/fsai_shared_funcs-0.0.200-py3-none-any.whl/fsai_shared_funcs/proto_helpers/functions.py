from datetime import datetime

from ..time_helper import get_pb_ts_from_datetime


# TODO: Move this to fsai_shared_funcs
def dict_to_proto(dictionary, protobuf_message):
    # Iterate over the key-value pairs in the dictionary
    for key, value in dictionary.items():
        if isinstance(value, datetime):
            # Instead of setattr we need to use CopyFrom for composite fields
            # Otherwise we will get AttributeError:
            #   Assignment not allowed to composite field “field name” in protocol message object
            getattr(protobuf_message, key).CopyFrom(get_pb_ts_from_datetime(value))
        else:
            # Set the field value in the Protobuf message
            setattr(protobuf_message, key, value)

    return protobuf_message
