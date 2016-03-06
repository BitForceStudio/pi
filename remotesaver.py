import urllib2

def main():
    qdbg = 1
    printhelp()
    while 1:
        cmd = raw_input(">>")
        ulistname = "url.list"
        if cmd == "exit":
            break
        elif cmd == "help":
            printhelp()
        elif cmd == "read":
            print "read url list from url.list"
            readurls(ulistname,0)
        elif cmd == "read auto":
            res =raw_input("This mode will save file based on its name detect from url, continue? (Y/N)")
            if (res=="Y" or res=="y"):
                readurls(ulistname,1)
            else: 
                readurls(ulistname,0)
        elif len(cmd)>9 and cmd[0:9] == "read from":
            tlen = len(cmd)
            ulistname = cmd[10:tlen]
            print "Read urls from "+ulistname
            readurls(ulistname,0)
        elif len(cmd)>14 and cmd[0:14] =="read auto from":
            tlen = len(cmd)
            ulistname = cmd[15:tlen]
            print "read url list from " + ulistname
            res =raw_input("This mode will save file based on its name detect from url, continue? (Y/N)")
            if (res=="Y" or res=="y"):
                readurls(ulistname,1)
            else:
                readurls(ulistname,0)
        elif len(cmd)>3 and cmd[0:3]=="url":
            fname = "temp.pdf"
            tlen = len(cmd)
            url = cmd[4:tlen]
            if qdbg == 1:
                print url
            afname = autoname(url)
            nfname = namefilter(afname,0)
            res = raw_input("Do your like "+nfname+" be your file name?(Y/N)")
            if (res=="Y" or res=="y"):
                fname = nfname
            else:
                fname = raw_input("Name:")
            download_file(url,fname)
        else:
            printhelp()

def printhelp():
    print "-------------input file url to download file-------------"
    print "url FILEURLADDRESS          download file from FILEURLADDRESS"
    print "read                        read url from url.list (default) to download files"
    print "read auto                   automatically read url and detect name from url.list. (USER CANNOT CHANGE THE FILE NAME DURING THE DOWNLOAD PROCESS)"
    print "read from FILENAME          read url from FILENAME"
    print "read auto from FILENAME     read url, autoset downlad file name, from FILENAME"
    print "help                        show help message"
    print "exit                        end this program"

def readurls(filename,qautoname):
    i = 0
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
                download_file(url,fname)
                i=i+1
        print 'download finished'
    except IOError:
        print "Fail to read file"+ filename
        return


def download_file(url,fname):
    if (url and fname):
        response = urllib2.urlopen(url)
        # detect image file : jpg, pnp, etc...
        nend = len(fname)
        if (fname[nend-3:nend] == "jpg" or fname[nend-3:nend]== "png"):
            print "Save "+fname+" from "+url+" to "+"/var/www/html/pickbits/images"
            imagefile = open("/var/www/html/pickbits/images/"+fname, 'wb')
            imagefile.write(response.read())
            imagefile.close()
        else:
            print "Save "+fname+" from "+url+" to "+"/media/pi/Doc/remotesaved/"
            file = open("/media/pi/Doc/remotesaved/"+fname, 'wb')
            file.write(response.read())
            file.close()
        print("Completed")
    else:
        print("undefined url or file name")

def autoname(url):
    i=0
    loc=0
    while 1:
        i =  url.find("/",i+1)
        if i<0:
            break
        else:
            j=i
    return url[j+1:]

def namefilter(name,qautoname):
    # 1:replace %20 to _
    if name.find("%20")>0:
        oldname = name
        if qautoname == 0:
            print "Old name is: "+oldname
            newname = name.replace("%20","_")
            res = raw_input("Would you like to keep "+newname+"(Y/N)")
            if (res=="Y" or res=="y"):
                return newname
            else:
                return oldname
        else:
            newname = name.replace("%20","_")
            return newname
    else:
        return name

if __name__ == "__main__":
    main()


