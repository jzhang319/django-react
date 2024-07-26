import requests
import re
import json
import base64
import msgpack

# Base URL
base_url = "https://ciphersprint.pulley.com/"

def decrypt_path(encrypted_path):
    try:
        ascii_values = json.loads(encrypted_path.replace("task_", ""))
        decrypted_path = ''.join(chr(num) for num in ascii_values)
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Error decoding JSON or converting ASCII values: {e}")
        return None
    return decrypted_path

def handle_non_hex(encrypted_path):
    hex_string = encrypted_path.replace("task_", "")
    sanitized_path = re.sub(r'[^0-9a-fA-F]', '', hex_string)
    # print(f"Sanitized path (non-hex removed): {sanitized_path}")
    return sanitized_path

def rotate_left(encoded_string, rotation_amount):
    length = len(encoded_string)
    if length == 0:
        return encoded_string

    rotation_amount %= length  # Ensure rotation is within bounds
    rotated_string = encoded_string[rotation_amount:] + encoded_string[:rotation_amount]
    print(encoded_string[rotation_amount:], ' <---------- rotation 1')
    print(encoded_string[:rotation_amount], ' <---------- rotation 2' )
    return rotated_string

def handle_circular_rotation(encrypted_path, rotation_amount):
    print('encrypted_path -------> ', encrypted_path)
    hex_string = encrypted_path.replace("task_", "")
    print('amount --------> ', rotation_amount)
    if not hex_string:
        print("Hex string is empty after removing 'task_'")
        return None
    rotated_path = rotate_left(hex_string, rotation_amount)
    print(f"Rotated path: {rotated_path}")  # Debug
    return rotated_path

def extract_rotation_amount(encryption_method):
    match = re.search(r'circularly rotated left by (\d+)', encryption_method)
    if match:
        return int(match.group(1))
    return None

def extract_custom_hex_set(encryption_method):
    match = re.search(r'custom hex character set ([0-9a-fA-F]+)', encryption_method)
    if match:
        return match.group(1)
    return None

def encode_with_custom_hex(hex_string, custom_hex_set):
    # Define the standard hexadecimal characters
    standard_hex = '0123456789abcdef'

    # Ensure custom hex set is lowercase and has exactly 16 characters
    custom_hex_set = custom_hex_set.lower()
    if len(custom_hex_set) != 16:
        raise ValueError("Custom hex character set must be exactly 16 characters long.")

    # Create a reverse translation table: map custom hex characters to standard hex characters
    reverse_translation_table = str.maketrans(custom_hex_set, standard_hex)

    # Remove the 'task_' prefix from the encrypted path
    clean_hex_string = hex_string.replace("task_", "")

    # Translate the hex string using the reverse translation table
    decoded_path = clean_hex_string.translate(reverse_translation_table)

    return decoded_path

def base64_decode_messagepack(encoded_str):
    # Decode base64
    decoded_bytes = base64.b64decode(encoded_str)
    # Unpack MessagePack
    unpacked_data = msgpack.unpackb(decoded_bytes, raw=False)
    return unpacked_data

def unscramble(encrypted_path, positions):
    # Remove 'task_' prefix
    clean_hex_string = encrypted_path.replace("task_", "")
    # Create a list from the hex string
    hex_list = list(clean_hex_string)

    # Initialize the scrambled list with placeholders
    unscrambled_list = [''] * len(hex_list)

    # Rearrange according to positions
    for index, position in enumerate(positions):
        unscrambled_list[position] = hex_list[index]

    # Convert list back to string
    unscrambled_path = ''.join(unscrambled_list)
    return unscrambled_path

def fetch_challenge(url):
    while True:
        print(f"Fetching URL: {url}")  # Debug

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            print("Response from server:", data)

            encrypted_path = data.get("encrypted_path", "")
            encryption_method = data.get("encryption_method", "")

            if encryption_method == "nothing":
                next_url = f"{base_url}{encrypted_path}"
            elif encryption_method == "converted to a JSON array of ASCII values":
                decrypted_path = decrypt_path(encrypted_path)
                if decrypted_path:
                    next_url = f"{base_url}task_{decrypted_path}"
                else:
                    break
            elif encryption_method == "inserted some non-hex characters":
                sanitized_path = handle_non_hex(encrypted_path)
                if sanitized_path:
                    next_url = f"{base_url}task_{sanitized_path}"
                else:
                    break
            elif "circularly rotated left by" in encryption_method:
                rotation_amount = extract_rotation_amount(encryption_method)
                if rotation_amount is not None:
                    decrypted_path = handle_circular_rotation(encrypted_path, rotation_amount)
                    if decrypted_path:
                        next_url = f"{base_url}task_{decrypted_path}"
                    else:
                        break
                else:
                    print("Failed to extract rotation amount.")
                    break
            elif "encoded it with custom hex character set" in encryption_method:
                custom_hex_set = extract_custom_hex_set(encryption_method)
                if custom_hex_set:
                    decrypted_path = encode_with_custom_hex(encrypted_path.replace("task_", ""), custom_hex_set)
                    next_url = f"{base_url}task_{decrypted_path}"
                else:
                    print("Failed to extract custom hex character set.")
                    break
            elif "scrambled! original positions as base64 encoded messagepack" in encryption_method:
                # Extract the base64 string
                base64_encoded_messagepack = re.search(r'base64 encoded messagepack: (.+)', encryption_method)
                if base64_encoded_messagepack:
                    base64_string = base64_encoded_messagepack.group(1)
                    # Decode the MessagePack
                    positions = base64_decode_messagepack(base64_string)
                    # Unscramble the path
                    unscrambled_path = unscramble(encrypted_path, positions)
                    next_url = f"{base_url}task_{unscrambled_path}"
                else:
                    print("Failed to extract base64 encoded messagepack.")
                    break
            else:
                print("Unexpected encryption method:", encryption_method)
                break

            print("Next URL:", next_url)  # Debug
            url = next_url
        else:
            print(f"Failed to fetch the URL. Status code: {response.status_code}")
            break

# Initial URL
initial_url = f"{base_url}jzhang319@gmail.com"
fetch_challenge(initial_url)
