from typing import Dict, List
from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        print(f"WebSocket connected for user {user_id}.")

    def disconnect(self, user_id: int, websocket: WebSocket):
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        print(f"WebSocket disconnected for user {user_id}.")

    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            dead_sockets = []
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    print(f"Failed to send WS message to user {user_id}: {e}")
                    dead_sockets.append(connection)
            for connection in dead_sockets:
                self.disconnect(user_id, connection)

    async def broadcast(self, message: dict):
        for user_id, connections in list(self.active_connections.items()):
            dead_sockets = []
            for connection in connections:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    print(f"Failed to broadcast WS message to user {user_id}: {e}")
                    dead_sockets.append(connection)
            for connection in dead_sockets:
                self.disconnect(user_id, connection)


manager = ConnectionManager()
