"""Fake news detector GUI

This module contains all the logic needed to build the program's GUI.
"""

import fnd
import pickle
import os
import threading
import configurator

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from pathlib import Path
from ttkthemes import themed_style


class FakeDetector:

    def __init__(self, root) -> None:

        root.title('Fake News Detector')

        # Menu
        root.option_add('*tearOff', FALSE)
        menubar = Menu(root)
        root['menu'] = menubar

        menu_pref = Menu(menubar)
        menu_help = Menu(menubar)

        menu_theme = Menu(menu_pref)

        menubar.add_cascade(menu=menu_pref, label='Preferences', underline=0)
        menubar.add_cascade(menu=menu_help, label='Help', underline=0)

        menu_pref.add_cascade(menu=menu_theme, label='Theme', underline=0)

        self.s = themed_style.ThemedStyle(root)
        for theme_name in self.s.theme_names():
            # Using the i=i trick causes your function to store the current
            # value of i at the time your lambda is defined, instead of waiting
            # to look up the value of i later.
            menu_theme.add_command(
                label=theme_name,
                command=lambda theme_name=theme_name: self.update_theme(theme_name))

        menu_help.add_command(
            label='About',
            command=lambda: self.show_about(root), underline=0)

        self.configuration = configurator.Configurator()
        self.prefs = self.configuration.get_prefs()
        self.s.set_theme(self.prefs['theme'])

        self.interface_mode = StringVar()
        self.interface_mode.set(self.prefs['mode'])

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

        # temp
        self.set_interface(
            self.interface_mode.get(),
            self.mainframe)  # might want to rework
        # temp

        # TODO: CHECK IT'S NOT TOO BIG
        self.input_text = Text(self.mainframe, width=40, height=20)
        self.input_text.grid(
            column=0, row=1, rowspan=2, sticky=(
                N, W, E, S), padx=(
                10, 0))
        self.scroll_text = ttk.Scrollbar(
            self.mainframe, orient=VERTICAL, command=self.input_text.yview)
        self.scroll_text.grid(
            column=1, row=1, rowspan=2, sticky=(
                N, S, W), padx=(0, 10))  # sticky=(N,S)
        self.input_text.configure(yscrollcommand=self.scroll_text.set)

        labelfr_result = ttk.Labelframe(self.mainframe, text='Result')
        labelfr_result.grid(
            column=2, row=2, sticky=(
                N, W, S, E), pady=(
                10, 0), padx=10)
        self.analysis_result = StringVar()
        self.result_lb = ttk.Label(
            labelfr_result,
            textvariable=self.analysis_result)
        self.result_lb.grid(column=0, row=0)

        labelfr_result.columnconfigure(0, weight=1)
        labelfr_result.rowconfigure(0, weight=1)

        ttk.Button(
            self.mainframe,
            text='Analyse',
            state='active',
            command=self.analyse).grid(
            column=2,
            row=1, sticky=(E, W))  # sticky=W
        ttk.Button(self.mainframe, text='Close', command=root.destroy).grid(
            column=2, row=3, pady=(10, 0), sticky=(E, S))

        ttk.Label(
            self.mainframe,
            text='Put the text to analyze below \u2193').grid(
            column=0,
            row=0,
            sticky=(S, N))
        ttk.Label(
            self.mainframe,
            text='Click to start analysation \u2193').grid(
            column=2,
            row=0,
            sticky=S)

        if len(dir_list := os.listdir('./models')) != 0:
            if 'basic.pickle' in dir_list:
                self.unpickle_model('./models/basic.pickle')  # meh
            else:
                # have to check for exceptions down below
                self.unpickle_model('./models/' + dir_list[0])
        else:
            messagebox.showwarning(
                title='No models',
                message='No models detected. Create a model to use the app')

        # self.update_padding(self.mainframe)

        # Temporarily
        self.mainframe.columnconfigure((0, 2), weight=1)
        self.mainframe.rowconfigure((1, 2), weight=1)

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
        try:
            result = self.model.predict(self.input_text.get('1.0', 'end-1c'))
        except AttributeError:
            messagebox.showerror(
                title='No models',
                message='Can\'t analyse. No models detected. Create a model to use the app')
            return
        # messagebox.showinfo(
        #    self.input_text.get(
        #        '1.0', 'end-1c'))  # end-1c trim newline
        if result == ['FAKE']:
            self.analysis_result.set('The news is most likely FAKE!')
            self.result_lb['foreground'] = 'red'
        elif result == ['REAL']:
            self.analysis_result.set('The news is most likely REAL!')
            self.result_lb['foreground'] = 'green'

    def set_interface(self, mode, mainframe):
        # Not very OOP; maybe rework
        if mode == 'advanced':
            self.configuration.update_pref(mode='advanced')
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
            self.current_model_lb = ttk.Label(
                self.labelfr_advanced,
                textvariable=self.current_model)
            self.current_model_lb.grid(
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
                # maybe rework in case i need to check the directory in several
                # places? # should i also use lambda? # should update after
                # each click on update button # for now have to restart the
                # program
                values=self.get_models(),
                state='readonly', textvariable=self.selected_model)
            self.cb_models.grid(
                column=0,
                row=3)
            self.cb_models.bind(
                '<<ComboboxSelected>>',
                lambda e: self.unpickle_model(
                    './models/' +
                    self.selected_model.get() +
                    '.pickle'))  # test without lambda for interest # no need to put self in?
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
            ttk.Entry(
                self.labelfr_options,
                textvariable=self.model_name).grid(
                column=0,
                row=1)
            ttk.Label(
                self.labelfr_options,
                text='Classifier:').grid(
                column=1,
                row=0)
            self.CLASSIFIER_MAPPING = {
                'Passive Aggressive Classifier': fnd.PAClassifier,
                'Perceptron': fnd.Percept,
                'Multinomial Naive Bayes': fnd.MultiNB,
                'Complement Naive Bayes': fnd.ComplNB}
            self.CLASSIFIER_ITEMS = sorted(self.CLASSIFIER_MAPPING.keys())
            self.selected_classifier = StringVar()
            self.selected_classifier.set(
                'Passive Aggressive Classifier')  # self.CLASSIFIER_ITEMS[0] # tmp
            self.cb_classifier = ttk.Combobox(
                self.labelfr_options,
                textvariable=self.selected_classifier,
                values=self.CLASSIFIER_ITEMS,
                state='readonly')
            self.cb_classifier.grid(
                column=1,
                row=1)
            self.cb_classifier.bind(
                '<<ComboboxSelected>>',
                lambda e: self.disable_widgets(
                    self.CLASSIFIER_MAPPING[self.selected_classifier.get()]))
            ttk.Label(
                self.labelfr_options,
                text='Test Size:').grid(
                column=0,
                row=2)
            ttk.Label(
                self.labelfr_options,
                text='Train Size:').grid(
                column=0,
                row=3)
            self.spin_test = DoubleVar()
            self.spin_test.set(0.25)
            # change readonly to validation
            ttk.Spinbox(
                self.labelfr_options,
                from_=0.0,
                to=1.0,
                textvariable=self.spin_test,
                increment=0.05,
                format='%.2f',
                state='readonly').grid(
                column=1,
                row=2)
            self.spin_train = DoubleVar()
            self.spin_train.set(0.75)
            ttk.Spinbox(
                self.labelfr_options,
                from_=0.0,
                to=1.0,
                textvariable=self.spin_train,
                increment=0.05,
                format='%.2f',
                state='readonly').grid(
                column=1,
                row=3)
            ttk.Label(
                self.labelfr_options,
                text='Max Iterations:').grid(
                column=0,
                row=4)
            ttk.Label(
                self.labelfr_options,
                text='Early Stopping:').grid(
                column=0,
                row=5)
            self.spin_iter = IntVar()
            self.spin_iter.set(1000)
            self.sb_iter = ttk.Spinbox(
                self.labelfr_options,
                from_=0,
                to=10000,
                textvariable=self.spin_iter,
                increment=100)
            self.sb_iter.grid(
                column=1,
                row=4)  # add progress bar for big numbers
            self.spin_stopping = BooleanVar()  # not a spinbox: rename
            self.spin_stopping.set(False)
            self.ckbtn_stopping = ttk.Checkbutton(
                self.labelfr_options,
                variable=self.spin_stopping,
                onvalue=True,
                offvalue=False)
            self.ckbtn_stopping.grid(
                column=1,
                row=5)
            ttk.Button(
                self.labelfr_advanced,
                text='Create new...',  # maybe just Create new model?
                command=self.get_filename).grid(
                column=2,
                row=5,
                pady=(
                    10,
                    0))
            ttk.Button(
                self.labelfr_advanced,
                text='Export',
                command=self.export_model).grid(
                column=3,
                row=5,
                pady=(
                    10,
                    0))
            ttk.Button(
                self.labelfr_advanced,
                text='Update\\save',  # rename to just save?
                command=self.thread_helper).grid(
                column=4,
                row=5,
                pady=(
                    10,
                    0))

            # tmp
            self.labelfr_advanced.columnconfigure((2, 3, 4), weight=1)
            self.labelfr_advanced.rowconfigure((4), weight=1)
            # tmp

            # testing
            for child in self.labelfr_advanced.winfo_children(
            ):  # create a function(frame, padding, except for)
                child.grid_configure(padx=5, pady=5)

            for child in self.labelfr_options.winfo_children():
                child.grid_configure(padx=5, pady=5)

        elif mode == 'simple':
            self.configuration.update_pref(mode='simple')
            try:
                self.labelfr_advanced
            except AttributeError:
                pass  # is it even legal?
            else:
                self.labelfr_advanced.destroy()

    def get_models(self):
        return [os.path.splitext(file_name)[0]
                for file_name in os.listdir('./models')]

    def disable_widgets(self, classifier_class):
        # isinstance(classifier,fnd.LinearDetector) or
        if issubclass(classifier_class, fnd.LinearDetector):
            self.ckbtn_stopping['state'] = 'enabled'
            self.sb_iter['state'] = 'enabled'
        else:
            self.ckbtn_stopping['state'] = 'disabled'
            self.sb_iter['state'] = 'disabled'

    def export_model(self):
        path = filedialog.asksaveasfilename(
            initialfile='myModel.pickle',
            initialdir='./models',
            filetypes=[
                ("pickle files",
                 ".pickle"),
                ("all files",
                 "*.*")])  # file type; more flair
        # make sure that path is set
        if path == ():
            return
        self.pickle_model(
            self.model,
            path)  # file type; more flair

    def update_theme(self, theme_name):
        self.configuration.update_pref(theme=theme_name)
        self.s.set_theme(theme_name)

    def get_filename(self):
        self.file = filedialog.askopenfile(
            filetypes=[("CSV files", ".csv"), ("all files", "*.*")])  # check if cancelled
        # use regex to propose a default file name
        try:
            self.current_model.set(self.file.name + ' <Unsaved>')
        except AttributeError:
            return
        self.current_model_lb['foreground'] = 'red'  # make red
        self.cb_models.set('')
        # self.model_name.set(os.path.basename(os.path.normcase(self.file.name)))
        self.model_name.set(Path(self.file.name).stem)

    def thread_helper(self):
        # with Pool() as p:
        #    p.apply(func=self.create_model)
        # works but multiprocessing would be better
        self.prog_bar = ttk.Progressbar(
            self.labelfr_advanced,
            orient=HORIZONTAL,
            length=460,
            mode='indeterminate')
        self.prog_bar.grid(row=4, column=2, columnspan=3)
        self.prog_bar.start()
        t = threading.Thread(target=self.create_model)
        t.start()
        # t.join()

    # def multiprocess_model(self):
    #    # use queue? # add a progress bar
    #    p = multiprocessing.Process(target=self.create_model)
    #    p.start()
    #    p.join()
    #    #p.close()

    def update_after_create(self):
        self.set_labels(self.model)
        self.cb_models['values'] = self.get_models()
        self.prog_bar.stop()
        self.prog_bar.destroy()

    def create_model(self):
        if self.spin_test.get() + self.spin_train.get() != 1.0:
            if messagebox.askyesno(
                    title='Potential mistake',
                    message='It is recommended that Train Size and Test Size be set to give 1.0 in sum. Are you sure that you want to continue?',
                    default='no') is False:
                return
        try:
            self.model = self.CLASSIFIER_MAPPING[self.selected_classifier.get()](data=self.file, test_size=self.spin_test.get(
            ), train_size=self.spin_train.get(), max_iter=self.spin_iter.get(), early_stopping=self.spin_stopping.get())
            self.file.close()
        except (AttributeError, ValueError):
            try:
                self.model = self.CLASSIFIER_MAPPING[self.selected_classifier.get()](data_frame=self.model.data_frame, test_size=self.spin_test.get(
                ), train_size=self.spin_train.get(), max_iter=self.spin_iter.get(), early_stopping=self.spin_stopping.get())
            except AttributeError:
                messagebox.showerror(
                    title='Error occured',
                    message='An error has occured. Check that your data is a .csv file with utf-8 encoding')
                return

        self.pickle_model(
            self.model,
            './models/' +
            self.model_name.get() +
            '.pickle')
        self.update_after_create()

    def pickle_model(self, model, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(model, f, pickle.HIGHEST_PROTOCOL)

    def unpickle_model(self, file_path):
        with open(file_path, 'rb') as f:
            self.model = pickle.load(f)
        self.set_labels(self.model)

    def set_labels(self, model):
        if self.interface_mode.get() == 'advanced':
            self.accuracy.set(round(model.score * 100, 2))
            self.stats.set(model.matrix)
            if self.model_name.get() == '':
                self.model_name.set(self.selected_model.get())
            self.current_model.set(self.model_name.get())
            self.current_model_lb['foreground'] = ''
            self.spin_test.set(model.test_size)
            self.spin_train.set(model.train_size)
            self.selected_classifier.set(str(model))

            if isinstance(model, fnd.LinearDetector):
                # enable max iter and early stopping
                # have to send classes in; else cant check for both class and
                # isntance
                self.disable_widgets(model.__class__)
                self.spin_iter.set(model.max_iter)
                self.spin_stopping.set(model.early_stopping)
            else:
                # disable max iter and early stop
                self.disable_widgets(model.__class__)

    def show_about(self, root):
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
            row=0, columnspan=2)
        ttk.Label(
            frame_about,
            text='Made with: Python 3.10.4, Tk 8.6').grid(
            column=0,
            row=1, columnspan=2)
        ttk.Label(frame_about,
                  text='Licensed under the Apache-2.0 license').grid(column=0,
                                                                     row=2,
                                                                     columnspan=2)
        ttk.Label(frame_about,
                  text='Link to code: ').grid(column=0, row=3)
        link_to_code = ttk.Entry(frame_about, width=40)
        link_to_code.grid(column=1, row=3)
        link_to_code.insert(
            0, 'https://github.com/P1car00n/fake-news-detector')
        link_to_code['state'] = 'readonly'
        ttk.Button(
            frame_about,
            text='Close',
            command=win_about.destroy,
            state='active').grid(
            column=1,
            row=4,
            sticky=(E, S))
        frame_about.columnconfigure((0, 1), weight=1)
        frame_about.rowconfigure((0, 1, 2, 3), weight=1)
        win_about.bind('<Return>', lambda e: win_about.destroy())

        for child in frame_about.winfo_children():
            child.grid_configure(padx=5, pady=5)


if __name__ == '__main__':
    if not os.path.exists(
            path_to_check := './models'):
        os.makedirs(path_to_check)
    root = Tk()
    FakeDetector(root)
    root.mainloop()
