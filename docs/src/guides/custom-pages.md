# Adding custom pages to App Framework FastAPI servers

If you have an App Framework project with a FastAPI backend and React frontend, you can add custom pages without much overhead. This guide shows how to add Jinja-rendered pages, HTMX interactions, or simple static content.

## How Jinja templates drive the frontend

The React frontend is served as a Jinja template through FastAPI.

Here is where that pattern shows up across the foundation templates:

| Template | Template file | Route handler |
|----------|--------------|---------------|
| Talk To My Data | `app_backend/templates/index.html` | `app_backend/app/__init__.py` |
| Agent Starter | `fastapi_server/templates/index.html` | `fastapi_server/app/__init__.py` |
| Talk to My Docs | `web/templates/index.html` | `web/app/__init__.py` |

All of these come from the same source in the App Framework component:

- **Base template:** `af-component-fastapi-backend/template/{{fastapi_app_name}}/templates/index.html`
- **Base route handler:** `af-component-fastapi-backend/template/{{fastapi_app_name}}/app/__init__.py.jinja`

The key route is a catch-all `serve_root` handler that serves the React application. Any custom routes you add must come **before** that catch-all.

## Adding your own pages

### Option 1: Add a new template route

Create a new Jinja template in your `templates/` directory and add a route to serve it, **above** the catch-all:

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

Most foundation templates organize routes into routers by concern. You can follow the same pattern and group your template renderers into a dedicated router, similar to the way the `api` routers are organized. See [`talk-to-my-docs-agents`](https://github.com/datarobot-community/talk-to-my-docs-agents) for a reference implementation:

```python
from fastapi import APIRouter

from .auth import auth_router
from .chat import chat_router

router = APIRouter(prefix="/v1")

router.include_router(chat_router)
router.include_router(auth_router)
```

### Option 2: HTMX

If you want HTMX interactivity, create your template with HTMX attributes and add the corresponding API endpoints:

```python
@router.get("/htmx-content")
async def htmx_content():
    return HTMLResponse("<div>Fresh content loaded via HTMX!</div>")
```

Your Jinja template can then trigger this endpoint:

```html
<button hx-get="/htmx-content" hx-target="#result">Load content</button>
<div id="result"></div>
```

### Option 3: Static content

The FastAPI server already serves static content from `app/static/` by default. Add your CSS, JavaScript, images, or other files there, and they are available at `/static/YOUR_FILE.ext`. No additional configuration is needed.

## Going full FastAPI

You might not need React at all. If you want faster builds, a smaller footprint, or a fully server-side-rendered application, you can remove it cleanly.

To remove React entirely:

1. Rename `infra/infra/frontend_web.py` to `infra/infra/frontend_web.py.bak`.
2. Fix the import in your FastAPI server `infra/infra/` folder.

That leaves you with a pure FastAPI application. From there, you can build any frontend you want, including HTMX, Alpine.js, vanilla JavaScript, or Jinja templates.

## The bottom line

App templates give you a full FastAPI application with all the power and flexibility that comes with it. The React frontend is one option. You can extend it, replace it, or remove it entirely. You still have Jinja templates, static file serving, and the full FastAPI ecosystem available.

Build the admin panel, HTMX-powered dashboard, or custom page set that your application needs. The framework is designed to support those choices, not constrain them.

## Starting from scratch

If you want to build something completely custom from the ground up, see the [0-Vibe guide](zero-vibe.md).
