from fastapi import FastAPI
from app.core.database import engine, Base
from app.api import auth_routes, organization_routes
from app.models import user, organization, membership, project
from app.api import project_routes
from app.models import issue
from app.api import issue_routes
from app.models import activity_log
from app.models import comment
from app.api import comment_routes
from app.models import tag

app = FastAPI(title="Issue Tracker API")

Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)
app.include_router(project_routes.router)
app.include_router(organization_routes.router)
app.include_router(issue_routes.router)
app.include_router(comment_routes.router)

@app.get("/")
def root():
    return {"message": "API Working Successfully"}