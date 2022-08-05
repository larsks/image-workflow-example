import os

import markdown

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

def filter_markdown(text):
    return markdown.markdown(text)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
templates.env.filters['markdown'] = filter_markdown

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    environment = {k: v for k, v in os.environ.items() if k.startswith("KUBE_")}
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "environment": environment,
        },
    )
