
from pymongo import MongoClient
import sys

__author__ = 'stephane mbatchou'


'''
this script look at the database and remove the lowest homework score for each student

'''
# establish a connection to the database
connection = MongoClient()
db = connection.school
students = db.students


def removeLowest():
    print "retrieving scores document"

    try:
        cur = students.find({"scores.type": "homework"})
        for doc in cur:
            # retrieve scores list
            scores = doc['scores']
            print "before:-> ",scores
            lowestHomework = findLowest(scores)

            #remove the lowest homework doc from scores list
            scores.remove(lowestHomework)
            print "after:-> ", scores,'\n'

            #update the document in the collection with the new scores
            id = doc['_id']
            students.update({"_id":id},{"$set":{"scores": scores}})


    except:
        print "Unexpected error:", sys.exc_info()[0]

    connection.close()


def findLowest(scores):
    MIN = sys.maxsize

    for doc in scores:
        if doc['type'] == 'homework' and doc['score'] < MIN:
            MIN = doc['score']
            removableDoc = doc

    return removableDoc


def main():
    removeLowest()

if __name__ == "__main__":
    main()

