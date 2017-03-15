import can
import sys
import time

def send_one(num_messages):
    
    bus = can.interface.Bus()
    for i in xrange(int(num_messages)): 
        try:
            data = [i] * 8
            msg = can.Message(data=data, arbitration_id=000, extended_id=False)
            bus.send(msg)
            print msg, "sent on", bus.channel_info
            time.sleep(1)
        except can.CanError:
            print "Message NOT sent"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        send_one(sys.argv[1])
    else:
        send_one(1)
