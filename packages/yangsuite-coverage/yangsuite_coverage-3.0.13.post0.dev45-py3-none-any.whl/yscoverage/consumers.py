from channels.generic.websocket import AsyncJsonWebsocketConsumer


class DataSetInfoConsumer(AsyncJsonWebsocketConsumer):
    """Pass async messages to the websocket client."""
    async def connect(self, *args):
        self.group_name = str(hash(str(self.scope["user"]) + 'datasetinfo'))
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def dataset_state_update(self, event):
        await self.send_json(event['message'])

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
