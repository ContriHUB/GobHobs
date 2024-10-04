# 🧙‍♂️ GobHobs - The Goblin Data Extractor 🧙‍♀️

**Welcome to GobHobs, the goblin-themed data extraction tool!** In the world of goblins, there’s one thing they excel at—looting and extracting valuable information. Inspired by their relentless pursuit of treasures, **GobHobs** is here to help you “extract” data from multiple sources and organize it in ways only a goblin would dream of!

### The Story of GobHobs:
Once upon a time, a mischievous goblin stumbled upon an ancient library filled with data. From legal PDFs to phone records and web search results, it was all too much for even the greediest goblin to process. But this goblin was no ordinary thief—he wanted **all the data** and to process it intelligently, organizing it for future "plunders."

Thus, **GobHobs** was born—a magical tool that allows you to:
1. Extract and structure data from **PDFs** (loot the precious structured data).
2. Search and manage **phone records** (sneaky, sneaky goblin-style investigation).
3. **Scrape the web** and organize it based on your needs (goblin-grade web-looting).

But there’s a twist—the goblin leaves some work for **you** to do! You can implement the brains of the goblin's operations in either **Python (.py)** or **JavaScript (.js)**. Let’s dive in!

---

## 🛠️ Project Structure
**GobHobs** is divided into three microservices:
1. **PDF Extractor**: Extract structured data from PDF files and convert it into JSON format.
2. **Phone Records**: Manage and search phone records by converting CSV data into JSON and performing complex searches.
3. **Web Scraping**: Scrape data from web pages and order it based on relevance or user-defined criteria.

Each microservice provides the option to implement functionality in either **Python (.py)** or **JavaScript (.js)**, giving you the freedom to choose based on your expertise.

---

## 🎯 What You Need to Do
### Implement the following microservices:
1. **PDF Extractor**:
   - Extract tables, key-value pairs, or any structured data from a PDF file.
   - Save the data as a JSON file.
   - You can implement this in either `extractfrompdf.py` or `extractfrompdf.js`.

2. **Phone Records**:
   - Convert phone records from CSV format to JSON.
   - Implement a smart search function to find exact and approximate matches (goblins love finding hidden treasures).
   - You can implement this in `searchrecords.py` or `searchrecords.js`.

3. **Web Scraping**:
   - Scrape the web based on a query provided by the user.
   - Implement functionality to order and rank the results.
   - You can implement this in `ordering.py` or `ordering.js`.

---

## 💻 How to Use GobHobs
To unleash the goblin magic, follow these steps:

### 1. Install Dependencies
Ensure you have both **Python** and **Node.js** installed on your system. Then, install the necessary Python dependencies by running:

```bash
pip install -r requirements.txt
```

### 2.  Run the Frontend CLI
Navigate to the frontend folder and run the Goblin command-line interface (CLI) using:

```bash
cd frontend
python shell_script.py
```

### 3. Run the backend file 
Navigate to the backend directory and run the backend file 

```bash
cd backend
python app.py
```

### 4. using the frontend cli application
You can use the ferontend cli using the commands by typing a help keyword and seeing the command and its usage

## 🎥 Video Tutorial

Watch the video tutorial below to get a complete walkthrough of how to set up and implement each microservice within **GobHobs**. The video covers:

1. Installing dependencies.
2. Running the frontend CLI and backend API.
3. Using the GobHobs CLI for PDF extraction, phone record searching, and web scraping.
4. Implementing your custom logic in Python or JavaScript for each microservice.

**[Click here to watch the full video walkthrough](https://www.example.com/your-video-link)**

---

## 🛠️ How to Pull the Code and Make Changes on a New Branch

Follow these steps to pull the code, make your own changes, and create a new branch:

### 1. Clone the Repository
First, clone the repository to your local machine using Git:

```bash
git clone https://github.com/your-username/GobHobs.git
```

### 2. navigate to the Project directory 
```bash
cd GobHobs
```

### 3. Create your own branch 
```bash
git checkout -b your-feature-branch
```

### 4. Make changes and commit and raise a PR
```bash
git add .
git commit -m "change-mentioned"
git push origin your-feature-branch-name



---

## 🎉 All the Best & Happy Coding! 🎉

Thank you for joining the **GobHobs** adventure! We hope you enjoy working on this project as much as the goblins enjoy looting and extracting data.

Whether you're mastering the art of **PDF extraction**, building intelligent **search algorithms** for phone records, or crafting the perfect **web scraping and ranking** logic, the goblins are always watching your progress with excitement. 🧙‍♂️✨

Remember, this project is all about improving your skills in:
- Data extraction.
- Algorithm building.
- Smart searching.
- Web scraping.

Feel free to customize, improve, and make this project your own! The goblins can’t wait to see what you’ll do next.

**Good luck, and happy coding!** 💻💡🧙‍♀️



