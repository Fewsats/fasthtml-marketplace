from fasthtml.common import *

def MainLayout(title="Files catalog", content=None, search_bar=None):
    return Main(
                Div(cls='flex min-h-screen w-full')(
                Div(cls='w-full flex-1')(
                    Div(cls='h-full min-h-screen w-full flex-col')(
                    Div(cls='relative w-full')(
                        Img(alt='background', loading='lazy', decoding='async',
                            data_nimg='fill',
                            style='position:absolute;height:100%;width:100%;left:0;top:0;right:0;bottom:0;color:transparent',
                            sizes='100vw',
                            src='https://marketplace.fewsats.com/images/CatalogBackground.png', 
                            cls='absolute left-0 top-0 object-cover'),
                        Div(cls='relative mx-auto flex w-full max-w-screen-1xl flex-col items-center px-4 pb-64 pt-8 md:px-14')(
                            Div(cls='mb-10 flex w-full justify-between items-center')(  # Changed to justify-between and added items-center
                                A(href="/", cls="flex items-center")(  # Logo as a link
                                    Img(alt='Fewsats',
                                        loading='lazy',
                                        width='126',
                                        height='41',
                                        decoding='async',
                                        data_nimg='1',
                                        style='color:transparent',
                                        src='https://marketplace.fewsats.com/images/FewsatsLogo.svg', cls='h-auto w-32')
                                ),
                                A(href="/upload", cls="flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors duration-300")(
                                    Span(cls="mr-2")("+"),
                                    "Upload File"
                                )
                            ),
                            H1(title, cls='mb-5 text-3xl font-bold text-white sm:text-4xl md:text-5xl'),
                            search_bar,
                        )
                    ),
                    content
                )
            )
        )
    )