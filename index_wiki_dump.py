#!/usr/bin/env python

import sys
import wiki_extract
import xapian

import settings

def main():
    database = xapian.WritableDatabase(settings.DATABASE_NAME,
                                       xapian.DB_CREATE_OR_OPEN)

    indexer = xapian.TermGenerator()
    stemmer = xapian.Stem("english")
    indexer.set_stemmer(stemmer)

    with open(sys.argv[1]) as f:
        for page in wiki_extract.extract_pages(f):
            no, title, content = page

            content = wiki_extract.text_only(content)
            if content.startswith('#RE'):
                continue

            print 'Indexing %s' % title

            doc = xapian.Document()
            doc.add_value(settings.VALUENO_DOC_NUM, title)
            doc.set_data(content[:4000])

            indexer.set_document(doc)
            indexer.index_text(content)

            database.add_document(doc)

if __name__ == '__main__':
    main()

