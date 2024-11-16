from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello() -> str:
    return 'Start of vehicle creation - round 3!'