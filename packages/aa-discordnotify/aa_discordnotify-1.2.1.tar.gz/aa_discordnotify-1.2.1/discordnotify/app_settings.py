"""Settings for Discord Notify."""

from django.conf import settings

DISCORDNOTIFY_DISCORDPROXY_PORT = getattr(
    settings, "DISCORDNOTIFY_DISCORDPROXY_PORT", 50051
)
"""Port used to communicate with Discord Proxy."""

DISCORDNOTIFY_SUPERUSER_ONLY = getattr(settings, "DISCORDNOTIFY_SUPERUSER_ONLY", False)
"""When set to True, only superusers will be get their notifications forwarded."""


DISCORDNOTIFY_ENABLED = getattr(settings, "DISCORDNOTIFY_ENABLED", True)
"""Set this to False to disable this app temporarily."""

DISCORDNOTIFY_MARK_AS_VIEWED = getattr(settings, "DISCORDNOTIFY_MARK_AS_VIEWED", False)
"""When set True will mark all notifications as read
that have been successfully submitted to Discord.
"""
