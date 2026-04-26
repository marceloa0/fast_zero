# Fast_zero

Fast_zero é um projeto desenvolvido com base no curso "FastAPI do Zero", elaborado por [Eduardo Mendes (dunossauro)](https://github.com/dunossauro). O seu propósito é criar uma aplicação de gerenciamento de tarefas passando pelos principais tópicos no desenvolvimento de uma API com FastAPI, como criação de rotas, schemas, models, configuração de ambiente de desenvolvimento, banco de dados, etc.

## Tecnologias e ferramentas

- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- Poetry
- Pytest
- Taskipy

## Como executar o projeto

### Pré-requisitos

- Python 3.12
- Poetry instalado (pip install poetry)

### Passo a passo

1. Clone o repositório

```
git clone https://github.com/marceloa0/fast_zero.git
cd fast_zero
```

2. Instale as dependências

```
poetry install
```

3. Rode as migrações:

```
poetry run alembic upgrade head
```

4. Execute o servidor de desenvolvimento

```
poetry run fastapi dev fast_zero/app.py
```

O servidor estará disponível em `http://127.0.0.1:8000`. Você pode acessar a documentação interativa da API (Swagger UI) em `/docs`.

## Testes

```
# Rodar todos os testes
poetry run pytest -v

# Rodar testes com cobertura
poetry run pytest --cov=fast_zero
```

## Como contribuir

1. Faça um Fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feat/minha-feature`).
3. Faça o Commit das suas alterações (`git commit -m 'feat: Adicionando nova funcionalidade'`).
4. Faça o Push para a branch remota (`git push origin feature/minha-feature`).
5. Abra um Pull Request.