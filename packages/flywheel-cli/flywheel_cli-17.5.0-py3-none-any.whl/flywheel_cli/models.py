"""Flywheel CLI global models"""

from pydantic import BaseModel


class FWAuth(BaseModel):
    """Flywheel site and user info model"""

    api_key: str
    host: str
    user_id: str
    is_admin: bool
    is_device: bool
