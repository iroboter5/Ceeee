def stat(getUser):
    msg = '👤User: '+getUser['user']+'\n'
    msg +='🔑Passw: '+getUser['passw']+'\n'
    msg +='🌐Host: '+getUser['host']+'\n'
    msg +='🔵Repo: '+str(getUser['repo'])+'\n'
    msg +='🗜️Zips: '+str(getUser['zips'])+'\n'
    msg +='🔰Userid: '+getUser['userid']
    return msg