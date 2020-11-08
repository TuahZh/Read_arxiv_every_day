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
import webbrowser


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self._widget_collection = {0:[]}
        self._frame_titles = {0:''}
        self.create_widgets()

    def create_widgets(self):
        _title = "Today"
        self.winfo_toplevel().title(_title)
        self.today = tk.Button(self)
        self.today["text"] = "Today"
        self.today["command"] = self.search_today
        self.today.pack(side=tk.TOP)

        self.text = tk.Text(self)
        _text = """Seize the day, then let it go.
                                           -- Marty Rubin"""
        self.text.tag_config('center', justify='center')
        self.text.insert(tk.END, _text)
        self.text.tag_add('center','1.0',tk.END)
        self.text.pack(side=tk.TOP)
        self.text['state'] = tk.DISABLED

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side=tk.BOTTOM)
        self._widget_collection[1] = [(self.today, tk.TOP),
                                      (self.text, tk.TOP),
                                      (self.quit, tk.BOTTOM)]
        self._frame_titles[1] = _title

    def search_today(self):
        _title = "Summary"
        self.winfo_toplevel().title(_title)
        widget_list = self.all_children()
        for item in widget_list:
            item.pack_forget()
        self.fin = False
        pl, ts = arxiv_reading()
        lp_c = ListPapers(pl)
        self.summary = tk.Text(self)
        self.summary.insert(tk.END, mystdout.getvalue())
        self.summary.pack(sid=tk.TOP)
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
        self.summary.insert(tk.END, lp_d.summary(called_tk=True))
        self._lp = lp_d
        self._cur_id = 0
        self.seguir_button = tk.Button(self, text="Continue", fg="red",
                                command=self.seguir)
        self.seguir_button.pack(side=tk.RIGHT)
        self.quit.pack(side=tk.LEFT)
        self._widget_collection[2] = [(self.summary, tk.TOP),
                                      (self.seguir_button, tk.RIGHT),
                                      (self.quit, tk.LEFT)]
        self._frame_titles[2] = _title

    def seguir(self):
        _title = "Head"
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
        self.summary.pack_forget()
        self.show_items(self._hd_setups, res)
        self.seguir_button.pack_forget()
        self.next_button = tk.Button(self)
        self.next_button["text"] = "Next"
        self.next_button["command"] = self.next
        self.next_button.pack(side=tk.RIGHT)
        self.quit.pack_forget()
        self.quit.pack(side=tk.LEFT)
        _title += " %d papers" % sigp_n
        self.winfo_toplevel().title(_title)
        try:
            self._widget_collection[3] = [(self.items, tk.TOP),
                                          (self.items_text, tk.TOP),
                                          (self.fin_sign, tk.BOTTOM),
                                          (self.next_button, tk.RIGHT),
                                          (self.quit, tk.LEFT)]
        except AttributeError:
            self._widget_collection[3] = [(self.items, tk.TOP),
                                          (self.items_text, tk.TOP),
                                          (self.next_button, tk.RIGHT),
                                          (self.quit, tk.LEFT)]
        self._frame_titles[3] = _title

    def show_message(self, mes, title="Message" ):
        messagebox.showinfo(title, mes)

    def next(self):
        _title = ""
        self.winfo_toplevel().title(_title)
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
        self.next_button.pack(side=tk.RIGHT)
        self.quit.pack(side=tk.LEFT)
        try:
            self._widget_collection[3] = [(self.items, tk.TOP),
                                          (self.items_text, tk.TOP),
                                          (self.fin_sign, tk.BOTTOM),
                                          (self.next_button, tk.RIGHT),
                                          (self.quit, tk.LEFT)]
        except AttributeError:
            self._widget_collection[3] = [(self.items, tk.TOP),
                                          (self.items_text, tk.TOP),
                                          (self.next_button, tk.RIGHT),
                                          (self.quit, tk.LEFT)]
        self._frame_titles[3] = _title

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
                self.items[ii].menu.add_command(label='Read abstract',
                                                command=lambda: self.read_abstract(res['list_paper'][ii]))
                self.items[ii].menu.add_command(label='Open arXiv',
                                                command=lambda: self.linkto_arx(res['list_paper'][ii]))
                self.items[ii].menu.add_command(label='Open ADS',
                                                command=lambda: self.linkto_ads(res['list_paper'][ii]))
                self.items[ii].pack(side=tk.TOP)
            if(setups['title']):
                text += "TITLE: " + res['list_paper'][ii].title
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
                                           font=14,
                                           wrap=tk.WORD))
            self.items_text[ii].insert(tk.END, text)
            self.items_text[ii].pack(side=tk.TOP)
            self.items_text[ii].tag_add("title", "1.0", "1.150")
            self.items_text[ii].tag_config("title", font=("Georgia", "16", "bold"),
                                           foreground = "blue")
            self.items_text[ii]['state'] = tk.DISABLED
            self._cur_id += 1
        if (self.fin):
            self.fin_sign = tk.Button(self, text="Fin",
                                      command = self.fin_func)
            self.fin_sign.pack(side=tk.BOTTOM)

    def read_abstract(self, p):
        # store the previous apearance
        widget_list = self.all_children()
        for item in widget_list:
            item.pack_forget()
        read_abstract = tk.Text(self, font=16, wrap=tk.WORD)
        read_abstract.insert(tk.END, "Abstract: "+p.abstract)
        read_abstract.insert(tk.END, "Title: "+p.title)
        read_abstract.pack(side=tk.TOP)
        back_button = tk.Button(self, text='Back',
                                command=lambda: self.restore(3))
        back_button.pack(side=tk.BOTTOM)
       # self.show_message(p.abstract, title="Abstract")

    def restore(self, frame_id):
        wl_tmp = self.all_children()
        for item in wl_tmp:
            item.pack_forget()
        if (frame_id==3):
            _items = self._widget_collection[frame_id][0][0]
            _side = self._widget_collection[frame_id][0][1]
            _items_text = self._widget_collection[frame_id][1][0]
            _side_text = self._widget_collection[frame_id][1][1]
            for ii, tt in zip(_items, _items_text):
                ii.pack(side=_side)
                tt.pack(side=_side_text)
            for item in self._widget_collection[frame_id][2:]:
                item[0].pack(side=item[1])
        else:
            for item in self._widget_collection[frame_id]:
                item[0].pack(side=item[1])

    def linkto_arx(self, p):
        try:
            _link = p.link
            if (_link != ''):
                webbrowser.open(_link, new=2)
                return
        finally:
            p.search_online()
            _link = p.link
            if (_link != ''):
                webbrowser.open(_link, new=2)
                return
            else:
                self.show_message("Sorry, I didn't find the arXiv link for this paper.")
                return

    def linkto_ads(self, p):
        try:
            _link = p.link_ads
            if (_link != ''):
                webbrowser.open(_link, new=2)
                return
        finally:
            p.search_online()
            _link = p.link_ads
            if (_link != ''):
                webbrowser.open(_link, new=2)
                return
            else:
                self.show_message("Sorry, I didn't find ADS link for this paper.")
                return
    def fin_func(self):
        self.master.destroy()

old_stdout = sys.stdout
sys.stdout = mystdout = StringIO()
root = tk.Tk()
app = Application(master=root)
app.mainloop()

sys.stdout = old_stdout
