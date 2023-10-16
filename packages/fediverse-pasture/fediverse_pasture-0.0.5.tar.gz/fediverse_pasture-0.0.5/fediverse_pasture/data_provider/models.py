from pydantic import BaseModel
from typing import List


class ActorKeyPair(BaseModel):
    name: str
    public: str
    private: str


class ActorData(BaseModel):
    actor_name: str
    key_pairs: List[ActorKeyPair] = []
    user_part: str | None = None

    summary: str = ""

    requires_signed_get_for_actor: bool = False
    requires_signed_post_for_inbox: bool = False
