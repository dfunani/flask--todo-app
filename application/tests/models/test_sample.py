from app import app
from models.todo import Users

# Simple integration testing (DB Models exists)
def test_users():
    # Init a new User
    user = Users( email = "dfunani@gmail.com",
    username = "delali",
    hashcode = "db.Column(db.String(255), nullable=False))"
    )

    # Assert the validity of the user initialized
    assert user.email == "dfunani@gmail.com"
    assert user.username == "delali"
    assert user.hashcode == "db.Column(db.String(255), nullable=False))"

# Simple Unit testing login Endpoint
def test_login():
    # Simple test of the token endpoint
    with app.test_client() as testClient:
        response = testClient.get('/login')
        assert response.status_code == 200
        # Checks the login page is returned
        assert b"Flask TODO App" in response.data