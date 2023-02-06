# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 16:27:57 2023

@author: zelul
"""
import os
import sys
import socket
import argparse
import threading
from datetime import datetime

HOST = '127.0.0.1' # LOCALHOST

def msgProcess(msg,dic):
    msgList = msg.split('\r\n')
    firstLine = msgList[0].split(' ')
    method = firstLine[0]
    if firstLine[1] == '/':
        path = os.path.join(dic ,'index.html')
    else:
        path = dic
        for p in firstLine[1].split('/'):
            path = os.path.join(path ,p)
    print(path)
    
    if method != 'GET':
        return sendResponse('403 Forbidden', 'text/html', 
        "<h1><b>HTTP 403 Forbidden</b></h1>")
    elif os.path.isfile(path):
        type = path.split('.')[-1]
        if type == 'html':
            fy = 'text/html'
        elif type in ['png','jpg']:
            fy = 'image/png'
        elif type == 'xml':
            fy = 'text/xml'
        else:
            fy = '*/*'
        fb = open(path,'rb').read()
        return sendResponse('200 OK',fy,bytes(fb))
    else:
        return sendResponse('404 Not Found', 'text/html',
        "<h1><b>HTTP 404 Not Found</b></h1>")
    

def sendResponse(status_code,contentType,content):
    response = "HTTP/1.1 " + status_code + '\r\n'
    response += 'Content-Type: ' + contentType + '\r\n'
    response += 'ContentLength: '+ str(len(content)) + '\r\n'
    response += 'Date: ' + str(datetime.now()) + '\r\n\r\n'
    if type(content) == 'str':
        response += content
    response = bytes(response,'utf-8')

    if len(response) + len(content) > 1024:
        n=len(content)
        response_list = [response + content[:1024-len(response)]]
        i=1024-len(response)
        while i<n:
            response_list.append(content[i:min(i+1024,n)])
            i+=1024
        return response_list
    else:
        return [response]


def deal(sock,addr,dic):
    print('Connected by '+ str(addr))
    try:
        data = sock.recv(1024).decode("utf-8")
        response = msgProcess(data, dic)
    except:
        print(sock.recv(1024).decode("utf-8"))
        response = sendResponse('400 Bad Request', 'text/html',
        "<h1><b>HTTP 400 Bad Request</b></h1>")
    for rep in response:
        sock.sendall(rep)
    sock.close()
    print('Loss connect with' + str(addr))
    return


def main(dic,port):
    # server_stream: TCP protocal, AF_INET: IPV4
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST,port))
    server.listen()
    while True:
        try:
            sock,addr = server.accept()
            xd = threading.Thread(target=deal, args=(sock,addr,dic))
            xd.start()
        except:
            print('Connection error!')
    return


if __name__ == '__main__':
    sys.path.append("C:\Application\Anaconda\Lib\site-packages")
    parser = argparse.ArgumentParser()
    parser.add_argument('-document_root', type = str, help = 
                        'the directory which the webserver uses to server files, must be absolute paths',
                        required = True)
    parser.add_argument('-port', type = int, help = 
                        'the port that the server listens on', default= 8080)
    args = parser.parse_args()
    main(args.document_root,args.port)