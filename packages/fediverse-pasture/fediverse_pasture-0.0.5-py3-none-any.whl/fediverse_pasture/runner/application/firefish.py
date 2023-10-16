import aiohttp
from dataclasses import dataclass
from datetime import datetime
import bovine

from fediverse_pasture.types import ApplicationAdapterForLastActivity


@dataclass
class FirefishApplication:
    domain: str
    username: str
    session: aiohttp.ClientSession | None = None

    async def determine_actor_uri(self):
        actor_uri, _ = await bovine.clients.lookup_uri_with_webfinger(
            self.session, f"acct:{self.username}@{self.domain}", f"http://{self.domain}"
        )
        return actor_uri

    async def top_public(self):
        response = await self.session.post(
            f"http://{self.domain}/api/notes/global-timeline"
        )
        public_timeline = await response.json()
        return public_timeline[0]

    async def top_public_with_published(self, published: datetime) -> dict | None:
        data = await self.top_public()
        created_at = data.get("createdAt")
        created_at = datetime.fromisoformat(created_at.removesuffix("Z"))
        if created_at == published:
            return data
        return None

    async def last_activity(self, session: aiohttp.ClientSession):
        self.session = session

        actor_uri = await self.determine_actor_uri()

        return ApplicationAdapterForLastActivity(
            actor_uri=actor_uri,
            fetch_activity=self.top_public_with_published,
            application_name="firefish",
        )
