from accentnotifications.notifications.base import BaseNotification


class NotificationManager:
    async def send(self, options: BaseNotification):
        async with options.backend(options) as backend:
            return await backend.send()
