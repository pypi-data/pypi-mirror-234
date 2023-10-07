import os

import humanize.time
import rich.console
import rich.table
import typer

from . import config, sentry

app = typer.Typer()

console = rich.console.Console(highlight=False)


def print_issues(issues: list[sentry.SentryIssue], title: str) -> None:
    table = rich.table.Table(show_lines=True, title=title)
    table.add_column("Issue")
    table.add_column("Count")
    table.add_column("First Seen")
    table.add_column("Last Seen")
    for issue in issues:
        table.add_row(
            f"[link={issue.permalink}]{issue.title}[/]",
            str(issue.count),
            humanize.time.naturaltime(issue.first_seen),
            humanize.time.naturaltime(issue.last_seen),
        )
    console.print(table)


@app.command("configure")
def configure() -> None:
    typer.launch(str(config.get_config_path()))


@app.command("issues")
def get_issues(
    env: str,
    query: str,
    take: int | None = None,
    sort: sentry.SortMode | None = None,
) -> None:
    try:
        config_ = config.get_config()
    except config.NoConfig:
        console.print("App has not been configured")
        raise typer.Exit(code=1)

    sentry_token = config_.sentry_token or os.getenv("SENTRY_TOKEN")
    if not sentry_token:
        console.print(
            "No sentry token (set sentry_token in the config file or use the SENTRY_TOKEN environment variable)"
        )
        raise typer.Exit(code=1)

    try:
        env = config_.envs[env]
    except KeyError:
        console.print("Unrecognized environment")
        console.print("Configured environment: " + ", ".join(config_.envs.keys()))
        raise typer.Exit(code=1)

    sentry_client = sentry.SentryClient(
        sentry_token=sentry_token,
        organisation=env.organisation,
        project=env.project,
        environment=env.environment,
    )

    if query.startswith(":"):
        try:
            query_config = config_.queries[query[1:]]
        except KeyError:
            console.print("Unrecognized query")
            console.print("Configured queries: " + ", ".join(config_.queries.keys()))
            raise typer.Exit(code=1)

        query = query_config.query
        take = take or query_config.take
        sort = sort or query_config.sort_mode
        title = query_config.title
    else:
        title = query

    take = take or 10
    sort = sort or sentry.SortMode.LAST_SEEN

    issues = sentry_client.get_issues_for_query(query, take, sort)
    print_issues(issues, title)


if __name__ == "__main__":
    app()
