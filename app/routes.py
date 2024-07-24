# from flask import current_app as app, render_template, request, jsonify
# import subprocess

# # Array de pessoas
# people = [
#     {
#         "uid": "08 11 33 3E",
#         "name": "John Doe",
#         "age": 30,
#         "email": "johndoe@example.com"
#     }
# ]

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/execute', methods=['POST'])
# def execute():
#     try:
#         # Usar o caminho completo do script pm3
#         result = subprocess.run(["/home/text/Documents/proxymark/proxmark3/pm3", "-c", "hf search"], capture_output=True, text=True)
        
#         # Verificar se a saída contém "UID" e retornar essa linha
#         uid_line = ""
#         for line in result.stdout.splitlines():
#             if "UID" in line:
#                 uid_line = line.strip()
#                 break
        
#         print(f"UID line found: {uid_line}")  # Log para depuração

#         # Extrair o UID da linha
#         uid = uid_line.split(":")[1].strip() if uid_line else ""
#         print(f"Extracted UID: {uid}")  # Log para depuração

#         # Verificar se o UID corresponde a uma pessoa
#         person = next((p for p in people if p["uid"] == uid), None)
        
#         if person:
#             return jsonify(person)
#         else:
#             return "UID not found", 404
#     except Exception as e:
#         print(f"Error: {str(e)}")  # Log de erro
#         return str(e), 500

# @app.route('/person/<uid>')
# def person(uid):
#     person = next((p for p in people if p["uid"] == uid), None)
#     if person:
#         return render_template('person.html', person=person)
#     else:
#         return "Person not found", 404

from flask import current_app as app, render_template, request, jsonify
import subprocess

# Array de pessoas
people = [
    {
        "uid": "08 11 33 3E",
        "name": "John Doe",
        "age": 30,
        "email": "johndoe@example.com"
    },
    {
        "uid": "08 11 33 3A",
        "name": "Kevin Yun",
        "age": 39,
        "email": "kevinyun@example.com"
    }
]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/execute', methods=['POST'])
def execute():
    try:
        # Usar o caminho completo do script pm3
        result = subprocess.run(["/home/text/Documents/proxymark/proxmark3/pm3","-c", "hf search"], capture_output=True, text=True)

        # Verificar se a saída contém "UID" e retornar essa linha
        uid_line = ""
        for line in result.stdout.splitlines():
            if "UID" in line:
                uid_line = line.strip()
                break

        print(f"UID line found: {uid_line}")  # Log para depuração

        # Extrair o UID da linha
        uid = uid_line.split(":")[1].strip() if uid_line else ""
        print(f"Extracted UID: {uid}")  # Log para depuração
        
        uid_parts = uid.split()[:4]
        formatted_uid = " ".join(uid_parts)
        print(f"Extracted and formatted UID: {formatted_uid}")  # Log para depuração

        # Verificar se o UID corresponde a uma pessoa
        person = next((p for p in people if p["uid"] == formatted_uid), None)
        print(person)
        if person:
            print(f"Person found: {person}")  # Log para depuração
            return jsonify(person)
        else:
            print("UID not found")  # Log para depuração
            return "UID Not Found", 404
    except Exception as e:
        print(f"Error: {str(e)}")  # Log de erro
        return str(e), 500


@app.route('/execute_dump', methods=['POST'])
def execute_dump():
    try:
        # Usar o caminho completo do script pm3 para o segundo comando
        result = subprocess.run(["/home/text/Documents/proxymark/proxmark3/pm3", "-c",
                                "hf mf dump -k /home/text/Documents/development/proxymark/hf-mf-key.bin -f teste.bin"], capture_output=True, text=True)

        print(result.stdout)  # Log para depuração
        
        # Procurar e deletar o arquivo test.bin
        find_command = "find /home -name test.bin -type f -delete"
        find_result = subprocess.run(
            find_command, shell=True, capture_output=True, text=True)
        if find_result.returncode == 0:
            print("Arquivo test.bin deletado com sucesso")
        else:
            print(f"Erro ao deletar arquivo: {find_result.stderr}")
        
        return result.stdout if result.stdout else "No output from command"
    except Exception as e:
        print(f"Error: {str(e)}")  # Log de erro
        return str(e), 500


@app.route('/person')
def person():
    uid = request.args.get('uid')
    person = next((p for p in people if p["uid"] == uid), None)
    if person:
        return render_template('person.html', person=person)
    else:
        return "Person not found", 404
