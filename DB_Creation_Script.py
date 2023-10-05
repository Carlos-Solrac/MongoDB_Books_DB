"""

Name:Carlos Cuellar Benitez
Date: 2/27/2023
Assignment: 8 Document Store Search Script and App
Due Date:03/12/2023
About this project: Complete three different scripts to show proficiency in searching a mongoDB, using a index search,
 and incorporating both into the  Document App from assignment 7.
Assumptions: assumes correct user input
All work below was performed by Carlos Cuellar Benitez

"""

from pymongo import MongoClient
import pandas as pd

# Connection to MongoDB
client = MongoClient("mongodb://localhost:27017/")
# drop database if it already exits
client.drop_database('Literature')
# Create books database
BooksDB = client['Literature']
# create books collection
colBooks = BooksDB['Books']

myList = [
    {
        "title": "Fairy Tale",
        "author": "Stephen King",
        "publisher": "Scribner",
        "year": 2021,
        "price": 25.99,
        "ISBN" : "9781668002179",
        "metadata": {
            "genre": "Horror",
            "length": 563,
            "ratings": {
                "total": 50,
                "average": 4.2,
                "reviews": {
                    "positive": 40,
                    "neutral": 8,
                    "negative": 2
                }
            }
        }
    },
    {
        "title": "Harry Potter and the Philosopher's Stone",
        "author": "J.K. Rowling",
        "publisher": "Bloomsbury",
        "year": 1997,
        "price": 10.99,
        "ISBN": "9780747532743",
        "metadata": {
            "genre": "Fantasy",
            "length": 223,
            "ratings": {
                "total": 100,
                "average": 4.8,
                "reviews": {
                    "positive": 95,
                    "neutral": 3,
                    "negative": 2
                }
            }
        }
    },
    {
        "title": "Harry Potter and the Chamber of Secrets",
        "author": "J.K. Rowling",
        "publisher": "Bloomsbury",
        "year": 1998,
        "price": 11.99,
        "ISBN": "9780747538486",
        "metadata": {
            "genre": "Fantasy",
            "length": 251,
            "ratings": {
                "total": 95,
                "average": 4.7,
                "reviews": {
                    "positive": 90,
                    "neutral": 3,
                    "negative": 2
                }
            }
        }
    },
    {
        "title": "Harry Potter and the Prisoner of Azkaban",
        "author": "J.K. Rowling",
        "publisher": "Bloomsbury",
        "year": 1999,
        "price": 12.99,
        "ISBN": "9780747542155",
        "metadata": {
            "genre": "Fantasy",
            "length": 317,
            "ratings": {
                "total": 98,
                "average": 4.9,
                "reviews": {
                    "positive": 95,
                    "neutral": 2,
                    "negative": 1
                }
            }
        }
    },
    {
        "title": "Harry Potter and the Goblet of Fire",
        "author": "J.K. Rowling",
        "publisher": "Bloomsbury",
        "year": 2000,
        "price": 13.99,
        "ISBN": "9780747546245",
        "metadata": {
            "genre": "Fantasy",
            "length": 636,
            "ratings": {
                "total": 99,
                "average": 4.7,
                "reviews": {
                    "positive": 92,
                    "neutral": 6,
                    "negative": 1
                }
            }
        }
    },

    {
        "title": "Harry Potter and the Order of Phoenix",
        "author": "J.K. Rowling",
        "publisher": "Bloomsbury",
        "year": 2003,
        "price": 15.99,
        "ISBN": "9780747551003",
        "metadata": {
            "genre": "Fantasy",
            "length": 766,
            "ratings": {
                "total": 98,
                "average": 4.6,
                "reviews": {
                    "positive": 89,
                    "neutral": 7,
                    "negative": 2
                }
            }
        }
    },
    {
        "title": "Harry Potter and the Half-Blood Prince",
        "author": "J.K. Rowling",
        "publisher": "Bloomsbury",
        "year": 2005,
        "price": 16.99,
        "ISBN": "9780747581081",
        "metadata": {
            "genre": "Fantasy",
            "length": 607,
            "ratings": {
                "total": 97,
                "average": 4.8,
                "reviews": {
                    "positive": 92,
                    "neutral": 4,
                    "negative": 1
                }
            }
        }
    },
    {
        "title": "Harry Potter and the Deathly Hallows",
        "author": "J.K. Rowling",
        "publisher": "Bloomsbury",
        "year": 2007,
        "price": 18.99,
        "ISBN": "9780545010221",
        "metadata": {
            "genre": "Fantasy",
            "length": 607,
            "ratings": {
                "total": 99,
                "average": 4.9,
                "reviews": {
                    "positive": 95,
                    "neutral": 3,
                    "negative": 1
                }
            }
        }
    },
    {
        "title": "Fantastic Beasts and Where to Find Them",
        "author": "Newt Scamander (J.K. Rowling)",
        "publisher": "Arthur A. Levine Books",
        "year": 2001,
        "price": 15.99,
        "ISBN": "9781338132311",
        "metadata": {
            "genre": "Fantasy",
            "length": 128,
            "ratings": {
                "total": 67,
                "average": 4.5,
                "reviews": {
                    "positive": 61,
                    "neutral": 5,
                    "negative": 1
                }
            }
        }
    },
    {"title": "Harry Potter and the Cursed Child",
     "author": ["J.K. Rowling", "John Tiffany", "Jack Thorne"],
     "publisher": "Arthur A. Levine Books",
     "year": 2016,
     "price": 29.99,
     "ISBN": "9781338216660",
     "metadata": {
         "genre": "Fantasy",
         "length": 336,
         "ratings": {
             "total": 75,
             "average": 3.4,
             "reviews": {
                 "positive": 39,
                 "neutral": 12,
                 "negative": 24
                }
            }
         }
     },
    {
        "title": "Quidditch Through the Ages",
        "author": "Kennilworthy Whisp (J.K. Rowling)",
        "publisher": "Arthur A. Levine Books",
        "year": 2001,
        "price": 12.99,
        "ISBN": "9780545850582",
        "metadata": {
            "genre": "Fantasy",
            "length": 56,
            "ratings": {
                "total": 43,
                "average": 4.1,
                "reviews": {
                    "positive": 36,
                    "neutral": 6,
                    "negative": 1
                }
            }
        }

    }
]

colBooks.insert_many(myList)
# Print list of the _id values of the inserted docts
records = colBooks.find({}, {'_id': 0})
# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(list(records))
# Display the dataFrame as a table
print(df.to_string(index=False, justify='center'))
# close connection
client.close()
