"""
This file contains the CRUD classe for the database

Classes:
    CRUD: This class will be used to create the CRUD classes for the database
"""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from gateway.server.core.database import Base

# Define the type hint for 'ModelType'
ModelType = TypeVar("ModelType", bound=Base)

# Define the type hint for 'CreateSchemaType'
CreateSchemaType = TypeVar("CreateSchemaType")

# Define the type hint for 'UpdateSchemaType'
UpdateSchemaType = TypeVar("UpdateSchemaType")


# We will use this class to create the CRUD classes for the database
class CRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        """
        This function will initialize the CRUD class
        :param model: Type[ModelType]
        """
        self.model = model

    def get(self, db: Session, pk: int) -> Optional[ModelType]:
        """
        This function will get the model from the database
        :param db: Session
        :param pk: int
        :return: Optional[ModelType]
        """
        return db.query(self.model).filter(self.model.id == pk).first()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 10000, options: list = None) -> List[ModelType]:
        """
        This function will get multiple models from the database
        :param options: list
        :param db: Session
        :param skip: int
        :param limit: int
        :return: List[ModelType]
        """
        if options is None:
            options = []
        return db.query(self.model).options(*options).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        This function will create a model in the database
        :param db: Session
        :param obj_in: CreateSchemaType
        :return: ModelType
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        This function will update a model in the database
        :param db: Session
        :param db_obj: ModelType
        :param obj_in: Union[UpdateSchemaType, Dict[str, Any]]
        :return: ModelType
        """
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def remove(self, db: Session, *, pk: int) -> ModelType:
        """
        This function will remove a model from the database
        :param db: Session
        :param pk: int
        :return: ModelType
        """
        obj = db.query(self.model).get(pk)
        db.delete(obj)
        db.commit()

        return obj
