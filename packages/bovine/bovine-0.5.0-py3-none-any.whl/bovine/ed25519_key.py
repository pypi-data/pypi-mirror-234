from bovine.crypto import generate_ed25519_private_key, private_key_to_did_key


def main():
    private_key = generate_ed25519_private_key()
    did_key = private_key_to_did_key(private_key)

    print(f"Secret: {private_key}")
    print(f"Did-key: {did_key}")


if __name__ == "__main__":
    main()
