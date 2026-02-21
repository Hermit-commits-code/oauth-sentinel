import pytest
from httpx import ASGITransport, AsyncClient

from oauth_sentinel.main import app


# This decorator tells Pytest that the following function is an asynchronous coroutine.
# Without this, Pytest will try to run the test like a normal function and immediately
# crash because it doesn't know how to handle await.
@pytest.mark.asyncio
# verifying that when someone hits the /canary/callback URL, the server is alive and
# responds with a success code.
async def test_canary_callback_returns_200():
    # create a virtual client, point it at my app, and simulate a GET request to the
    # tripwire. This happens entirely in memory—no actual network ports are used, which
    # makes the tests lightning fast.
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/canary/callback")
        # "assert" (demand) that the status code is 200 and the JSON message matches
        # exactly what I wrote in main.py
        assert response.status_code == 200
        assert response.json() == {
            "status": "authorized",
            "message": "Security Audit Logged",
        }
