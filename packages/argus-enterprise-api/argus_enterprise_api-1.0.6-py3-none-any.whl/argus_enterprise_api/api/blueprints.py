import json
import os
from .utils import camel_to_snake, compile_method_name, make_api_method


class Blueprint:
    _MODULE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, client):
        self._client = client

        class_name = self.__class__.__name__
        doc_help = f"{class_name}Api-{self._client.version.replace('.', '_')}"
        swagger_file_name = f"{doc_help}-swagger.json"
        self._doc_help_url = f"https://cloud.altusplatform.com/help/{doc_help}.html"
        self._spec_path = f"{self._MODULE_DIRECTORY}/spec/{swagger_file_name}"

        self.__doc__ = (
            f"{class_name}: A Python class for interacting with the Argus {class_name} API.\n\n"
            f"This class provides methods to interface with the {class_name}-related operations in the Argus API."
            "The methods are dynamically generated based on the Swagger API specification,"
            f"allowing for a convenient and straightforward way to interact with the {class_name} API.\n\n"
            "Attributes:\n\t"
            "client (ArgusClient): An instance of the ArgusClient class for API interactions.\n\n"
            "Internal Attributes:\n\t"
            "spec_path (str): Internal attribute pointing to the Swagger JSON specification file.\n\t"
            "The path is generated dynamically based on the ArgusClient version.\n\n"
            "Example:\n\t"
            f"# The {class_name} class is usually instantiated through the ArgusClient.\n\t"
            "client = ArgusClient(...)\n\t"
            f"{camel_to_snake(class_name)}_instance = client.{camel_to_snake(class_name)}\n\t"
            f"{camel_to_snake(class_name)}_instance.some_method()  # some_method() would be a dynamically generated API method.\n\n"
            "Documentation:\n\t"
            "For more technical details, refer to https://cloud.altusplatform.com/help/index.htm\n\t"
            f"{class_name} API Swagger: {self._doc_help_url}"
        )

        with open(self._spec_path) as f:
            swagger_json = json.load(f)

        base_url = swagger_json["servers"][0]["url"]
        tags = list(
            set(
                [
                    details["tags"][0]
                    for path, methods in swagger_json["paths"].items()
                    for method, details in methods.items()
                ]
            )
        )

        for tag in tags:
            paths = {
                path: methods
                for path, methods in swagger_json["paths"].items()
                for method, details in methods.items()
                if details["tags"][0] == tag
            }
            dynamic_class_name = camel_to_snake(tag)
            dynamic_class = self._create_dynamic_class(
                paths, base_url, self._doc_help_url
            )
            setattr(self, dynamic_class_name, dynamic_class(self._client))

    def _create_dynamic_class(self, paths, base_url, doc_help_url):
        class Tag:
            def __init__(self, client):
                self._client = client
                self._init_dynamic_methods()

            def _init_dynamic_methods(self):
                for path, methods in paths.items():
                    for method, details in methods.items():
                        method_name = compile_method_name(method, path)
                        setattr(
                            self,
                            method_name,
                            make_api_method(
                                method, path, base_url, details, doc_help_url
                            ).__get__(self),
                        )

        return Tag


class Workspace(Blueprint):
    pass


class ModelManagement(Blueprint):
    pass
