def load(filename):
    try:
        with open(filename, "r") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Error loading file: {e}")


def save(filename, content):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
    except IOError as e:
        print(f"Error saving file: {e}")
