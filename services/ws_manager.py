from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):
        self.activas = []

    async def conectar(self, websocket: WebSocket):
        await websocket.accept()
        self.activas.append(websocket)

    def desconectar(self, websocket: WebSocket):
        if websocket in self.activas:
            self.activas.remove(websocket)

    async def broadcast(self, datos: dict):
        caidas = []

        for websocket in self.activas:
            try:
                await websocket.send_json(datos)
            except Exception:
                caidas.append(websocket)

        for websocket in caidas:
            self.desconectar(websocket)


manager = ConnectionManager()
