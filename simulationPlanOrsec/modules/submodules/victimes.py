import random
from rdflib import RDF, Namespace
kesaio = Namespace("http://www.semanticweb.org/mandiaye/ontologies/2023/7/CatastropheV2/")
def creer_victimes(g, row, seisme_uri):
    l = {
        "dcd_uri": kesaio["décédé"],
        "ua_uri": kesaio["ua"],
        "ur_uri": kesaio["ur"],
        "ump_uri": kesaio["ump"],
        "ind_uri": kesaio["indemne"]
    }
        
    for i in range(0, int(row["nombreMorts"])): 
        victime_id = kesaio["victime_" + str(i)]  
        g.add((victime_id, RDF.type, kesaio["Victime"]))  
        g.add((victime_id, kesaio["has_status"], l["dcd_uri"]))
        g.add((seisme_uri, kesaio["engendre"], victime_id))

    for i in range(int(row["nombreMorts"]), int(row["nombreMorts"])
                    + int(row["nombreBlesse"])):
        element_aleatoire = random.choice([key for key in l.keys() if key != "dcd_uri"])
        victime_id = kesaio["victime_" + str(i)]  
        g.add((victime_id, RDF.type, kesaio["Victime"]))  
        g.add((victime_id, kesaio["has_status"], l[element_aleatoire]))

        element_aleatoire = random.choice(list(l.keys()))
        g.add((victime_id, kesaio["has_evolution"], l[element_aleatoire]))
        g.add((seisme_uri, kesaio["engendre"], victime_id))

# def creer_victimes(g, row, seisme_uri):
#     l = {
#         "dcd_uri": kesaio["décédé"],
#         "ua_uri": kesaio["ua"],
#         "ur_uri": kesaio["ur"],
#         "ump_uri": kesaio["ump"],
#         "ind_uri": kesaio["indemne"]
#     }
        
#     for i in range(0, int(row["nombreMorts"])): 
#         victime_id = kesaio["victime_" + str(i)]  
#         g.add((victime_id, RDF.type, kesaio["Victime"]))  
#         g.add((victime_id, kesaio["has_status"], l["dcd_uri"]))
#         g.add((seisme_uri, kesaio["engendre"], victime_id))

#     for i in range(int(row["nombreMorts"]), int(row["nombreMorts"]) + int(row["nombreBlesse"])):
#         element_aleatoire = random.choice([key for key in l.keys() if key != "dcd_uri"])
#         victime_id = kesaio["victime_" + str(i)]  
#         g.add((victime_id, RDF.type, kesaio["Victime"]))  

#         # Récupération de l'état actuel et choix d'une évolution autorisée en fonction de cet état
#         etat_actuel = l[element_aleatoire]
#         if etat_actuel == kesaio["indemne"]:
#             evolution_autorisee = random.choice([l["ump_uri"], l["ur_uri"]])
#         elif etat_actuel == kesaio["ump"]:
#             evolution_autorisee = random.choice([l["ind_uri"], l["ur_uri"], l["ua_uri"]])
#         elif etat_actuel in [kesaio["ur"], kesaio["ua"]]:
#             evolution_autorisee = random.choice(list(l.values()))
#         else:
#             evolution_autorisee = l["dcd_uri"]  # État actuel: "décédé", aucune évolution possible
        
#         # Assignation de l'évolution autorisée et ajout des triples
#         g.add((victime_id, kesaio["has_status"], etat_actuel))
#         g.add((victime_id, kesaio["has_evolution"], evolution_autorisee))
#         g.add((seisme_uri, kesaio["engendre"], victime_id))
