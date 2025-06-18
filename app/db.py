from arango import ArangoClient
from app.config import ARANGO_URL, DB_NAME, USERNAME, PASSWORD

# client = ArangoClient()
# sys_db = client.db("_system", username=USERNAME, password=PASSWORD)
client = ArangoClient(hosts=ARANGO_URL)
sys_db = client.db('_system', username=USERNAME, password=PASSWORD)

if not sys_db.has_database(DB_NAME):
    sys_db.create_database(DB_NAME)

db = client.db(DB_NAME, username=USERNAME, password=PASSWORD)