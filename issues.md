# Static Code Analysis Issues

## Before Analysis

The original `parking_system.py` was analyzed using Pylint, Bandit, and Flake8.

### Pylint

Initial score: **6.32/10**

Major issues included:

- Missing module and function docstrings
- Mutable default argument
- Bare exception handling
- Global statement
- File opened without a context manager
- File opened without explicitly specifying encoding
- Invalid function naming
- Long lines

### Bandit

Two security-related findings were identified:

- **B311:** Use of standard pseudo-random generator
- **B110:** `try/except/pass` detected

### Flake8

The initial analysis reported issues involving:

- Missing blank lines
- Lines exceeding the recommended length
- Bare `except` statements
- Missing blank lines after function definitions

---

## Issue and Fix Table

| Issue | Tool | Type | Location | Description | Fix |
|---|---|---|---|---|---|
| Mutable default argument | Pylint | Code quality | `register_permit()` | A list was used as a default argument and could be shared between calls. | Changed the default to `None` and initialized the list inside the function. |
| Missing module docstring | Pylint | Code quality | Module | The Python file did not contain a module-level description. | Added a module docstring. |
| Missing function docstrings | Pylint | Code quality | Multiple functions | Functions did not document their purpose. | Added docstrings to the functions. |
| Bare exception | Pylint / Flake8 | Code quality | Exception handlers | Bare `except` statements catch every exception. | Replaced them with specific exception types. |
| `try/except/pass` | Bandit | Security/code quality | Permit revocation | Exceptions were silently ignored. | Replaced the bare exception with `except KeyError` and an explicit return. |
| Standard random generator | Bandit | Security | Permit generation | `random.randint()` was flagged as unsuitable for security-sensitive random generation. | Replaced `random` with Python's `secrets` module. |
| Global statement | Pylint | Design | Database loading | The function explicitly modified the global variable using `global`. | Updated the existing dictionary using `clear()` and `update()`. |
| Unmanaged file resource | Pylint | Code quality | Database functions | Files were opened without a context manager. | Used `with open(...)`. |
| Unspecified encoding | Pylint | Code quality | Database functions | File encoding was not explicitly defined. | Added `encoding="utf-8"`. |
| Invalid function naming | Pylint | Style | `setExpiry()` | Function name did not follow snake_case. | Renamed it to `set_expiry()`. |
| Long lines | Pylint / Flake8 | Style | Multiple locations | Lines exceeded the configured length limit. | Reformatted long statements across multiple lines. |
| Missing blank lines | Flake8 | Style | Multiple locations | Required blank lines were missing between definitions. | Added the required blank lines. |
| Missing final newline | Pylint | Style | End of file | The file did not end with a newline. | Added a final newline. |

## After Analysis

The cleaned code was rerun through all three static analysis tools.

- **Pylint:** 10.00/10
- **Bandit:** 0 issues
- **Flake8:** 0 issues