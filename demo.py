#! /bin/python3
#  Spring 2020 (PJW)
#
#  Demonstrates reading from zip files without unzipping them 
#  first, as well as reading from CSV files.
#
#  Requires "demo.zip" from the course data repository for this 
#  exercise.
# 

import csv
import io
import zipfile

#
#  Input names. zipname is the name of the zip file, and csvname 
#  is the name the specific file within it. The latter is needed 
#  since there may be more than one file in a zip file.
#

zipname = 'demo.zip'
csvname = 'iso-country-codes.csv'

#
#  Name of the output file
#

outname = 'demo.csv'

#
#  Set up a zip object for working with the zip file. Then use it
#  to get a handle to the specific file within it. The call to 
#  io.TextIOWrapper() is needed to convert the raw string of 
#  bytes in the zip file into Python's internal string format.
#

zip_object = zipfile.ZipFile(zipname)
inp_byte   = zip_object.open(csvname)
inp_handle = io.TextIOWrapper(inp_byte)

# 
#  Set up a CSV reader to parse the input and return
#  a list of elements for each line of the file.
#

inp_reader = csv.DictReader(inp_handle)

#
#  Loop through the file and build an odd dictionary just 
#  to illustrate a few points. The key in the dictionary
#  is going to be a tuple combining the length of the 
#  country's name and its ISO code. The value will be 
#  the country's full name.
#

codes = {}

for rec in inp_reader:

    #  Get fields from this record
    
    name = rec['country']
    code = rec['code']
    
    #  Some countries with long official names are 
    #  stored like this "KOREA, REPUBLIC OF". Convert 
    #  them back to their true names.

    if ',' in name:
        (last,first) = name.split(',')
        name = first+' '+last
        name = name.strip()
    
    #  Make a tuple with the length of the name and
    #  the country code. It will be the key.

    key = ( len(name), code )

    #  Store the entry in the dictionary

    codes[key] = name

inp_handle.close()

#%%
#
#  All done reading the data. Now sort it and write it out.
#
#  Sort the entries by the tuples. That will cause all 
#  the short names to be listed first, and within a group 
#  that has the same length, the countries will be sorted 
#  alphabetically by code.
#
#  Also, the Vatican is listed twice with two slightly 
#  different names. Omit one just to illustrate the 
#  continue statement.
#

for key in sorted(codes):

    #  If we're looking at the 29-character version of the 
    #  Vatican's name, skip it by using the continue statement 
    #  to go onto the next key without executing the rest of 
    #  the loop.
    
    if key == (29,'VA'):
        continue

    #  OK, write this one, converting the name to title case
    #  along the way.
    
    name = codes[key].title()
    (length,code) = key    
    
    print( f"{length:2d}: {name} ({code})")

