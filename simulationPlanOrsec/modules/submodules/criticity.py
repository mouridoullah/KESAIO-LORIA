from rdflib import Literal, XSD, Namespace
kesaio = Namespace("http://www.semanticweb.org/mandiaye/ontologies/2023/7/CatastropheV2/")
def sévérité(g, seisme_uri, nombre_morts):
    severite_niveau_0 = range(0, 1)
    severite_niveau_1 = range(1, 10)
    severite_niveau_2 = range(10, 1000000)
    
    if nombre_morts in severite_niveau_0:
        severite = "Niveau 0"
    elif nombre_morts in severite_niveau_1:
        severite = "Niveau 1"
    elif nombre_morts in severite_niveau_2:
        severite = "Niveau 2"
    else:
        severite = "Niveau inconnu"
    g.add((seisme_uri, kesaio["sévérite_de_la_catastrophe"], 
           Literal(severite, datatype=XSD.string)))