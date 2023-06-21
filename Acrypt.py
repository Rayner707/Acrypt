import subprocess
import inquirer


def check_tool_availability(tool_name):
    result = subprocess.run(["which", tool_name], capture_output=True, text=True)
    return result.returncode == 0


def install_tool(tool_name):
    if tool_name == "hash-identifier":
        command = "apt-get install hash-identifier"
    elif tool_name == "hashcat":
        command = "apt-get install hashcat"
    else:
        print(f"No se puede instalar la herramienta '{tool_name}'.")
        return

    result = subprocess.run(command, shell=True)
    if result.returncode == 0:
        print(f"La herramienta '{tool_name}' se ha instalado correctamente.")
    else:
        print(f"No se pudo instalar la herramienta '{tool_name}'.")


def install_hash_identifier():
    if check_tool_availability("hash-identifier"):
        print("La herramienta 'hash-identifier' ya está instalada.")
    else:
        print("La herramienta 'hash-identifier' no está instalada.")
        install_prompt = input("¿Deseas instalar 'hash-identifier'? (Y/N): ")
        if install_prompt.lower() == "y":
            install_tool("hash-identifier")


def install_hashcat():
    if check_tool_availability("hashcat"):
        print("La herramienta 'hashcat' ya está instalada.")
    else:
        print("La herramienta 'hashcat' no está instalada.")
        install_prompt = input("¿Deseas instalar 'hashcat'? (Y/N): ")
        if install_prompt.lower() == "y":
            install_tool("hashcat")


def print_logo():
    logo = """
 
 
    █████╗   █████══╗ ██████═╗ ██╗   ██╗ ██████╗ ████████╗
   ██╔══██╗ ██    ██║ ██   ██║  ██╗ ██╔╝ ██╔══██╗╚══██╔══╝
   ███████║ ██        ██████╗    ████╔╝  ██████╔╝   ██║   
   ██╔══██║ ██    ██║ ██║  ██║    ██╔╝   ██╔═══╝    ██║   
   ██║  ██║ ╚█████╔╝  ██║  ██║    ██║    ██║        ██║   
   ╚═╝  ╚═╝  ╚════╝   ╚═╝  ╚═╝    ╚═╝    ╚═╝        ╚═╝    


                By Near7O7 with Diego555 and UthaGhoul
    https://github.com/Near707?tab=repositories
    """

    print(logo)


def main():
    print_logo()

    while True:
        tool_questions = [
            inquirer.List(
                "tool",
                message="Por favor, elige la herramienta",
                choices=["Hash-Creator", "Hash-Identifier", "Hashcat", "Salir"],
            ),
        ]
        tool = inquirer.prompt(tool_questions)["tool"]

        if tool == "Salir":
            break

        if tool == "Hash-Creator":
            text = input("Por favor, introduce el texto que quieres hashear: ")
            hash_type_questions = [
                inquirer.List(
                    "hash_type",
                    message="Por favor, elige el formato de hash",
                    choices=["md5", "sha1", "sha256", "sha512"],
                ),
            ]
            hash_type = inquirer.prompt(hash_type_questions)["hash_type"]

            # Obtener el hash
            hash_value = get_hash(text, hash_type)
            print(f"Hash: {hash_value}")

            # Preguntar si desea guardar el hash
            save_hash_prompt = inquirer.prompt([
                inquirer.Confirm("save_hash", message="¿Deseas guardar el hash?")
            ])["save_hash"]

            if save_hash_prompt:
                file_name = input("Por favor, introduce el nombre del archivo donde quieres guardar el hash: ")
                save_hash(hash_value, file_name)
            else:
                continue_prompt = input("¿Deseas usar otra herramienta? (S/N): ")
                if continue_prompt.lower() != "s":
                    break

        elif tool == "Hash-Identifier":
            hash_string = input("Por favor, introduce el hash que quieres identificar: ")
            result = identify_hash(hash_string)
            print(result)

        elif tool == "Hashcat":
            install_hashcat()
            run_hashcat()

        continue_prompt = input("¿Deseas usar otra herramienta? (S/N): ")
        if continue_prompt.lower() != "s":
            break


def get_hash(text, hash_type):
    hash_command = {
        "md5": "md5sum",
        "sha1": "sha1sum",
        "sha256": "sha256sum",
        "sha512": "sha512sum",
        # Add more here
    }

    command = hash_command.get(hash_type)

    if not command:
        print(f"No se encontró el hash de tipo '{hash_type}'. Por favor, elige otro.")
        return

    result = subprocess.run(
        f'echo -n "{text}" | {command} | tr -d " -"',
        shell=True,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Hubo un error al ejecutar el comando.")
        return

    hash_value = result.stdout.strip()
    return hash_value


def save_hash(hash_value, file_name):
    with open(file_name, "w") as f:
        f.write(hash_value)

    print(f"Se ha guardado el hash en el archivo '{file_name}'.")


def identify_hash(text):
    command = f'echo "{text}" | hash-identifier'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip()

    # Obtener las líneas del resultado
    output_lines = output.split("\n")

    # Eliminar las primeras 12 líneas (logo)
    cleaned_lines = output_lines[12:]

    # Unir las líneas limpias nuevamente en una sola cadena de texto
    cleaned_output = "\n".join(cleaned_lines)

    return cleaned_output


def run_hashcat():
    hash_modes = {
        "MD5": 0,
        "SHA-1": 100,
        "SHA-256": 1400,
        "SHA-512": 1700,
        "HMAC-MD5": 50,
        "HMAC-SHA1": 110,
        "HMAC-SHA256": 1450,
        "HMAC-SHA512": 1750,
        "bcrypt": 3200,
        "NTLM": 1000,
        "LM": 3000,
        "MySQL": 300,
        "MSSQL": 131,
        "Cisco PIX": 2400,
        "WPA/WPA2": 2500,
    }

    attack_modes = {
        "Ataque de diccionario": 0,
        "Ataque de fuerza bruta": 1,
        "Ataque de fuerza bruta combinado": 2,
        "Ataque de máscara": 3,
        "Ataque de permutación": 4,
        "Ataque de tabla de arco iris": 5,
        "Ataque de generación personalizada": 6,
        "Ataque de mangle": 7,
        "Ataque híbrido de diccionario + máscara": 8,
        "Ataque híbrido de diccionario + reglas": 9,
        "Ataque híbrido de máscara + diccionario": 10,
        "Ataque híbrido de máscara + reglas": 11,
    }

    hash_type_questions = [
        inquirer.List(
            "hash_type",
            message="Por favor, elige el tipo de hash",
            choices=list(hash_modes.keys()),
        ),
    ]
    hash_type = inquirer.prompt(hash_type_questions)["hash_type"]

    attack_mode_questions = [
        inquirer.List(
            "attack_mode",
            message="Por favor, elige el modo de ataque",
            choices=list(attack_modes.keys()),
        ),
    ]
    attack_mode = inquirer.prompt(attack_mode_questions)["attack_mode"]

    hash_file = input("Por favor, introduce el archivo de hashes: ")
    dictionary_file = input("Por favor, introduce el archivo de diccionario: ")

    hash_mode = hash_modes.get(hash_type)
    attack_mode = attack_modes.get(attack_mode)

    command = f"hashcat -a {attack_mode} -m {hash_mode} {hash_file} {dictionary_file}"
    result = subprocess.run(command, shell=True)

    if result.returncode != 0:
        print("Hubo un error al ejecutar el comando.")
    else:
        print("El proceso de hashcat se ha completado.")


if __name__ == "__main__":
    main()
