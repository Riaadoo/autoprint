"""
Developped by Riad DRAOUI, september 2021
"""

import cv2
from pyzbar.pyzbar import decode
import urllib.request
from urllib.error import HTTPError
import cups, pprint

# Lancer la webcam
cap = cv2.VideoCapture(0)

#fonction pour télécharger le fichier pdf
def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)    
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()

# Se connecter à l'imprimante
conn = cups.Connection()
printers = conn.getPrinters ()
#pprint.pprint(printers)
printer = conn.getDefault()
 
if printer == None:
    printer = list(printers.keys())[0]

# La liste des urls déja scannés
Links_list = ['']

while True:
    
    check, img = cap.read()
    #img = cv2.resize(img, (64, 64))
    cv2.imshow("image", img)
    for code in decode(img):
        link = code.data.decode('utf-8')
        if link not in Links_list:
            Links_list.extend([link])
            print(link)
            file = link.split(".")
            print(file)
            if file[0] == "http://www" and file[-1] == "pdf":
                try:
                    download_file(link, "Test2")
                    myfile = "Test2.pdf"
                    pid = conn.printFile(printer, myfile, "test", {})
                    print("Printig file...")
                #while conn.getJobs().get(pid, None) is not None:
                except urllib.error.HTTPError as err:
                    print(err.code)
            else:
                print("not valid file")
                       
    if(cv2.waitKey(1) == ord("q")):
        break

cap.release()
cv2.destroyAllWindows()
print("fin du programme")