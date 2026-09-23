from app.routes.routes import app

if __name__ == '__main__':
    # Run the Flask app on port 5001
    app.run(port=5001, debug=True)