#!/usr/bin/env python

import sys
import xapian

import settings

def main():
    database = xapian.WritableDatabase(settings.DATABASE_NAME,
                                       xapian.DB_CREATE_OR_OPEN)

    indexer = xapian.TermGenerator()
    stemmer = xapian.Stem("english")
    indexer.set_stemmer(stemmer)

    for filename in sys.argv[1:]:
        with open(filename) as f:
            content = f.read()

        doc = xapian.Document()
        doc.add_value(settings.VALUENO_DOC_NUM, filename)
        doc.set_data(content)

        indexer.set_document(doc)
        indexer.index_text(content)

        database.add_document(doc)

if __name__ == '__main__':
    main()

