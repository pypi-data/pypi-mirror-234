import sqlalchemy as sa
from axsqlalchemy.model import BaseTableInt, Base


__all__ = [
    'Base',
    'Organization',
]


class Organization(BaseTableInt):
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.String)

