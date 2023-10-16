"""
    This module build the graphql client
"""
from python_graphql_client import GraphqlClient
from ramda import path_or, is_empty


class GraphQLExecutor:
    """
    graphql excecuter
    """

    def __init__(self, client):
        """Initalizer for GraphQLClient which initializes Gr

        Args:
            client (object): GraphqlClient object that request to the graphql endpoint
        """
        self.client = client

    def execute(self, query, variables):
        """
        excecute the query
        """
        return self.client.execute(query=query, variables=variables)

    def execute_query(self, data):
        """
        excecute the query
        """
        query = path_or("", ["query"], data)
        variables = path_or({}, ["variables"], data)
        return self.execute(query, variables)


class GraphQLClientBuilder:
    """Main class for graphql client builder which builds the url and token"""

    def __init__(self, env_varaibles, prefix="application"):
        """Initalizer for GraphQlClientBuilder which initializes url and token

        Args:
            env_varaibles (dict): contains all the env variables
            prefix (str, optional): config which used to get url and token from env . \
                Defaults to 'servicing'.
        """
        if not is_empty(prefix):
            prefix = prefix + "_"
        # prefix should be 'application' or servicing
        self.graphql_endpoint = path_or(
            "", [prefix + "graphql_endpoint"], env_varaibles
        )
        self.auth_token = path_or("", [prefix + "graphql_auth_token"], env_varaibles)

    def get_endpoint(self):
        """Function which returns the graphq endpoint url from env

        Returns:
            string: Returns the graphql endpoint url
        """
        return self.graphql_endpoint

    def get_auth_token(self):
        """Function which returns the graphql auth token frome env

        Returns:
            string: Returns the graphql auth token
        """
        return self.auth_token


class GraphQlClient(GraphQLClientBuilder):
    """Class for handling graphql client

    Args:
        GraphQLClientBuilder (Class): Initalizing class graphql client which forms \
            url and auth token
    """

    def get_client(self):
        """Function which returns the graphql client

        Returns:
            dict:instance of graphql client with url and auth token connected
        """
        return GraphQLExecutor(
            GraphqlClient(
                endpoint=self.get_endpoint(),
                headers={"x-hasura-admin-secret": self.get_auth_token()},
            )
        )

    def respose_as_json(self, response):
        """Function which returns the response as json

        Args:
            response (dict): contains the response

        Returns:
            JSONB: returns the response as json
        """
        return response.json()
