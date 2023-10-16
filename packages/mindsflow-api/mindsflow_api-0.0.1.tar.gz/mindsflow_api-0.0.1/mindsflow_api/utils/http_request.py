import httpx


async def get_request(url, params=None, headers=None) -> httpx.Response:
    async with httpx.AsyncClient(timeout=3600) as client:
        response = await client.get(url, headers=headers, params=params)
    await client.aclose()
    return response


async def post_request(url, data=None, json=None, headers=None) -> httpx.Response:
    async with httpx.AsyncClient(timeout=3600) as client:
        response = await client.post(url, data=data, json=json, headers=headers)
    await client.aclose()
    return response


async def put_request(url, data=None, json=None, headers=None) -> httpx.Response:
    async with httpx.AsyncClient(timeout=3600) as client:
        response = await client.put(url, data=data, json=json, headers=headers)
    await client.aclose()
    return response


async def patch_request(url, data=None, json=None, headers=None) -> httpx.Response:
    async with httpx.AsyncClient(timeout=3600) as client:
        response = await client.patch(url, data=data, json=json, headers=headers)
    await client.aclose()
    return response


async def delete_request(url, params, headers=None) -> httpx.Response:
    async with httpx.AsyncClient(timeout=3600) as client:
        response = await client.delete(url, params=params, headers=headers)
    await client.aclose()
    return response
