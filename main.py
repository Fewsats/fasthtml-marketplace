from fasthtml.common import *
import os
import uuid
from starlette.responses import RedirectResponse, PlainTextResponse, Response
from starlette.middleware.cors import CORSMiddleware
from l402.server import Authenticator, FastHTML_l402_decorator
from l402.server.invoice_provider import FewsatsInvoiceProvider
from credentials import get_macaroon_service
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from storage import get_storage


# Database configuration
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./data/marketplace.db")
DATABASE_URL = DATABASE_URL.replace("postgres", "postgresql")

engine = create_engine(DATABASE_URL)
db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Integer)
    cover_image = Column(String)
    file_path = Column(String)

Base.metadata.create_all(bind=engine)

# Set up Fewsats invoice provider
# 1. Sign up at app.fewsats.com
# 2. Create API Key
# 3a. Export env variable FEWSATS_API_KEY=fs_...
# or
# 3b. Pass the api key to the provider FewsatsInvoiceProvider(api_key="fs_...")

api_key = os.environ.get("FEWSATS_API_KEY")
fewsats_provider = FewsatsInvoiceProvider(api_key=api_key)

# Set up MacaroonService for storing authentication tokens
macaroon_service = get_macaroon_service()

# Initialize the L402 Authenticator
authenticator = Authenticator(location='localh8000',
                              invoice_provider=fewsats_provider,
                              macaroon_service=macaroon_service)

storage = get_storage()

# Add Flexbox Grid CSS
flexboxgrid = Link(
    rel="stylesheet",
    href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css",
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


@patch
def __ft__(self: Item):
    price = f'${self.price / 100:.2f}'
    cover_image = f'/files/{self.cover_image}' if self.cover_image else 'https://via.placeholder.com/250x200'
    return Div(Card(
        Img(src=cover_image, alt=self.title, cls="card-img-top"),
        Div(H3(self.title, cls="card-title"),
            P(self.description[:100] +
              '...' if len(self.description) > 100 else self.description,
              cls="card-text"),
            P(B("Price: "), price, cls="card-text"),
            A("Download Link",
              href=f"/download/{self.id}",
              cls="btn btn-primary"),
            A("Pay with Hub",
              href=
              f"https://app.paywithhub.com/purchases?l402_url=https://fast-html-l402-market.replit.app/download/{self.id}",
              cls="btn btn-primary"),
            cls="card-body")),
               id=f'item-{self.id}',
               cls="col-xs-12 col-sm-6 col-md-4 col-lg-3")

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
    items = db.query(Item).all()
    gallery = Div(*reversed(items), id='item-list', cls="row")
    return Titled("Marketplace", Main(upload_form, gallery, cls='container'))

@rt("/")
async def post(request):
    form = await request.form()

    item = Item(
        title=form.get('title'),
        description=form.get('description'),
        price=int(float(form.get('price')) * 100) if form.get('price') else 0,
        cover_image='',
        file_path=''
    )

    cover_image = form.get('cover_image')
    if cover_image:
        content = await cover_image.read()
        filename = f"cover_{uuid.uuid4()}{os.path.splitext(cover_image.filename)[1]}"
        storage.upload(filename, content)
        item.cover_image = filename  # Store only the filename

    file = form.get('file')
    if file:
        content = await file.read()
        filename = f"file_{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
        storage.upload(filename, content)
        item.file_path = filename  # Store only the filename

    db.add(item)
    db.flush()  # This will populate the id
    db.commit()

    return item.__ft__()

@rt("/download/{id:int}", methods=["GET"])
@FastHTML_l402_decorator(authenticator, lambda req:
                         (1, 'USD', 'Download of an item'))
async def download_file(req, id: int):
    item = db.query(Item).filter(Item.id == id).first()
    if not item or not item.file_path:
        return PlainTextResponse("File not found", status_code=404)

    return RedirectResponse(url=f"/files/{item.file_path}")

serve()