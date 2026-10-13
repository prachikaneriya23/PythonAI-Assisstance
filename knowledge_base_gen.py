import pandas as pd

# Each row: keywords (space separated, used for matching), category,
# title, explanation, code_example
ROWS = [
    # ---------------- BASICS ----------------
    dict(keywords="variable variables assignment naming",
         category="Basics", title="Variables",
         explanation="A variable is a name bound to a value in memory. Python is dynamically "
                      "typed, so you don't declare a type - it is inferred from the value you "
                      "assign. Names must start with a letter or underscore and are case-sensitive.",
         code_example="age = 21\nname = \"Agrim\"\nis_student = True\nprint(age, name, is_student)"),

    dict(keywords="data types int float str bool list tuple dict set",
         category="Basics", title="Built-in Data Types",
         explanation="Core built-in types: int, float, complex, str, bool, list, tuple, dict, "
                      "set, frozenset, bytes, and NoneType. Use type(x) to check a value's type.",
         code_example="x = 10          # int\ny = 3.14        # float\nname = \"hi\"     # str\nflag = True     # bool\nitems = [1,2,3] # list\npoint = (1,2)   # tuple\nperson = {\"a\":1} # dict\nuniq = {1,2,3}  # set\nprint(type(x), type(name))"),

    dict(keywords="operators arithmetic comparison logical bitwise",
         category="Basics", title="Operators",
         explanation="Arithmetic: + - * / // % **. Comparison: == != > < >= <=. Logical: and or "
                      "not. Bitwise: & | ^ ~ << >>. // is floor division, ** is exponent.",
         code_example="print(7 // 2)   # 3\nprint(7 % 2)    # 1\nprint(2 ** 5)   # 32\nprint((5 > 3) and (2 < 4))"),

    dict(keywords="if else elif conditional condition",
         category="Basics", title="Conditionals (if/elif/else)",
         explanation="Conditionals run code based on a boolean expression. Python uses "
                      "indentation (not braces) to define blocks - be consistent with spaces.",
         code_example="score = 82\nif score >= 90:\n    grade = \"A\"\nelif score >= 75:\n    grade = \"B\"\nelse:\n    grade = \"C\"\nprint(grade)"),

    dict(keywords="loop for while range break continue",
         category="Basics", title="Loops (for / while)",
         explanation="`for` iterates over an iterable (list, range, string...). `while` repeats "
                      "while a condition is true. `break` exits a loop, `continue` skips to the "
                      "next iteration.",
         code_example="for i in range(5):\n    if i == 3:\n        continue\n    print(i)\n\nn = 0\nwhile n < 3:\n    print(\"n =\", n)\n    n += 1"),

    dict(keywords="function def parameters arguments return default args kwargs",
         category="Basics", title="Functions",
         explanation="Define reusable code with `def`. Parameters can have default values, and "
                      "you can accept variable args (*args) and keyword args (**kwargs).",
         code_example="def greet(name, greeting=\"Hello\"):\n    return f\"{greeting}, {name}!\"\n\ndef total(*args, **kwargs):\n    return sum(args) + sum(kwargs.values())\n\nprint(greet(\"Agrim\"))\nprint(total(1, 2, 3, bonus=10))"),

    dict(keywords="lambda anonymous function",
         category="Basics", title="Lambda Functions",
         explanation="A lambda is a small anonymous function: `lambda args: expression`. Useful "
                      "for short throwaway functions, e.g. as a `key=` for sorted().",
         code_example="square = lambda x: x * x\nprint(square(5))\n\nnames = [\"Bob\", \"al\", \"Charlie\"]\nprint(sorted(names, key=lambda s: len(s)))"),

    dict(keywords="list comprehension dict comprehension set comprehension",
         category="Basics", title="Comprehensions",
         explanation="Comprehensions build lists/dicts/sets in one concise line, often faster "
                      "and more readable than an equivalent for-loop with append().",
         code_example="squares = [x*x for x in range(10) if x % 2 == 0]\nsq_map = {x: x*x for x in range(5)}\nuniq = {x % 3 for x in range(10)}\nprint(squares, sq_map, uniq)"),

    dict(keywords="string str methods slicing format f-string",
         category="Basics", title="Strings",
         explanation="Strings are immutable sequences of characters. Slicing: s[start:stop:step]. "
                      "Common methods: split, join, strip, replace, upper/lower, find. f-strings "
                      "embed expressions: f'{value}'.",
         code_example="s = \"  Hello, World!  \"\nprint(s.strip().lower())\nprint(s[2:7])\nparts = \"a,b,c\".split(\",\")\nprint(\"-\".join(parts))\nname = \"Agrim\"\nprint(f\"Hi {name}, len={len(name)}\")"),

    dict(keywords="list methods append pop insert remove sort slicing",
         category="Basics", title="Lists",
         explanation="Lists are ordered, mutable sequences. Key methods: append, extend, insert, "
                      "pop, remove, sort, reverse. Slicing works the same as strings.",
         code_example="nums = [3, 1, 4, 1, 5]\nnums.append(9)\nnums.sort()\nprint(nums)\nprint(nums[1:4])\nnums.remove(1)\nprint(nums)"),

    dict(keywords="dictionary dict keys values items get update",
         category="Basics", title="Dictionaries",
         explanation="Dicts store key-value pairs (insertion-ordered since 3.7). Use .get(key, "
                      "default) to avoid KeyError, .items()/.keys()/.values() to iterate.",
         code_example="person = {\"name\": \"Agrim\", \"age\": 21}\nperson[\"city\"] = \"Lucknow\"\nprint(person.get(\"country\", \"India\"))\nfor k, v in person.items():\n    print(k, \"->\", v)"),

    dict(keywords="tuple immutable unpacking",
         category="Basics", title="Tuples",
         explanation="Tuples are ordered and immutable. Great for fixed collections and for "
                      "unpacking multiple return values.",
         code_example="point = (3, 4)\nx, y = point\nprint(x, y)\n\ndef minmax(nums):\n    return min(nums), max(nums)\n\nlo, hi = minmax([4,1,9,2])\nprint(lo, hi)"),

    dict(keywords="set union intersection difference",
         category="Basics", title="Sets",
         explanation="Sets are unordered collections of unique items. Support union (|), "
                      "intersection (&), difference (-), and symmetric_difference (^).",
         code_example="a = {1,2,3}\nb = {2,3,4}\nprint(a | b)\nprint(a & b)\nprint(a - b)"),

    # ---------------- EXCEPTIONS ----------------
    dict(keywords="exception try except finally error handling raise",
         category="Exceptions", title="Exception Handling",
         explanation="Wrap risky code in try/except. Use `finally` for cleanup that always runs, "
                      "and `raise` to signal your own errors. Catch specific exceptions rather "
                      "than a bare `except:`.",
         code_example="try:\n    x = int(\"abc\")\nexcept ValueError as e:\n    print(\"Bad input:\", e)\nfinally:\n    print(\"Done trying\")\n\ndef check(age):\n    if age < 0:\n        raise ValueError(\"Age cannot be negative\")\n    return age"),

    dict(keywords="custom exception class exception subclass",
         category="Exceptions", title="Custom Exceptions",
         explanation="Create your own exception types by subclassing Exception. This makes "
                      "error handling more precise in larger programs.",
         code_example="class InsufficientFundsError(Exception):\n    pass\n\ndef withdraw(balance, amount):\n    if amount > balance:\n        raise InsufficientFundsError(\"Not enough balance\")\n    return balance - amount\n\ntry:\n    withdraw(100, 200)\nexcept InsufficientFundsError as e:\n    print(e)"),

    # ---------------- OOP ----------------
    dict(keywords="class object oop init self",
         category="OOP", title="Classes & Objects",
         explanation="A class is a blueprint for objects. `__init__` is the constructor, `self` "
                      "refers to the current instance.",
         code_example="class Dog:\n    def __init__(self, name):\n        self.name = name\n\n    def bark(self):\n        return f\"{self.name} says Woof!\"\n\nd = Dog(\"Rex\")\nprint(d.bark())"),

    dict(keywords="inheritance super parent child class extend",
         category="OOP", title="Inheritance",
         explanation="A subclass inherits attributes/methods from a parent class. Use super() to "
                      "call the parent's implementation.",
         code_example="class Animal:\n    def __init__(self, name):\n        self.name = name\n    def speak(self):\n        return \"...\"\n\nclass Cat(Animal):\n    def speak(self):\n        return f\"{self.name} says Meow\"\n\nprint(Cat(\"Tom\").speak())"),

    dict(keywords="polymorphism method overriding duck typing",
         category="OOP", title="Polymorphism",
         explanation="Different classes can implement the same method name differently. Code "
                      "that calls the method doesn't need to know the exact class.",
         code_example="class Shape:\n    def area(self):\n        return 0\n\nclass Square(Shape):\n    def __init__(self, s): self.s = s\n    def area(self): return self.s ** 2\n\nclass Circle(Shape):\n    def __init__(self, r): self.r = r\n    def area(self): return 3.14 * self.r ** 2\n\nfor shape in [Square(4), Circle(3)]:\n    print(shape.area())"),

    dict(keywords="encapsulation private protected underscore property",
         category="OOP", title="Encapsulation",
         explanation="Python uses naming conventions for access control: `_protected` (by "
                      "convention) and `__private` (name-mangled). `@property` exposes controlled "
                      "getters/setters.",
         code_example="class Account:\n    def __init__(self, balance):\n        self.__balance = balance\n\n    @property\n    def balance(self):\n        return self.__balance\n\n    @balance.setter\n    def balance(self, value):\n        if value < 0:\n            raise ValueError(\"negative balance\")\n        self.__balance = value\n\na = Account(100)\nprint(a.balance)"),

    dict(keywords="decorator function wrapper functools wraps",
         category="OOP", title="Decorators",
         explanation="A decorator wraps a function to add behaviour without modifying its code. "
                      "Use functools.wraps to preserve the original function's metadata.",
         code_example="import functools\n\ndef log_call(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        print(f\"Calling {func.__name__}\")\n        return func(*args, **kwargs)\n    return wrapper\n\n@log_call\ndef add(a, b):\n    return a + b\n\nprint(add(2, 3))"),

    dict(keywords="generator yield iterator iter next",
         category="OOP", title="Generators & Iterators",
         explanation="Generators produce values lazily with `yield`, saving memory versus "
                      "building a full list. Any object with __iter__/__next__ is an iterator.",
         code_example="def countdown(n):\n    while n > 0:\n        yield n\n        n -= 1\n\nfor num in countdown(3):\n    print(num)\n\ngen = (x*x for x in range(5))\nprint(list(gen))"),

    dict(keywords="magic methods dunder str repr eq len",
         category="OOP", title="Magic / Dunder Methods",
         explanation="Special methods like __str__, __repr__, __eq__, __len__ let your objects "
                      "work with built-in functions and operators.",
         code_example="class Point:\n    def __init__(self, x, y):\n        self.x, self.y = x, y\n    def __repr__(self):\n        return f\"Point({self.x}, {self.y})\"\n    def __eq__(self, other):\n        return (self.x, self.y) == (other.x, other.y)\n\nprint(Point(1,2) == Point(1,2))"),

    # ---------------- FILES / MODULES ----------------
    dict(keywords="file open read write with context manager",
         category="Files", title="File Handling",
         explanation="Use `with open(path, mode) as f:` so the file is closed automatically. "
                      "Modes: 'r' read, 'w' write (overwrite), 'a' append, 'rb'/'wb' binary.",
         code_example="with open(\"notes.txt\", \"w\") as f:\n    f.write(\"Hello file!\\n\")\n\nwith open(\"notes.txt\", \"r\") as f:\n    content = f.read()\nprint(content)"),

    dict(keywords="module import package pip install venv virtual environment",
         category="Modules", title="Modules, Packages & pip",
         explanation="A module is a .py file; a package is a folder of modules with __init__.py. "
                      "`pip install <name>` installs third-party packages. Use a virtual "
                      "environment per project: `python -m venv venv` then activate it.",
         code_example="# terminal commands\npython -m venv venv\nvenv\\Scripts\\activate      # Windows\nsource venv/bin/activate    # macOS/Linux\npip install requests\npip freeze > requirements.txt"),

    # ---------------- REGEX ----------------
    dict(keywords="regex re module pattern match search findall sub",
         category="Regex", title="Regex Basics (re module)",
         explanation="The `re` module does pattern matching. re.match checks the start of a "
                      "string, re.search finds anywhere, re.findall returns all matches, re.sub "
                      "replaces matches.",
         code_example="import re\n\ntext = \"Call me at 987-654-3210 or 123-456-7890\"\npattern = r\"\\d{3}-\\d{3}-\\d{4}\"\nprint(re.findall(pattern, text))\nprint(re.sub(pattern, \"[hidden]\", text))"),

    dict(keywords="regex groups named groups compile",
         category="Regex", title="Regex Groups & Compiling",
         explanation="Parentheses create capture groups. Use (?P<name>...) for named groups. "
                      "re.compile() precompiles a pattern for reuse/performance.",
         code_example="import re\npattern = re.compile(r\"(?P<user>[\\w.]+)@(?P<domain>[\\w.]+)\")\nm = pattern.search(\"contact: agrim@example.com\")\nprint(m.group(\"user\"), m.group(\"domain\"))"),

    dict(keywords="regex email validation phone validation common patterns",
         category="Regex", title="Common Regex Patterns",
         explanation="Handy reusable patterns for validation tasks. Note: for real email "
                      "validation, a simple regex is a heuristic, not a full RFC check.",
         code_example="import re\nEMAIL = r\"^[\\w.+-]+@[\\w-]+\\.[a-zA-Z]{2,}$\"\nPHONE_IN = r\"^[6-9]\\d{9}$\"\nprint(bool(re.match(EMAIL, \"agrim@lbsim.in\")))\nprint(bool(re.match(PHONE_IN, \"9876543210\")))"),

    # ---------------- NUMPY / PANDAS ----------------
    dict(keywords="numpy array ndarray create reshape",
         category="NumPy", title="NumPy Arrays",
         explanation="numpy.ndarray is a fast, fixed-type, multi-dimensional array - the base of "
                      "numerical Python. Much faster than plain Python lists for math.",
         code_example="import numpy as np\na = np.array([1, 2, 3, 4])\nb = a.reshape(2, 2)\nprint(b)\nprint(a * 2)\nprint(a.sum(), a.mean())"),

    dict(keywords="pandas dataframe series csv read_csv",
         category="Pandas", title="Pandas DataFrames",
         explanation="pandas.DataFrame is a labeled 2D table, built on numpy. Read data with "
                      "pd.read_csv(), inspect with .head()/.info(), filter with boolean masks.",
         code_example="import pandas as pd\ndf = pd.DataFrame({\"name\": [\"A\", \"B\"], \"score\": [80, 92]})\nprint(df.head())\nprint(df[df[\"score\"] > 85])"),

    # ---------------- DJANGO ----------------
    dict(keywords="django project startproject startapp manage.py",
         category="Django", title="Starting a Django Project",
         explanation="Django is installed via pip and scaffolded with django-admin. A project can "
                      "contain multiple apps. manage.py runs project-level commands.",
         code_example="# terminal commands\npip install django\ndjango-admin startproject mysite\ncd mysite\npython manage.py startapp blog\npython manage.py runserver"),

    dict(keywords="django model models.py orm field",
         category="Django", title="Django Models",
         explanation="Models define your database schema as Python classes in models.py. Each "
                      "class attribute maps to a table column via a Field type.",
         code_example="# blog/models.py\nfrom django.db import models\n\nclass Post(models.Model):\n    title = models.CharField(max_length=200)\n    content = models.TextField()\n    created_at = models.DateTimeField(auto_now_add=True)\n\n    def __str__(self):\n        return self.title"),

    dict(keywords="django migrate migrations makemigrations",
         category="Django", title="Django Migrations",
         explanation="Migrations sync your models with the database schema. Run makemigrations "
                      "after changing models, then migrate to apply them.",
         code_example="# terminal commands\npython manage.py makemigrations\npython manage.py migrate\npython manage.py createsuperuser"),

    dict(keywords="django view views.py request response render",
         category="Django", title="Django Views",
         explanation="A view is a Python function (or class) that takes a request and returns a "
                      "response, often rendering an HTML template.",
         code_example="# blog/views.py\nfrom django.shortcuts import render\nfrom .models import Post\n\ndef post_list(request):\n    posts = Post.objects.all()\n    return render(request, \"blog/list.html\", {\"posts\": posts})"),

    dict(keywords="django url urls.py urlpatterns routing",
         category="Django", title="Django URLs",
         explanation="urls.py maps URL paths to views. Each app usually has its own urls.py "
                      "included from the project's main urls.py.",
         code_example="# blog/urls.py\nfrom django.urls import path\nfrom . import views\n\nurlpatterns = [\n    path(\"\", views.post_list, name=\"post_list\"),\n]"),

    dict(keywords="django orm queryset filter get all objects",
         category="Django", title="Django ORM Queries",
         explanation="Model.objects is the manager used to query the database: .all(), "
                      ".filter(), .get(), .exclude(), .order_by() build QuerySets lazily.",
         code_example="from blog.models import Post\n\nPost.objects.all()\nPost.objects.filter(title__icontains=\"django\")\nPost.objects.get(id=1)\nPost.objects.order_by(\"-created_at\")[:5]"),

    dict(keywords="django form forms.py modelform validation",
         category="Django", title="Django Forms",
         explanation="Django Forms handle input validation and HTML rendering. ModelForm "
                      "auto-generates a form from a model.",
         code_example="# blog/forms.py\nfrom django import forms\nfrom .models import Post\n\nclass PostForm(forms.ModelForm):\n    class Meta:\n        model = Post\n        fields = [\"title\", \"content\"]"),

    dict(keywords="django admin admin.py register",
         category="Django", title="Django Admin",
         explanation="Django's built-in admin gives a ready-made UI for managing your models. "
                      "Register models in admin.py to expose them.",
         code_example="# blog/admin.py\nfrom django.contrib import admin\nfrom .models import Post\n\nadmin.site.register(Post)"),

    dict(keywords="django template templates render html jinja",
         category="Django", title="Django Templates",
         explanation="Templates are HTML files with Django Template Language tags ({{ }} for "
                      "variables, {% %} for logic) rendered by views.",
         code_example="<!-- blog/templates/blog/list.html -->\n<ul>\n{% for post in posts %}\n  <li>{{ post.title }}</li>\n{% endfor %}\n</ul>"),

    dict(keywords="django rest framework drf api serializer",
         category="Django", title="Django REST Framework Basics",
         explanation="DRF (installed separately: pip install djangorestframework) adds "
                      "Serializers (convert models <-> JSON) and API Views/ViewSets for building "
                      "REST APIs on top of Django.",
         code_example="# serializers.py\nfrom rest_framework import serializers\nfrom .models import Post\n\nclass PostSerializer(serializers.ModelSerializer):\n    class Meta:\n        model = Post\n        fields = \"__all__\""),
]

def build():
    df = pd.DataFrame(ROWS)
    df.insert(0, "id", range(1, len(df) + 1))
    df.to_csv("knowledge_base.csv", index=False)
    print(f"Wrote knowledge_base.csv with {len(df)} rows")

if __name__ == "__main__":
    build()
