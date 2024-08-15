from flask import current_app as app, render_template, request, jsonify
import subprocess
import threading

lock = threading.Lock()

# Array de pessoas
people = [
    {
        "uid": "00 00 00 00",
        "name": "John Doe",
        "age": 30,
        "email": "johndoe@example.com",
        "photo_path": "/static/images/Minecraft-creeper.avif"
    },
    {
        "uid": "E7 E1 9A 47",
        "name": "Andre Chang",
        "age": 39,
        "email": "andrechangn@example.com",
        "photo_path": "/static/images/Minecraft-creeper.avif"
    },
    {
        "uid": "49 36 8A 93",
        "name": "Joao Pedro",
        "age": 20,
        "email": "joaopedro@example.com",
        "photo_path": "/static/images/Minecraft-creeper.avif"
    }
]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/execute', methods=['POST'])
def execute():
    try:
        result = subprocess.run(["/home/text/Documents/proxymark/proxmark3/pm3","-c", "hf search"], capture_output=True, text=True)

        uid_line = ""
        for line in result.stdout.splitlines():
            if "UID" in line:
                uid_line = line.strip()
                break

        print(f"UID line found: {uid_line}")

        uid = uid_line.split(":")[1].strip() if uid_line else ""
        print(f"Extracted UID: {uid}")

        uid_parts = uid.split()[:4]
        formatted_uid = " ".join(uid_parts)
        print(f"Extracted and formatted UID: {formatted_uid}")

        try:
            with open("uid_person.txt", "w") as file:
                file.write(f"{formatted_uid}\n")
                print("UID added to uid_person.txt")
        except Exception as file_error:
            print(f"Error writing to file: {str(file_error)}")

        person = next((p for p in people if p["uid"] == formatted_uid), None)
        print(person)
        if person:
            print(f"Person found: {person}")
            return jsonify(person)
        else:
            print("UID not found")
            return jsonify({"error": "UID Not Found"}), 404
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "An error occurred during the opening the door", "details": str(e)}), 500


@app.route('/execute_dump', methods=['POST'])
def execute_dump():
    try:
        
        result_UID = subprocess.run(["/home/text/Documents/proxymark/proxmark3/pm3","-c", "hf search"], capture_output=True, text=True)

        uid_line = ""
        for line in result_UID.stdout.splitlines():
            if "UID" in line:
                uid_line = line.strip()
                break
        uid = uid_line.split(":")[1].strip() if uid_line else ""
        
        uid_parts = uid.split()[:4]
        formatted_uid = " ".join(uid_parts)
        print(f"Extracted and formatted UID: {formatted_uid}")

        try:
            with open("uid_person.txt", "w") as file:
                file.write(f"{formatted_uid}\n")
                print("UID added to uid_person.txt")
        except Exception as file_error:
            print(f"Error writing to file: {str(file_error)}")

        result = subprocess.run(["/home/text/Documents/proxymark/proxmark3/pm3", "-c","hf mf dump -k /home/text/Documents/development/proxymark/hf-mf-key.bin -f dump/teste.bin"], capture_output=True, text=True)
    
        full_output = result.stdout
        print(full_output)

        part1_start = "[=] ................."
        part1_end = "[+] time:"
        part1_content = ""

        if part1_start in full_output and part1_end in full_output:
            part1_content = full_output.split(
                part1_start)[-1].split(part1_end)[0].strip()

        separator = "[=] -----+-----+-------------------------------------------------+-----------------"
        part2_content = ""

        separator_occurrences = full_output.split(separator)
        print("Number of Separator Occurrences:", len(separator_occurrences))

        if len(separator_occurrences) > 3:
            # part2_content = separator + separator_occurrences[2] + separator + separator_occurrences[3].split(separator)[0].strip()
            # part2_header = separator + separator_occurrences[1] + separator + separator_occurrences[1].split(separator)[0].strip()
            
            part2_header = "[=] -----+-----+-------------------------------------------------+-----------------\n[=]  sec | blk | data                                            | ascii           \n"

            relevant_content = part2_header + separator + separator_occurrences[2] + separator + separator_occurrences[3]
            part2_content = relevant_content.split("[+] Saved")[0].strip()

            print("Part 2 Content:")
            print(part2_content)  # Log de depuração para part2

            # print("Part 2 Header:")
            # print(part2_header)
        else:
            print("Separator not found enough times in the output.")

        # Defina o usuário que irá executar o comando
        user = "text"

        # Comando a ser executado
        find_command = [
            "sudo",
            "-u", user,
            "find", "/home/text/dump", "-name", "test.bin", "-type", "f", "-delete"
        ]

        # Procurar e deletar o arquivo test.bin
        # find_command = "sudo -u findeuser find /home/text -name test.bin -type f -delete"
        find_result = subprocess.run(
            find_command, capture_output=True, text=True)

        if find_result.returncode == 0:
            print("Arquivo test.bin deletado com sucesso")
        else:
            print(f"Erro ao deletar arquivo: {find_result.stderr}")

        return jsonify({"part1": part1_content, "part2": part2_content}) if result.stdout else "No output from command"
    except Exception as e:
        print(f"Error: {str(e)}")  # Log de erro
        return jsonify({"error": "An error occurred during the dumping the data", "details": str(e)}), 500


@app.route('/execute_clone', methods=['POST'])
def execute_clone():
    try:
        # Ler o UID do arquivo uid_person.txt
        with open("uid_person.txt", "r") as file:
            last_uid = file.readlines()[-1].strip().replace(" ", "")
        print(f"Last UID from file: {last_uid}")

        # Comando para clonar os dados do cartão
        clone_command_data = [
            "/home/text/Documents/proxymark/proxmark3/pm3",
            "-c",
            f"hf mf restore -k /home/text/Documents/development/proxymark/hf-mf-key.bin -f dump/teste.bin"
        ]
        
        # Executar o comando de restauração
        subprocess.run(clone_command_data, check=True)
        print("Dump restored successfully.")
        
        #===
        
        # Comando para alterar o UID do cartão
        clone_command_uid = [
            "/home/text/Documents/proxymark/proxmark3/pm3",
            "-c",
            f"hf mf csetuid -u {last_uid}"
        ]

        # Executar o comando de alteração de UID
        subprocess.run(clone_command_uid, check=True)
        print("UID changed successfully.")
        
        #===
        
        # Verificação do cartão clonado
        check_command = [
            "/home/text/Documents/proxymark/proxmark3/pm3",
            "-c",
            "hf mf chk"
        ]

        result = subprocess.run(check_command, capture_output=True, text=True)
        print(result.stdout)  # Output do comando
        
        return jsonify({"status": "Cloning successful"})
        
    except Exception as e:
        print(f"Error: {str(e)}")  # Log de erro
        return jsonify({"error": "An error occurred during the Clone", "details": str(e)}), 500


@app.route('/execute_wipe', methods=['POST'])
def execute_wipe():
    try:
        # Comando para limpar o cartão usando o arquivo de chave fornecido
        wipe_command = [
            "/home/text/Documents/proxymark/proxmark3/pm3",
            "-c",
            "hf mf wipe -f /home/text/Documents/development/proxymark/hf-mf-key.bin"
        ]

        # Executar o comando de wipe
        subprocess.run(wipe_command, check=True)
        print("Card wiped successfully.")

        # Comando para alterar o UID para 00000000
        setuid_command = [
            "/home/text/Documents/proxymark/proxmark3/pm3",
            "-c",
            "hf mf csetuid -u 00000000"
        ]

        # Executar o comando de alteração de UID
        subprocess.run(setuid_command, check=True)
        print("UID set to 00000000 successfully.")

        # Retornar uma resposta de sucesso
        return jsonify({"status": "Wipe and UID change successful"}), 200

    except subprocess.CalledProcessError as e:
        print(f"Error during wipe or UID change: {str(e)}")
        return jsonify({"error": "An error occurred during the wipe or UID change", "details": str(e)}), 500

@app.route('/person')
def person():
    uid = request.args.get('uid')
    person = next((p for p in people if p["uid"] == uid), None)
    if person:
        return render_template('person.html', person=person)
    else:
        return "Person not found", 404
