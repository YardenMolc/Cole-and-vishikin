from socket import socket
from socket import error
from socket import AF_INET
from socket import SOCK_STREAM
from socket import SOCK_DGRAM
from socket import SHUT_RDWR
from socket import SHUT_WR
from threading import Thread
from threading import Lock
import math


class Vertex(object):
    def __init__(self,ID):
        path="input_vertex_" + str(ID) +".txt"
        self.ID=ID
        v_parm=[]
        with open(path) as fp:
            line = fp.readline()
            v_parm.append(line)
            while line:
                line = fp.readline()
                v_parm.append(line)   
        self.ver_num = v_parm[0].strip('\n')
        self.UDP_master = v_parm[1].strip('\n')
        self.IP_master=v_parm[2].strip('\n')
        self.UDP_v=v_parm[3].strip('\n')
        self.TCP_v=v_parm[4].strip('\n')
        if (v_parm[5].strip('\n')!='None'):
            self.TCP_p=int((v_parm[5]).strip('\n'))
        else: self.TCP_p=None
        if (v_parm[6].strip('\n')!='None'):
            self.IP_p=v_parm[6].strip('\n')
        else: self.IP_p=None 
        self.v_childs=[]
        if (len(v_parm)>=7):
            for i in range(7,len(v_parm),2):
                if (v_parm[i].strip('\n')!='*'):
                    self.v_childs.append([[v_parm[i].strip('\n'),v_parm[i+1].strip('\n')]])
        self.color=ID
        self.SERVER_v=socket(AF_INET, SOCK_STREAM)
        self.SERVER_v.bind(('', int(self.TCP_v)))
        self.SERVER_v.listen(1024)
        self.message_got=""
        self.old_father=""
        self.old_color=""
        self.old_round='0'
        self.round='0'
        self.destroy=False
        self.cpy_color=self.ID
        #self.threads=[]
        self.childs_color={}
        self.new_father=""
        self.Destory_final=False
        self.Destory_final_tcp=False
        self.Destory_final_listen_UDP=False
        self.f = open('output_vertex'+'_'+self.ID+'.txt', 'w')
        self.f.close()
        self.lock=Lock()
        self.parent_ID=""



def write_to_file(v,write):
    #lock=Lock()
    v.lock.acquire() # thread blocks at this line until it can obtain lock
    file1 = open('output_vertex'+'_'+v.parent_ID+'.txt', "a")
    file1.write(v.message_got + '_' + str(write) + '\n')
    file1.close()
    v.lock.release()
    #return "succ"

def listener_tcp(v,tcp,ip):
    while True:
        if (int(v.round)>1):
            s = socket(AF_INET, SOCK_STREAM)
            s.connect((ip, int(tcp)))
            #print(ip,tcp)
            break
    while True:


        try:
            msg = s.recv(1024)
            if (msg.decode()!="" and tcp==v.TCP_p):
                if ( v.parent_ID==""):
                    if ('_' in msg.decode("utf-8")):
                        v.parent_ID=msg.decode("utf-8").split('_')[0]
                        v.message_got=msg.decode("utf-8").split('_')[1]
                    else:
                         v.parent_ID=msg.decode("utf-8")
                         v.message_got=msg.decode("utf-8")
                else: v.message_got=msg.decode("utf-8")
                
                if (v.message_got!="done"): Thread(target=write_to_file,args=(v,str(v.TCP_v),)).start()

                # while True:
                #     word=write_to_file(v,tcp)
                #     if (word=="succ"): break
            if (v.Destory_final_tcp==True):
                #print("listener_tcp - break")
                s.close()
                break
        except Exception as e:     print(e, ip,tcp)
  # print("exit from trying \n")


def listener_UDP(v):
    try:
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('', int(v.UDP_v)))
        while True:
            data, addr = s.recvfrom(4096)
            v.round=(data.decode("utf-8"))
            if (v.Destory_final_listen_UDP == True):
                #print("listener_UDP break")
                s.close()
                break
            #if (v.destroy==True): break

    except Exception as e: print(e)

def server_udp(v,msg):
    port=int(v.UDP_master)
    sock_udp = socket(AF_INET, SOCK_DGRAM)
    try:
        sock_udp.connect((v.IP_master, port))
        sock_udp.sendto(str(msg).encode(), (v.IP_master, port))
        sock_udp.close()
    except Exception as e: print("Yarden "+e)

def msg_handle(v,accept):
    sending_color=""
    while True:
        if (sending_color!=v.cpy_color):
            if ((int(v.round)==1 or int(v.round)==2) and v.TCP_p == None) : 
                accept[0].send(bytes(v.ID+ '_' + v.cpy_color, 'utf-8'))
            else: accept[0].send(bytes(v.cpy_color, 'utf-8'))
            sending_color = v.cpy_color
        if (v.Destory_final_tcp==True):
            #print("msg_handle break")
            accept[0].close()
            break



def server_tcp(v):
    counter=0
    while True:
        if (counter>=len(v.v_childs)): 
            #print("server_tcp -break")
            break
        Thread(target=msg_handle,args=(v,v.SERVER_v.accept(),)).start()
        counter+=1
       #print(len(v.v_childs))


def bit_checker(v):
    b=bin(int(v.color,2)^int(v.message_got,2))
    J=""
    for i in range(0, len(b)):
        try:
            if (int(b[i]) == 1):
                j=(len(b) - 1 - i)
        except:
            ""
    return j # is the min location where the colors differ
#101011

def first_round(v):
    while True:
        if (int(v.round)==1):
            msg='next'+'_'+str(v.ID)
            Thread(target=server_tcp , args=(v,)).start()
            Thread(target=server_udp,args=(v,msg,)).start()
            break

def repeat(v):
    #send=False
    while True:

        if (v.TCP_p == None and  int(v.round)>1):
            v.cpy_color=v.color
            v.old_round = v.round
            b=len(str(v.ID))
            while b>3:
                b=math.floor(math.log2(b-1))+2
                v.old_round = v.round
                Thread(target=server_udp,args=(v,'next_'+str(v.ID),)).start()
            v.destroy = True
            break




        # if (v.TCP_p == None and v.old_round!=v.round and int(v.round)>1):
        #     v.cpy_color=v.color
        #     v.old_round=v.round
        #     Thread(target=server_udp,args=(v,'next_'+str(v.ID),)).start()
        #     if (send == False):
        #         for child in v.v_childs:
        #             print ((child[0][0]), child[0][1])
        #             Thread(target=listener_tcp, args=(v, int(child[0][0]), child[0][1])).start()
        #         send = True
        #     rand_child=int(v.v_childs[0][0][0])
        #     if(len(v.childs_color[rand_child])<=3):
        #         v.destroy = True
        #         break


        if (len(v.color)<=3 and v.TCP_p != None  ):
            v.destroy=True
            b=len(str(v.ID))
            counter=0
            while b>3:
                b=math.floor(math.log2(b-1))+2
                counter+=1
            if (int(v.round)<counter+2):
                for i in range(int(v.round),counter+2):
                    v.old_round = v.round
                    Thread(target=server_udp,args=(v,'next_'+str(v.ID),)).start()
            v.destroy = True
            break
            

        elif ( int(v.round)>1 and v.message_got!="" and v.round!=v.old_round and len(v.color)>3):
            j = bit_checker(v)
            i_bit = v.color[-(j + 1)]
            v.color = bin(j) + i_bit
            v.color = v.color[2:]
            v.old_round=v.round
            Thread(target=server_udp,args=(v,'next_'+str(v.ID),)).start()
            while (True):
                if (v.old_round!=v.round):
                    v.cpy_color = v.color
                    break

def shift_down(v):
    while True:
        if(v.round!=v.old_round ):
            v.old_round = v.round
            #v.old_message_got=v.message_got
            if (v.TCP_p is None):
                v.old_color=v.color
                for color in ['00','01','10']:
                    if color==v.old_color: continue
                    else: v.color= color
                Thread(target=server_udp, args=(v, 'next_' + str(v.ID),)).start()
                while (True):
                    if (v.old_round != v.round):
                        v.old_round = v.round
                        v.cpy_color = v.color
                        break
                Thread(target=server_udp, args=(v, 'next_' + str(v.ID),)).start()
                break
                #need to change!!


            else:
                v.old_color=v.color
                v.color=v.old_father
                Thread(target=server_udp, args=(v, 'next_' + str(v.ID),)).start()
                while (True):
                    if (v.old_round != v.round):
                        v.old_round = v.round
                        v.cpy_color = v.color
                        break
                #v.color=v.message_got.split('_')[0]
                Thread(target=server_udp, args=(v, 'next_' + str(v.ID),)).start()
                break



def three_coloring(v):
    while True:
        if v.destroy and len(v.message_got)<=3:
            for x in [7,6,5,4,3]:
                while True:
                    if (v.old_round != v.round ):
                        if (v.TCP_p is not None): v.old_father=v.message_got
                        v.old_color=v.color
                        v.old_round = v.round
                        Thread(target=server_udp, args=(v, 'next_' + str(v.ID),)).start()
                        break
                while (True):
                    if (v.old_round != v.round):
                        v.old_round = v.round
                        v.cpy_color = v.color
                        Thread(target=server_udp, args=(v, 'next_' + str(v.ID),)).start()
                        break
                while (True):
                    if (v.old_round != v.round):
                        shift_down(v)
                        break
                while (True):
                    if (v.old_round != v.round):
                        v.old_round = v.round
                        if (v.TCP_p is not None): v.new_father=v.message_got
                        break
                if(v.color==str(bin(x)[2:])):
                    for color in ['00','01','10']:
                        if (color==v.old_color):continue
                        elif (color == v.new_father): continue
                        else:
                            v.color=color
                            v.cpy_color=v.color
                            break
                if (x!=3) :Thread(target=server_udp, args=(v, 'next_' + str(v.ID),)).start()
                #break
            break

    file_name = 'color_vertex_' + str(v.ID)+'.txt'
    f = open(file_name, 'w')
    f.write(v.color)
    f.close()
    v.Destory_final_tcp = True
    v.cpy_color="done"
    v.old_round=v.round
    v.Destory_final_listen_UDP=True
    Thread(target=server_udp, args=(v, 'next_' + str(v.ID),)).start()
    v.Destory_final = True
    while True:
        if(v.old_round!=v.round):
            Thread(target=server_udp, args=(v, 'done_' + str(v.ID),)).start()
            break
    v.cpy_color="Done!!"




def vertex (ID):
    v=Vertex(ID)
    Thread(target=listener_UDP, args=(v,)).start()
    if (v.TCP_p == None):
        v.color = '00'
        v.cpy_color= '00'
    Thread(target=first_round, args=(v,)).start()
    if (v.TCP_p != None):
        Thread(target=listener_tcp, args=(v,v.TCP_p,v.IP_p)).start()
    Thread(target=repeat, args=(v,)).start()
    Thread(target=three_coloring, args=(v,)).start()






        
        
        
        
    