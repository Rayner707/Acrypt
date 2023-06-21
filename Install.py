import subprocess
import inquirer


def get_linux_distribution():
    try:
        with open('/etc/os-release', 'r') as file:
            for line in file:
                if line.startswith('ID='):
                    return line.split('=')[1].strip().strip('"')
    except FileNotFoundError:
        return None

    return None


def check_tool_availability(tool_name):
    result = subprocess.run(["which", tool_name], capture_output=True, text=True)
    if result.returncode == 0:
        return True
    else:
        return False


def install_hash_identifier():
    linux_distribution = get_linux_distribution()

    if linux_distribution == "ubuntu":
        subprocess.run(["sudo", "apt", "install", "hash-identifier"])
    elif linux_distribution == "fedora":
        subprocess.run(["sudo", "dnf", "install", "hash-identifier"])
    elif linux_distribution == "arch":
        subprocess.run(["sudo", "pacman", "-S", "hash-identifier"])
    else:
        print("No se puede determinar la distribución de Linux. No se puede realizar la instalación de hash-identifier.")


def install_hashcat():
    linux_distribution = get_linux_distribution()

    if linux_distribution == "ubuntu":
        subprocess.run(["sudo", "apt", "install", "hashcat"])
    elif linux_distribution == "fedora":
        subprocess.run(["sudo", "dnf", "install", "hashcat"])
    elif linux_distribution == "arch":
        subprocess.run(["sudo", "pacman", "-S", "hashcat"])
    else:
        print("No se puede determinar la distribución de Linux. No se puede realizar la instalación de hashcat.")


def main():
    linux_distributions = ["ubuntu", "fedora", "arch", "debian", "opensuse"]

    distribution_questions = [
        inquirer.List(
            "distribution",
            message="Por favor, selecciona tu distribución de Linux:",
            choices=linux_distributions,
        ),
    ]

    distribution = inquirer.prompt(distribution_questions)["distribution"]

    hash_identifier_available = check_tool_availability("hash-identifier")
    hashcat_available = check_tool_availability("hashcat")

    if not hash_identifier_available:
        install_hash_identifier()

    if not hashcat_available:
        install_hashcat()

    print("Proceso completado.")


if __name__ == "__main__":
    main()
