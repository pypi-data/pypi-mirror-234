from dataclasses import dataclass
from datetime import datetime

from bovine.clients.bearer import BearerAuthClient

from fediverse_pasture.types import ApplicationAdapterForLastActivity


@dataclass
class MastodonApplication:
    domain: str
    access_token: str
    username: str
    client: BearerAuthClient | None = None

    def actor_uri(self):
        return f"http://{self.domain}/users/{self.username}"

    async def top_public(self):
        response = await self.client.get(
            f"http://{self.domain}/api/v1/timelines/public"
        )
        public_timeline = await response.json()
        return public_timeline[0]

    async def top_public_with_published(self, published: datetime) -> dict | None:
        data = await self.top_public()
        created_at = data.get("created_at")
        if not created_at:
            return None
        created_at = datetime.fromisoformat(created_at.removesuffix("Z"))
        if created_at == published:
            return data
        return None

    def last_activity(self, session):
        self.client = BearerAuthClient(session, self.access_token)

        return ApplicationAdapterForLastActivity(
            actor_uri=self.actor_uri(),
            fetch_activity=self.top_public_with_published,
            application_name="mastodon",
        )
