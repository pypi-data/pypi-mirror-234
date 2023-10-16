import tkinter as tk
from tkinter import ttk
''' Progress bar for loading with one input '''

class progressLoadBar(tk.Tk):
    ''' Progress bar for loading with one input '''
    def __init__(self):
        super().__init__()
        self.geometry("400x50")
        self.title("Loading...")
        self.progress = ttk.Progressbar(self, orient="horizontal", length=350, mode="determinate")
        self.progress.pack(pady=20)

    def load_update(self,new_value):
        ''' Change bar to specific value '''
        self.progress["value"] = new_value
        self.progress.start()
        self.progress.update()
        self.progress.stop()

class UpDownButton(tk.Frame):
    '''special type of button'''
    def __init__(self, master,value=5):
        super().__init__(master)

        self.font = value
        self.up_button = tk.Button(self, text="▲", width=1, height=1, command=self.increment)
        self.up_button.pack(side="top")

        self.label = tk.Label(self, width=1, height=1, text=self.font)
        self.label.pack(side="top")

        self.down_button = tk.Button(self, text="▼", width=1, height=1, command=self.decrement)
        self.down_button.pack(side="top")

    def increment(self):
        if self.font < 50:
            self.font += 1
            self.label.config(text=self.font)

    def decrement(self):
        if self.font > 1:
            self.font -= 1
            self.label.config(text=self.font)

    def get_val(self):
        return self.font

class EntryLock(tk.Frame):
    ''' Entry with checkbox that turns entry on/off, while off insertion of text is disabled. '''
    def __init__(self, master=None,text=None, background=None, width=4):
        super().__init__(master)
        self.locked = tk.BooleanVar()
        self.locked.set(False)
        self.config(bg=background)

        self.entry = tk.Entry(self, state=tk.DISABLED if self.locked.get()==False else tk.NORMAL, width=width)
        self.entry.grid(row=0, column=0)

        self.lock_checkbutton = tk.Checkbutton(self, text=text, variable=self.locked, command=self.update_state,bg=background)
        self.lock_checkbutton.grid(row=0, column=1)

    def update_state(self):
        self.entry.config(state=tk.DISABLED if self.locked.get() == False else tk.NORMAL)

class EntryWithPlaceholder(tk.Entry):
    ''' Entry that has grey text as background. '''
    def __init__(self, master=None, text="", background=None, width=None):
        super().__init__(master)
        self.placeholder = text
        self.placeholder_color = "grey"
        self.default_color = self["fg"]

        if background:
            self.configure(bg=background)

        if width:
            self.configure(width=width)

        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

        self.add_placeholder()

    def add_placeholder(self):
        self.insert(0, self.placeholder)
        self.config(fg=self.placeholder_color)

    def on_focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, "end")
            self.config(fg=self.default_color)

    def on_focus_out(self, event):
        if not self.get():
            self.add_placeholder()

class InfoCircleLabel(tk.Label):
    ''' Label with question mark that show info when cursor hover above it '''
    def __init__(self, master, info_text):
        super().__init__(master)
        self.info_text = info_text
        self.info_window = None
        self.create_circle_icon()
        self.bind("<Enter>", self.show_info)
        self.bind("<Leave>", self.hide_info)

    def create_circle_icon(self):
        size = 24  # Adjust the size of the circle
        self.circle_icon = tk.Canvas(self, width=size, height=size, bg=None, highlightthickness=0)
        self.circle_icon.create_oval(4, 4, size-4, size-4, outline="gray", width=2)
        self.circle_icon.create_text(size // 2, size // 2, text="?", fill="gray", font=("Helvetica", 12, "bold"))
        self.circle_icon.pack()

    def show_info(self, event):
        if not self.info_window:
            self.info_window = tk.Toplevel(self.master)
            self.info_window.wm_overrideredirect(True)
            self.info_window.wm_geometry("+{}+{}".format(event.x_root, event.y_root))
            self.info_window_label = tk.Label(self.info_window, text=self.info_text, bg="lightgray")
            self.info_window_label.pack(ipadx=10, ipady=5)

    def hide_info(self, event):
        if self.info_window:
            self.info_window.destroy()
            self.info_window = None