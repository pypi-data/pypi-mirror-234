from __future__ import annotations

from typing import TYPE_CHECKING

from litestar.plugins import CLIPluginProtocol, InitPluginProtocol

from litestar_vite.config import ViteTemplateConfig
from litestar_vite.template_engine import ViteTemplateEngine

if TYPE_CHECKING:
    from click import Group
    from litestar.config.app import AppConfig

    from litestar_vite.config import ViteConfig


class VitePlugin(InitPluginProtocol, CLIPluginProtocol):
    """Vite plugin."""

    __slots__ = ("_config",)

    def __init__(self, config: ViteConfig) -> None:
        """Initialize ``Vite``.

        Args:
            config: configure and start Vite.
        """
        self._config = config

    def on_cli_init(self, cli: Group) -> None:
        from litestar_vite.cli import vite_group

        cli.add_command(vite_group)
        return super().on_cli_init(cli)

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        """Configure application for use with Vite.

        Args:
            app_config: The :class:`AppConfig <.config.app.AppConfig>` instance.
        """
        app_config.template_config = ViteTemplateConfig(  # type: ignore[assignment]
            directory=self._config.templates_dir,
            engine=ViteTemplateEngine,
            config=self._config,
        )
        return app_config
