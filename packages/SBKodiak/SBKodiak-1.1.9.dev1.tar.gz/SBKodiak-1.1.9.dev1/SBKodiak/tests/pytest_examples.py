from test_app import *

def test_request_example(client):
    response = client.get("/posts")
    assert b"<h2>Hello, World!</h2>" in response.data


# def test_json_data(client):
#     response = client.post("/graphql",
#                            json={ "query": """
#                                             query User($id: String!) {
#                                                 user(id: $id) {
#                                                     name
#                                                     theme
#                                                     picture_url
#                                                 }
#                                             }
#                                         """,
#                                     "variables"={"id": 2}
#                 })
#     assert response.json["data"]["user"]["name"] == "Flask"