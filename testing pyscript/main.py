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
genanki.Package(my_deck).write_to_file('output.apkg')