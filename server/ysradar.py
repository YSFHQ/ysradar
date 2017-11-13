#!/usr/bin/env python

from socket import *
from random import randrange
import sys, os, threading, re, math, time, urllib, string, struct

try: import psyco; psyco.full()
except: pass


def adebug(var):
    global debug
    debug=var
    debug=debug.replace('\x01','-01-')
    debug=debug.replace('\x02','-02-')
    debug=debug.replace('\x03','-03-')
    debug=debug.replace('\x04','-04-')
    debug=debug.replace('\x05','-05-')
    debug=debug.replace('\x06','-06-')
    debug=debug.replace('\x07','-07-')
    debug=debug.replace('\x08','-08-')
    debug=debug.replace('\x09','-09-')
    debug=debug.replace('\x10','-10-')
    debug=debug.replace('\x11','-11-')
    debug=debug.replace('\x12','-12-')
    debug=debug.replace('\x13','-13-')
    debug=debug.replace('\x14','-14-')
    debug=debug.replace('\x15','-15-')
    debug=debug.replace('\x16','-16-')
    debug=debug.replace('\x17','-17-')
    debug=debug.replace('\x18','-18-')
    debug=debug.replace('\x19','-19-')
    debug=debug.replace('\x20','-20-')
    debug=debug.replace('\x0A','-0A-')
    debug=debug.replace('\x0B','-0B-')
    debug=debug.replace('\x0C','-0C-')
    debug=debug.replace('\x0D','-0D-')
    debug=debug.replace('\x0E','-0E-')
    debug=debug.replace('\x0F','-0F-')
    debug=debug.replace('\x1A','-1A-')
    debug=debug.replace('\x1B','-1B-')
    debug=debug.replace('\x1C','-1C-')
    debug=debug.replace('\x1D','-1D-')
    debug=debug.replace('\x1E','-1E-')
    debug=debug.replace('\x1F','-1F-')
    debug=debug.replace('\x80','-80-')
    debug=debug.replace('\x8c','-8c-')
    print "s"
    print debug.replace('\x00','.')
    print "e"
    return debug

def cut_coord(coord):
    res=""
    for n in coord:
        v=str(hex(ord(n)))[2:4]
        if len(v)==1:
            v="0"+v
        res=v+res
    #print res
    return res

def bin(n):
    res = ''
    while n != 0: n, res = n >> 1, `n & 1` + res
    return res


def ieee_to_int(nb):
    #nb=bin(int(nb,16)).replace('L','')
    nb=bin(int(nb,16)).replace('L','')
    while len(nb)<32:
        nb="0"+str(nb)
    sign=(int(str(nb)[0])*2-1)*-1
    exp=int(str(nb)[1:9],2)-127
    #print exp
    nb="1"+str(nb)[9:]
    result=0
    for n in nb:
        result=result+int(n)*2**exp
        exp-=1
    result*=sign
    #print result
    return result


class ThreadURL(threading.Thread):
    """object thread for the reception of the messages, print the players"""
    def __init__(self,url):
        threading.Thread.__init__(self)
        self.url=url
    def run(self):
        try:
            urllib.urlopen(self.url)
        except:
            print "cannot do it"

class SendMess30s(threading.Thread):
    """thread which send the messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        #self.c = conn            # ref. du socket de connexion
        self.c = conn
        self.running = threading.Event( )
        #print "30s thread auto mess"
    def run(self):

        while not self.running.isSet():
            self.running.wait(30)
            try:
                self.c.send("\x04\x00\x00\x00\x11\x00\x00\x00")
                self.c.send("\x04\x00\x00\x00\x25\x00\x00\x00")
                #print("30s")
            except:
                print "disconnected ?"
                sys.exit(0)


    def stop(self):
        self.running.set( )

class ThreadReception(threading.Thread):
    """objet thread for reception"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn            # ref. du socket de connexion
        self.message="0"
        self.ids={}
        self.ptime=time.time()
        #self.s_c=0 #connected fully or not
    def run(self):
        s_c=0
        while 1:
            if s_c==0:
                mess = self.connexion.recv(2048)
            else:
                mess = self.connexion.recv(462)

            clef=""
            if s_c==1:
                if mess.find('\x00\x00\x25\x00\x00\x00')!=-1:
                    self.ids={}
                    mess2 = mess
                    while mess2.find('\x00\x00\x25\x00\x00\x00')!=-1:
                        pos = mess2.find('\x00\x00\x25\x00\x00\x00') + 2
                        packet_size = struct.unpack('I', mess2[pos-4:pos])[0]
                        player = mess2[pos:packet_size+pos]
                        mess2 = mess2[packet_size+pos:]
                        try:
                            status=struct.unpack('H', player[4:6])[0]
                            iff=struct.unpack('H', player[6:8])[0]
                            id=struct.unpack('I', player[8:12])[0]
                            username=player[16:]
                            username=username[:username.find('\x00')]
                            if status == 1 or status==3: #flying user (1=regular, 3=server)
                                self.ids[str(id)]='[IFF'+str(iff+1)+']'+username.replace(":","").replace(" ","")
                        except:
                            continue
                if time.time()-self.ptime>=refresh_rate:
                    self.ptime=time.time()
                    if len(self.message)<5:
                        nb_t=2
                        #print "less"
                    else:
                        nb_t=sensibility

                    self.message="0"
                    if s_c==1:
                        pos_mess=-1
                        c=0

                        while mess[0:5]!="\x49\x00\x00\x00\x0B" and c<nb_t:
                            #print "not found" + str(hex(ord(mess[0])))
                            mess=self.connexion.recv(462)
                            if len(mess)!=462:# and mess[0]!="\x00":
                                c+=1

                        if mess[0:5]=="\x49\x00\x00\x00\x0B":
                            pos_mess=0
                        while pos_mess!=-1:
                            pos_z=ieee_to_int(cut_coord(mess[22+pos_mess:26+pos_mess]))/0.3048
                            #print pos_z
                            if alt_limit<pos_z:
                                if self.message=="0":
                                    self.message=""
                                id2=hex(ord(mess[12+pos_mess:13+pos_mess]))[2:]
                                id3=hex(ord(mess[13+pos_mess:14+pos_mess])+256)[2:]
                                id=int(str(id3)+id2,16)
                                #print id
                                pos_x=ieee_to_int(cut_coord(mess[18+pos_mess:22+pos_mess]))
                                pos_y=ieee_to_int(cut_coord(mess[26+pos_mess:30+pos_mess]))
                                try:
                                    speed=math.sqrt((pos_x-players_x[id])**2+(pos_y-players_y[id])**2)/refresh_rate*1.943844#to be in knot
                                except:
                                    speed=0
                                players_x[id]=pos_x
                                players_y[id]=pos_y

                                heading=int(cut_coord(mess[30+pos_mess:32+pos_mess]),16)*360/65535.0
                                self.ptime=time.time()
                                name = ""
                                #for k, v in self.ids.items():
                                    #print k+' '+str(id)
                                if str(id) in self.ids:
                                    name=self.ids[str(id)]
                                else:
                                    name=str(id)
                                self.message+=name+":"+str(int(pos_x)*0.053996)+":"+str(int(pos_z/10))+":"+str(int(pos_y)*0.053996)+":"+str(int(heading))+":"+str(int(speed))+"\\"
                                #print "T>> ",self.message
                            pos_mess=mess.find("\x49\x00\x00\x00\x0b",pos_mess+1)
                            #print "pu",pos_mess
                    #print "here"
                    self.message+="\r\n"
                    for cle in conn_client:
                        #print "do it"
                        try:
                            if self.message!="":
                                conn_client[cle].send(self.message)
                        except:
                            clef=cle
                            print str(cle)+" left"
                        #print self.message
                        #print dic_online[key],pos_x,pos_y,pos_z
                if clef!="":
                    conn_client.__delitem__(clef)

            if s_c==0:
                print "do it"
                if mess.find("\x04\x00\x00\x00\x10\x00\x00\x00")!=-1:
                    print "end login"
                    s_c=1
                    self.connexion.send("\x0C\x00\x00\x00\x06\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00")
                    self.connexion.send("\x08\x00\x00\x00\x26\x00\x00\x00\x00\x00\x00\x00")
                    self.connexion.send("\x04\x00\x00\x00\x25\x00\x00\x00")
                    th_server = Server()
                    th_server.start()

                if mess.find("\x00\x00\x2C\x00\x00\x00\x01")!=-1:
                    #adebug(mess)
                    print "sending airplane list"
                    self.connexion.send(mess)

            if mess.find("\x1C\x00\x00\x00\x21\x00\x00\x00\x01\x00")!=-1 or mess.find("\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\x9C\x46")!=-1:
                print "almost"
                self.connexion.send("\x0C\x00\x00\x00\x06\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00")
                self.connexion.send("\x08\x00\x00\x00\x26\x00\x00\x00\x00\x00\x00\x00")

            if mess =='':
                break
            if mess.find('\x00\x00\x00\x20\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')!=-1:
                #print "mess"
                chat = mess[mess.find('\x00\x00\x00\x20\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')+15:]
                #chat = chat[:chat.find('\x00')]
                if chat.find('took off (')!=-1 or chat.find('has left the airplane')!=-1:
                    self.connexion.send("\x04\x00\x00\x00\x25\x00\x00\x00")

        # On force la fermeture du thread <emission> :
        #th_E._Thread__stop()
        print "***Connection stopped***"
        self.connexion.close()
        st=raw_input("Press <ENTER> to exit")
        os._exit(1)

class ThreadServerList(threading.Thread):
    """thread which send the messages"""
    def __init__(self):
        threading.Thread.__init__(self)
        #self.c = conn            # ref. du socket de connexion
        self.running = threading.Event( )

    def run(self):

        while not self.running.isSet():
            try:
                print "updating"
                st=ThreadURL("http://marcjeanmougin.free.fr/ys_servers/radaronline.php?ips="+ips.replace(' ',''))
                st.start()
                #p=urllib.urlopen("http://marcjeanmougin.free.fr/ys_servers/radaronline.php?ips="+ips.replace(' ',''))

            except:
                print "canno update the state on the radar list"

            self.running.wait(300)


    def stop(self):
        self.running.set( )


##try:
##    p=urllib.urlopen('http://www.yspilots.com/shadowhunters/yschat/yscradar.txt')
##except:
##    print "cannot check the version"
##if p.read().find("0")!=-1:
##    print "You cannot use this version now, update YSChat to use the radar for the YSATC radar"
##    st=raw_input("Press <ENTER> to exit...")
##    sys.exit(0)
s_c=0
c=socket()

port=7915
#alt_limit=10.0
#refresh_rate=3
#sensibility=3
conversion=20110207
alt_limit=input("Altitude limit? (enter a number in feet, efficient if upper than 100) ")/10.0 #in feet
refresh_rate=input("Refresh rate in seconds? (1.25 -> 5) ")
sensibility=input("Sensibility? (choose 3 for a map without motion path, else choose 6) ")
ipaddr=raw_input("IP Address? ")
#conversion=input("YSFS version? ")
conn_version=hex(conversion)
conn_version=chr(int(conn_version[len(conn_version)-2:len(conn_version)],16))+chr(int(conn_version[len(conn_version)-4:len(conn_version)-2],16))+chr(int(conn_version[len(conn_version)-6:len(conn_version)-4],16))+chr(int(conn_version[2:len(conn_version)-6]))
mySocket = socket(AF_INET,SOCK_STREAM)

conn_client = {} # dictionnaire des connexions clients

class Server(threading.Thread):
    """objet thread for reception"""
    def __init__(self):
        threading.Thread.__init__(self)
        print "starting"

    def run(self):

        try:
            mySocket.bind(('', 7910))
        except:
            print "The server failed to start"
            st=raw_input("Press <ENTER> to exit...")
            sys.exit(0)
        print "Server ready, waiting for requests..."
        mySocket.listen(30)

        while 1:

            connexion, adresse = mySocket.accept()
            # Record the connexion in a dictionnary
            #it = th.getName() # identifiant du thread
            it=randrange(1,1000)
            conn_client[it] = connexion
            #connexion.send("")
            print "Client %s connected, address IP %s, port %s." %\
            (it, adresse[0], adresse[1])
            connexion.send("0\r\n")

ids={}
ips=""
ip_info=getaddrinfo(gethostname(), None)
for nb in ip_info:
    ips+="|"+nb[4][0]
try:
    c.connect((ipaddr,port))
except:
    print "failed to connect"
    sys.exit(0)
#username=raw_input('USERNAME (15 characters max) ? ')
players_x={}
players_y={}
username="~server-radar"
username=username+"\x00"*(15-len(username))
username='\x18\x00\x00\x00\x01\x00\x00\x00'+username
username+='\x00'+conn_version
c.send(username)
mess1=c.recv(1024)
#if mess1[:5]=="\x08\x00\x00\x00\x1D":
    #print "version "+ mess1[8:12]
if len(mess1)<12:
    mess1=c.recv(1024)
mt="\x00"*28
#adebug(mess1)
if mess1.find("RADARALTI")!=-1:
    pos1=mess1.find("RADARALTI")-12
    print "found"
else:
    print "not found"
    pos1=mess1.find("\x40",20)
#ms="\x0C\x00\x00\x00\x06\x00\x00\x00\x09\x00\x00\x00\x00\x00\x00\x00\x0C\x00\x00\x00\x06\x00\x00\x00\x0A\x00\x00\x00\x00\x00\x00\x00\x0C\x00\x00\x00\x06\x00\x00\x00\x0B\x00\x00\x00\x00\x00\x00\x00"+mess1[pos1:mess1.find(mt)+28]+"\x00\x04\x00\x00\x00\x21\x00\x00"+mess1[mess1.find(mt)+28:]
ms="\x0C\x00\x00\x00\x06\x00\x00\x00\x09\x00\x00\x00\x00\x00\x00\x00\x0C\x00\x00\x00\x06\x00\x00\x00\x0A\x00\x00\x00\x00\x00\x00\x00\x0C\x00\x00\x00\x06\x00\x00\x00\x0B\x00\x00\x00\x00\x00\x00\x00"+mess1[pos1:mess1.find(mt)+28].replace("\x00\x40\x00\x00\x00\x04\x00\x00\x00","\x00\x04\x00\x00\x00\x21\x00\x00\x00\x40\x00\x00\x00\x04\x00\x00\x00")+mess1[mess1.find(mt)+28:]
#adebug(ms[:48])
#raw_input("press enter")
c.send(ms)
dic_online={}

try:
    #th_E      = ThreadServerList()
    #th_E.daemon = True
    th_R      = ThreadReception(c)
    th_R.daemon = True
    thread30s = SendMess30s(c)
    thread30s.daemon = True
    th_R.start()
    #th_E.start()
    thread30s.start()
    while True: time.sleep(100)
except (KeyboardInterrupt, SystemExit):
    print '\n! Received keyboard interrupt, quitting threads.\n'
