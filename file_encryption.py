# ================================================================
#   CODVEDA PYTHON INTERNSHIP - LEVEL 3, TASK 2
#   Basic File Encryption / Decryption
#   Methods: Caesar Cipher + Fernet (AES-128) Encryption
#
#   HOW TO RUN:
#       pip install cryptography
#       python file_encryption.py
# ================================================================

import os
import string
from datetime import datetime

# ── Try importing cryptography (for Fernet) ─────────────────────
try:
    from cryptography.fernet import Fernet, InvalidToken
    FERNET_AVAILABLE = True
except ImportError:
    FERNET_AVAILABLE = False

# ── Constants ────────────────────────────────────────────────────
KEY_FILE        = "fernet_secret.key"
SEPARATOR       = "=" * 55


# ================================================================
#   UTILITY FUNCTIONS
# ================================================================

def print_header():
    print(f"\n{SEPARATOR}")
    print("    FILE ENCRYPTION / DECRYPTION TOOL")
    print("    Codveda Python Internship - Level 3, Task 2")
    print(SEPARATOR)


def file_size(path):
    """Return file size as a human-readable string."""
    size = os.path.getsize(path)
    return f"{size} bytes" if size < 1024 else f"{size/1024:.1f} KB"


def check_file_exists(path):
    """Check if a file exists; print error if not."""
    if not os.path.exists(path):
        print(f"\n  [ERROR] File not found: '{path}'")
        print("      Please check the filename and try again.")
        return False
    return True


def create_sample_files():
    """Create sample text files for testing."""
    files = {
        "sample1.txt": """Hello! This is a sample text file for encryption testing.
Codveda Python Internship - Level 3, Task 2.

This file demonstrates:
  - Caesar Cipher encryption (simple shift-based)
  - Fernet encryption (AES-128, production-grade)

Confidential data: PROJECT-CODE-2024
Secret key value : CODVEDA-INTERN-XYZ
""",
        "sample2.txt": """Python is a high-level, general-purpose programming language.
It was created by Guido van Rossum and first released in 1991.

Key features of Python:
  1. Easy to read and write
  2. Dynamically typed
  3. Supports multiple programming paradigms
  4. Large standard library

This is sample file 2 for encryption testing!
"""
    }
    for name, content in files.items():
        with open(name, "w") as f:
            f.write(content)
    print(f"\n  Created: sample1.txt and sample2.txt")


# ================================================================
#   METHOD 1: CAESAR CIPHER
# ================================================================

def caesar_encrypt_text(text, shift):
    """
    Encrypt text using Caesar cipher.
    Shifts each letter by 'shift' positions.
    Numbers and special characters are preserved unchanged.
    """
    result = []
    for ch in text:
        if ch.isalpha():
            base  = ord('A') if ch.isupper() else ord('a')
            shifted = chr((ord(ch) - base + shift) % 26 + base)
            result.append(shifted)
        else:
            result.append(ch)   # digits, spaces, punctuation unchanged
    return "".join(result)


def caesar_decrypt_text(text, shift):
    """Decrypt Caesar cipher by shifting in the opposite direction."""
    return caesar_encrypt_text(text, -shift)


def caesar_encrypt_file(input_path, shift):
    """Read a file, encrypt its content with Caesar cipher, save result."""
    if not check_file_exists(input_path):
        return

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            original = f.read()

        encrypted = caesar_encrypt_text(original, shift)

        # Build output filename
        base, ext  = os.path.splitext(input_path)
        output_path = f"{base}_caesar_encrypted{ext}"

        # Save header + encrypted content
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# CAESAR CIPHER ENCRYPTED FILE\n")
            f.write(f"# Shift    : {shift}\n")
            f.write(f"# Encrypted: {timestamp}\n")
            f.write(f"# Original : {input_path}\n")
            f.write(f"# {'='*45}\n")
            f.write(encrypted)

        print(f"\n  Caesar Encryption Successful!")
        print(f"  {'-'*45}")
        print(f"  Input File   : {input_path}  ({file_size(input_path)})")
        print(f"  Output File  : {output_path}  ({file_size(output_path)})")
        print(f"  Shift Used   : {shift}")
        print(f"\n  Preview (first 80 chars of encrypted content):")
        print(f"  {encrypted[:80]}...")

    except UnicodeDecodeError:
        print("  Error: File is not a text file (binary files not supported by Caesar).")
    except Exception as e:
        print(f"  Error: {e}")


def caesar_decrypt_file(input_path, shift):
    """Read an encrypted file, strip header, decrypt and save."""
    if not check_file_exists(input_path):
        return

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Strip metadata header lines (lines starting with #)
        lines = content.splitlines(keepends=True)
        body  = "".join(ln for ln in lines if not ln.startswith("#"))

        decrypted = caesar_decrypt_text(body, shift)

        base, ext   = os.path.splitext(input_path)
        # Remove _caesar_encrypted suffix if present
        clean_base  = base.replace("_caesar_encrypted", "")
        output_path = f"{clean_base}_caesar_decrypted{ext}"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(decrypted)

        print(f"\n  Caesar Decryption Successful!")
        print(f"  {'-'*45}")
        print(f"  Input File   : {input_path}")
        print(f"  Output File  : {output_path}  ({file_size(output_path)})")
        print(f"  Shift Used   : {shift}")
        print(f"\n  Preview (first 120 chars of decrypted content):")
        print(f"  {decrypted[:120]}")

    except Exception as e:
        print(f"  Error: {e}")


# ================================================================
#   METHOD 2: FERNET ENCRYPTION (AES-128)
# ================================================================

def generate_fernet_key():
    """Generate a new Fernet key and save to KEY_FILE."""
    if not FERNET_AVAILABLE:
        print("  cryptography library not installed.")
        print("      Run: pip install cryptography")
        return

    if os.path.exists(KEY_FILE):
        confirm = input(f"\n  Key file '{KEY_FILE}' already exists! Overwrite? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("  Key generation cancelled.")
            return

    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

    print(f"\n  New Fernet key generated!")
    print(f"  {'-'*45}")
    print(f"  Saved to : {KEY_FILE}")
    print(f"  Key size : 32 bytes (256-bit, URL-safe base64)")
    print(f"\n  IMPORTANT: Keep '{KEY_FILE}' safe.")
    print(f"      Without it, encrypted files CANNOT be recovered!")


def load_fernet_key():
    """Load Fernet key from KEY_FILE. Returns Fernet instance or None."""
    if not FERNET_AVAILABLE:
        print("  cryptography library not installed. Run: pip install cryptography")
        return None

    if not os.path.exists(KEY_FILE):
        print(f"\n  Key file '{KEY_FILE}' not found!")
        print(f"      Please generate a key first (Option 5 in the menu).")
        return None

    try:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
        return Fernet(key)
    except Exception as e:
        print(f"  Failed to load key: {e}")
        return None


def fernet_encrypt_file(input_path):
    """Encrypt any file with Fernet (AES-128 CBC + HMAC-SHA256)."""
    if not check_file_exists(input_path):
        return

    fernet = load_fernet_key()
    if not fernet:
        return

    try:
        with open(input_path, "rb") as f:
            original_data = f.read()

        encrypted_data = fernet.encrypt(original_data)

        output_path = input_path + ".fernet"
        with open(output_path, "wb") as f:
            f.write(encrypted_data)

        print(f"\n  Fernet Encryption Successful!")
        print(f"  {'-'*45}")
        print(f"  Input File  : {input_path}  ({file_size(input_path)})")
        print(f"  Output File : {output_path}  ({file_size(output_path)})")
        print(f"  Algorithm   : AES-128 CBC + HMAC-SHA256 (Fernet)")
        print(f"\n  The original file is still intact.")
        print(f"  Share or store '{output_path}' safely.")

    except Exception as e:
        print(f"  Encryption Error: {e}")


def fernet_decrypt_file(input_path):
    """Decrypt a .fernet encrypted file."""
    if not check_file_exists(input_path):
        return

    fernet = load_fernet_key()
    if not fernet:
        return

    try:
        with open(input_path, "rb") as f:
            encrypted_data = f.read()

        decrypted_data = fernet.decrypt(encrypted_data)

        # Build output path
        if input_path.endswith(".fernet"):
            base_path = input_path[:-7]        # remove .fernet
        else:
            base_path = input_path

        root, ext   = os.path.splitext(base_path)
        output_path = f"{root}_decrypted{ext}"

        with open(output_path, "wb") as f:
            f.write(decrypted_data)

        print(f"\n  Fernet Decryption Successful!")
        print(f"  {'-'*45}")
        print(f"  Input File  : {input_path}")
        print(f"  Output File : {output_path}  ({file_size(output_path)})")

        # Show text preview if it's a text file
        try:
            preview = decrypted_data.decode("utf-8")
            print(f"\n  Preview (first 120 chars):")
            print(f"  {preview[:120]}")
        except UnicodeDecodeError:
            print("  (Binary file -- no text preview available)")

    except InvalidToken:
        print("\n  Decryption Failed: Wrong key or corrupted file!")
        print("      Make sure you are using the correct fernet_secret.key")
    except Exception as e:
        print(f"  Decryption Error: {e}")


# ================================================================
#   SHOW ALL FILES IN CURRENT DIRECTORY
# ================================================================

def list_files():
    print(f"\n  Files in current directory:")
    print(f"  {'-'*45}")
    files = [f for f in os.listdir(".") if os.path.isfile(f)]
    if not files:
        print("  (No files found)")
        return
    for fname in sorted(files):
        print(f"  {fname:<40}  {file_size(fname)}")


# ================================================================
#   MAIN MENU
# ================================================================

def main():
    print_header()

    if not FERNET_AVAILABLE:
        print("\n  NOTE: 'cryptography' library not installed.")
        print("      Fernet options will be disabled.")
        print("      Install with: pip install cryptography\n")

    while True:
        print(f"\n  {'-'*45}")
        print("  MENU")
        print(f"  {'-'*45}")
        print("  -- Caesar Cipher ---------------------")
        print("  1.  Encrypt a file  (Caesar Cipher)")
        print("  2.  Decrypt a file  (Caesar Cipher)")
        print()
        print("  -- Fernet (AES-128) ------------------")
        if FERNET_AVAILABLE:
            print("  3.  Generate Fernet encryption key")
            print("  4.  Encrypt a file  (Fernet)")
            print("  5.  Decrypt a file  (Fernet)")
        else:
            print("  3-5. [Requires: pip install cryptography]")
        print()
        print("  -- Utilities -------------------------")
        print("  6.  Create sample text files for testing")
        print("  7.  List files in current directory")
        print("  8.  Exit")
        print(f"  {'-'*45}")

        choice = input("\n  Enter your choice (1-8): ").strip()

        # ── Caesar Encrypt ──────────────────────────────────────
        if choice == "1":
            print("\n  -- Caesar Cipher Encryption --")
            path = input("  Enter filename to encrypt (e.g. sample1.txt): ").strip()
            try:
                shift = int(input("  Enter shift value (1-25, default=13): ").strip() or "13")
                shift = max(1, min(25, shift))
            except ValueError:
                shift = 13
            caesar_encrypt_file(path, shift)

        # ── Caesar Decrypt ──────────────────────────────────────
        elif choice == "2":
            print("\n  -- Caesar Cipher Decryption --")
            path = input("  Enter filename to decrypt: ").strip()
            try:
                shift = int(input("  Enter shift value used during encryption (default=13): ").strip() or "13")
                shift = max(1, min(25, shift))
            except ValueError:
                shift = 13
            caesar_decrypt_file(path, shift)

        # ── Generate Fernet Key ─────────────────────────────────
        elif choice == "3":
            if FERNET_AVAILABLE:
                generate_fernet_key()
            else:
                print("  Install cryptography first: pip install cryptography")

        # ── Fernet Encrypt ──────────────────────────────────────
        elif choice == "4":
            if FERNET_AVAILABLE:
                print("\n  -- Fernet Encryption --")
                path = input("  Enter filename to encrypt (e.g. sample1.txt): ").strip()
                fernet_encrypt_file(path)
            else:
                print("  Install cryptography first: pip install cryptography")

        # ── Fernet Decrypt ──────────────────────────────────────
        elif choice == "5":
            if FERNET_AVAILABLE:
                print("\n  -- Fernet Decryption --")
                path = input("  Enter .fernet filename to decrypt (e.g. sample1.txt.fernet): ").strip()
                fernet_decrypt_file(path)
            else:
                print("  Install cryptography first: pip install cryptography")

        # ── Create sample files ─────────────────────────────────
        elif choice == "6":
            create_sample_files()

        # ── List files ──────────────────────────────────────────
        elif choice == "7":
            list_files()

        # ── Exit ────────────────────────────────────────────────
        elif choice == "8":
            print("\n  Goodbye!\n")
            break

        else:
            print("  Invalid choice! Please enter 1-8.")


if __name__ == "__main__":
    main()
