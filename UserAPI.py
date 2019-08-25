'''
    This UserAPI script would act as the GraphQL API server.
    It would be used as an API.
    Internally it would call Schema script to handle different API schema call.
'''

import falcon
import json
from wsgiref import simple_server
from Schema import getUserDetailsInfo

class RestRequestHelper:

    def getRequestValue(self,req,resp):

        try:

            if req.content_length in (None, 0):
                resp.status = falcon.HTTP_400
                resp.body = json.dumps(
                    {"errors": [{"message": "POST body sent invalid JSON."}]},
                    separators=(',', ':')
                )
                return

            body = req.bounded_stream.read()

            if not body:
                raise falcon.HTTPBadRequest('Empty request body','A valid query is required.')

            queryValue = json.loads(body.decode('utf-8'))

            # Please note if you using postman to do the query you need to make sure you are fetching
            #       only the query part from the dictionary. Because in this case dict value comes up as per below
            # {'query': 'query allUsers {\r\n          user {\r\n            id\r\n            name\r\n            email\r\n          }\r\n        }'}
            # Out of this dict you would only require to send the query to fetch the result.

            print(queryValue)

            return queryValue["query"]

        except Exception as error:
            print(error)
            raise falcon.HTTPBadRequest('Wrong format in request','A valid query is required.')


class UserManagerResource:

  restRequestHelper = None

  def __init__(self):

      self.restRequestHelper = RestRequestHelper()

  '''
      only on_post() method has been implemented.
      Because we would always require to pass value in request body from client
  '''
  def on_post(self, req, resp):

      try:

          # Fetch read the request
          requestQuery = self.restRequestHelper.getRequestValue(req,resp)

          # read and decode request body
          userDetails = getUserDetailsInfo(str(requestQuery))

          print("userDetails",userDetails)

          resp.status = falcon.HTTP_200
          resp.content_type = falcon.MEDIA_JSON
          resp.body = json.dumps({"result": "success", "details": userDetails})

      except Exception as error:

          print(error)
          resp.status = falcon.HTTP_500
          resp.body = json.dumps({"result": "failed", "details": falcon.HTTPInternalServerError("Unable to fetch user details !")})


appManager = falcon.API()
userManagerResourceObj = UserManagerResource()
appManager.add_route("/manage/user/graphql/info",userManagerResourceObj)


if __name__ == '__main__':
    httpd = simple_server.make_server('0.0.0.0', 8000, appManager)
    print("API has been started and listening on http://0.0.0.0:8000/manage/user/graphql/info")
    httpd.serve_forever()