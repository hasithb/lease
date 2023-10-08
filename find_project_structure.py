

import os

def generate_project_structure(root_dir, output_file):
    with open(output_file, 'w') as f:
        for root, dirs, files in os.walk(root_dir):
            if root != root_dir:
                relative_path = os.path.relpath(root, root_dir)
                f.write(f"{relative_path}/\n")
            for file in files:
                f.write(f"  {file}\n")

if __name__ == "__main__":
    root_directory = "//Users/HasithB/PycharmProjects/Lease_Analysis_Project/app"  # You can change this to your project's root directory
    output_filename = "project_structure.txt"  # Name of the output text file
    generate_project_structure(root_directory, output_filename)
    print(f"Project structure saved to '{output_filename}'")

import os

