from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .models import Desk


class WaitingConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        desks = await database_sync_to_async(self.get_desks)(user)

        for desk in desks:
            await self.channel_layer.group_add(
                desk.code,
                self.channel_name
            )
        await self.accept()


    def get_desks(self, user):
        return list(Desk.objects.filter(waiter=user))

    async  def request_waiter(self, event):
        await self.send_json({'code':event['code']})