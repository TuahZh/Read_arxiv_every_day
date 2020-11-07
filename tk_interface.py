#########################################################################
# File Name: tk_interface.py
# Author: ZHANG, Gao-Yuan
# mail: zgy0106@gmail.com
# Created Time: Fri Nov  6 18:52:10 2020
#########################################################################
#description

#!/bin/env python

from pylab import *
import tkinter as tk
from papers import *
from io import StringIO
import sys
from tkinter import messagebox



class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.today = tk.Button(self)
        self.today["text"] = "Today"
        self.today["command"] = self.search_today
        self.today.pack(side=tk.TOP)

        self.text = tk.Text(self)

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side=tk.BOTTOM)

    def search_today(self):
#        self.today.pack_forget()
#        self.today["text"] = "Fetching"
#        self.today.pack(side=tk.TOP)
        # not working
        self.fin = False
        pl, ts = arxiv_reading()
        lp_c = ListPapers(pl)
        self.text.insert(tk.END, mystdout.getvalue())
        self.text.pack(sid=tk.TOP)
        try:
            lp_c.add_key_words(self._kws, self._boost)
        except AttributeError:
            pass
        try:
            for kk, ss in zip(self._fs, self._fs_sign):
                if(ss<=0):
                    lp_d = lp_c.filter_subjects(self._fs, exclude=True)
                else:
                    lp_d = lp_c.filter_subjects(self._fs, exclude=False)
        except AttributeError:
            lp_d = lp_c
        self.text.insert(tk.END, lp_d.summary(called_tk=True))
        self._lp = lp_d
        self._cur_id = 0
        self.today.pack_forget()
        self.seguir = tk.Button(self, text="Continue", fg="red",
                                command=self.seguir)
        self.seguir.pack(side=tk.RIGHT)
        self.quit.pack_forget()
        self.quit.pack(side=tk.LEFT)

    def seguir(self):
        try:
            sigp_n = self._sigp_n
        except AttributeError:
            sigp_n = 2
            self._sigp_n = sigp_n
        if(self._lp.tot_num<=sigp_n):
            sigp_n = self._lp.tot_num
            self.fin = True
        if (sigp_n<=0):
            self.next()
            return
        try:
            sync = self._sync
        except AttributeError:
            sync = False
        res = self._lp.head(n=sigp_n, sync=sync, called_tk=True)
        self.head_setup()
        self.text.pack_forget()
        self.show_items(self._hd_setups, res)
        self.seguir.pack_forget()
        self.seguir["text"] = "Next"
        self.seguir["command"] = self.next
        self.seguir.pack(side=tk.RIGHT)
        self.quit.pack_forget()
        self.quit.pack(side=tk.LEFT)

    def show_message(self, mes):
        messagebox.showinfo("Message", mes)

    def next(self):
        try:
            n_perp = self._n_perp
        except AttributeError:
            n_perp = 4
            self._n_perp = n_perp
        res = self._lp.next(n=n_perp, cur_id=self._cur_id,
                            sync=False, called_tk=True)
        self.next_setup()
        widget_list = self.all_children()
        for item in widget_list:
            item.pack_forget()
        if (self._cur_id+n_perp>=self._lp.tot_num):
            self.fin = True
        self.show_items(self._nx_setups, res)
        self.seguir.pack(side=tk.RIGHT)
        self.quit.pack(side=tk.LEFT)

    def head_setup(self):
        try:
            hd_setups = self._hd_setups
        except AttributeError:
            hd_setups = {'ID':True, 'authors': True, 'title': True,
                         'abstract': True, 'date': True, 'comments': True,
                         'subjects': True, 'score': True}
            self._hd_setups = hd_setups

    def next_setup(self):
        try:
            nx_setups = self._nx_setups
        except AttributeError:
            nx_setups = {'ID':True, 'authors': True, 'title': True,
                         'abstract': False, 'date': False, 'comments': False,
                         'subjects': False, 'score': True}
            self._nx_setups = nx_setups

    def all_children (self) :
        _list = self.winfo_children()

        for item in _list :
            if item.winfo_children() :
                _list.extend(item.winfo_children())

        return _list

    def show_items(self, setups, res):
        self.items = []
        self.items_text = []
        for ii in range(len(res['list_paper'])):
            text = ""
            height = 0
            if(setups['ID']):
                text_id = res['list_paper'][ii].arxiv_id
                self.items.append(tk.Menubutton(self, text=text_id, relief=tk.RAISED))
                self.items[ii].grid()
                self.items[ii].menu = tk.Menu(self.items[ii], tearoff=0)
                self.items[ii]['menu'] = self.items[ii].menu
                self.items[ii].menu.add_command(label='get more', command=self.get_more)
                self.items[ii].menu.add_command(label='arXiv link', command=self.linkto_arx)
                self.items[ii].menu.add_command(label='ADS link', command=self.linkto_ads)
                self.items[ii].pack(side=tk.TOP)
            if(setups['title']):
                text += "Title: " + res['list_paper'][ii].title
                text += '\n'
                height += 2
            if(setups['abstract']):
                text += "Abstract: " + res['list_paper'][ii].abstract
                text += '\n'
                height += 15
            if(setups['authors']):
                text += "Authors: "
                for aa in res['list_paper'][ii].authors:
                    text += aa+"; "
                text += '\n'
                height += 2
            if(setups['score']):
                try:
                    res['score']
                    text += 'The relating score: '
                    text += res['score'][ii]
                except:
                    pass
                text += '\n'
                height += 1
            if(setups['comments']):
                text += res['list_paper'][ii].comments
                text += '\n'
            if(setups['subjects']):
                text += res['list_paper'][ii].subjects
                text += '\n'
            if(setups['date']):
                text += res['list_paper'][ii].date
                text += '\n'
            self.items_text.append(tk.Text(self, height = height,
                                           font=16,
                                           wrap=tk.WORD))
            self.items_text[ii].insert(tk.END, text)
            self.items_text[ii].pack(side=tk.TOP)
            self._cur_id += 1
        if (self.fin):
            self.fin_sign = tk.Button(self, text="Fin",
                                      command = self.fin_func)
            self.fin_sign.pack(side=tk.BOTTOM)

    def get_more(self):
        pass
    def linkto_arx(self):
        pass
    def linkto_ads(self):
        pass
    def fin_func(self):
        self.master.destroy()

old_stdout = sys.stdout
sys.stdout = mystdout = StringIO()
root = tk.Tk()
app = Application(master=root)
app.mainloop()

sys.stdout = old_stdout
