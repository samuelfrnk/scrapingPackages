import subprocess
import os
import re
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm



def scrape_package_name(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        pip_command_tag = soup.find('span', id='pip-command')

        if pip_command_tag:
            pip_command = pip_command_tag.text.strip()
            package_name = pip_command.split(' ')[-1]
            return package_name
        else:
            print("Pip install command not found.")
            return None
    except requests.RequestException as e:
        print(f"An error occurred while fetching the PyPI page: {e}")
        return None


def install_package_and_get_name(package_name, env_path):
    """
    Install a package in the specified virtual environment using Bash script and retrieve its name.
    """
    bash_script_path = os.path.join(os.path.dirname(__file__), "get_package_name.sh")
    result = subprocess.run(["bash", bash_script_path, package_name, env_path], capture_output=True, text=True, check=True)
    return result.stdout.strip()

def perform_import_search(file_name):
    """
    Process the file to install packages, retrieve their names, and save to a single file.
    """
    with open(file_name, 'r') as file:
        content = file.read()
    path_to_script = os.path.join(".", "get_package_name.sh")
    urls = re.findall(r'URL: (\S+)', content)
    package_names = []

    for url in tqdm(urls, desc='Find package name'):
        package_names.append(scrape_package_name(url))

    index_of_results = file_name.index("results")  # Finds the first occurrence of 'results'
    output_file_name = file_name[:index_of_results] + "import name results.txt"

    last_line_output = {}
    for package_name in tqdm(package_names, desc='Processed packages'):
        arg_list = list(map(str, ["./get_package_name.sh", package_name]))
        # Run the subprocess and capture the output
        proc = subprocess.Popen(arg_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = proc.communicate()
        if stdout:
            # Extract the last line from stdout
            last_line = stdout.strip().split('\n')[-1]
            last_line_output[package_name] = last_line
        else:
            # If there's no stdout, you might want to handle errors or store an error message
            last_line_output[package_name] = "No output or error occurred"

    with open(output_file_name, 'w') as output_file:
        for package_name, last_line in last_line_output.items():
            output_file.write(f"{package_name}: {last_line}\n")



def main():

    file_name = input("Enter the file name used to find the import statements: ")
    perform_import_search(file_name)


if __name__ == "__main__":
    main()
