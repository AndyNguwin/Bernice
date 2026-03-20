import asyncio
import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

DISCORD_API_BASE_URL = "https://discord.com/api/v10"
MAX_RETRY_ATTEMPTS = 3
DEFAULT_RETRY_AFTER_SECONDS = 1.0


def _parse_retry_after(response: httpx.Response) -> float:
    try:
        payload = response.json()
    except ValueError:
        payload = {}

    retry_after = payload.get("retry_after")
    if retry_after is not None:
        try:
            return max(float(retry_after), 0.0)
        except (TypeError, ValueError):
            pass

    header_retry_after = response.headers.get("Retry-After")
    if header_retry_after is not None:
        try:
            return max(float(header_retry_after), 0.0)
        except (TypeError, ValueError):
            pass

    reset_after = response.headers.get("X-RateLimit-Reset-After")
    if reset_after is not None:
        try:
            return max(float(reset_after), 0.0)
        except (TypeError, ValueError):
            pass

    return DEFAULT_RETRY_AFTER_SECONDS


async def _patch_with_rate_limit_retry(
    client: httpx.AsyncClient,
    url: str,
    content: dict[str, Any],
) -> httpx.Response:
    for attempt in range(1, MAX_RETRY_ATTEMPTS + 1):
        response = await client.patch(url, json=content)

        if response.status_code != 429:
            response.raise_for_status()
            return response

        retry_after = _parse_retry_after(response)
        is_last_attempt = attempt == MAX_RETRY_ATTEMPTS

        logger.warning(
            "Discord webhook edit rate limited (attempt %s/%s). Retrying in %.2fs.",
            attempt,
            MAX_RETRY_ATTEMPTS,
            retry_after,
        )

        if is_last_attempt:
            response.raise_for_status()

        await asyncio.sleep(retry_after)

    raise RuntimeError("Unreachable: Discord webhook retry loop exhausted.")


async def edit_deferred_message(
    application_id: str,
    interaction_token: str,
    content: dict[str, Any],
) -> None:
    url = (
        f"{DISCORD_API_BASE_URL}/webhooks/"
        f"{application_id}/{interaction_token}/messages/@original"
    )

    try:
        async with httpx.AsyncClient() as client:
            await _patch_with_rate_limit_retry(client, url, content)
    except httpx.HTTPStatusError:
        logger.exception("Failed to edit deferred Discord message after retries.")
