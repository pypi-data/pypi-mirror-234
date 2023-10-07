import dataclasses
import datetime
import enum
from urllib.parse import urlencode as encode_query_params

import pydantic
import requests


class SentryIssue(pydantic.BaseModel):
    id: int
    permalink: str
    title: str
    first_seen: datetime.datetime = pydantic.Field(..., alias="firstSeen")
    last_seen: datetime.datetime = pydantic.Field(..., alias="lastSeen")
    count: int


class SortMode(enum.Enum):
    LAST_SEEN = "LAST_SEEN"
    COUNT = "COUNT"


@dataclasses.dataclass(kw_only=True, frozen=True)
class SentryClient:
    sentry_token: str
    organisation: str
    project: str
    environment: str

    # TODO Handle paging when `take` is greater than single page size.
    def get_issues_for_query(
        self, query: str, take: int, sort_mode: SortMode
    ) -> list[SentryIssue]:
        query_params = {
            "environment": self.environment,
            "query": query,
            "statsPeriod": "14d",
        }

        if sort_mode != SortMode.LAST_SEEN:
            # LAST_SEEN is the sentry default - no param needed.
            sort_query_param = {SortMode.COUNT: "freq"}[sort_mode]
            query_params["sort"] = sort_query_param

        url = (
            f"https://sentry.io/api/0/projects/{self.organisation}/{self.project}/issues/?"
            + encode_query_params(query_params)
        )

        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {self.sentry_token}"},
        )
        response.raise_for_status()

        return [SentryIssue.model_validate(issue) for issue in response.json()][:take]
