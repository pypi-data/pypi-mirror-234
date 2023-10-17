from enum import Enum
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped

from gateway.server.core.database import Base


class Method(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class Microservice(Base):
    """
    This class will be used to store the microservices

    Attributes:
        id (int): The id of the microservice
        name (str): The name of the microservice
        base_url (str): The base url of the microservice
        is_active (bool): Whether the microservice is active or not
        scopes (list): The scopes of the microservice
    """
    __tablename__ = 'fastapi_gateway_microservices'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, unique=True, index=True)
    base_url: str = Column(String, unique=True, index=True)
    is_active: bool = Column(Boolean, default=True)

    scopes: Mapped[list["Scope"]] = relationship("Scope", back_populates="microservice")

    def __repr__(self):
        return f"<Microservice(name='{self.name}', endpoint='{self.endpoint}')>"

    def __str__(self):
        return f"{self.name}"


class Scope(Base):
    """
    This class will be used to store the scopes

    Attributes:
        id (int): The id of the scope
        name (str): The name of the scope
        path (str): The path of the scope
        is_active (bool): Whether the scope is active or not
        dependencies (list): The dependencies of the scope, stored as a list of strings path to the dependency
        microservice_id (int): The id of the microservice of the scope
        microservice (Microservice): The microservice of the scope
    """
    __tablename__ = 'fastapi_gateway_scopes'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, unique=True, index=True)
    path: str = Column(String, unique=False, index=True)
    microservice_path: str = Column(String, unique=False, index=True)
    is_active: bool = Column(Boolean, default=True)
    dependencies: list[str] = Column(JSON, default=[])
    method: Method = Column(String, default=Method.GET)
    body_params: dict[str, str] = Column(JSON, default={})
    query_params: dict[str, str] = Column(JSON, default={})
    form_params: dict[str, str] = Column(JSON, default={})
    override_headers: bool = Column(Boolean, default=True)
    response_model: str = Column(String, default="")

    microservice_id: int = Column(Integer, ForeignKey('fastapi_gateway_microservices.id'))
    microservice: Mapped["Microservice"] = relationship("Microservice", back_populates="scopes")

    __table_args__ = (
        UniqueConstraint('microservice_id', 'microservice_path', 'method', name='unique_microservice_path'),
        UniqueConstraint('path', 'method', name='unique_path')
    )

    def __repr__(self):
        return f"<Scope(name='{self.name}', path='{self.path}')>"

    def __str__(self):
        return f"{self.name}"
