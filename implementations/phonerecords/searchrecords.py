import json
import os

def search_records(json_filename, field_index, search_term):
    """
    Search for records in the specified JSON file.

    Parameters:
    - json_filename (str): The name of the JSON file (without extension) to search in.
    - field_index (int): The field index to search in (e.g., 1 for name).
    - search_term (str): The search term or keyword.

    Returns:
    - exact_matches (list): A list of exact matches (currently empty).
    - like_matches (list): A list of like/suggestive matches (currently empty).
    """

    # TODO: Implement actual search logic
    exact_matches = []
    like_matches = []

    return exact_matches, like_matches
