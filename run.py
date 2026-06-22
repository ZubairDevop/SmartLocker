from app import create_app
#script to simply run application.
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
