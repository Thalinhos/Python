
shards = {
    0: 'postgresql://shard0-db',
    1: 'postgresql://shard1-db',
    2: 'postgresql://shard2-db',
    3: 'postgresql://shard3-db',
}

def get_shard_connection(user_id):
    shard_id = user_id % 4 
    db_url = shards[shard_id]
    return connect_to_db(db_url) 

def insert_user(user_id, name):
    conn = get_shard_connection(user_id)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (id, name) VALUES (%s, %s)", (user_id, name))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = get_shard_connection(user_id)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# exemplo agora usando por range, da pra fazer com hashs/strings prefixadas
# também pra facilitar, o esquema eh meter pau marco veio
def get_shard_by_range(user_id):
    if user_id < 1_000_000:
        return connect_to_db('postgresql://shard0')
    elif user_id < 2_000_000:
        return connect_to_db('postgresql://shard1')
    ...
