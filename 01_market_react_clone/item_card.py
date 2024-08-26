from fasthtml.common import *

def ItemCard(item):
    price = f'${item.price / 100:.2f}'
    cover_image = f'https://fewsats-production-public-files.s3.us-west-1.amazonaws.com/cover-images/{item.id}'

    return Div(
        A(href=f'/file/{item.id}', cls='flex h-full w-full flex-col rounded-lg border border-gray-200')(
            Div(cls='relative aspect-video w-full overflow-hidden rounded-t-xl')(
                Img(alt=item.title, decoding='async', data_nimg='fill',
                    style='width:100%',
                    #  style='position:absolute;height:100%;width:100%;left:0;top:0;right:0;bottom:0;color:transparent', 
                      src=cover_image, cls='bg-gray-100 object-cover transition-opacity')
            ),
            Div(cls='flex w-full flex-1 flex-col justify-between p-5')(
                Div(
                    Div(item.title, cls='mb-2 line-clamp-2 h-12 text-base font-medium text-zinc-950'),
                    Div(item.description[:200] + '...' if len(item.description) > 200 else item.description, cls='mb-4 line-clamp-5 h-25 text-sm text-gray-400'),
                    (Div(cls='mb-4 flex flex-wrap items-start gap-2')(
                        *[Div(tag, cls='rounded-md bg-purple-100 px-1.5 py-1 text-xs font-medium leading-4 text-purple-700') for tag in item.tags.split(';')]
                    ) if item.tags else None)
                ),
                Div(cls='pt-10 text-base font-semibold leading-6 text-gray-400')(
                    'Price:',
                    Span(price, cls='ml-2 text-base font-semibold leading-6 text-zinc-950')
                )
            )
        )
    )