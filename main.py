from pyscript import display
# display("display test") # shows up at the bottom of the page
print("print test")
try:
    with open("_hanziWriter.js", "r") as js_file:
        console.log("_hanziWriter.js loaded successfully")
except FileNotFoundError:
    console.error("Could not load _hanziWriter.js")
print("print test2")


# from ui_handler import testFunction
# no need to import the test function! local functions seem to magically appear in scope
# testFunction()

from js import document, Uint8Array, File, URL, window, console, fetch, validateForm
from pyodide.ffi import create_proxy, to_js
import io
import genanki
import random
# import requests

# Import the UI functions
# from ui_handler import update_error_messages, update_vocabulary_table, update_statistics

# Global variables
decks = {}
errorTermsList = []
vocabulary_data = []

async def getStrokeData(character = "我"):
    url = f"https://cdn.jsdelivr.net/npm/hanzi-writer-data@latest/{character}.json"
    try:
        # Make the fetch request
        response = await fetch(url)
        
        # Check if the response is OK (status 200)
        if not response.ok:
            console.log(f"Could not find file for {character}; skipping this character")
            return None
        
        # Read the response content as text
        json_data = await response.text()
        
        # Check if the response contains an error message
        if "Couldn't find the requested file" in json_data:
            console.log(f"Could not find file for {character}; skipping this character")
            return None
        
        return json_data
    
    except Exception as e:
        console.error(f"Error fetching stroke data for {character}: {str(e)}")
        return None
    # response = requests.get(url)
    # jsonData = response.content
    # jsonData = jsonData.decode()

    # # if its not a chinese character, then returns None
    # if "Couldn't find the requested file" in jsonData:
    #     console.log("could not find file for " + character + "; skipping this character")
    #     return None
    # return jsonData

async def process_file(file_content, textbook_name, lesson_name):
    global decks, errorTermsList, vocabulary_data
    
    # Reset global variables
    decks = {}
    errorTermsList = []
    vocabulary_data = []
    
    # Process messages to display to user
    messages = []
    messages.append(f"Processing file for {textbook_name}: {lesson_name}")
    
    # Set up outer deck name
    outerDeckName = f"{textbook_name}::{lesson_name}"
    
    # Process the file content line by line
    lines = file_content.split('\n')
    currentDeckName = None
    
    for line in lines:
        # if a line is empty, then skip it 
        if not line.strip(): 
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
            messages.append(f"Found deck section: {deckName}")
            currentDeckName = deckName
            continue

        # otherwise, this is a vocab term
        vocabTerm = lineParts
        
        hanzi = vocabTerm[0]
        messages.append(f"Processing term: {hanzi}")
        
        if len(vocabTerm) < 3:
            errorMsg = f"ERROR: Term '{hanzi}' has too few parts ({len(vocabTerm)}), need at least 3 (hanzi, pinyin, definition)"
            messages.append(errorMsg)
            errorTermsList.append((hanzi, "", len(vocabTerm)))
            continue
            
        pinyin = vocabTerm[1]
        definition = vocabTerm[2]
        examplesExist = True
        
        if len(vocabTerm) == 5:
            exampleChinese = vocabTerm[3]
            exampleEnglish = vocabTerm[4]
        elif len(vocabTerm) == 3:
            examplesExist = False
            errorMsg = f"Note: Term '{hanzi}' has no examples, but this might be intentional"
            messages.append(errorMsg)
            errorTermsList.append((hanzi, pinyin, len(vocabTerm)))
            exampleChinese = ""
            exampleEnglish = ""
        else:
            errorMsg = f"ERROR: Term '{hanzi}' has unexpected number of parts ({len(vocabTerm)})"
            messages.append(errorMsg)
            errorTermsList.append((hanzi, pinyin, len(vocabTerm)))
            if len(vocabTerm) >= 4:
                exampleChinese = vocabTerm[3]
                exampleEnglish = "" if len(vocabTerm) < 5 else vocabTerm[4]
            else:
                exampleChinese = ""
                exampleEnglish = ""

        # Add to vocabulary data for display in table
        vocab_item = {
            "english": definition,
            "chinese": hanzi,
            "pinyin": pinyin,
            "example_en": exampleEnglish,
            "example_cn": exampleChinese
        }
        vocabulary_data.append(vocab_item)

        # if no deck was specified, use default
        if currentDeckName is None:
            currentDeckName = lesson_name if lesson_name else "Vocabulary"

        # format for hanzi writer + my template
        async def getCardFrontBack():
            front = f"{definition}"
            if examplesExist: front += f"<br>(phrases: {exampleEnglish})"

            back = f"{hanzi} {pinyin}"
            if examplesExist: back += f"<br>(phrases: {exampleChinese})"
            back += "<br>"

            back += f'<div id="hanzi" style="display:none">{hanzi.replace("（", "").replace("）", "")}</div>'
            front += f'<div id="hanzi" style="display:none">{hanzi.replace("（", "").replace("）", "")}</div>'

            # add the stroke order data in an invisible div
            for character in hanzi:
                strokeJsonData = await getStrokeData(character)
                if strokeJsonData == None: continue
                back += f'<div id="{character}" style="display:none">{strokeJsonData}</div>'
            
            return (front, back)

        # Get card front and back content
        front, back = await getCardFrontBack()
        
        # Store in decks dictionary
        if (currentDeckName not in decks): 
            decks[currentDeckName] = []
        decks[currentDeckName].append((front, back))

    # Update UI with processed data
    update_error_messages(messages)
    update_vocabulary_table(vocabulary_data)
    
    stats = {
        'total_cards': sum(len(cards) for cards in decks.values()),
        'success': sum(len(cards) for cards in decks.values()) - len(errorTermsList),
        'warnings': len(errorTermsList)
    }
    update_statistics(stats)
    
    # Enable download button if we have cards
    if stats['total_cards'] > 0:
        download_btn = document.getElementById("download-btn")
        
        # download_btn.disabled = not validateForm()
        validateForm() # automatically enables or disables the download button
        # Set up download button event listener
        download_btn.addEventListener("click", create_proxy(generate_and_download_anki_package))

def generate_and_download_anki_package(event):
    # Get deck metadata
    textbook_name = document.getElementById("textbook-name").value
    lesson_name = document.getElementById("lesson-name").value
    outerDeckName = f"{textbook_name}::{lesson_name}"
    
    try:
        # Card template setup
        model_id = 1956882460  # Template ID
        model_name = "Kabir's Chinese Card Template"

        # Try to read template files, or use defaults if files don't exist
        try:
            # frontTemplateFileString = open("FrontTemplate.html", "r", encoding="utf8").read()
            # backTemplateFileString = open("BackTemplateNoStrokeData.html", "r", encoding="utf8").read()
            # templateStylingFileString = open("TemplateStyling.css", "r", encoding="utf8").read()
            frontTemplateFileString = window.frontTemplate
            backTemplateFileString = window.backTemplate
            templateStylingFileString = window.templateStyling
        except Exception as e:
            update_error_messages([f"Error generating Anki package: {str(e)}"])
            frontTemplateFileString = "{{Front}}"
            backTemplateFileString = "{{FrontSide}}<hr id='answer'>{{Back}}"
            templateStylingFileString = ".card { font-family: arial; font-size: 20px; text-align: center; }"
        
        # print("from python front template:", backTemplateFileString)

        # Create the model aka template
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

        # Generate all decks
        allGenAnkiDecks = []
        for deckName in decks.keys():
            deckFullName = f"{outerDeckName}::{deckName}"
            deckId = random.randrange(1 << 30, 1 << 31)
            
            # Create the new deck
            my_deck = genanki.Deck(deckId, deckFullName)
            
            # Add cards to deck
            cards = decks[deckName]
            for front, back in cards:
                newCard = genanki.Note(
                    model=my_model, 
                    fields=[front, back]
                )
                my_deck.add_note(newCard)
            
            allGenAnkiDecks.append(my_deck)

        # Create package with all decks
        my_package = genanki.Package(allGenAnkiDecks)
        
        # Try to add media files if they exist
        try:
            my_package.media_files = ['_hanziWriter.js']
        except:
            pass
            
        # Generate package filename
        ankiPackageFileName = f'{outerDeckName.replace("::", " ")} {lesson_name} Anki Package.apkg'

        # Write to in-memory buffer instead of file
        buffer = io.BytesIO()
        my_package.write_to_file(buffer)
        buffer.seek(0)  # Reset buffer position to the beginning

        # Convert the buffer to a format usable in the browser
        content = buffer.getvalue()
        content_array = Uint8Array.new(bytearray(content))

        # Create a Blob and URL for downloading
        file = File.new([content_array], ankiPackageFileName, {"type": "application/octet-stream"})
        url = URL.createObjectURL(file)

        # Trigger download directly
        download_link = document.createElement("a")
        download_link.href = url
        download_link.download = ankiPackageFileName
        download_link.style.display = "none"
        document.body.appendChild(download_link)
        download_link.click()
        document.body.removeChild(download_link)
        
        # Clean up the URL object
        URL.revokeObjectURL(url)
        
        # Update UI with success message
        update_error_messages([f"Successfully generated Anki package: {ankiPackageFileName}"])
        
    except Exception as e:
        update_error_messages([f"Error generating Anki package: {str(e)}"])

# Connect to UI handler
async def handle_file_from_ui(file_text, file_name):
    # Get deck metadata
    textbook_name = document.getElementById("textbook-name").value
    lesson_name = document.getElementById("lesson-name").value
    
    # Process the file
    await process_file(file_text, textbook_name, lesson_name)
    
    return {
        'status': 'success',
        'message': f'Processed file: {file_name}',
        'vocab_count': len(vocabulary_data)
    }