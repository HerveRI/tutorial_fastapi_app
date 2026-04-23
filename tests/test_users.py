import pytest
from jose import jwt
from app import schema
#from .database import client, session
from app.config import settings


# SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

## Tell sqlalchemcy to build all tables based on the models
# Base.metadata.create_all(bind=engine)

# def override_get_db():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     try:
#         yield db 
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db

# @pytest.fixture
# def session():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @pytest.fixture
# def client(session):
#     def override_get_db():
#         try:
#             yield session
#         finally:
#             session.close()
#     app.dependency_overrides[get_db] = override_get_db
#     yield TestClient(app)

    #Base.metadata.drop_all(bind=engine)
    #Base.metadata.create_all(bind=engine)
    # Allows to run code before we return client - create the tables
    #yield TestClient(app)
    # Allow to run code after test finishes - drop created tables
    #Base.metadata.drop_all(bind=engine)
#client = TestClient(app)

def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == "Welcome to my API - Successfuly CI/CD witn DG_Ocean"
    assert res.status_code == 200

# Pass in the client fixture
def test_create_user(client):
    res = client.post("/users/", json={"email": "myname@gmail.com", "password": "password123"})
    
    new_user = schema.UserResponse(**res.json())
    print(res.json())
    assert new_user.email == "myname@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schema.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert int(id) == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


#@pytest.mark.parametrize("email, password, status_code", [list])
def test_incorrect_login(test_user, client):
    res = client.post("/login", data={"username": test_user['email'], "password": "wrongPassword"})

    assert res.status_code == 403
    assert res.json().get('detail') == "Invalid credentials"