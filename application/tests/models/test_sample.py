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
