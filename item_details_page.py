from fasthtml.common import *
from back_button import BackButton


def ItemDetailsPage(item):
    price = f'${item.price / 100:.2f}'
    cover_image = f'/files/{item.cover_image}' if item.cover_image else 'https://via.placeholder.com/250x200'
    file_name = item.file_path.split('/')[-1] if item.file_path else ''

    return Div(cls='flex min-h-screen w-full')(
        Div(cls='w-full flex-1')(
            Div(cls='mx-auto h-full min-h-screen w-full max-w-screen-1xl flex-col space-y-6 bg-white px-4 pb-8 pt-6 sm:space-y-8 sm:pb-16 sm:pt-8 md:px-14')(
                Div(cls='flex w-full py-2 text-sm leading-6 text-gray-500')(
                    A(href='/', cls='items-align flex space-x-3 transition-colors hover:text-violet-600')(
                        BackButton(),
                        Span('Back to Catalog')
                    )
                ),
                Div(cls='w-full')(
                    Div(item.title, cls='mb-1 text-2xl font-bold text-zinc-950 sm:mb-4 sm:text-3xl'),
                    Div(cls='mb-6 py-1.5 text-base font-medium leading-6 text-zinc-400 sm:mb-8 md:mb-9')(
                        'Price:',
                        Span(price, cls='ml-2 text-lg font-semibold leading-6 text-zinc-950 sm:text-xl')
                    ),
                    Div(cls='flex flex-col space-y-6 sm:space-y-8 md:flex-row md:space-y-0')(
                        Div(cls='relative flex-1')(
                            Img(alt=item.title, loading='lazy', width='692', height='603', decoding='async', data_nimg='1', src=cover_image, style='color: transparent;', cls='h-auto w-full rounded-lg border border-gray-200')
                        ),
                        Div(cls='flex-1 space-y-6 px-0 sm:space-y-8 md:px-4 lg:px-11')(
                            Div(item.description, cls='whitespace-pre-line text-base font-light text-zinc-950'),
                            Div(cls='flex flex-wrap items-start gap-2')(
                                *[Div(tag, cls='rounded-md bg-purple-100 px-1.5 py-1 text-xs font-medium leading-4 text-purple-700 sm:px-2 sm:py-2 sm:text-base') for tag in item.tags.split(';')]
                            ) if item.tags else None,
                            Div(cls='flex gap-2')(
                                Div(cls='flex-1 rounded-lg border border-gray-300 p-3 text-sm leading-4 text-zinc-400 sm:p-4 sm:text-base')(
                                    'File Name:',
                                    Span(file_name, cls='ml-2 break-all font-medium text-zinc-950')
                                )
                            ),
                            Div(cls='w-full flex flex-col space-y-4')(
                                A('Pay with Hub (Credit Card)', target='_blank', href='http://app.paywithhub.com/purchases?l402_url=https%3A%2F%2Fapi.fewsats.com%2Fv0%2Fstorage%2Fdownload%2F5e3cda4c-5a5e-4635-953f-cb6fa2fb5647', cls='flex transition-all w-full justify-center rounded-lg px-3 py-2 text-base text-white outline-none hover:bg-violet-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 bg-violet-700 shadow-inner-white outline-none ring-1 ring-inset ring-zinc-700'),
                                Div(cls='space-y-2 relative')(
                                    P('After paying with Hub, enter the provided credentials here:', cls='text-sm text-gray-600 text-center flex items-center justify-center'),
                                    Div(cls='w-full')(
                                        Div(cls='relative rounded-md')(
                                            Input(id='credentials', placeholder='Enter credentials', aria_describedby='credentials-error', type='text', value='', name='credentials', cls='block w-full rounded-md border-0 px-2 py-1.5 text-black ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-1 focus:ring-inset focus:ring-zinc-950 shadow-none outline-none sm:text-sm sm:leading-6')
                                        )
                                    ),
                                    Button('Download File', type='button', disabled='', cls='flex transition-all w-full justify-center rounded-lg px-3 py-2 text-base text-white outline-none hover:bg-violet-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 pointer-events-none bg-gray-200 text-gray-500'),
                                )
                            )
                        )
                    )
                )
            )
        )
    )