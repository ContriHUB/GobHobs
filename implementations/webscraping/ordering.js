const fs = require('fs');
const path = require('path');

function orderJsonByKeywords(jsonFile, keywords, outputFilePath) {
    //implement the logic here
}

if (process.argv.length < 5) {
    console.log("Usage: node ordering.js <json_file> <keyword1> <keyword2> ... <output_file>");
    process.exit(1);
}

const jsonFile = process.argv[2];
const keywords = process.argv.slice(3, -1); // Keywords
const outputFilePath = process.argv[process.argv.length - 1]; // Output file path

orderJsonByKeywords(jsonFile, keywords, outputFilePath);
