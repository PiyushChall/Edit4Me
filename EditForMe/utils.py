def read_code(filename: str = "generated_code.py") -> str:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def write_code_to_file(code: str, filename: str = "generated_code.py"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)
    return f"✅ Code written to {filename}"
