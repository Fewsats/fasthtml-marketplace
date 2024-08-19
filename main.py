from fasthtml.common import *
import os
import uuid
from starlette.responses import RedirectResponse, PlainTextResponse, Response
from starlette.middleware.cors import CORSMiddleware
from l402.server import Authenticator, FastHTML_l402_decorator

from main_layout import MainLayout
from item_details_page import ItemDetailsPage
from item_card import ItemCard
from gallery import Gallery
from api_client import fetch_items, map_api_item_to_item, fetch_single_item
import httpx



# Add Flexbox Grid CSS
flexboxgrid = Link(
    rel="stylesheet",
    href=
    "https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css",
    type="text/css")

# Add Tailwind CSS from CDN
# tailwind = Link(
#     rel="stylesheet",
#     href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css",
#     type="text/css")

tailwind_script = Script(src="https://cdn.tailwindcss.com")

app = FastHTML(hdrs=(flexboxgrid, tailwind_script))
# app = FastHTML(hdrs=(picolink, flexboxgrid, tailwind))

# Update CORS middleware to expose all headers for L402
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

rt = app.route



@rt("/", methods=["GET"])
async def get(request):
    api_items = await fetch_items()
    return MainLayout(title="Files Catalog", items=api_items)

@rt("/search", methods=["GET"])
async def search(request):
    query = request.query_params.get("search", "").lower()
    api_items = await fetch_items()
    filtered_items = [
        map_api_item_to_item(item) for item in api_items
        if query in item["name"].lower() or any(query in tag.lower() for tag in item["tags"])
    ]
    return Gallery(filtered_items)


@rt("/download/{id:str}", methods=["GET"])
async def download_file(req, id: str):
    api_items = await fetch_items()
    item = next((item for item in api_items if item["external_id"] == id), None)
    if not item:
        return PlainTextResponse("File not found", status_code=404)
    return RedirectResponse(url=item["l402_url"])


@rt("/file/{id:str}", methods=["GET"])
async def get_item_details(request, id: str):
    try:
        item = await fetch_single_item(id)
        return ItemDetailsPage(item)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return PlainTextResponse("Item not found", status_code=404)
        else:
            return PlainTextResponse("An error occurred", status_code=500)


serve()
