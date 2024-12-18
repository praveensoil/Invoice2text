import os
import json
import pandas as pd
from extract_functions import (
    load_json_data,
    extract_invoice_value,
    extract_invoice_date,
    process_invoice_number,
    process_particular_item,
)

# Folder containing JSON files
json_folder_path = "C:/Users/USER/Downloads/prav/scan/Amazon/json"

# Output file for storing extracted data
output_file_path = "extracted_values.json"
excel_output_path = "extracted_values.xlsx"  # New Excel output path

# Dictionary to store extracted data from all files
all_extracted_data = {}

# Process each JSON file in the folder
for filename in os.listdir(json_folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(json_folder_path, filename)
        
        try:
            # Load JSON data from the file
            data = load_json_data(file_path)

            # Combine all text into a single string
            all_text = " ".join([data[key]["text"] for key in data])

            # Split text into individual lines
            lines = all_text.splitlines()

            # Extract required values using functions
            invoice_value = extract_invoice_value(data)
            invoice_date = extract_invoice_date(lines)
            invoice_number = process_invoice_number(lines)
            particular_item = process_particular_item(lines)

            # Store the extracted values for the current file
            all_extracted_data[filename] = {
                "Invoice Value": invoice_value,
                "Invoice Number": invoice_number,
                "Invoice Date": invoice_date,
                "Item Particular": particular_item
            }

            print(f"Processed {filename} successfully.")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

# Save all extracted data to a JSON file
with open(output_file_path, "w") as f:
    json.dump(all_extracted_data, f, indent=4)

print(f"\nAll extracted values saved to '{output_file_path}'.")

# Convert extracted data to a DataFrame and export it to Excel
df = pd.DataFrame.from_dict(all_extracted_data, orient='index')
df.reset_index(inplace=True)
df.columns = ['Item', 'Invoice Value', 'Invoice Number', 'Invoice Date', 'Item Particular']

# Save DataFrame to Excel
df.to_excel(excel_output_path, index=False)
print(f"Data has been exported to Excel: {excel_output_path}")


