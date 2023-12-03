import subprocess
import concurrent.futures
import sys

def colorize(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def check_dmarc(domain):
    command = ['dig', 'txt', f'_dmarc.{domain}']

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
        output = result.stdout

        if "p=none" in output:
            print(f"{domain.strip()}: {colorize('VULNERABLE', '32')}")  # '32' for green
        else:
            print(f"{domain.strip()}: {colorize('Not Vulnerable', '31')}")  # '31' for red

    except subprocess.CalledProcessError as e:
        # Handle errors, if any
        print(f"Error executing the command for {domain.strip()}: {e}")

if len(sys.argv) != 2:
    print("Usage: python3 program.py domain_list.txt")
    sys.exit(1)

# Read domains from the specified file
file_path = sys.argv[1]
try:
    with open(file_path, 'r') as file:
        domains = file.readlines()
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
    sys.exit(1)

# Use ProcessPoolExecutor for parallel processing
with concurrent.futures.ProcessPoolExecutor() as executor:
    # Map the check_dmarc function to each domain in parallel
    executor.map(check_dmarc, domains)
