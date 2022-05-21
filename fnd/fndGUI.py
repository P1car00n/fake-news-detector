"""Fake news detector GUI

This module contains all the logic needed to build the program's GUI.
"""
import fnd
import pickle
import os

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from pathlib import Path


class FakeDetector:

    def __init__(self, root) -> None:

        root.title('Fake News Detector')

        # Menu
        root.option_add('*tearOff', FALSE)
        menubar = Menu(root)
        root['menu'] = menubar

        menu_pref = Menu(menubar)
        menu_help = Menu(menubar)

        menubar.add_cascade(menu=menu_pref, label='Preferences', underline=0)
        menubar.add_cascade(menu=menu_help, label='Help', underline=0)

        menu_help.add_command(
            label='About',
            command=lambda: self.show_about(root), underline=0)

        self.interface_mode = StringVar()
        menu_pref.add_checkbutton(
            label='Activate advanced mode',
            command=lambda: self.set_interface(
                self.interface_mode.get(),
                self.mainframe),
            variable=self.interface_mode,
            onvalue='advanced',
            offvalue='simple',
            underline=0)

        # Main frame
        # Why did i make it self?
        self.mainframe = ttk.Frame(root, padding='3 3 12 12')
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # TODO: CHECK IT'S NOT TOO BIG
        self.input_text = Text(self.mainframe, width=40, height=10)
        self.input_text.grid(
            column=0, row=2, rowspan=2, sticky=(
                N, W, E, S), padx=(
                10, 0))
        self.scroll_text = ttk.Scrollbar(
            self.mainframe, orient=VERTICAL, command=self.input_text.yview)
        self.scroll_text.grid(
            column=1, row=2, rowspan=2, sticky=(
                N, S, W), padx=(0, 10))  # sticky=(N,S)
        self.input_text.configure(yscrollcommand=self.scroll_text.set)

        labelfr_result = ttk.Labelframe(self.mainframe, text='Result')
        labelfr_result.grid(
            column=2, row=3, sticky=(
                N, W, S, E), pady=(
                10, 0), padx=10)
        self.analysis_result = StringVar()
        ttk.Label(
            labelfr_result,
            textvariable=self.analysis_result).grid(
            column=0,
            row=0)

        ttk.Button(
            self.mainframe,
            text='Analyse',
            state='active',
            command=self.analyse).grid(
            column=2,
            row=2)  # sticky=W
        ttk.Button(self.mainframe, text='Close', command=root.destroy).grid(
            column=2, row=4, pady=(10, 0))

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

        if len(dir_list:=os.listdir('./models')) != 0:
            if 'basic.pickle' in dir_list:
                self.unpickle_model('./models/basic.pickle') # meh
            else:
                self.unpickle_model('./models/' + dir_list[0]) # have to check for exceptions down below
        else:
            messagebox.showwarning(title='No models', message='No models detected. Create a model to use the app')

        # self.update_padding(self.mainframe)

        # Temporarily
        self.mainframe.columnconfigure(tuple(range(10)), weight=1)
        self.mainframe.rowconfigure(tuple(range(10)), weight=1)

        # This code is bad: refactor it somehow
        # for child in self.mainframe.winfo_children():
        #    name = str(child)
        #    if name == '.!frame.!scrollbar':
        #        child.grid_configure(padx=(0, 5), pady=5)
        #        continue
        #    elif name == '.!frame.!text':
        #        child.grid_configure(padx=(5, 0), pady=5)
        #        continue
        #    elif name == '.!frame.!button2':
        #        continue
        #    child.grid_configure(padx=5, pady=5)

        self.input_text.focus_set()
        root.bind('<Return>', self.analyse)

    # def update_padding(self, frame):
    #    columns, rows = frame.grid_size()
    #    frame.rowconfigure(rows, pad=5)
    #    frame.columnconfigure(columns, pad=5)

    def analyse(self, *args):
        # end-1c trim newline # there still is a newline \n
        result = self.model.predict(self.input_text.get('1.0', 'end-1c'))
        # messagebox.showinfo(
        #    self.input_text.get(
        #        '1.0', 'end-1c'))  # end-1c trim newline
        self.analysis_result.set(result)

    def set_interface(self, mode, mainframe):
        # Not very OOP; maybe rework
        if mode == 'advanced':
            self.labelfr_advanced = ttk.Labelframe(
                mainframe, text='Advanced Interface')
            self.labelfr_advanced.grid(
                column=3, row=0, rowspan=4, sticky=(
                    N, W, S, E), pady=(10, 0), padx=10)
            ttk.Label(
                self.labelfr_advanced,
                text='Current model:').grid(
                column=0,
                row=0)
            self.current_model = StringVar()
            ttk.Label(
                self.labelfr_advanced,
                textvariable=self.current_model).grid(
                column=0,
                row=1)
            ttk.Label(
                self.labelfr_advanced,
                text='Choose a model:').grid(
                column=0,
                row=2)
            self.selected_model = StringVar()
            self.cb_models = ttk.Combobox(
                self.labelfr_advanced,
                values=[os.path.splitext(file_name)[0] for file_name in os.listdir('./models')], # maybe rework in case i need to check the directory in several places? # should i also use lambda? # should update after each click on update button
                state='readonly', textvariable=self.selected_model)
            self.cb_models.grid(
                column=0,
                row=3)
            self.cb_models.bind('<<ComboboxSelected>>', lambda e: self.unpickle_model('./models/' + self.selected_model.get() + '.pickle')) # test without lambda for interest # no need to put self in?
            ttk.Label(
                self.labelfr_advanced,
                text='Accuracy:').grid(
                column=1,
                row=0)
            self.accuracy = StringVar()
            ttk.Label(
                self.labelfr_advanced,
                textvariable=self.accuracy).grid(
                column=1,
                row=1)
            ttk.Label(
                self.labelfr_advanced,
                text='Confusion matrix:').grid(
                column=1,
                row=2)
            self.stats = StringVar()
            ttk.Label(
                self.labelfr_advanced,
                textvariable=self.stats).grid(
                column=1,
                row=3)
            self.labelfr_options = ttk.Labelframe(
                self.labelfr_advanced, text=r'Options\tweaks')
            self.labelfr_options.grid(
                column=2, row=0, columnspan=3, rowspan=4, sticky=(
                    N, W, S, E), pady=(10, 0), padx=10)
            ttk.Label(
                self.labelfr_options,
                text='Name of the model:').grid(
                column=0,
                row=0)
            self.model_name = StringVar()
            ttk.Entry(self.labelfr_options, textvariable=self.model_name).grid(column=0, row=1)
            ttk.Button(
                self.labelfr_advanced,
                text='Create new...',  # maybe just Create new model?
                command=self.get_filename).grid(
                column=2,
                row=4,
                pady=(
                    10,
                    0))
            ttk.Button(
                self.labelfr_advanced,
                text='Export as...',  # probably better just export
                command=lambda: print('i work')).grid(
                column=3,
                row=4,
                pady=(
                    10,
                    0))
            ttk.Button(
                self.labelfr_advanced,
                text='Update\\save',
                command=self.create_model).grid(
                column=4,
                row=4,
                pady=(
                    10,
                    0))
        elif mode == 'simple':
            self.labelfr_advanced.destroy()

    def get_filename(self):
        self.file = filedialog.askopenfile(
            filetypes=[("CSV files", ".csv"), ("all files", "*.*")])
        # use regex to propose a default file name
        self.current_model.set(self.file.name + ' <Unsaved>')  # make red
        self.cb_models.set('')
        # self.model_name.set(os.path.basename(os.path.normcase(self.file.name)))
        self.model_name.set(Path(self.file.name).stem)

    def create_model(self):
        # think how to make use of picling\unpickling
        # if click update again -- error IO on closed file -- 
        # should just create models from pickle
        self.model = fnd.PAClassifier(self.file)
        self.file.close()  # check if closed -- maybe no need to close
        # should do it with combobox
        # make score into a property? # print(f'Accuracy:
        # {round(score*100,2)}%') user friendliness
        self.accuracy.set(self.model.score)
        self.stats.set(self.model.matrix)
        self.pickle_model(self.model, './models/' + self.model_name.get() + '.pickle')
    
    def pickle_model(self, model, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(model, f, pickle.HIGHEST_PROTOCOL)

    def unpickle_model(self, file_path):
        with open(file_path, 'rb') as f:
            self.model = pickle.load(f)

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
    if not os.path.exists(path_to_check:='./models'): # check if works on windows
        os.makedirs(path_to_check)
    root = Tk()
    FakeDetector(root)
    root.mainloop()

# TODO: make the arrows point exactly at the respective buttons; 95% True
# appears not directly under the button 'Analyse'. add (decent) resizing support
# for the main window. Check macos support. Put grid statements separately?
# Add paste to the textbox? Theming support? Contextual menu? Add better
# docstrings?
