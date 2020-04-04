import psycopg2

DBG = "----> "

def add_pokemon_to_db(encounter_id, expire, pokemon_id, latitude, longitude):
    #1. Open connection
    conn = psycopg2.connect(host = "pokemon-go-class.cgtudp6v0ujx.us-west-2.rds.amazonaws.com",
                            port = 5432,
                            user = "pkgo1",
                            password = "pkgo123456",
                            dbname = "postgres"
                            )                    

    #2. Execute SQL
    with conn.cursor() as cur:
        cur.execute("INSERT INTO pokemon_map(encounter_id, expire, pokemon_id, latitude, longitude)" +
                    " VALUES(%s, %s, %s, %s, %s)" +
                    " ON CONFLICT (encounter_id) DO NOTHING", (encounter_id, expire, pokemon_id, latitude, longitude))

    #3. connection commit
    conn.commit()

    print DBG + "add_pokemon_to_db with encounter_id" + str(encounter_id)

    return