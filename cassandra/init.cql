CREATE KEYSPACE IF NOT EXISTS sentiment WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};

CREATE TABLE IF NOT EXISTS sentiment.messages (
  id uuid PRIMARY KEY,
  text text,
  sentiment text,
  created_at timestamp
);
