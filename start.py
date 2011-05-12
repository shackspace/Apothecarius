#!/usr/bin/python2
import sys, os, time, subprocess, random, sqlite3
dbdir   = "./lager_db"
drucker = "shack"

## returns random in with 8 digits
def randxdig(x):
    dig = ""
    for i in range(x):
        dig += str(random.randint(1,9))
    return dig;

## print function

def hardcopy(txt, drucker):
    txt = "echo -e '" + txt + "' |lpr -P " + drucker
    #hardcopy = subprocess.popen(txt)
    print(txt)

## creates and shows a barcode!

def createbarcode(number, nick):
    zint = subprocess.os.popen("zint -d " + str(number) + " -o o")
    img = subprocess.os.popen("convert out.png -gravity East -background White -splice 300x0 -pointsize 50  -annotate +10+0 '" + nick + "' out.png")
    img.close()
    img = subprocess.os.popen("convert out.png   -background black -fill white  label:'" + time.asctime() + "' +swap  -gravity Center -append " + nick + "_" + number + ".png")
    img.close()
    qiv = subprocess.os.popen("qiv " + nick + "_" + number + ".png")
    time.sleep(3)
    qiv = subprocess.os.popen("killall qiv")


## function to create inital dv
def create_db(dbdir):
        conn = sqlite3.connect(dbdir)
        db = conn.cursor()
        db.execute('''create table users(nick text, id int)''')
        conn.commit()
        db.close()

## function to add user

def adduser(nick):
    conn = sqlite3.connect("./lager_db")
    db = conn.cursor()
    db.execute('select * from users where nick="' + nick + '"')
    for i in db:
        if len(i) != 0:
            return -1
    tupel = [nick, randxdig(8)]
    db.execute('insert into users values(?, ?)', tupel)
    conn.commit()
    db.close()
    return tupel

## function to list all users in database

def showusers():
    conn = sqlite3.connect("./lager_db")
    db = conn.cursor()
    db.execute('select * from users')
    for users in db:
        for i in range(len(users)):
            print(users[i])
    db.close()

## program start!
try:
    create_db(dbdir)
except:
    pass
while True:
    print("input 0 to show print all users in db")
    print("input 1 to add a new user")

    shell = raw_input("input: ")
    if shell == "0":
        showusers()

    elif shell == "1":
        user = raw_input("username: ")
        idcode = adduser(user)
        if idcode == -1:
            print("user exitsts!\n")
        else:
            createbarcode(idcode[1], user)    
            hardcopy("user and barcode would get printed now","")
            print("\n")
    
