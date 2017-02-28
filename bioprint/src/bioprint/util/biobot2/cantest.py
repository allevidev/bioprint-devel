import can

def send_one(msg):
    bus = can.interface.Bus(channel="can0", bustype="socketcan")
    msg = can.Message(arbitration_id=0x00000,
            data=msg)
    try:
        bus.send(msg)
        print "Message sent on", bus.channel_info
    except can.CanError:
        print "Message NOT sent"

if __name__ == "__main__":
    send_one([0, 1, 2, 3, 4, 5, 6, 7])
