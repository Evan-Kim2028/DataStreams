Examples
=============

#1. Getting Subgraph data from cow protocol on ethereum and gnosis.
-------------------------------------------------------------------

.. code-block:: python
    
    from datastreams.datastream import DataStream

    ds = DataStream()

    endpoint_ids = [
                    'https://api.thegraph.com/subgraphs/name/cowprotocol/cow',
                    'https://api.thegraph.com/subgraphs/name/cowprotocol/cow-gc'
                    ]


    # test getDataStream() functionality by getting all data from cow subgraphs
    for endpoint in endpoint_ids:
        ds.getDataStream(endpoint)



