# ouzayb

import tkinter as tk
from move_box_module import init_move_box
from ImageViewer import init_image_viewer
from console import init_console_window
from up_left import up_left_anim
from rdt1_0_module import rdt1_0
from rdt2_0_module import rdt2_0
from rdt3_0_module import rdt3_0
from tcp_module import tcp
from time import sleep


#this is the progress loop of the simulation

def sender_rdt_send():
   global button
   button.config(state=tk.DISABLED) #disable the buttons until the current sim is completed
   newBox = upleft.CreateNewBox("inst", upleft.targets["user_sender"]) #create a new box for animation
   upleft.rdt_send((sender_udt_send,newBox), newBox) #play the animation and after the animation, call sender_udt_send with the given parameters
   # sender_udt_send()
   
def sender_udt_send(new_box):
   sleep(0.3)
   upleft.DestroyBox(new_box)
   #wait and destroy the box
   global rdt, command
   rdt.sender_send(command, sender_transferTunnel) # send the signal to state machine abd after call sender transfer tunnel
   
def sender_transferTunnel(state, send, bit, fake_wait = False, pck_name = "Pck"):
   global state_changer, command, box_mover, upleft, pkc_corrupt, button
   state_changer.change_image1(rdt.version, state) #change the state according to state machine output
   
   if(fake_wait): #if waiting is required (if this is a timeout)
      box_mover.last_y += 15 # add to the last_y value(last_y value is the y value the new box will be created on the lower left)
      box_mover.print_timeout() # prints timeout to show that there was a timeout
   
   if(send): #if the state machine output is send pkc
      new_box = upleft.CreateNewBox(f"{pck_name}{bit}", upleft.targets["sender"]) #create new box
      
      if loss_pkc.get(): #loss pck scenerio
         upleft.udt_send_lost(None, new_box, 0.9 if not late.get() else (0.3))
         box_mover.move_loss_to_reciever(None, f"                {pck_name}{bit}", 1 if not late.get() else (0.4))
      
      else: #no loss
         upleft.udt_send1(None,new_box, 0.9 if not late.get() else (0.3))
         box_mover.move_box_to_reciever((reciever_rdt_rcv,(not pkc_corrupt.get(), bit, pck_name, new_box)),
                                       f"                {pck_name}{bit}", 1 if not late.get() else (0.4))
         #after this function, call reciever rdt and pass the parameters of the package and the id of the box in the upleft animation
         #the id is passed in order to be able to control multiple packages in a late situation
         #the last parameter given to move_box_to_reviever is the speed multiplier and slows the package down to create a late ack scenerio
   
   else:# if no send, then the progress loop is broken as no new progress will be called. Enable the button
      button.config(state=tk.NORMAL)
   
def reciever_rdt_rcv(args):
   #the package is at the reciever
   #wait 3 second for animation purposes
   sleep(0.3)
   global upleft
   #the package is unpacked and sent to reciever user
   upleft.unpack((reciever_unpack,args[0:3]), args[3])
   
def reciever_unpack(args):
   #the package is at the reciever user
   global command, upleft
   #send the message properties to reciever state machine and send state machine outputs to reviever_answer func
   rdt.reciever_recieve(args, command, reciever_answer) 

def reciever_answer(state, send, bit, type): 
   #the package is at the reciever user
   global state_changer, box_mover
   state_changer.change_image2(rdt.version, state) #change the state according to output
   if(send): # if the output of the state machine requires an ack to be sent to the sender
      new_box = upleft.CreateNewBox(f"{type}{bit}", upleft.targets["user_reciever"])
      if loss_ack.get(): #loss package scenerio
         upleft.ack_udt_send_lost(None, new_box, 0.9)
         box_mover.move_loss_to_sender(None, f"                {type}{bit}", 1)
      else: # no loss
         upleft.ack_udt_send1(None,new_box, 0.9)
         box_mover.move_box_to_sender((unpack_ack,(type, bit, not ack_corrupt.get(), new_box)), f"                {type}{bit}", 1)
         #there is no speed difference on ack if the late is selected as a choice of design and not a requirement for the bugs to not to show that is easy to solve but cannot be solved under the time constraints. No, never.
   else:#if no send, then loop breaks, activate the button
      button.config(state=tk.NORMAL)
   
def unpack_ack(args):
   #the ack is at the sender.
   sleep(0.3)
   #the ack is unpacked and sent to the sender user.
   upleft.unpack_ack((answer_ack,args[0:3]), args[3])

def answer_ack(ack):
   #the package is at the sender user
   global rdt, command
   #send the ack to the state machine in order to process the ack and decide if another package is needed to be sent
   rdt.sender_recieve(ack, command, sender_transferTunnel)
   #if the sender decided to not send another package, it will not order to send and the loop will be broken, another progress could be started

def printer(version):
   """selection of version"""
   global rdt
   match version:
      case "rdt 1.0":
         rdt = rdt1_0()
      case "rdt 2.0":
         rdt = rdt2_0()
      case "rdt 3.0":
         rdt = rdt3_0()
      case "Tcp":
         rdt = tcp()
   root.destroy()

global root, rdt, box_mover, state_changer, button, upleft, command


#selection screen
root = tk.Tk()
root.geometry("500x500")
root.title("Protocol Selection")

selection_frame = tk.Frame(root, width=50, height=50, bg = "lightgray")
selection_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

lab = tk.Label(selection_frame, text = "Select one of the protocols to simulate")
lab.grid(row=0, column=0, padx=10, pady=10)

options = ["rdt 1.0", "rdt 2.0", "rdt 3.0", "Tcp"]

selected_var = tk.StringVar(selection_frame)
selected_var.set(options[0]) 

dropdown = tk.OptionMenu(selection_frame, selected_var, *options, command=printer)
dropdown.grid(row=1, column=0, padx=10, pady=10)

root.mainloop()



#simulation screen
root = tk.Tk()
root.title("Simulation From Oğuzhan Aybar")

#state window
upper_right_frame = tk.Frame(root, width=400, height=400, bg="lightgray")
upper_right_frame.grid(row=0, column=1, padx=10, pady=10)
state_changer = init_image_viewer(upper_right_frame, rdt.version)

#unreliable channel animation window
upper_left_frame = tk.Frame(root, width=400, height=400, bg="lightgray")
upper_left_frame.grid(row=0, column=0, padx=10, pady=10)
upleft = up_left_anim(upper_left_frame)

#console window
lower_right_frame = tk.Frame(root, width=400, height=400, bg="lightgray")
lower_right_frame.grid(row=1, column=1, padx=10, pady=10)
command = init_console_window(lower_right_frame)

#package exchange animation window
lower_left_frame = tk.Frame(root, width=400, height=400, bg="lightgray")
lower_left_frame.grid(row=1, column=0, padx=10, pady=10)
box_mover = init_move_box(lower_left_frame)

#control window
button_frame = tk.Frame(root, width=50, height=50, bg="lightgray")
button_frame.grid(row=0, column=2, padx=10, pady=10)

#scenerio checkboxes
pkc_corrupt = tk.BooleanVar()
ack_corrupt = tk.BooleanVar()
loss_ack = tk.BooleanVar()
loss_pkc = tk.BooleanVar()
late = tk.BooleanVar()

checkbox = tk.Checkbutton(button_frame, text="Pkc Corrupt", variable=pkc_corrupt)
checkbox.grid(row=0, column=0, padx=10, pady=10)
checkbox = tk.Checkbutton(button_frame, text="Ack Corrupt", variable=ack_corrupt)
checkbox.grid(row=0, column=1, padx=10, pady=10)
checkbox = tk.Checkbutton(button_frame, text="loss Ack", variable=loss_ack)
checkbox.grid(row=1, column=1, padx=10, pady=10)
checkbox = tk.Checkbutton(button_frame, text="loss Pck", variable=loss_pkc)
checkbox.grid(row=1, column=0, padx=10, pady=10)
checkbox = tk.Checkbutton(button_frame, text="late Ack", variable=late)
checkbox.grid(row=2, column=0, padx=10, pady=10)

#control button
button = tk.Button(button_frame, text="Send Instructions", command = sender_rdt_send)
button.grid(row=3, column=0, padx=10, pady=10)


#on closing
def on_closing():
   #first destroy rdt
   rdt.destroy()
   root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()