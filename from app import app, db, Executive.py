from app import app, db, Executive
with app.app_context():
    exec_user = Executive(
        username="admin",
        password=generate_password_hash("admin123"),
        full_name="System Admin",
        email="kabuusumonalisa@gmail.com",
        phone="+256703953711"
    )
    db.session.add(exec_user)
    db.session.commit()