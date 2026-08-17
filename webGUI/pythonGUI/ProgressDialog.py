import tkinter
from tkinter import ttk
from threading import Thread
from queue import Queue


class ProgressDialog:

    def __init__(self, message, title='', numberSteps=100):
        self.q = Queue(1)
        self.numberSteps = numberSteps
        self.th = Thread(target=self._run, args=(message, title, numberSteps, self.q))
        self.th.start()
    
    def __del__(self):
        if self.th.is_alive():
            self.Update(self.numberSteps+1)
            sleep(1)

    def _createDialog(self, message, title, numberSteps):
        self.main_window = tkinter.Tk()
        if title == "":
            title = message
        self.main_window.title(title)
        self.label = ttk.Label(text=message)
        self.label.place(x=30, y=20)
        self.numberSteps = numberSteps
        self.progressbar = ttk.Progressbar(maximum=numberSteps)
        self.progressbar.place(x=30, y=50, width=200)
        self.main_window.geometry("300x100")
        self.main_window.attributes("-topmost", True)
        self.lastStep = 0

    def _run(self, message, title, numberSteps, queue):
        self._createDialog(message, title, numberSteps)
        self.q = queue
        self.main_window.after(1000, self._checkQueue)
        self.main_window.after_cancel(self.main_window.quit)
        self.main_window.mainloop()

    def _checkQueue(self):
        if not self.q.empty():
            step, new_msg = self.q.get()
            self.progressbar.step(step-self.lastStep)
            self.lastStep = step
            if new_msg != "":
                self.label.config(text=new_msg)

        if self.lastStep >= self.numberSteps:
            self.main_window.quit()
        self.main_window.after(1000, self._checkQueue)
    
    def Update(self, step, new_msg = ""):
        if self.th.is_alive():
            try:
                self.q.put((step, new_msg), block=True, timeout=2)
            except:
                None

    def WasCancelled(self):
        return not self.th.is_alive()

    def Destroy(self):
        self.__del__()