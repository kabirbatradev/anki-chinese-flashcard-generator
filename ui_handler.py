from js import document, File, console
from pyodide.ffi import create_proxy
import asyncio

async def handle_file_upload(event):
    file = event.target.files[0]
    text = await file.text()
    
    # Import the main module
    import main
    
    # Get deck metadata
    textbook_name = document.getElementById("textbook-name").value
    lesson_name = document.getElementById("lesson-name").value
    
    # Use the main module to process the file
    result = main.handle_file_from_ui(text, file.name)
    
    # Show initial upload success message
    update_error_messages([f"File uploaded: {file.name}", f"Found {result['vocab_count']} vocabulary items"])

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

# Set up event listeners
file_input = document.getElementById("file-input")
file_input.addEventListener("change", create_proxy(handle_file_upload))

# Set up download button
download_btn = document.getElementById("download-btn")
download_btn.disabled = True 