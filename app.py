import json
from time import sleep

from flask import Flask, render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv
import os

from pdf_util import extract_text_from_pdf

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))
modelo = "gpt-4"

app = Flask(__name__)
app.secret_key = 'profchat'


def bot(prompt):
    max_retries = 1
    rep = 0

    while True:
        try:
            prompt_system = f"""
                Voce é um chatbot de analise, entendimento, sugestões e correções de
                provas, exercícios e atividades de alunos.
                Voce não deve responder perguntas que não sejam sobre conteudos de estudantes informados.
            """

            response = cliente.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": prompt_system
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=1,
                max_tokens=300,
                top_p=1,
                frequency_penalty=0,
                model=modelo
            )
            return response
        except Exception as error:
            rep += 1
            if rep >= max_retries:
                return "Cant connect to OpenAI"
            print("Error communicating with OpenAI...")
            sleep(1)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    question = request.form.get("msg")
    response = bot(question)

    # Retrieve file if any
    file = request.files.get('file')
    file_content = ""
    if file:
        filename = file.filename.lower()
        if filename.endswith('.pdf'):
            # Handle PDF parsing
            file_content = extract_text_from_pdf(file)
            print("pdf")
            print(file_content)
        elif filename.endswith('.txt'):
            # Handle TXT reading
            file_content = file.read().decode('utf-8', errors='ignore')
        else:
            # Handle other file types or raise an error
            file_content = file.read().decode('utf-8', errors='ignore')

    return json.dumps(response.choices[0].message.content)


if __name__ == "__main__":
    app.run(debug=True)
