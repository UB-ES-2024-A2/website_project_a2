""" Test CRUD operations on users """
import bcrypt
from app.crud.user import (
    create_user, get_user_by_id, get_user_by_email ,
    read_users, read_top5_matched_users, update_user
)
from app.models import UserCreate, UserUpdate


def test_create_user(db):
    """ Test for creating a new user."""
    user_in = UserCreate(
        name="Test3",
        surname="User",
        username="testuser",
        email="testuser@example.com",
        password="securepassword"
    )

    create_user(cursor=db, user_in=user_in)

    # Verify user was created
    db.execute("SELECT * FROM users WHERE email = %s", (user_in.email,))
    user = db.fetchone()

    assert user is not None
    assert user[4] == user_in.email
    assert bcrypt.checkpw(user_in.password.encode('utf-8'), user[5].encode('utf-8'))

def test_get_user_by_id(db, user_id):
    """Test for retrieving a user by ID."""
    user = get_user_by_id(cursor=db, user_id=user_id)

    assert user is not None
    assert user[0] == user_id

def test_get_user_by_email(db):
    """Test for retrieving a user by email."""
    email = 'test@test'
    user = get_user_by_email(cursor=db, email=email)

    assert user is not None
    assert user[4] == email

def test_read_user(db):
    """ Test Read Users """
    users = read_users(cursor=db)

    assert users is not None
    assert users.count > 0

def test_read_top5_matched_users(db):
    """ Test Read Users by keyword """
    users = read_top5_matched_users(cursor=db, keyword="Test")

    print(users)

    assert users is not None
    assert users.count > 0

def test_update_user(db, user_id):
    test_user = UserUpdate(
        name="Updated User",
        surname="Updated User",
        username="Updated User",
        email="Updated User",
        password="Updated User"
    )

    message = update_user(cursor=db, user_id=user_id, user_in=test_user)

    assert message == "User updated successfully"