"""
You need install next packages before execute

$ pip install langchain-openai
$ pip install langchain


Install patched version of `langchain` package:

$ git clone https://github.com/OpenLinkSoftware/langchain.git
$ cd langchain/libs/community/
$ pip install -e .

"""
import os
os.environ["OPENAI_API_KEY"] = "{YOUR-OPENAI-API-KEY}"

from langchain_openai import ChatOpenAI
from langchain_community.graphs import RdfGraph
from langchain.chains import GraphSparqlQAChain

graph = RdfGraph(query_endpoint="https://dbpedia.org/sparql")

#graph = RdfGraph(
#   query_endpoint="https://dbpedia.org/sparql",
#    standard="rdf",
#    local_copy="test.ttl"
#)

chain = GraphSparqlQAChain.from_llm(
    ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0, verbose=True), graph=graph, verbose=True
#    ChatOpenAI(model="gpt-4-0125-preview", temperature=0, verbose=True), graph=graph, verbose=True
)

query = """
Relevant DBpedia Knowledge Graph relationship types (relations):
  ?movie rdf:type dbo:Film .
  ?movie dbo:director ?name .

Associated namespaces:
 dbr:  <http://dbpedia.org/resource/>
 dbo:  <http://dbpedia.org/ontology/>
 rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

List movies by Spike Lee
"""

res = chain.invoke({chain.input_key: query})[chain.output_key]

print(res)
 