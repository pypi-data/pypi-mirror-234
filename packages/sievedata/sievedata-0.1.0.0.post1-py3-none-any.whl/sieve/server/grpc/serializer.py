"""
This file defines utility functions for serialization
"""

from pydantic import BaseModel
from ..logging.logging import get_sieve_internal_logger

logger = get_sieve_internal_logger()


def add_type_converters(unpickled_input):
    """
    This will define parse_obj and __dict__ for types we decide to support
    Note: due to Pydantic limitations, we can't pickle classes with validators
    https://github.com/cloudpipe/cloudpickle/issues/408

    :param unpickled_input: The input to add type converters to
    :type unpickled_input: Any
    :return: The input with type converters added
    :rtype: Any
    """
    if issubclass(type(unpickled_input), BaseModel):
        for field in unpickled_input.__fields__.values():
            field.validators = []
    elif isinstance(unpickled_input, list):
        return [add_type_converters(item) for item in unpickled_input]
    elif isinstance(unpickled_input, dict):
        return {
            key: add_type_converters(value) for key, value in unpickled_input.items()
        }
    return unpickled_input


def input_to_type(unpickled_input, input_type):
    """
    This will convert the input to the correct type if it is not already the correct type

    :param unpickled_input: The input to convert
    :type unpickled_input: Any
    :param input_type: The type to convert to
    :type input_type: Any
    :return: The converted input
    :rtype: Any
    """

    if input_type and str(type(unpickled_input)) != str(input_type):
        if type(unpickled_input) == dict:
            try:
                return input_type.parse_obj(unpickled_input)
            except Exception as e:
                raise Exception("Invalid input type: " + str(e))
        else:
            raise Exception(
                f"Invalid input type: {str(type(unpickled_input))}. Expected {str(input_type)}"
            )
    return unpickled_input
