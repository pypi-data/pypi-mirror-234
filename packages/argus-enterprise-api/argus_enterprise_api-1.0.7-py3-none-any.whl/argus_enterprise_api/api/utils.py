import re
import requests
import json
from json.decoder import JSONDecodeError


def camel_to_snake(string):
    acronyms = ["KPI", "FX"]

    for acronym in acronyms:
        string = string.replace(acronym, f"{acronym[0]}{acronym[1:].lower()}")

    string = re.sub(r"[^a-zA-Z0-9]", "", string)
    string = re.sub(r"(?<!^)(?=[A-Z])", "_", string).lower()

    return string


def compile_method_name(method, path):
    orig_path = path
    rems = ["api/", "Workspace/PropertyAsset/"]

    for rem in rems:
        path = path.replace(rem, "")

    method = method.replace("delete", "del")

    path_split = path.split("/")
    path_split = [x for x in path_split if x]

    path_names = [camel_to_snake(x) for x in path_split if not re.search(r"{.*}", x)]
    path_names = "_".join(path_names)

    path_vars = [camel_to_snake(x) for x in path_split if re.search(r"{*.}", x)]
    path_vars = "_and_".join(path_vars)

    name = (
        f"{method}_property_asset"
        if not path_names and "PropertyAsset" in orig_path
        else f"{method}_{path_names}"
    )
    name = f"{name}_by_{path_vars}" if path_vars else name

    return name


def prepare_url(path, **kwargs):
    path_vars = [x[1:-1] for x in path.split("/") if re.search(r"{.*}", x)]
    if path_vars:
        for path_var in path_vars:
            if path_var not in kwargs:
                raise ValueError(f"Required path variable '{path_var}' not provided")
            path = path.replace(f"{{{path_var}}}", str(kwargs[path_var]))
    return path


def prepare_payload_and_files(method, content_type, body, files):
    payload, upload_files = None, None
    if method.upper() in ["POST", "PUT"]:
        if content_type == "application/json":
            payload = json.dumps(body) if body else None
        elif content_type == "multipart/form-data":
            upload_files = files
        else:
            payload = body if body else None
    return payload, upload_files


def make_api_method(method, path, base_url, details, doc_help_url):
    content_type_list = list(details.get("requestBody", {}).get("content", {}).keys())
    content_type = content_type_list[0] if content_type_list else None

    summary = details.get("summary")
    description = details.get("description")
    payload_description = details.get("requestBody", {}).get("description")
    payload_example = (
        details.get("requestBody", {})
        .get("content", {})
        .get(content_type, {})
        .get("example")
        if content_type
        else None
    )
    api_documentation = (
        f"{doc_help_url}#/{details['tags'][0]}/{method}{re.sub(r'[{}/]', '_', path)}"
    )

    def api_method(self, body=None, query_params=None, files=None, **kwargs):
        # Prepare URL with path variables replaced
        url = f"{base_url}{prepare_url(path, **kwargs)}"

        # Prepare headers
        headers = self._client._get_base_headers()
        content_type and headers.update({"Content-Type": content_type})

        # Prepare params, payload and upload_files
        payload, upload_files = prepare_payload_and_files(
            method, content_type, body, files
        )

        # Send HTTP Request
        params = query_params or {}
        response = requests.request(
            method.upper(),
            url,
            headers=headers,
            params=params,
            data=payload,
            files=upload_files,
        )

        response_description = (
            details.get("responses", {})
            .get(str(response.status_code), {})
            .get("description", "")
        )

        if not response.ok:
            raise requests.RequestException(
                f"Error {response.status_code}: {response.text or response_description}"
            )

        try:
            response_json = response.json()
            return response_json
        except JSONDecodeError:
            response_json = {
                "status_code": response.status_code,
                "description": response_description,
            }
            return response_json

    api_method.__doc__ = (
        f"Method: {method.upper()}\n\n"
        f"Endpoint: '{path}'\n\n"
        f"Summary: {summary}\n\n"
        f"Description:\n{description}\n\n"
        f"Payload Description: {payload_description}\n\n"
        f"Payload Example:\n{payload_example}\n\n"
        f"API Documentation: {api_documentation}"
    )

    return api_method
