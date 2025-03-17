
# write the name of the vocab list here: 
# Example: vocabListFileName = "Lesson 1.txt"
outerDeckName = "Chinese::Lesson 10"
vocabListFileName = "L10 Vocab List Updated.txt"
# note that only txt files work

# import html
import requests
import genanki
import random

    
def getStrokeData(character = "我"):
    # if character in "（）":
    #     # skip because its just a parenthesis
    #     return None

    url = f"https://cdn.jsdelivr.net/npm/hanzi-writer-data@latest/{character}.json"
    response = requests.get(url)
    jsonData = response.content
    jsonData = jsonData.decode()

    # if its not a chinese character, then returns None
    if "Couldn't find the requested file" in jsonData:
        print("could not find file for " + character + "; skipping this character")
        return None
    return jsonData

# test
# print("testing getStrokeData", getStrokeData("（"))

vocabListFile = open(vocabListFileName, "r", encoding="utf8") # "r" means read
# print(file.read())

# 'deckname': [('front', 'back'), ('front', 'back'), ...)]
decks = {}
writeToFiles = False

# new file is created whenever a new section is reached in the file
ankiDeckFile = None
currentDeckName = None

# keep track of all terms with errors to print them at the end
errorTermsList = []

# each line has a new line at the end of it already
for line in vocabListFile:

    # if a line is empty, then skip it 
    if line == "\n": 
        # print("empty line")
        continue
    
    # split the line into parts by semicolon or colon
    chineseSemicolon = "；"
    normalSemicolon = ";"
    colon = ":"

    # replace occurences of colon or chinese semicolon with normal semicolon
    line = line.replace(chineseSemicolon, normalSemicolon)
    line = line.replace(colon, normalSemicolon)
    # then split by semicolon
    lineParts = line.split(normalSemicolon)

    # strip/trim off any learning or trailing whitespace from each part
    for i in range(len(lineParts)):
        lineParts[i] = lineParts[i].strip()


    
    # if a line does not have any semicolons, it must be the title of a new deck
    if len(lineParts) == 1:
        deckName = lineParts[0]
        # deckName = deckName.replace(' ', ' ') # attempt to replace chinese space with regular space
        print("NEW DECK:", deckName)

        # if we already have a file open, then close it before creating a new file
        if currentDeckName != None:
            if writeToFiles: ankiDeckFile.close()
        
        # create a new file for this new deck
        if writeToFiles: ankiDeckFile = open(deckName + ".txt", "w", encoding="utf8")
        currentDeckName = deckName
        
        continue

    # otherwise, this is a vocab term
    vocabTerm = lineParts

    
    
    # print(vocabTerm)
    hanzi = vocabTerm[0]
    print('downloading ', hanzi)
    pinyin = vocabTerm[1]
    definition = vocabTerm[2]
    examplesExist = True
    if len(vocabTerm) == 5:
        exampleChinese = vocabTerm[3]
        exampleEnglish = vocabTerm[4] # chinese example translated into english
        # examplesExist = True
    elif len(vocabTerm) == 3:
        examplesExist = False
        print("this term seems to not have examples, but it might be an error")
        errorTermsList.append((hanzi, pinyin, len(vocabTerm)))
    else:
        
        print(f"ERROR: len of vocabTerm is {len(vocabTerm)} for word: {hanzi} {pinyin}")
        print(f"(This means it might be missing pinyin or english translation of examples)")
        errorTermsList.append((hanzi, pinyin, len(vocabTerm)))
        
    # print("hanzi:", hanzi)
    # print("pinyin:", pinyin)


    # if no file was opened, then this vocab term comes before something like "Text 1" to label the deck
    if currentDeckName == None:
        if writeToFiles: ankiDeckFile = open("NoDeckName.txt", 'w', encoding="utf8")
        currentDeckName = "NoDeckName"
        


    # format for hanzi writer + my template
    def getCardFrontBack():

        front = f"{definition}"
        if examplesExist: front += f"<br>(phrases: {exampleEnglish})"

        back = f"{hanzi} {pinyin}"
        if examplesExist: back += f"<br>(phrases: {exampleChinese})"
        back += "<br>"

        # format for the back side:
        # <div id="hanzi" style="display:none">我是钢琴</div>
        # <img src="我.js" style="display:none">
            # for each hanzi

        back += f'<div id="hanzi" style="display:none">{hanzi.replace("（", "").replace("）", "")}</div>'
        # add the hanzi to the front too so we can potentially add hanzi writer quiz
        front += f'<div id="hanzi" style="display:none">{hanzi.replace("（", "").replace("）", "")}</div>'

        # add the stroke order data in an invisible div
        for character in hanzi:
            # no need to add the dummy image to trick anki into thinking the character js is a dependency
            # back += f'<img src="{character}.js" style="display:none">'
            # downloadStrokeData(character)

            strokeJsonData = getStrokeData(character)
            if strokeJsonData == None: continue
            back += f'<div id="{character}" style="display:none">{strokeJsonData}</div>'
        
        return (front, back)
        # ankiDeckFile.write(front + ";" + back + "\n")

    # writeToFileHanziWriterFormat()
    front, back = getCardFrontBack()
    if writeToFiles: ankiDeckFile.write(front + ";" + back + "\n")
    if (currentDeckName not in decks): decks[currentDeckName] = []
    decks[currentDeckName].append((front, back))

# decks dictionary
# each deck should contain a list of tuples: front and back of card

# https://github.com/AnKing-VIP/advanced-browser
# https://ankiweb.net/shared/info/874215009
# use this addon to get internal information on cards
# including the note type id aka model id
# this will allow me to overwrite the old model on lesson 8
# (because it will have the same id)
# nvm this

# old model id: 1607392319
# updating the model id will create a new model (card template)

model_id = 1956882460  # make a new id for new template (no stroke data)
# random.randrange(1 << 30, 1 << 31)
# deck_ids = [1567115450, 1705746358, 1152996867, 1085417380]
model_name = "Kabir's Chinese Card Template"


frontTemplateFileString = open("FrontTemplate.html", "r", encoding="utf8").read()
backTemplateFileString = open("BackTemplate.html", "r", encoding="utf8").read()
templateStylingFileString = open("TemplateStyling.css", "r", encoding="utf8").read()


# create the model aka template
my_model = genanki.Model(
    model_id,
    model_name,
    fields=[
        {"name": "Front"},
        {"name": "Back"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": frontTemplateFileString,
            "afmt": backTemplateFileString,
        },
    ],
    css=templateStylingFileString
)
# make sure to use a unique model id:
# import random; random.randrange(1 << 30, 1 << 31)
# and hardcode it into your Model definition.

# create a new note:
# my_note = genanki.Note(
#     model=my_model, 
#     fields=["Capital of Argentina", "Buenos Aires"]
# )

allGenAnkiDecks = []
for deckName in decks.keys():
    deckFullName = f"{outerDeckName}::{deckName}"
    deckId = random.randrange(1 << 30, 1 << 31) # deck id is always new
    print("NEW DECK:", deckFullName)

    # create the new deck
    my_deck = genanki.Deck(deckId, deckFullName)

    # (front, back)
    cards = decks[deckName]

    for front, back in cards:
        print('adding to anki: ', front[0:15] + "..." if len(front) > 15 else "")

        newCard = genanki.Note(
            model=my_model, 
            # fields=[html.escape(front), html.escape(back)]
            fields=[front, back]
        )

        # add new card to deck
        my_deck.add_note(newCard)

    allGenAnkiDecks.append(my_deck)

# add all the decks into one package called {outerDeckName}
my_package = genanki.Package(allGenAnkiDecks)
my_package.media_files = ['_hanziWriter.js']
ankiPackageFileName = f'{outerDeckName.replace("::", " ")} Anki Package.apkg'
my_package.write_to_file(ankiPackageFileName)

print("\nCompleted generation of anki package: " + ankiPackageFileName)

print("\nNOTE: terms with errors (they might be missing pinyin, examples, example english translation, or even just a semicolon): ")
for term in errorTermsList:
    print(f"hanzi: {term[0]}, pinyin: {term[1]}", end="")
    if (term[2] == 3): print("; note: this term might simply be missing examples")
    else: print()