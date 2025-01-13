from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
from socketio import AsyncServer, ASGIApp  # Note the explicit imports

# Create FastAPI app
app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Socket.IO instance
sio = AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    logger=True
)

# Create the ASGI application
socket_app = ASGIApp(
    socketio_server=sio,
    other_asgi_app=app,
    socketio_path='/'
)

# Socket.IO event handlers
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
async def heart_rate(sid, data, callback=None):
    print(f"Received heart rate data: {data}")
    response = {
        'status': 'received',
        'data': data
    }
    if callback:
        callback(response)
    await sio.emit('heart_rate_response', response, room=sid)
# Service URLs
services = {
    'data-ingestion': 'http://localhost:5001',
    'real-time-monitoring': 'http://localhost:5002',
    'historical-analysis': 'http://localhost:5003',
    'alert-service': 'http://localhost:5004'
}

# Proxy requests to the appropriate service
@app.api_route('/api/{service}/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def proxy(service: str, path: str, request: Request):
    if service not in services:
        return {"error": "Service not found"}, 404

    url = f"{services[service]}/{path}"
    method = request.method
    headers = {key: value for key, value in request.headers.items() if key != 'host'}
    data = await request.body()

    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            cookies=request.cookies,
            allow_redirects=False
        )
        return response.content, response.status_code, dict(response.headers)
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(socket_app, host='0.0.0.0', port=3001)