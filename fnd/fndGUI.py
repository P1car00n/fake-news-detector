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

        self.interface_mode = StringVar()
        menu_pref.add_checkbutton(
            label='Activate advanced mode',
            command=lambda: self.set_interface(
                self.interface_mode.get(),
                self.mainframe),
            variable=self.interface_mode,
            onvalue='advanced',
            offvalue='simple')

        # Main frame
        self.mainframe = ttk.Frame(root, padding='3 3 12 12')
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # TODO: CHECK IT'S NOT TOO BIG
        self.input_text = Text(self.mainframe, width=40, height=10)
        self.input_text.grid(column=0, row=2, rowspan=2, sticky=(N, W, E, S))
        self.scroll_text = ttk.Scrollbar(
            self.mainframe, orient=VERTICAL, command=self.input_text.yview)
        self.scroll_text.grid(
            column=1, row=2, rowspan=2, sticky=(
                N, S, W))  # sticky=(N,S)
        self.input_text.configure(yscrollcommand=self.scroll_text.set)

        labelfr_result = ttk.Labelframe(self.mainframe, text='Result')
        labelfr_result.grid(column=2, row=3, sticky=(N, W, S, E))
        self.analysis_result = StringVar()
        ttk.Label(
            labelfr_result,
            textvariable=self.analysis_result).grid(
            column=0,
            row=0)

        ttk.Button(self.mainframe, text='Analyse', command=self.analyse).grid(
            column=2, row=2)  # sticky=W
        ttk.Button(self.mainframe, text='Close', command=self.analyse).grid(
            column=2, row=4)

        ttk.Label(
            self.mainframe,
            text='Put the text to analyze below \u2193').grid(
            column=0,
            row=0,
            sticky=S)
        ttk.Label(
            self.mainframe,
            text='Click to start analysation \u2193').grid(
            column=2,
            row=0,
            sticky=S)

        # for child in self.mainframe.winfo_children():
        #    if str(child) == '.!frame.!scrollbar':
        #        print('found')
        #        continue
        #    child.grid_configure(padx=5, pady=5)

        self.input_text.focus_set()
        root.bind('<Return>', self.analyse)

    def analyse(self, *args):
        messagebox.showinfo(
            self.input_text.get(
                '1.0', 'end-1c'))  # end-1c trim newline
        self.analysis_result.set('95% True')

    def set_interface(self, mode, mainframe):
        # Not very OOP; maybe rework
        if mode == 'advanced':
            self.labelfr_advanced = ttk.Labelframe(
                mainframe, text='Advanced Interface')
            self.labelfr_advanced.grid(
                column=3, row=0, rowspan=4, sticky=(
                    N, W, S, E))
            ttk.Label(
                self.labelfr_advanced,
                text='Placeholder').grid(
                column=0,
                row=0)
        elif mode == 'simple':
            self.labelfr_advanced.destroy()

    def show_about(self, root):
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
# appears not directly under the button 'Analyse'. add resizing support
# for the main window. Check macos support. Put grid statements separately?
# Add paste to the textbox?
