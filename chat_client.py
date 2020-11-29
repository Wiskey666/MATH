# Imports
import sys
import socket
import select
import errno
from colorama import init, Fore, Back, Style
import socket
import threading
import time
import os

from win10toast import ToastNotifier

# Inits
toaster = ToastNotifier()
init(convert=True)

print("\33[37m\33[1m","""
                   :::!~!!!!!:.
                  .xUHWH!! !!?M88WHX:.
                .X*#M@$!!  !X!M$$$$$$WWx:.
               :!!!!!!?H! :!$!$$$$$$$$$$8X:
              !!~  ~:~!! :~!$!#$$$$$$$$$$8X:  
             :!~::!H!<   ~.U$X!?R$$$$$$$$MM!  
             ~!~!!!!~~ .:XW$$$U!!?$$$$$$RMM!                      
               !:~~~ .:!M"T#$$$$WX??#MRRMMM!               
               ~?WuxiW*`   `"#$$$$8!!!!??!!!
             :X- M$$$$       `"T#$T~!8$WUXU~
            :%`  ~#$$$m:        ~!~ ?$$$$$$
          :!`.-   ~T$$$$8xx.  .xWW- ~""##*"
.....   -~~:<` !    ~?T#$$@@W@*?$$      /`
W$@@M!!! .!~~ !!     .:XUW$W!~ `"~:    :
#"~~`.:x%`!!  !H:   !WM$$$$Ti.: .!WUn+!`
:::~:!!`:X~ .: ?H.!u "$$$B$$$!W:U!T$$M~
.~~   :X@!.-~   ?@WTWo("*$$$W$TH$! `
Wi.~!X$?!-~    : ?$$$B$Wu("**$RM!
$R@i.~~ !     :   ~$$$$$B$$en:``
?MXT@Wx.~    :     ~"##*$$$$M~
    """ + Fore.WHITE)

time.sleep(2)
os.system('cls||clear')

# Info
print(Fore.CYAN + """
     ███▄ ▄███▓ ▄▄▄     ▄▄▄█████▓ ██░ ██ 
    ▓██▒▀█▀ ██▒▒████▄   ▓  ██▒ ▓▒▓██░ ██▒
    ▓██    ▓██░▒██  ▀█▄ ▒ ▓██░ ▒░▒██▀▀██░
    ▒██    ▒██ ░██▄▄▄▄██░ ▓██▓ ░ ░▓█ ░██ 
    ▒██▒   ░██▒ ▓█   ▓██▒ ▒██▒ ░ ░▓█▒░██▓
    ░ ▒░   ░  ░ ▒▒   ▓▒█░ ▒ ░░    ▒ ░░▒░▒
    ░  ░      ░  ▒   ▒▒ ░   ░     ▒ ░▒░ ░
    ░      ░     ░   ▒    ░       ░  ░░ ░
       ░         ░  ░         ░  ░  ░                                     
""" + "\33[90m" + """
    -----------------------------------""" + Fore.CYAN + """
    Version: Alpha 1_1
    Author: Wiskey666
    Mail: 1488step@horsefucker.org
    DS: yourmomgay#1488""" + "\33[90m" + """
    -----------------------------------""" + Fore.CYAN + """

    This is a console chat for special lovers of this shit.
    The chat will be improved (both the client side and the server side).
    Thank you for noticing and trying it!
""" + "\33[90m" + """
    -----------------------------------""" + Fore.CYAN + """
    """+ Fore.WHITE)

# Client Settings
IP = input('    IP: ')
if IP == '':
    print(Fore.YELLOW + "\n    [!] Please enter IP!")
    time.sleep(5)
    sys.exit()
    
try:
    PORT = int(input('    Port: '))
    if PORT == '':
        print(Fore.YELLOW + "\n    [!] Please enter port!")
        time.sleep(5)
        sys.exit()   
except ValueError:
    print(Fore.YELLOW + "\n    [!] Port must be an integer!")
    time.sleep(5)
    sys.exit()
    
ver = "Alpha 1_1"

# Choosing Nickname
nickname = input('    Username: ')
if nickname == '':
    print(Fore.YELLOW + "\n    [!] Please enter nickname!")
    time.sleep(5)
    sys.exit()

print("""
    -----------------------------------    
""")
# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((IP, PORT))
except socket.error as e:
    if e.errno == errno.ECONNREFUSED:
        print(Fore.YELLOW + "\n    [!] Server refused connection or unavailable")
    else:
        raise

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            message = client.recv(1024).decode('utf-8')
            
            #Version Check
            #If Server Sends Conflict Code - Kick
            if "Code 409" in message:
                print(Fore.RED +'░' + Fore.WHITE + '░' + Fore.RED + '░ ' + Fore.WHITE + message)
                client.close()
                break
            if "Code 401" in message:
                print(Fore.RED +'░' + Fore.WHITE + '░' + Fore.RED + '░ ' + Fore.WHITE + message)
                client.close()
                break
            else:
                # If 'NICK' Send Nickname
                if message == 'NICK':
                    client.send(nickname.encode('utf-8'))
                    client.send(ver.encode('utf-8'))
                else:
                    print(Fore.RED +'░' + Fore.WHITE + '░' + Fore.RED + '░ ' + Fore.WHITE + message)
                    #Check For New Messages
                    if "<"+ nickname +">" in message or "[+]" in message or "[-]" in message or "[!]" in message:
                        continue
                    else:
                       toaster.show_toast("MATH", message, threaded=True)
        except:
            # Close Connection When Error 
            print(Fore.RED +'>' + Fore.WHITE + '>' + Fore.RED + '> ' + Fore.RED + "[-] An error occured!")
            client.close()
# Sending Messages To Server
def write():
    while True:
        try:
            message_text = input('')
            # Check for blank massage
            if message_text == '':
                continue
            else:
                message = '<{}> {}'.format(nickname, message_text)
                client.send(message.encode('utf-8'))
        except:
            pass

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

