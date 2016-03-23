import pdfkit
#from xvfbwrapper import Xvfb

def main():
#    with Xvfb() as xvfb:
#    config = pdfkit.configuration(wkhtmltopdf='/bin/wkhtmltopdf')
    pdfkit.from_url('http://www.google.com', 'out.pdf')#,configuration=config)

if __name__ == "__main__":
    main()
