from app import create_app

# Admin requests page workflow
def test_admin_requests_page_requires_login():

    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()

    response = client.get(
        "/admin/requests",
        follow_redirects=False
    )

    assert response.status_code == 302
    assert "/login" in response.location

# User dashboard workflow
def test_user_dashboard_requires_login():

    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()

    response = client.get(
        "/user/",
        follow_redirects=False
    )

    assert response.status_code == 302
    assert "/login" in response.location

## User can access dashboard and request replacement laptop
def test_logged_in_user_can_access_dashboard():

    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    client = app.test_client()

    client.post(
        "/login",
        data={
            "email": "brucew123@cgi.com",
            "password": "Password123!"
        },
        follow_redirects=True
    )

    response = client.get("/user/")

    assert response.status_code == 200
    assert b"User Dashboard" in response.data