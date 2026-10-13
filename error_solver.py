import re

# Each entry: a regex matched against the traceback text, a human
# explanation (may use {0}, {1}... for captured groups), and common fixes.
_PATTERNS = [
    (re.compile(r"SyntaxError.*invalid syntax"),
     "Python couldn't parse your code — the grammar is wrong at that point.",
     ["Check for a missing/extra colon `:` after if/for/while/def/class.",
      "Check for unmatched brackets/parentheses/quotes.",
      "Make sure you didn't use a reserved keyword as a variable name."]),

    (re.compile(r"IndentationError"),
     "A block of code isn't indented consistently. Python uses indentation "
     "to define code blocks, so this is a hard error, not a style issue.",
     ["Use spaces consistently (4 spaces is the convention) — don't mix tabs and spaces.",
      "Make sure every line inside a block (after a `:`) is indented one level further."]),

    (re.compile(r"NameError: name '(\w+)' is not defined"),
     "You used a variable or function ('{0}') before defining it, or misspelled its name.",
     ["Check the spelling matches exactly (case-sensitive).",
      "Make sure it's defined/imported before this line runs.",
      "If it's meant to be a string, wrap it in quotes."]),

    (re.compile(r"TypeError: (.+)"),
     "You used a value of the wrong type for this operation — e.g. mixing "
     "str and int, calling something that isn't callable, or passing the "
     "wrong number/type of arguments.",
     ["Print type(x) for the values involved to confirm what type they actually are.",
      "Convert types explicitly, e.g. str(x) or int(x), where needed.",
      "Check the function signature — are you passing the right number of arguments?"]),

    (re.compile(r"IndexError"),
     "You tried to access a list/tuple/string index that doesn't exist.",
     ["Remember indexing starts at 0 and the last valid index is len(x) - 1.",
      "Print len(x) to check the size before indexing.",
      "Use a try/except IndexError, or check `if i < len(x):` first."]),

    (re.compile(r"KeyError: (.+)"),
     "You tried to access a dictionary key ({0}) that doesn't exist.",
     ["Use dict.get(key, default) instead of dict[key] to avoid crashing.",
      "Check spelling/case of the key.",
      "Print dict.keys() to see what's actually available."]),

    (re.compile(r"AttributeError: '(.+?)' object has no attribute '(\w+)'"),
     "You called `.{1}` on a `{0}` object, but that type doesn't have that "
     "attribute or method.",
     ["Print dir(obj) to see what's actually available on that object.",
      "Check you didn't return None from a function by mistake (None has no attributes).",
      "Check for a typo in the method/attribute name."]),

    (re.compile(r"ZeroDivisionError"),
     "You divided a number by zero, which is mathematically undefined.",
     ["Add a check: `if denominator != 0:` before dividing.",
      "Wrap the division in a try/except ZeroDivisionError."]),

    (re.compile(r"ValueError: (.+)"),
     "A function received an argument of the right type, but an invalid "
     "value — e.g. int('abc'), or an unpackable mismatch.",
     ["Validate/convert user input before using it (e.g. check .isdigit() before int()).",
      "Wrap the conversion in try/except ValueError."]),

    (re.compile(r"ModuleNotFoundError: No module named '(\w+)'|ImportError"),
     "Python can't find the module/package you tried to import ({0}).",
     ["Install it: pip install {0}",
      "Check the spelling of the import and that your virtual environment is activated.",
      "If it's your own file, make sure it's in the same folder or on sys.path."]),

    (re.compile(r"RecursionError"),
     "A function called itself too many times without reaching a base case "
     "— you likely have infinite (or too-deep) recursion.",
     ["Make sure your recursive function has a base case that actually gets reached.",
      "Check that each recursive call moves the input closer to the base case.",
      "For deep problems, consider converting to an iterative loop."]),

    (re.compile(r"FileNotFoundError"),
     "The file path you tried to open doesn't exist from where the script "
     "is running.",
     ["Double check the path and filename (case-sensitive on Linux/Mac).",
      "Use an absolute path, or check your current working directory with os.getcwd().",
      "Make sure the file exists before opening: os.path.exists(path)."]),

    (re.compile(r"UnboundLocalError"),
     "You tried to use a local variable before assigning it inside the "
     "current function — often because you assigned to it *anywhere* in "
     "the function, which makes Python treat it as local everywhere in "
     "that function.",
     ["If you meant the global/outer variable, add a `global` or `nonlocal` declaration.",
      "Make sure the variable is assigned on every code path before it's used."]),
]


def explain_error(traceback_text: str):
    """Given raw traceback / error text, return (title, explanation, fixes[])
    for the first matching known pattern, or a generic fallback."""
    if not traceback_text or not traceback_text.strip():
        return None

    # Find the last non-empty line — that's normally "ExceptionType: message"
    lines = [l for l in traceback_text.strip().splitlines() if l.strip()]
    last_line = lines[-1] if lines else traceback_text.strip()

    for pattern, explanation, fixes in _PATTERNS:
        m = pattern.search(traceback_text) or pattern.search(last_line)
        if m:
            groups = m.groups() if m.groups() else ()
            try:
                explanation_filled = explanation.format(*groups)
            except (IndexError, KeyError):
                explanation_filled = explanation
            fixes_filled = []
            for f in fixes:
                try:
                    fixes_filled.append(f.format(*groups))
                except (IndexError, KeyError):
                    fixes_filled.append(f)
            title = last_line.split(":")[0].strip()
            return title, explanation_filled, fixes_filled

    # Fallback: unknown error type
    title = last_line.split(":")[0].strip() if ":" in last_line else "Error"
    return (
        title,
        "This doesn't match a common known pattern, but here's the raw error line: "
        f"'{last_line}'. Read it carefully — the exception type (before the colon) "
        "tells you the category of problem, and the message after it usually "
        "names the exact variable or value at fault.",
        ["Re-read the last line of the traceback carefully — it names the exact error.",
         "Look at the line number mentioned in the traceback in your code.",
         "Search the exact exception type name plus 'python' if you're stuck."],
    )
