# app/db/cassandra_session.py
from cassandra.cluster import Cluster, NoHostAvailable
from app.config import CASSANDRA_HOST, CASSANDRA_PORT, KEYSPACE

try:
    # Connect to the Cassandra cluster and keyspace
    cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT)
    session = cluster.connect(KEYSPACE)
    print(f"Connected to Cassandra keyspace '{KEYSPACE}' on {CASSANDRA_HOST}:{CASSANDRA_PORT}")

except NoHostAvailable as e:
    print(f"Unable to connect to Cassandra at {CASSANDRA_HOST}:{CASSANDRA_PORT}. Ensure Cassandra is running and accessible.")
    raise e


