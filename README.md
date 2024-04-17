# Enumeration/Chronology Batch Updater for Alma Items
Script to take spreadsheet of corrected Enum/Chron fields for Alma items and make changes to records using the Alma Bibs API.

# What You'll Need
- Python 3.x with Pandas and Beautiful Soup libraries installed
- An Alma Bibs API key with Read/Write permissions
- An import file (in .xlsx format) containing MMS ID, Holding ID, Item PID, and the Enumeration and Chronology fields
  - To prevent any possible problems (particularly where Excel thinks its being helpful by rounding what it thinks is super big numbers) the identifiers should have quotation marks around them (the script will strip them out at runtime)
  - The script will look for all 13 Enumeration and Chronology fields, but in all likelihood most will be blank
  - I've uploaded an example of what the input file should look like to this repository
 
# How to Use
1. Identify the items you want to fix (I used an Analytics report that I used as the basis for Step 2)
2. Make the changes you want on your spreadsheet
3. Save the spreadsheet (that contains the MMS ID/Holding ID/Item PID and the corrected Enum/Chron fields) to the same folder as your script
4. Run the script, entering the filename of the spreadsheet (minus the file extension) when prompted
5. When it's finished running your items will be updated

# Additional Notes
- This script *only* makes changes to the Enumeration and Chronology fields, you *could* modify it to edit descriptions too, or you could run the "Rebuild Item Descriptions" job in Alma on the records after updating them if you also wanted to update those.
- If you're not on an North American ExLibris server you'll also need to change the base URL at the top of the script to point to your region
