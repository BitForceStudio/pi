import urllib2

def main():
    url = raw_input("URL:")
    fname = "temp.pdf"
    afname = autoname(url)
    nfname = namefilter(afname)
    res = raw_input("Do your like "+nfname+" be your file name?(Y/N)")
    if (res=="Y" or res=="y"):
        fname = nfname
    else:
        fname = raw_input("Name:")
    download_file(url,fname)

def download_file(url,fname):
    if (url and fname):
        print "Save "+fname+" from "+url+" to "+" /Doc/remotesaved/"
        response = urllib2.urlopen(url)
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

def namefilter(name):
    # 1:replace %20 to _
    if name.find("%20")>0:
        oldname = name
        print "Old name is: "+oldname
        newname = name.replace("%20","_")
        res = raw_input("Would you like to keep "+newname+"(Y/N)")
        if (res=="Y" or res=="y"):
            return newname
        else:
            return oldname
    else:
        return name

if __name__ == "__main__":
    main()


