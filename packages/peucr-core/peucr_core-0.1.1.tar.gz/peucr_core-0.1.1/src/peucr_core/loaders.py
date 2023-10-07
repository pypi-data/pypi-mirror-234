import sys
import os
import inspect
import importlib
import json
from peucr_core.validatorsuite import ValidatorSuite
from peucr_core.pluginsuite import PluginSuite


class ConfigLoader:

    def __init__(self, args):
        self.prefix = "--"
        self.args = args


    def apply(self):
        config = {}

        if not self.get(self.args, "plugins"):
            config["plugins"] = "plugins"

        if not self.get(self.args, "specs"):
            config["specs"] = "specs"

        if not self.get(self.args, "validators"):
            config["validators"] = "validators"

        for index in range(len(self.args)):
            if self.is_flag(self.args, index):
                value = self.get(self.args, self.args[index])
                if value:
                    config[self.args[index][len(self.prefix):]] = value

        return config


    def get(self, args, name):
        flag = self.prefix + name if name[:2] != self.prefix else name

        if flag not in args:
            return None

        index = args.index(flag)

        if len(args) <= index+1 or self.is_flag(args, index+1):
            return None

        return args[index+1]


    def is_flag(self, args, index):
        return self.prefix == args[index][:2]



class PluginLoader:

    def __init__(self, config):
        self.plugin = "TestPlugin"
        self.config = config


    def apply(self):
        path = self.config["plugins"]

        if path[-1] == "/":
            path = path[0:-1]
        parentModule = path.split("/")[-1]

        plugins = []

        if os.path.exists(path):
            for file in os.listdir(path):
                try:
                    lib = importlib.import_module(parentModule+"."+file.split(".")[0])
                except Exception as e:
                    print(e)
                    sys.exit(1)
                    
                members = inspect.getmembers(lib, inspect.isclass)
                
                plugins.append(self.getTestPlugin(members, parentModule, lib))
            
        return PluginSuite([plugin(self.config) for plugin in plugins if plugin is not None], self.config)


    def getTestPlugin(self, member, parent, lib):
        pluginClass = None
        testPlugin = False

        for clazz in member:
            if clazz[0] == self.plugin:
                testPlugin = True

            if parent+"." in str(clazz[1]):
                pluginClass = clazz[0]

        if testPlugin and pluginClass:
            return getattr(lib, pluginClass)



class SpecLoader:

    def __init__(self, config):
        self.spec = "_spec.json"
        self.preconditions = "preconditions.json"
        self.config = config

    def apply(self):
        path = self.config["specs"]

        specs = {}
        if self.spec in path:
            directory = "/".join(path.split("/")[:-1])
            files = os.listdir(directory)
            spec_files = [path.split("/")[-1]]
        else:
            directory = path
            files = os.listdir(directory)
            spec_files = [file for file in files if "_spec.json" in file]
            spec_files.sort()
        
        preconditions = directory+"/"+self.preconditions if self.preconditions in files else None

        if preconditions:
            with open(preconditions, "r") as p:
                specs["preconditions"] = json.loads(p.read())

        execution = []
        for file in spec_files:
            with open(directory+"/"+file, "r") as f:
                execution.append(json.loads(f.read()))

        specs["execution"] = execution

        return specs



class ValidatorLoader:

    def __init__(self, config):
        self.validator = "TestValidator"
        self.config = config


    def apply(self):
        path = self.config["validators"]

        if path[-1] == "/":
            path = path[0:-1]
        parentModule = path.split("/")[-1]

        validators = []

        if os.path.exists(path):
            for file in os.listdir(path):
                try:
                    lib = importlib.import_module(parentModule+"."+file.split(".")[0])
                except Exception as e:
                    print(e)
                    sys.exit(1)
                    
                members = inspect.getmembers(lib, inspect.isclass)
                
                validators.append(self.getValidator(members, parentModule, lib))
            
        return ValidatorSuite([validator() for validator in validators if validator is not None])

    
    def getValidator(self, member, parent, lib):
        validatorClass = None
        testValidator = False

        for clazz in member:
            if clazz[0] == self.validator:
                testValidator = True

            if parent+"." in str(clazz[1]):
                validatorClass = clazz[0]

        if testValidator and validatorClass:
            return getattr(lib, validatorClass)
