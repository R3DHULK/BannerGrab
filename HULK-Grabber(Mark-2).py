import socket

logo = '''
          __  ____  ____    __ __    ______           __    __             
         / / / / / / / /   / //_/   / ____/________ _/ /_  / /_  ___  _____
        / /_/ / / / / /   / ,<     / / __/ ___/ __ `/ __ \/ __ \/ _ \/ ___/
       / __  / /_/ / /___/ /| |   / /_/ / /  / /_/ / /_/ / /_/ /  __/ /    
      /_/ /_/\____/_____/_/ |_|   \____/_/   \__,_/_.___/_.___/\___/_/   
                                                                    
                    coded by Sumalya Chatterjee
'''
print(logo)

def ban_grab(host, port, delay) :
    '''
    This function takes three parameters from main() to process and get the banner of the requested port
    It has a specific condition for HTTP port which make this program more flexible than other simple
    banner grabbers

    :param host:        Ask HULK a IP ADDRESS or URL
    :param port:         HULK REQUESTED PORT
    :param delay:      TIME DELAY for SEARCH
    :return:                 None
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)           # Making a TCP socket
    try :
        s.settimeout(delay)
        if port == 80 :                                             # If user requested port is 80
            s.connect((str(host), port))
            GET = 'GET / HTTP/1.1\nHost: '+ str(host) +'\n\n'       # Request more than ordinary three way handshake
            s.sendall(str.encode(GET))
            banner = s.recvfrom(512)                                # Important part of the banner received

        else :
            s.connect((str(host), port))                            # Trying normal TCP handshake and getting banner
            banner = s.recvfrom(512)

        banner = banner[0]
        banner = banner.splitlines()                                # Processing received banner
        for line in banner:
            line = str(line)
            line = line.replace('\'','')                            # Removing unnecessary part of the line
            print(line[1::])

    except Exception as er :
        print('Error : ' + str(er))                                 # Exception handling

    finally :
        s.close()                                                   # Closing socket

def user_input(msg) :                                               # Checking for keyboard interrupt
    while True :
        try :
            return input(msg)
        except KeyboardInterrupt :
            print('HULK does not allowed you to quit right now !')

def main() :
    host = user_input('Ask HULK a IP or URL : ')                         # Taking and validating user inputs
    port = int(user_input('Ask HULK a port : '))
    if port < 1 or port > 65535 :
        print('Invalid input for port\nDefault set 80')
        port = 80
    delay = int(user_input('Enter delay : '))
    if delay < 0 or delay > 100 :
        print('Invalid input for delay\nDefault set 5')
        delay = 5
    print('='*30 + 'Banner' +'='*30)
    ban_grab(host, port, delay)                                     # Calling function ban_grab()

if __name__ == '__main__' :
    main()