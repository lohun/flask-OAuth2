from src import createApp, db

if __name__ == "__main__":
    app = createApp()
    app.run(port=5000, debug=True)

