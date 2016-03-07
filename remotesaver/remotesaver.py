import urllib2
g_qdebug = 0

def main():
    global qgdebug
    dlocation = "/media/pi/Doc/remotesaved"     #default locaiton
    printhelp()
    while 1:
        cmd = raw_input(">>")
        ulistname = "url.list"
        locaiton = dlocation
        if cmd == "exit":
            break
        elif cmd == "help":
            printhelp()
        elif cmd == "read":
            print "read url list from url.list"
            readurls(ulistname,0,locaiton)
        elif cmd == "read auto":
            res =raw_input("This mode will save file based on its name detect from url, continue? (Y/N)")
            if (res=="Y" or res=="y"):
                readurls(ulistname,1,locaiton)
            else: 
                readurls(ulistname,0,locaiton)
        elif len(cmd)>9 and cmd[0:9] == "read from":
            tlen = len(cmd)
            ulistname = cmd[10:tlen]
            print "Read urls from "+ulistname
            readurls(ulistname,0,locaiton)
        elif len(cmd)>14 and cmd[0:14] =="read auto from":
            tlen = len(cmd)
            ulistname = cmd[15:tlen]
            print "read url list from " + ulistname
            res =raw_input("This mode will save file based on its name detect from url, continue? (Y/N)")
            if (res=="Y" or res=="y"):
                readurls(ulistname,1,locaiton)
            else:
                readurls(ulistname,0,locaiton)
        elif len(cmd)>3 and cmd[0:3]=="url":
            fname = "temp.pdf"
            tlen = len(cmd)
            url = cmd[4:tlen]
            if g_qdebug == 1:
                print url
            afname = autoname(url)
            nfname = namefilter(afname,0)
            res = raw_input("Do your like "+nfname+" be your file name?(Y/N)")
            if (res=="Y" or res=="y"):
                fname = nfname
            else:
                fname = raw_input("Name:")
            download_file(url,fname,locaiton)
        else:
            printhelp()

def printhelp():
    print "------------- download file to my pi -------------"
    print "url FILEURLADDRESS          download file from FILEURLADDRESS"
    print "read                        read url from url.list (default) to download files"
    print "read auto                   automatically read url and detect name from url.list. (USER CANNOT CHANGE THE FILE NAME DURING THE DOWNLOAD PROCESS)"
    print "read from FILENAME          read url from FILENAME"
    print "read auto from FILENAME     read url, autoset downlad file name, from FILENAME"
    print "download to DIRECTORY       set the downlaod to directory manully. default is /media/pi/Doc/remotesaved"
    print "help                        show help message"
    print "exit                        end this program"

def readurls(filename,qautoname,location):
    i = 0
    global g_qdebug
    location = ""
    if len(filename) == 0:
        return
    try:
        with open(filename,"r") as urls:
            for url in urls:
                #remove \n
                i = url.find("\n")
                fname = "temp"
                if i>=0:
                    url = url[0:i]
                    if g_qdebug == 1:
                        print "URL is : < "+url+" >"
                afname = autoname(url)
                nfname = namefilter(afname,qautoname)
                if qautoname == 0:
                    res = raw_input("Do your like "+nfname+" be your file name?(Y/N)")
                    if (res=="Y" or res=="y"):
                        fname = nfname
                    elif res == "exit":
                        break
                    else:
                        fname = raw_input("Name:")
                else:
                    fname = nfname
                download_file(url,fname,location)
                i=i+1
        print 'download finished'
    except IOError:
        print "Fail to read file"+ filename
        return


def download_file(url,fname,location):
    if (url and fname):
        response = urllib2.urlopen(url)
        # detect image file : jpg, pnp, etc...
        print "Save "+fname+" from "+url+" to "+location
        file = open(location+fname, 'wb')
        file.write(response.read())
        file.close()
        print("Completed")
    else:
        print("undefined url or file name")

def autoname(url):
    i=0
    global g_qdebug
    while 1:
        i =  url.find("/",i+1)
        if i<0:
            break
        else:
            j=i
    if g_qdebug==1:
        print "Detect name is "+url[j+1:] 
    return url[j+1:]

def namefilter(name,qautoname):
    # 1:replace %20 to _
    global g_qdebug
    if name.find("%20")>0:
        oldname = name
        if g_qdebug == 1:
            print "Old name is: "+oldname
        newname = name.replace("%20","_")
        if qautoname == 0:
            res = raw_input("Would you like to keep "+newname+"(Y/N)")
            if (res=="Y" or res=="y"):
                return newname
            else:
                return oldname
        else:
            return newname
    else:
        return name

if __name__ == "__main__":
    main()


