#!/usr/bin/env python

import flask
import xapian

import settings

app = flask.Flask(__name__, static_folder='static')
app.config.from_object(__name__)

app.config.update({
    'DEBUG':True
    })

database = xapian.Database(settings.DATABASE_NAME)

@app.route('/')
def homepage():
    return flask.render_template('home.html')

@app.route('/search', methods=['GET'])
def search():
    query=flask.request.args.get('q')

    enquire = xapian.Enquire(database)
    qp = xapian.QueryParser()

    stemmer = xapian.Stem('english')
    snipper = xapian.Snipper()

    qp.set_stemmer(stemmer)
    qp.set_database(database)
    qp.set_stemming_strategy(xapian.QueryParser.STEM_SOME)

    parsed_query = qp.parse_query(query)
    enquire.set_query(parsed_query)

    mset = enquire.get_mset(0, 10)

    snipper.set_mset(mset)
    snipper.set_stemmer(stemmer)

    results = []
    for m in mset:
        results.append({
            'name': m.document.get_value(settings.VALUENO_DOC_NUM),
            'snippet': snipper.generate_snippet(m.document.get_data())})

    return flask.render_template('results.html',
                                 query=query,
                                 results=results)

@app.route('/files/<fname>')
def download_file(fname):
    return flask.redirect(flask.url_for('static', filename='img/' + fname),
                          code=301)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
