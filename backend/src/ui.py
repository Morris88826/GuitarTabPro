import numpy as np
from tkinter import *
from PIL import Image, ImageTk

ROI = None
class MainView(Tk):
    def __init__(self, thumbnail, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.wm_title("Annotation")

        self.my_rect = None
        self.image = Image.open(thumbnail)
        self.height, self.width = np.array(self.image).shape[:2]

        self.canvas = Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()
        self.frame = Frame(self, width=self.width, height=40)
        self.frame.pack()
        self.submit = Button(self.frame, text="OK",
                             bg="white", command=self.select)
        self.submit.pack()
        self.img = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.img, anchor="nw")
        self.key_binding()

    def key_binding(self):
        self.canvas.bind("<Button-1>", self.event_handler)
        self.canvas.bind("<B1-Motion>", self.event_handler)
        self.canvas.bind("<ButtonRelease-1>", self.event_handler)

    def select(self):
        if self.my_rect is not None:
            global ROI
            ROI = np.array([[self.start_position[0], self.start_position[1]], [
                           self.end_position[0], self.end_position[1]]])
            self.destroy()

    def event_handler(self, event):
        if event.type == EventType.ButtonPress:
            self.start_position = [event.x, event.y]
            self.finish_click = False

        if event.type == EventType.Motion or event.type == EventType.ButtonRelease:
            self.end_position = [event.x, event.y]

            if self.my_rect is not None:
                self.canvas.delete(self.my_rect)
            self.my_rect = self.canvas.create_rectangle(
                self.start_position[0], self.start_position[1], self.end_position[0], self.end_position[1],  width=2, outline="red")
