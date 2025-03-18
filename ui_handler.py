def testFunction():
    print("test function called")
from js import document, File, console
from pyodide.ffi import create_proxy
import asyncio

async def handle_file_upload(event):
    try:
        console.log("File upload event triggered")
        if not event.target.files or event.target.files.length == 0:
            console.error("No files selected")
            update_error_messages(["Error: No files selected"])
            return
        
        # print(event.target.files.item(0))
        file = event.target.files.item(0)

        console.log(f"Processing file: {file.name}")
        
        # Read the file content
        try:
            text = await file.text()
            console.log(f"File content length: {len(text)}")
        except Exception as e:
            console.error(f"Error reading file: {str(e)}")
            update_error_messages([f"Error reading file: {str(e)}"])
            return
        
        # Import the main module
        # try:
            # import main
        # except Exception as e:
        #     console.error(f"Error importing main module: {str(e)}")
        #     update_error_messages([f"Error importing main module: {str(e)}"])
        #     return
        
        # Get deck metadata
        textbook_name = document.getElementById("textbook-name").value
        lesson_name = document.getElementById("lesson-name").value
        
        # Use the main module to process the file
        try:
            # result = main.handle_file_from_ui(text, file.name)
            result = handle_file_from_ui(text, file.name)
            console.log(f"File processing result: {result}")
            
            # Show initial upload success message
            update_error_messages([f"File uploaded: {file.name}", f"Found {result['vocab_count']} vocabulary items"])
        except Exception as e:
            console.error(f"Error processing file: {str(e)}")
            update_error_messages([f"Error processing file: {str(e)}"])
    except Exception as e:
        console.error(f"Unexpected error in handle_file_upload: {str(e)}")
        update_error_messages([f"Unexpected error: {str(e)}"])

def update_error_messages(messages):
    error_div = document.getElementById("error-messages")
    error_div.innerHTML = ""
    for message in messages:
        msg_elem = document.createElement("div")
        msg_elem.className = "p-4 mb-2 text-sm rounded-lg"
        if "error" in message.lower():
            msg_elem.className += " bg-red-100 text-red-700"
        else:
            msg_elem.className += " bg-blue-100 text-blue-700"
        msg_elem.textContent = message
        error_div.appendChild(msg_elem)

def update_vocabulary_table(data):
    tbody = document.getElementById("vocabulary-table-body")
    tbody.innerHTML = ""
    for item in data:
        row = document.createElement("tr")
        for field in [item["english"], item["chinese"], item["pinyin"], 
                     item["example_en"], item["example_cn"]]:
            cell = document.createElement("td")
            cell.className = "px-6 py-4 whitespace-nowrap text-sm text-gray-900"
            cell.textContent = field
            row.appendChild(cell)
        tbody.appendChild(row)

def update_statistics(stats):
    stats_div = document.getElementById("statistics")
    stats_div.innerHTML = f"""
        <p>Total cards: {stats['total_cards']}</p>
        <p>Processed successfully: {stats['success']}</p>
        <p>Warnings: {stats['warnings']}</p>
    """

# This function will be called when PyScript is ready
def on_pyscript_ready():
    console.log("PyScript is ready, initializing UI handlers")
    # Set up event listeners
    file_input = document.getElementById("file-input")
    if file_input:
        file_input.addEventListener("change", create_proxy(handle_file_upload))
        console.log("File input event listener attached")
    else:
        console.error("Could not find file-input element")
    
    # Set up download button
    download_btn = document.getElementById("download-btn")
    if download_btn:
        download_btn.disabled = True
        console.log("Download button initialized")
    else:
        console.error("Could not find download-btn element")
    
    # Hide loading indicator if it exists
    loading = document.getElementById("loading-indicator")
    if loading:
        loading.style.display = "none"
        console.log("Loading indicator hidden")

# Initialize when the module is loaded
console.log("UI handler module loaded")
on_pyscript_ready() 