# server.py

from flask import Flask

# Create the Flask app
app=Flask(__name__,template_folder='templates')
app.secret_key = 'your_secret_key_here'  # if you use sessions

if __name__ == "__main__":
    app.run(debug=True, port=5000)



