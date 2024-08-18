from fasthtml.common import *
from search_bar import SearchBar
from gallery import Gallery

def MainLayout(title="Files catalog", items=(), search_query=""):
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
                            Div(cls='mb-10 flex w-full justify-start')(
                                Img(alt='Fewsats',
                                     loading='lazy',
                                       width='126',
                                         height='41',
                                           decoding='async',
                                             data_nimg='1',
                                               style='color:transparent',
                                                 src='https://marketplace.fewsats.com/images/FewsatsLogo.svg', cls='h-auto w-32')
                            ),
                            H1(title, cls='mb-5 text-3xl font-bold text-white sm:text-4xl md:text-5xl'),
                            SearchBar(search_query),
                        )
                    ),
                    Gallery(items)
                )
            )
        )
    )