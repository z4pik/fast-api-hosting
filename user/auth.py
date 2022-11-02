from fastapi_users import FastAPIUsers
from user.models import user_db
from user.schemas import User, UserDB, UserCreate, UserUpdate
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

SECRET = "Sdasdad3w#RmF34ef43%E5&*6DV%$5DSvBF*fY9V(y*&VNFdfBU(t8DnfDS"

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
