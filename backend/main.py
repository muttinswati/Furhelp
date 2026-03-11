# main.py
from file import app  # base routes
import file2       # extra routes

if __name__ == "__main__":
    app.run(debug=True)
