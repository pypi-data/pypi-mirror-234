import pydantic
from typing import Optional, Dict

from gateway.server.core.database.models import Method


class MicroserviceCreate(pydantic.BaseModel):
    """
    This class will be used to create a microservice

    Attributes:
        name (str): The name of the microservice
        base_url (str): The base url of the microservice
        is_active (bool): Whether the microservice is active or not
    """
    name: str
    base_url: str
    is_active: bool

    class Config:
        if pydantic.__version__ > "2.0.0":
            from_attributes = True
        else:
            orm_mode = True


class MicroserviceRead(MicroserviceCreate):
    """
    This class will be used to store the microservices

    Attributes:
        id (int): The id of the microservice
        name (str): The name of the microservice
        base_url (str): The base url of the microservice
        is_active (bool): Whether the microservice is active or not
    """
    id: int


class ScopeCreate(pydantic.BaseModel):
    """
    This class will be used to create a scope

    Attributes:
        name (str): The name of the scope
        path (str): The path of the scope
        is_active (bool): Whether the scope is active or not
        dependencies (list): The dependencies of the scope, stored as a list of strings path to the dependency
        microservice_id (int): The id of the microservice of the scope
    """
    name: str
    path: str
    microservice_path: str
    is_active: bool
    dependencies: list[str]
    microservice_id: int
    method: Method
    body_params: Optional[Dict[str, str]] = {}
    query_params: Optional[Dict[str, str]] = {}
    form_params: Optional[Dict[str, str]] = {}
    override_headers: Optional[bool] = True
    response_model: Optional[str] = ""

    class Config:
        if pydantic.__version__ > "2.0.0":
            from_attributes = True
        else:
            orm_mode = True


class ScopeRead(ScopeCreate):
    """
    This class will be used to store the scopes

    Attributes:
        id (int): The id of the scope
    """
    id: int
    dependencies: Optional[list[str]] = None
    method: Optional[Method] = "GET"
    microservice_id: Optional[int] = None


class ScopeUpdate(ScopeCreate):
    """
    This class will be used to update a scope and will be optional for all fields
    """
    name: Optional[str] = None
    path: Optional[str] = None
    microservice_path: Optional[str] = None
    is_active: Optional[bool] = None
    dependencies: Optional[list[str]] = None
    microservice_id: Optional[int] = None
    method: Optional[Method] = None


class MicroserviceUpdate(MicroserviceCreate):
    """
    This class will be used to update a microservice and will be optional for all fields
    """
    name: Optional[str] = None
    base_url: Optional[str] = None
    is_active: Optional[bool] = None

