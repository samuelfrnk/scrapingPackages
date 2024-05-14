import os
import time
import requests
import matplotlib.pyplot as plt

headers = {'Authorization': 'Bearer YOUR_SUPER_SECRET_TOKEN'}


def search_github(package_name):
    """ Search GitHub for the number of code occurrences using the GitHub API. """
    query = f"import {package_name} in:file language:python"
    url = f"https://api.github.com/search/code?q={query}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['total_count']
    else:
        print(f"Failed to fetch data for {package_name}: {response.status_code}")
        print(response.reason)
        print(response.json())
        return 0


def read_packages_from_file(filename):
    packages = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split(':')
            packages[key.strip()] = value.strip()
    return packages
def custom_autopct(pct):
    # Only display the percentage if it is above 3%
    return '{:.1f}%'.format(pct) if pct >= 3 else ''

def main():
    filename = input('Enter file name: ')
    file_title = filename.replace("import name results.txt", "").strip()
    results_dir = os.path.join('results/Install names/results', file_title)
    os.makedirs(results_dir, exist_ok=True)

    packages = read_packages_from_file(filename)
    total_usages = 0
    usage_data = {}

    # Read and count usages from GitHub
    with open(os.path.join(results_dir, f'{file_title} absolute values.txt'), 'w') as f:
        iteration = 0
        for key, package in packages.items():
            if iteration % 9 == 0 and iteration != 0:
                print("Pausing for 60 seconds...")
                time.sleep(60)
            count = search_github(package)
            usage_data[package] = count
            total_usages += count
            f.write(f"{package}: {count} usages\n")
            print(f"{package}: {count} usages\n")
            iteration += 1

    print("Total usages across all packages:", total_usages)

    threshold = 0.03  # 3%
    others_count = 0
    final_data = {}

    # Aggregate small packages into "Others"
    for package, count in usage_data.items():
        if (count / total_usages) < threshold:
            others_count += count
        else:
            final_data[package] = count

    if others_count > 0:
        final_data['Others'] = others_count

    # Create the explode array here, ensuring it matches the length of final_data
    explode = [0 for _ in final_data]

    # Colors and plotting the pie chart
    colors = ['skyblue', 'coral', 'limegreen', 'tomato', 'mediumpurple', 'goldenrod',
    'turquoise', 'lightcoral', 'mediumseagreen', 'indianred', 'slateblue', 'peru',
    'cadetblue', 'salmon', 'darkseagreen', 'crimson', 'orchid', 'darkkhaki',
    'steelblue', 'darksalmon', 'palegreen', 'firebrick', 'plum', 'tan',
    'cornflowerblue', 'lightsalmon', 'springgreen', 'darkred', 'thistle', 'burlywood'] * (len(final_data) // 6 + 1)
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(final_data.values(), colors=colors[:len(final_data)], explode=explode, autopct=custom_autopct, startangle=90)
    ax.legend(wedges, final_data.keys(), title="Packages", loc="center left", bbox_to_anchor=(0.88, 0, 0.5, 1))
    ax.axis('equal')
    plt.title(f"Package Usage for Algorithm: {file_title}")
    plt.subplots_adjust(left=0.1, right=0.85, top=0.9, bottom=0.1)  # Adjust these parameters as needed
    fig.set_size_inches(10, 8)
    plt.savefig(os.path.join(results_dir, f'{file_title}_usage_distribution.png'))
    plt.close(fig)

if __name__ == "__main__":
    main()
