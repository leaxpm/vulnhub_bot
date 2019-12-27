import requests
from bs4 import BeautifulSoup
import os
from winreg import HKEY_CURRENT_USER, OpenKey, QueryValueEx
import logging
import telegram
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.error import NetworkError, Unauthorized

print("####_New VM's on Vulnhub_####")
print("By Leax")

r = requests.get("https://www.vulnhub.com/") #Convert Url To Text
data = r.text
soup= BeautifulSoup(data,features="html.parser")

#Download Links
vmnames = []
def search():
    i = 0
    message = ""
    for link in soup.find_all('h1'):
        for a in link.find_all('a'):
            #New VM's
            vmnames.append(a.text)
            #print("#"+str(i+1)+": "+a.text+"\n")
            message = message + "#"+str(i+1)+": "+a.text+"\n"
            i += 1
            
    return message


def downloader(): 
#Download Menu
    download = []
    for link in soup.find_all('div', {'class':'modal hide fade'}):
        #Inside the description 
        #print(link.text)
        for div in link.find_all('div', {'class':'modal-body'}):
            #Down on download links
            #print(div.text)
            for bhref in div.find_all('b', text="Download (Mirror)"):
                #Download Link Mirror
                a = bhref.nextSibling
                a = a.nextSibling
                #print(a.get('href'))
                download.append(a.get('href'))

    with OpenKey(HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
        Downloads = QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]

    vm = int(input("Will you like to download one?: "))
    vm -= 1
    linkdw = download[vm]

    try:
        Downloads = Downloads.replace("\\"," ")
        Downloads= Downloads.replace(" ","/")
        ext = str(linkdw)
        ext = ext.split(".")[3]
        namefile = (str(vmnames[vm])+"."+ext)
    #Print File Name
        print("\n"+namefile)
        namefile = namefile.replace(" ","")
        namefile = namefile.replace(":","")
        output= Downloads +"/"+ namefile
        print(output)
        os.system("curl -o "+ output +" "+str(linkdw))
        print("Ready, Have Fun!!!")
    except:
        Downloads = Downloads.replace("\\"," ")
        Downloads = Downloads.replace(" ","/")
        ext = str(linkdw)
        ext = ext.split(".")[3]
        namefile = (str(vmnames[vm])+"."+ext)
        namefile = namefile.replace(" ","")
        namefile = namefile.replace(":","")
        output= Downloads +"/"+ namefile
        os.system("curl -o "+ output+" "+str(linkdw))
        print("Ready, Have Fun!!!")


def news(bot, update):
    #Telegram Bot VM's
    text = search()
    #print(message)
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id,text=text)


def help(bot,update):
    #Telegram Bot Help
    text = "/help - See All Commands \n /news - New VM's"
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id,text=text)


def main():
    updater = Updater('TOKEN_API')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('news',news))
    dp.add_handler(CommandHandler('help',help))
    updater.start_polling()
    updater.idle()
    

if __name__ == "__main__":
    main()
    pass

#WebScrapping 
#System Commands