import re

from polar.config import settings
from polar.models import Issue, Organization, Repository


class GithubBadge:
    BADGE_START = "<!-- POLAR PLEDGE BADGE START -->"
    BADGE_END = "<!-- POLAR PLEDGE BADGE END -->"
    BADGE_REGEX = re.compile(
        r"<!-- POLAR PLEDGE BADGE START -->(.*?)<!-- POLAR PLEDGE BADGE END -->",
        re.DOTALL,
    )

    def __init__(
        self,
        *,
        organization: Organization,
        repository: Repository,
        issue: Issue,
        pledge_as_action: bool = False,
    ) -> None:
        self.organization = organization
        self.repository = repository
        self.issue = issue
        self.pledge_as_action = pledge_as_action

    def generate_svg_url(self) -> str:
        return f"{settings.BACKEND_BASE_URL}/api/github/{self.organization.name}/{self.repository.name}/issues/{self.issue.number}/pledge.svg"

    def generate_issue_url(self) -> str:
        return f"{settings.FRONTEND_BASE_URL}/{self.organization.name}/{self.repository.name}/issues/{self.issue.number}"

    def generate_org_url(self) -> str:
        return f"{settings.FRONTEND_BASE_URL}/{self.organization.name}"

    def badge_markdown(self) -> str:
        svg_url = self.generate_svg_url()
        issue_url = self.generate_issue_url()
        org_url = self.generate_org_url()

        return f"""{self.BADGE_START}
## Upvote & Fund

- We're using [Polar.sh]({org_url}) so you can upvote and help fund this issue.
- We receive the funding once the issue is completed & confirmed by you.
- Thank you in advance for helping prioritize & fund our backlog.

<a href="{issue_url}">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="{svg_url}?darkmode=1">
  <img alt="Fund with Polar" src="{svg_url}">
</picture>
</a>
{self.BADGE_END}"""

    @classmethod
    def has_badge(cls, body: str | None) -> bool:
        if not body:
            return False
        return bool(cls.BADGE_REGEX.search(body))

    @classmethod
    def strip_badge(cls, body: str | None) -> str:
        if not body:
            return ""
        return cls.BADGE_REGEX.sub("", body).strip()

    def embed(self, body: str | None) -> str:
        badge = self.badge_markdown()
        if not body:
            return badge

        if self.has_badge(body):
            return self.BADGE_REGEX.sub(lambda m: badge, body)

        return f"{body.rstrip()}\n\n{badge}"
