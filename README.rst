.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/


===========
DataStreams
===========
DataStreams a Subgraph query utility package that allows users to execute more complex GraphQL queries. 
It provides extended functionality on top of The Graph data access package `Subgrounds`_.

The overarching goals of DataStreams are the following:
- provide a DRY experience for developers to manage subgraph queries
- batch support for subgraph query searches
- provide parallelization for subgraph query exeuction
- provide an interface to query search across multiple Subgraph nodes simultaneously (WIP)

The main class in DataStreams is called 'Streamer'. `Streamer`_. `Streamer`_ stores a Subgraph schema information
and provides an interface to easily construct and execute Subgraph queries. 


.. _Subgrounds: https://github.com/Protean-Labs/subgrounds



.. _pyscaffold-notes:


Dependencies and Setup
======================
Since DataStream uses Subgrounds, Python 3.10 is required.

DataStream also requires:

* Python (>= 3.10)
* Subgrounds (>= 1.0.3)
* Pandas (>= 1.5.0)


Installation
============
Install via `pip install git+https://github.com/Evan-Kim2028/DataStreams.git
    

Documentation
=============
Find a `work in progress documentation here`_.

.. _work in progress documentation here: https://datastreams-subgraph.readthedocs.io/en/latest/
