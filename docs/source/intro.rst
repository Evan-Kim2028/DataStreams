===========
Intro
===========
DataStreams a Subgraph query utility package that allows users to execute more complex GraphQL queries. 
It provides extended functionality on top of The Graph data access package `Subgrounds`_.

The overarching goals of DataStreams are the following:
- provide a DRY experience for developers to manage subgraph queries
- batch support for subgraph query searches
- provide parallelization for subgraph query exeuction
- provide an interface to query search across multiple Subgraph nodes simultaneously (WIP w/ :class:`DataStream <src/datastreams/datastream.py>`)

The main class in DataStreams is called :class:`Streamer <src/datastreams/streamer.py>`. :class:`Streamer <src/datastreams/streamer.py>` stores a Subgraph schema information
and provides an interface to easily construct and execute Subgraph queries. 

.. _Subgrounds: https://github.com/Protean-Labs/subgrounds


Dependencies and Setup
======================
Since DataStream uses Subgrounds, Python 3.10 is required.

DataStream also requires:

- Python (>= 3.10)
- Subgrounds (>= 1.0.3)
- Pandas (>= 1.5.0)