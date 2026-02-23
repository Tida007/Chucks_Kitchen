from app.database import SessionLocal
from app.models.user import User

db = SessionLocal()

admin = "tonytidatmg@gmail.com"

user = db.query(User).filter(User.email == admin).first()
if user:
    user.is_admin = True
    db.commit()
    print(f"✓ {admin} is now an Admin")
else:
    print("User not found")

db.close()