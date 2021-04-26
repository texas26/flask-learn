import flask
from flask_json import FlaskJSON, json_response, as_json
import sqlite3

app = flask.Flask(__name__)
FlaskJSON(app)

@app.route('/urlinfo/1/<hostname_port>/<path_and_query>', methods=['GET'])
def check_url(hostname_port, path_and_query):
    url_unsafe = False
    url_infected = False
    query_infected = False
    hostname_port_list = hostname_port.split(":")

    rows=get_url_data(hostname_port_list[0])
    for url in rows:
        if hostname_port_list[0] in url[0]:
            url_unsafe = True
        if len(hostname_port_list)>1 and hostname_port_list[1] in url[1]:
            url_infected = True
        if path_and_query in url[2]:
            query_infected = True

    return json_response(url_unsafe=url_unsafe, url_infected=url_infected, query_infected=query_infected)

def get_url_data(hostname):
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    create_db(conn)

    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE url LIKE ?", ('%' + hostname + '%',))
    rows = cur.fetchall()
    conn.close()

    return rows

def create_db(conn):
    if not conn.execute('CREATE TABLE IF NOT EXISTS students (url TEXT, port TEXT, query TEXT)'):
        print("Database already present")
        cur = conn.cursor()
        cur.execute("INSERT INTO students (url,port,query) VALUES ('www.infected1.com','4000','malwarequery=2')")
        cur.execute("INSERT INTO students (url,port,query) VALUES ('www.infected1.com','6000', '')")
        cur.execute("INSERT INTO students (url,port,query) VALUES ('www.infected2.com','4000','malwarequery=1')")
    print("Table created successfully")

if __name__ == '__main__':
    app.run()