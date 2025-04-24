from pydantic import BaseModel, ConfigDict


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"

    model_config = ConfigDict(from_attributes=True)
