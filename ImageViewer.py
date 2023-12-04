# ouzayb

import tkinter as tk
from PIL import Image, ImageTk

class ImageViewer:
   def __init__(self, parent_frame, rdt_version):
      self.parent_frame = parent_frame
      self.curr_image1 = None
      self.curr_image2 = None
      
      self.image_init(rdt_version)
      
      self.image_label1 = tk.Label(parent_frame, image=self.curr_image1)
      self.image_label1.grid(row=0, column=0, padx=5, pady=5)

      self.image_label2 = tk.Label(parent_frame, image=self.curr_image2)
      self.image_label2.grid(row=1, column=0, padx=5, pady=5)
   
   def image_init(self, rdt_version):
      """initialize both images"""
      img = Image.open(f"{rdt_version}/sender/s0.png")
      img = img.resize((450, 200))
      self.curr_image1 = ImageTk.PhotoImage(img)
      
      img = Image.open(f"{rdt_version}/reciever/s0.png")
      img = img.resize((450, 200))
      self.curr_image2 = ImageTk.PhotoImage(img)
   
   def change_image1(self, rdt_version, index):
      """change image 1 to the selected index in the corresponding rdt version"""
      img = Image.open(f"{rdt_version}/sender/s{index}.png")
      img = img.resize((450, 200))
      self.curr_image1 = ImageTk.PhotoImage(img)
      
      self.image_label1.config(image = self.curr_image1)
   
   def change_image2(self, rdt_version, index):
      """change image 2 to the selected index in the corresponding rdt version""" 
      img = Image.open(f"{rdt_version}/reciever/s{index}.png")
      img = img.resize((450, 200))
      self.curr_image2 = ImageTk.PhotoImage(img)
      
      self.image_label2.config(image = self.curr_image2)

def init_image_viewer(parent_frame, rdt_version):
   """initialize and return an image viwer"""
   image_viewer = ImageViewer(parent_frame, rdt_version)
   return image_viewer
