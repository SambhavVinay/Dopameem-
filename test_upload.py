import io
import pytest
from app import app, db, Gooners

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create dummy user
            user = Gooners(user_name="testuser", user_password="testpass")
            db.session.add(user)
            db.session.commit()
            # Simulate login
            with client.session_transaction() as sess:
                sess["user_name"] = "testuser"
                sess["user_id"] = user.user_id
        yield client

def test_file_upload(client):
    with open("tests/files/sample.jpg", "rb") as f:
        data = {
            "file": (f, "sample.jpg")
        }
        response = client.post(
            "/post1", 
            data=data, 
            content_type="multipart/form-data"
        )
    assert response.status_code == 200


