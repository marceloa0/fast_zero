from dataclasses import asdict
from datetime import datetime

import pytest
from sqlalchemy import select

from fast_zero.models import Todo, User


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username="alice", password="secret", email="teste@test"
        )
        session.add(new_user)
        await session.commit()

    user = await session.scalar(select(User).where(User.username == "alice"))

    assert asdict(user) == {
        "id": 1,
        "username": "alice",
        "password": "secret",
        "email": "teste@test",
        "created_at": time,
        "updated_at": time,
        "todos": [],
    }


@pytest.mark.asyncio
async def test_update_user(session, mock_db_time):
    with mock_db_time(model=User, time=datetime(2024, 1, 1)) as creation_time:
        new_user = User(
            username="alice", password="secret", email="teste@test"
        )
        session.add(new_user)
        await session.commit()

    user = await session.scalar(select(User).where(User.username == "alice"))

    with mock_db_time(model=User, time=datetime(2024, 1, 2)) as update_time:
        user.username = "alice.freitas"
        session.add(user)
        await session.commit()
        await session.refresh(user)

    assert asdict(user) == {
        "id": 1,
        "username": "alice.freitas",
        "password": "secret",
        "email": "teste@test",
        "created_at": creation_time,
        "updated_at": update_time,
        "todos": [],
    }


@pytest.mark.asyncio
async def test_create_todo(session, user):
    todo = Todo(
        title="Test Todo",
        description="Test Desc",
        state="draft",
        user_id=user.id,
    )

    session.add(todo)
    await session.commit()

    todo = await session.scalar(select(Todo))

    assert asdict(todo) == {
        "description": "Test Desc",
        "id": 1,
        "state": "draft",
        "title": "Test Todo",
        "user_id": user.id,
    }


@pytest.mark.asyncio
async def test_user_todo_relationship(session, user):
    # cria o todo com o user
    todo = Todo(
        title="Test Todo",
        description="Test Desc",
        state="draft",
        user_id=user.id,
    )
    # salva no banco
    session.add(todo)
    await session.commit()
    await session.refresh(user)

    user = await session.scalar(select(User).where(User.id == user.id))

    # testa se user.todos tem o todo criado
    assert user.todos == [todo]
