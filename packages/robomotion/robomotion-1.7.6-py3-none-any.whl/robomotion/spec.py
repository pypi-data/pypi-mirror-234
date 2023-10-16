import inspect
import json
import sys
from robomotion.node import Node
from robomotion.variable import (
    Variable,
    InVariable,
    OptVariable,
    OutVariable,
    Credentials,
    ECategory,
)
from re import sub


class NodeSpec:
    def __init__(
        self,
        id: str,
        icon: str = "",
        name: str = "",
        color: str = "",
        editor: str = None,
        inputs: int = 0,
        outputs: int = 0,
    ):
        self.id = id
        self.icon = icon
        self.name = name
        self.color = color
        self.editor = editor
        self.inputs = inputs
        self.inputs = self.inputs[0]
        self.outputs = outputs
        self.outputs = self.outputs[0]
        self.properties = []


class Property:
    def __init__(self, schema):
        self.schema = schema
        self.formData = {}
        self.uiSchema = {}


class Schema:
    def __init__(self, type: str, title: str):
        self.type = type
        self.title = title
        self.properties = {}


class SProperty:
    type = ""
    title = ""
    description = None
    subtitle = None
    category = None
    properties = None
    csScope = None
    jsScope = None
    customScope = None
    messageScope = None
    messageOnly = None
    multiple = None
    variableType = None
    enum = []
    enumNames = []


class VarDataProperty:
    def __init__(self, name: str, scope: str):
        self.scope = scope
        self.name = name


class Spec:
    @staticmethod
    def generate(plugin_name, version):
        frm = inspect.stack()[2]
        mod = inspect.getmodule(frm[0])
        clsmembers = inspect.getmembers(sys.modules[mod.__name__], inspect.isclass)

        pspec = {"name": plugin_name, "version": version}

        nodes = []

        for c in clsmembers:
            cls = c[1]
            if issubclass(cls, Node) and cls is not Node:
                node = {}
                inst = cls()
                node["id"] = inst.name
                node["name"] = inst.title
                node["icon"] = inst.icon
                node["color"] = inst.color
                node["editor"] = inst.editor
                node["inputs"] = inst.inputs
                node["outputs"] = inst.outputs

                properties = []
                inputVars = Spec.get_inputs_vars(cls)
                inputs = Spec.get_inputs(cls)

                if len(inputs) + len(inputVars) > 0:
                    prop = {}

                    pSchema, pUISchema = {}, {}
                    pSchema["title"] = "Input"
                    pSchema["type"] = "object"

                    inProperties, formData = {}, {}
                    uiOrder = []

                    for _input in inputVars:
                        input = _input["val"]
                        inObject = {
                            "title": input.title,
                            "variableType": input.type,
                        }

                        if input.arrayFields is not None:
                            arrProps = {}
                            for arrField in input.arrayFields:
                                arrProps[Spec.to_snake_case(arrField)] = {
                                    "type": "string",
                                    "title": arrField,
                                }

                            inObject["items"] = {
                                "type": "object",
                                "properties": {
                                    "scope": {"type": "string"},
                                    "name": {"properties": arrProps},
                                },
                            }

                        else:
                            inObject["type"] = "object"
                            inObject["properties"] = {
                                "scope": {"type": "string"},
                                "name": {"type": "string"},
                            }

                        if input.customScope:
                            inObject["customScope"] = True
                        if input.messageScope:
                            inObject["messageScope"] = True
                        if input.messageOnly:
                            inObject["messageOnly"] = True
                        if input.jsScope:
                            inObject["jsScope"] = True
                        if input.pyScope:
                            inObject["pyScope"] = True
                        if input.description != "":
                            inObject["description"] = input.description

                        name = Spec.lower_first_letter(_input["key"])
                        if input.format != "":
                            inObject["format"] = input.format
                            pUISchema[name] = {"ui:field": input.format}
                        else:
                            pUISchema[name] = {"ui:field": "variable"}

                        inProperties[name] = inObject
                        formData[name] = {"scope": input.scope, "name": input.name}
                        uiOrder.append(name)

                    for _input in inputs:
                        input = _input["val"]
                        inObject = {"type": input.type, "title": input.title}

                        name = Spec.lower_first_letter(_input["key"])
                        if input.hidden:
                            pUISchema[name] = {"ui:widget": "hidden"}
                        if input.description != "":
                            inObject["description"] = input.description
                            pUISchema[name] = {"ui:field": "input"}
                        if input.format != "":
                            inObject["format"] = input.format
                            pUISchema[name] = {"ui:field": input.format}

                        inProperties[name] = inObject
                        formData[name] = input.default
                        uiOrder.append(name)

                    pSchema["properties"] = inProperties
                    pUISchema["ui:order"] = uiOrder

                    prop["schema"] = pSchema
                    prop["uiSchema"] = pUISchema
                    prop["formData"] = formData

                    properties.append(prop)

                outputVars = Spec.get_output_vars(cls)
                outputs = Spec.get_outputs(cls)

                if len(outputs) + len(outputVars) > 0:
                    prop = {}

                    pSchema, pUISchema = {}, {}
                    pSchema["title"] = "Output"
                    pSchema["type"] = "object"

                    outProperties, formData = {}, {}
                    uiOrder = []

                    for _output in outputVars:
                        output = _output["val"]
                        outObject = {
                            "type": "object",
                            "title": output.title,
                            "variableType": output.type,
                            "properties": {
                                "scope": {"type": "string"},
                                "name": {"type": "string"},
                            },
                        }

                        if output.messageScope:
                            outObject["messageScope"] = True
                        if output.messageOnly:
                            outObject["messageOnly"] = True
                        if output.description != "":
                            outObject["description"] = output.description

                        name = Spec.lower_first_letter(_output["key"])
                        outProperties[name] = outObject
                        pUISchema[name] = {"ui:field": "variable"}
                        formData[name] = {"scope": output.scope, "name": output.name}
                        uiOrder.append(name)

                    for _output in outputs:
                        output = _output["val"]
                        outObject = {"type": output.type, "title": output.title}

                        name = Spec.lower_first_letter(_output["key"])
                        if output.hidden:
                            pUISchema[name] = {"ui:widget": "hidden"}
                        if output.description != "":
                            outObject["description"] = output.description
                            pUISchema[name] = {"ui:field": "input"}

                        outProperties[name] = outObject
                        formData[name] = output.default
                        uiOrder.append(name)

                    pSchema["properties"] = outProperties
                    pUISchema["ui:order"] = uiOrder

                    prop["schema"] = pSchema
                    prop["uiSchema"] = pUISchema
                    prop["formData"] = formData

                    properties.append(prop)

                optionVars = Spec.get_option_vars(cls)
                options = Spec.get_options(cls)
                credentials = Spec.get_credentials(cls)

                if len(options) + len(optionVars) + len(credentials) > 0:
                    prop = {}

                    pSchema, pUISchema = {}, {}
                    pSchema["title"] = "Options"
                    pSchema["type"] = "object"

                    optProperties, formData = {}, {}
                    uiOrder = []

                    for _option in optionVars:
                        option = _option["val"]
                        optObject = {
                            "title": option.title,
                            "variableType": option.type,
                        }

                        if option.arrayFields is not None:
                            arrProps = {}
                            for arrField in option.arrayFields:
                                arrProps[Spec.to_snake_case(arrField)] = {
                                    "type": "string",
                                    "title": arrField,
                                }

                            optObject["items"] = {
                                "type": "object",
                                "properties": {
                                    "scope": {"type": "string"},
                                    "name": {"properties": arrProps},
                                },
                            }

                        else:
                            optObject["type"] = "object"
                            optObject["properties"] = {
                                "scope": {"type": "string"},
                                "name": {"type": "string"},
                            }

                        if option.customScope:
                            optObject["customScope"] = True
                        if option.messageScope:
                            optObject["messageScope"] = True
                        if option.messageOnly:
                            optObject["messageOnly"] = True
                        if option.jsScope:
                            optObject["jsScope"] = True
                        if option.pyScope:
                            optObject["pyScope"] = True
                        if option.description != "":
                            optObject["description"] = option.description

                        name = Spec.lower_first_letter(_option["key"])
                        if option.format != "":
                            optObject["format"] = option.format
                            pUISchema[name] = {"ui:field": option.format}
                        else:
                            pUISchema[name] = {"ui:field": "variable"}

                        optProperties[name] = optObject
                        formData[name] = {"scope": option.scope, "name": option.name}
                        uiOrder.append(name)

                    for _option in options:
                        option = _option["val"]
                        optObject = {"type": option.type, "title": option.title}

                        name = Spec.lower_first_letter(_option["key"])

                        category = option.category
                        if category != ECategory.Null:
                            optObject["category"] = int(category)
                        if option.description != "":
                            optObject["description"] = option.description
                            pUISchema[name] = {"ui:field": "input"}
                        if option.format != "":
                            optObject["format"] = option.format
                            pUISchema[name] = {"ui:field": option.format}

                        if option.enum is not None:
                            enums = option.enum.enums
                            if enums is not None and len(enums) > 0:
                                enumNames = option.enum.enumNames
                                optObject["enum"] = enums
                                optObject["enumNames"] = enumNames

                        if option.hidden:
                            pUISchema[name] = {"ui:widget": "hidden"}

                        if option.default is not None:
                            formData[name] = option.default

                        optProperties[name] = optObject
                        uiOrder.append(name)

                    for _credential in credentials:
                        credential = _credential["val"]
                        optObject = {
                            "type": "object",
                            "title": credential.title,
                            "subtitle": credential.title,
                            "category": int(credential.category),
                            "customScope": True,
                            "messageScope": True,
                            "properties": {
                                "scope": {
                                    "type": "string",
                                },
                                "name": {
                                    "type": "object",
                                    "properties": {
                                        "vaultId": {"type": "string"},
                                        "itemId": {"type": "string"},
                                    },
                                },
                            },
                        }

                        if credential.description != "":
                            optObject["description"] = credential.description

                        name = Spec.lower_first_letter(_credential["key"])
                        pUISchema[name] = {"ui:field": "vault"}
                        formData[name] = {
                            "scope": "Custom",
                            "name": {"vaultId": "_", "itemId": "_"},
                        }
                        optProperties[name] = optObject
                        uiOrder.append(name)

                    pSchema["properties"] = optProperties
                    pUISchema["ui:order"] = uiOrder

                    prop["schema"] = pSchema
                    prop["uiSchema"] = pUISchema
                    prop["formData"] = formData

                    properties.append(prop)

                node["properties"] = properties
                nodes.append(node)

        pspec["nodes"] = nodes
        js = json.dumps(pspec, default=lambda o: o.__dict__)
        print(js)

    @staticmethod
    def cleandict(d):
        if not isinstance(d, dict):
            return d
        return dict((k, Spec.cleandict(v)) for k, v in d.iteritems() if v is not None)

    @staticmethod
    def jsonKeys2int(x):
        if isinstance(x, dict):
            return {int(k): v for k, v in x.items()}
        return x

    @staticmethod
    def get_variable_type(val) -> str:
        if isinstance(val, Variable):
            return Spec.upper_first_letter(val.type)

        return "String"

    @staticmethod
    def lower_first_letter(text: str) -> str:
        if len(text) < 2:
            return text.lower()
        return text[:1].lower() + text[1:]

    @staticmethod
    def upper_first_letter(text: str) -> str:
        if len(text) < 2:
            return text.upper()
        return text[:1].upper() + text[1:]

    @staticmethod
    def get_inputs(cls) -> list[any]:
        inputs = []
        fields = cls().cls().__dict__
        for key in fields.keys():
            val = fields[key]
            if (
                isinstance(val, Variable)
                and not isinstance(val, InVariable)
                and not isinstance(val, OutVariable)
                and not isinstance(val, OptVariable)
                and val.input
            ):
                inputs.append({"key": key, "val": val})
            elif (
                not isinstance(val, InVariable)
                and not isinstance(val, OutVariable)
                and not isinstance(val, OptVariable)
                and key.lower().startswith("in")
            ):
                inputs.append(
                    {
                        "key": key,
                        "val": Variable(
                            title=Spec.camel_case_to_text(key.lstrip("in")),
                            type=Spec.get_type(val),
                            default=val,
                        ),
                    }
                )

        return inputs

    @staticmethod
    def get_inputs_vars(cls) -> list[any]:
        inputs = []
        fields = cls().cls().__dict__
        for key in fields.keys():
            val = fields[key]
            if isinstance(val, InVariable):
                inputs.append({"key": key, "val": val})

        return inputs

    @staticmethod
    def get_outputs(cls) -> list[any]:
        outputs = []
        fields = cls().cls().__dict__
        for key in fields.keys():
            val = fields[key]
            if (
                isinstance(val, Variable)
                and not isinstance(val, InVariable)
                and not isinstance(val, OutVariable)
                and not isinstance(val, OptVariable)
                and val.output
            ):
                outputs.append({"key": key, "val": val})
            elif (
                not isinstance(val, InVariable)
                and not isinstance(val, OutVariable)
                and not isinstance(val, OptVariable)
                and key.lower().startswith("out")
            ):
                outputs.append(
                    {
                        "key": key,
                        "val": Variable(
                            title=Spec.camel_case_to_text(key.lstrip("out")),
                            type=Spec.get_type(val),
                            default=val,
                        ),
                    }
                )

        return outputs

    @staticmethod
    def get_output_vars(cls) -> list[any]:
        outputs = []
        fields = cls().cls().__dict__
        for key in fields.keys():
            val = fields[key]
            if isinstance(val, OutVariable):
                outputs.append({"key": key, "val": val})

        return outputs

    @staticmethod
    def get_options(cls) -> list[any]:
        options = []
        fields = cls().cls().__dict__
        for key in fields.keys():
            val = fields[key]
            if (
                isinstance(val, Variable)
                and not isinstance(val, InVariable)
                and not isinstance(val, OutVariable)
                and not isinstance(val, OptVariable)
                and val.option
            ):
                options.append({"key": key, "val": val})
            elif (
                not isinstance(val, InVariable)
                and not isinstance(val, OutVariable)
                and not isinstance(val, OptVariable)
                and not isinstance(val, Credentials)
                and key.lower().startswith("opt")
            ):
                options.append(
                    {
                        "key": key,
                        "val": Variable(
                            title=Spec.camel_case_to_text(key.lstrip("opt")),
                            type=Spec.get_type(val),
                            default=val,
                        ),
                    }
                )

        return options

    @staticmethod
    def get_credentials(cls) -> list[any]:
        credentials = []
        fields = cls().cls().__dict__
        for key in fields.keys():
            val = fields[key]
            if isinstance(val, Credentials):
                credentials.append({"key": key, "val": val})

        return credentials

    @staticmethod
    def get_option_vars(cls) -> list[any]:
        options = []
        fields = cls().cls().__dict__
        for key in fields.keys():
            val = fields[key]
            if isinstance(val, OptVariable):
                options.append({"key": key, "val": val})

        return options

    @staticmethod
    def camel_case_to_text(str):
        words = [[str[0].upper()]]

        for c in str[1:]:
            if words[-1][-1].islower() and c.isupper():
                words.append(list(c))
            else:
                words[-1].append(c)

        word_arr = ["".join(word) for word in words]
        return " ".join(word_arr)

    @staticmethod
    def get_type(val):
        if isinstance(val, bool):
            return "boolean"
        elif isinstance(val, int) or isinstance(val, float):
            return "number"
        return "string"

    @staticmethod
    def to_snake_case(s):
        return "_".join(
            sub(
                "([A-Z][a-z]+)", r" \1", sub("([A-Z]+)", r" \1", s.replace("-", " "))
            ).split()
        ).lower()
