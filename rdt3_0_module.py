# ouzayb

from automat import MethodicalMachine
import time, threading

class rdt3_0(object):
   version = "rdt3_0"
   
   
   class Sender(object):
      machine = MethodicalMachine()
      
      def __init__(self):
         self.state = 0
         self.current_timer = None
         pass
      
      def recieve_ack(self, ack, command, callback_func):
         # print(f"{ack[0]}{ack[1]} has been recieved")
         #ack = (type, bit, corrupt)
         if(ack[0] == "Ack"):
            if(ack[2] == False):
               self.recieve_corrupt_ack(command, callback_func)
            elif(ack[1] == 0):
               self.recieve_ack0(command, callback_func)
            elif(ack[1] == 1):
               self.recieve_ack1(command, callback_func)
         
      
      @machine.state(initial=True)
      def wait_0_from_above(self):
         pass 
      
      @machine.state()
      def wait_1_from_above(self):
         pass 
      
      @machine.state()
      def wait_for_ack0(self):
         pass 
      
      @machine.state()
      def wait_for_ack1(self):
         pass 

      @machine.input()
      def instruction_from_above(self, command, callback_func):
         pass
      
      @machine.input()
      def recieve_ack0(self, command, callback_func):
         pass
      
      @machine.input()
      def recieve_ack1(self, command, callback_func):
         pass
      
      @machine.input()
      def recieve_corrupt_ack(self, command, callback_func):
         pass
      
      @machine.output()
      def send_pkc_0(self, command, callback_func):
         self.state = 1
         command.write("udp_send(data) from above")
         command.write("rdt_send(data)")
         command.write("sndpkt=make_pkt(0,data,checksum)")
         command.write("udt_send(sndpkt)")
         command.write("start_timer")
         if(self.current_timer != None):
            print("The current timer wasn't null when trying to create a new timer. Stopping the old timer.")
            self.current_timer.cancel()
            self.current_timer = None
         self.current_timer = threading.Timer(5, self.send_pkc_0_again, args=(command, callback_func))
         self.current_timer.start()
         # print(f"timer started {self.current_timer}")
         callback_func(self.state, True, 0)
         pass
      
      @machine.output()
      def send_pkc_1(self, command, callback_func):
         self.state = 3
         command.write("udp_send(data) from above")
         command.write("rdt_send(data)")
         command.write("sndpkt=make_pkt(0,data,checksum)")
         command.write("udt_send(sndpkt)")
         command.write("start_timer")
         if(self.current_timer != None):
            print("The current timer wasn't null when trying to create a new timer. Stopping the old timer.")
            self.current_timer.cancel()
            self.current_timer = None
         self.current_timer = threading.Timer(5, self.send_pkc_1_again, args=(command, callback_func))
         self.current_timer.start()
         # print(f"timer started {self.current_timer}")
         callback_func(self.state, True, 1)
         pass
      
      def send_pkc_0_again(self, command, callback_func):
         # self.current_timer.cancel()
         # self.current_timer = None
         
         # self.state = 1

         command.write("timeout")
         command.write("udt_send(sndpkt)")
         command.write("start_timer")

         if(self.state == 1):
            self.current_timer = threading.Timer(5, self.send_pkc_1_again, args=(command, callback_func))
            self.current_timer.start()
         # print(f"timer started {self.current_timer}")
         callback_func(self.state, True, 0, True)
         pass
      
      def send_pkc_1_again(self, command, callback_func):
         # self.current_timer.cancel()
         # self.current_timer = None
         
         # self.state = 3
         
         command.write("timeout")
         command.write("udt_send(sndpkt)")
         command.write("start_timer")
            
         if(self.state == 3):
            self.current_timer = threading.Timer(5, self.send_pkc_1_again, args=(command, callback_func))
            self.current_timer.start()
         # print(f"timer started {self.current_timer}")
         callback_func(self.state, True, 1, True )
         pass
      
      @machine.output()
      def reset_to_wait1(self, command, callback_func):
         self.state = 2
         command.write("rdt_rcv(rcvpkt) && notcorrupt(rcvpkt) && isACK(rcvpkt,0)")
         command.write("stop_timer")
         self.current_timer.cancel()
         self.current_timer = None
         # print(f"timer stopped {self.current_timer}")
         callback_func(self.state, False, 1)
         pass
      
      @machine.output()
      def reset_to_wait0(self, command, callback_func):
         self.state = 0
         command.write("rdt_rcv(rcvpkt) && notcorrupt(rcvpkt) && isACK(rcvpkt,1)")
         command.write("stop_timer")
         self.current_timer.cancel()
         self.current_timer = None
         # print(f"timer stopped {self.current_timer}")
         callback_func(self.state, False, 0)
         pass
      
      @machine.output()
      def do_nothing_0(self, command, callback_func):
         self.state = 0
         if(self.current_timer):
            print("current timer found")
            self.current_timer.cancel()
            self.current_timer = None
         command.write("rdt_rcv(rcvpkt)")
         command.write("-Do Nothing-")
         callback_func(self.state, False, 0)
         pass
      
      @machine.output()
      def do_nothing_1(self, command, callback_func):
         self.state = 2
         if(self.current_timer):
            print("current timer found")
            self.current_timer.cancel()
            self.current_timer = None
         command.write("rdt_rcv(rcvpkt)")
         command.write("-Do Nothing-")
         callback_func(self.state, False, 0)
         pass
      
      @machine.output()
      def reviece_wrong_ack0(self, command, callback_func):
         self.state = 1
         command.write("rdt_rcv(rcvpkt) && (corrupt(rcvpkt)|| isACK(rcvpkt,1))")
         command.write("-Do Nothing-")
         callback_func(self.state, False, 0)
         pass
      
      @machine.output()
      def reviece_wrong_ack1(self, command, callback_func):
         self.state = 3
         command.write("rdt_rcv(rcvpkt) && (corrupt(rcvpkt)|| isACK(rcvpkt,0))")
         command.write("-Do Nothing-")
         callback_func(self.state, False, 0)
         pass
      
      wait_0_from_above.upon(instruction_from_above , enter = wait_for_ack0     , outputs = [send_pkc_0]         )
      wait_0_from_above.upon(recieve_ack0           , enter = wait_0_from_above , outputs = [do_nothing_0]       )
      wait_0_from_above.upon(recieve_ack1           , enter = wait_0_from_above , outputs = [do_nothing_0]       )
      wait_0_from_above.upon(recieve_corrupt_ack    , enter = wait_0_from_above , outputs = [do_nothing_0]       )
      wait_1_from_above.upon(instruction_from_above , enter = wait_for_ack1     , outputs = [send_pkc_1]         )
      wait_1_from_above.upon(recieve_ack0           , enter = wait_1_from_above , outputs = [do_nothing_1]       )
      wait_1_from_above.upon(recieve_ack1           , enter = wait_1_from_above , outputs = [do_nothing_1]       )
      wait_1_from_above.upon(recieve_corrupt_ack    , enter = wait_1_from_above , outputs = [do_nothing_1]       )
      wait_for_ack0.upon    (recieve_ack0           , enter = wait_1_from_above , outputs = [reset_to_wait1]     )
      wait_for_ack0.upon    (recieve_ack1           , enter = wait_for_ack0     , outputs = [reviece_wrong_ack0] )
      wait_for_ack0.upon    (recieve_corrupt_ack    , enter = wait_for_ack0     , outputs = [reviece_wrong_ack0] )
      wait_for_ack1.upon    (recieve_ack0           , enter = wait_for_ack1     , outputs = [reviece_wrong_ack1] )
      wait_for_ack1.upon    (recieve_ack1           , enter = wait_0_from_above , outputs = [reset_to_wait0]     )
      wait_for_ack1.upon    (recieve_corrupt_ack    , enter = wait_for_ack1     , outputs = [reviece_wrong_ack1] )

      
      
      
   class Reciever(object):
      
      def __init__(self):
         self.state = 0
         self.ack = True
         pass

      machine = MethodicalMachine()

      def recieve_pcg(self, message, command, callback_func):
         # print(f"pkc{message[1]} has been recieved")
         #message[0] == True means it is uncorrupt. False means corrupt
         if message[0] == True:
            if(message[1] == 0):
               self.instruction_from_below_uncorrupt0(command, callback_func)
            elif(message[1] == 1):
               self.instruction_from_below_uncorrupt1(command, callback_func)
            else:
               print(f"Reciever recieved a bit that is not known. bit: {message[1]}")
         else:
            self.instruction_from_below_corrupt(command, callback_func)
            
            
      @machine.state(initial=True)
      def wait_0_from_below(self):
         pass

      @machine.state()
      def wait_1_from_below(self):
         pass

      @machine.input()
      def instruction_from_below_corrupt(self, command, callback_func):
         pass
      
      @machine.input()
      def instruction_from_below_uncorrupt0(self, command, callback_func):
         pass
      
      @machine.input()
      def instruction_from_below_uncorrupt1(self, command, callback_func):
         pass


      @machine.output()
      def send_ack0_first_time(self, command, callback_func):
         self.state = 1
         command.write("rdt_rcv(rcvpkt) && (notcorrupt(rcvpkt) || has_seq0(rcvpkt))")
         command.write("extract(rcvpkt,data)")
         command.write("deliver_data(data)")
         command.write("sndpkt=make_pkt(ACK,0,checksum)")
         command.write("udt_send(sndpkt)")
         callback_func(self.state, True, 0, "Ack")
         
      @machine.output()
      def send_ack1_first_time(self, command, callback_func):
         self.state = 0
         command.write("rdt_rcv(rcvpkt) && (notcorrupt(rcvpkt) || has_seq1(rcvpkt))")
         command.write("extract(rcvpkt,data)")
         command.write("deliver_data(data)")
         command.write("sndpkt=make_pkt(ACK,1,checksum)")
         command.write("udt_send(sndpkt)")
         callback_func(self.state, True, 1, "Ack")
         
      @machine.output()
      def send_ack1_again(self, command, callback_func):
         self.state = 0
         command.write("rdt_rcv(rcvpkt) && (corrupt(rcvpkt) || has_seq1(rcvpkt))")
         command.write("sndpkt=make_pkt(ACK,1,checksum)")
         command.write("udt_send(sndpkt)")
         callback_func(self.state, True, 1, "Ack")
         
      @machine.output()
      def send_ack0_again(self, command, callback_func):
         self.state = 1
         command.write("rdt_rcv(rcvpkt) && (corrupt(rcvpkt) || has_seq0(rcvpkt))")
         command.write("sndpkt=make_pkt(ACK,0,checksum)")
         command.write("udt_send(sndpkt)")
         callback_func(self.state, True, 0, "Ack")
      
         
      wait_0_from_below.upon(instruction_from_below_uncorrupt0, enter= wait_1_from_below, outputs = [send_ack0_first_time] )
      wait_0_from_below.upon(instruction_from_below_uncorrupt1, enter= wait_0_from_below, outputs = [send_ack1_again]      )
      wait_1_from_below.upon(instruction_from_below_uncorrupt1, enter= wait_0_from_below, outputs = [send_ack1_first_time] )
      wait_1_from_below.upon(instruction_from_below_uncorrupt0, enter= wait_1_from_below, outputs = [send_ack0_again]      )
      wait_1_from_below.upon(instruction_from_below_corrupt, enter= wait_1_from_below, outputs = [send_ack0_again]         )
      wait_0_from_below.upon(instruction_from_below_corrupt, enter= wait_0_from_below, outputs = [send_ack1_again]         )

   def __init__(self):
      self.reciever = rdt3_0.Reciever()
      self.sender = rdt3_0.Sender()
      
   def sender_send(self, command, callback_func):
      self.sender.instruction_from_above(command, callback_func)
      # callback_func(self.sender.state, self.sender.send, int(self.sender.state/2))
      
   def sender_recieve(self,ack, command, callback_func):
      self.sender.recieve_ack(ack, command, callback_func)

      # callback_func(self.sender.state, self.sender.send, int(self.sender.state/2))
      pass
   
      
   def reciever_recieve(self, message, command, callback_func):
      self.reciever.recieve_pcg(message, command, callback_func)
         
      # callback_func(self.reciever.state, True, int(self.reciever.state/2), "Ack" if self.reciever.ack else "Nack")
      
   def reciever_send(self, callback_func):
      pass
   
   def destroy(self):
      #if there are any timers, cancel as it can cause errors when the main thread is finished
      if(self.sender.current_timer):
         self.sender.current_timer.cancel()
