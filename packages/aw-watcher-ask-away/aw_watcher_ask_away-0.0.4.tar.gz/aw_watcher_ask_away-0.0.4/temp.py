import tkinter as tk


def show_help(event):
    help_text = tk.Toplevel(root)
    help_text.geometry(f"+{event.x_root+10}+{event.y_root+10}")  # Position the help text near the mouse pointer
    help_label = tk.Label(help_text, text='This is the help text!')
    help_label.pack()


def hide_help(event):
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel):
            widget.destroy()


root = tk.Tk()
label = tk.Label(root, text='Hover over me!')
label.pack()
label.bind('<Enter>', show_help)
label.bind('<Leave>', hide_help)
root.mainloop()
