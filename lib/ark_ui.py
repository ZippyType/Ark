"""
Ark UI Library - Cross-platform GUI toolkit for Ark
Built on top of tkinter but with native Ark syntax
"""

import tkinter as tk
from tkinter import font as tkfont
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from interpreter import Function


class ArkWidget:
    def __init__(self, widget):
        self._widget = widget
    
    def config(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, Font):
                self._widget.config(font=value._font)
            elif isinstance(value, Color):
                pass
            else:
                self._widget.config(**{key: value})
        return self
    
    def pack(self, **kwargs):
        self._widget.pack(**kwargs)
        return self
    
    def grid(self, **kwargs):
        self._widget.grid(**kwargs)
        return self
    
    def bind(self, event, callback):
        self._widget.bind(event, lambda e: callback())
        return self
    
    def get(self):
        return self._widget.get() if hasattr(self._widget, 'get') else ""
    
    def delete(self, start, end=None):
        if hasattr(self._widget, 'delete'):
            if end:
                self._widget.delete(start, end)
            else:
                self._widget.delete(start)
        return self
    
    def insert(self, index, text):
        if hasattr(self._widget, 'insert'):
            self._widget.insert(index, text)
        return self


class Window(ArkWidget):
    def __init__(self, title: str = "Ark Window", width: int = 400, height: int = 300):
        self._root = tk.Tk()
        self._root.title(title)
        self._root.geometry(f"{width}x{height}")
        self._widgets = []
        super().__init__(self._root)
    
    def button(self, text: str = "", **kwargs):
        btn = tk.Button(self._root, text=text, command=self._make_handler(kwargs.get('command')))
        if 'command' in kwargs:
            del kwargs['command']
        widget = ArkWidget(btn)
        self._widgets.append(widget)
        return widget
    
    def label(self, text: str = "", **kwargs):
        lbl = tk.Label(self._root, text=text, **kwargs)
        widget = ArkWidget(lbl)
        self._widgets.append(widget)
        return widget
    
    def entry(self, **kwargs):
        ent = tk.Entry(self._root, **kwargs)
        widget = ArkWidget(ent)
        self._widgets.append(widget)
        return widget
    
    def text(self, **kwargs):
        txt = tk.Text(self._root, **kwargs)
        widget = ArkWidget(txt)
        self._widgets.append(widget)
        return widget
    
    def checkbox(self, text: str = "", **kwargs):
        var = tk.BooleanVar(value=False)
        cb = tk.Checkbutton(self._root, text=text, variable=var, **kwargs)
        widget = ArkWidget(cb)
        widget._var = var
        self._widgets.append(widget)
        return widget
    
    def canvas(self, width: int = 200, height: int = 200, **kwargs):
        cnv = tk.Canvas(self._root, width=width, height=height, **kwargs)
        widget = ArkWidget(cnv)
        self._widgets.append(widget)
        return widget
    
    def listbox(self, **kwargs):
        lst = tk.Listbox(self._root, **kwargs)
        widget = ArkWidget(lst)
        self._widgets.append(widget)
        return widget
    
    def menu(self, **kwargs):
        m = tk.Menu(self._root, **kwargs)
        widget = ArkWidget(m)
        self._widgets.append(widget)
        return widget
    
    def frame(self, **kwargs):
        frm = tk.Frame(self._root, **kwargs)
        widget = ArkWidget(frm)
        self._widgets.append(widget)
        return widget
    
    def _make_handler(self, callback):
        if callback is None:
            return lambda: None
        if isinstance(callback, Function):
            return lambda: callback(None)
        if callable(callback):
            return callback
        return lambda: None
    
    def mainloop(self):
        self._root.mainloop()
    
    def destroy(self):
        self._root.destroy()
    
    @property
    def width(self):
        return self._root.winfo_width()
    
    @property
    def height(self):
        return self._root.winfo_height()


class Color:
    RED = "#ff0000"
    GREEN = "#00ff00"
    BLUE = "#0000ff"
    YELLOW = "#ffff00"
    ORANGE = "#ff8800"
    PURPLE = "#8800ff"
    WHITE = "#ffffff"
    BLACK = "#000000"
    GRAY = "#888888"
    LIGHT_GRAY = "#cccccc"
    DARK_GRAY = "#333333"


class Font:
    def __init__(self, family: str = "Arial", size: int = 12, weight: str = "normal"):
        self._font = tkfont.Font(family=family, size=size, weight=weight)
    
    def bold(self):
        return Font(self._font.actual('family'), self._font.actual('size'), 'bold')
    
    def italic(self):
        return Font(self._font.actual('family'), self._font.actual('size'), 'italic')


WINDOW = "window"
BUTTON = "button"
LABEL = "label"
ENTRY = "entry"
TEXT = "text"
CHECKBOX = "checkbox"
CANVAS = "canvas"
LISTBOX = "listbox"
MENU = "menu"
FRAME = "frame"

LEFT = tk.LEFT
RIGHT = tk.RIGHT
TOP = tk.TOP
BOTTOM = tk.BOTTOM
NONE = tk.NONE
BOTH = tk.BOTH
X = tk.X
Y = tk.Y
CENTER = tk.CENTER

N = tk.N
S = tk.S
E = tk.E
W = tk.W
NE = tk.NE
NW = tk.NW
SE = tk.SE
SW = tk.SW

END = tk.END
ANCHOR = tk.ANCHOR
CURRENT = tk.CURRENT


def create_window(title: str = "Ark Window", width: int = 400, height: int = 300):
    win = Window(title, width, height)
    return win

def create_button(parent, text: str = "", command=None):
    if isinstance(parent, Window):
        return parent.button(text, command=command)
    btn = tk.Button(parent._widget if hasattr(parent, '_widget') else parent, text=text, command=command or (lambda: None))
    return ArkWidget(btn)

def create_label(parent, text: str = "", **kwargs):
    if isinstance(parent, Window):
        return parent.label(text, **kwargs)
    lbl = tk.Label(parent._widget if hasattr(parent, '_widget') else parent, text=text, **kwargs)
    return ArkWidget(lbl)

def create_entry(parent, **kwargs):
    if isinstance(parent, Window):
        return parent.entry(**kwargs)
    ent = tk.Entry(parent._widget if hasattr(parent, '_widget') else parent, **kwargs)
    return ArkWidget(ent)

def create_canvas(parent, width: int = 200, height: int = 200, **kwargs):
    if isinstance(parent, Window):
        return parent.canvas(width, height, **kwargs)
    cnv = tk.Canvas(parent._widget if hasattr(parent, '_widget') else parent, width=width, height=height, **kwargs)
    return ArkWidget(cnv)

def run_window(win):
    win.mainloop()

def message(text: str, title: str = "Ark", type: str = "info"):
    if type == "error":
        tk.messagebox.showerror(title, text)
    elif type == "warning":
        tk.messagebox.showwarning(title, text)
    elif type == "question":
        return tk.messagebox.askyesno(title, text)
    else:
        tk.messagebox.showinfo(title, text)

def ask_yes_no(question: str, title: str = "Ark"):
    return tk.messagebox.askyesno(title, question)

def ask_file(title: str = "Open File", filetypes=None):
    if filetypes is None:
        filetypes = [("All Files", "*.*")]
    return tk.filedialog.askopenfilename(title=title, filetypes=filetypes)

def ask_save_file(title: str = "Save File", filetypes=None):
    if filetypes is None:
        filetypes = [("All Files", "*.*")]
    return tk.filedialog.asksaveasfilename(title=title, filetypes=filetypes)

def ask_directory(title: str = "Choose Directory"):
    return tk.filedialog.askdirectory(title=title)

def get(widget):
    return widget.get()

def config(widget, **kwargs):
    return widget.config(**kwargs)

def pack(widget, **kwargs):
    return widget.pack(**kwargs)

def grid(widget, **kwargs):
    return widget.grid(**kwargs)