# -*- coding: utf-8 -*-

"""
Draw the Graphic User Interface (GUI) for the SMS checker application
Uses different thread to check for word containing profanity using http
request from http://www.wdylike.appspot.com/
"""

# %%
import tkinter as tk
import re as reg
import requests
import threading
import send_sms


# %%
class ThreadedClient(threading.Thread):
    def __init__(self, parent=None, text=None, word=None):
        super(ThreadedClient, self).__init__()
        self.parent = parent
        self.text_box = text
        self.word = word

    def run(self):
        payload = {'q': self.word}
        r = None
        try:
            r = requests.get('http://www.wdylike.appspot.com/',
                             params=payload)
        except Exception as e:
            print(e)
        if "true" in r.text:
            self.highlight_pattern(self.word)
            self.parent.prof["fg"] = "#FF3D00"
            self.parent.prof["text"] = "Profanity detected"
        elif "false" in r.text:
            pass
        else:
            pass

    def highlight_pattern(self, word):
        start = self.parent.text_area.index("1.0")
        end = self.parent.text_area.index("end")
        self.parent.text_area.mark_set("matchStart", start)
        self.parent.text_area.mark_set("matchEnd", start)
        self.parent.text_area.mark_set("searchLimit", end)
        self.parent.text_area.tag_configure('warning', foreground="#ff3d00",
                                            underline=1)
        count = tk.IntVar()
        while True:
            index = self.parent.text_area.search(word, "matchEnd",
                                                 "searchLimit", count=count)
            if index == "":
                break
            self.parent.text_area.mark_set("matchStart", index)
            self.parent.text_area.mark_set("matchEnd",
                                           "%s+%sc" % (index, count.get()))
            self.parent.text_area.tag_add('warning', index,
                                          "%s+%sc" % (index, count.get()))


# %%
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.createWidgets()

    def changed(self, value=None):
        flag = self.text_area.edit_modified()
        if flag:
            line = self.text_area.get('0.0', tk.END)
            lis = self.get_words(line)

            self.word_count["text"] = str(len(lis)) + " Words"
            self.char_count["text"] = str(len(line)-1) + " Characters"
            self.prof["fg"] = "#76FF03"
            self.prof["text"] = "No Profanity detected"

            for w in lis:
                self.thread = ThreadedClient(self, self.text_area, w)
                self.thread.start()
        self.text_area.edit_modified(False)

    def request(self, word):
        """ Sends and Checks for profanity """
        payload = {'q': word}
        r = requests.get('http://www.wdylike.appspot.com/', params=payload)
        if "true" in r.text:
            self.highlight_pattern(word)
        elif "false" in r.text:
            pass
        else:
            pass

    def highlight_pattern(self, word):
        start = self.text_area.index("1.0")
        end = self.text_area.index("end")
        self.text_area.mark_set("matchStart", start)
        self.text_area.mark_set("matchEnd", start)
        self.text_area.mark_set("searchLimit", end)
        self.text_area.tag_configure('warning', foreground="#ff3d00",
                                     underline=1)
        count = tk.IntVar()
        while True:
            index = self.text_area.search(word, "matchEnd", "searchLimit",
                                          count=count)
            if index == "":
                break
            self.text_area.mark_set("matchStart", index)
            self.text_area.mark_set("matchEnd",
                                    "%s+%sc" % (index, count.get()))
            self.text_area.tag_add('warning', index,
                                   "%s+%sc" % (index, count.get()))

    def get_words(self, text):
        return reg.compile('\w+').findall(text)

    def send(self):
        line = self.text_area.get('0.0', tk.END)
        st = self.prof["text"]
        if not line:
            self.status_text["text"] = "Empty message!"
        if st == "No Profanity detected":
            self.status_text["text"] = "Sending..."
            try:
                send_sms.send_msg(self.text_area.get('0.0', tk.END),
                                  self.phone.get())
                self.status_text["text"] = "Sent."
            except Exception as e:
                self.status_text["text"] = "Cannot send."
                print(e)
        elif st == "Profanity detected":
            self.status_text["text"] = "Cannot send. Contains Profanity!"

    def createWidgets(self):
        """ Top frame """
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        """ Message Frame """
        self.msg_frame = tk.Frame(self, padx=10)
        self.msg_frame.grid(row=0, column=0, sticky=tk.E+tk.W)
        self.msg_frame.columnconfigure(0, weight=1)
        self.msg_frame.columnconfigure(1, weight=1)
        self.msg_frame.columnconfigure(0, weight=1)

        """ Message Label """
        self.msg_label = tk.Label(self.msg_frame, padx=10, text="To: ")
        self.msg_label.grid(row=0, column=0, sticky=tk.E)

        """ Phone Entry """
        self.phone = tk.Entry(self.msg_frame)
        self.phone.insert(tk.END, '+918017207442')
        self.phone.grid(row=0, column=1, sticky=tk.W)

        """ Send Button """
        self.send_button = tk.Button(self.msg_frame, text="Send",
                                     command=self.send, padx=10, pady=2,
                                     bd=1, bg="#1DE9B6", fg="#000",
                                     relief=tk.RAISED)
        self.send_button.grid(row=0, column=2, sticky=tk.W)

        """ Text Editer Widget """
        self.text_area = tk.Text(self, padx=10, pady=10,
                                 selectbackground="#ff3d00")
        self.text_area.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.text_area.grid_rowconfigure(0, weight=1)

        self.text_area.focus_set()
        self.text_area.bind('<<Modified>>', self.changed)

        scrollb = tk.Scrollbar(self, command=self.text_area.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.text_area['yscrollcommand'] = scrollb.set

        """ Status Bar Frame """
        self.frame = tk.Frame(self)
        self.frame.grid(row=2, column=0, sticky=tk.E+tk.W)
        self.frame.columnconfigure(0, weight=4)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=2)

        """ Status Label Widget """
        self.status_text = tk.Label(self.frame, text=" ",
                                    bg="#eeeeee", bd=2, padx=0, pady=4)
        self.status_text.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        """ Status Word Count Widget """
        self.word_count = tk.Label(self.frame, text="3 Words", bg="#424242",
                                   fg="#ffffff", padx=0, pady=4)
        self.word_count.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

        """ Status Charecter Count Widget """
        self.char_count = tk.Label(self.frame, text="40 Characters",
                                   bg="#212121", fg="#ffffff",
                                   padx=0, pady=4)
        self.char_count.grid(row=0, column=2, sticky=tk.N+tk.S+tk.E+tk.W)

        """ Profanity Status """
        self.prof = tk.Label(self.frame, text="Profanity Detected",
                             bg="#37474F", fg="#ffffff", padx=0, pady=4)
        self.prof.grid(row=0, column=3, sticky=tk.N+tk.S+tk.E+tk.W)


# %%
root = tk.Tk()
root.geometry('800x500')
root["bg"] = "red"
app = Application(master=root)
app.master.title("SMS Checker")
app.mainloop()

# %%
