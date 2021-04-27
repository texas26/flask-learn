import flask
from flask_json import FlaskJSON, json_response, as_json
import sqlite3
import validators

app = flask.Flask(__name__)
FlaskJSON(app)

@app.route('/urlinfo/1/<hostname_port>/')
@app.route('/urlinfo/1/<hostname_port>/<path_and_query>')
def check_url(hostname_port, path_and_query=None):
    host_unsafe = False   # HOSTNAME is in list of infected sites
    host_infected = False # HOSTNAME:PORT is in list of affected sites
    url_infected = False # URL is in list of affected sites
    
    hostname_port_list = hostname_port.split(":")
    h_under_test = "http://" + hostname_port_list[0]

    if not validators.url(h_under_test):
        return "Hostname under test not Valid"

    rows=get_url_data(hostname_port_list[0])
    print(str(rows))
    for url in rows:
        if hostname_port_list[0] in url[0]:
            host_unsafe = True
        if len(hostname_port_list)>1 and hostname_port_list[1] in url[1]:
            if host_unsafe:
                host_infected = True
        if host_unsafe and not len(hostname_port_list)>1:
            host_infected = True
        if path_and_query is not None:
            if path_and_query in url[2] and host_unsafe:
                url_infected = True

    return json_response(host_unsafe=host_unsafe, host_infected=host_infected, url_infected=url_infected)

def get_url_data(hostname):
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    create_db(conn)

    cur = conn.cursor()
    cur.execute("SELECT * FROM url")
    rows = cur.fetchall()
    conn.close()

    return rows

def create_db(conn):
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS url")
    cur.execute(''' SELECT count(*) FROM sqlite_master WHERE type='table' AND name='url' ''')
    if not cur.fetchone()[0]:
        cur.execute('CREATE TABLE url (url TEXT, port TEXT, query TEXT)')
        cur.execute("INSERT INTO url (url,port,query) VALUES ('www.infected1.com','4000','malwarequery=2')")
        cur.execute("INSERT INTO url (url,port,query) VALUES ('www.infected1.com','6000', '')")
        cur.execute("INSERT INTO url (url,port,query) VALUES ('www.infected2.com','4000','malwarequery=1')")
        cur.execute("INSERT INTO url (url,port,query) VALUES ('www.infected2.com','','malwarequery=1')")
        cur.execute("INSERT INTO url (url,port,query) VALUES ('www.infected3.com','','')")
        print("Table created successfully")
    else:
        print("Table already exists")

if __name__ == '__main__':
    app.run()