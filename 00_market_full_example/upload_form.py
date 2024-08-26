from fasthtml.common import *

def UploadForm():
    return Form(
        Div(cls="space-y-8 w-full max-w-2xl mx-auto")(  # Increased width and spacing
            Div(
                Label("Title", for_="title", cls="block text-base font-medium text-gray-700 mb-2"),  # Larger text
                Input(id="title", name="title", type="text", required=True, 
                      cls="mt-1 block w-full rounded-md border-2 border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 text-base p-2")  # Added border and padding
            ),
            Div(
                Label("Description", for_="description", cls="block text-base font-medium text-gray-700 mb-2"),
                Textarea(id="description", name="description", required=True, 
                         cls="mt-1 block w-full rounded-md border-2 border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 text-base p-2")
            ),
            Div(
                Label("Price ($)", for_="price", cls="block text-base font-medium text-gray-700 mb-2"),
                Input(id="price", name="price", type="number", required=True, 
                      cls="mt-1 block w-full rounded-md border-2 border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 text-base p-2")
            ),
            Div(
                Label("Cover Image", for_="cover_image", cls="block text-base font-medium text-gray-700 mb-2"),
                Input(id="cover_image", name="cover_image", type="file", required=True, 
                      cls="mt-1 block w-full text-base text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-base file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100")
            ),
            Div(
                Label("Item File", for_="file", cls="block text-base font-medium text-gray-700 mb-2"),
                Input(id="file", name="file", type="file", required=True, 
                      cls="mt-1 block w-full text-base text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-base file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100")
            ),
            Button("Upload", cls="w-full py-3 px-4 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500")
        ),
        hx_post="/",
        hx_target="#upload-result",
        enctype="multipart/form-data"
    )