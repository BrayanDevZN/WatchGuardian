from watch.main import app 
import asyncio
asyncio.run(app.load_module())
client = app.client_http
print(asyncio.run(client.health()))