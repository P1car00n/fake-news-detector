"""Fake news detector GUI

This module contains all the logic needed to build the program's GUI.
"""

from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class FakeDetector:

    def __init__(self, root) -> None:

        root.title('Fake News Detector')

        # Menu
        root.option_add('*tearOff', FALSE)
        menubar = Menu(root)
        root['menu'] = menubar

        menu_pref = Menu(menubar)
        menu_help = Menu(menubar)

        menubar.add_cascade(menu=menu_pref, label='Preferences')
        menubar.add_cascade(menu=menu_help, label='Help')

        menu_help.add_command(
            label='About',
            command=lambda: self.showAbout(root))

        mainframe = ttk.Frame(root, padding='3 3 12 12')
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.input_text = StringVar()
        input_text_entry = ttk.Entry(
            mainframe, textvariable=self.input_text)  # width=7
        input_text_entry.grid(column=1, row=2, rowspan=2, sticky=(N, W, E, S))

        self.analysis_result = StringVar()
        ttk.Label(mainframe, textvariable=self.analysis_result).grid(
            column=2, row=3, sticky=(N, W, S, E))

        ttk.Button(mainframe, text='Analyse', command=self.analyse).grid(
            column=2, row=2)  # sticky=W
        ttk.Button(mainframe, text='Advanced', command=self.analyse).grid(
            column=3, row=2, sticky=W)

        ttk.Label(mainframe, text='Put the text to analyze below \u2193').grid(
            column=1, row=1, sticky=S)
        ttk.Label(mainframe, text='Click to start analysation \u2193').grid(
            column=2, row=1, sticky=S)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        input_text_entry.focus()
        root.bind('<Return>', self.analyse)

    def analyse(self, *args):
        messagebox.showinfo(self.input_text.get())
        self.analysis_result.set('95% True')

    def showAbout(self, root):
        # Potentially replace with OOP
        win_about = Toplevel(root)
        win_about.title('About Fake News Detector')
        win_about.columnconfigure(0, weight=1)
        win_about.rowconfigure(0, weight=1)
        frame_about = ttk.Frame(win_about, padding='3 3 12 12')
        frame_about.grid(column=0, row=0, sticky=(N, W, E, S))
        ttk.Label(
            frame_about,
            text='Creator: Arthur Zevaloff').grid(
            column=0,
            row=0)
        ttk.Label(
            frame_about,
            text='Made with: Python 3.10.4, Tk 8.6').grid(
            column=0,
            row=1)
        ttk.Label(frame_about,
                  text='Licensed under the Apache-2.0 license').grid(column=0,
                                                                     row=2)
        frame_about.columnconfigure(0, weight=1)
        frame_about.rowconfigure((0, 1, 2, 3), weight=1)
        ttk.Button(
            frame_about,
            text='Close',
            command=win_about.destroy,
            state='active').grid(
            column=0,
            row=3,
            sticky=(E))
        win_about.bind('<Return>', lambda e: win_about.destroy())

        for child in frame_about.winfo_children():
            child.grid_configure(padx=5, pady=5)


if __name__ == '__main__':
    root = Tk()
    FakeDetector(root)
    root.mainloop()

# TODO: make the arrows point exactly at the respective buttons; 95% True
# appears not directly under the button 'Analyse'. Replce entry with
# text area. add resizing support for the main window. Check macos support
