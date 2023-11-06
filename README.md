# Flask NER app

An API that where the POSTed JSON payload should comprise:
- a URL (which will return a text file when dereferenced) with key "URL"
- One or more metadata fields with unknown keys

The API should return a JSON object, where the function of the API is to:
1. Fetch the text at the URL key
2. Identify all of the people in the document
3. Sort the people by the number of times the person's name appears in the document
4. For each person:
   - create a list of places that are associated with that person in the document (that is, where the place appears within 100 words either side of the person's name)
   - sort the list of places by the number of times that place appears with that person
5. return any metadata fields sent in the initial request unchanged


Example request

    {"URL": "https://www.gutenberg.org/cache/epub/345/pg345.txt", "author": "Bram Stoker", "title": "Dracula"}


Example return:

    {
        "url": "https://www.gutenberg.org/cache/epub/345/pg345.txt",
        "title": "Dracula",
        "author": "Bram Stoker",
        "people": [{
                "name": "Jonathan Harker",
                "count": 8,
                "associated_places": [{
                    "name": "Munich",
                    "count": 2
                }, {
                    "name": "Bucharest",
                    "count": 1
                }]
            },
            {
                "name": "Professor Van Helsing",
                "count": 2,
                "associated_places": [{
                    "name": "London",
                    "count": 1
                }, {
                    "name": "Cambridge",
                    "count": 1
                }]
            }
        ]
    }

## To run
Download the Spacy English model with the following command line
    
    python -m spacy download en

To send requests to the Flask app

    curl -X POST -H "Content-Type: application/json" -d '<example request json>' http://127.0.0.1:5000/process_json

