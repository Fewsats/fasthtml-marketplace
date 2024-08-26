from fasthtml.common import *
import fasthtml.svg as svg


def BackButton():
    return Svg(xmlns='http://www.w3.org/2000/svg', viewbox='0 0 20 20', fill='currentColor', aria_hidden='true', data_slot='icon', cls='h-6 w-6')(
        svg.Path(fill_rule='evenodd', d='M11.78 5.22a.75.75 0 0 1 0 1.06L8.06 10l3.72 3.72a.75.75 0 1 1-1.06 1.06l-4.25-4.25a.75.75 0 0 1 0-1.06l4.25-4.25a.75.75 0 0 1 1.06 0Z', clip_rule='evenodd')
    ),