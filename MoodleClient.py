from re import escape
from typing import Counter
import requests
import os
import json
import traceback
from bs4 import BeautifulSoup

class Client(object):
    def __init__(self, user, passw, host,repo,userid):
        self.username = user
        self.password = passw
        self.host = host
        self.repo = repo
        self.userid = userid
        self.session = requests.Session()

    def login(self):
        login = self.host+'/login/index.php'
        resp = self.session.get(login)
        soup = BeautifulSoup(resp.text, 'html.parser')
        logintoken = soup.find('input', attrs={'name':'logintoken'})['value']
        username = self.username
        password = self.password
        payload = {'anchor':'', 'logintoken': logintoken, 'username': username, 'password': password}
        resp2 = self.session.post(login, data=payload)
        counter = 0
        for i in resp2.text.splitlines():
            if 'loginerrors' in i or (0 < counter <=3):
                counter += 1
                print(i)
        if counter > 0:
            return False
        else:
            return True
    
    def upload_file(self, file):
        try:
            fileurl = f'{self.host}/user/edit.php?id={self.userid}&returnto=profile'
            resp = self.session.get(fileurl)
            soup = BeautifulSoup(resp.text, 'html.parser')
            sesskey = soup.find('input', attrs={'name':'sesskey'})['value']
            submitbutton = soup.find('input', attrs={'name':'submitbutton'})['value']
            usertext = soup.find('span', attrs={'class':'usertext mr-1'})
            query = self.extractQuery(soup.find('object', attrs={'type':'text/html'})['data'])
            client_id = self.getclientid(resp.text)
            try:
                of = open(file, 'rb')
                print('Subiendo....')
            except:
                print('Fallo al leer el archivo')    
            upload_file = {
                'repo_upload_file':(file,of,'image/jpeg'),

            }
            upload_data = {
                'title':(None,''), 'author':(None, usertext),
                'license':(None, 'cc-nc-sa'),
                'itemid': (None, query['itemid']),
                'repo_id': (None,self.repo),
                'p':(None, ''),
                'Content-Type':'image/jpeg',
                'page': (None, ''),
                'env': (None, query['env']),
                'sesskey': (None, sesskey),
                'client_id':(None, client_id),
                'maxbytes':(None, query['maxbytes']),
                'areamaxbytes': (None, query['areamaxbytes']),
                'ctx_id': (None, query['ctx_id']),
                'savepath': (None, '/')
            }
            post_file_url = f'{self.host}/repository/repository_ajax.php?action=upload'
            resp2 = self.session.post(post_file_url, files=upload_file, data=upload_data)
            print(resp2.text)
            of.close()
            
            try:
                data = self.parsejson(resp2.text)['url'] 
            except:
                data=resp2.text[0]    
            payload = {
                'returnurl': fileurl,
                'sesskey': sesskey,
                '_qf__user_files_form': '.jpg',
                #'files_filemanager': files_filemanager,
                'submitbutton': 'Guardar+cambios'
            }
            resp3 = self.session.post(fileurl, data = payload)
            
            return data
        except Exception as e:
            print(traceback.format_exc())    

    def getSpaceData(self):
        try:
            urlfiles = f'{self.host}/user/edit.php?id={self.userid}&returnto=profile'
            resp = self.session.get(urlfiles)
            soup = BeautifulSoup(resp.text,'html.parser')
            availabledata = soup.find('div',attrs={'data-aria-autofocus':'true'})
            if availabledata:
                data = availabledata.contents[2].replace('\n','').split(' ')
                current = data[8]
                if 'KB' in current:
                    current = int(str(current).replace('KB',''))
                if 'MB' in current:
                    current = int(str(current).replace('MB','')) * (1024 * 1024)
                if 'GB' in current:
                    current = int(str(current).replace('GB','')) * (1024 * 1024 * 1024)
                max = 1024 * 1014 * 1024 * 2
                available = int(max - current)
                return {'actual':current,'max':max,'available':available}
            else:
                max = 1024 * 1014 * 1024 * 2
                return {'actual':0,'max':max,'available':max}
        except Exception as ex:
                max = 1024 * 1014 * 1024 * 2
                return {'actual':0,'max':max,'available':max}
                
    def parsejson(self, json):
        try:
            data = {}
            tokens = str(json).replace('{', '').replace('}', '').split(',')
            for t in tokens:
                split = str(t).split(':', 1)
                data[str(split[0]).replace('"', '')]= str(split[1]).replace('"', '')
            return data
        except:
            print(traceback.format_exc(),'parsejson errror!!')
            return json    

    def getclientid(self, html):
        index = str(html).index('client_id')
        max = 25
        ret = html[index:(index+max)]
        return str(ret).replace('client_id":"','')

    def extractQuery(self, url):
        tokens = str(url).split('?')[1].split('&')
        retQuery = {}
        for q in tokens:
            qsp1 = q.split('=')
            retQuery[qsp1[0]] = qsp1[1]
        return retQuery