# Imports ---------------------------------------
from socket import gethostbyname, gethostname, socket, AF_INET, SOCK_STREAM, SOCK_DGRAM, setdefaulttimeout
from threading import Thread
import sys
import getopt
from datetime import datetime

# Global variables ------------------------------
target = gethostname()  # Set default host to be localhost
startingport = 1
endingport = 0xffff + 1
outputfile = ""
verbose = False
default_timeout = 1

default_port_list = {
    20: "FTP data transfer",
    21: "FTP control",
    22: "SSH",
    80: "HTTP",
    23: "Telnet",
    43: "WHOIS protocol",
    53: "Domain Name system (DNS)",
    67: "Dynamic Host Configuration Protocol (DHCP)",
    68: "Dynamic Host Configuration Protocol (DHCP)",
    139: "NetBIOS Session Service",
    199: "SNMP Unix multiplexer",
    194: "Internet Relay Chat (IRC)",
    218: "Message posting protocol (MPP)",
    220: "Internet Message Access Protocol (IMAP)",
    311: "Mac OS X Server Admin",
    433: "HTTPS",
    445: "SMB",
    465: "SMTP",
    502: "Modbus protocl",
    992: "Telnet over TLS/SSL",
    989: "FTPS (data)",
    990: "FPTS (control)",
    993: "Internet Message Access Protocol over TLS/SSL(IMAPS)",
    995: "Post Office Protocol 3 over TLS/SSL (POP3S)",
    853: "DNS over TLS"
}


class Scanner(Thread):

    def __init__(self, host, startingPort, endingPort, outputfile, default_timeout):
        setdefaulttimeout(default_timeout)
        Thread.__init__(self)

        self.open_ports = []

        # Ports from 1-65535
        self.ports = range(startingPort, endingPort)
        self.host = host
        self.ip = gethostbyname(self.host)
        self.output = outputfile

    def scan(self, host, port):
        print(f"Scanning {host}:{port} >>", end="\r", flush=True)
        try:
            # Create a TCP socket and try to connect
            s = socket(AF_INET, SOCK_STREAM)
            s.connect((host, port))
            description = "" if port not in default_port_list else "\t"+ default_port_list[port]
            self.open_ports.append(
                "Port %s is [Open] on host %s%s" % (port, host, description))
        except (KeyboardInterrupt, SystemExit):
            # Write out the ports that were aquired so far and exit the program
            self.write()
            print("\t----- User initiated break -----\n")
        except:
            pass

    def write(self, Print=False):
        # If output file was specified, write data there, otherwise display output on console
        if self.output is not "" and not Print:
            with open(self.output, 'w+') as f:
                if verbose:
                    f.write(
                        f"Current scan was made at: {datetime.now()}, target was: {target}, scanned ports: [{startingport} - {endingport-1}]\n"+"-"*69+"\n")
                f.writelines("%s\n" % port for port in self.open_ports)
            print("-"*69+f"\nOutput was written to: {self.output}\n"+"-"*69)
        else:
            if verbose:
                print(
                    f"\n\nCurrent scan was made at: {datetime.now()}, target was: {target}, scanned ports: {startingport}-{endingport-1}\n"+"-"*69)
            for op in self.open_ports:
                print(op)
            print()

    def run(self):
        self.threads = []

        # Enumerate our ports and scan
        for i, port in enumerate(self.ports):
            try:
                s = Thread(target=self.scan, args=(self.ip, port))
                s.start()
                self.threads.append(s)
            except (KeyboardInterrupt, SystemExit):
                # Write out the ports that were aquired so far and exit the program
                self.write(True)
                print("----- User initiated break -----\n")
                sys.exit(2)

        # Finish threads before main thread starts again
        for thread in self.threads:
            thread.join()

        # Write out the ports that are open
        self.write()


def handleError():
    print('Incorrect input format: use -h or --help for help with argument format')
    sys.exit(2)


try:
    opts, args = getopt.getopt(sys.argv[1:], "hs:e:t:o:vd:", ["help",
                                                              "start=", "end=", "target=", "out=", "verbose", "timeout"])
except getopt.GetoptError:
    handleError()
for opt, arg in opts:
    if opt in ("-h", "--help"):
        print(
            '\n\tCommand format: py ./portScanner.py [OPTIONS]\n\n\tOption\t\t\t\t\tDescription\n\
\t------------------------------------------------------------------------------------------------------------\
\n\t-h --help\t\t\t\tShows this helper box, overrides all other arguments.\n\
\n\t-s --start\t <startPortNumber>\tMust be in range [1 - endPortNumber]. (Default is 1)\n\
\n\t-e --end\t <endPortNumber>\tMust be in range [startPortNumber - 65535]. (Default is 65535)\n\
\n\t-t --target\t <targetIPv4>\t\tIP of the target to scan. (Default is localhost)\n\
\n\t-o --output\t <outputFileName>\tLog script output to file, option is omitted in case of\
\n\t\t\t\t\t\tuser interrupt. (Prints output to console if not specified)\n\
\n\t-v --verbose\t\t\t\tInclude extra information about the scan.\n\
\n\t-d --timeout\t <seconds>\t\tSet the timout for each connection. (Default is 3.0s)\n')
        sys.exit()
    elif opt in ("-s", "--start"):
        if 1 <= int(arg) <= endingport:
            startingport = int(arg)
        else:
            handleError()
    elif opt in ("-e", "--end"):
        if startingport <= int(arg)+1 <= 0xffff:
            endingport = int(arg)+1
        else:
            handleError()
    elif opt in ("-t", "--target"):
        target = arg
    elif opt in ("-o", "--out"):
        outputfile = arg
    elif opt in ("-v", "--verbose"):
        verbose = True
    elif opt in ("-d", "--timeout"):
        if float(arg) > 0:
            default_timeout = float(arg)

# Scanner object which initializes our vars and then we run our scanner
scanner = Scanner(target, startingport, endingport,
                  outputfile, default_timeout)
scanner.run()
