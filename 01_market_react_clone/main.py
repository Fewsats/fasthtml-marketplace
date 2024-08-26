from fasthtml.common import *
from starlette.responses import PlainTextResponse, StreamingResponse

from main_layout import MainLayout
from item_details_page import ItemDetailsPage
from gallery import Gallery
from api_client import fetch_items, fetch_single_item
import httpx


# Add Flexbox Grid CSS
flexboxgrid = Link(
    rel="stylesheet",
    href=
    "https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css",
    type="text/css")


tailwind_script = Script(src="https://cdn.tailwindcss.com")

app = FastHTML(hdrs=(flexboxgrid, tailwind_script))

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
        item for item in api_items
        if query in item.title.lower() or any(query in tag.lower() for tag in item.tags)
    ]
    return Gallery(filtered_items)


@rt("/download", methods=["POST"])
async def download_file(request):
    form_data = await request.form()
    l402_url = form_data.get("url")
    credentials = form_data.get("credentials")

    if not l402_url or not credentials:
        return PlainTextResponse("Missing URL or credentials", status_code=400)

    async with httpx.AsyncClient() as client:
        response = await client.get(l402_url, headers={"Authorization": f"L402 {credentials}"})
        
        if response.status_code == 200:
            filename = response.headers.get("Content-Disposition", "").split("filename=")[-1].strip('"')
            return StreamingResponse(
                response.iter_bytes(),
                media_type="application/octet-stream",
                headers={"Content-Disposition": f'attachment; filename="{filename}"'}
            )
        else:
            return PlainTextResponse(f"Download failed: {response.text}", status_code=response.status_code)


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