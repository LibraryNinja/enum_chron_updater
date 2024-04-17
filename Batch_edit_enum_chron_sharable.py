import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from datetime import datetime

date = datetime.now().strftime("%m%d%y")

#Sets up logging
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, filename="update_enum-chron.log", datefmt='%Y-%m-%d %H:%M:%S')

#Set up default things for base URL and bib API key
alma_base = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1'

#Insert Bib R/W API key:
bibapi = 'INSERT YOUR API KEY HERE'


#Required headers for requests to work
headers = {"Accept": "application/xml", "Content-Type": "application/xml"}

#Update log file
logging.info("Script started-" + date)

#Take input file
inputfile = input('Enter Input Filename without extension (Note: must be in .xlsx format and in same folder as this script): ')

#Keep_default_na=False so that it doesn't add "nan" to blank cells from input file
source = pd.read_excel(f"{inputfile}.xlsx", keep_default_na=False)

#Reads columns from input spreadsheet, all as strings
lookupmms_raw=source['MMS Id'].astype(str)
lookupholdid_raw=source['Holding Id'].astype(str)
lookupitemid_raw=source['Physical Item Id'].astype(str)

lookup_update_enum_a = source['Enum A'].astype(str)
lookup_update_enum_b = source['Enum B'].astype(str)
lookup_update_enum_c = source['Enum C'].astype(str)
lookup_update_enum_d = source['Enum D'].astype(str)
lookup_update_enum_e = source['Enum E'].astype(str)
lookup_update_enum_f = source['Enum F'].astype(str)
lookup_update_enum_g = source['Enum G'].astype(str)
lookup_update_enum_h = source['Enum H'].astype(str)
lookup_update_chron_i = source['Chron I'].astype(str)
lookup_update_chron_j = source['Chron J'].astype(str)
lookup_update_chron_k = source['Chron K'].astype(str)
lookup_update_chron_l = source['Chron L'].astype(str)
lookup_update_chron_m = source['Chron M'].astype(str)

#Removes precautionary ""s from long ID numbers
lookupmms = ([s.replace('"', '') for s in lookupmms_raw])
lookupholdid = ([t.replace('"', '') for t in lookupholdid_raw])
lookupitemid = ([r.replace('"', '') for r in lookupitemid_raw])


#The actual function, loop through input file data, pull record from Alma, update the enum/chron fields based on input file data, send data back to Alma
for i, itemid in enumerate(lookupitemid, 0):
   mms_id = lookupmms[i]
   holding_id = lookupholdid[i]
   item_pid = lookupitemid[i]
   update_enum_a = lookup_update_enum_a[i]
   update_enum_b = lookup_update_enum_b[i]
   update_enum_c = lookup_update_enum_c[i]
   update_enum_d = lookup_update_enum_d[i]
   update_enum_e = lookup_update_enum_e[i]
   update_enum_f = lookup_update_enum_f[i]
   update_enum_g = lookup_update_enum_g[i]
   update_enum_h = lookup_update_enum_h[i]
   update_chron_i = lookup_update_chron_i[i]
   update_chron_j = lookup_update_chron_j[i]
   update_chron_k = lookup_update_chron_k[i]
   update_chron_l = lookup_update_chron_l[i]
   update_chron_m = lookup_update_chron_m[i]

   #Let user know what's going on and also add to log file
   print(f"Processing {item_pid}, entry # {str(i+1)} of {str(len(lookupitemid))}")
   logging.info(f"Processing {item_pid}, entry # {str(i+1)} of {str(len(lookupitemid))}")

   #Pull item record from Alma
   r = requests.get(f"{alma_base}/bibs/{mms_id}/holdings/{holding_id}/items/{item_pid}?view=brief&apikey={bibapi}", headers=headers)

   #Check that response is 200 (record found, no errors), log any errors, if record is found then proceed 
   if r.status_code != 200:
      logging.error(f"Error on {item_pid}, record not found?")
   else:
      soup = BeautifulSoup(r.content, "xml") 

      #Find enum and chron fields in item record data, replace their contents with the updated data from spreadsheet:
      enum_a = soup.enumeration_a
      enum_a.string = update_enum_a

      enum_b = soup.enumeration_b
      enum_b.string = update_enum_b

      enum_c = soup.enumeration_c
      enum_c.string = update_enum_c

      enum_d = soup.enumeration_d
      enum_d.string = update_enum_d

      enum_e = soup.enumeration_e
      enum_e.string = update_enum_e

      enum_f = soup.enumeration_f
      enum_f.string = update_enum_f

      enum_g = soup.enumeration_g
      enum_g.string = update_enum_g

      enum_h = soup.enumeration_h
      enum_h.string = update_enum_h

      chron_i = soup.chronology_i
      chron_i.string = update_chron_i

      chron_j = soup.chronology_j
      chron_j.string = update_chron_j

      chron_k = soup.chronology_k
      chron_k.string = update_chron_k

      chron_l = soup.chronology_l
      chron_l.string = update_chron_l

      chron_m = soup.chronology_m
      chron_m.string = update_chron_m

      #Takes the Soup item...
      newitemdata = soup.item

      #Makes it a string instead of an object??? (So it can be sent off in the request)
      newitemdata_str = str(newitemdata)

      #Sends updated item record back to Alma as a PUT request
      updatepush = requests.put(f"{alma_base}/bibs/{mms_id}/holdings/{holding_id}/items/{item_pid}?generate_description=false&apikey={bibapi}", data=newitemdata.encode('utf-8'),headers=headers)

      #Checks that update was successful and logs result
      if updatepush.status_code != 200:
         logging.error(f"Record not updated, Item ID {item_pid}")
      else:
         logging.info(f"Item PID Record {item_pid} updated successfully")