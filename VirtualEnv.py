import subprocess
import os
import virtualenv
import re
from bs4 import BeautifulSoup
import requests


def create_virtual_environment(env_name):
    """Create a virtual environment."""
    if not os.path.exists(env_name):
        virtualenv.create_environment(env_name)


def scrape_pip_install_command(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        pip_command_tag = soup.find('span', id='pip-command')

        if pip_command_tag:
            pip_command = pip_command_tag.text.strip()
            return pip_command
        else:
            print("Pip install command not found.")
            return None
    except requests.RequestException as e:
        print(f"An error occurred while fetching the PyPI page: {e}")
        return None

def install_package_and_get_name(package_name, env_path):
    """
    Install a package in the specified virtual environment and retrieve its name.
    """
    pip_executable = os.path.join(env_path, 'bin', 'pip')
    # Install the package
    subprocess.run([pip_executable, 'install', package_name], check=True)
    # Run `pip show` and extract the package name
    result = subprocess.run([pip_executable, 'show', package_name], capture_output=True, text=True, check=True)
    name_line = [line for line in result.stdout.split('\n') if line.startswith('Name:')][0]
    return name_line.split(': ')[1]

def perform_import_search(file_name, env_name="temp_env"):
    """
    Process the file to install packages, retrieve their names, and save to a single file.
    """
    #create_virtual_environment(env_name)
    with open(file_name, 'r') as file:
        content = file.read()

    urls = re.findall(r'URL: (\S+)', content)
    package_names = []
    for url in urls:
        print(url + ": installed which gave command "+ scrape_pip_install_command(url) + "\n")
        package_install_name = scrape_pip_install_command(url)
        #package_name = install_package_and_get_name(package_install_name, env_name)
        #package_names.append(package_name)

    # Save the package names to a single file
    #with open("all_import_names.txt", 'w') as file:
    #    for name in package_names:
    #        file.write(name + "\n")


def main():

    file_name = input("Enter the file name used to find the import statements: ")
    perform_import_search(file_name)


if __name__ == "__main__":
    main()
