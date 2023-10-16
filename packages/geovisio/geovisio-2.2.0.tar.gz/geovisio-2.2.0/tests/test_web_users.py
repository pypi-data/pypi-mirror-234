def test_unlogged_user_retrieval_without_oauth(client):
    """it should be impossible to access current user info if the instance has no oauth"""
    response = client.get("/api/users/me")
    assert response.status_code == 403
