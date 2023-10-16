class TestValidator:

    def __init__(self):
        pass

    def executes(self, name):
        return name.upper() in [l.upper() for l in self.labels]
