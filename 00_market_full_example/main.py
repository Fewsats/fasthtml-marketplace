from fasthtml.common import *
import os
import uuid
from starlette.responses import RedirectResponse, PlainTextResponse, Response
from starlette.middleware.cors import CORSMiddleware
from l402.server import Authenticator, FastHTML_l402_decorator
from l402.server.invoice_provider import FewsatsInvoiceProvider
from l402.server.macaroons import SqliteMacaroonService
from storage import get_storage
from main_layout import MainLayout
from item_details_page import ItemDetailsPage
from item_card import ItemCard
from gallery import Gallery
from search_bar import SearchBar
from upload_form import UploadForm

# Database configuration
db = database('data/market.db')


# Initialize database
@dataclass
class Item:
    id: int
    title: str
    description: str
    price: int
    cover_image: str
    file_path: str
    tags: str = ""


@patch
def __ft__(self: Item):
    return ItemCard(self)


items = db.create(Item, pk='id')

# Set up Fewsats invoice provider
# 1. Sign up at app.fewsats.com
# 2. Create API Key
# 3a. Export env variable FEWSATS_API_KEY=fs_...
# or
# 3b. Pass the api key to the provider FewsatsInvoiceProvider(api_key="fs_...")
api_key = os.environ.get("FEWSATS_API_KEY")
fewsats_provider = FewsatsInvoiceProvider(api_key=api_key)

# Set up MacaroonService for storing authentication tokens
macaroon_service = SqliteMacaroonService('data/credentials.db')

# Initialize the L402 Authenticator
authenticator = Authenticator(location='localh8000',
                              invoice_provider=fewsats_provider,
                              macaroon_service=macaroon_service)

# Initialize the storage to handle file uploads
storage = get_storage()

# Add Flexbox Grid CSS
flexboxgrid = Link(
    rel="stylesheet",
    href=
    "https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css",
    type="text/css")


tailwind_script = Script(src="https://cdn.tailwindcss.com")

app = FastHTML(hdrs=(flexboxgrid, tailwind_script))

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


@rt("/files/{fname:path}", methods=["GET"])
async def get(fname: str):
    file_content = storage.download(fname)
    if file_content is None:
        return PlainTextResponse("File not found", status_code=404)
    return Response(content=file_content)


def mk_form(**kw):
    input_fields = Fieldset(
        Label(
            "Title",
            Input(id="new-title",
                  name="title",
                  placeholder="Heart of Gold",
                  required=True,
                  **kw)),
        Label(
            "Description",
            Input(id="new-description",
                  name="description",
                  placeholder="3D Model of the spaceship Heart of Gold",
                  required=True,
                  **kw)),
        Label(
            "Price",
            Input(id="new-price",
                  name="price",
                  placeholder="Price ($)",
                  type="number",
                  required=True,
                  **kw)),
        Group(
            Label(
                "Cover Image",
                Input(id="new-cover-image",
                      name="cover_image",
                      type="file",
                      required=True,
                      **kw)),
            Label(
                "Item File",
                Input(id="new-file",
                      name="file",
                      type="file",
                      required=True,
                      **kw))))
    return Form(Group(input_fields),
                Button("Upload"),
                hx_post="/",
                hx_target="#item-list",
                hx_swap="afterbegin",
                enctype="multipart/form-data")



@rt("/upload")
async def get_upload_page(request):
    upload_content = Div(id='upload-form', cls='relative mx-auto -mt-60 w-full max-w-screen-1xl px-4 pb-7 md:px-14')(
        Div(cls='w-full rounded-lg border border-gray-200 bg-white px-4 py-8 md:px-8 md:py-12')(
            Div(cls='max-w-md mx-auto')(
                UploadForm(),
                Div(id="upload-result", cls="mt-4")
            )
        )
    )
    return MainLayout(title="Upload File", content=upload_content)

# Modify the existing POST handler to return a success message
@rt("/")
async def post(request):
    form = await request.form()

    item_data = {
        'title': form.get('title'),
        'description': form.get('description'),
        'price': form.get('price'),
    }

    for field in ['cover_image', 'file_path']:
        if file := form.get(field):
            content = await file.read()
            filename = f"{field}_{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
            storage.upload(filename, content)
            item_data[field] = filename

    new_item = items.insert(Item(**item_data))
    return Div(cls="bg-green-100 border-l-4 border-green-500 text-green-700 p-4", role="alert")(
        P(cls="font-bold")("Success!"),
        P(f"Item '{new_item.title}' has been uploaded successfully.")
    )


@rt("/")
async def get(request):
    return MainLayout(title="Files Catalog", 
                      search_bar=SearchBar(), 
                      content=Gallery(items()))


@rt("/search", methods=["GET"])
async def search(request):
    query = request.query_params.get("search", "")
    filtered_items = [
        item for item in items() if query.lower() in item.title.lower()
    ]
    return Gallery(filtered_items)


@rt("/download/{id:int}", methods=["GET"])
@FastHTML_l402_decorator(authenticator, lambda req:
                         (1, 'USD', 'Download of an item'))
async def download_file(req, id: int):
    item = items[id]
    if not item or not item.file_path:
        return PlainTextResponse("File not found", status_code=404)
    return RedirectResponse(url=f"/files/{item.file_path}")


@rt("/file/{id:int}", methods=["GET"])
async def get_item_details(request, id: int):
    item = items[id]
    if not item:
        return PlainTextResponse("Item not found", status_code=404)
    return ItemDetailsPage(item)


serve()