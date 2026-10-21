"""Authenticated WebSocket streams for logs and observability events."""

import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from WatchGuardian._internal.service.token import WatchAuth


realtime_router = APIRouter(tags=["realtime"])


async def _authorize(websocket: WebSocket) -> bool:
    token = (
        websocket.headers.get("X-user_token")
        or websocket.headers.get("Authorization", "").removeprefix("Bearer ")
        or websocket.query_params.get("token")
    )
    if not token:
        await websocket.close(code=4401, reason="Authentication required")
        return False

    try:
        payload = await WatchAuth(settings=websocket.app.state.settings).decode(token)
    except Exception:
        await websocket.close(code=4401, reason="Invalid token")
        return False

    if payload.get("type") != "user_token":
        await websocket.close(code=4401, reason="Invalid user token")
        return False

    allowed_origins = websocket.app.state.allowed_origins
    request_origin = websocket.headers.get("origin")
    if request_origin and allowed_origins and request_origin not in allowed_origins:
        await websocket.close(code=4403, reason="Origin not allowed")
        return False

    return True


async def _stream(websocket: WebSocket, event_prefix: str) -> None:
    if not await _authorize(websocket):
        return

    await websocket.accept()
    events = websocket.app.state.realtime_events

    try:
        async with events.subscribe(prefix=event_prefix) as queue:
            while True:
                event_task = asyncio.create_task(queue.get())
                receive_task = asyncio.create_task(websocket.receive_text())
                done, pending = await asyncio.wait(
                    {event_task, receive_task},
                    return_when=asyncio.FIRST_COMPLETED,
                )

                for task in pending:
                    task.cancel()
                if pending:
                    await asyncio.gather(*pending, return_exceptions=True)

                if receive_task in done and receive_task.result() == "ping":
                    await websocket.send_json({"type": "pong"})

                if event_task in done:
                    await websocket.send_json(event_task.result())
    except WebSocketDisconnect:
        return


@realtime_router.websocket("/logs/ws")
async def logs_websocket(websocket: WebSocket) -> None:
    await _stream(websocket, event_prefix="logs.")


@realtime_router.websocket("/obs/ws")
async def obs_websocket(websocket: WebSocket) -> None:
    await _stream(websocket, event_prefix="observability.")
