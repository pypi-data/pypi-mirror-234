gqlclient
=========

|codecov|

.. image:: https://readthedocs.org/projects/graphql-client/badge/?version=latest
   :target: https://dkistdc.readthedocs.io/projects/graphql-client/en/latest/?badge=latest
   :alt: Documentation Status

A pythonic interface for making requests to a GraphQL server using
standard library or pydantic dataclasses to spare you from string manipulation.

Features
--------

-  Use standard library dataclasses to specify graphql parameters and responses

-  Use `pydantic <https://pypi.org/project/pydantic/>`__ dataclasses to
   specify graphql parameters and responses that have type validation

-  Create and execute GraphQL Queries based upon typed models

-  Create and execute GraphQL Mutations based upon typed models

-  Async support

Installation
------------

.. code:: bash

   pip install gqlclient

with ``asyncio`` support

.. code:: bash

   pip install gqlclient[async]

for developers

.. code:: bash

   pip install gqlclient[test]
   pip install pre-commit
   pre-commit install

Examples
--------

**Query**

.. code:: python

   from pydantic.dataclasses import dataclass

   from gqlclient import GraphQLClient

   @dataclass
   class Parameters:
       attr_one: str
       attr_two: int

   @dataclass
   class Response:
       attr_three: int
       attr_four: str

   client = GraphQLClient(gql_uri="http://localhost:5000/graphql")
   parameters = Parameters(attr_one="foo", attr_two=3)
   query = client.get_query(query_base="baseType", query_response_cls=Response, query_parameters=parameters)
   print(query)
   # {'query': '{baseType(filterParams: {attr_one: "foo", attr_two: 3}){attr_three, attr_four} }'}
   response = client.execute_gql_query(query_base="baseType", query_response_cls=Response, query_parameters=parameters, response_encoder=json_encoder)
   print(response)
   # with the default dataclass_encoder
   # [Response(attr_three=5, attr_four="bar")]

**Mutation**

.. code:: python

   from pydantic.dataclasses import dataclass

   from gqlclient import GraphQLClient


   @dataclass
   class Parameters:
       attr_one: str
       attr_two: int


   @dataclass
   class Response:
       attr_three: int
       attr_four: str

   client = GraphQLClient(gql_uri="http://localhost:5000/graphql")
   parameters = Parameters(attr_one="foo", attr_two=3)
   query = client.get_mutation(mutation_base="baseMutation", mutation_response_cls=Response, mutation_parameters=parameters)
   print(query)
   # {'query': 'mutation baseType {baseType(mutateParams: {attr_one: "foo", attr_two: 3}){attr_three, attr_four} }', 'operationName': 'baseType'}

   response = client.execute_gql_mutation(mutation_base="baseMutation", mutation_response_cls=Response, mutation_parameters=parameters)
   print(response)
   # with the default dataclass_encoder
   # [Response(attr_three=5, attr_four="bar")]

**Encoders**

.. code:: python

    from dataclasses import dataclass

    from gqlclient import GraphQLClient
    from gqlclient import json_encoder

    # set the default encoder to the json_encoder
    client = GraphQLClient(gql_uri="http://127.0.0.1:30003/graphql", response_encoder=json_encoder)

    @dataclass
    class QueryResponse:
        workflowId: int
        workflowName: str
        workflowDescription: str | None

    response = client.execute_gql_query("workflows",QueryResponse)
    print(response)
    # Response is a json formatted string
    # {"workflows": [{"workflowId": 1, "workflowName": "gql3_full - workflow_name", "workflowDescription": "gql3_full - workflow_description"}, {"workflowId": 2, "workflowName": "VBI base calibration", "workflowDescription": "The base set of calibration tasks for VBI."}]}

    from gqlclient import dataclass_encoder
    # for this call override the default encoder
    response = client.execute_gql_query("workflows", QueryResponse, response_encoder=dataclass_encoder)
    print(response)
    # Response type is a list of dataclasses
    # [QueryResponse(workflowId=1, workflowName='gql3_full - workflow_name', workflowDescription='gql3_full - workflow_description'), QueryResponse(workflowId=2, workflowName='VBI base calibration', workflowDescription='The base set of calibration tasks for VBI.')]


.. |codecov| image:: https://codecov.io/bb/dkistdc/graphql_client/branch/master/graph/badge.svg
   :target: https://codecov.io/bb/dkistdc/graphql_client
