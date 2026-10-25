# News Brief Generator

A small command-line Python app that fetches up to five top headlines from
NewsAPI and prints them as a readable brief. Choose Technology, Business, or
Health when prompted.

## Requirements

- Python 3.10 or later
- A NewsAPI account and API key: <https://newsapi.org/register>
- The `requests` and `python-dotenv` packages

NewsAPI's free Developer plan is for development and testing only, not
production use. Its availability, quotas, and freshness limits are determined
by NewsAPI and may change. Headlines and publication times come from the API;
the brief heading shows today's local date, but the free plan may not provide
articles published today.

## Setup

Open PowerShell in the project folder and install the required packages:

```powershell
python -m pip install requests python-dotenv
```

Create a `.env` file in the same folder as `News Generator Api.py` and add
your key:

```text
NEWS_API_KEY=your_newsapi_key_here
```

Do not share or commit your API key. The project's `.gitignore` should exclude
`.env`.

Optional: set a country code for the headlines (defaults to `us`):

```text
NEWS_COUNTRY=us
```

NewsAPI's country support depends on the account/plan and its currently
supported country codes.

## Run

```powershell
python ".\News Generator Api.py"
```

Choose `1` for Technology, `2` for Business, or `3` for Health. The brief
shows the headline, source, publication time in your local timezone, a short
description when available, and a link to the article.

## Error handling

The program reports a clear message for a missing/invalid API key, API errors
and rate limits, timeouts, connection failures, invalid API responses, and an
invalid category choice. It exits with a non-zero status when it cannot fetch
headlines.
