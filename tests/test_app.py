from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Olá Mundo!"}


# CRUD de usuários
def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "secret",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "alice",
        "email": "alice@example.com",
        "id": 1,
    }


def test_read_users(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_read_user(client, user):
    response = client.get("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "Teste",
        "email": "teste@test.com",
        "id": 1,
    }


def test_read_user_deve_retornar_404_se_nao_encontrar_user(client):
    response_nao_existe_id = client.get("/users/2")

    assert response_nao_existe_id.status_code == HTTPStatus.NOT_FOUND
    assert response_nao_existe_id.json() == {"detail": "User not found"}

    response_id_negativo = client.get("/users/-1")

    assert response_id_negativo.status_code == HTTPStatus.NOT_FOUND
    assert response_id_negativo.json() == {"detail": "User not found"}


def test_update_user(client, user):
    response = client.put(
        "/users/1",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "bob",
        "email": "bob@example.com",
        "id": 1,
    }


def test_update_user_deve_retornar_404_se_nao_encontrar_user(client):
    response_nao_existe_id = client.put(
        "/users/2",
        json={
            "username": "jack",
            "email": "jack@example.com",
            "password": "secret",
        },
    )

    assert response_nao_existe_id.status_code == HTTPStatus.NOT_FOUND
    assert response_nao_existe_id.json() == {"detail": "User not found"}

    response_id_negativo = client.put(
        "/users/-1",
        json={
            "username": "jack",
            "email": "jack@example.com",
            "password": "secret",
        },
    )

    assert response_id_negativo.status_code == HTTPStatus.NOT_FOUND
    assert response_id_negativo.json() == {"detail": "User not found"}


def test_update_integrity_error(client, user):
    client.post(
        "/users",
        json={
            "username": "fausto",
            "email": "fausto@example.com",
            "password": "secret",
        },
    )

    # Alterando o user.username da fixture para fausto
    response_update = client.put(
        f"users/{user.id}",
        json={
            "username": "fausto",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        "detail": "Username or email already exists"
    }


def test_delete_user(client, user):
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_delete_user_deve_retornar_404_se_nao_encontrar_user(client):
    response_nao_existe_id = client.delete("/users/2")

    assert response_nao_existe_id.status_code == HTTPStatus.NOT_FOUND
    assert response_nao_existe_id.json() == {"detail": "User not found"}

    response_id_negativo = client.delete("/users/-1")

    assert response_id_negativo.status_code == HTTPStatus.NOT_FOUND
    assert response_id_negativo.json() == {"detail": "User not found"}
