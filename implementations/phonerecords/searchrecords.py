import json
import os

# Function to calculate Levenshtein distance with a threshold for early exit
def levenshtein_distance(str1, str2):
    m = len(str1)
    n = len(str2)

    # Create a distance matrix
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Initialize the matrix
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Fill the matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if str1[i - 1] == str2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1,      # Deletion
                           dp[i][j - 1] + 1,      # Insertion
                           dp[i - 1][j - 1] + cost)  # Replacement

    return dp[m][n]

def search_records(json_filename, field_index, search_term):

    # Load JSON data
    json_path = f'./data/{json_filename}.json'  
    if not os.path.exists(json_path):
        print(f"Error: The file {json_filename}.json does not exist in the data folder.")
        return [], []

    try:
        with open(json_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {json_filename}.json.")
        return [], []

    exact_matches = []
    like_matches = []

    # Adjust field_index for one-based indexing
    adjusted_index = field_index - 1  # Convert to zero-based index

    # Define a threshold for fuzzy matching
    threshold = max(1, len(search_term) // 4)

    # Iterate over each record
    for record in data:
        # Get the keys of the record
        keys = list(record.keys())

        # Check if the adjusted index is valid
        if adjusted_index < 0 or adjusted_index >= len(keys):
            print(f"Error: Field index {field_index} is out of bounds.")
            return exact_matches, like_matches

        # Get the value for the specified field using the adjusted field index
        field_value = record.get(keys[adjusted_index])

        # Check for exact match
        if field_value and field_value.lower() == search_term.lower():
            exact_matches.append(record)
            
        # Check for fuzzy match
        elif field_value:
            if search_term.lower() in field_value.lower():
                like_matches.append(record)
            # Levenshtein distance check with threshold
            elif levenshtein_distance(field_value.lower(), search_term.lower()) <= threshold:
                like_matches.append(record)

    return exact_matches, like_matches







