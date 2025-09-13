import logging
from typing import Optional
from fastapi import Request, Depends
from fastapi_users import BaseUserManager, FastAPIUsers, models
from fastapi_users.authentication import JWTStrategy, BearerTransport, AuthenticationBackend

from dependecies.auth import get_user_db
from models import User
from common.settings import Settings

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager[User, int]):
    reset_password_token_secret = Settings().auth.reset_password_token_secret.get_secret_value()
    verification_token_secret = Settings().auth.verification_token_secret.get_secret_value()

    async def on_after_register(self, user, request: Optional[Request] = None):
        logger.debug(f"User {User.email} successfully registered.")

    async def on_after_forgot_password(self, user, token, request: Optional[Request] = None):
        logger.debug(f"User {User.email} forgot password.Reset token: {token}.")

    async def on_after_request_verify(self, user, token, request: Optional[Request] = None):
        logger.debug(f"User {User.email} sent the verification request.Token: {token}.")

    def parse_id(self, user_id):
        return int(user_id)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="/users/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=Settings().auth.jwt_strategy_token_secret.get_secret_value(), lifetime_seconds=3600
    )


auth_backend = AuthenticationBackend(
    name="jwt", transport=bearer_transport, get_strategy=get_jwt_strategy
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)
