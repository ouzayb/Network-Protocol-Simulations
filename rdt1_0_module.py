# ouzayb

from automat import MethodicalMachine

class rdt1_0(object):
   version = "rdt1_0"
   
   
   class Sender(object):
      machine = MethodicalMachine()
      
      def __init__(self):
         self.state = 0
         # self.send = 0
         pass
      
      @machine.state(initial=True)
      def wait_from_above(self):
         pass 

      @machine.input()
      def instruction_from_above(self, command, callback_func):
         pass

      @machine.output()
      def udp_sent(self, command, callback_func):
         self.state = 0
         command.write("udp_send(data) from above")
         command.write("rdt_send(data)")
         command.write("sndpkt=make_pkt(data,checksum)")
         command.write("udt_send(sndpkt)")
         callback_func(self.state, True, 0)
         pass
      
      wait_from_above.upon(instruction_from_above, enter= wait_from_above, outputs = [udp_sent])
      
   class Reciever(object):
      
      def __init__(self):
         self.state = 0
         pass

      machine = MethodicalMachine()

      @machine.state(initial=True)
      def wait_from_below(self):
         pass

      @machine.input()
      def instruction_from_below(self, command, callback_func):
         pass

      @machine.output()
      def wait_to_wait(self, command, callback_func):
         self.state = 0
         command.write("rdt_rcv(rcvpkt)")
         callback_func(self.state, False, 0, "Ack")
         
      wait_from_below.upon(instruction_from_below, enter= wait_from_below, outputs = [wait_to_wait])

   def __init__(self):
      self.reciever = rdt1_0.Reciever()
      self.sender = rdt1_0.Sender()
      
   def sender_send(self, message, callback_func):
      self.sender.instruction_from_above(message, callback_func)
      # callback_func(self.sender.state, True, self.sender.state%2)
      
   def reciever_recieve(self, message, command, callback_func):
      #message[0] == True means it is uncorrupt. False means corrupt
      self.reciever.instruction_from_below(command, callback_func)
      # callback_func(self.sender.state, False, self.sender.state%2, "Ack")
      
   def sender_recieve(self,ack, command, callback_func):
      pass
      
   def reciever_send(self, command, callback_func):
      pass
   
   def destroy(self):
      pass
