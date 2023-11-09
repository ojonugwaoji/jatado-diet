
from typing import Annotated, Optional
from pydantic import BaseModel
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

# Create a custom OAuth2PasswordBearer-like dependency


class MockOAuth2PasswordBearer(OAuth2PasswordBearer):
    def __init__(self, tokenUrl: str = "token"):
        self.tokenUrl = tokenUrl

    async def __call__(self, request: Request) -> Optional[str]:
        return request


mock_oauth2_scheme = MockOAuth2PasswordBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
OAuthTokenDeps = Annotated[str, Depends(oauth2_scheme)]
