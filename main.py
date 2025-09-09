from src import createApp, db

app = createApp()
if __name__ == "__main__":
    app.run(port=5000, debug=True)

