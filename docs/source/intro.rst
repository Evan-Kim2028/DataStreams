# DataStreams
DataStreams a package that lets user build GraphQL DAG queries out of Subgraph data on The Graph Network. 
It provides extended functionality on top of The Graph data access package [Subgrounds](https://github.com/Protean-Labs/subgrounds).


Dependencies and Setup:
=======================
Since DataStreams uses Subgrounds, which requires >=Python 3.10, Python 3.10 is also a requirement for DataStreams.

### Dependencies
DataStream requires:
* Python (>= 3.10)
* Subgrounds (>= 1.0.3)
* Pandas (>= 1.5.0)

How it Works:
=======================
Instantiate the main module (name TBD) to firehose all historical data from a subgraph to your PC stored in a folder of pandas dataframes. 
