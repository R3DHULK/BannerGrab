import argparse # Parsing arguments.
import socket # Connecting to things.
import time # Creating logs and sleeping threads. 

# get_args ... getsCLI arguments using argparser.
def get_args():
    parser = argparse.ArgumentParser(description='Grab SSH, FTP, and HTTP banners.')
    parser.add_argument('hosts', type=str, help='CSV list of addresses to grab from.') 
    parser.add_argument('-p', '--ports', type=str, default='22,25,80', help='CSV list of ports {default: %(default)s}')
    parser.add_argument('-n', '--no-log', action='store_true', help='no log file')
    parser.add_argument('-t', '--timeout', type=int, default=3, help='time (in seconds) to wait before closing connection {default: %(default)s}')
    return parser.parse_args()

def main():
    a = get_args() # Get the CLI args.
    grab(a.hosts, a.ports, not a.no_log, a.timeout, True)

def grab(hosts, ports, logging, timeout, verbose):
    # GET HOST:
    # CONNECT -> LISTEN [TIMEOUT] -> ?LOG PRINT [loop]

    logo = '''
          __  ____  ____    __ __    ______           __    __             
         / / / / / / / /   / //_/   / ____/________ _/ /_  / /_  ___  _____
        / /_/ / / / / /   / ,<     / / __/ ___/ __ `/ __ \/ __ \/ _ \/ ___/
       / __  / /_/ / /___/ /| |   / /_/ / /  / /_/ / /_/ / /_/ /  __/ /    
      /_/ /_/\____/_____/_/ |_|   \____/_/   \__,_/_.___/_.___/\___/_/   
                                                                    
                    coded by Sumalya Chatterjee
'''

    print(logo)

    hosts = hosts.split(',')
    ports = ports.split(',')


    # Write in custom behaviors here.
    port_req = {
        22: [''],
        25: [''],
        80: ['HEAD / HTTP/1.0\r\n\r\n', '']  
    }

    log = []

    for host in hosts:
        address_down = True # We assume it is to start out. 

        for port in ports:
            sock = socket.socket()
            sock.settimeout(timeout)

            port = int(port)

            connect = '*'
            greeting = '*'
            msgs = []
            msg = '*'
            resps = []
            resp = '*'

            try:
                sock.connect((host, port))

            except socket.timeout:
                if address_down:  
                    connect = 'address down or address\' port closed'
                else:
                    connect = 'port closed'

            except Exception as e:
                connect = str(e)
                address_down = True

            else:
                connect = 'connection successful'
                address_down = False

            if not address_down:
                try:
                    greeting = recv(sock, 4096)
                except socket.timeout:
                    greeting = 'empty greeting'

                for msg in port_req.get(port, ''):
                    try:
                        msgs.append(msg)
                        send(sock, msg)

                        resp = recv(sock, 4096)

                        if resp == '':
                            resp = 'empty response'
                    except socket.timeout: 
                        resp = 'empty response'
                    except socket.error as e:
                        resp = e
                    else:
                        resps.append(resp)

            full_data = [host, port, connect, greeting, msgs, resps]
            full_data_desc = ['host', 'port', 'connection', 'greeting', 'messages', 'responses']

            if verbose:
                pretty_print(full_data, full_data_desc)
            
            log.append(full_data)

            sock.close()

# pretty_print ... Prints data all pretty.
def pretty_print(data, data_desc):
    for val in range(0, len(data)):
        if type(data[val]) is not list:
            print(str(data_desc[val]) + ': ' + str(data[val]).rstrip())

        if type(data[val]) is list and data[val]:
            print('--------------------------------')
            max_length = get_max(data[val])

            for element in range(0, len(data[val])):
                if element == 0:
                    print('[' + data_desc[val] + ']') 

                if data[val][element].strip().count(' ') == len(data[val][element]):
                    data[val][element] = '[empty msg]'
                    max_length = get_max(data[val])

                num_of_spaces = (max_length - len(data[val][element]))
                spaces = ' ' * num_of_spaces

                print(data[val][element].strip() + spaces + ' [' + str(element) + ']')
    
    print('--------------------------------')
    print('\n')

# get_max ... Returns the max number of characters in a list of strings.
def get_max(lizt):
    max = -1

    for element in lizt:
        element = element.strip()

        length = len(element)

        if element.count('\n') > 0:
            start = element.rfind('\n')
            length = len(element[start + 1:])

        if length > max:
            max = length
        
    return max

# recv ... A cleaner way of recieving data.
def recv(sock, bufsize):
    data = ''

    while True:
        try:
            buffer = sock.recv(bufsize)
        except socket.timeout:
            break
        
        data += buffer.decode('utf-8')

        if not buffer:
            break

    return data

# send ... A clean way of sending data.
def send(sock, msg):
    sock.send(msg.encode())

if __name__ == "__main__":
    main()