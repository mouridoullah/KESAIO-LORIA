from rdflib.plugins.sparql import prepareQuery

def executer_requete_sparql(g, requete_sparql, kesaio=None, common_core_ns=None):
    namespaces = {}
    if kesaio:
        namespaces["kesaio"] = kesaio
    if common_core_ns:
        namespaces["cco"] = common_core_ns
        
    requete = prepareQuery(requete_sparql, initNs=namespaces)
    resultats = g.query(requete)
    
    return resultats
