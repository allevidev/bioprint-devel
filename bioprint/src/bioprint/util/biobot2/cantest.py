import can
import sys

def send_one(num_messages):
    
    bus = can.interface.Bus(channel="can0", bustype="socketcan")
    msg = can.Message(data=[0,0,0,0,0,0,0,0], arbitration_id=001)
    try:
        for i in xrange(int(num_messages)):
            bus.send(msg)
            print msg, "sent on", bus.channel_info
        bus.flush_tx_buffer()
        bus.shutdown()
    except can.CanError:
        print "Message NOT sent"

if __name__ == "__main__":
    print sys.argv[1]
    if len(sys.argv) > 1:
        send_one(sys.argv[1])
    else:
        send_one(1)