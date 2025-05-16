import os

from langchain_openai import ChatOpenAI

from langchain_community.graphs.rdf_graph import RdfGraph
from langchain_community.chains.graph_qa.sparql import GraphSparqlQAChain


os.environ["OPENAI_API_KEY"] = "{YOUR-OPENAI-API-KEY}"


# 1) Instantiate the RDF graph against DBpedia
graph = RdfGraph(
    query_endpoint="https://dbpedia.org/sparql",
    # you can still pass `standard="rdf"` or a local TTL copy if you like
)

# 2) Build the QA chain from the ChatOpenAI wrapper
chain = GraphSparqlQAChain.from_llm(
    llm=ChatOpenAI(model_name="gpt-4o",  # or "gpt-4" if you have access
                    temperature=0.0, verbose=True),
        graph=graph,
        allow_dangerous_requests=True,
)

# 3) Define and run your query
query = """
Relevant DBpedia Knowledge Graph relationship types (relations):
  ?movie rdf:type dbo:Film .
  ?movie dbo:director ?name .

Associated namespaces:
  dbr:  <http://dbpedia.org/resource/>
  dbo:  <http://dbpedia.org/ontology/>
  rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

List movies by Spike Lee.
"""

question = "List all films directed by Spike Lee."

result = chain.invoke({"query": query})
print(result["result"])
