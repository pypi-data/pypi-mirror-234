"""
    This module handles the update
"""

class RunQuery:
    """
    This class will update the data
    """

    def run_query(self, query_data):
        """
        This function will run the query
        """
        #print("=======updating==>", query_data) # print will be removed after testing
        res = self.graphql_client.execute_query(query_data)
        #print("Response ==>", res) # print will be removed after testing
        return res

    def excecute_for_single_query_data(self, query_data: dict):
        """
        This function will update the data
        single data : dict
        """
        return self.run_query(query_data)

    def excecute_for_list_of_query_data(self, query_datas: list):
        """
        This function will update all the data
        """
        result = []
        for query_data in query_datas:
            result.append(self.excecute_for_single_query_data(query_data))
        return result
