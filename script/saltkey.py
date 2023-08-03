#!/usr/bin/env python3
##################################################################
# Author  : Percio Andrade
# Email   : perciocastelo@gmail.com
# Info    : Get keys from https://api.wordpress.org/secret-key/1.1/salt/ and update on wp-config.php
# Version : 1.0
# changelog :
# 1.0
#   - Initial Release
##################################################################

import os
import re
import urllib.request

# Get the absolute path of the script file
script_directory = os.path.dirname(os.path.abspath(__file__))
wp_config_file_path = os.path.join(script_directory, "wp-config.php")

# Check if wp-config.php file exists
if not os.path.exists(wp_config_file_path):
    print("The wp-config.php file was not found. The script will exit.")
    exit(1)

# Fetch values from the URL and save them in key.txt
url = "https://api.wordpress.org/secret-key/1.1/salt/"
response = urllib.request.urlopen(url)
keys_content = response.read().decode("utf-8")

with open("key.txt", "w") as key_file:
    key_file.write(keys_content)

# Create a backup of the original wp-config.php file
os.rename(wp_config_file_path, "wp-config.php.bak")

# Update the wp-config.php file with the new keys
key_dict = {}
with open("key.txt", "r") as key_file:
    for line in key_file:
        match = re.search(r"define\('([^']*)',\s*'([^']*)'\);", line)
        if match:
            key, value = match.groups()
            key_dict[key] = f"define('{key}', '{value}');"

with open("wp-config.php.bak", "r") as wp_config_file:
    wp_config_content = wp_config_file.read()

for key, value in key_dict.items():
    wp_config_content = re.sub(r"define\('" + key + r"',\s*'.*'\);", value, wp_config_content)

with open("wp-config.php", "w") as wp_config_file:
    wp_config_file.write(wp_config_content)

# Remove the temporary key.txt file
os.remove("key.txt")

print("The keys have been updated in the wp-config.php file")