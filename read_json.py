import json
import os
import sys

from pprint import pprint

import ijson
import requests
from elasticsearch import Elasticsearch, helpers




#   helpers.bulk(es, load_json(sys.argv[1]), index='MR', body=json.loads(docket_content))


def search(es, index_name, name, value):
    """Simple Elasticsearch Query"""
    query = json.dumps({
        "query": {
            "match": {
                 name: value
            }
        }
    })
    res = es.search(index=index_name, body=query)
    pprint(res['hits']['hits'])
    pprint(res)


def format_results(results):
    """Print results nicely:
    doc_id) content
    """
    data = [doc for doc in results['hits']['hits']]
    for doc in data:
        print("%s) %s" % (doc['_id'], doc['_source']['content']))


def create_doc(uri, doc_data={}):
    """Create new document."""
    query = json.dumps(doc_data)
    response = requests.post(uri, data=query)
    print(response)




    # create_doc(uri_create, {"content": "The fox!"})
    # results = search(uri_search, "fox")
    # format_results(results)


def searchFullText(es, index_name, name, value):
    search_body = {'query':
                       {'match':
                            {name: value}
                        }
                   }

    res = es.search(index=index_name, body=search_body)
    pprint(res['hits']['hits'])
    pprint(res)


def searchByIndex(es_object,index_name,type, id):
    res = es_object.get(index=index_name,doc_type=type,id=id)
    pprint(res)



# Function for creating index in Elastic Search
def createIndex(es, index_name,type_name):
    doc = {

        index_name: {

            type_name: {

                "properties": {
                    "vr": {"type": "string"},
                    "Value": {"type": "string"},




                }
            }
        }
    }

    res = es.index(index=index_name,doc_type=type_name,body=doc)
    print(res['result'])
    return es


# Establish connection to elastic search and returns ES object
def connectElasticSearch():
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}], sniff_on_start=True)
    # es.indices.create(index='MR')

    # returns true if connection is successful
    if es.ping():
        print('Elasticsearch connected')
    else:
        print('Elasticsearch could not connect!')

    return es


# Search for JSON files in cwd and store JSON files in Elastic Search
def storeElasticSearch(es):
    i = 1
    if es is not None:
        for filename in os.listdir(os.getcwd()):
            if filename.endswith(".json"):
                f = open(filename)
                docket_content = f.read()

                # Send the data into es
                es.index(index='mr', ignore=400, id=i, body=json.loads(docket_content))
                print('Data indexed successfully')
                i = i + 1

    return es


if __name__ == '__main__':
    es = connectElasticSearch()

    es = storeElasticSearch(es)
    createIndex(es, "mr","_doc")



    es.indices.refresh(index="mr")


    search(es,"mr","vr","TM")

    #results = search(uri_search, "CS")


    searchByIndex(es,"mr","_doc", 5)

    # searchByIndex(es,"mr",1)
    #format_results(search("mr","2"))


    # searchForMatch(es, "restaurant", "neighborhood", "Manhattan")

    #searchFullText(es, "mr",'vr','SH')
    # function("es","mr",'CS')


