# Exercise: Working with Large Zipped CSV Data

### Summary

This exercise focuses on techniques that are useful for working with 
large datasets in zipped CSV format.

### Input Data

The input data is a file called **id114_2014.zip** that will need to be 
downloaded from the course Google Drive folder. See the course web page
for a link to the folder. Please resist the temptation to unzip the file: 
the contents are large (72 MB) and part of the point of the exercise is 
to work with the data without unzipping the file first.

The zip file contains a single large CSV file called **id114_2014.csv**. 
It contains data from the Pecan Street Project, a research project in 
Austin, Texas, that collects high resolution data on household electricity 
consumption. This file particular file is the data for household 114 in 
2014.

The file has one record for every minute (around 525,600 in all). Each 
record contains electricity use for up to 67 circuits in the house, though
not all are used for this particular household. In this exercise we'll 
only use two of the fields: the timestamp for the record, showing the date
and time of the data, and the household's total usage. The timestamp is the 
second field in each record and usage is the third field. If you'd like to 
see what the records in the CSV file look like, see **firstlines.csv** in 
the Google Drive folder. It has the file's first 10 lines.

If you want to run the `demo.py` script for this exercise, you'll 
also need to download **demo.zip**. It has data on ISO country codes
but it isn't necessary for the actual assignment.

### Deliverables

A script called **pecan.py** that goes through the steps below to produce
a sorted file of average hourly usage called `usage.csv`, and a short
Markdown file called **pecan.md**. Note that `usage.csv` itself is not a 
deliverable and will not be uploaded to GitHub when you push your 
repository: the .gitignore file in the directory tells GitHub not to 
upload zip or csv files.

### Instructions

1. Import the following modules: `csv`, `io`, and `zipfile`.

1. Import the numpy module using `import numpy as np`. Numpy is a module
   with extensive support for numerical analysis. It's usually imported
   as `np` to make calls to its functions more concise.

1. See `demo.py` for an example showing how to open a CSV file within
   a zip archive. There are three steps: (1) using `zipfile.ZipFile()` to 
   set up a zip object for working with the archive as a whole; (2) using 
   that object's `open()` call to open file `id114_2014.csv` within the 
   archive; and (3) a call to `io.TextIOWrapper()` to translate the way
   the data is stored in the file (as a sequence of bytes) into Python's 
   internal way of representing strings. The last step is not necessary 
   when opening a regular text file because the operating system does the 
   job instead.
   
1. Use a call to `csv.reader()` to create an object called `inp_reader` 
   that will let you loop through the file one line at a time using commas
   to split each line into fields.
   
1. Use `open()` to open a file handle for an output file called `usage.csv`.
   Include the keyword argument `newline=''`. It's needed to keep the 
   file from having extra returns when it is used with the CSV module.
   
1. Use a call to `csv.writer()` to create an object called `out_writer`
   that will let you write CSV records to the output file.
   
1. Create an empty dictionary called `hourly` to collect the data.

1. Use a for loop with running variable `rec` to loop through `inp_reader`.
   Within the loop do the following.
   
   1. Use an `if` statement and `inp_reader.line_num` to skip the first 
   line.
   
   1. Drop any records where the usage field is missing (blank) by 
   using an `if` statement to check whether `rec[2]` is empty ("").
   Use a `continue` statement to go on to the next record when it is.
   
   1. Create a variable called `localmin` and set it to the timestamp,
   which is `rec[1]`. Then create a variable called `usage` and
   use `float()` to set it to the numerical value of the usage, which is 
   `rec[2]`.
   
   1. Split `localmin` on spaces and call the pieces `date` and `time`.
   Then split `date` using "/" and call the pieces `mo`,`dy`, and `yr` 
   and split `time` into `hr` and `mi` using ":".
   
   1. Create a tuple called `key` that consists of `int(mo)`, `int(dy)` 
   and `int(hr)`. It will represent the hour within the year.
   
   1. If `key` is in `hourly`, look up the entry and then add `usage` 
   to its `sum` attribute and add `1` to its `n` attribute. Using an
   `else` statement, if `key` is not in `hourly`, create a dictionary 
   called `new_entry` having the following keys: `sum`, which should be 
   set to `usage`, and `n`, which should be set to 1. Store `new_entry` 
   in `hourly` using `key` as the key.
   
1. After the loop completes, use the `writerow()` call on `out_writer` with 
   a list of strings that will be used as column headers. The list should 
   look like this: `['month','day','hour','usage']`.
   
1. Create an empty list called `averages`.

1. Use a for loop with a running variable of `key` iterating over
   `sorted(hourly)`. Within the loop do this:
   
   1. Create a variable called `entry` that is equal to the value of 
   `hourly` for `key`.
   
   1. Check whether `entry['n']` is greater than 60. When `n` is over 60, 
   print out a message to indicate that it's being dropped and include 
   `entry` itself. Then use a `continue` statement to go on to the next 
   entry. The extra minutes happen due to daylight savings time: an hour in 
   November is repeated when the clock shifts back. We'll drop it just
   to illustrate how to remove inconsistent data. There's also a 
   missing hour in the spring when the clock shifts forward, and a few 
   hours where some minutes are missing. We won't do anything special 
   about the missing minutes.
   
   1. Compute the average usage by dividing the `sum` attribute by 
   the `n` attribute.

   1. Append the average to the `averages` list.
   
   1. Use the `list()` call to create a list from `key` and then 
   append the average to it. Call the new list `result`.
   
   1. Use `writerow()` to write out `result`. 

1. An important feature of electricity consumption is that it has sharp 
   spikes: that is, it has a small number of very high values. To see 
   this, we'll look at some percentiles for this data. Create a list 
   called `pctiles` that consists of the following five percentiles: 1, 
   25, 50, 75, 99. 
   
1. Now add a call to the numpy percentiles function as follows:
   `np.percentile(averages,pctiles)`. That will calculate the average
   usage at each percentile cutoff.
   
1. Print the result.

1. Use a text editor to write a short Markdown file called `pecan.md` using 
   the percentile information to describe electricity use. The first line 
   should be the title `# Average Hourly Electricity Use for 114`. In the 
   remainder of the file please briefly describe the results. Don't just 
   say "X percentile is Y". Aim for something more like "half the time it 
   is between X and Y" and so on.
   
### Submitting

Once you're happy with everything and have committed all of the changes to
your local repository, please push the changes to GitHub. At that point, 
you're done: you have submitted your answer.

### Tips

+ Reading CSV files that aren't in zip archives is simpler: just use
  an `open()` call to open the file, and then give the file handle to 
  `csv.reader()`. 

+ It's handy to open the output file *before* reading the whole input
  file so the script will crash immediately if opening the output file
  fails. A common cause of open failures is having the last output file
  open in Excel and then trying to rerun the script. If you open the 
  output file *after* processing the input file you may end up waiting 
  a long time only to have the script crash.
  
+ There are other ways to translate timestamp strings into numerical
  values beside using `split()` repeatedly. In this case, however, 
  `split()` is substantially faster than most of the alternatives. That 
  matters because this file is only one small part of a large dataset 
  with multiple years of data and hundreds of households.
  
+ Using the `sorted()` call with tuples is very handy. It's especially
  useful when the data will be viewed by a person: you can order the 
  elements of the tuples so the data will be grouped in the most 
  appropriate way. 
  
+ The daylight savings issue comes about because the instrument used to 
  record the data is set to local time (i.e., what a clock on the wall 
  would show). An alternative would be to use Coordinated Universal
  Time (UTC), a world-wide standard that has no adjustment for 
  daylight savings or timezones. If you're ever working on datasets that 
  need to be synchronized, and have a say in how the timestamps are set up,
  UTC is often better than local time.
  
