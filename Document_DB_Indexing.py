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
import pymongo
from pymongo import MongoClient
import pandas as pd


def display_record(collectionRecord):
    # Convert the records to a pandas DataFrame.
    df = pd.DataFrame(list(collectionRecord))
    # Display the DataFrame.
    if not df.empty:
        print(df.to_string(index=False, justify='center'))
    else:
        print("No book(s) exists in the collection matching the search query.")


def main():
    # Provide the mongoDB atlas url to connect python to mongodb using pymongo
    # Blank in our case as it will be local. Can always be updated as needed.
    CONNECTION_STRING = "mongodb://localhost:27017/"

    # Create a connection using MongoClient.
    client = MongoClient(CONNECTION_STRING)
    # Statically assign database to be used.
    literature_db = client.get_database('Literature')
    # Statically assign collection to be used.
    book_col = literature_db.get_collection('Books')

    # 1) Create a find that does not use an index (2 points) (aka step 1)
    print("1. Create a find that does not use an index ")
    record = book_col.find({'ISBN': '9780545850582'}, {'_id': 0}).hint(None)
    display_record(record)
    # 2) Use the Explain to show that no index is used when running the find from step 1 (2 points)+
    print("\n2. Use the Explain to show that no index is used when running the find from step 1. Looking for 'stage': "
          "'COLLSCAN' ")
    record = book_col.find({'ISBN': '9780545850582'}).explain()
    print(record)

    # 3) Add an index that will be used when running the find from step 1 (2 points)
    print("\n3. Add an index that will be used when running the find from step 1")
    # Create an index for the ISBN attribute.
    print("Before adding an index:")
    for index in book_col.list_indexes():
        print(index)
    book_col.create_index("ISBN")
    print("After adding an index:")
    for index in book_col.list_indexes():
        print(index)
    record = book_col.find({'ISBN': '9780545850582'}, {'_id': 0}).hint('ISBN_1')
    display_record(record)

    # 4) Use the Explain to show that an index is now used when running the find from step 1 (2 points)
    print("\n4. Use the Explain to show that an index is now used when running the find from step 1."
          "Looking for 'stage': 'IXSCAN' and 'ISBN_1'.")
    record = book_col.find({'ISBN': '9780545850582'}).explain()
    print(record)

    # 5) Drop the index you created in step 3 (2 points)
    print("\n5. Drop the index you created in step 3, \nBefore:")
    for index in book_col.list_indexes():
        print(index)
    book_col.drop_index("ISBN_1")
    print("\nAfter drop:")
    for index in book_col.list_indexes():
        print(index)


if __name__ == "__main__":
    main()
