from fastapi import FastAPI, Request, HTTPException, Header
from openproject.client import Client, WorkPackages
from openproject.constants import BASE_URL


app = FastAPI()


BASE_URL = "https://samorb.openproject.com/"
client = Client(
    BASE_URL, "invalid_key"
)


@app.post("/webhook/")
async def read_webhook(request: Request):
    body = await request.json()

    object_attributes = body.get("object_attributes")

    title = object_attributes.get("title")
    description = object_attributes.get("description")

    work_package = WorkPackages(client)
    resp = work_package.create(
        subject=title,
        description={
            "format": "markdown",
            "raw": description,
        },
        _links={
            "project": {"href": "/api/v3/projects/1"},
            "type": {"href": "/api/v3/types/1"},
        },
    )

    return {"msg": "success", "data": resp}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8000, reload=True)
