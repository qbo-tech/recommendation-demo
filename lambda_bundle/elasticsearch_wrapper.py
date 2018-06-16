from __future__ import print_function
from pprint import pprint
import boto3
import json
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch import helpers
import csv
import urllib
import json


def connectES(esEndPoint):
 print ('Connecting to the ES Endpoint {0}'.format(esEndPoint))
 try:
  esClient = Elasticsearch(
   hosts=[{'host': esEndPoint, 'port': 443}],
   use_ssl=True,
   verify_certs=True,
   connection_class=RequestsHttpConnection)
  return esClient
 except Exception as E:
  print("Unable to connect to {0}".format(esEndPoint))
  print(E)
  exit(3)


def createIndex(esClient, indexName):
 try:
  res = esClient.indices.exists(indexName)
  print("Index Exists ... {}".format(res))
  if res is False:
   esClient.indices.create(indexName, body=indexDoc)
   return 1
 except Exception as E:
  print("Unable to Create Index {0}".format(indexName))
  print(E)
  exit(4)

def indexBulkCsv(esClient, indexName, bucket, key):
  s3_client = boto3.client('s3')
  tmp_download_file = '/tmp/{}{}'.format(uuid.uuid4(), key)
  s3_client.download_file(bucket, key, tmp_download_file)
  with open(tmp_download_file) as f:
      reader = csv.DictReader(f, encoding='utf-8')
      for success, info in helpers.parallel_bulk(es, reader, thread_count=8, chunk_size=500, index=indexName, doc_type=<yourdoctype>, request_timeout=30):
          if not success: 
            print('Doc failed', info) 
            exit(4)

