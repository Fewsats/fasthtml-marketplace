from fasthtml.common import *

def ItemCard(item):
    price = f'${item.price / 100:.2f}'
    cover_image = f'/files/{item.cover_image}' if item.cover_image else 'https://via.placeholder.com/250x200'
    return Div(Card(
        Img(src=cover_image, alt=item.title, cls="card-img-top"),
        Div(H3(item.title, cls="card-title"),
            P(item.description[:100] + '...' if len(item.description) > 100 else item.description, cls="card-text"),
            P(B("Price: "), price, cls="card-text"),
            A("Download Link", href=f"/download/{item.id}", cls="btn btn-primary"),
            A("Pay with Hub", href=f"https://app.paywithhub.com/purchases?l402_url=https://fast-html-l402-market.replit.app/download/{item.id}", cls="btn btn-primary"),
            cls="card-body")),
        id=f'item-{item.id}',
        cls="col-xs-12 col-sm-6 col-md-4 col-lg-3")


