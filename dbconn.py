import sqlalchemy


# 192.168.1.104 5432 내부
# 121.140.47.102 25432 외부
def connect(user, password, db, host='121.140.47.102', port=35432):
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    # postgresql://federer:grandestslam@localhost:5432/tennis
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    con = sqlalchemy.create_engine(url, client_encoding='utf8')

    # We then bind the connection to MetaData()
    # meta = sqlalchemy.MetaData(bind=con, reflect=True)

    return con


def get_con():
    return connect('postgres', 'levware1234', 'levtest')

# connection
# conn = connect('postgres', 'levware1234', 'levtest')