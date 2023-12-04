# ouzayb

import tkinter as tk

class ConsoleDisplay:
   def __init__(self, parent_frame):
      self.root = parent_frame
      self.text = "Console:\n"
      self.max_text_length = 100 
      
      self.text_frame = tk.Frame(parent_frame)
      self.text_frame.grid(row=0, column=0)
      
      self.text_area = tk.Text(self.text_frame, height=10, width=80)
      self.text_area.pack(side=tk.LEFT, fill=tk.Y)
      
      self.scrollbar = tk.Scrollbar(self.text_frame, command=self.text_area.yview)
      self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
      
      self.text_area.config(yscrollcommand=self.scrollbar.set)
      self.text_area.insert(tk.END, self.text)
      
   def write(self, text):
      """write text to the console"""
      self.text_area.insert(tk.END, text + "\n")
      self.text_area.see(tk.END)

def init_console_window(parentWindow):
   """initialize the console"""
   text_display = ConsoleDisplay(parentWindow)
   return text_display


def main():
   root = tk.Tk()
   root.title("Text Display Module")
   
   sample_text = "This is an example text to display."
   
   text_display = ConsoleDisplay(root, sample_text)
   
   root.mainloop()

if __name__ == "__main__":
   main()
