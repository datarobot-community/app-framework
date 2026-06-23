# Adding custom pages to App Framework FastAPI servers

App Framework projects with a FastAPI backend and React frontend support custom pages with minimal overhead. This guide covers Jinja-rendered pages, HTMX interactions, and simple static content.

## How Jinja templates drive the frontend

The React frontend is served as a Jinja template through FastAPI.

The following table shows where that pattern appears across the foundation templates:

| Template | Template file | Route handler |
|----------|--------------|---------------|
| Talk To My Data | `app_backend/templates/index.html` | `app_backend/app/__init__.py` |
| Agent Starter | `fastapi_server/templates/index.html` | `fastapi_server/app/__init__.py` |
| Talk to My Docs | `web/templates/index.html` | `web/app/__init__.py` |

All of these come from the same source in the App Framework component:

- **Base template:** `af-component-fastapi-backend/template/{{fastapi_app_name}}/templates/index.html`
- **Base route handler:** `af-component-fastapi-backend/template/{{fastapi_app_name}}/app/__init__.py.jinja`

The key route is a catch-all `serve_root` handler that serves the React application. Add any custom routes **before** that catch-all.

## Adding custom pages

### Option 1: Add a template route

Create a Jinja template in the `templates/` directory and add a route to serve it **above** the catch-all:

```python
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/my-custom-page", response_class=HTMLResponse)
async def custom_page(request: Request):
    return templates.TemplateResponse("my_custom_page.html", {"request": request})

# This route must come BEFORE the catch-all route that serves React.
```

Most foundation templates organize routes into routers by concern. Follow the same pattern and group template renderers into a dedicated router, similar to the `api` routers. See [`talk-to-my-docs-agents`](https://github.com/datarobot-community/talk-to-my-docs-agents) for a reference implementation:

```python
from fastapi import APIRouter

from .auth import auth_router
from .chat import chat_router

router = APIRouter(prefix="/v1")

router.include_router(chat_router)
router.include_router(auth_router)
```

### Option 2: HTMX

For HTMX interactivity, create a template with HTMX attributes and add the corresponding API endpoints:

```python
@router.get("/htmx-content")
async def htmx_content():
    return HTMLResponse("<div>Fresh content loaded via HTMX!</div>")
```

The Jinja template can then trigger this endpoint:

```html
<button hx-get="/htmx-content" hx-target="#result">Load content</button>
<div id="result"></div>
```

### Option 3: Static content

The FastAPI server serves static content from `app/static/` by default. Add CSS, JavaScript, images, or other files there; they are available at `/static/YOUR_FILE.ext`. No additional configuration is required.

## Going full FastAPI

React is optional. For faster builds, a smaller footprint, or a fully server-side-rendered application, remove it cleanly.

To remove React entirely:

1. Rename `infra/infra/frontend_web.py` to `infra/infra/frontend_web.py.bak`.
2. Fix the import in the FastAPI server `infra/infra/` folder.

The result is a pure FastAPI application. From there, build any frontend, including HTMX, Alpine.js, vanilla JavaScript, or Jinja templates.

## Summary

App templates provide a full FastAPI application with the power and flexibility of the FastAPI ecosystem. The React frontend is one option — extend it, replace it, or remove it entirely. Jinja templates, static file serving, and the full FastAPI ecosystem remain available.

Build the admin panel, HTMX-powered dashboard, or custom page set the application requires. The framework supports those choices rather than constraining them.

## Starting from scratch

To build something completely custom from the ground up, see the [0-Vibe guide](zero-vibe.md).
