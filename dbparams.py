import psycopg2

# global connection object
con = psycopg2.connect(
    dbname="professionals",
    user='postgres',
    host='localhost',
    password='Post@515',
    port=5433
)
def get_cursor():
    return con.cursor()