Xapian Flask App
================
Flask application that can be used to index Wikipedia, then perform searches
and generate query-relevant snippets by using the ```Snipper``` class


Installation
============

```
pip install flask
```

```
# Compile and Install Xapian at the current SVN revision
# You can use the Xapian Vagrant box in which you can install Flask
./index_wiki_dump $WIKI_FILE # This might take a while
./app.py
```


