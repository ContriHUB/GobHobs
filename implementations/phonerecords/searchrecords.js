const fs = require('fs');
const path = require('path');

function searchRecords(jsonFilename, fieldIndex, searchTerm) {
    /**
     * Search for exact and like/suggestive matches in the specified JSON file.
     * 
     * Parameters:
     * - jsonFilename (String): The name of the JSON file (without extension) to search in.
     * - fieldIndex (Number): The index of the field to search in (e.g., 1 for name, 2 for address).
     * - searchTerm (String): The search term or keyword.
     * 
     * Returns:
     * - An object containing exactMatches and likeMatches arrays.
     */

    // TODO: Participants will implement the actual search logic here

    // Returning empty lists for now
    const exactMatches = [];
    const likeMatches = [];

    // Return the matches as an object
    return { exactMatches, likeMatches };
}

// Command-line arguments handling
if (require.main === module) {
    const jsonFilename = process.argv[2];
    const fieldIndex = parseInt(process.argv[3]);
    const searchTerm = process.argv[4];

    const result = searchRecords(jsonFilename, fieldIndex, searchTerm);
    console.log(JSON.stringify(result));  // Output the result as a JSON string
}

module.exports = { searchRecords };
