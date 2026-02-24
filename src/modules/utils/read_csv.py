import csv

# Define the path to your CSV file
csv_file_path = 'src\inputs.csv'

# Initialize an empty list to hold the rows
rows_list = []

# Read the CSV file
with open(csv_file_path, mode='r', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    
    # Skip the header if needed
    header = next(csvreader)  # Uncomment this line if you want to skip the header

    # Append each row to the list
    for row in csvreader:
        rows_list.append(row)
    flattened_list = [item[0] for item in rows_list]

# Display the list of rows
print(flattened_list)
