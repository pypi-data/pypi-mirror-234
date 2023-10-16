import requests
from peucr_core.validator import TestValidator

class StatusValidator(TestValidator):

    def __init__(self):
        self.labels = ["STATUS", "STATUS-CODE"]


    def apply(self, expectation, response, suite):
        if expectation.get("value") is not None:
            success = expectation["value"] == response["status-code"]
            error = "Status code expected to be {} but was {}".format(expectation["value"], response["status-code"])
        else:
            success = response["status-code"] >= 200 and response["status-code"] < 300
            error = "Status code expected to be successful but was {}".format(response["status-code"])

        return {"success": success, "msg": error}
