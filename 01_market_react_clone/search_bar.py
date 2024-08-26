from fasthtml.common import *

def SearchBar(search_query="", results_target="item-list"):
    return Div(cls='relative mb-20 flex w-full max-w-4xl items-center rounded-lg bg-white px-8 py-4')(
                Label('Search by file name or tags', fr='search-field', cls='sr-only'),
                Svg(xmlns='http://www.w3.org/2000/svg', viewbox='0 0 20 20', fill='currentColor', aria_hidden='true', data_slot='icon', cls='pointer-events-none absolute inset-y-0 left-8 top-4 h-6 w-6 text-gray-400')(
                    Path(fill_rule='evenodd', d='M9 3.5a5.5 5.5 0 1 0 0 11 5.5 5.5 0 0 0 0-11ZM2 9a7 7 0 1 1 12.452 4.391l3.328 3.329a.75.75 0 1 1-1.06 1.06l-3.329-3.328A7 7 0 0 1 2 9Z', clip_rule='evenodd')
                ),
                Input(id='search-field', placeholder='Search by file name or tags', type='search', name='search', value=search_query, 
                      cls='block h-6 w-full border-0 py-0 pl-8 pr-0 text-base leading-6 text-black outline-none placeholder:text-gray-400 focus:ring-0',
                      hx_get="/search", target_id="gallery", hx_swap="innerHTML", hx_trigger="keyup changed delay:500ms")
            )