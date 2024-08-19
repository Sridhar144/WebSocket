import asyncio
import os
from channels.generic.websocket import AsyncWebsocketConsumer

class LogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.logfile_path = 'logviewer/example.log'
        await self.accept()

        # Send the last 10 lines when a client connects
        self.logfile = open(self.logfile_path, 'rb')
        self.logfile.seek(0, os.SEEK_END)
        file_size = self.logfile.tell()
        buffer_size = 1024
        buffer = bytearray()
        last_lines = []

        while file_size > 0 and len(last_lines) < 10:
            file_size -= buffer_size
            if file_size < 0:
                file_size = 0
            self.logfile.seek(file_size)
            buffer = self.logfile.read(buffer_size) + buffer
            last_lines = buffer.splitlines()[-10:]

        for line in last_lines:
            await self.send(text_data=line.decode('utf-8'))

        # Stream updates
        while True:
            line = self.logfile.readline()
            if line:
                await self.send(text_data=line.decode('utf-8'))
            else:
                await asyncio.sleep(0.1)

    async def disconnect(self, close_code):
        self.logfile.close()
