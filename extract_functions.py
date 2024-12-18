import json
import re

def load_json_data(json_file_path):
    """Load JSON data from a file."""
    with open(json_file_path, "r") as file:
        return json.load(file)

#def extract_invoice_value(all_text):
    """Extract the invoice value using regex."""
   # match = re.search(r"Invoice Value\s*[:\-]?\s*([\d.]+)", all_text)
   # return match.group(1) if match else None



def extract_invoice_value(data_obj):
    """
    Extract the maximum invoice value based on context within a JSON-like object.
    Searches for 'Amount' or 'Invoice Value' and processes word by word.
    """
    potential_values = []
    
    # Define a list of value patterns to match
    value_patterns = [
        r"\b\d{1,3}(,\d{3})*(\.\d{2})?\b",  # e.g., 1,234.56 or 1234.56
        r"\b\d+\.\d{2}\b",                  # e.g., 1234.56
    ]
    
    # Iterate over the object to extract values
    for key, text in data_obj.items():
        if "Amount" in text or "Invoice Value" in text:
            # Split the text into words
            words = text.split()
            for word in words:
                # Check each word against the value patterns
                for pattern in value_patterns:
                    match = re.fullmatch(pattern, word)
                    if match:
                        # Remove commas for numeric comparison
                        clean_value = float(match.group().replace(",", ""))
                        potential_values.append(clean_value)
    
    # Return the maximum value if matches are found, else an empty string
    return max(potential_values, default="") if potential_values else ""




def extract_invoice_date(lines):
    """Extract the invoice date based on context."""
    invoice_date = ""
    
    # Define a list of date formats to match
    date_patterns = [
        r"\b\d{2}\.\d{2}\.\d{4}\b",  # e.g., 09.02.2024
        r"\b\d{2}-\d{2}-\d{4}\b",      # e.g., 09-02-2024
        r"\b\d{4}/\d{2}/\d{2}\b",      # e.g., 2024/02/09
        r"\b\d{2}/\d{2}/\d{4}\b",      # e.g., 09/02/2024
    ]

    for i, line in enumerate(lines):
        if "Invoice Date" in line:
            prev_line = lines[i-1] if i > 0 else ""
            next_line = lines[i+1] if i < len(lines) - 1 else ""
            combined_lines = f"{prev_line} {line} {next_line}"
            
            # Search for date patterns in the combined text
            for pattern in date_patterns:
                match = re.search(pattern, combined_lines)
                if match:
                    invoice_date = match.group()
                    break

        if invoice_date:  # Stop processing once date is found
            break

    return invoice_date


def clean_line(line):
    """Clean a line by removing special characters, numbers, and specific tax keywords."""
    cleaned = re.sub(r'[^a-zA-Z\s]', ' ', line)  # Remove special characters and numbers
    cleaned = re.sub(r'\b(IGST|SGST|CGST)\b', '', cleaned, flags=re.IGNORECASE)  # Remove tax keywords
    return " ".join(cleaned.split())  # Remove extra spaces

def process_invoice_number(lines):
    """Extract the invoice number based on context."""
    invoice_number = ""
    for i, line in enumerate(lines):
        if "Invoice Number" in line:
            prev_line = lines[i-1] if i > 0 else ""
            next_line = lines[i+1] if i < len(lines) - 1 else ""
            combined_lines = f"{prev_line} {next_line} {line}"
            words = combined_lines.split()
            for word in words:
                if re.match(r"\b[A-Za-z0-9]+-\d{5,}\b", word):
                    if len(word) <= 10:
                        invoice_number = word
                        break
    return invoice_number

def process_particular_item(lines):
    """Extract and clean specific item details from lines based on tax keywords."""
    particular_cleaned = ""
    for i, line in enumerate(lines):
        if "cGST" in line or "IGST" in line:  # Search for tax-related lines
            prev_line = lines[i-1] if i > 0 else ""
            next_line = lines[i+1] if i < len(lines) - 1 else ""
            cleaned_prev = clean_line(prev_line)
            cleaned_current = clean_line(line)
            cleaned_next = clean_line(next_line)
            particular_cleaned = f"{cleaned_prev} {cleaned_current} {cleaned_next}"
            break
    return particular_cleaned
