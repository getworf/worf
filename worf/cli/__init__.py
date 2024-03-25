from .api import api
from .worker import worker
from .db import db
from .user import user
from .tenant import tenant

commands = [api, worker, db, user, tenant]
