from app import create_app
# these test are for Unit Testing, Functional Testing ,Authentication Testing and Regression Testing


# Pytest checks Flask app loads successfully.
def test_home_page_loads():
    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Smart Locker" in response.data

# Pytest to check Login page loads
def test_login_page_loads():

    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()

    response = client.get("/login")

    assert response.status_code == 200
    assert b"Login" in response.data

# valid user login test
def test_valid_user_login():

    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    client = app.test_client()

    response = client.post(
        "/login",
        data={
            "email": "peterp123@cgi.com",
            "password": "Password123!"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"User Dashboard" in response.data    

# an invalid login test.
def test_invalid_login_rejected():

    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    client = app.test_client()

    response = client.post(
        "/login",
        data={
            "email": "user123@cgi.com",
            "password": "Password900!"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Invalid email or password" in response.data

# pytest to verify an unauthenticated user cannot access the Admin Dashboard.
# this proves Authentication Control, Authorisation Control, Access Control
def test_admin_dashboard_requires_login():

    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()

    response = client.get(
        "/admin/",
        follow_redirects=False
    )

    assert response.status_code == 302

    assert "/login" in response.location


# test for successful admin login with correct credentials
def test_valid_admin_login():

    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    client = app.test_client()

    response = client.post(
        "/login",
        data={
            "email": "zubaira123@cgi.com",
            "password": "Password123!"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Admin Dashboard" in response.data    


# this test is to prove RABC (Role Based Access Control)
# registered standard user can access Admin dashboard
def test_user_cannot_access_admin_dashboard():

    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    client = app.test_client()

    client.post(
        "/login",
        data={
            "email": "stever123@cgi.com",
            "password": "Password123!"
        },
        follow_redirects=True
    )

    response = client.get(
        "/admin/",
        follow_redirects=False
    )

    assert response.status_code == 403    

    # to run test type  python -m pytest on terminal when in virtual envoirment
    # Github actions will run this automatically