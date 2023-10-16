import requests
from peucr_core.validator import TestValidator
from peucr_core.exceptions import InvalidDefinitionException

class OneOfValidator(TestValidator):

    def __init__(self):
        self.labels = ["ONEOF"]


    def apply(self, expectation, response, suite):
        items = expectation.get("items")
        if items is None or not isinstance(items, list) or len(items) == 0:
            raise InvalidDefinitionException("ONEOF expectation requires no empty \"items\"")

        errors = []
        for item in items:
            result = suite.apply(item, response)

            if result["success"]:
                return result
            else:
                errors.append(result["msg"])

        return {"success": False, "msg": ". ".join(errors)}
