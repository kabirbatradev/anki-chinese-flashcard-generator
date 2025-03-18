from pyscript import display
import random

display("Hello")

print("this is a print statement") # converts to console.log


display(random.randrange(1 << 30, 1 << 31))









import genanki 

# how to create a model:
my_model = genanki.Model(
    1607392310,
    "Simple Model",
    fields=[
        {"name": "Question"},
        {"name": "Answer"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Question}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
    ],
    css=\
""".card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}"""
)
# use a unique model id:
# import random; random.randrange(1 << 30, 1 << 31)
# and hardcode it into your Model definition.

# create a new note:
my_note = genanki.Note(
    model=my_model, 
    fields=["Capital of Argentina", "Buenos Aires"]
)


# make a deck
# old deck id:2059400110
my_deck = genanki.Deck(2059400110, "Country Capitals")

my_deck.add_note(my_note)

# this doesnt work in website, need to make fake url
# genanki.Package(my_deck).write_to_file('output.apkg')











from pyodide.ffi import create_proxy
from js import document, Uint8Array, File, URL, window
import io

# Instead of writing directly to a file, write to an in-memory buffer
buffer = io.BytesIO()
genanki.Package(my_deck).write_to_file(buffer)
buffer.seek(0)  # Reset buffer position to the beginning

# Convert the buffer to a format usable in the browser
content = buffer.getvalue()
content_array = Uint8Array.new(bytearray(content))

# Create a Blob and URL for downloading
file = File.new([content_array], "output.apkg", {type: "application/octet-stream"})
url = URL.createObjectURL(file)

# Create a download link and trigger it
download_link = document.createElement("a")
download_link.href = url
download_link.download = "output.apkg"
download_link.innerHTML = "Download Anki Package"
document.body.appendChild(download_link)

# Optional: Auto-trigger the download without requiring a click
# download_link.click()

# Clean up the URL object when done
def cleanup(event):
    URL.revokeObjectURL(url)

download_link.addEventListener("click", create_proxy(cleanup))