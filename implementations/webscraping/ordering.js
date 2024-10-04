const fs = require('fs');
const path = require('path');

function orderJsonByKeywords(jsonFile, keywords) {
    /**
     * Orders the entries in the provided JSON file based on the presence of keywords.
     *
     * @param {string} jsonFile - Name of the JSON file (without path).
     * @param {Array} keywords - List of keywords to use for ordering.
     * @returns {Array} - Ordered JSON data.
     */

    // Construct the full path to the JSON file in the data folder
    const dataFolder = path.join(__dirname, 'data');
    const jsonPath = path.join(dataFolder, jsonFile);

    // Check if file exists
    if (!fs.existsSync(jsonPath)) {
        console.log(`File ${jsonFile} not found in the data folder.`);
        return [];
    }

    // Load the JSON data from the file
    const data = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));

    // Placeholder for ordering logic
    // Implement logic to order the data based on the provided keywords

    return data;
}

if (process.argv.length < 4) {
    console.log("Usage: node ordering.js <json_file> <keyword1> <keyword2> ...");
    process.exit(1);
}

const jsonFile = process.argv[2] + '.json';  // Assume the file is given without an extension
const keywords = process.argv.slice(3);

const orderedData = orderJsonByKeywords(jsonFile, keywords);

// Print or
