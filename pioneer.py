'''
Created on Jan 3, 2015

@author: jochem
'''
'''
Volume:

    VD = VOLUME DOWN
    MZ = MUTE ON/OFF
    VU = VOLUME UP
    ?V = QUERY VOLUME

Power control:

    PF = POWER OFF
    PO = POWER ON
    ?P = QUERY POWER STATUS

Input selection

    05FN = TV/SAT
    01FN = CD
    03FN = CD-R/TAPE
    04FN = DVD
    19FN = HDMI1
    05FN = TV/SAT
    00FN = PHONO
    03FN = CD-R/TAPE
    26FN = HOME MEDIA GALLERY(Internet Radio)
    15FN = DVR/BDR
    05FN = TV/SAT
    10FN = VIDEO 1(VIDEO)
    14FN = VIDEO 2
    19FN = HDMI1
    20FN = HDMI2
    21FN = HDMI3
    22FN = HDMI4
    23FN = HDMI5
    24FN = HDMI6
    25FN = BD
    17FN = iPod/USB
    FU = INPUT CHANGE (cyclic)
    ?F = QUERY INPUT
'''

import logging
import socket
import sys
logger = logging.getLogger(__name__)

size = 1024

class pioneer():
    '''
    Pioneer control class
    '''

    def __init__(self,host, port):
        '''
        Constructor
        '''
        self.host=host
        self.port=port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.debug("Initialized host {:s} on port {:d}".format(self.host, self.port))
    
    def send(self,cmd):
        logger.debug("Sending command")
        buf=bytes(cmd+"\r\n",'ascii')
        self.socket.send(buf)
        
        datastr=[]
        data=bytearray()
        
        try:
            msg = self.socket.recv(4096)
        except socket.timeout as e:
            err = e.args[0]
            # this next if/else is a bit redundant, but illustrates how the
            # timeout exception is setup
            if err == 'timed out':
                print('recv timed out, retry later')
            else:
                print(e)
                sys.exit(1)
        except socket.error as e:
            # Something else happened, handle error, exit, etc.
            print(e)
            sys.exit(1)
        else:
            if len(msg) == 0:
                print('orderly shutdown on server end')
                sys.exit(0)
            else:
                print(msg)
            # got a message do something :)
    # waiting for receiving data
#         while 1:
#             rxbuf = self.socket.recv(size)
#             if rxbuf:
#                 data.extend(rxbuf)
#                 print("received")
#                 datastr.append(data.decode(encoding='ascii'))
#                 break
#             else:
#                 print("closing")
#                 self.socket.shutdown(socket.SHUT_WR) 
#                 self.socket.close()
#                 break
#         datastr = data.decode(encoding='ascii')
#         print("%"+ "".join(datastr))
        
    def open(self):
        
        self.socket.connect((self.host,self.port))
        self.socket.settimeout(1)
        logger.debug("Opening connection to host {:s} on port {:d}".format(self.host, self.port))
        
    def close(self):
        self.socket.shutdown(socket.SHUT_WR) 
        self.socket.close()
        logger.debug("Closing connection to host {:s} on port {:d}".format(self.host, self.port))
    

        
if __name__ == "__main__":
    print("one.py is being run directly")
    logging.basicConfig(level = logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')  
    rcx = pioneer("pioneer.lan", 8102)
    
    rcx.open()
    rcx.send("VD")
    rcx.send("VD")
    rcx.send("VD")
    rcx.send("VD")
    rcx.send("VU")
    rcx.send("VU")
    rcx.send("VU")
    rcx.send("VU")
    
    rcx.send("?V")
    rcx.send("?F")
    rcx.send("04FN")
#     rcx.send("05FN") #TV
#     rcx.send("06FN") #SAT
    rcx.close()

        