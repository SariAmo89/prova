import sys
sys.path.append('D:\\Python\\hydro')

from backend.config import app
from backend.config import UserRole
from backend.config import db

app.app_context().push()

userRole = UserRole(
    user_id = 2,
    role_id = 1
)
db.session.add(userRole)
db.session.commit()