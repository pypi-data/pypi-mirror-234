import time
import sys
from peucr_core.loaders import ConfigLoader, SpecLoader, PluginLoader, ValidatorLoader
from peucr_core.exceptions import InvalidDefinitionException


class TestFramework:
    def __init__(self, args):
        self.separator = "**************************************************"
        self.retryInterval = 0.2
        self.config = ConfigLoader(args).apply()
        self.specs = SpecLoader(self.config).apply()
        self.plugins = PluginLoader(self.config).apply()
        self.validators = ValidatorLoader(self.config).apply()



    def exec_actions(self, actions):
        if actions is None or len(actions) == 0:
            return True

        for action in actions:
            executed = False
            startTime = time.time()

            while not executed and time.time() - startTime < 2:
                r = self.plugins.apply(action)
                executed = r["success"]

                if executed:
                    break

                time.sleep(self.retryInterval)

        if not executed:
            print("Action failed. Validation will not be executed")
            return False

        return True



    def exec_validation(self, validation):
        time.sleep(validation.get("wait", 0))

        attempts = min(5, validation.get("duration", self.retryInterval)) / self.retryInterval
        counter = 0
        result = {"success": False}

        while not result["success"] and counter < attempts:
            try:
                response = self.plugins.apply(validation)
                result = self.validators.apply(validation.get("expectation"), response)

            except InvalidDefinitionException as e:
                result["msg"] = e
                break

            except Exception as e:
                result["msg"] = "Error:", e

            if result["success"]:
                break

            time.sleep(self.retryInterval)
            counter += 1

        if not result["success"]:
            print("Failure.", result["msg"])

        return result["success"]



    def exec_validations(self, validations):
        if not validations or not isinstance(validations, list) or len(validations) == 0:
            print("No validation specified in test. Aborting.")
            return False

        for validation in validations:
            if not self.exec_validation(validation):
                return False

        return True



    def exec_test(self, spec):
        print("Executing test \"{}\"".format(spec.get("name", "UNNAMED")))

        if not self.exec_actions(spec.get("context")):
            return False

        if not self.exec_actions(spec.get("actions")):
            return False

        return self.exec_validations(spec.get("validation"))



    def exec_test_suite(self, specs):
        successes = 0

        for spec in specs:
            if self.exec_test(spec):
                successes += 1

        print(self.separator)

        if successes != len(specs):
            print(len(specs), "tests run", len(specs) - successes, "failures")
            sys.exit(1)        

        print(len(specs), "tests run. No failures.")



    def exec_preconditions(self, validations):
        if validations is None or validations.get("validation") is None:
            return

        for validation in validations["validation"]:
            print("Verifying", validation.get("name", "UNNAMED"))
            if not self.exec_validation(validation):
                print("Precondition validation failed. Test will be aborted")
                sys.exit(1)

        print(self.separator)



    def exec(self):
        self.exec_preconditions(self.specs.get("preconditions"))
        self.exec_test_suite(self.specs.get("execution"))
