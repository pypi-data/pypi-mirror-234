---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.6
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Using Ontolex-Lemon data


## Using Ontolex-Lemon with NIF data


Nifigator includes functionality to work with the Lexicon Model for Ontologies (lemon), developed by the Ontology Lexicon community group (OntoLex).

We will show how to create a lexicon from NIF data and how to use an existing Ontolex-Lemon termbase to search in NIF data.


### Open a graph with NIF data


We read the NIF data that we created earlier.

```python
from nifigator import NifGraph, generate_uuid

original_uri = "https://www.dnb.nl/media/4kobi4vf/dnb-annual-report-2021.pdf"
uri = "https://dnb.nl/rdf-data/"+generate_uuid(uri=original_uri)

# create a NifGraph from this collection and serialize it 
nif_graph = NifGraph().parse(
    "..//data//"+generate_uuid(uri=original_uri)+".ttl", format="turtle"
)
```

Then we create a lexicon from NIF data. First we extract all words with lemma and part to speech tags.

```python
lexicon = nif_graph.lexicon
```

The lexicon now contains a lexicon for all languages used in the NIF data. In our case we only have an English lexicon.

```python
lexicon['en']
```

```console
(ontolex:Lexicon) uri = <https://mangosaurus.eu/rdf-data/lexicon/en>
  language : en
  entry : <https://mangosaurus.eu/rdf-data/lexicon/en/DNB>
  entry : <https://mangosaurus.eu/rdf-data/lexicon/en/in>
  entry : <https://mangosaurus.eu/rdf-data/lexicon/en/the>
  entry : <https://mangosaurus.eu/rdf-data/lexicon/en/of>
  entry : <https://mangosaurus.eu/rdf-data/lexicon/en/money>
  entry : <https://mangosaurus.eu/rdf-data/lexicon/en/,>
  entry : <https://mangosaurus.eu/rdf-data/lexicon/en/and>
  entry : <https://mangosaurus.eu/rdf-data/lexicon/en/other>
  entry : <https://mangosaurus.eu/rdf-data/lexicon/en/financial>
  entry : <https://mangosaurus.eu/rdf-data/lexicon/en/for>
  entry : ...
```


The lemon lexicon consists of lexical entries that can be retrieved with


From this a lexicon graph can be made.

```python
from nifigator import LemonGraph

lexicon_graph = LemonGraph(lexicon=lexicon)
```

```python
print("Number of triples: "+str(len(lexicon_graph)))
```

This shows:

```console
Number of triples: 34298
```

```python
# store graph to a file
import os
file = os.path.join("..//data//", generate_uuid(uri=original_uri)+"_lexicon.ttl")
lexicon_graph.serialize(file, format="turtle")
```

## Using an existing Ontolex-Lemon termbase

Below, we will give same examples based on the [Solvency 2 termbase](https://termate.readthedocs.io/en/latest/tbx2lemon.html) constructed from the Solvency 2 XBRL taxonomy.

Open the Ontolex-Lemon termbase and add to graph

```python
from rdflib import Graph

TAXO_NAME = "EIOPA_SolvencyII_XBRL_Taxonomy_2.6.0_PWD_with_External_Files"

termbase = Graph().parse(
    "P://projects//rdf-data//termbases//"+TAXO_NAME+".ttl", format="turtle"
)
```

The termbase can be combined with the nif data and we bind the prefixes to the nif graph.

```python
# combine the termbase with the NIF data
nif_graph += termbase

# bind namespaces
from rdflib import Namespace, namespace
nif_graph.bind("tbx", Namespace("http://tbx2rdf.lider-project.eu/tbx#"))
nif_graph.bind("ontolex", Namespace("http://www.w3.org/ns/lemon/ontolex#"))
nif_graph.bind("lexinfo", Namespace("http://www.lexinfo.net/ontology/3.0/lexinfo#"))
nif_graph.bind("decomp", Namespace("http://www.w3.org/ns/lemon/decomp#"))
nif_graph.bind("skos", namespace.SKOS)
```

### Running SPARQL queries

Some examples of SPARQL queries:

```python
# All altLabels of the concept Risk margin

q = """
SELECT ?altlabel
WHERE {
    ?concept skos:prefLabel "Risk margin"@en .
    ?concept skos:altLabel ?altlabel .
}
"""
# execute the query
results = list(nif_graph.query(q))

print("Number of hits: "+str(len(results)))

# print the results
for result in results[0:5]:
    print((result))
```

This returns all locations in the reporting framework that has label 'risk margin'.

```console
Number of hits: 59
(rdflib.term.Literal('SE.02.01.18.01,R0550', lang='en'),)
(rdflib.term.Literal('SR.02.01.07.01,R0640', lang='en'),)
(rdflib.term.Literal('S.02.01.08.01,R0720', lang='en'),)
(rdflib.term.Literal('S.02.01.08.01,R0590', lang='en'),)
(rdflib.term.Literal('SE.02.01.16.01,R0720', lang='en'),)
```

Now we combine the termbase data and the nif data. The termbase contains the labels and the template codes of all rows and columns. Given a specific datapoint we can look for the prefLabel (the textual representation of the row or column) and look for the lexical entry of that concept in the nif data.

```python
# all occurrences of concepts that have altLabel "S.26.01.01.01,C0030"

q = """
SELECT ?r ?word ?concept
WHERE {
    ?word nif:lemma ?t .
    ?entry ontolex:canonicalForm [ rdfs:label ?t ; ontolex:writtenRep ?r] .
    ?entry ontolex:sense [ ontolex:reference ?concept ] .
    ?concept skos:altLabel "S.26.01.01.01,C0030"@en .
}
"""
# execute the query
results = list(nif_graph.query(q))

print("Number of hits: "+str(len(results)))

# print the results
for result in results[0:5]:
    print((result[0].value, result[1:]))
```

This returns:

```console
Number of hits: 89
('liability', (rdflib.term.URIRef('https://dnb.nl/rdf-data/nif-5282967702ae37d486ad338b9771ca8f&nif=word_266314_266325'), rdflib.term.URIRef('http://eiopa.europa.eu/xbrl/s2md/fws/solvency/solvency2/2021-07-15/tab/s.26.01.01.01#s2md_c5730')))
('liability', (rdflib.term.URIRef('https://dnb.nl/rdf-data/nif-5282967702ae37d486ad338b9771ca8f&nif=word_272070_272079'), rdflib.term.URIRef('http://eiopa.europa.eu/xbrl/s2md/fws/solvency/solvency2/2021-07-15/tab/s.26.01.01.01#s2md_c5730')))
('liability', (rdflib.term.URIRef('https://dnb.nl/rdf-data/nif-5282967702ae37d486ad338b9771ca8f&nif=word_273065_273074'), rdflib.term.URIRef('http://eiopa.europa.eu/xbrl/s2md/fws/solvency/solvency2/2021-07-15/tab/s.26.01.01.01#s2md_c5730')))
('liability', (rdflib.term.URIRef('https://dnb.nl/rdf-data/nif-5282967702ae37d486ad338b9771ca8f&nif=word_276241_276252'), rdflib.term.URIRef('http://eiopa.europa.eu/xbrl/s2md/fws/solvency/solvency2/2021-07-15/tab/s.26.01.01.01#s2md_c5730')))
('liability', (rdflib.term.URIRef('https://dnb.nl/rdf-data/nif-5282967702ae37d486ad338b9771ca8f&nif=word_289288_289297'), rdflib.term.URIRef('http://eiopa.europa.eu/xbrl/s2md/fws/solvency/solvency2/2021-07-15/tab/s.26.01.01.01#s2md_c5730')))
```

If we want to include the pagenumbers of the hits we can use the following query.

```python
# all occurrences of concepts that have altLabel "S.26.01.01.01,C0030"
# including the pagenumber

q = """
SELECT ?r ?word ?pagenumber ?concept
WHERE {
    ?word nif:lemma ?t .
    ?entry ontolex:canonicalForm [ rdfs:label ?t ; ontolex:writtenRep ?r] .
    ?entry ontolex:sense [ ontolex:reference ?concept ] .
    ?concept skos:altLabel "S.26.01.01.01,C0030"@en .

    ?word nif:beginIndex ?word_beginIndex .
    ?word nif:endIndex ?word_endIndex .
    ?page rdf:type nif:Page .
    ?page nif:pageNumber ?pagenumber .
    ?page nif:beginIndex ?page_beginIndex .
    FILTER( ?page_beginIndex <= ?word_beginIndex ) .
    ?page nif:endIndex ?page_endIndex .
    FILTER( ?page_endIndex >= ?word_endIndex ) .
}
"""
# execute the query
results = nif_graph.query(q)

print("Number of hits: "+str(len(results)))

for result in list(results)[0:10]:
    print((result[0].value, result[1], result[2].value))
```

This gives:

```console
Number of hits: 89
('liability', rdflib.term.URIRef('https://dnb.nl/rdf-data/nif-5282967702ae37d486ad338b9771ca8f&nif=word_161209_161220'), 66)
('liability', rdflib.term.URIRef('https://dnb.nl/rdf-data/nif-5282967702ae37d486ad338b9771ca8f&nif=word_160848_160859'), 66)
('liability', rdflib.term.URIRef('https://dnb.nl/rdf-data/nif-5282967702ae37d486ad338b9771ca8f&nif=word_168715_168726'), 69)
('liability', rdflib.term.URIRef('https://dnb.nl/rdf-data/nif-5282967702ae37d486ad338b9771ca8f&nif=word_261149_261160'), 114)
('liability', rdflib.term.URIRef('https://dnb.nl/rdf-data/nif-5282967702ae37d486ad338b9771ca8f&nif=word_260373_260384'), 114)
('liability', rdflib.term.URIRef('https://dnb.nl/rdf-data/nif-5282967702ae37d486ad338b9771ca8f&nif=word_260676_260687'), 114)
('liability', rdflib.term.URIRef('https://dnb.nl/rdf-data/nif-5282967702ae37d486ad338b9771ca8f&nif=word_260742_260753'), 114)
('liability', rdflib.term.URIRef('https://dnb.nl/rdf-data/nif-5282967702ae37d486ad338b9771ca8f&nif=word_260865_260876'), 114)
('liability', rdflib.term.URIRef('https://dnb.nl/rdf-data/nif-5282967702ae37d486ad338b9771ca8f&nif=word_260925_260936'), 114)
('liability', rdflib.term.URIRef('https://dnb.nl/rdf-data/nif-5282967702ae37d486ad338b9771ca8f&nif=word_260993_261004'), 114)
```

Now we check for all concepts in the termbase in the text:

```python
# All concepts in the text

q = """
SELECT distinct ?concept
WHERE {
    ?word nif:lemma ?t .
    ?entry ontolex:canonicalForm [ rdfs:label ?t ; ontolex:writtenRep ?r] .
    ?entry ontolex:sense [ ontolex:reference ?concept ] .
}
"""
# execute the query
results = list(nif_graph.query(q))

print("Number of hits: "+str(len(results)))
```

This returns:

```console
Number of hits: 1259
```

Sometimes terms consists of multiwords:

```python
# All occurrence of 'dutch financial institution'

def find_term(s: str=""):
    
    words = s.split(" ")
    q = "SELECT ?s ?e\nWHERE {\n"
    q += "    ?w a nif:Word . \n"
    q += "    ?w nif:beginIndex ?s . \n"
    for idx, word in enumerate(words):
        q += '    ?w '+'nif:nextWord/'*(idx)+'nif:lemma "'+word+'"^^xsd:string .\n'
    q += '    ?w '+'nif:nextWord/'*(len(words)-1)+'nif:endIndex ?e .\n'    
    q += "}"
    q += "order by ?s"
#     print(q)
    return q

#  execute the query
results = list(nif_graph.query(find_term("dutch financial institution")))
print("Number of hits: "+str(len(results))+"\n")

for result in results:
    print(str(result[0].value) + ":"+str(result[1].value))
```

```console
Number of hits: 8

40579:40607
47488:47516
58193:58221
115913:115941
116187:116217
116925:116953
203374:203403
322642:322669
```
