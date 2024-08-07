from fasthtml.common import *
import os
import uuid
from starlette.responses import RedirectResponse, FileResponse
from starlette.datastructures import UploadFile
from fastalchemy import *
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database configuration
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./data/marketplace.db")
engine = create_engine(DATABASE_URL)
db: Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
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

# Add Flexbox Grid CSS
flexboxgrid = Link(
    rel="stylesheet",
    href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css",
    type="text/css"
)

app = FastHTML(hdrs=(picolink, flexboxgrid))
rt = app.route

@rt("/{fname:path}.{ext:static}")
async def get(fname: str, ext: str):
    return FileResponse(f'{fname}.{ext}')

@patch
def __ft__(self: Item):
    price = f'${self.price / 100:.2f}'
    cover_image = self.cover_image if self.cover_image else 'https://via.placeholder.com/250x200'
    return Div(
        Card(
            Img(src=cover_image, alt=self.title, cls="card-img-top"),
            Div(
                H3(self.title, cls="card-title"),
                P(self.description[:100] + '...' if len(self.description) > 100 else self.description, cls="card-text"),
                P(B("Price: "), price, cls="card-text"),
                cls="card-body"
            )
        ),
        id=f'item-{self.id}',
        cls="col-xs-12 col-sm-6 col-md-4 col-lg-3"
    )

def mk_form(**kw):
    input_fields = Fieldset(
        Label("Title", Input(id="new-title", name="title", placeholder="Heart of Gold", required=True, **kw)),
        Label("Description", Input(id="new-description", name="description", placeholder="3D Model of the spaceship Heart of Gold", required=True, **kw)),
        Label("Price", Input(id="new-price", name="price", placeholder="Price ($)", type="number", required=True, **kw)),
        Group(
            Label("Cover Image", Input(id="new-cover-image", name="cover_image", type="file", required=True, **kw)),
            Label("Item File", Input(id="new-file", name="file", type="file", required=True, **kw))
        )
    )
    return Form(
        Group(input_fields),
        Button("Upload"),
        hx_post="/",
        hx_target="#item-list",
        hx_swap="afterbegin",
        enctype="multipart/form-data"
    )

@rt("/")
async def get(request):
    upload_form = Card(H4("Upload a New Item Form"), mk_form(hx_target="#item-list", hx_swap="afterbegin"))
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
        filepath = os.path.join('uploads', filename)
        os.makedirs('uploads', exist_ok=True)
        with open(filepath, 'wb') as f:
            f.write(content)
        item.cover_image = filepath
    
    file = form.get('file')
    if file:
        content = await file.read()
        filename = f"file_{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
        filepath = os.path.join('uploads', filename)
        os.makedirs('uploads', exist_ok=True)
        with open(filepath, 'wb') as f:
            f.write(content)
        item.file_path = filepath
    
    db.add(item)
    db.commit()
    
    return item.__ft__()

serve()