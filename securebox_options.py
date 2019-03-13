import argparse

def parse_options():
    parser = argparse.ArgumentParser(description="Cliente de SecureBox")

    # Gestión de usuarios e identidades
    parser.add_argument("--create_id", nargs=2)
    parser.add_argument("--search_id")
    parser.add_argument("--delete_id", type=int)

    # Subida y descarga de ficheros
    parser.add_argument("--upload")
    parser.add_argument("--source_id", type=int)
    parser.add_argument("--dest_id", type=int)
    parser.add_argument("--list_files", action="store_true")
    parser.add_argument("--download", type=int)
    parser.add_argument("--delete_file", type=int)

    # Cifrado y firma de ficheros local
    parser.add_argument("--encrypt")
    parser.add_argument("--sign")
    parser.add_argument("--enc_sign")

    return parser.parse_args()
