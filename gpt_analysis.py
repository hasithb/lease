import os

source_folder = "/Users/HasithB/PycharmProjects/Lease_Analysis_Project/app"
output_file = "//Users/HasithB/PycharmProjects/Lease_Analysis_Project/output.txt"

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w', encoding='utf-8') as outfile:
    # Loop through all files in the source folder
    for filename in os.listdir(source_folder):
        # Check for Python files
        if filename.endswith(".py"):
            # Write filename as a header in the output file
            outfile.write(f"\n\n##{filename}##\n\n")

            # Open and read the content of the python file
            with open(os.path.join(source_folder, filename), 'r', encoding='utf-8') as infile:
                # Write content of the python file to the output file
                outfile.write(infile.read())
