#!/usr/bin/python2
import sys, os, time, subprocess, random, MySQLdb
drucker = ""
dbhost = "" 
dbuser = ""
dbpasswort = ""
dbase = "testdb"
## returns random in with 8 digits

def quersum(x):
    y = 0
    for i in str(x):
        y += int(i)
    if y > 9:
        y = quersum(y)
    return y

def randxdig(x, y):
    dig = str(y)
    
    for i in range(int(x) - 2):
        dig += str(random.randint(1,9))
    dig += str(quersum(dig))
    return dig;
    


## print function
def hardcopy(txt, drucker):

    txt = "echo -e '" + txt + "' |lpr -P " + drucker
    #hardcopy = subprocess.popen(txt)
    print(txt)

## creates and shows a barcode!

def createbarcode(number, nick):
    print("generating barcode")
    zint = subprocess.os.popen("zint -d " + str(number) + " -o o")
    zint.close()
    print("adding nickname to barcode")
    img = subprocess.os.popen("convert out.png -gravity East -background White -splice 300x0 -pointsize 50  -annotate +10+0 '" + nick + "' out.png")
    img.close()
    print("adding date to barcode")
    img = subprocess.os.popen("convert out.png   -background black -fill white  label:'" + time.asctime() + "' +swap  -gravity Center -append " + nick + "_" + number + ".png")
    img.close()
    print("viewing barcode")
    qiv = subprocess.os.popen("qiv " + nick + "_" + number + ".png")
    time.sleep(10)
    qiv = subprocess.os.popen("killall qiv")


## function to create inital dv
def create_db():
    conn = MySQLdb.connect(dbhost, dbuser, dbpasswort, dbase)
    db = conn.cursor()
    sql = '''create table users(nick text, ownerid unique)'''
    db.execute(sql)
    conn.commit()
    sql = '''create table box(name text, info text, ownerid int, boxid unique)'''
    db.execute(sql) 
    conn.commit()
    sql = '''create table items(name text, info text, boxid int, itemid unique)'''
    db.execute(sql)
    conn.commit()
    db.close()

## function to add user

def adduser(nick):
    conn = MySQLdb.connect(dbhost, dbuser, dbpasswort, dbase)
    db = conn.cursor()
    sql = 'select * from users where nick="' + nick + '"'
    db.execute(sql)
    for i in db:
        if len(i) != 0:
            return -1
    sql = 'insert into users value(' + nick + ',' + randxdig(13, 1)
    db.execute(sql)
    conn.commit()
    db.close()
    return tupel

## function to add box
def addbox(ownerid):
    conn = MySQLd.connect(dbhost, dbuser, dbpasswort, dbase)
    db = conn.cursor()
    sql = 'select nick from users where ownerid="' + ownerid + '"'
    db.execute(sql)
    conn.commit()
    for i in db:
         nick = i[0]
    sql = 'insert into box(ownerid, boxid) values('+ ownerid + ',' + randxdig(13,2) +' )'
    db.execute(sql)
    conn.commit()
    db.close()
    tupel = [randxdig(13, 2), str(nick)]
    return tupel

## function to list all users in database

def showusers():
    conn = MySQLdb.connect(dbhost, dbuser, dbpasswort, dbase)
    db = conn.cursor()
    db.execute('select * from users')
    for users in db:
        for i in range(len(users)):
            print(users[i])
    db.close()

## program start!
try:
    print(" not found! creating..\n\n\n")
except:
    print(" found! using it.. \n\n\n")

while True:
    print("input 0 to show print all users in db")
    print("input 1 to add a new user")

    shell = raw_input("input: ")
    if shell == "0":
        showusers()

    elif shell == "1":
        user = raw_input("username: ")
        if len(user) < 8:
            idcode = adduser(user)
            if idcode == -1:
                print("user exitsts!\n")
            else:
                createbarcode(idcode[1], user)    
                hardcopy("user and barcode would get printed now","")
                print("\n")
        else:
            print("max length = 7\n")
    elif len(shell) == 13:
        # quersummen check
        if  int(quersum(shell[:12])) == int(shell[12]):
            if int(shell[0]) == 1:
                box = addbox(shell)
                print(box)
                createbarcode(box[0], "box." + box[1])
                #hardcopy(box)
                print("\n")
        else: 
            print("invalid number!")
