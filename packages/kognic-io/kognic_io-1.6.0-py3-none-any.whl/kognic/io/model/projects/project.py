from datetime import datetime

from kognic.io.model.base_serializer import BaseSerializer
from kognic.io.util import ts_to_dt


class Project(BaseSerializer):
    created: datetime
    title: str
    description: str
    status: str
    project: str
