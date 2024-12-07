import json
from crypt import methods

from click import prompt
from flask import Flask,render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))
modelo = "gpt-4"

app = Flask(__name__)
app.secret_key = 'profchat'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods = ["POST"])
def chat():
    question = request.get_json().get("msg")

    resp = cliente.chat.completions.create(
        model=modelo,
        temperature=1.0,
        messages=[
            {"role": "user", "content": question}
        ]
    )

    return json.dumps(resp.choices[0].message.content)

if __name__ == "__main__":
    app.run(debug = True)
