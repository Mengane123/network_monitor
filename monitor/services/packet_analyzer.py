# this script implements a network packet analyzer using scapy . it captures live network traffic , 
# extracts useful information from the packet like (ip address , ports and protocol) , and stores them in the NetworkConnection Model . 

# the PacketAnalyzer class provides methods to start and stop packet capture in a thread safe manner , using (threading.event)

from scapy.all import sniff, IP  #sniff captures network packets , and helps in filtering and analyzing IP Based packets 
from ..models import NetworkConnection 
from django.utils import timezone #used to store timestamp in django-compatible format 
import threading #used to control packet capturing (start/stop) functionality 

class PacketAnalyzer:
    def __init__(self):
        self.stop_flag = threading.Event() #threading.Event() object is used to control when the packet sniffing should stop 

    #this method is called each time a packet is captured 
    def packet_process(self,packet):
        if IP in packet: #checks if the packet contains the ip layer 
            #extracting relevant information from the packet 
            




