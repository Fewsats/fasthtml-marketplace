from fasthtml.common import *
import os
import uuid
from starlette.responses import RedirectResponse, PlainTextResponse, Response
from starlette.middleware.cors import CORSMiddleware
from l402.server import Authenticator, FastHTML_l402_decorator
from l402.server.invoice_provider import FewsatsInvoiceProvider
from credentials import FastSQLMacaroonService
from storage import get_storage
from store import get_db

# Database configuration
connstr = os.environ.get("DATABASE_URL", "sqlite:///./data/marketplace.db")
if connstr.startswith("postgres://"):
    connstr = connstr.replace("postgres://", "postgresql://", 1)

# Initialize database
db = get_db(connstr)

# Set up Fewsats invoice provider
# 1. Sign up at app.fewsats.com
# 2. Create API Key
# 3a. Export env variable FEWSATS_API_KEY=fs_...
# or
# 3b. Pass the api key to the provider FewsatsInvoiceProvider(api_key="fs_...")
api_key = os.environ.get("FEWSATS_API_KEY")
fewsats_provider = FewsatsInvoiceProvider(api_key=api_key)

# Set up MacaroonService for storing authentication tokens
macaroon_service = FastSQLMacaroonService(connstr)

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

app = FastHTML(hdrs=(picolink, flexboxgrid))

# Update CORS middleware to expose all headers
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


@rt("/")
async def get(request):
    upload_form = Card(H4("Upload a New Item Form"),
                       mk_form(hx_target="#item-list", hx_swap="afterbegin"))
    items = db.get_items()
    gallery = Div(*[item.__ft__() for item in items],
                  id='item-list',
                  cls="row")
    return Titled("Marketplace", Main(upload_form, gallery, cls='container'))


@rt("/")
async def post(request):
    form = await request.form()

    item_data = {
        'title': form.get('title'),
        'description': form.get('description'),
        'price':
        int(float(form.get('price')) * 100) if form.get('price') else 0,
        'cover_image': '',
        'file_path': ''
    }

    # Handle file uploads
    for field in ['cover_image', 'file']:
        if file := form.get(field):
            content = await file.read()
            filename = f"{field}_{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
            storage.upload(filename, content)
            item_data[field] = filename

    new_item = db.create_item(item_data)
    return new_item.__ft__()


@rt("/download/{id:int}", methods=["GET"])
@FastHTML_l402_decorator(authenticator, lambda req:
                         (1, 'USD', 'Download of an item'))
async def download_file(req, id: int):
    item = db.get_item(id)
    if not item or not item.file_path:
        return PlainTextResponse("File not found", status_code=404)
    return RedirectResponse(url=f"/files/{item.file_path}")


serve()
