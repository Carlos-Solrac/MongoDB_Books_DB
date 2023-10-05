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
import pprint


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

    #  1) Using find you must display all items in your collection to the screen (2 points)
    print("1) Using find you must display all items in your collection to the screen")
    record = book_col.find({}, {'_id': 0})
    display_record(record)

    # 2) Create a find that using a  $lt (2 points)
    print("\n2) Create a find that using a  $lt. Looking for books published before 2000. ")
    record = book_col.find({'year': {'$lt': 2000}}, {'_id': 0})
    display_record(record)

    # 3) Create a find that using a  $gte (2 points)
    print("\n3) Create a find that using a  $gte. Looking for books published after 2000.")
    record = book_col.find({'year': {'$gte': 2000}}, {'_id': 0})
    display_record(record)

    # 4) Create a find that using an  $eq (2 points)
    print("\n4) Create a find that using an  $eq. Looking for books made in 2016.")
    record = book_col.find({'year': {'$eq': 2016}}, {'_id': 0})
    display_record(record)

    # 5) Create a find that using a  $ne (2 points)
    print("\n5) Create a find that using a  $ne. Looking for books NOT authored by JK Rowling. ")
    record = book_col.find({'author': {'$ne': 'J.K. Rowling'}}, {'_id': 0})
    display_record(record)

    # 6) Create a find that using an  $or (2 points)
    print("\n6) Create a find that using an  $or where we're looking for horror or thriller books..")
    record = book_col.find({'$or': [{'metadata.genre': 'Horror'}, {'metadata.genre': 'Thriller'}]}, {'_id': 0})
    display_record(record)

    # 7) Create a find that using an  $and (2 points)
    print("\n7) Create a find that using an  $and. We are looking for books that are fantasy AND have over 400 pages.")
    record = book_col.find({'$and': [{'metadata.genre': 'Fantasy'}, {'metadata.length': {'$gte': 400}}]}, {'_id': 0})
    display_record(record)

    # 8) Create a find that using a  $not (2 points)
    print("\n8) Create a find that using a  $not. Looking for books not authored by JK Rowling.")
    record = book_col.find({'author': {'$not': {'$eq': 'J.K. Rowling'}}}, {'_id': 0})
    display_record(record)

    # 9) Create a find that using an  $exists (2 points)
    print("\n9) Create a find that using an  $exists. Looking if a book by author Christopher Paolini exists.")

    record = book_col.find({'author': 'Christopher Paolini', 'title': {'$exists': True}}, {'_id': 0})
    display_record(record)

    # 10) Create a find that using an $elemMatch (2 points)
    print(
        "\n10) Create a find that using an $elemMatch. We are looking for Horror books with a avg rating grater than "
        "4.5.")
    record = book_col.find({
        'metadata.ratings': {
            '$elemMatch': {
                'genre': 'Horror',
                'average': {'$gt': 4.5}
            }
        }
    })
    display_record(record)

    # 11) Create a statement that using an $inc (2 points)
    print("\n11) Create a statement that using an $inc. We will display a books total rating and increase it by 1 by "
          "increasing the positive ratings by 1..")
    print("Record before increment:")
    record = book_col.find({'ISBN': "9781668002179"}, {'_id': 0})
    display_record(record)

    book_col.update_one({'title': "Fairy Tale"}, {'$inc': {'metadata.ratings.reviews.positive': +1}})
    book_col.update_one({'title': "Fairy Tale"}, {'$inc': {'metadata.ratings.total': +1}})
    print("\nRecord after increment:")
    record = book_col.find({'ISBN': "9781668002179"}, {'_id': 0})
    display_record(record)

    # 12) Create a find using {item: null } null search (2 points)
    print(
        "\n12) Create a find using {item: null } null search. I will change the title of 'Fairy Tale' to null and then "
        "find it.")
    print("Entry after the change to null:")
    # Update the title of Fairy Tale to NULL
    book_col.update_one({'ISBN': "9781668002179"}, {'$set': {'title': None}})

    display_record(record)
    record = book_col.find({'title': {'$type': 'null'}}, {'_id': 0})
    print("Entry after search with null:")
    display_record(record)

    # 13) Create a find using {item: {$exists : false} } null search (2 points)
    print(
        "\n13) Create a find using {item: {$exists : false} } null search. Looking for any entry where the title does "
        "not exists.")
    record = book_col.find({'title': {'$exists': False}}, {'_id': 0})
    display_record(record)

    # 14) Create a find using {item: {$type : 10} } null search (2 points)
    print("\n14) Create a find using {item: {$type : 10} } null search. Looking for the nulled out Fairy Tale book by "
          "Stephen King. ")
    record = book_col.find({'title': {'$type': 10}}, {'_id': 0})
    display_record(record)

    # 15) Create a find that uses projection to limit the results to two fields per document  (2 points)
    print("\n15) Create a find that uses projection to limit the results to two fields per document. Only printing the "
          "authors and publishers. ")
    projection = {'author': 1, 'publisher': 1, '_id': 0}
    record = book_col.find({}, projection)
    display_record(record)


if __name__ == "__main__":
    main()
