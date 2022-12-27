from pyrogram import Client, filters
import MoodleClient
from time import time, localtime
import info
from zipfile import ZipFile , ZipInfo 
import multiFile
import os
import zipfile
import S5Crypto
import socket
import datetime
import time

#Conectar bot con el cliente
app = Client(
"bot",
api_id="12729863", #Ingresa tu api_id
api_hash="ebb09446c3def9fc6c69f1a10e1252a0", #Ingresa tu api_hash
bot_token="5965546694:AAE-VfOcsFkuCe_CA7A3rpmYh2OQFleDYDk") #Ingresa el token de tu bot
 
####Configuración de todos los usuarios###$
UserCollection = {'JAGB2021'}

sec = 0
def progress_dl(current, total, msg, app):
    global sec
    if sec != localtime().tm_sec:
        try: msg.edit_text(f'📥Descargando📥\n\n💯Porcentaje: {current * 100 / total:.1f}%\n📂Total: {round(total / 1000000,2)}MB\n📥Descargado: {round(current / 1000000,2)}MB\n')
        
        except: pass
    sec = localtime().tm_sec 
    
    
#####Obtener Tamaño de archivo en kb####
def get_file_size(file):
    file_size = os.stat(file)
    return file_size.st_size

####Comprimir####
def Compress(file,msg,username):
    global UserCollection
    getUser = UserCollection[username]
    file_size = get_file_size(file)
    file_size_max = 1024 * 1024 * getUser['zips']
    user = getUser['user']
    passw = getUser['passw']
    host = getUser['host']
    repo = getUser['repo']
    userid = getUser['userid']    
    if file_size > file_size_max:
        msg.edit_text('🗜️Comprimiendo🗜️')
        mult_file =  multiFile.MultiFile(file+'.7z',file_size_max)
        zip = ZipFile(mult_file,  mode='w', compression=zipfile.ZIP_DEFLATED)
        zip.write(file)
        zip.close()
        mult_file.close()
        data = []
        for f in multiFile.files:
            moodle = MoodleClient.Client(user,passw,host,repo,userid)
            loged = moodle.login()
            if loged == True:
                msg.edit_text('⚡Subiendo⚡\n👉'+f)
                resp = moodle.upload_file(f)
                link=str(resp).replace('\\','')
                separator = '\n'
                data.append(link+separator)
            msg.edit_text('⚡Subida finalizada⚡\n\n'+str(data))
    else:
        Upload(file,msg,username)
        
#Subir un solo archivo
def Upload(file,msg,username):
    global UserCollection
    getUser = UserCollection[username]
    user = getUser['user']
    passw = getUser['passw']
    host = getUser['host']
    repo = getUser['repo']
    userid = getUser['userid']
    msg.edit_text('🔑Logueandose')
    moodle = MoodleClient.Client(user,passw,host,repo,userid)
    loged = moodle.login()
    if loged == True:
        msg.edit_text('⚡Subiendo⚡\n👉'+file)
        resp = moodle.upload_file(file)
        data=str(resp).replace('\\','')
        msg.edit_text('⚡Subida finalizada⚡\n\n'+data)

####Detectar y descargar si mandan archivos al bot####
@app.on_message(filters.document | filters.video | filters.audio | filters.photo)
def download(client, message):
	
    username = message.from_user.username
    root = './'+username+'/'
	
    msg = message.reply("📥Descargando📥")
    file_name = root
    file = app.download_media(message, file_name, progress=progress_dl, progress_args=(msg, app))
    msg.edit_text("📥Descarga finalizada📥")
    Compress(file,msg,username)

####Comandos####
@app.on_message()
def commands(client, message):
    global UserCollection
    text = message.text
    username = message.from_user.username

    if '/start' in text:
        UserCollection[username] =
        msg_start = f'🔰Bienvenido {username}'
        message.reply(msg_start)
        
    if '/acc' in text:
        getUser = UserCollection[username]
        user = text.split(' ')[1]
        passw = text.split(' ')[2]
        getUser['user'] = user
        getUser['passw'] = passw
        statinfo = info.stat(getUser)
        message.reply(statinfo)

    if '/host' in text:
        getUser = UserCollection[username]
        host = text.split(' ')[1]
        getUser['host'] = host
        statinfo = info.stat(getUser)
        message.reply(statinfo)

    if '/repo' in text:
        getUser = UserCollection[username]
        repo = int(text.split(' ')[1])
        getUser['repo'] = repo
        statinfo = info.stat(getUser)
        message.reply(statinfo)
        
    if '/userid' in text:
        getUser = UserCollection[username]
        userid = text.split(' ')[1]
        getUser['userid'] = userid
        statinfo = info.stat(getUser)
        message.reply(statinfo)

    if '/myuser' in text:
        getUser = UserCollection[username]
        statinfo = info.stat(getUser)
        message.reply(statinfo)

    if '/zips' in text:
        getUser = UserCollection[username]
        zips = int(text.split(' ')[1])
        getUser['zips'] = zips
        statinfo = info.stat(getUser)
        message.reply(statinfo)

    if '/crypt' in text:
        proxy_sms = str(text).split(' ')[1]
        proxy = S5Crypto.encrypt(f'{proxy_sms}')
        message.reply(f'🛰️Proxy encryptado:\n{proxy}')

    if '/decrypt' in text:
        proxy_sms = str(text).split(' ')[1]
        proxy_de = S5Crypto.decrypt(f'{proxy_sms}')
        message.reply(f'🛰️Proxy decryptado:\n{proxy_de}')


print('👾Bot Online👾')
app.run()
