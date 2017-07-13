import socket
import subprocess
import sys, time
from datetime import datetime
import threading


class PortScanner():
    def __init__(self):
        self.mode = input('Enter mode [(t)urbo, (n)ormal]')
        self.ports_names = {
            1: 'ICMP',
            6: 'TCP',
            17: 'UDP',
            20: 'FTP',
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            42: 'WINS',
            47: 'GRE',
            50: 'AH',
            51: 'ESP',
            53: 'DNS',
            80: 'HTTP',
            81: 'HTTP',
            88: 'Kerberos',
            110: 'POP3',
            111: 'Portmapper (Linux)',
            119: 'NNTP',
            135: 'RPC-DCOM',
            137: 'SMB',
            138: 'SMB',
            139: 'SMB',
            143: 'IMAP',
            161: 'SNMP',
            162: 'SNMP',
            8080: 'HTTP'
        }
        self.ip_address = ''
        self.start_time = ''
        self.stop_time = ''
        self.init()

    def init_values(self):
        subprocess.call('clear', shell=True)
        #remote_server = input('IP or remote server name to scan: ')
        remote_server = '192.168.0.22'
        self.ip_address = socket.gethostbyname(remote_server)

    @staticmethod
    def print_scanning(remoteServerIP):
        print("-" * 60)
        print("Please wait, scanning remote host", remoteServerIP)
        print("-" * 60)

    def single_scan(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((self.ip_address, port))

        if result == 0:
            print('Port {}: Open [{}]'.format(port, self.ports_names[port]))
            sock.close()

    def scan_ports(self):
        self.start_time = datetime.now()

        socket.setdefaulttimeout(0.1)

        try:
            print('Scanning all ports 1-9999...')
            for port in range(1, 9999):
                self.single_scan(port)

            print('Scanning most common ports...')
            for port in self.ports_names:
                self.single_scan(port)

        except KeyboardInterrupt:
            print('Pressed Ctrl + C, exiting...')
            sys.exit()
        except socket.gaierror:
            print('Hostname could not be resolved')
        except socket.error:
            print("Couldn't connect to server")
            sys.exit()

        self.stop_time = datetime.now()

    def TCP_connect(self, ip, port_number, delay, output):
        TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        TCPsock.settimeout(delay)

        try:
            TCPsock.connect((ip, port_number))
            output[port_number] = 'Listening'
        except:
            output[port_number] = ''

    def scan_turbo(self):
        print('Turbo scaning...')

        range_ports = 99999
        step = 0
        threads = []
        output = {}
        delay = 1

        for i in range(step, range_ports):
            t = threading.Thread(target=self.TCP_connect, args=(self.ip_address, i, delay, output))
            threads.append(t)

        for i in range(step, range_ports):
            threads[i].start()

        for i in range(step, range_ports):
            threads[i].join()

        for i in range(step, range_ports):
            if output[i] == 'Listening':
                print(str(i) + ': ' + output[i])

    def scan(self):
        self.print_scanning(self.ip_address)
        if self.mode == 't':
            self.scan_turbo()
        elif self.mode == 'n':
            self.scan_ports()
        else:
            self.scan_ports()

    def init(self):
        self.init_values()
        self.scan()


if __name__ == '__main__':
    port_scanner = PortScanner()
