from typing import Optional, Dict, Any

import uvicorn
from fastapi import FastAPI
from starlette.testclient import TestClient as StarletteTestClient

import easy_pysy as ez

fast_api = FastAPI()

websocket = fast_api.websocket
get = fast_api.get
put = fast_api.put
post = fast_api.post
delete = fast_api.delete
options = fast_api.options
head = fast_api.head
patch = fast_api.patch
trace = fast_api.trace


@fast_api.on_event("shutdown")
def shutdown_event():
    ez.stop()


@ez.command(name='start-api')
def start_api(host: str = '0.0.0.0', port: int = 5000):
    uvicorn.run(fast_api, host=host, port=port)


class TestClient(StarletteTestClient):
    def __init__(
            self,
            base_url: str = "http://testserver",
            raise_server_exceptions: bool = True,
            root_path: str = "",
            backend: str = "asyncio",
            backend_options: Optional[Dict[str, Any]] = None):
        super().__init__(
            fast_api,
            base_url=base_url,
            raise_server_exceptions=raise_server_exceptions,
            root_path=root_path,
            backend=backend,
            backend_options=backend_options,
        )
