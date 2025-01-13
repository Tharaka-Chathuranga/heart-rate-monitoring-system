from fastapi import FastAPI, Request
import requests

app = FastAPI()

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

    response = requests.request(
        method=method,
        url=url,
        headers=headers,
        data=data,
        cookies=request.cookies,
        allow_redirects=False
    )

    return response.content, response.status_code, response.headers.items()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=3000)