"""Fetch and print a short news brief for a selected category."""

import os
import sys
from datetime import datetime, timezone
from typing import Any

import requests
from dotenv import load_dotenv

API_URL = "https://newsapi.org/v2/top-headlines"
CATEGORIES = {
    "1": ("technology", "Technology"),
    "2": ("business", "Business"),
    "3": ("health", "Health"),
}
MAX_HEADLINES = 5
TIMEOUT_SECONDS = 15


def choose_category() -> tuple[str, str] | None:
    """Ask the user to select one of the supported news categories."""
    print("Choose a news category:")
    for number, (_, label) in CATEGORIES.items():
        print(f"  {number}. {label}")

    choice = input("Enter 1, 2, or 3: ").strip()
    return CATEGORIES.get(choice)


def format_published_at(value: str | None) -> str:
    """Convert a NewsAPI UTC timestamp into a readable local timestamp."""
    if not value:
        return "Publication time unavailable"

    try:
        published_at = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if published_at.tzinfo is None:
            published_at = published_at.replace(tzinfo=timezone.utc)
        return published_at.astimezone().strftime("%Y-%m-%d %H:%M %Z")
    except ValueError:
        return "Publication time unavailable"


def fetch_headlines(category: str, api_key: str) -> list[dict[str, Any]]:
    """Fetch top headlines and raise a useful error if the API rejects the request."""
    response = requests.get(
        API_URL,
        headers={"X-Api-Key": api_key},
        params={
            "country": os.getenv("NEWS_COUNTRY", "us").strip().lower(),
            "category": category,
            "pageSize": MAX_HEADLINES,
        },
        timeout=TIMEOUT_SECONDS,
    )

    try:
        payload = response.json()
    except ValueError as error:
        response.raise_for_status()
        raise RuntimeError("NewsAPI returned a response that was not valid JSON.") from error

    if not isinstance(payload, dict):
        raise RuntimeError("NewsAPI returned an unexpected response format.")

    if not response.ok or payload.get("status") != "ok":
        error = payload.get("code", "unknownError")
        message = payload.get("message", response.reason or "Request failed.")
        if error in {"apiKeyMissing", "apiKeyInvalid", "apiKeyDisabled"}:
            raise RuntimeError("The NewsAPI key is missing, invalid, or disabled.")
        if error == "rateLimited":
            raise RuntimeError("NewsAPI's request limit has been reached. Try again later.")
        if error == "parameterInvalid":
            raise RuntimeError(f"NewsAPI rejected a request parameter: {message}")
        raise RuntimeError(f"NewsAPI error ({error}): {message}")

    articles = payload.get("articles")
    if not isinstance(articles, list):
        raise RuntimeError("NewsAPI's response did not include an articles list.")
    return articles


def print_brief(category_label: str, articles: list[dict[str, Any]]) -> None:
    """Print a concise, readable brief, omitting incomplete article records."""
    today = datetime.now().astimezone().strftime("%A, %B %d, %Y")
    print(f"\nNEWS BRIEF | {category_label.upper()} | {today}")
    print("=" * 64)

    valid_articles = [
        article for article in articles
        if isinstance(article, dict) and article.get("title")
    ]
    if not valid_articles:
        print("No headlines were returned for this category.")
        return

    for index, article in enumerate(valid_articles[:MAX_HEADLINES], start=1):
        source = article.get("source") or {}
        source_name = source.get("name") if isinstance(source, dict) else None
        description = article.get("description")
        link = article.get("url")

        print(f"\n{index}. {article['title']}")
        print(
            f"   {source_name or 'Unknown source'}"
            f" | {format_published_at(article.get('publishedAt'))}"
        )
        if description:
            print(f"   {description}")
        if link:
            print(f"   Read more: {link}")


def main() -> int:
    load_dotenv()
    api_key = os.getenv("NEWS_API_KEY", "").strip()
    if not api_key:
        print(
            "Error: NEWS_API_KEY is not set. Add your NewsAPI key to a .env file.",
            file=sys.stderr,
        )
        return 1

    selected = choose_category()
    if selected is None:
        print("Invalid choice. Please run the program again and enter 1, 2, or 3.")
        return 1

    category, label = selected
    try:
        articles = fetch_headlines(category, api_key)
    except requests.Timeout:
        print("Error: The NewsAPI request timed out. Try again.", file=sys.stderr)
        return 1
    except requests.ConnectionError:
        print("Error: Could not connect to NewsAPI. Check your internet connection.", file=sys.stderr)
        return 1
    except requests.RequestException as error:
        print(f"Error: The NewsAPI request failed: {error}", file=sys.stderr)
        return 1
    except RuntimeError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print_brief(label, articles)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())