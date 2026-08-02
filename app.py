from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Cloud Native DevSecOps CI/CD Platform</h1>
    <h2>Welcome to My Flask Application</h2>
    <p>Created by Bhumika Deshmukh</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

GITHUB_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"
