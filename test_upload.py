import io
import pytest
from app import app, db, Gooners

@pytest.fixture
def client():
    # Configure app for testing
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:test.db"
    app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for tests if using Flask-WTF

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            
            # Create dummy user
            user = Gooners(user_name="testuser", user_password="testpass")
            db.session.add(user)
            db.session.commit()

            # Simulate login session
            with client.session_transaction() as sess:
                sess["user_name"] = "testuser"
                sess["user_id"] = user.user_id
        
        yield client


def test_file_upload(client):
    # Use in-memory file (instead of actual sample.jpg file dependency)
    file_data = io.BytesIO(b"fake image data")
    file_data.name = "sample.jpg"

    data = {
        "file": (file_data, "sample.jpg")
    }

    response = client.post(
        "/post1",
        data=data,
        content_type="multipart/form-data"
    )

    # Expect success
    assert response.status_code == 200
