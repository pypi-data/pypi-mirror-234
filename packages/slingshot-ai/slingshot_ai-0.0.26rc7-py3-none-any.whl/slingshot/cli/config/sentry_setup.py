from __future__ import annotations

from logging import getLogger

import sentry_sdk
import typer
from sentry_sdk.integrations.asyncio import AsyncioIntegration

from slingshot.sdk.config import global_config
from slingshot.sdk.errors import SlingshotException
from slingshot.slingshot_version import __version__

logger = getLogger(__name__)


def sentry_init() -> None:
    dsn: str | None = "https://8a6bd4ec961f4e93adf09164a5318b14@o4504169163718656.ingest.sentry.io/4505331795492864"

    if 'site-packages' not in __file__:
        logger.debug('Disabling Sentry reporting as running from source')
        dsn = None
    elif global_config.slingshot_backend_url == global_config.slingshot_local_url:
        logger.debug('Disabling Sentry reporting as running against local backend')
        dsn = None

    # No local here as we exclude Sentry altogether
    environment = "prod" if global_config.slingshot_backend_url == global_config.slingshot_prod_url else "dev"
    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        traces_sample_rate=0.1,
        ignore_errors=[typer.Abort, typer.Exit, SlingshotException],
        integrations=[AsyncioIntegration()],
        auto_enabling_integrations=False,
    )
    sentry_sdk.set_tag("slingshot_version", __version__)
    sentry_sdk.set_tag("environment", environment)
