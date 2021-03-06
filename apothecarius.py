#!/usr/bin/python2

#######################################
## Apothecarius v0a1
##  under construction! by miefda
##  miefda@miefda.de
#######################################
import sys, os, time, subprocess, random, MySQLdb
drucker = ""
dbhost = "miefda.de" 
dbuser = "lager"
dbpasswort = "884001"
dbase = "testdb"

## creats a checksum
def quersum(x):
    y = 0
    for i in str(x):
        y += int(i)
    if y > 9:
        y = quersum(y)
    return y

## returns random in with 8 digits
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
    #img = subprocess.os.popen("convert out.png -gravity East -background White -splice 300x0 -pointsize 25  -annotate +10+0 '" + nick + "' out.png")
    img = subprocess.os.popen("convert out.png   -background white -fill black -pointsize 20  label:'" + nick  + "'  -gravity Center -append out.png")
    img.close()
    print("adding date to barcode")
    img = subprocess.os.popen("convert out.png   -background black -fill white  label:'" + time.asctime() + "' +swap  -gravity Center -append out.png")
    img.close()
    print("viewing barcode")
    qiv = subprocess.os.popen("qiv out.png")
    time.sleep(10)
    qiv = subprocess.os.popen("killall qiv")


## function to create inital dv
def create_db():
    conn = MySQLdb.connect(dbhost, dbuser, dbpasswort, dbase)
    db = conn.cursor()
    sql = '''create table users(nick text, ownerid double, password text,  unique(Ownerid))'''
    db.execute(sql)
    conn.commit()
    sql = '''create table box(name text, info text, ownerid double, boxid double, UNIQUE(boxid))'''
    db.execute(sql) 
    conn.commit()
    sql = '''create table items(name text, info text, boxid double, itemid double, UNIQUE(itemid))'''
    db.execute(sql)
    conn.commit()
    db.close()

## function to add user

def adduser(nick):
    conn = MySQLdb.connect(dbhost, dbuser, dbpasswort, dbase)
    db = conn.cursor()
    sql = "select * from users where nick='" + nick + "'"
    db.execute(sql)
    for i in db:
        if len(i) != 0:
            return -1
    tupel = [nick, randxdig(13, 1)]
    db.execute("INSERT INTO users(nick, ownerid) VALUES ('" + tupel[0] + "'," + tupel[1] + ")")
    conn.commit()
    db.close()
    return tupel

## function to add box
def addbox(ownerid, boxname):
    
    if len(boxname) == 0:
        boxname = time.asctime()
    
    conn = MySQLdb.connect(dbhost, dbuser, dbpasswort, dbase)
    db = conn.cursor()
    sql = 'select nick from users where ownerid="' + ownerid + '"'
    db.execute(sql)
    conn.commit()
    for i in db:
         nick = i[0]
    tupel = [randxdig(13, 2), str(nick), boxname]
    sql = 'insert into box(name, ownerid, boxid) values("' + boxname + '",'+ ownerid + ',' + tupel[0] +' )'
    db.execute(sql)
    conn.commit()
    db.close()
    return tupel

def additem(boxid, itemname):
    
    if len(itemname) == 0:
       itemname = time.asctime()
     
    conn = MySQLdb.connect(dbhost, dbuser, dbpasswort, dbase)
    db = conn.cursor()
    sql = 'select name from box where boxid="' + boxid + '"'
    db.execute(sql)
    conn.commit()
    for i in db:
         name = i[0]
    tupel = [randxdig(13, 3), str(name), itemname]
    sql = 'insert into items(name, boxid, itemid) values("' + itemname + '",'+ boxid + ',' + tupel[0] +' )'
    db.execute(sql)
    conn.commit()
    db.close()
    return tupel






def showusers():
    conn = MySQLdb.connect(dbhost, dbuser, dbpasswort, dbase)
    db = conn.cursor()
    db.execute('select nick, ownerid from users')
    for users in db:
        print(users[0] + " " + str(int(users[1])))
    db.close()

## program start!
try:
    create_db()
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
        if len(user) < 11:
            idcode = adduser(user)
            if idcode == -1:
                print("user exitsts!\n")
            else:
                createbarcode(idcode[1], user)    
                hardcopy("user and barcode would get printed now","")
                print("\n")
        else:
            print("max length = 10\n")
    elif len(shell) == 13:
        # quersummen check
        if  int(quersum(shell[:12])) == int(shell[12]):
            ## if ownerd is entered, box aadding get initiated xD
            if int(shell[0]) == 1:
                boxname = raw_input("Please enter Boxname:")
                box = addbox(shell, boxname)
                print(box)
                createbarcode(box[0], box[1] + "_" + box[2])
                #hardcopy(box)

            if int(shell[0]) == 2:
                itemname = raw_input("Please enter Itemname:")
                item = additem(shell, itemname)
                print(item)
                createbarcode(item[0], item[0] + "_" + item[2])


                print("\n")
        else: 
            print("invalid number!")
