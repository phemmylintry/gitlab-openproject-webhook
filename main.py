from fastapi import FastAPI, Request
from openproject.client import Client
from openproject.constants import BASE_URL
import gitlab


app = FastAPI()

# open project onfig
client = Client(BASE_URL, "api-token")

# gitlab client config
gl = gitlab.Gitlab(private_token="api-token")


@app.post("/gitlab/webhook/")
async def gitlab_read_webhook(request: Request):
    body = await request.json()

    object_attributes = body.get("object_attributes")

    title = object_attributes.get("title")
    description = object_attributes.get("description")
    # fetch work package with id 20
    work = client.work_packages.view(id=20)
    resp = client.work_packages.update(
        id=20,
        subject=title,
        description={
            "format": "markdown",
            "raw": description,
        },
        _links={
            "project": {"href": "/api/v3/projects/1"},
            "type": {"href": "/api/v3/types/1"},
        },
        lockVersion=work["lockVersion"],
    )
    return {"msg": "success", "data": resp}


@app.post("/openproject/webhook/")
async def openproject_read_webhook(request: Request):
    body = await request.json()

    work_package = body.get("work_package")
    title = work_package.get("subject")
    description = work_package.get("description").get("raw") 

    print("Title", title)
    print("Description", description)

    # make request to gitlab
    project_id = 50914086
    project = gl.projects.get(project_id, lazy=True)
    
    editable_issue = project.issues.list()[0]

    editable_issue.title = "title"
    editable_issue.description = "description"
    resp = editable_issue.save()

    return {"msg": "success", "data": resp}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8000, reload=True)
