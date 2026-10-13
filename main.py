
import os
import sys
import subprocess
import tempfile

import pandas as pd
import customtkinter as ctk

from matcher import KnowledgeMatcher
from error_solver import explain_error

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KB_PATH = os.path.join(BASE_DIR, "knowledge_base.csv")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def load_knowledge_base() -> pd.DataFrame:
    if not os.path.exists(KB_PATH):
        # Build it on first run if missing
        import knowledge_base_gen
        cwd = os.getcwd()
        os.chdir(BASE_DIR)
        try:
            knowledge_base_gen.build()
        finally:
            os.chdir(cwd)
    return pd.read_csv(KB_PATH)


class ChatBubble(ctk.CTkFrame):
    """A single message bubble in the chat log."""

    def __init__(self, master, text, sender="assistant", **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        is_user = sender == "user"
        bubble_color = "#2563eb" if is_user else "#2b2b2b"
        anchor = "e" if is_user else "w"

        label = ctk.CTkLabel(
            self,
            text=text,
            fg_color=bubble_color,
            corner_radius=12,
            justify="left",
            wraplength=560,
            padx=12,
            pady=10,
            anchor="w",
        )
        label.pack(anchor=anchor, padx=10, pady=4)


class AskLearnTab(ctk.CTkFrame):
    """Ask questions in natural language, get explanations + code."""

    def __init__(self, master, matcher: KnowledgeMatcher):
        super().__init__(master, fg_color="transparent")
        self.matcher = matcher

        self.chat_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.chat_scroll.pack(fill="both", expand=True, padx=10, pady=(10, 0))

        input_row = ctk.CTkFrame(self, fg_color="transparent")
        input_row.pack(fill="x", padx=10, pady=10)

        self.entry = ctk.CTkEntry(
            input_row,
            placeholder_text="Ask anything about Python, e.g. 'how do decorators work?'",
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.entry.bind("<Return>", lambda e: self.on_send())

        send_btn = ctk.CTkButton(input_row, text="Ask", width=80, command=self.on_send)
        send_btn.pack(side="left")

        self._add_bubble(
            "Hi! I'm your Python learning assistant. Ask me about any Python "
            "topic — variables, OOP, decorators, regex, NumPy, Pandas, or "
            "Django — and I'll explain it with a code example.",
            "assistant",
        )

    def _add_bubble(self, text, sender):
        bubble = ChatBubble(self.chat_scroll, text, sender=sender)
        bubble.pack(fill="x")
        self.after(50, lambda: self.chat_scroll._parent_canvas.yview_moveto(1.0))

    def on_send(self):
        query = self.entry.get().strip()
        if not query:
            return
        self.entry.delete(0, "end")
        self._add_bubble(query, "user")

        results = self.matcher.search(query, top_k=2)
        if not results:
            self._add_bubble(
                "I don't have a specific topic matching that yet. Try rephrasing, "
                "or check the 'Browse Topics' tab for the full list of what I cover.",
                "assistant",
            )
            return

        for score, row in results:
            reply = f"{row['title']} ({row['category']})\n\n{row['explanation']}\n\nExample:\n{row['code_example']}"
            self._add_bubble(reply, "assistant")


class RunDebugTab(ctk.CTkFrame):
    """Write/paste code, run it safely, see output and auto error explanations."""

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=10, pady=(10, 0))

        run_btn = ctk.CTkButton(toolbar, text="Run Code", command=self.run_code, width=120)
        run_btn.pack(side="left")

        clear_btn = ctk.CTkButton(
            toolbar, text="Clear", width=80, fg_color="#555", command=self.clear_all
        )
        clear_btn.pack(side="left", padx=8)

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=10, pady=10)
        body.grid_columnconfigure(0, weight=1)
        body.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(body, text="Your code:", anchor="w").grid(row=0, column=0, sticky="w")
        self.code_box = ctk.CTkTextbox(body, font=("Consolas", 13))
        self.code_box.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        self.code_box.insert(
            "1.0",
            'print("Hello, World!")\n\n# Try something broken to see the debug helper:\n# print(undefined_variable)',
        )

        ctk.CTkLabel(body, text="Output:", anchor="w").grid(row=2, column=0, sticky="w")
        self.output_box = ctk.CTkTextbox(body, font=("Consolas", 13), height=140, text_color="#d1d5db")
        self.output_box.grid(row=3, column=0, sticky="nsew", pady=(0, 10))
        self.output_box.configure(state="disabled")

        ctk.CTkLabel(body, text="Auto Debug Helper:", anchor="w").grid(row=4, column=0, sticky="w")
        self.debug_box = ctk.CTkTextbox(body, font=("Consolas", 13), height=160, text_color="#fca5a5")
        self.debug_box.grid(row=5, column=0, sticky="nsew")
        self.debug_box.configure(state="disabled")

    def _set_text(self, box, text):
        box.configure(state="normal")
        box.delete("1.0", "end")
        box.insert("1.0", text)
        box.configure(state="disabled")

    def clear_all(self):
        self.code_box.delete("1.0", "end")
        self._set_text(self.output_box, "")
        self._set_text(self.debug_box, "")

    def run_code(self):
        code = self.code_box.get("1.0", "end")
        self._set_text(self.output_box, "Running...")
        self._set_text(self.debug_box, "")
        self.update_idletasks()

        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".py", delete=False, dir=BASE_DIR
            ) as tmp:
                tmp.write(code)
                tmp_path = tmp.name

            result = subprocess.run(
                [sys.executable, tmp_path],
                capture_output=True,
                text=True,
                timeout=10,
            )
            output = result.stdout
            error = result.stderr
        except subprocess.TimeoutExpired:
            output, error = "", "TimeoutExpired: your code took longer than 10 seconds to run (possible infinite loop)."
        finally:
            if tmp_path:
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass

        self._set_text(self.output_box, output if output else "(no output)")

        if error:
            self._set_text(self.output_box, (output + "\n" if output else "") + "--- errors below ---\n" + error)
            result_tuple = explain_error(error)
            if result_tuple:
                title, explanation, fixes = result_tuple
                fixes_text = "\n".join(f"  - {f}" for f in fixes)
                debug_text = f"{title}\n\n{explanation}\n\nSuggested fixes:\n{fixes_text}"
                self._set_text(self.debug_box, debug_text)


class ErrorSolverTab(ctk.CTkFrame):
    """Paste a traceback, get an explanation without running any code."""

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=10, pady=10)
        body.grid_columnconfigure(0, weight=1)
        body.grid_rowconfigure(1, weight=1)
        body.grid_rowconfigure(4, weight=1)

        ctk.CTkLabel(body, text="Paste your error / traceback:", anchor="w").grid(
            row=0, column=0, sticky="w"
        )
        self.error_box = ctk.CTkTextbox(body, font=("Consolas", 13), height=180)
        self.error_box.grid(row=1, column=0, sticky="nsew", pady=(0, 10))

        solve_btn = ctk.CTkButton(body, text="Solve Error", command=self.solve)
        solve_btn.grid(row=2, column=0, sticky="w", pady=(0, 10))

        ctk.CTkLabel(body, text="Explanation & Fixes:", anchor="w").grid(row=3, column=0, sticky="w")
        self.result_box = ctk.CTkTextbox(body, font=("Consolas", 13), text_color="#93c5fd")
        self.result_box.grid(row=4, column=0, sticky="nsew")
        self.result_box.configure(state="disabled")

    def solve(self):
        text = self.error_box.get("1.0", "end").strip()
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", "end")
        result = explain_error(text)
        if not result:
            self.result_box.insert("1.0", "Paste an error message or traceback first.")
        else:
            title, explanation, fixes = result
            fixes_text = "\n".join(f"  - {f}" for f in fixes)
            self.result_box.insert("1.0", f"{title}\n\n{explanation}\n\nSuggested fixes:\n{fixes_text}")
        self.result_box.configure(state="disabled")


class BrowseTopicsTab(ctk.CTkFrame):
    """Browse the whole knowledge base grouped by category."""

    def __init__(self, master, df: pd.DataFrame):
        super().__init__(master, fg_color="transparent")
        self.df = df

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(top, text="Category:").pack(side="left", padx=(0, 8))
        categories = ["All"] + sorted(df["category"].unique().tolist())
        self.category_var = ctk.StringVar(value="All")
        dropdown = ctk.CTkOptionMenu(
            top, values=categories, variable=self.category_var, command=lambda _: self.refresh()
        )
        dropdown.pack(side="left")

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.refresh()

    def refresh(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()

        category = self.category_var.get()
        subset = self.df if category == "All" else self.df[self.df["category"] == category]

        for _, row in subset.iterrows():
            card = ctk.CTkFrame(self.scroll, corner_radius=10)
            card.pack(fill="x", pady=6, padx=4)

            header = ctk.CTkLabel(
                card,
                text=f"{row['title']}  ·  {row['category']}",
                font=ctk.CTkFont(weight="bold", size=15),
                anchor="w",
            )
            header.pack(fill="x", padx=12, pady=(10, 2))

            explanation = ctk.CTkLabel(
                card, text=row["explanation"], anchor="w", justify="left", wraplength=760
            )
            explanation.pack(fill="x", padx=12, pady=(0, 6))

            code = ctk.CTkTextbox(card, font=("Consolas", 12), height=100)
            code.pack(fill="x", padx=12, pady=(0, 12))
            code.insert("1.0", row["code_example"])
            code.configure(state="disabled")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Python Learning Assistant")
        self.geometry("980x720")
        self.minsize(760, 560)

        df = load_knowledge_base()
        matcher = KnowledgeMatcher(df)

        header = ctk.CTkLabel(
            self,
            text="Python Learning Assistant",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        header.pack(pady=(14, 4))

        subtitle = ctk.CTkLabel(
            self,
            text="Ask questions, run & debug code, decode errors, and browse Python topics "
                 "- including OOP, regex, NumPy, Pandas, and Django.",
            text_color="#9ca3af",
        )
        subtitle.pack(pady=(0, 10))

        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        tab_ask = tabview.add("Ask / Learn")
        tab_run = tabview.add("Run & Debug")
        tab_error = tabview.add("Error Solver")
        tab_browse = tabview.add("Browse Topics")

        AskLearnTab(tab_ask, matcher).pack(fill="both", expand=True)
        RunDebugTab(tab_run).pack(fill="both", expand=True)
        ErrorSolverTab(tab_error).pack(fill="both", expand=True)
        BrowseTopicsTab(tab_browse, df).pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
