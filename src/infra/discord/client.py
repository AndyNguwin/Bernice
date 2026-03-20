import logging

import httpx

logger = logging.getLogger(__name__)


async def edit_deferred_message(
    application_id: str,
    interaction_token: str,
    content,
    interaction_id: str | None = None,
    interaction_name: str | None = None,
) -> None:
    url = f"https://discord.com/api/v10/webhooks/{application_id}/{interaction_token}/messages/@original"

    logger.info(
        "Editing deferred Discord message for interaction_id=%s interaction_name=%s application_id=%s",
        interaction_id,
        interaction_name,
        application_id,
    )

    async with httpx.AsyncClient() as client:
        response = await client.patch(url, json=content)

        if response.status_code == 429:
            try:
                payload = response.json()
            except ValueError:
                payload = response.text

            logger.warning(
                "Discord PATCH rate limited for interaction_id=%s interaction_name=%s status=%s body=%s retry_after=%s bucket=%s remaining=%s reset_after=%s",
                interaction_id,
                interaction_name,
                response.status_code,
                payload,
                response.headers.get("Retry-After"),
                response.headers.get("X-RateLimit-Bucket"),
                response.headers.get("X-RateLimit-Remaining"),
                response.headers.get("X-RateLimit-Reset-After"),
            )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError:
            logger.exception(
                "Discord PATCH failed for interaction_id=%s interaction_name=%s content_type=%s server=%s cf_ray=%s",
                interaction_id,
                interaction_name,
                response.headers.get("Content-Type"),
                response.headers.get("Server"),
                response.headers.get("CF-RAY"),
            )
