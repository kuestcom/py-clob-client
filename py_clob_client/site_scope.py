import re
import time
from dataclasses import dataclass
from urllib.parse import urlencode, urlparse, urlunparse

from .http_helpers.helpers import get
from .site_config import SITE_CONFIG

SITE_SCOPE_TTL_SECONDS = 5 * 60
SITE_EVENTS_LIMIT = 100
SITE_EVENTS_MAX_PAGES = 50
CONDITION_ID_PATTERN = re.compile(r"^0x[0-9a-fA-F]{64}$")
TOKEN_ID_PATTERN = re.compile(r"^(0x[0-9a-fA-F]+|\d+)$")


@dataclass
class SiteMarketScope:
    condition_ids: set[str]
    token_ids: set[str]


@dataclass
class SiteScopeCacheEntry:
    scope: SiteMarketScope
    expires_at: float


_site_scope_cache: SiteScopeCacheEntry | None = None


def has_configured_site_scope() -> bool:
    return bool(SITE_CONFIG["site_url"].strip())


def normalize_condition_id(value) -> str | None:
    if not isinstance(value, str):
        return None
    normalized = value.strip().lower()
    return normalized if CONDITION_ID_PATTERN.match(normalized) else None


def normalize_token_id(value) -> str | None:
    if not isinstance(value, (str, int)):
        return None
    normalized = str(value).strip().lower()
    return normalized if TOKEN_ID_PATTERN.match(normalized) else None


def _normalize_site_origin() -> str:
    raw = SITE_CONFIG["site_url"].strip()
    if not raw:
        raise RuntimeError(
            "site_url must be configured for site-scoped market discovery"
        )

    candidate = raw if raw.startswith(("http://", "https://")) else f"https://{raw}"
    parsed = urlparse(candidate)
    return urlunparse((parsed.scheme, parsed.netloc, "", "", "", "")).rstrip("/")


def _site_api_url(path: str, params: dict[str, str]) -> str:
    origin = _normalize_site_origin()
    return f"{origin}{path}?{urlencode(params)}"


def _empty_scope() -> SiteMarketScope:
    return SiteMarketScope(condition_ids=set(), token_ids=set())


def _add_condition_id(scope: SiteMarketScope, value) -> None:
    condition_id = normalize_condition_id(value)
    if condition_id:
        scope.condition_ids.add(condition_id)


def _add_token_id(scope: SiteMarketScope, value) -> None:
    token_id = normalize_token_id(value)
    if token_id:
        scope.token_ids.add(token_id)


def _collect_token_scope(value, scope: SiteMarketScope) -> None:
    if isinstance(value, list):
        for item in value:
            _collect_token_scope(item, scope)
        return

    if isinstance(value, dict):
        _collect_market_scope(value, scope)
        return

    _add_token_id(scope, value)


def _collect_market_scope(value, scope: SiteMarketScope) -> None:
    if isinstance(value, list):
        for item in value:
            _collect_market_scope(item, scope)
        return

    if not isinstance(value, dict):
        return

    _add_condition_id(scope, value.get("condition_id"))
    _add_condition_id(scope, value.get("conditionId"))
    _add_condition_id(scope, value.get("conditionID"))
    _add_condition_id(scope, value.get("c"))

    _add_token_id(scope, value.get("token_id"))
    _add_token_id(scope, value.get("tokenId"))
    _add_token_id(scope, value.get("asset_id"))
    _add_token_id(scope, value.get("assetId"))
    _add_token_id(scope, value.get("t"))

    for key in (
        "markets",
        "outcomes",
        "tokens",
    ):
        _collect_market_scope(value.get(key), scope)

    for key in (
        "clob_token_ids",
        "clobTokenIds",
        "outcome_assets",
        "outcomeAssets",
    ):
        _collect_token_scope(value.get(key), scope)


def get_site_market_scope() -> SiteMarketScope:
    global _site_scope_cache

    if not has_configured_site_scope():
        return _empty_scope()

    now = time.monotonic()
    if _site_scope_cache and _site_scope_cache.expires_at > now:
        return _site_scope_cache.scope

    scope = _empty_scope()
    for page in range(SITE_EVENTS_MAX_PAGES):
        events = get(
            _site_api_url(
                "/api/events",
                {
                    "status": "active",
                    "includeBookmarkState": "false",
                    "limit": str(SITE_EVENTS_LIMIT),
                    "offset": str(page * SITE_EVENTS_LIMIT),
                },
            )
        )
        if not isinstance(events, list):
            raise RuntimeError(
                "site-scoped market discovery expected /api/events to return an array"
            )

        _collect_market_scope(events, scope)
        if len(events) < SITE_EVENTS_LIMIT:
            break

    _site_scope_cache = SiteScopeCacheEntry(
        scope=scope,
        expires_at=now + SITE_SCOPE_TTL_SECONDS,
    )
    return scope


def _market_condition_id(market) -> str | None:
    if not isinstance(market, dict):
        return None
    return (
        normalize_condition_id(market.get("condition_id"))
        or normalize_condition_id(market.get("conditionId"))
        or normalize_condition_id(market.get("conditionID"))
        or normalize_condition_id(market.get("c"))
    )


def _market_has_allowed_token(market, scope: SiteMarketScope) -> bool:
    local_scope = _empty_scope()
    _collect_market_scope(market, local_scope)
    return any(token_id in scope.token_ids for token_id in local_scope.token_ids)


def filter_site_scoped_markets(markets: list, scope: SiteMarketScope) -> list:
    if not scope.condition_ids and not scope.token_ids:
        return []

    filtered = []
    for market in markets:
        condition_id = _market_condition_id(market)
        if condition_id and condition_id in scope.condition_ids:
            filtered.append(market)
        elif _market_has_allowed_token(market, scope):
            filtered.append(market)

    return filtered
