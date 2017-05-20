import Tkinter as tk
import tkMessageBox

import time


class ResultsView:
    def __init__(self, root, frames):

        self.body = tk.Frame(root, bg='#e6e6e6')
        frames['results'] = self.body
        frames['results'].place(x=120, y=0, width=380, height=435)
        tk.Label(self.body, bg='#e6e6e6', text='Generate Report').place(x=102, y=2)
        self.results_btn = tk.Button(self.body,
                                     text='Today report',
                                     fg='#ffffff',
                                     bg='#3b5998', activebackground='#3b5998',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.results_btn.bind("<Button-1>", self.generate_report)
        self.results_btn.place(x=20, y=30)

        self.all_results_btn = tk.Button(self.body,
                                     text='All report',
                                     fg='#ffffff',
                                     bg='#3b5998', activebackground='#3b5998',
                                     borderwidth=0,
                                     highlightthickness=0,
                                     width=18, height=2)

        self.all_results_btn.bind("<Button-1>", self.generate_all_report)
        self.all_results_btn.place(x=170, y=30)

    def generate_report(self, event):
        self.results_btn.unbind("<Button-1>")
        Results().get_result_current_day()
        tkMessageBox.showinfo("Updated", "Report was generated successful")
        self.results_btn.bind("<Button-1>", self.generate_report)

    def generate_all_report(self, event):
        self.all_results_btn.unbind("<Button-1>")
        Results().get_all_result()
        tkMessageBox.showinfo("Updated", "Report was generated successful")
        self.all_results_btn.bind("<Button-1>", self.generate_all_report)
