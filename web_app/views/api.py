from aiohttp.web import (
    Response, RouteTableDef,
    json_response, Request
)


routes = RouteTableDef()


@routes.get('/')
async def hello(request):
    return Response(text="Hello, world")


@routes.get("/data")
async def json_response_answer(request: Request):
    print(request.headers)
    print(request.method)
    return json_response({"data": "hi"})


@routes.post("/data")
async def get_data(request: Request):
    data = await request.json()
    return json_response(dict(data=data["data"]))

