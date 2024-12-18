import json
from extract_functions import (
    load_json_data,
    extract_invoice_value,
    extract_invoice_date,
    process_invoice_number,
    process_particular_item,
)

# Path to your JSON file
json_file_path = "C:/Users/USER/Downloads/prav/scan/Amazon/json/059_007.json"

# Load JSON data from the file
data = load_json_data(json_file_path)

# Combine all text into a single string
all_text = " ".join([data[key]["text"] for key in data])

# Split text into individual lines
lines = all_text.splitlines()

# Extract required values using functions
invoice_value = extract_invoice_value(data)
invoice_date = extract_invoice_date(lines)
invoice_number = process_invoice_number(lines)
particular_item = process_particular_item(lines)

# Display extracted values
print("Extracted Values:")
print(f"Invoice Value: {invoice_value}")
print(f"Invoice Number: {invoice_number}")
print(f"Invoice Date: {invoice_date}")
print(f"Item Particular: {particular_item}")

# Save the results to a JSON file
extracted_data = {
    "Invoice Value": invoice_value,
    "Invoice Number": invoice_number,
    "Invoice Date": invoice_date
}

output_file_path = "extracted_values.json"
with open(output_file_path, "w") as f:
    json.dump(extracted_data, f, indent=4)

print(f"\nExtracted values saved to '{output_file_path}'.")
