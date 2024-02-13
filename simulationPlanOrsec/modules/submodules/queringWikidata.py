import cachetools
from SPARQLWrapper import SPARQLWrapper, JSON

# Créer un cache (dict dans cet exemple)
cache = cachetools.LRUCache(maxsize=128)
@cachetools.cached(cache)
def queryWikidata(query):
    endpoint_url = "https://query.wikidata.org/sparql"
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    # sparql.addParameter("language", language)
    results = sparql.query().convert()
    return results

def search_nearby_entities(lat, lon, entity_type):
    query = f"""
    SELECT DISTINCT ?entity ?entityLabel ?location ?dist 
    WHERE {{
        SERVICE wikibase:around {{
            ?entity wdt:P625 ?location . 
            bd:serviceParam wikibase:center "Point({lon} {lat})"^^geo:wktLiteral . 
            bd:serviceParam wikibase:radius "50" . 
            bd:serviceParam wikibase:distance ?dist.
        }}
        VALUES ?entity_type {{ wd:{entity_type} }}
        ?entity wdt:P31/wdt:P279* ?entity_type .
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "fr". }}
    }}
    ORDER BY ASC(?dist)
    LIMIT 3
    """
    return queryWikidata(query)