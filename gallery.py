from fasthtml.common import *
from item_card import ItemCard

def Gallery(items):
    return Div(cls='relative mx-auto -mt-60 w-full max-w-screen-1xl px-4 pb-7 md:px-14')(
        Div(cls='w-full rounded-lg border border-gray-200 bg-white px-4 py-8 md:px-8 md:py-12')(
        Div(id='item-list', cls='grid grid-cols-1 items-stretch gap-x-6 gap-y-11 md:grid-cols-2 xl:grid-cols-3 items-col')(
            *[ItemCard(item) for item in items()]
        ),
        # Div(cls='mt-4 flex items-center justify-center')(
        #     Div(cls='-mb-4 flex w-fit items-center justify-center opacity-1 transition')(
        #         Button(cls='-mt-px mr-10 flex flex-1 py-4 pointer-events-none opacity-50 transition-all')(
        #             Span(cls='inline-flex items-center border-t-2 border-transparent pr-1 text-sm font-semibold text-zinc-950 hover:text-violet-600')(
        #                 Svg(xmlns='http://www.w3.org/2000/svg', viewbox='0 0 20 20', fill='currentColor', aria_hidden='true', data_slot='icon', cls='mr-3 h-5 w-5 text-zinc-500')(
        #                     Path(fill_rule='evenodd', d='M18 10a.75.75 0 0 1-.75.75H4.66l2.1 1.95a.75.75 0 1 1-1.02 1.1l-3.5-3.25a.75.75 0 0 1 0-1.1l3.5-3.25a.75.75 0 1 1 1.02 1.1l-2.1 1.95h12.59A.75.75 0 0 1 18 10Z', clip_rule='evenodd')
        #                 ),
        #                 'Previous'
        #             )
        #         ),
        #         Ul(cls='-mt-px flex')(
        #             Li(
        #                 Button('1', cls='inline-flex items-center border-t-2 border-transparent p-4 text-sm font-semibold text-violet-600 transition-all')
        #             ),
        #             Li(
        #                 Button('2', cls='inline-flex items-center border-t-2 border-transparent p-4 text-sm font-semibold text-zinc-950 hover:text-violet-500 transition-all')
        #             )
        #         ),
        #         Button(cls='-mt-px ml-10 flex flex-1 justify-end py-4 opacity-1 transition-all')(
        #             Span(cls='inline-flex items-center border-t-2 border-transparent pl-1 text-sm font-semibold text-zinc-950 hover:text-violet-600')(
        #                 'Next',
        #                 Svg(xmlns='http://www.w3.org/2000/svg', viewbox='0 0 20 20', fill='currentColor', aria_hidden='true', data_slot='icon', cls='ml-3 h-5 w-5 text-zinc-500')(
        #                     Path(fill_rule='evenodd', d='M2 10a.75.75 0 0 1 .75-.75h12.59l-2.1-1.95a.75.75 0 1 1 1.02-1.1l3.5 3.25a.75.75 0 0 1 0 1.1l-3.5 3.25a.75.75 0 1 1-1.02-1.1l2.1-1.95H2.75A.75.75 0 0 1 2 10Z', clip_rule='evenodd')
        #                 )
        #             )
        #         )
        #     )
        # )
    )
)