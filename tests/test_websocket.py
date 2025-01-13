# import pytest
# import asyncio
# import socketio
#
# @pytest.mark.asyncio
# async def test_heart_rate_websocket():
#     sio = socketio.AsyncClient(logger=True)
#     connected = False
#     received_response = False
#     received_data = None
#
#     @sio.event
#     async def connect():
#         nonlocal connected
#         connected = True
#         print("Connected!")
#
#     @sio.event
#     async def disconnect():
#         nonlocal connected
#         connected = False
#         print("Disconnected!")
#
#     @sio.on('heart_rate_response')
#     async def on_response(data):
#         nonlocal received_response, received_data
#         received_response = True
#         received_data = data
#         print(f"Received response: {data}")
#
#     try:
#         # Connect to the server
#         await sio.connect('http://localhost:3001')
#         assert connected, "Failed to connect to server"
#
#         # Send heart rate data
#         heart_rate_data = {"heart_rate": 75}
#
#         # Wait for both the emit response and the event response
#         await sio.emit('heart_rate', heart_rate_data)
#
#         # Wait a bit for the response to come back
#         await asyncio.sleep(1)
#
#         # Check if we received the response via event
#         assert received_response, "No event response received"
#         assert received_data is not None, "No data in event response"
#         assert received_data['status'] == 'received', "Incorrect response status"
#         assert 'data' in received_data, "Response missing data field"
#         assert received_data['data']['heart_rate'] == 75, "Heart rate data mismatch"
#
#     finally:
#         # Cleanup
#         if sio.connected:
#             await sio.disconnect()
#
# if __name__ == "__main__":
#     pytest.main([__file__])


import pytest
import asyncio
import socketio

@pytest.mark.asyncio
async def test_heart_rate_websocket():
    sio = socketio.AsyncClient(logger=True)
    connected = False
    received_response = False
    received_data = None

    @sio.event
    async def connect():
        nonlocal connected
        connected = True
        print("Connected!")

    @sio.event
    async def disconnect():
        nonlocal connected
        connected = False
        print("Disconnected!")

    @sio.on('heart_rate_response')
    async def on_response(data):
        nonlocal received_response, received_data
        received_response = True
        received_data = data
        print(f"Received response: {data}")

    try:
        # Connect to the server
        await sio.connect('http://localhost:3001')
        assert connected, "Failed to connect to server"

        # Send heart rate data
        heart_rate_data = {"heart_rate": 75}
        await sio.emit('heart_rate', heart_rate_data)

        # Wait a bit for the response to come back
        await asyncio.sleep(1)

        # Check if we received the response via event
        assert received_response, "No event response received"
        assert received_data is not None, "No data in event response"
        assert received_data['status'] == 'received', "Incorrect response status"
        assert 'data' in received_data, "Response missing data field"
        assert received_data['data']['heart_rate'] == 75, "Heart rate data mismatch"

        # Wait for one minute before disconnecting
        print("Waiting for 60 seconds before disconnecting...")
        await asyncio.sleep(60)
        print("One minute has passed, disconnecting now...")

    finally:
        # Cleanup
        if sio.connected:
            await sio.disconnect()
            print("Socket disconnected")

if __name__ == "__main__":
    pytest.main([__file__])