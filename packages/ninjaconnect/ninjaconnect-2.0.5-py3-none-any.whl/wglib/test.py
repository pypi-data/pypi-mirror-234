new_address = "172.20.19.178/32"  # Replace NEW_IP_ADDRESS with the desired IP address

# Specify the path to your WireGuard configuration file
config_file_path = "snaconf.txt"  # Replace with the actual path to your configuration file

# Read the configuration file and store its lines in a list
with open(config_file_path, 'r') as file:
    config_lines = file.readlines()

# Search for the 'Address' line and replace it with the new address
for i, line in enumerate(config_lines):
    if line.startswith("Address"):
        config_lines[i] = f"Address = {new_address}\n"

# Write the modified configuration back to the file
with open(config_file_path, 'w') as file:
    file.writelines(config_lines)

print(f"Address updated to: {new_address}")