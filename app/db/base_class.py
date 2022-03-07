from sqlalchemy import Column
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr


class_registry: dict = {}


@as_declarative(class_registry=class_registry)
class Base:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    __name__: str
    
    @declared_attr
    def __tablename__(cls) -> str:
        '''
            Method for auto-generating table names
        '''
        return cls.__name__.lower()
    