# Garry's Mod Content Assistant v0.3
# by Tomeczekqq

__author__ = "Tomeczekqq"
__version__ = "0.3"

from pySmartDL import SmartDL
from tkinter import ttk
import tkinter as tk
from time import sleep
import threading
import tools
import json
import sys

COLOR_BG = "#3C2ECC"
COLOR_FG = "#ecf0f1"


class MainWindow():
    '''
    Main Window.
    TODO: Add scrollboxes to panels
    '''

    def __init__(self, master):
        self.master = master
        self.choices = []
        self.create_layout()
        self.get_links()

    def create_layout(self):
        self.logo = tk.PhotoImage(file="resources/header.png")
        self.label_logo = tk.Label(image=self.logo, background="#3C2ECC")
        self.label_about = tk.Label(
            text="v0.3 by Tomeczekqq ",
            background=COLOR_BG,
            font=("Helvetica", 10),
            foreground=COLOR_FG
        )
        self.label_eta = tk.Label(
            text='Time',
            background=COLOR_BG,
            font=("Helvetica", 12),
            foreground=COLOR_FG
        )
        self.label_speed = tk.Label(
            text='Speed',
            background=COLOR_BG,
            font=("Helvetica", 12),
            foreground=COLOR_FG,
            justify=tk.RIGHT
        )
        self.label_status = tk.Label(
            text="Status",
            background=COLOR_BG,
            font=("Helvetica", 12),
            foreground=COLOR_FG
        )
        self.label_path = tk.Label(
            text="Content will be automatically downloaded and unzipped in /addons/",
            background=COLOR_BG,
            font=("Helvetica", 16),
            foreground=COLOR_FG
        )
        self.label_content = tk.Label(
            text="Content",
            background=COLOR_BG,
            font=("Helvetica", 15),
            foreground=COLOR_FG
        )
        self.label_maps = tk.Label(
            text="Maps",
            background=COLOR_BG,
            font=("Helvetica", 15),
            foreground=COLOR_FG
        )
        self.label_minfo = tk.Label(
            text="Portal 2 and Left4Dead 2 maps are incompatible with GarrysMod",
            background=COLOR_BG,
            font=("Helvetica", 10),
            foreground=COLOR_FG
        )
        self.label_info = tk.Label(
            text="GMCA is free, open source and non-profit. I dont own this content, I am using reuploaded content from cscheater.era.ee.",
            background=COLOR_BG,
            font=("Helvetica", 10),
            foreground=COLOR_FG
        )
        self.label_link = tk.Label(
            text="Read more",
            background=COLOR_BG,
            font=("Helvetica", 10, "bold"),
            foreground=COLOR_FG,
            cursor="hand2"
        )
        self.label_link.bind(
            "<Button-1>",
            tools.open_website
        )
        self.frame_con = tk.Frame(
            self.master,
            background=COLOR_BG
        )
        self.frame_map = tk.Frame(
            self.master,
            background=COLOR_BG
        )
        self.button_start = tk.Button(
            text="Download",
            cursor="hand2",
            command=self.init_download,
            bg=COLOR_BG,
            foreground=COLOR_FG,
            relief=tk.GROOVE,
            font=("Helvetica", 15, "bold")

        )
        self.button_action = tk.Button(
            text="Pause",
            bg=COLOR_BG,
            foreground=COLOR_FG,
            relief=tk.GROOVE,
            command=self.action,
            cursor='hand2'
        )
        self.progressbar = ttk.Progressbar()

        self.label_logo.place(x=18, y=25)
        self.label_about.place(x=658, y=68)
        self.label_content.place(x=150, y=100)
        self.label_maps.place(x=580, y=100)
        self.label_minfo.place(x=405, y=425)
        self.label_info.place(x=1, y=580)
        self.label_path.place(x=30, y=480, width=740, height=20)
        self.label_link.place(x=718, y=580)
        self.frame_con.place(height=320, width=360, x=40, y=135)
        self.frame_map.place(height=290, width=340, x=450, y=135)
        self.button_start.place(x=345, y=525)

    def disable_checkboxes(self):
        for checkbox in self.choices:
            checkbox.element['state'] = 'disabled'

    def action(self):
        '''
        Pausing and unpausing downloader, also exit if downloaded is successful
        '''
        if self.button_action["text"] == "Resume":
            downloader.unpause()
            self.button_action.place(x=375)
            self.button_action["text"] = "Pause"
        elif self.button_action['text'] == 'Exit':
            on_close()
        else:
            downloader.pause()
            self.button_action["text"] = "Resume"
            self.button_action.place(x=370)

    def init_download(self):
        '''
        Gets checkboxes state and adds it to query.
        Starts threading
        '''
        for choice in self.choices:
            if (choice.enabled.get()) and ((choice.tag in to_download) == False):
                to_download.append(choice)
            elif (choice.enabled.get() == False) and (choice.tag in to_download):
                to_download.remove(choice)
        self.thread = threading.Thread(target=self.queue)
        self.thread.daemon = True
        self.thread.start()

    def queue(self):
        '''
        -Setups ui disable checkboxes and place downloading widgets
        -Starts downloading from queue
        '''
        self.label_status['text'] = "Preparing queue"
        if to_download == []:
            self.label_path["text"] = "You need to select item to download"
            return False
        self.button_start.destroy()
        self.label_path.destroy()
        self.progressbar.place(x=30, y=525, width=740, height=10)
        self.label_eta.place(x=26, y=540)
        self.label_speed.place(x=690, y=540, width=100)
        self.label_status.place(x=30, y=500, width=740, height=20)
        self.label_status["text"] = "Preparing queue... | {0} items in queue)".format(
            len(to_download)
        )
        self.disable_checkboxes()
        for con in to_download:
            self.start_download(con)
            if is_close:
                break

        self.button_action["text"] = "Exit"

    def start_download(self, content):
        '''
        Starts downloading and update widgets (eta, speed and status)
        '''
        if "mediafire" in content.url:
            content.url = tools.scrap_mediafire(content.url)
        global downloader
        downloader = SmartDL(content.url, GMOD_DIR, progress_bar=False)
        try:
            downloader.start(blocking=False)
        except:
            self.label_status["text"] = "Cant reach {}".format(content.name)

        self.button_action.place(x=380, y=545)

        while not downloader.isFinished():
            if is_close:
                return False
            self.label_speed["text"] = downloader.get_speed(human=True)
            self.label_eta["text"] = downloader.get_eta(human=True)
            self.progressbar["value"] = downloader.get_progress()*100
            self.label_status["text"] = ("{} {} ({}/{}) | {} files in queue").format(
                downloader.get_status(),
                content.name,
                downloader.get_dl_size(human=True),
                tools.size_format(downloader.filesize),
                str(len(to_download))
            )
            sleep(0.2)

        if downloader.isSuccessful():
            self.label_status["text"] = "Downloading {} completed".format(
                content.name)
            self.label_status["text"] = "Unziping..."
            is_unzipped = tools.unzip(content.url, GMOD_DIR)
            if is_unzipped[0]:
                self.label_status["text"] = "Completed {}".format(content.name)
            else:
                self.label_status["text"] = "Unziping {} FAILED! You have to unzip it manualy.".format(
                    is_unzipped[1]
                )
            return True
        else:
            self.label_status["text"] = "Downloading {} FAILED!".format(
                content.name)
            return False

    def get_links(self):
        '''
        parse links.json
        and create checkboxes
        '''
        with open('links.json', 'r') as f:
            self.data = json.load(f)
        for item in self.data['contents']:
            element = self.Checkbox(
                item,
                self.data['contents'][item]['name'],
                self.data['contents'][item]['url'],
                self.frame_con
            )
            self.choices.append(element)
            element.create_layout()
        for item in self.data['maps']:
            element = self.Checkbox(
                item,
                self.data['maps'][item]['name'],
                self.data['maps'][item]['url'],
                self.frame_map
            )
            self.choices.append(element)
            element.create_layout()

    class Checkbox():

        def __init__(self, tag, name, url, target):
            self.tag = tag
            self.name = name
            self.url = url
            self.enabled = tk.BooleanVar()
            self.target = target

        def create_layout(self):
            self.element = tk.Checkbutton(
                master=self.target,
                text=self.name,
                background=COLOR_BG,
                font=("Helvetica", 12),
                foreground=COLOR_FG,
                selectcolor=COLOR_BG,
                activebackground=COLOR_BG,
                variable=self.enabled
            )
            self.element.pack(anchor=tk.W)


def on_close():
    is_close = True
    try:
        downloader.stop()
    except:
        pass
    root.destroy()


def center_window(w, h):
    width = w
    height = h
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - (width/2)
    y = (hs/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))


if __name__ == "__main__":
    is_close = False
    to_download = []
    GMOD_DIR = tools.find_steam()
    root = tk.Tk()
    root.title("Garry's Mod Content Assistant v0.3")
    root.configure(background=COLOR_BG)
    root.resizable(0, 0)
    root.iconbitmap('resources/icon.ico')
    root.protocol("WM_DELETE_WINDOW", on_close)
    center_window(800, 600)
    app = MainWindow(root)
    root.mainloop()
