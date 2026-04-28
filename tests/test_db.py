from dataclasses import asdict
from datetime import datetime

from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username="alice", password="secret", email="teste@test"
        )
        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == "alice"))

    assert asdict(user) == {
        "id": 1,
        "username": "alice",
        "password": "secret",
        "email": "teste@test",
        "created_at": time,
        "updated_at": time,
    }


def test_update_user(session, mock_db_time):
    with mock_db_time(model=User, time=datetime(2024, 1, 1)) as creation_time:
        new_user = User(
            username="alice", password="secret", email="teste@test"
        )
        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == "alice"))

    with mock_db_time(model=User, time=datetime(2024, 1, 2)) as update_time:
        user.username = "alice.freitas"
        session.add(user)
        session.commit()
        session.refresh(user)

    assert asdict(user) == {
        "id": 1,
        "username": "alice.freitas",
        "password": "secret",
        "email": "teste@test",
        "created_at": creation_time,
        "updated_at": update_time,
    }
