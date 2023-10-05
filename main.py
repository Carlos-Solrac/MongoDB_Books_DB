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
import datetime
import random

from pymongo import MongoClient
import pandas as pd

# Provide the mongoDB atlas url to connect python to mongodb using pymongo
# Blank in our case as it will be local. Can always be updated as needed.
CONNECTION_STRING = "mongodb://localhost:27017/"

# Create a connection using MongoClient.
client = MongoClient(CONNECTION_STRING)
# Statically assign database to be used.
literature_db = client.get_database('Literature')
# Statically assign collection to be used.
book_col = literature_db.get_collection('Books')


def display_menu():
    print("Main Menu")
    print("A) Add a book.")
    print("B) Update book in an existing book database.")
    print("C) Display All books in database.")
    print("D) Display a specific book.")
    print("E) Delete a specific book.")
    print("Q) Quit")


def get_user_choice():
    while True:
        option = input("Enter your choice: ").strip().upper()
        if option in ['A', 'B', 'C', 'D', 'E', 'Q']:
            return option
        else:
            print("Invalid choice. Please try again.")


def set_book():
    # set book info
    title = input("Enter book title: ")
    author = input("Enter the author name: ")
    publisher = input("Enter the publisher name: ")

    while True:
        try:
            isbn = input("Enter the book ISBN number without dashes: ")
            if not isbn.isspace() and isbn.isnumeric() and len(isbn) == 13:
                break
            else:
                print("Invalid input! Please enter a valid 13-digit ISBN number without dashes.")
        except ValueError:
            print("Invalid input! Please enter a valid book ISBN number without dashes..")

    while True:
        try:
            # Assign the current year to ensure books are not incorrectly stated as published in the future or before 0.
            today = datetime.datetime.now()
            year_today = today.year
            year = int(input("Enter the publication year: "))
            if 0 < year <= year_today:
                break
        except ValueError:
            print("Invalid input! Please enter a valid year.")
    num_of_reviews = 3.0
    length = random.randint(100, 600)
    price = random.uniform(10.00, 50.00)
    genre_list = ["Fantasy", "Horror","Thriller"]
    genre = random.choice(genre_list)
    positive_review = random.randint(0, 80)
    neutral_review = random.randint(0, 100)
    negative_review = random.randint(0, 20)
    ratings_total = positive_review + neutral_review + negative_review
    ratings_avg = ratings_total / num_of_reviews

    # Create a dictionary of the book information to add to the database collection.

    book = {
        "title": title,
        "author": author,
        "publisher": publisher,
        "year": year,
        "price": price,
        "metadata": {
            "genre": genre,
            "length": length,
            "ratings": {
                "total": ratings_total,
                "average": ratings_avg,
                "reviews": {
                    "positive": positive_review,
                    "neutral": neutral_review,
                    "negative": negative_review
                }
            }
        }
        ,
        "ISBN": isbn
    }
    # insert validation.
    try:
        result = book_col.insert_one(book)
        print("Book added successfully.\n")
    except Exception as e:
        print(f"Error adding book", e)


def update_book():
    # Allow the user to enter in a value for the unique attribute in the collection
    genre = ""
    length = 0
    total_ratings = 0.0
    avg_ratings = 0.0
    positive_review = 0
    neutral_review = 0
    negative_review = 0
    review_types = 3.0

    # Search db by isbn value, return an error if the value is not in the database.
    target = str(input("Search for a book by ISBN, only input numbers, no dash ( - ). \n"))
    record = book_col.find_one({'ISBN': target})
    if record:
        # metadata holds our 3 subtypes with ratings having another set of subtypes.
        metadata = record['metadata']

        print("Current genre:", metadata['genre'])
        while True:
            try:
                genre = input("Enter in new genre value: ")
                if len(genre) > 0 and not genre.isspace() and not genre.isnumeric():
                    break
            except ValueError:
                print("Invalid input! Please enter a valid number.")

        print("Current length:", metadata['length'])
        while True:
            try:
                length = int(input("Enter in new length value: "))
                if length > 0:
                    break
            except ValueError:
                print("Invalid input! Please enter a valid number.")

        # the total ratings and avg ratings are calculated from the number of positive, neutral, and negative reviews.
        # Thus, not only are these needed to calculate total_ratings and avg_ratings, but they must also be updated in
        # the document housing the book information.
        print("Current total ratings:", metadata['ratings']['total'])
        print("In order to update the total and average ratings you must provide the new number of positive, neutral, "
              "and negative reviews:")
        while True:
            try:
                positive_review = int(input("Enter in the new number of positive reviews: "))
                neutral_review = int(input("Enter in the new number of neutral reviews: "))
                negative_review = int(input("Enter in the new number of negative reviews: "))
                if positive_review > 0 and neutral_review > 0 and negative_review > 0:
                    break
            except ValueError:
                print("Invalid input! Please enter a valid number.")
        total_ratings = positive_review + neutral_review + negative_review
        avg_ratings = total_ratings / review_types
    else:
        print("Error: Book not found.")

    # Update the book metadata (Sub type attributes)
    book_col.update_one(
        {'ISBN': target},
        {
            '$set': {
                'metadata.genre': genre,
                'metadata.length': length,
                'metadata.ratings.total': total_ratings,
                'metadata.ratings.average': avg_ratings,
                'metadata.ratings.reviews.positive': positive_review,
                'metadata.ratings.reviews.neutral': neutral_review,
                'metadata.ratings.reviews.negative': negative_review
            }
        }
    )
    print("Book updated successfully!")


def display_books_in_db():
    # display all books in the db using pandas to create a table.
    records = book_col.find({}, {'_id': 0})
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(list(records))
    # Display the dataFrame as a table
    print(df.to_string(index=False))


def display_specific_book():
    # display a particular db entry with some identifier.
    while True:
        try:
            target = str(input("Search for a book by ISBN, only input numbers, no dash ( - ). \n"))
            if not target.isspace() and target.isnumeric() and len(target) == 13:
                break
            else:
                print("Invalid input! Please enter a valid 13-digit ISBN number without dashes.")
        except ValueError:
            print("Invalid input! Please enter a valid book ISBN number without dashes..")

    record = book_col.find_one({'ISBN': target}, {'_id': 0})
    if record:
        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame([record])
        # Display the dataFrame as a table without an index.
        print(df.to_string())

    else:
        print(f"No record found with ISBN '{target}' ")


def delete_specific_book():
    # display a particular db entry with some identifier.
    while True:
        try:
            target = str(input("Search for a book by ISBN, only input numbers, no dash ( - ). \n"))
            if not target.isspace() and target.isnumeric() and len(target) == 13:
                break
            else:
                print("Invalid input! Please enter a valid 13-digit ISBN number without dashes.")
        except ValueError:
            print("Invalid input! Please enter a valid book ISBN number without dashes..")
    record = book_col.delete_one({'ISBN': target})
    if record:
        print("Book successfully removed.\n")
    else:
        print("Book not found. Not removed.\n")


# Menu option for program
while True:
    display_menu()
    choice = get_user_choice()
    if choice == 'A':
        print("You chose 'Add a book.'")
        set_book()
    elif choice == 'B':
        print("You chose 'Update book in an existing book database.'")
        update_book()
    elif choice == 'C':
        print("You chose 'Display All books in database.'")
        display_books_in_db()
    elif choice == 'D':
        print("You chose 'Display a specific book.'")
        display_specific_book()
    elif choice == 'E':
        print("You chose 'Delete a specific book.'")
        delete_specific_book()
    elif choice == 'Q':
        print("You chose 'Quit', goodbye!")
        break
