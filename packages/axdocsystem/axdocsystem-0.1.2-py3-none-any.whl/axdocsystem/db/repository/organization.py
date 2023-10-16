from axsqlalchemy.repository import BaseRepository
from axdocsystem.db.models import Organization as Model
from axdocsystem.db.schemas import Organization as Schema


class OrganizationRepository(BaseRepository[Model, Schema, Schema]):
    pass

