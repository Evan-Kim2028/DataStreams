=========
Changelog
=========

Version 1.1.0
===========

- Simplify run_query by removing query_size parameter. Note that this breaks existing queries that used v1.0.0
- Remove parallelization queries. Requires a redesign.

Version 1.0.0
===========

- Added test_streamer.py to test the streamer class functionality
- Added DataStream.py class as an execution layer interface to streamer
- Added test_datastream.py to test the DataStream class functionality
- Added documentation via Sphinx & tox