from PIL import Image

# ---------------------------------- Encode Function -------------------------------------------------------------
def encode_message(img_path, message, output_path):
    img = Image.open(img_path)
    img = img.convert("RGB")  # ensure RGB format
    pixels = img.load()

    # Convert message to binary + EOF marker
    binary_msg = ''.join(format(ord(i), '08b') for i in message)
    binary_msg += '11111110'  # special end marker (8-bit)

    idx = 0
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if idx < len(binary_msg):
                r, g, b = pixels[x, y]

                # Modify R channel
                if idx < len(binary_msg):
                    r = (r & ~1) | int(binary_msg[idx])
                    idx += 1

                # Modify G channel
                if idx < len(binary_msg):
                    g = (g & ~1) | int(binary_msg[idx])
                    idx += 1

                # Modify B channel
                if idx < len(binary_msg):
                    b = (b & ~1) | int(binary_msg[idx])
                    idx += 1

                pixels[x, y] = (r, g, b)

    img.save(output_path)
    print(f"[+] Message encoded successfully into {output_path}")


# ------------------------------------ Decode Function ----------------------------------------------------------
def decode_message(img_path):
    img = Image.open(img_path)
    img = img.convert("RGB")
    pixels = img.load()

    binary_msg = ""
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b = pixels[x, y]
            binary_msg += str(r & 1)
            binary_msg += str(g & 1)
            binary_msg += str(b & 1)

    # Split into 8-bit chunks
    chars = [binary_msg[i:i+8] for i in range(0, len(binary_msg), 8)]

    message = ""
    for c in chars:
        if c == "11111110":  # EOF marker
            break
        message += chr(int(c, 2))

    return message


# ---------------------------------------------- Main -------------------------------------------------------------------
if __name__ == "__main__":
    print("==== IMAGE STEGANOGRAPHY SYSTEM ====")
    print("1. Encode Message")
    print("2. Decode Message")
    choice = input("Choose option (1/2): ")

    if choice == "1":
        img_path = input("Enter input image path: ").strip()
        output_path = input("Enter output (stego) image path: ").strip()
        message = input("Enter secret message: ").strip()
        encode_message(img_path, message, output_path)

    elif choice == "2":
        img_path = input("Enter stego image path: ").strip()
        hidden_msg = decode_message(img_path)
        print("[+] Extracted Message:", hidden_msg)

    else:
        print("Invalid choice. Please enter 1 or 2.")
