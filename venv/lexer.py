def tokenize(code):
    tokens = []
    for line in code.splitlines():
        line = line.strip()
        if line == "BEGIN":
            tokens.append(("BEGIN", "BEGIN"))
        elif line == "END":
            tokens.append(("END", "END"))
        elif line.startswith("SET"):
            tokens.append(("SET", "SET"))
            _, var, _, value = line.split()
            tokens.append(("IDENT", var))
            tokens.append(("TO", "TO"))
            tokens.append(("NUMBER", value))
        elif line.startswith("IF"):
            tokens.append(("IF", "IF"))
            _, var, op, value, _ = line.split()
            tokens.append(("IDENT", var))
            tokens.append(("LESS" if op == "<" else "GREATER" if op == ">" else "EQUAL", op))
            tokens.append(("NUMBER", value))
            tokens.append(("THEN", "THEN"))
        elif line == "ELSE":
            tokens.append(("ELSE", "ELSE"))
        elif line == "ENDIF":
            tokens.append(("ENDIF", "ENDIF"))
        elif line.startswith("PRINT"):
            tokens.append(("PRINT", "PRINT"))
            _, value = line.split()
            if value.isdigit():
                tokens.append(("NUMBER", value))
            else:
                tokens.append(("IDENT", value))
    return tokens