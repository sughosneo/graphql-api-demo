'''
    In this script we would define the specific GraphQL schema.
    In this script we would mock the sample data. In actual production scenario the data would get returned from data source.
'''

import pytest
import graphene

'''
    Schema Definitions
'''
class User(graphene.ObjectType):

    id = graphene.ID()
    name = graphene.String()
    email = graphene.String()

class Query(graphene.ObjectType):

    user = graphene.Field(User)

    def resolve_user(self, info):
        return User(id=1, name="Sumit", email="sumit@abc.com")


schema = graphene.Schema(query=Query)

'''
    Below are the methods which would get referenced by other scripts to pull the information. 
'''
def getUserDetailsInfo(query):

    if query :
        print(query)
        result = schema.execute(query)
    else:
        raise ValueError

    return result.data
'''
    Test method which would help to test out the User Details.
'''
def test_query():

    print(schema)
    query = """
        query allUsers {
          user {
            id
            name
            email
          }
        }
    """

    print(query)
    result = schema.execute(query)
    assert not result.errors
    assert result.data == {"user": {"id": "1", "name": "Sumit", "email": "sumit@abc.com"}}
