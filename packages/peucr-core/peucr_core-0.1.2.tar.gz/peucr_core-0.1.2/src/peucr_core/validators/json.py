import requests
from peucr_core.validator import TestValidator
from peucr_core.exceptions import InvalidDefinitionException

class JsonValidator(TestValidator):

    def __init__(self):
        self.labels = ["JSON"]


    def apply(self, expectation, response, suite):
        body = response.get("json")
        if body is None:
            raise InvalidDefinitionException("No JSON body in response")

        if expectation.get("value") is None:
            raise InvalidDefinitionException("JSON expectation requires \"value\"")
        value = expectation["value"]

        if expectation.get("field") is None:
            raise InvalidDefinitionException("JSON expectation requires \"field\"")
        field = expectation["field"]

        success = value == body.get(field)
        error = "Expected \"{}\" to be \"{}\" but got \"{}\"".format(field, value, body.get(field))

        return {"success": success, "msg": None if success else error}

