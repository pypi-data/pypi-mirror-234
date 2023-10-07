import asyncio
import json

import websockets

from .config import get_store_reader

get_env = get_store_reader()

def ws_send_and_receive(server=None, ignore_list=None, data=None):

    log_type = "[WebSockets]"
    wait_ms = int(get_env('WEBSOCKETS_WAIT_MS'))

    async def receive_async():
        async with websockets.connect(server) as websocket:
            received = False
            while not received:
                received_data = await websocket.recv()
                if received_data in ignore_list:
                    print(f"Ignoring received message <{received_data}>")
                else:
                    received = True
        return received_data

    async def receive_async_with_timeout():
        seconds = wait_ms / 1000
        received_data = await asyncio.wait_for(
            receive_async(),
            seconds
        )
        print(f"{log_type} Received <{received_data}>")
        return received_data

    def start_receiving():
        print(f"{log_type} Waiting {wait_ms} ms for packets from {server}")
        return asyncio.ensure_future(receive_async_with_timeout())

    def end_receiving(a_handle):
        received_data = asyncio.get_event_loop().run_until_complete(a_handle)
        print(f"{log_type} Finished waiting for packets from {server}, received {received_data}")
        return json.loads(received_data)

    async def send_async(data_to_send):
        async with websockets.connect(server) as websocket:
            await websocket.send(data_to_send)
            print(f"Sent <{data_to_send}>")

    def send_sync(data_to_send):
        asyncio.get_event_loop().run_until_complete(send_async(data_to_send))

    handle = start_receiving()
    to_send = json.dumps(data)
    send_sync(to_send)
    return end_receiving(handle)
