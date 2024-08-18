from fasthtml.common import *
from item_card import ItemCard

def Gallery(items):
    return Div(id='gallery', cls='relative mx-auto -mt-60 w-full max-w-screen-1xl px-4 pb-7 md:px-14')(
        Div(cls='w-full rounded-lg border border-gray-200 bg-white px-4 py-8 md:px-8 md:py-12')(
        Div(id='item-list', cls='grid grid-cols-1 items-stretch gap-x-6 gap-y-11 md:grid-cols-2 xl:grid-cols-3 items-col')(
            *[ItemCard(item) for item in items]
        ),
    )
)