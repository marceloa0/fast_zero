from http import HTTPStatus

from jwt import decode

from fast_zero.security import create_access_token
from fast_zero.settings import Settings

settings = Settings()


def test_jwt():
    data = {"test": "test"}
    token = create_access_token(data)

    decoded = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert decoded["test"] == data["test"]
    assert "exp" in decoded


def test_jwt_invalid_token(client):
    response = client.delete(
        "/users/1",
        headers={"Authorization": "Bearer token-invalido"},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


def test_jwt_no_sub_sent(client):
    no_sub_token = create_access_token(data={"no-email": "test"})

    response = client.delete(
        "/users/1", headers={"Authorization": f"Bearer {no_sub_token}"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


def test_jwt_no_user(client):
    no_user_token = create_access_token(data={"sub": "test@example.com"})

    response = client.delete(
        "/users/1", headers={"Authorization": f"Bearer {no_user_token}"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}
