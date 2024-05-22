#!/usr/bin/python3
"""
A simple Flask web application that displays different messages
"""


from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Route to display 'Hello HBNB!' at the root URL.
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Route to display 'HBNB' at the /hbnb URL.
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """
    Route to display 'C ' followed by the value
    Replaces underscores in text with spaces.
    """
    text = text.replace('_', ' ')
    return f"C {text}"


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text):
    """
    Route to display 'Python ' followed
    Replaces underscores in text with spaces.
    Default value of text is 'is cool'.
    """
    text = text.replace('_', ' ')
    return f"Python {text}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
