# ouzayb

# I know this looks horrible as all the movements are hard coded but 
# I had very limited time to implement this and decided to hardcode everything


import tkinter as tk
from PIL import Image, ImageTk

class LeftUp:
   def __init__(self, parent_frame):
      self.speed = 10
      self.box_girth = 50 
      self.box_height = 20 
      self.start_posx = 90
      self.start_posy = 30
      
      self.targets = {"user_sender":(90,30), "sender":(90, 170), "utc_left":(90, 410), "utc_right":(370, 410), "reciever":(370, 170), "user_reciever":(370, 30)}

      self.root = parent_frame
      self.canvas = tk.Canvas(parent_frame, width=500, height=500, bg="white")

      img = Image.open(f"leftup.png")
      img = img.resize((500, 500))
      self.image = ImageTk.PhotoImage(img)
      
      self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
      self.canvas.pack()
      

   def DestroyBox(self, box):
      self.canvas.delete(box[0])
      self.canvas.delete(box[1])
      
   def CreateNewBox(self, text, pos):
         box = self.canvas.create_rectangle(pos[0], pos[1], 
                                             pos[0] + self.box_girth, pos[1] + self.box_height, fill="blue")
         textOnBox = self.canvas.create_text(pos[0] + 20, pos[1] + 10, 
                                             text = text, fill="white")
         
         return (box, textOnBox)
   
   def rdt_send(self, call_after, BoxAndText = None, speed_mult = 1):
      target = self.targets["sender"]
      
      current_pos = self.canvas.coords(BoxAndText[0])
      
      if current_pos[1] < target[1]:
         self.canvas.move(BoxAndText[0], 0, self.speed * speed_mult)
         self.canvas.move(BoxAndText[1], 0, self.speed * speed_mult)
         self.root.after(10, lambda: self.rdt_send(call_after, BoxAndText, speed_mult))
      elif current_pos[1] != target[1]:
         self.canvas.move(BoxAndText[0],0, -current_pos[1] + target[1])
         self.canvas.move(BoxAndText[1],0, -current_pos[1] + target[1])
         self.root.after(10, lambda: self.rdt_send(call_after, BoxAndText, speed_mult))
      else:
         if(call_after):
            call_after[0](call_after[1])
            
   def udt_send1(self, call_after, BoxAndText = None, speed_mult = 1):
      target = self.targets["utc_left"]
      
      current_pos = self.canvas.coords(BoxAndText[0])
      
      if current_pos[1] < target[1]:
         self.canvas.move(BoxAndText[0], 0, self.speed * speed_mult)
         self.canvas.move(BoxAndText[1], 0, self.speed * speed_mult)
         self.root.after(10, lambda: self.udt_send1(call_after, BoxAndText, speed_mult))
      elif current_pos[1] != target[1]:
         self.canvas.move(BoxAndText[0],0, -current_pos[1] + target[1])
         self.canvas.move(BoxAndText[1],0, -current_pos[1] + target[1])
         self.root.after(10, lambda: self.udt_send1(call_after, BoxAndText, speed_mult))
      else:
         self.udt_send2(call_after, BoxAndText, speed_mult)
         
   def udt_send_lost(self, call_after, BoxAndText = None, speed_mult = 1):
      target = self.targets["utc_left"]
      
      current_pos = self.canvas.coords(BoxAndText[0])
      
      if current_pos[1] < target[1]:
         self.canvas.move(BoxAndText[0], 0, self.speed * speed_mult)
         self.canvas.move(BoxAndText[1], 0, self.speed * speed_mult)
         self.root.after(10, lambda: self.udt_send_lost(call_after, BoxAndText, speed_mult))
      elif current_pos[1] != target[1]:
         self.canvas.move(BoxAndText[0],0, -current_pos[1] + target[1])
         self.canvas.move(BoxAndText[1],0, -current_pos[1] + target[1])
         self.root.after(10, lambda: self.udt_send_lost(call_after, BoxAndText, speed_mult))
      else:
         self.DestroyBox(BoxAndText)
      
   def udt_send2(self, call_after, BoxAndText = None, speed_mult = 1):
      target = self.targets["utc_right"]
      
      current_pos = self.canvas.coords(BoxAndText[0])
      
      if current_pos[0] < target[0]:
         self.canvas.move(BoxAndText[0], self.speed * speed_mult, 0)
         self.canvas.move(BoxAndText[1], self.speed * speed_mult, 0)
         self.root.after(10, lambda: self.udt_send2(call_after, BoxAndText, speed_mult))
      elif current_pos[0] != target[0]:
         self.canvas.move(BoxAndText[0], target[0] - current_pos[0], 0)
         self.canvas.move(BoxAndText[1], target[0] - current_pos[0], 0)
         self.root.after(10, lambda: self.udt_send2(call_after, BoxAndText, speed_mult))
      else:
         self.udt_send3(call_after, BoxAndText, speed_mult)
      
   def udt_send3(self, call_after, BoxAndText = None, speed_mult = 1):
      target = self.targets["reciever"]
      
      current_pos = self.canvas.coords(BoxAndText[0])
      
      if current_pos[1] > target[1]:
         self.canvas.move(BoxAndText[0], 0, -self.speed * speed_mult)
         self.canvas.move(BoxAndText[1], 0, -self.speed * speed_mult)
         self.root.after(10, lambda: self.udt_send3(call_after, BoxAndText, speed_mult))
      elif current_pos[1] != target[1]:
         self.canvas.move(BoxAndText[0],0, -current_pos[1] + target[1])
         self.canvas.move(BoxAndText[1],0, -current_pos[1] + target[1])
         self.root.after(10, lambda: self.udt_send3(call_after, BoxAndText, speed_mult))
      else:
         if(call_after):
            call_after[0](call_after[1])
            
   def unpack(self, call_after, BoxAndText = None, speed_mult = 1):
      target = self.targets["user_reciever"]
      
      current_pos = self.canvas.coords(BoxAndText[0])
      
      if current_pos[1] > target[1]:
         self.canvas.move(BoxAndText[0], 0, -self.speed * speed_mult)
         self.canvas.move(BoxAndText[1], 0, -self.speed * speed_mult)
         self.root.after(10, lambda: self.unpack(call_after, BoxAndText, speed_mult))
      elif current_pos[1] != target[1]:
         self.canvas.move(BoxAndText[0],0, -current_pos[1] + target[1])
         self.canvas.move(BoxAndText[1],0, -current_pos[1] + target[1])
         self.root.after(10, lambda: self.unpack(call_after, BoxAndText, speed_mult))
      else:
         self.DestroyBox(BoxAndText)
         if(call_after):
            call_after[0](call_after[1])
      
      
   def ack_rdt_send(self, call_after, BoxAndText = None, speed_mult = 1):
      target = self.targets["reciever"]
      
      current_pos = self.canvas.coords(BoxAndText[0])
      
      if current_pos[1] < target[1]:
         self.canvas.move(BoxAndText[0], 0, self.speed * speed_mult)
         self.canvas.move(BoxAndText[1], 0, self.speed * speed_mult)
         self.root.after(10, lambda: self.ack_rdt_send(call_after, BoxAndText, speed_mult))
      elif current_pos[1] != target[1]:
         self.canvas.move(BoxAndText[0],0, -current_pos[1] + target[1])
         self.canvas.move(BoxAndText[1],0, -current_pos[1] + target[1])
         self.root.after(10, lambda: self.ack_rdt_send(call_after, BoxAndText, speed_mult))
      else:
         if(call_after):
            call_after[0](call_after[1])
      
   def ack_udt_send1(self, call_after, BoxAndText = None, speed_mult = 1):
      target = self.targets["utc_right"]
      
      current_pos = self.canvas.coords(BoxAndText[0])
      
      if current_pos[1] < target[1]:
         self.canvas.move(BoxAndText[0], 0, self.speed * speed_mult)
         self.canvas.move(BoxAndText[1], 0, self.speed * speed_mult)
         self.root.after(10, lambda: self.ack_udt_send1(call_after, BoxAndText, speed_mult))
      elif current_pos[1] != target[1]:
         self.canvas.move(BoxAndText[0],0, -current_pos[1] + target[1])
         self.canvas.move(BoxAndText[1],0, -current_pos[1] + target[1])
         self.root.after(10, lambda: self.ack_udt_send1(call_after, BoxAndText, speed_mult))
      else:
         self.ack_udt_send2(call_after, BoxAndText, speed_mult)
         
   def ack_udt_send_lost(self, call_after, BoxAndText = None, speed_mult = 1):
      target = self.targets["utc_right"]
      
      current_pos = self.canvas.coords(BoxAndText[0])
      
      if current_pos[1] < target[1]:
         self.canvas.move(BoxAndText[0], 0, self.speed * speed_mult)
         self.canvas.move(BoxAndText[1], 0, self.speed * speed_mult)
         self.root.after(10, lambda: self.ack_udt_send_lost(call_after, BoxAndText, speed_mult))
      elif current_pos[1] != target[1]:
         self.canvas.move(BoxAndText[0],0, -current_pos[1] + target[1])
         self.canvas.move(BoxAndText[1],0, -current_pos[1] + target[1])
         self.root.after(10, lambda: self.ack_udt_send_lost(call_after, BoxAndText, speed_mult))
      else:
         self.DestroyBox(BoxAndText)
      
      
   def ack_udt_send2(self, call_after, BoxAndText = None, speed_mult = 1):
      target = self.targets["utc_left"]
      
      current_pos = self.canvas.coords(BoxAndText[0])
      
      if current_pos[0] > target[0]:
         self.canvas.move(BoxAndText[0], -self.speed * speed_mult, 0)
         self.canvas.move(BoxAndText[1], -self.speed * speed_mult, 0)
         self.root.after(10, lambda: self.ack_udt_send2(call_after, BoxAndText, speed_mult))
      elif current_pos[0] != target[0]:
         self.canvas.move(BoxAndText[0], target[0] - current_pos[0], 0)
         self.canvas.move(BoxAndText[1], target[0] - current_pos[0], 0)
         self.root.after(10, lambda: self.ack_udt_send2(call_after, BoxAndText, speed_mult))
      else:
         self.ack_udt_send3(call_after, BoxAndText, speed_mult)
      
   def ack_udt_send3(self, call_after, BoxAndText = None, speed_mult = 1):
      target = self.targets["sender"]
      
      current_pos = self.canvas.coords(BoxAndText[0])
      
      if current_pos[1] > target[1]:
         self.canvas.move(BoxAndText[0], 0, -self.speed * speed_mult)
         self.canvas.move(BoxAndText[1], 0, -self.speed * speed_mult)
         self.root.after(10, lambda: self.ack_udt_send3(call_after, BoxAndText, speed_mult))
      elif current_pos[1] != target[1]:
         self.canvas.move(BoxAndText[0],0, -current_pos[1] + target[1])
         self.canvas.move(BoxAndText[1],0, -current_pos[1] + target[1])
         self.root.after(10, lambda: self.ack_udt_send3(call_after, BoxAndText, speed_mult))
      else:
         if(call_after):
            call_after[0](call_after[1])
      

   def unpack_ack(self, call_after, BoxAndText = None, speed_mult = 1):
      target = self.targets["user_sender"]
      # // burda bi problem var 
      if(BoxAndText == None):
         BoxAndText = self.boxAndText
      
      current_pos = self.canvas.coords(BoxAndText[0])
      
      if current_pos[1] > target[1]:
         self.canvas.move(BoxAndText[0], 0, -self.speed * speed_mult)
         self.canvas.move(BoxAndText[1], 0, -self.speed * speed_mult)
         self.root.after(10, lambda: self.unpack_ack(call_after, BoxAndText, speed_mult))
      elif current_pos[1] != target[1]:
         self.canvas.move(BoxAndText[0],0, -current_pos[1] + target[1])
         self.canvas.move(BoxAndText[1],0, -current_pos[1] + target[1])
         self.root.after(10, lambda: self.unpack_ack(call_after, BoxAndText, speed_mult))
      else:
         self.DestroyBox(BoxAndText)
         if(call_after):
            call_after[0](call_after[1])


def up_left_anim(parent_frame):
   image_box_movement = LeftUp(parent_frame)
   return image_box_movement

if __name__ == "__main__":
   root = tk.Tk()
   
   upper_right_frame = tk.Frame(root, width=400, height=400, bg="lightgray")
   lower_left_frame = tk.Frame(root, width=400, height=400, bg="lightgray")
   
   upper_right_frame.grid(row=0, column=0, padx=10, pady=10)
   lower_left_frame.grid(row=1, column=0, padx=10, pady=10)
   
   root.title("Image with Moving Box")
   a = up_left_anim(upper_right_frame)
   
   button = tk.Button(lower_left_frame, text="Rdt", command = a.rdt_send)
   button.pack()
   button = tk.Button(lower_left_frame, text="Udt", command = a.udt_send1)
   button.pack()
   button = tk.Button(lower_left_frame, text="unpack", command = a.unpack)
   button.pack()
   button = tk.Button(lower_left_frame, text="ack rdt", command = a.ack_rdt_send)
   button.pack()
   button = tk.Button(lower_left_frame, text="ack udt", command = a.ack_udt_send1)
   button.pack()
   button = tk.Button(lower_left_frame, text="ack deliver", command = a.unpack_ack)
   button.pack()
   root.mainloop()
