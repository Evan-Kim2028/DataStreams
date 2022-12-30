.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/DataStreams.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/DataStreams
    .. image:: https://readthedocs.org/projects/DataStreams/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://DataStreams.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/DataStreams/main.svg
        :alt: Coveralls/home/evan/Documents/github/DataStream/README.md
        :target: https://coveralls.io/r/<USER>/DataStreams
    .. image:: https://img.shields.io/pypi/v/DataStreams.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/DataStreams/
    .. image:: https://img.shields.io/conda/vn/conda-forge/DataStreams.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/DataStreams
    .. image:: https://pepy.tech/badge/DataStreams/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/DataStreams
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/DataStreams

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

===========
DataStreams
===========


DataStream a package that lets user build GraphQL DAG queries out of Subgraph data. 



It provides extended functionality on top of The Graph data access package [Subgrounds](https://github.com/Protean-Labs/subgrounds).


.. _pyscaffold-notes:

Dependencies and Setup
======================
Since DataStream uses Subgrounds, Python 3.10 is required.

DataStream also requires:
* Python (>= 3.10)
* Subgrounds (>= 1.0.3)
* Pandas (>= 1.5.0)