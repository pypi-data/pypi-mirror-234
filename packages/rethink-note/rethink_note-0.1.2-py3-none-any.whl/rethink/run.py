import os
from typing import Literal

import uvicorn


def run(
        host="127.0.0.1",
        port=8000,
        reload=False,
        language: Literal["en", "zh"] = "en",
        workers=1,
):
    os.environ["VUE_APP_API_PORT"] = str(port)
    os.environ["VUE_APP_MODE"] = "local"
    os.environ["VUE_APP_LANGUAGE"] = language
    uvicorn.run(
        "rethink.application:app",
        host=host,
        port=port,
        reload=reload,
        workers=workers,
        env_file=os.path.join(os.path.abspath(os.path.dirname(__file__)), ".env.local"),
    )
