from peucr_core.validators.default import DefaultValidator
from peucr_core.validators.status import StatusValidator
from peucr_core.validators.json import JsonValidator
from peucr_core.validators.oneof import OneOfValidator
from peucr_core.exceptions import InvalidDefinitionException


class ValidatorSuite:
    def __init__(self, custom):
        self.default = [StatusValidator(), JsonValidator(), OneOfValidator()]
        self.custom = custom

    def apply(self, expectation, result):
        if expectation is not None and "type" not in expectation:
            raise InvalidDefinitionException("expectation should have \"type\" defined")

        validator = self.getValidator(expectation.get("type") if expectation is not None else None)

        return validator.apply(expectation, result, self)
        

    def getValidator(self, type):
        if type is None:
            return DefaultValidator()

        validators = [v for v in self.custom if v.executes(type)]
        if validators:
            return validators[0]

        validators = [v for v in self.default if v.executes(type)]
        if validators:
            return validators[0]

        return DefaultValidator()
