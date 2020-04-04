from django.shortcuts import render

import json

from django.http import HttpResponse

# self-defined imports
from my_pokemon_api import *
from db_accessor import *

DBG = "---->"

class Config:
    pass

# Create your views here.

def add_crawl_point(request):
    
    print DBG + "I'm in add_crawl_point"

    #crawl  pokemon data

    #1. Get cell id from the request
    request_obj = json.loads(request.body)
    cell_id = request_obj["cell_id"]

    #print DBG + cell_id


    #2. Call search api
    config = Config()
    config.auth_service = "ptc"
    config.username = "testuser1"
    config.password = "testuser1"
    config.proxy = "sock5://127.0.0.1:9050"

    api = init_api(config)

    search_response = search_point(cell_id, api)
    result = parse_pokemon(search_response)
    pokemon_data = json.dumps(result, indent=2)
    #print DBG + pokemon_data

    #3. Store the search results into database
    for pokemon in result:
        add_pokemon_to_db(pokemon["encounter_id"],
                          pokemon["expiration_timestamp_ms"],
                          pokemon["pokemon_id"],
                          pokemon["latitude"],
                          pokemon["longitude"])

    return HttpResponse(pokemon_data)