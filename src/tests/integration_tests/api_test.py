from httpx import AsyncClient


async def test_get_logs(ac: AsyncClient):
    response = await ac.get("/logs")
    assert response.status_code == 200
