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

inp_reader = csv.reader(inp_handle)

#
#  Loop through the file and build an odd dictionary just 
#  to illustrate a few points. The key in the dictionary
#  is going to be a tuple combining the length of the 
#  country's name and its ISO code. The value will be 
#  the country's full name.
#

codes = {}

for rec in inp_reader:

    #  Skip the first line because it's a header

    if inp_reader.line_num == 1:
        continue
    
    #  Use a tuple to extract the fields from the list

    (name,code) = rec
    
    #  Some countries with long official names are 
    #  stored like this "KOREA, REPUBLIC OF". Convert 
    #  them back to their true names.

    if ',' in name:
        (last,first) = name.split(',')
        name = first+' '+last
        name = name.strip()
    
    #  Make a tuple with the length of the name and
    #  the country code. It will be the key.

    key = (len(name),code)

    #  Store the entry in the dictionary

    codes[key] = name

inp_handle.close()

#
#  All done reading the data. Now write it out as a new
#  CSV file.
#

out_handle = open(outname,'w',newline='')
out_writer = csv.writer(out_handle)

#
#  Write a header row with names for the columns
#

out_writer.writerow(['len','code','name'])

#
#  Sort the entries by the tuples. That will cause all 
#  the short names to be listed first, and within a group 
#  that has the same length, the countries will be sorted 
#  alphabetically by code.
#
#  This is a weird example but it illustrates a VERY 
#  powerful feature of sorted(): it does a hierarchical 
#  sort automatically. That is, it groups based on the 
#  first element in the tuple, then groups by the second 
#  element, etc.
#
#  To write out the row, use list() to turn the key into
#  a list and then append the name. Also, the Vatican is 
#  listed twice with two slightly different names. Omit 
#  one just to illustrate the continue statement.
#

for key in sorted(codes):

    if key == (29,'VA'):
        print("Omitting a duplicate code:")
        print("   ",key,':',codes[key])
        continue
    
    name = codes[key]
    out_writer.writerow(list(key)+[name])

out_handle.close()
