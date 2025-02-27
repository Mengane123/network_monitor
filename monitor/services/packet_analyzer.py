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
    def process_packet(self,packet):
        if IP in packet: #checks if the packet contains the ip layer 
            #extracting relevant information from the packet 
            connection = NetworkConnection(
                source_ip=packet[IP].src,
                destination_ip = packet[IP].dst,
                source_port = packet.sport if hasattr(packet , 'sport') else 0,
                destination_port = packet.dport if hasattr(packet , 'dport') else 0,
                protocol = packet.proto if hasattr(packet , 'proto') else 'Unknown',
                bytes_transferred = len(packet)

            )
            connection.save()


    def start_capture(self):
        sniff(prn=self.process_packet , store=0, stop_filter=lambda _: self.stop_flag.is_set())
        #here sniff() captures network traffic , and then prn=self.process_packet calls process_packet() method for each captured packet , 
        #store=0 prevents storing packets in memory (to save memory usage)
        #now the lambda , stop_filter checks if the self.stop_flag is set , if it is set (means if is_set() return TRUE) , sniff() will stop capturing

    def stop_filter(self):
        self.stop_flag.set()



        




