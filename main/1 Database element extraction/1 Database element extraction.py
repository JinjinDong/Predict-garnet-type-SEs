import pandas as pd
import re

file_path = 'file'
df = pd.read_excel(file_path)
chemical_column = df.iloc[:, 0]

# Extract the first element
def extract_first_element(chemical_formula):
    if not isinstance(chemical_formula, str):
        return ''
    matches = re.findall(r'([A-Z][a-z]*)(\d*)', chemical_formula)
    if matches:
        first_element = matches[0][0]
        return first_element
    return ''

# Apply function and create new column
df['First element'] = chemical_column.apply(extract_first_element)

# Save the modified DataFrame to a new.xlsx file
output_file_path = 'file'
df.to_excel(output_file_path, index=False)