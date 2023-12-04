# ouzayb

import tkinter as tk

class BoxMovement:
   def __init__(self, parent_frame):
      self.x_speed = 10/3
      self.y_speed = 1/4
      self.box_girth = 50
      self.box_height = 20 
      self.last_y = 50
      self.root = parent_frame
      self.canvas = tk.Canvas(parent_frame, width=500, height=350, bg="white")
      self.canvas.pack()

      self.sender_line_x = 50
      self.receiver_line_x = 450
      self.canvas.create_line(self.sender_line_x, 50, self.sender_line_x, 280, fill="green", width=2, tags="sender")
      self.canvas.create_text(self.sender_line_x + 10, 310, text="Sender", fill="green")

      self.canvas.create_line(self.receiver_line_x, 50, self.receiver_line_x, 280, fill="red", width=2, tags="receiver")
      self.canvas.create_text(self.receiver_line_x - 10, 310, text="Receiver", fill="red")


   def move_loss_to_reciever(self, call_after, text, speed_mult = 1):
      self.animation_playing = True
      self.create_and_lose_box(self.sender_line_x, self.last_y, text, "sender", call_after, speed_mult)

   def move_loss_to_sender(self, call_after, text, speed_mult = 1):
      self.animation_playing = True
      self.create_and_lose_box(self.receiver_line_x, self.last_y, text, "receiver", call_after, speed_mult)

   def draw_cross(self, canvas,centerX, centerY, size):
      canvas.create_line(centerX-size, centerY-size, centerX+size, centerY+size, width=2, fill = "red") 
      canvas.create_line(centerX-size, centerY+size, centerX+size, centerY-size, width=2, fill = "red") 
   
   def create_and_lose_box(self, start_x, start_y, text, tag, call_after, speed_mult):
      start_x_real = start_x - (self.box_girth if tag == "receiver" else 0)
      box = self.canvas.create_rectangle(start_x_real, start_y, start_x_real + self.box_girth,
                                          start_y + self.box_height, fill="blue")
      
      text = self.canvas.create_text(start_x_real, start_y + 10, text=text, fill="white")
      
      self.draw_arrow_sad(start_x, start_y, tag, speed_mult)
      self.lose_box(text, tag, None, False, speed_mult)
      self.lose_box(box, tag, call_after, True, speed_mult)
      
   def lose_box(self, box_id, tag, call_after, put_cross, speed_mult):
      current_pos = self.canvas.coords(box_id)
      if tag == "sender":
         end_x = (self.sender_line_x + self.receiver_line_x)/2
         sign = 1
      else:
         end_x = (self.receiver_line_x + self.sender_line_x)/2
         sign = -1

      if abs(current_pos[0] - end_x) > self.x_speed * speed_mult:
         # sign = (end_x - current_pos[0]) / abs(end_x - current_pos[0])
         self.canvas.move(box_id, sign * self.x_speed * speed_mult, self.y_speed)
         self.root.after(10, lambda: self.lose_box(box_id, tag, call_after, put_cross, speed_mult))
      elif current_pos[0] != end_x:
         self.canvas.move(box_id, -current_pos[0] + end_x, self.y_speed * abs(end_x-current_pos[0])/(self.x_speed * speed_mult))
         self.root.after(10, lambda: self.lose_box(box_id, tag, call_after, put_cross, speed_mult))
      else:
         self.last_y = current_pos[1] + 20
         # self.canvas.delete(box_id)
         
         if(put_cross):
            self.draw_cross(self.canvas, current_pos[0], current_pos[1], 10)
            
         if(call_after):
            call_after[0](call_after[1])
   
   def move_box_to_reciever(self, call_after, text, speed_mult = 1):
      self.animation_playing = True
      self.create_and_move_box(self.sender_line_x, self.last_y, text, "sender", call_after, speed_mult)

   def move_box_to_sender(self, call_after, text, speed_mult = 1):
      self.animation_playing = True
      self.create_and_move_box(self.receiver_line_x, self.last_y, text, "receiver", call_after, speed_mult)
      
   def create_and_move_box(self, start_x, start_y, text, tag, call_after, speed_mult):
      start_x_real = start_x - (self.box_girth if tag == "receiver" else 0)
      box = self.canvas.create_rectangle(start_x_real, start_y, start_x_real + self.box_girth,
                                          start_y + self.box_height, fill="blue")
      
      text = self.canvas.create_text(start_x_real, start_y + 10, text=text, fill="white")
      
      self.draw_arrow(start_x, start_y, tag, speed_mult)
      self.move_box(text, tag, None, speed_mult)
      self.move_box(box, tag, call_after, speed_mult)

   def move_box(self, box_id, tag, call_after, speed_mult):
      current_pos = self.canvas.coords(box_id)
      if tag == "sender":
         end_x = self.receiver_line_x - self.box_girth
         sign = 1
      else:
         end_x = self.sender_line_x
         sign = -1

      if abs(current_pos[0] - end_x) > self.x_speed * speed_mult:
         # sign = (end_x - current_pos[0]) / abs(end_x - current_pos[0])
         self.canvas.move(box_id, sign * self.x_speed * speed_mult, self.y_speed)
         self.root.after(10, lambda: self.move_box(box_id, tag, call_after , speed_mult))
      elif current_pos[0] != end_x:
         self.canvas.move(box_id, -current_pos[0] + end_x, self.y_speed * abs(end_x-current_pos[0])/(self.x_speed * speed_mult))
         self.root.after(10, lambda: self.move_box(box_id, tag, call_after, speed_mult))
      else:
         self.last_y = current_pos[1]
         # self.canvas.delete(box_id)
         if(call_after):
            call_after[0](call_after[1])

   def draw_arrow_sad(self, start_x, start_y, tag, speed_mult = 1):
      if tag == "sender":
         end_x = (self.receiver_line_x + start_x)/2
         arrow_color = "green"
      else:
         end_x = (self.sender_line_x + start_x)/2
         arrow_color = "red"

      end_y = start_y + self.y_speed * ((abs(end_x - start_x) - self.box_girth) // self.x_speed * speed_mult)

      self.canvas.create_line(start_x, start_y, end_x, end_y, arrow=tk.LAST, arrowshape=(10, 15, 5), width=2,
                              fill=arrow_color, tags=tag)
      
   def draw_arrow(self, start_x, start_y, tag, speed_mult):
      if tag == "sender":
         end_x = self.receiver_line_x
         arrow_color = "green"
      else:
         end_x = self.sender_line_x
         arrow_color = "red"

      end_y = start_y + self.y_speed * ((abs(end_x - start_x) - self.box_girth) // (self.x_speed * speed_mult))

      self.canvas.create_line(start_x, start_y, end_x, end_y, arrow=tk.LAST, arrowshape=(10, 15, 5), width=2,
                              fill=arrow_color, tags=tag)

   def print_timeout(self):
      self.canvas.create_text(self.sender_line_x - 25, self.last_y, text="timeout", fill="black")
      

def init_move_box(parent_frame):
   box_movement = BoxMovement(parent_frame)
   return box_movement
