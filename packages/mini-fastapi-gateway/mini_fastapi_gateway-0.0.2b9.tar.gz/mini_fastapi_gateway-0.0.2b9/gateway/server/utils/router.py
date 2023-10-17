"""
This file contains the functions that will be used to dynamically create routes and match the path of the request to
the microservices path of the scope

Functions:
    make_route(params: dict = None) -> function
    match_path(path: str) -> tuple[str, dict] or tuple[None, None]
"""
import re
import importlib
from typing import Callable, Dict, Type, TYPE_CHECKING, Union
from urllib.parse import urlparse

import cachetools
from fastapi import Response

if TYPE_CHECKING:
    from gateway.server.core.database.models import Scope


# Define the type hint for 'params'
T = Dict[str, Type]

# Initialize the cache
cache = cachetools.LRUCache(maxsize=100)

# Define a regular expression pattern to match text inside a {}
pattern = r'\{([^}]+)\}'


# Define a function to replace matches with the last string after the dot
def replace_last_string(match):
    match_content = match.group(1)  # Extract the content inside {}
    parts = match_content.split('.')  # Split by dot
    if len(parts) > 1:
        return parts[-1]  # Return the last part after the dot
    else:
        return match_content  # If there's no dot, return the original content


def process_params(scope: "Scope", param_type: str):
    import_strings = []
    string_params = []
    params = getattr(scope, param_type, None)
    if params:
        for key, value in params.items():
            matches = re.findall(pattern, value)
            value = re.sub(pattern, replace_last_string, value)
            if param_type == 'form_params':
                string_params.append(f"{key}: Annotated[{value}, Form()]")
            else:
                string_params.append(f"{key}: {value}")
            for match in matches:
                res = get_module_path_and_class_name(match)
                if (res is None) or (len(res) != 2):
                    continue
                import_strings.append(f"from {res[0]} import {res[1]}\n")

    return import_strings, string_params


# We will use this function to dynamically create a function that will be used as a route
@cachetools.cached(cache, key=lambda func_name, *args: f"cached_f_{func_name}")
def make_route(func_name: str, scope: "Scope", params: T = None) -> Callable[..., Response]:
    """
    This function will dynamically create a function that will be used as a route
    :param scope: Scope
    :param func_name: str
    :param params: dict
    :return: function
    """
    # If params is None, initialize it as an empty dictionary
    if params is None:
        params = {}

    # Create an empty dictionary 'd' to store the function
    d = {}
    # Define the required parameters for the function
    string_params = ['request: Request', 'response: Response']

    # Add the parameters from the 'params' dictionary
    for key, value in params.items():
        string_params.append(f"{key}: {value.__name__}")

    import_strings, string_params1 = process_params(scope, 'body_params')
    import_strings2, string_params2 = process_params(scope, 'form_params')
    import_strings3, string_params3 = process_params(scope, 'query_params')
    import_strings += import_strings2 + import_strings3
    string_params += string_params1 + string_params2 + string_params3

    # Define the function using 'exec()'
    function_definition = (f"from typing import Annotated, Union, Optional\n"
                           f"from fastapi import Body, Form, Request, Depends, Response\n"
                           f"{''.join(import_strings)}"
                           f"async def {func_name}({','.join(string_params)}): pass")

    # Execute the function definition and store it in dictionary 'd'
    exec(function_definition, d)

    # Return the dynamically created function 'f'
    return d[func_name]


# We will use this function to match the path of the request to the microservices path of the scope
def match_path(path: str, scopes: list["Scope"] = None) -> tuple["Scope", dict] or tuple[None, None]:
    """
    This function will match the path of the request to the microservices path of the scope
    :param scopes: List[Scope]
    :param path: str
    :return: Tuple[str, dict] or Tuple[None, None]
    """

    d = {}
    for scope_path in scopes:
        if not scope_path.is_active:
            continue

        parsed_scope = urlparse(scope_path.path)
        parsed_path = urlparse(path)
        split_scope = parsed_scope.path.split('/')
        split_path = parsed_path.path.split('/')

        if len(split_scope) != len(split_path):
            continue

        for i, part in enumerate(split_scope):
            if part.startswith('{') and part.endswith('}'):
                _key, _type = part[1:-1].split(':')
                try:
                    python_type = eval(_type)
                    d[_key] = python_type
                except NameError:
                    break
                continue

            if part != split_path[i]:
                return None, None

        return scope_path, d

    return None, None


# We will use this function to get the parameters from the path
@cachetools.cached(cache, key=lambda scope_path: scope_path)
def get_params_from_path(scope_path: str) -> dict:
    """
    This function will get the parameters from the path
    :param scope_path: str
    :return: dict
    """
    parsed_scope = urlparse(scope_path)
    split_scope = parsed_scope.path.split('/')

    d = {}

    for i, part in enumerate(split_scope):
        if part.startswith('{') and part.endswith('}'):
            _key, _type = part[1:-1].split(':')
            try:
                python_type = eval(_type)
                d[_key] = python_type
            except NameError:
                break
            continue

    return d


def delete_cache(scope: "Scope") -> None:
    """
    This function will delete the cache
    :return: None
    """
    func_name = scope.name.replace(' ', '_').lower()
    if f"cached_f_{func_name}" in cache:
        del cache[f"cached_f_{func_name}"]
    if scope.path in cache:
        del cache[scope.path]
    if "openapi_cache" in cache:
        del cache["openapi_cache"]

    cache["need_reload"] = True


def get_module_path_and_class_name(module_string: str) -> Union[tuple[str, str], None]:
    """
    This function will return the module path and the class name
    :param module_string: str
    :return: tuple[str, str]
    """
    try:
        module_path, class_name = module_string.rsplit('.', 1)
        return module_path, class_name
    except ValueError:
        return None


def import_from_module_string(module_string: str) -> Union[Type, None]:
    """
    This function will import a class from a module string
    :param module_string: str
    :return: Type
    """
    try:
        res = get_module_path_and_class_name(module_string)
        if (res is None) or (len(res) != 2):
            return None
        module = importlib.import_module(res[0])
        return getattr(module, res[1])
    except (ImportError, AttributeError, ValueError):
        return None
