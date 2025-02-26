import socket
import psutil 
from concurrent.futures import ThreadPoolExecutor
from ..models import PortStatus
from django.utils import timezone 

class PortScanner:
    def __init__(self,max_workers=10): #here workers are the threads that will be used to do the concurrent scanning
        self.max_workers = max_workers
    
    def scan_port(self,port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates a TCP socket to check connectivity 
        sock.settimeout(1) #timeout of 1 sec , so that it won't wait long 

        try:
            result = sock.connect_ex(('localhost',port))
            status = 'open' if result==0 else 'closed'
            service = socket.getservbyport(port) if status == 'open' else None
        except:
            status = 'filtered' #if exception occures such as permission denied or firewall blocks the connection , the port will be marked as 'filtered'
            service = None 
        finally:
            sock.close()

        return port, status, service
    
    #this method scans these 13 predefined list of ports.
    def scan_common_ports(self):
        common_ports = [20, 21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 5432, 8080]


        #uses threadpoolexecutor to scan multiple ports in parallel which improved efficiency 
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = executor.map(self.scan_port , common_ports) #this mapping runs scan_port() method for each port in common_ports list 
        

        #this updates the our postgres database after each scan 
        for port, status, service in results:
            PortStatus.objects.update_or_create(
                port_number = port,
                defaults={
                    'status' : status,
                    'service' : service,
                    'last_checked' : timezone.now()
                }
            )












