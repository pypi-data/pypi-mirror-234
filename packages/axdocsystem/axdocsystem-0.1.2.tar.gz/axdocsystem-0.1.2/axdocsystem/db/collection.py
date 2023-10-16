from axabc.db import BaseRepoCollector
from .repository import OrganizationRepository 


class RepoCollection(BaseRepoCollector):
    organization: OrganizationRepository

