from rdflib import Literal, XSD, RDF, Namespace, URIRef
from datetime import datetime
import uuid
from modules.submodules import victimes, criticity 

kesaio = Namespace("http://www.semanticweb.org/mandiaye/ontologies/2023/7/CatastropheV2/")
common_core_ns = Namespace("http://www.ontologyrepository.com/CommonCoreOntologies/")
hasRole = URIRef("http://purl.obolibrary.org/obo/RO_0000087")
participatesIn = URIRef("http://purl.obolibrary.org/obo/RO_0000056")

def catastrophe(g, row):
    date_uri = kesaio[row["date"]]
    
    g.add((date_uri, RDF.type, kesaio["Date"]))
        
    date_str = row["date"]
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    jour = date_obj.day
    mois = date_obj.month
    annee = date_obj.year
        
    jour_uri = kesaio[f"jour_{jour}"]
    mois_uri = kesaio[f"mois_{mois}"]
    annee_uri = kesaio[f"{annee}"]

    g.add((jour_uri, RDF.type, common_core_ns["GregorianDay"]))
    g.add((mois_uri, RDF.type, kesaio["Gregorian_Month"]))
    g.add((annee_uri, RDF.type, common_core_ns["GregorianYear"]))
        
    g.add((date_uri, kesaio["has_day"], jour_uri))
    g.add((date_uri, kesaio["has_month"], mois_uri))
    g.add((date_uri, kesaio["has_year"], annee_uri))

    seisme_uri = kesaio[row["seismeLabel"]]
    pays_uri = kesaio[row["paysLabel"]]
    city_uri = kesaio[row["lieuLabel"]]

    g.add((seisme_uri, RDF.type, kesaio["Séisme"]))
    g.add((pays_uri, RDF.type, common_core_ns["State"]))
    g.add((city_uri, RDF.type, common_core_ns["City"]))
        
    g.add((seisme_uri, kesaio["nombre_de_morts"], Literal(row["nombreMorts"], datatype=XSD.integer)))
    g.add((seisme_uri, kesaio["nombre_de_blessés"], Literal(row["nombreBlesse"], datatype=XSD.integer)))
    g.add((seisme_uri, kesaio["description"], Literal(row["description"], datatype=XSD.string)))
        
    g.add((seisme_uri, common_core_ns["occurs_at"], city_uri))
    g.add((city_uri, common_core_ns["spatial_part_of"], pays_uri))
    g.add((seisme_uri, common_core_ns["occurs_on"], date_uri))

    nombre_morts = int(row["nombreMorts"])
        
    criticity.sévérité(g, seisme_uri, nombre_morts)

    victimes.creer_victimes(g, row, seisme_uri)

    act_uri, uri_op = kesaio["Acte_de_réponse_"], kesaio["Opération_"]
    g.add((act_uri, RDF.type, kesaio["Acte_de_réponse"]))
    g.add((uri_op, RDF.type, kesaio["Opération"]))
    g.add((uri_op, kesaio["estSuperviséPAr"], kesaio["cos"]))
    g.add((uri_op, kesaio["estSuperviséPAr"], kesaio["commandantSAMU"]))
    g.add((uri_op, kesaio["estSuperviséPAr"], kesaio["commandantGendarmerie"]))
    g.add((uri_op, kesaio["estSuperviséPAr"], kesaio["commandantPolice"]))
    g.add((act_uri, common_core_ns["has_process_part"], uri_op))
    g.add((seisme_uri, kesaio["trigger_to"], act_uri))

    pompier_id = kesaio["Commandant_des_operations_de_secours_"]
    identifiant_unique = uuid.uuid4()
    g.add((pompier_id, RDF.type, kesaio["Pompier"])) 
    g.add((pompier_id, hasRole, kesaio["cos"]))
    g.add((pompier_id, kesaio["identifiant"], Literal(identifiant_unique, datatype=XSD.string)))
    g.add((pompier_id, common_core_ns["is_affiliated_with"], kesaio["sapeurPompier"]))

    samu_id = kesaio["s2"]
    identifiant_unique_samu = uuid.uuid4()
    g.add((samu_id, RDF.type, kesaio["Membre_SAMU"]))
    g.add((samu_id, hasRole, kesaio["commandantSAMU"]))
    g.add((samu_id, kesaio["identifiant"], Literal(identifiant_unique_samu, datatype=XSD.string)))
    g.add((samu_id, common_core_ns["is_affiliated_with"], kesaio["samu"]))

    policier_id = kesaio["Commandant_de_la_police"]
    identifiant_unique = uuid.uuid4()
    g.add((policier_id, RDF.type, kesaio["Policier"]))
    g.add((policier_id, hasRole, kesaio["commandantPolice"]))  
    g.add((policier_id, kesaio["identifiant"], Literal(identifiant_unique, datatype=XSD.string)))
    g.add((policier_id, common_core_ns["is_affiliated_with"], kesaio["policeNationale"]))

    gendarme_id = kesaio["Commandant_de_la_Gendarmerie"]
    identifiant_unique_gendarme = uuid.uuid4()
    g.add((gendarme_id, RDF.type, kesaio["Gendarme"]))
    g.add((gendarme_id, hasRole, kesaio["commandantGendarmerie"]))
    g.add((gendarme_id, kesaio["identifiant"], Literal(identifiant_unique_gendarme, datatype=XSD.string)))
    g.add((gendarme_id, common_core_ns["is_affiliated_with"], kesaio["gendarmerie"]))

    return uri_op


def create_PRV(g, lonPRV, latPRV):
    uri_prv = kesaio["Point_de_rassemblement_des_victimes" + "_1"]
    g.add((uri_prv, RDF.type, kesaio["Point_de_rassemblement_des_victimes"]))
    g.add((uri_prv, kesaio["longitude"], Literal(lonPRV, datatype=XSD.decimal)))
    g.add((uri_prv, kesaio["latitude"], Literal(latPRV, datatype=XSD.decimal)))
    pompiers_attributs = [
        (kesaio["Pompier1"], kesaio["deblaiement"]),
        (kesaio["Pompier2"], kesaio["desincarceration"]),
        (kesaio["Pompier3"], kesaio["premierSoins"]),
        (kesaio["Pompier4"], kesaio["rechercherDesVictimes"])
    ]

    for index, attributs in enumerate(pompiers_attributs, start=1):
        identifiant_unique = uuid.uuid4()
        pompier_id, fonction = attributs
        
        g.add((pompier_id, RDF.type, kesaio["Pompier"]))
        g.add((pompier_id, kesaio["identifiant"], Literal(identifiant_unique, datatype=XSD.string)))
        g.add((pompier_id, hasRole, kesaio["equipierInter"]))
        g.add((pompier_id, common_core_ns["is_affiliated_with"], kesaio["sapeurPompier"]))
        g.add((pompier_id, kesaio["aPourFonction"], fonction))

    return uri_prv

def createRamassage_act(g, uri_prv, uri_op):
    uri_actDeRamassage = kesaio["Acte_de_ramassage_des_victimes" + "_1"]
    g.add((uri_actDeRamassage, RDF.type, kesaio["Acte_de_ramassage_des_victimes"]))
    g.add((uri_actDeRamassage, common_core_ns["occurs_at"], uri_prv))
    g.add((uri_op, common_core_ns["has_process_part"], uri_actDeRamassage))
    g.add((uri_actDeRamassage, kesaio["needs"], kesaio["capteurDeMouvement"]))
    g.add((uri_actDeRamassage, kesaio["needs"], kesaio["battementDeCoeur"]))
    g.add((uri_actDeRamassage, kesaio["needs"], kesaio["detecteurDeChaleur"]))
    g.add((uri_actDeRamassage, kesaio["needs"], kesaio["grue"]))
    g.add((uri_actDeRamassage, kesaio["needs"], kesaio["marteauxPiqueurs"]))
    g.add((uri_actDeRamassage, kesaio["needs"], kesaio["verinHydraulique"]))
    g.add((uri_actDeRamassage, kesaio["needs"], kesaio["scie"]))

    return uri_actDeRamassage

def create_personnel(g, uri_actDeRamassage, nombre_pompiers, nombre_policiers, nombre_officiers_samu):
    for i in range(5, nombre_pompiers + 5): 
        pompier_id = kesaio["Pompier" + str(i)]
        identifiant_unique = uuid.uuid4()
        g.add((pompier_id, RDF.type, kesaio["Pompier"])) 
        g.add((pompier_id, hasRole, kesaio["equipierInter"]))
        g.add((pompier_id, kesaio["aPourFonction"], kesaio["rechercherDesVictimes"]))
        g.add((pompier_id, kesaio["identifiant"], Literal(identifiant_unique, datatype=XSD.string)))
        g.add((pompier_id, common_core_ns["is_affiliated_with"], kesaio["sapeurPompier"]))
        g.add((pompier_id, participatesIn, uri_actDeRamassage))
        # g.add((pompier_id, kesaio["estSuperviséPAr"], kesaio["cos"]))

    for i in range(0, nombre_policiers): 
        policier_id = kesaio["Policier" + str(i)]
        identifiant_unique = uuid.uuid4()
        g.add((policier_id, RDF.type, kesaio["Policier"]))
        g.add((policier_id, hasRole, kesaio["encadrementEtapplication"]))
        g.add((policier_id, kesaio["aPourFonction"], kesaio["assistanceAdministrative"]))
        g.add((policier_id, kesaio["identifiant"], Literal(identifiant_unique, datatype=XSD.string)))
        g.add((policier_id, common_core_ns["is_affiliated_with"], kesaio["policeNationale"]))
        g.add((policier_id, participatesIn, uri_actDeRamassage))
        # g.add((policier_id, kesaio["estSuperviséPAr"], kesaio["Commandant_de_la_police"]))

    for i in range(0, nombre_officiers_samu): 
        officier_id = kesaio["OfficierRamassage" + str(i)]
        identifiant_unique = uuid.uuid4()
        g.add((officier_id, RDF.type, kesaio["Gendarme"]))
        g.add((officier_id, hasRole, kesaio["uniteDeRecherche"]))
        g.add((officier_id, kesaio["identifiant"], Literal(identifiant_unique, datatype=XSD.string)))
        g.add((officier_id, common_core_ns["is_affiliated_with"], kesaio["gendarmerie"]))
        g.add((officier_id, kesaio["aPourFonction"], kesaio["rechercheEtSauvetage"]))
        g.add((officier_id, participatesIn, uri_actDeRamassage))
        # g.add((officier_id, kesaio["estSuperviséPAr"], kesaio["commandantSAMU"]))

def create_medical_post(g, lonPMA, latPMA):
    uri_pma = kesaio["Poste_médical_avancé" + "_1"]
    g.add((uri_pma, RDF.type, kesaio["Poste_médical_avancé"]))
    g.add((uri_pma, kesaio["longitude"], Literal(lonPMA, datatype=XSD.decimal)))
    g.add((uri_pma, kesaio["latitude"], Literal(latPMA, datatype=XSD.decimal)))
    g.add((uri_pma, kesaio["nombreDeLit"], Literal(50, datatype=XSD.integer)))

    uri_rolePMA = kesaio["officierPMA"]

    for i in range(0, 2): 
        identifiant_unique = uuid.uuid4()
        uri_OPMA = kesaio["OfficierPMA" + str(i)]  
        g.add((uri_OPMA, RDF.type, kesaio["Membre_SAMU"])) 
        g.add((uri_OPMA, common_core_ns["is_affiliated_with"], kesaio["samu"]))
        g.add((uri_OPMA, kesaio["identifiant"], Literal(identifiant_unique, datatype=XSD.string)))
        g.add((uri_OPMA, hasRole, uri_rolePMA))
        g.add((uri_OPMA, kesaio["aPourFonction"], kesaio["gestionInfra"]))
        # g.add((uri_rolePMA, kesaio["estSuperviséPAr"], kesaio["commandantSAMU"]))
        g.add((uri_OPMA, kesaio["monter"], uri_pma))
    
    return uri_pma

def create_evacuation_act(g,uri_pma, uri_op):
    uri_actDEvacution = kesaio["Acte_devacuation_des_victimes" + "_1"]
    g.add((uri_actDEvacution, RDF.type, kesaio["Acte_devacuation_des_victimes"]))
    g.add((uri_actDEvacution, common_core_ns["occurs_at"], uri_pma))
    g.add((uri_op, common_core_ns["has_process_part"], uri_actDEvacution))
    g.add((uri_actDEvacution, kesaio["needs"], kesaio["equipeMédicale"]))

    return uri_actDEvacution

def create_medical_aid(g, uri_pma, uri_op):
    uri_actDeSoins = kesaio["Acte_de_secours_des_victimes" + "_1"]
    g.add((uri_actDeSoins, RDF.type, kesaio["Acte_de_secours_des_victimes"]))
    g.add((uri_actDeSoins, common_core_ns["occurs_at"], uri_pma))
    g.add((uri_op, common_core_ns["has_process_part"], uri_actDeSoins))
    g.add((uri_actDeSoins, kesaio["needs"], kesaio["equipeMédicale"]))
    g.add((uri_actDeSoins, kesaio["needs"], kesaio["vehiculeDeSecoursEtDassistanceAuxVictimes"]))
    g.add((uri_actDeSoins, kesaio["needs"], kesaio["vehiculeDeSoutienSanitaire"]))
    
    
    return uri_actDeSoins

def create_medical_staff(g, uri_actDeSoins, nombre_de_medecins, nombre_d_infirmiers):
    uri_offPRV = kesaio["officierRassemblement"]
    for i in range(0, nombre_de_medecins): 
        medecin = kesaio["Médecin_urgentiste_" + str(i)]
        identifiant_unique = uuid.uuid4()
        g.add((medecin, RDF.type, kesaio["Membre_SAMU"]))
        g.add((medecin, hasRole, uri_offPRV))
        g.add((medecin, kesaio["identifiant"], Literal(identifiant_unique, datatype=XSD.string)))
        g.add((medecin, common_core_ns["is_affiliated_with"], kesaio["samu"]))
        g.add((medecin, participatesIn, uri_actDeSoins))
        g.add((medecin, kesaio["aPourFonction"], kesaio["useMaterielSpecialise"]))
        g.add((medecin, kesaio["aPourFonction"], kesaio["gestMedicauxAavances"]))
        g.add((medecin, kesaio["aPourFonction"], kesaio["transferIntrerHosp"]))
        
    for i in range(0, nombre_d_infirmiers): 
        infirmier = kesaio["Infirmier_SAMU_" + str(i)]
        identifiant_unique = uuid.uuid4()
        g.add((infirmier, RDF.type, kesaio["Membre_SAMU"]))
        g.add((infirmier, hasRole, uri_offPRV))
        g.add((infirmier, kesaio["identifiant"], Literal(identifiant_unique, datatype=XSD.string)))
        g.add((infirmier, common_core_ns["is_affiliated_with"], kesaio["samu"]))
        g.add((infirmier, participatesIn, uri_actDeSoins))
        g.add((infirmier, kesaio["aPourFonction"], kesaio["soutienMedical"]))
        g.add((infirmier, kesaio["aPourFonction"], kesaio["suiviPostInter"]))
        
def create_other_staff(g, uri_actDeSoins, nombre_psychologues):
    uri_offPRV = kesaio["officierRassemblement"]
    for i in range(0, nombre_psychologues): 
        psychologue = kesaio["Psychologue_SAMU_" + str(i)]
        identifiant_unique = uuid.uuid4()
        g.add((psychologue, RDF.type, kesaio["Membre_SAMU"]))
        g.add((psychologue, hasRole, uri_offPRV))
        g.add((psychologue, kesaio["identifiant"], Literal(identifiant_unique, datatype=XSD.string)))
        g.add((psychologue, common_core_ns["is_affiliated_with"], kesaio["samu"]))
        g.add((psychologue, participatesIn, uri_actDeSoins))
        g.add((psychologue, kesaio["aPourFonction"], kesaio["suiviPostInter"]))
        g.add((psychologue, kesaio["aPourFonction"], kesaio["interventionEnCasDeCrise"]))
        g.add((psychologue, kesaio["aPourFonction"], kesaio["evalPsychologique"]))
        g.add((psychologue, kesaio["aPourFonction"], kesaio["interSantéMentale"]))
        

def create_PompierPourLesMorts(g, uri_actDeSoins, nombre_pompiers):
    for i in range(0, nombre_pompiers): 
        pompier_id = kesaio["Pompier" + str(i)]
        identifiant_unique = uuid.uuid4()
        g.add((pompier_id, RDF.type, kesaio["Pompier"])) 
        g.add((pompier_id, hasRole, kesaio["equipierMedical"]))
        g.add((pompier_id, kesaio["identifiant"], Literal(identifiant_unique, datatype=XSD.string)))
        g.add((pompier_id, common_core_ns["is_affiliated_with"], kesaio["sapeurPompier"]))
        g.add((pompier_id, participatesIn, uri_actDeSoins))
        g.add((pompier_id, kesaio["aPourFonction"], kesaio["collectEtTransportDesMorts"]))
        


def add_ambulance_and_helicopter(g, uri_actDEvacution, nombre_ambulance, nombre_helicoptere):
    for i in range(0, nombre_ambulance):
        ambulance_id = kesaio["Ambulance_" + str(i)]
        g.add((ambulance_id, RDF.type, kesaio["Ambulance"])) 
        g.add((ambulance_id, kesaio["has_status"], kesaio["engagé"]))
        g.add((uri_actDEvacution, kesaio["needs"], ambulance_id))

        ambulancier = kesaio["ambulancier_" + str(i)]
        identifiant_unique = uuid.uuid4()
        g.add((ambulancier, RDF.type, kesaio["Membre_SAMU"]))
        g.add((ambulancier, hasRole, kesaio["ambulancier"]))  
        g.add((ambulancier, kesaio["identifiant"], Literal(identifiant_unique, datatype=XSD.string)))
        g.add((ambulancier, common_core_ns["is_affiliated_with"], kesaio["samu"]))
        g.add((ambulancier, kesaio["is_required"], uri_actDEvacution))
        g.add((ambulancier, participatesIn, uri_actDEvacution))
        g.add((ambulancier, kesaio["aPourFonction"], kesaio["transportDesPatients"]))

    for i in range(0, nombre_helicoptere): 
        helico_id = kesaio["helicoptereSAMU_" + str(i)]
        g.add((helico_id, RDF.type, kesaio["Helicoptere_SAMU"])) 
        g.add((helico_id, kesaio["has_status"], kesaio["engagé"]))
        g.add((uri_actDEvacution, kesaio["needs"], helico_id))

        pilote = kesaio["pilote_" + str(i)]
        identifiant_unique = uuid.uuid4()
        g.add((pilote, RDF.type, kesaio["Membre_SAMU"]))
        g.add((pilote, hasRole, kesaio["pilote"]))  
        g.add((pilote, kesaio["identifiant"], Literal(identifiant_unique, datatype=XSD.string)))
        g.add((pilote, common_core_ns["is_affiliated_with"], kesaio["samu"]))
        g.add((pilote, kesaio["is_required"], uri_actDEvacution))
        g.add((pilote, participatesIn, uri_actDEvacution))
        g.add((pilote, kesaio["aPourFonction"], kesaio["transportDesPatients"]))
