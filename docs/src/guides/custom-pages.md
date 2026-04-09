# Adding custom pages to App Template FastAPI servers

So you've got an App Template running with a FastAPI backend and React frontend, and now you want to add some custom pages? Maybe throw in some HTMX magic, or serve up a simple HTML page without all that React overhead? You're in the right place.

## The secret sauce: it's all Jinja templates

That fancy React app you're looking at? It's actually being served as a Jinja template through FastAPI.

Here's where the magic happens across the Foundation Templates:

| Template | Template file | Route handler |
|----------|--------------|---------------|
| Talk To My Data | `app_backend/templates/index.html` | `app_backend/app/__init__.py` |
| Agent Starter | `fastapi_server/templates/index.html` | `fastapi_server/app/__init__.py` |
| Talk to My Docs | `web/templates/index.html` | `web/app/__init__.py` |

All of these come from the same source in the App Framework component:

- **Base template:** `af-component-fastapi-backend/template/{{fastapi_app_name}}/templates/index.html`
- **Base route handler:** `af-component-fastapi-backend/template/{{fastapi_app_name}}/app/__init__.py.jinja`

The key route is a catch-all `serve_root` that serves the React app. Any custom routes you add need to come **before** that catch-all.

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

Most Foundation Templates organize routes into routers by concern. You can follow the same pattern and group your template renderers into a dedicated router, similar to how the `api` routers are organized. See [`talk-to-my-docs-agents`](https://github.com/datarobot-community/talk-to-my-docs-agents) for a reference implementation:

```python
from fastapi import APIRouter

from .auth import auth_router
from .chat import chat_router

router = APIRouter(prefix="/v1")

router.include_router(chat_router)
router.include_router(auth_router)
```

### Option 2: HTMX

Want HTMX interactivity? Create your template with HTMX attributes and add the corresponding API endpoints:

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

The FastAPI server already serves static content from `app/static/` by default. Drop your CSS, JavaScript, images, or other files in there and they'll be available at `/static/your-file.ext`. No additional configuration needed.

## Going full FastAPI (ditching React)

Maybe you don't need React at all — you want faster builds, a smaller footprint, or you're going server-side-rendered all the way down.

Here's how to remove React entirely:

1. Rename `infra/infra/frontend_web.py` to `infra/infra/frontend_web.py.bak`.
2. Fix the import in your FastAPI server `infra/infra/` folder.

That's it. Now you have a pure FastAPI app. Build whatever frontend you want: HTMX, Alpine.js, vanilla JavaScript, or Jinja templates all the way down.

## The bottom line

The App Templates give you a full FastAPI application with all the power and flexibility that comes with it. The React frontend is just one option — you can add to it, replace it, or remove it entirely. You've got Jinja templates, static file serving, and the entire FastAPI ecosystem at your fingertips.

Add that admin panel, create that HTMX-powered dashboard, or serve up whatever custom pages you need. The framework is here to support you, not constrain you.

## Starting from scratch

If you want to build something completely custom from the ground up, see the [0-Vibe guide](zero-vibe.md).
