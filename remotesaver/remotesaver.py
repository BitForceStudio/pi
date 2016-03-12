import urllib2
import pdfkit

g_qdebug = 0
g_skeyword=["url",              # -- 0
            "read",             # -- 1
            "read auto",        # -- 2
            "read from",        # -- 3
            "read auto from",   # -- 4
            "download to",      # -- 5
            "html",             # -- 6
            "help",             # -- 7
            "exit"]             # -- 8

def main():
    global qgdebug
    global g_skeyword
    dlocation = "/media/pi/Doc/remotesaved/"     #default locaiton
    printhelp()

    while 1:
        cmd = raw_input(">>")
        returncmd = start(cmd,dlocation,0)
        if returncmd == "exit":
            break;
        elif len(returncmd)>0:
            dlocation = returncmd

def start(cmd,location,qautoname):
    global qgdebug
    global g_skeyword

    ulistname = "url.list"
    dlocation = location
    returncmd = ""
    if   cmd ==                                   g_skeyword[8]:                                        # exit
        returncmd = "exit"
    elif cmd ==                                   g_skeyword[7]:                                        # help
        printhelp()
    elif cmd ==                                   g_skeyword[1]:                                        # read                
        print "read url list from url.list"
        readurls(ulistname,0,dlocation)
    elif cmd ==                                   g_skeyword[2]:                                        # read auto
        res =raw_input("This mode will save file based on its name detect from url, continue? (Y/N)")
        if (res=="Y" or res=="y"):
            readurls(ulistname,1,dlocation)
        else: 
            readurls(ulistname,0,dlocation)
    elif len(cmd)>9 and cmd[0:9] ==               g_skeyword[3]:                                        # read from
        tlen = len(cmd)
        ulistname = cmd[10:tlen]
        print "Read urls from "+ulistname
        readurls(ulistname,0,dlocation)
    elif len(cmd)>14 and cmd[0:14] ==             g_skeyword[4]:                                        # read from auto
        tlen = len(cmd)
        ulistname = cmd[15:tlen]
        print "read url list from " + ulistname
        res =raw_input("This mode will save file based on its name detect from url, continue? (Y/N)")
        if (res=="Y" or res=="y"):
            readurls(ulistname,1,dlocation)
        else:
            readurls(ulistname,0,dlocation)
    elif len(cmd)>11 and cmd[0:11]==              g_skeyword[5]:                                        # download to
        tlen = len(cmd)
        returncmd = cmd[12:tlen]
        if g_qdebug == 1:
            print "Global saving direction saved to "+dlocation
    elif len(cmd)>4 and cmd[0:4]==                g_skeyword[6]:                                        # html
        fname = "temp.pdf"
        print "Save html to pdf file"
        tlen = len(cmd)
        url = cmd[5:tlen]
        if g_qdebug == 1:
            print url
        fname = getname(url)
        if len(fname)==0:
            fname = raw_input("Input file name:")
        else:
            rname = url.find(" -> ")
            url = url[0:rname]

        nlen = len(fname)
        if nlen>4 and fname[nlen-4:nlen]==".pdf":
            fname = fname
        else:
            fname = fname+".pdf"
        if g_qdebug:
            print fname
        download_html_to_pdf(url,fname,dlocation)
    elif len(cmd)>3 and cmd[0:3]==                g_skeyword[0]:                                        # url
        fname = "temp.pdf"
        tlen = len(cmd)
        url = cmd[4:tlen]
        if g_qdebug == 1:
            print url

        fname = getname(url)
        if len(fname)==0:
            afname = autoname(url)
            nfname = namefilter(afname,0)

            if qautoname == 0:
                res = raw_input("Do your like "+nfname+" be your file name?(Y/N)")
                if (res=="Y" or res=="y"):
                    fname = nfname
                else:
                    fname = raw_input("Name:")
            else:
                fname = nfname
        
        rname = url.find(" -> ")
        if rname>0:
            url = url[0:rname]

        if g_qdebug==1:
            print url +"  --  "+fname
        download_file(url,fname,dlocation)
    else:
        printhelp()

    return returncmd

def printhelp():
    print "------------- download file to my pi -------------"
    print "url FILEURLADDRESS          download file from FILEURLADDRESS"
    print "read                        read url from url.list (default) to download files"
    print "read auto                   automatically read url and detect name from url.list. (USER CANNOT CHANGE THE FILE NAME DURING THE DOWNLOAD PROCESS)"
    print "read from FILENAME          read url from FILENAME"
    print "read auto from FILENAME     read url, autoset downlad file name, from FILENAME"
    print "download to DIRECTORY       set the downlaod to directory manully. default is /media/pi/Doc/remotesaved"
    print "html                        save html to pdf file"
    print "help                        show help message"
    print "exit                        end this program"

def readurls(filename,qautoname,location):
    global g_qdebug
    dlocation = location
    inbox = 0

    if len(filename) == 0:
        return
    try:
        with open(filename,"r") as urls:
            for line in urls:
                #remove \n
                i = line.find("\n")
                fname = "temp"
                if i>0:
                    line = line[0:i]
                    if g_qdebug==1:
                        print line
                else:
                    if g_qdebug==1:
                        print "empty line"
                    continue
                # read line and find out the command
                llen = len(line)

                if inbox == 0: 
                    if llen>12 and line[0:11]=="download to":
                        dlocation = line[12:llen]
                    elif llen>=4  and line[0:4] == "auto":
                        if g_qdebug == 1:
                            print "read "+filename+" save to "+dlocation+" automatically"
                        inbox = 1
                    elif llen>=5  and line[0:5] == "manul":
                        if g_qdebug == 1:
                            print "read "+filename+" save to "+dlocation+" by name"
                        inbox = 1
                    else:
                        print inbox 
                        print "-- I cannot understand this line: " + line
                        inbox = 0
                        dlocation = location
                elif inbox == 1:
                    if len(line)>0 and line[0]=="/":
                        if g_qdebug==1:
                            print "out of the box"
                        inbox = 0
                    else:
                        print line
                        print dlocation
                        start(line,dlocation,1)
                else:
                    print inbox 
                    print "-- I cannot understand this line: " + line
                    inbox = 0
                    dlocation = location
                    break

        print 'download finished'
    except IOError:
        print "Fail to read file "+ filename
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

def download_html_to_pdf(url,fname,location):
    if(url and fname):
        print "Save "+fname+" from "+url+" to "+location
        pdfkit.from_url(url,location+fname)
        print "Completed"
    else:
        print "Undefined url or file name"

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

def getname(line):
    global g_qdebug
    llen = len(line)
    fname = ""
    if line.find(" -> ")>0:
        if g_qdebug == 1:
            print "There is name set in this line"
        loc = line.find(" -> ")
        if g_qdebug == 1:
            print "name was : " + line[loc+4:llen]
        fname = line[loc+4:llen]
    else:
        if g_qdebug==1:
            print "No name found"
    return fname


if __name__ == "__main__":
    main()


