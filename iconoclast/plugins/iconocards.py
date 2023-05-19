import logging

import semver
from importlib_metadata import version
from material.plugins.social.plugin import SocialPlugin
from mkdocs.commands.build import DuplicateFilter
from mkdocs.config.defaults import MkDocsConfig
from path import Path

from iconoclast.plugins import utils


class IconocardsPlugin(SocialPlugin):
    def on_config(self, config):
        public_deprecation = semver.Version.parse(
            "999.999.999"  # placeholder until public version gets rewritten social plugin
        )
        insiders_deprecation = semver.Version.parse("4.33.0")

        theme_version = semver.Version.parse(version("mkdocs-material"))
        public = str(theme_version.finalize_version())
        insiders = theme_version.build or "insiders.0.0.0"

        if public >= public_deprecation or insiders >= insiders_deprecation:
            log.warning(
                utils.ansify(
                    "The [magenta]iconocards[/] plugin is deprecated for your version of Material for MkDocs. "
                    "Use the built-in social plugin instead."
                )
            )

        return super().on_config(config)

    # noinspection PyUnresolvedReferences
    def _load_logo(self, config: MkDocsConfig):
        theme = config.theme
        icon = theme["icon"]["logo"]

        if icon and "logo" not in theme:
            for path in theme.dirs:
                icon_path = Path(path) / ".icons" / f"{icon}.svg"
                if icon_path.exists():
                    return self._load_logo_svg(icon_path, self.color["text"])

        return super()._load_logo(config)


log = logging.getLogger("mkdocs")
log.addFilter(DuplicateFilter())
