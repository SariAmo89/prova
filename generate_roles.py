import sys
sys.path.append('D:\\Python\\hydro')

from backend.config import app
from backend.config import Role
from backend.config import db

app.app_context().push()

role = Role(
    name = 'admin',
    desc = 'Administrator'
)
db.session.add(role)
db.session.commit()