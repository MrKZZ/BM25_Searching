import requests
import json
import wikipedia

def get_wiki_result(keyword, lang='en', sentences=1):
    wikipedia.set_lang(lang)
    return wikipedia.summary(keyword, sentences=sentences), \
           wikipedia.search(keyword), \
           wikipedia.page(keyword)

api_url = 'https://meshb.nlm.nih.gov/api/search/record'

def get_mesh_result(q, field="allTerms", sort='', size=20,
                    type_="exactMatch", method="FullWord"):
    """Sends a GET request.

        :param q: query string
        :param field: { allTerms, termDescriptor, termQualifier, termSupplementalRecord,
                                ui, allChemical, termHeading, termIndexingInfo, termPharma,
                                allRegistry, termRelatedRegistry, termCASRegistry, freeText ,annotation
                                scopeNote, scrNote}
                                default is allTerms
                                more details about this field: https://meshb.nlm.nih.gov

        :param sort: default is ''(none), { primaryTerm, none}
        :param size: default is 20 {20, 1000 }
        :param type_: default is 'exactMatch', { exactMatch, allWords, anyWord }
        :param method: default is 'FullWord' ,  {SubString, FullWord}
        :return: :class:`dict` object
    """
    data = {
        'q': q,
        'searchInField': field,
        'sort': sort,
        'size': size,
        'searchType': type_,
        'searchMethod': method
    }
    r = requests.get(api_url, params=data)
    return json.loads(r.text)

def Mesh(query):
    Mesh_sim = []
    try:
        diction = get_mesh_result(query)['hits']['hits'][0]['_source']
        for term in diction['SeeRelatedList']['SeeRelatedDescriptor']:
            Mesh_sim.append(term['DescriptorReferredTo']['DescriptorName']['String']['t'])
    except:
        pass
    return Mesh_sim
