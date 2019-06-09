import requests, json, os
from pprint import pprint
from elasticsearch import Elasticsearch, helpers
import logging


# Simple search function for elastic search
def search(es_object, index_name, search):

    res = es_object.search(index=index_name, body=search)
    pprint(res)

# Function for creating index in Elastic Search
def createIndex(es, index_name, type_name):

    doc = {

        index_name:{

            type_name:{

                "properties":{

                    "name":{"type": "string"},
                    "neighborhood":{"type": "string"},
                    "photograph":{"type": "string"},
                    "address":{"type": "string"},
                    "latlng":{"lat": {"type": "numeric"},"lng": {"type": "numeric"},},
                    "cuisine_type":{"type": "string"},
                    "operating_hours":{"Monday": {"type": "string"},"Tuesday": {"type": "string"},"Wednesday": {"type": "string"},
                                       "Thursday": {"type": "string"},"Friday": {"type": "string"},"Saturday": {"type": "string"},
                                       "Sunday": {"type": "string"},
                    },
                    "reviews":[{
                        "name":{"type": "string"},
                        "date": {"type": "string"},
                        "rating": {"type": "numeric"},
                        "comments": {"type": "string"}
                    }]
                }
            }
        }
    }

    res = es.index(index=index_name, doc_type=type_name, body=doc)
    print(res['result'])
    return es

# Establish connection to elastic search and returns ES object
def connectElasticSearch():

    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    #es.indices.create(index='restaurant')

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
                es.index(index='restaurant', ignore=400, id=i, body=json.loads(docket_content))
                print('Data indexed successfully')
                i = i+1

    return es

if __name__ == '__main__':

    es = connectElasticSearch()
    es = createIndex(es,"restaurant","fastfood")

    storeElasticSearch(es)

    # Search all the records in ES to find name equals Roberta's Pizzax
    #search(es, 'restaurant', json.dumps({'query': {'match': {'name': 'Roberta}\'s Pizza'}}}))

