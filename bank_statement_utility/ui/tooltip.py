import tkinter as tk
from time import time

_bgcolor = '#d9d9d9'
_fgcolor = '#000000'


class ToolTip(tk.Toplevel):
    """ Provides a ToolTip widget for Tkinter. """

    def __init__(self, wdgt, msg=None, msgFunc=None, delay=0.5,
                 follow=True):
        self.wdgt = wdgt
        self.parent = self.wdgt.master
        tk.Toplevel.__init__(self, self.parent, bg='black', padx=1, pady=1)
        self.withdraw()
        self.overrideredirect(True)
        self.msgVar = tk.StringVar()
        if msg is None:
            self.msgVar.set('No message provided')
        else:
            self.msgVar.set(msg)
        self.msgFunc = msgFunc
        self.delay = delay
        self.follow = follow
        self.visible = 0
        self.lastMotion = 0
        self.msg = tk.Message(self, textvariable=self.msgVar, bg=_bgcolor,
                              fg=_fgcolor, font="TkDefaultFont",
                              aspect=1000)
        self.msg.grid()
        self.wdgt.bind('<Enter>', self.spawn, '+')
        self.wdgt.bind('<Leave>', self.hide, '+')
        self.wdgt.bind('<Motion>', self.move, '+')

    def spawn(self, event=None):
        self.visible = 1
        self.after(int(self.delay * 1000), self.show)

    def show(self):
        if self.visible == 1 and time() - self.lastMotion > self.delay:
            self.visible = 2
        if self.visible == 2:
            self.deiconify()

    def move(self, event):
        self.lastMotion = time()
        if self.follow is False:
            self.withdraw()
            self.visible = 1
        self.geometry('+%i+%i' % (event.x_root + 20, event.y_root - 10))
        try:
            self.msgVar.set(self.msgFunc())
        except:
            pass
        self.after(int(self.delay * 1000), self.show)

    def hide(self, event=None):
        self.visible = 0
        self.withdraw()

    def update(self, msg):
        self.msgVar.set(msg)

    def configure(self, **kwargs):
        backgroundset = False
        foregroundset = False
        # Get the current tooltip text just in case the user doesn't provide any.
        current_text = self.msgVar.get()
        # to clear the tooltip text, use the .update method
        if 'debug' in kwargs.keys():
            debug = kwargs.pop('debug', False)
            if debug:
                for key, value in kwargs.items():
                    print(f'key: {key} - value: {value}')
        if 'background' in kwargs.keys():
            background = kwargs.pop('background')
            backgroundset = True
        if 'bg' in kwargs.keys():
            background = kwargs.pop('bg')
            backgroundset = True
        if 'foreground' in kwargs.keys():
            foreground = kwargs.pop('foreground')
            foregroundset = True
        if 'fg' in kwargs.keys():
            foreground = kwargs.pop('fg')
            foregroundset = True

        fontd = kwargs.pop('font', None)
        if 'text' in kwargs.keys():
            text = kwargs.pop('text')
            if (text == '') or (text == "\n"):
                text = current_text
            else:
                self.msgVar.set(text)
        reliefd = kwargs.pop('relief', 'flat')
        justifyd = kwargs.pop('justify', tk.LEFT)
        padxd = kwargs.pop('padx', 1)
        padyd = kwargs.pop('pady', 1)
        borderwidthd = kwargs.pop('borderwidth', 2)
        wid = self.msg  # The message widget which is the actual tooltip
        if backgroundset:
            wid.config(bg=background)
        if foregroundset:
            wid.config(fg=foreground)
        wid.config(font=fontd)
        wid.config(borderwidth=borderwidthd)
        wid.config(relief=reliefd)
        wid.config(justify=justifyd)
        wid.config(padx=padxd)
        wid.config(pady=padyd)
#                   End of Class ToolTip
