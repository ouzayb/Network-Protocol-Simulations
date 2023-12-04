# ouzayb

from automat import MethodicalMachine

class rdt2_0(object):
   version = "rdt2_0"
   
   
   class Sender(object):
      machine = MethodicalMachine()
      
      def __init__(self):
         self.state = 0
         pass
      
      @machine.state(initial=True)
      def wait_from_above(self):
         pass 
      
      @machine.state()
      def wait_for_ack_or_nack(self):
         pass 

      @machine.input()
      def instruction_from_above(self, command, callback_func):
         pass
      
      @machine.input()
      def ack(self, command, callback_func):
         pass
      
      @machine.input()
      def nack(self, command, callback_func):
         pass

      @machine.output()
      def udp_sent(self, command, callback_func):
         self.state = 1
         command.write("udp_send(data) from above")
         command.write("rdt_send(data)")
         command.write("sndpkt=make_pkt(data,checksum)")
         command.write("udt_send(sndpkt)")
         callback_func(self.state, True, 0)
         pass
      
      @machine.output()
      def udp_sent_again(self, command, callback_func):
         self.state = 1
         command.write("rdt_rcv(rcvpkt) && isNAK(rcvpkt)")
         command.write("udt_send(sndpkt)")
         callback_func(self.state, True, 0)
         pass
      
      @machine.output()
      def reset_to_wait(self, command, callback_func):
         self.state = 0
         command.write("rdt_rcv(rcvpkt) && isACK(rcvpkt)")
         callback_func(self.state, False, 0)
         pass
      
      wait_from_above.upon(instruction_from_above, enter= wait_for_ack_or_nack, outputs = [udp_sent])
      wait_for_ack_or_nack.upon(ack, enter = wait_from_above, outputs = [reset_to_wait])
      wait_for_ack_or_nack.upon(nack, enter = wait_for_ack_or_nack, outputs = [udp_sent_again])
      
   class Reciever(object):
      
      def __init__(self):
         self.state = 0
         self.ack = True
         pass

      machine = MethodicalMachine()

      @machine.state(initial=True)
      def wait_from_below(self):
         pass

      @machine.input()
      def instruction_from_below_corrupt(self, command, callback_func):
         pass
      
      @machine.input()
      def instruction_from_below_uncorrupt(self, command, callback_func):
         pass


      @machine.output()
      def send_ack(self, command, callback_func):
         self.state = 0
         command.write("rdt_rcv(rcvpkt) && notcorrupt(rcvpkt)")
         command.write("extract(rcvpkt,data)")
         command.write("deliver_data(data)")
         command.write("sndpkt=make_pkt(ACK)")
         command.write("udt_send(sndpkt)")
         callback_func(self.state, True, 0, "Ack")
         
      @machine.output()
      def send_nack(self, command, callback_func):
         self.state = 0
         command.write("rdt_rcv(rcvpkt) && corrupt(rcvpkt)")
         command.write("sndpkt=make_pkt(NAK)")
         command.write("udt_send(sndpkt)")
         callback_func(self.state, True, 0, "Nack")
         
      wait_from_below.upon(instruction_from_below_uncorrupt, enter= wait_from_below, outputs = [send_ack])
      wait_from_below.upon(instruction_from_below_corrupt, enter= wait_from_below, outputs = [send_nack])

   def __init__(self):
      self.reciever = rdt2_0.Reciever()
      self.sender = rdt2_0.Sender()
      
   def sender_send(self, command, callback_func):
      self.sender.instruction_from_above(command, callback_func)
      # callback_func(self.sender.state, self.sender.send, int(self.sender.state/2))
      
   def sender_recieve(self,ack, command, callback_func):
      
      if ack[0] == "Nack":
         self.sender.nack(command, callback_func)
      else:
         self.sender.ack(command, callback_func)
         
      # callback_func(self.sender.state, self.sender.send, int(self.sender.state/2))
      pass
   
      
   def reciever_recieve(self, message, command, callback_func):
      #message[0] == True means it is uncorrupt. False means corrupt
      if message[0] == True:
         self.reciever.instruction_from_below_uncorrupt(command, callback_func)
      else:
         self.reciever.instruction_from_below_corrupt(command, callback_func)
         
      # callback_func(self.reciever.state, True, int(self.reciever.state/2), "Ack" if self.reciever.ack else "Nack")
      
   def reciever_send(self, callback_func):
      pass
   
   def destroy(self):
      pass
