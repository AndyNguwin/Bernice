import logging
import re

import httpx

logger = logging.getLogger(__name__)


def _condense_error_body(response: httpx.Response) -> str:
    content_type = response.headers.get("Content-Type", "")

    if "text/html" not in content_type:
        try:
            return str(response.json())
        except ValueError:
            return response.text[:300]

    body = response.text

    title_match = re.search(r"<title>(.*?)</title>", body, re.IGNORECASE | re.DOTALL)
    error_code_match = re.search(
        r"<span data-translate=\"error\">Error</span>\s*<span>(\d+)</span>",
        body,
        re.IGNORECASE | re.DOTALL,
    )
    heading_match = re.search(
        r"<h2[^>]*>\s*(.*?)\s*</h2>",
        body,
        re.IGNORECASE | re.DOTALL,
    )
    ip_match = re.search(
        r"<span class=\"hidden\" id=\"cf-footer-ip\">([^<]+)</span>",
        body,
        re.IGNORECASE | re.DOTALL,
    )

    parts = []
    if title_match:
        parts.append(f"title={title_match.group(1).strip()}")
    if error_code_match:
        parts.append(f"cf_error={error_code_match.group(1).strip()}")
    if heading_match:
        heading = re.sub(r"\s+", " ", heading_match.group(1)).strip()
        parts.append(f"heading={heading}")
    if ip_match:
        parts.append(f"outbound_ip={ip_match.group(1).strip()}")

    return " ".join(parts) if parts else "html_error_page"


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
            payload_summary = _condense_error_body(response)

            logger.warning(
                "Discord PATCH rate limited for interaction_id=%s interaction_name=%s status=%s body=%s retry_after=%s bucket=%s remaining=%s reset_after=%s",
                interaction_id,
                interaction_name,
                response.status_code,
                payload_summary,
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
