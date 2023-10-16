import typing

import orjson
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask


class StreamingJSONResponse(StreamingResponse):
    def __init__(
        self,
        content: typing.Any,
        status_code: int = 200,
        headers: typing.Optional[typing.Mapping[str, str]] = None,
        media_type: typing.Optional[str] = "application/json",
        background: typing.Optional[BackgroundTask] = None,
    ) -> None:
        super().__init__(generate_json(content), status_code, headers, media_type, background)


async def generate_json(content: typing.Dict[str, typing.Any]):
    yield b"{"

    comma = b""
    for key, value in content.items():
        yield comma
        comma = b","
        yield b'"' + key.encode("utf-8") + b'":'

        if isinstance(value, typing.AsyncIterable):
            yield b"["

            acomma = b""
            async for item in value:
                yield acomma
                acomma = b","
                yield orjson.dumps(item)

            yield b"]"
        else:
            yield orjson.dumps(value, default=jsonable_encoder)

    yield b"}"
