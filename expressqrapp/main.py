import cv2
import numpy as np
import pytesseract
from numpy.distutils.command.config import config
import pycountry
from langdetect import detect, DetectorFactory
import re
from flask import Flask, jsonify, request
import json 
from json import dumps
import werkzeug
import requests
from PIL import Image
from pyzbar.pyzbar import Decoded, decode

# Setup flask server
app = Flask(__name__)

# initialization
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


@app.route("/upload", methods=["POST"])
def index():
    # terrasect treatement
    request_data= request.data
    request_data=json.loads(request_data.decode('utf8'))
    print(request_data)
    filename = request_data['fileName']
    print(filename)
    qrname = request_data['fileNameTwo']
    EncodedQrdata = decode(Image.open("public/images/"+qrname))
    decodedData = json.loads(EncodedQrdata[0][0])
    print(decodedData)
    print(type(decodedData))
    decoded_firstname = decodedData["firstName"]
    decoded_lastname = decodedData["lastName"]
    decoded_birth = decodedData["dateOfBirth"]
    decoded_cin = decodedData["idNumber"]
    decoded_vaccine = decodedData["vaccineDTOS"][0]["vaccineName"]
    decoded_firstvaccineDate = decodedData["vaccineDTOS"][0]["vaccinDate"][0:10]
    listSize = len(decodedData["vaccineDTOS"])
    print("size of the list is   :   "+str(listSize))
    if listSize> 1:
     decoded_secondvaccineDate = decodedData["vaccineDTOS"][1]["vaccinDate"][0:10]
     decoded_vaccineCenter = decodedData["vaccineDTOS"][1]["vaccinationCenter"]
    else:
     decoded_vaccineCenter = decodedData["vaccineDTOS"][0]["vaccinationCenter"]
   
    print(decoded_firstname)
    print(decoded_lastname)
    print(decoded_birth)
    print(decoded_cin)
    print(decoded_vaccine)
    print(decoded_firstvaccineDate)
    
 
    #decode_data=json.loads(EncodedQrdata)
    #decodedQr = json.loads(EncodedQrdata)
    #print(decode_data)
    # Create Dictionary
    
    image = cv2.imread("public/images/"+filename)
    #resize the image to new size
    image = cv2.resize(image, None, fx=1.2, fy=1.2,
                       interpolation=cv2.INTER_CUBIC)
    #convert original rvb color to gray color
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #Renvoie un nouveau tableau de forme et de type donnés, rempli de ceux 
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.erode(image, kernel, iterations=1)
    #appliquer un filtre gaussien
    cv2.threshold(cv2.GaussianBlur(image, (5, 5), 0), 0, 255,
                  cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    #appliquer un filtre bilateral
    cv2.threshold(cv2.bilateralFilter(image, 5, 75, 75), 0,
                  255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    #appliquer un filtre median
    cv2.threshold(cv2.medianBlur(image, 3), 0, 255,
                  cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    #appliquer un filtre gaussien
    cv2.adaptiveThreshold(cv2.GaussianBlur(image, (5, 5), 0), 255,
                          cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    #appliquer un filtre bilateral
    cv2.adaptiveThreshold(cv2.bilateralFilter(
        image, 9, 75, 75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

     #appliquer un filtre median
    cv2.adaptiveThreshold(cv2.medianBlur(
        image, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # text=pytesseract.image_to_string(image)
    # custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(image, lang='fra+ara')
    # text = pytesseract.image_to_string(image,lang='ara+fra',config=custom_config)
    cleared_text = re.sub(r'[\W]+', ' ', text)
  
# -------Nom et Prenom-----------
    prenom_position = (cleared_text.find("Prénom") + 6)
    card_position = (cleared_text.find("Carte") - 1)
    nomPrenom = cleared_text[prenom_position:card_position].strip()
    print("nom et prenom: "+nomPrenom)
# ---------code d insription-----------
    evax_pos = (cleared_text.find("EVAX") + 5)
    nom_pos = (cleared_text.find("Nom") - 1)
    code_inscrit = cleared_text[evax_pos:nom_pos]
    print("code d inscription : " + code_inscrit)

# ---------- Vaccin------------------
    vaccin_pos = (cleared_text.find("dose")+ 4)
    lot_pos = (cleared_text.find("N lot") - 1)
    vaccin = cleared_text[vaccin_pos:lot_pos].strip()
    print(lot_pos)
    print("vaccin")
    print(vaccin)

# ---------- Vaccine center------------------
    center_pos = (cleared_text.find("Centre de vaccination")+21)
    center2_pos = center_pos + 25
    center = cleared_text[center_pos:center2_pos].strip()
    print("center")
    print(center)
  
# ---------- CIN------------------
    national_pos = (cleared_text.find("nationale") + 10)
    type_pos = (cleared_text.find("Type") - 1)
    cin = cleared_text[national_pos:type_pos].strip()
    cin = cin.replace('00','09')
    print("/////////////////////////////////////////////////")
    print("typepos : " + str(type_pos))
    print("CIN : " + cin)
    print("national_pos : " + str(national_pos))
    print("/////////////////////////////////////////////////")

# ------------reference du vaccin ---------------
    vacci1_pos = (cleared_text.find("de vaccination") + 15)
    nom2_pos = (cleared_text.find("Nom du")-3)
    ref = cleared_text[vacci1_pos:nom2_pos]
    print("Reference du vaccin : "+ref)
    decoded_fullname = decoded_firstname + ' ' +decoded_lastname
    print(decoded_fullname)
    print(decoded_vaccine)
    print(vaccin)
    print(center)
    if((decoded_cin == cin) and (decoded_fullname == nomPrenom) and (decoded_vaccine == vaccin) and (decoded_vaccineCenter == center)):
     print("Match found")
     if listSize > 1:
      thisdict = {
      "response": True,
      "cin": decoded_cin,
      "fullname": decoded_fullname ,
      "vaccine": decoded_vaccine,
      "center": decoded_vaccineCenter,
      "firstDate": decoded_firstvaccineDate,
      "SecondDate": decoded_secondvaccineDate
      }
     else:
       thisdict = {
      "response": True,
      "cin": decoded_cin,
      "fullname": decoded_fullname ,
      "vaccine": decoded_vaccine,
      "center": decoded_vaccineCenter,
      "firstDate": decoded_firstvaccineDate,
      "SecondDate": "none"
      }
    else:
     thisdict = {
     "response": False,
     "cin": "NO MATCH FOUND",
     "fullname": "" ,
     "vaccine":  "" ,
     "center":  "" ,
     "firstDate": "" ,
     "SecondDate":  "" ,
      }
  
    return   json.dumps(thisdict)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
