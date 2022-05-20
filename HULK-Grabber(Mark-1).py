import socket
from termcolor import colored

logo = '''
          __  ____  ____    __ __    ______           __    __             
         / / / / / / / /   / //_/   / ____/________ _/ /_  / /_  ___  _____
        / /_/ / / / / /   / ,<     / / __/ ___/ __ `/ __ \/ __ \/ _ \/ ___/
       / __  / /_/ / /___/ /| |   / /_/ / /  / /_/ / /_/ / /_/ /  __/ /    
      /_/ /_/\____/_____/_/ |_|   \____/_/   \__,_/_.___/_.___/\___/_/   
                                                                    
                    coded by Sumalya Chatterjee
'''
print(logo)

def retBanner(host, port):
    try:
        socket.setdefaulttimeout(2)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        banner = sock.recv(1024)

        return banner
    except:
        return


def main():
    host = str(input(colored("[*] HULK asks target IP: ", 'blue')))
    p = int(input(colored('[*] HULK wants you to enter the port upper bound: ', 'blue')))
    for i in range(1, p+1):
        banner = retBanner(host, i)

        if banner:
            print(colored(f"[+] {host}:{i}  ->     " + banner.decode("utf-8"), 'green'), end='')
        else:
            print(colored(f"[-] {host}:{i}  ->     " + "HULK can't find your target :( ", 'red'))

    exit(0)


main()