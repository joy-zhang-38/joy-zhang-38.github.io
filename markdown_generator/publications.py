#!/usr/bin/env python
# coding: utf-8

# # Page Generator for Publications
# 
# Takes a TSV file of publications with metadata and converts them for use with the academicpages template. This script generates a markdown file for each publication.
# 
# The TSV file has a header row with the following columns: pub_date, title, venue, excerpt, citation, url_slug, paper_url, and slides_url. An example is provided in publications.tsv.
# 
# The optional file bibtex.bib passed as a command line argument gets copied to `_bibliography/` for the Jekyll Scholar plugin.

# ## Import Libraries
import pandas as pd
import os
import sys

# ## Import TSV
# 
# Import the TSV file using the Pandas python library.

try:
    # TSV Filename
    filename_tsv = "publications.tsv"
    
    # Read the TSV file
    publications = pd.read_csv(filename_tsv, sep="\t", header=0)
except (IOError, SystemError) as e:
    print("Error: The file '" + filename_tsv + "' could not be found. \n" + str(e))
    # Stop the script if the file is not found
    sys.exit()

# ## Escape special characters
# 
# YAML is very picky about how it deals with special characters, so we need to fix this. This general loop goes through all the columns and fixes formatting where appropriate.

def escape_md(text):
    if type(text) is str:
        return text.replace('"', '\\"')
    else:
        return text

for key, value in publications.items():
    publications[key] = value.apply(escape_md)

# ## Copy Bibtex
# 
# The Jekyll Scholar plugin requires a bib file to be copied to the `_bibliography/` folder.

try:
    if len(sys.argv) > 1:
        # Bibtex Filename
        filename_bib = str(sys.argv[1])
        
        # Copy the bib file to the `_bibliography/` folder
        os.system("cp " + filename_bib + " ../_bibliography/references.bib")
    else:
        print("Warning: No bib file was provided. The bib file will not be copied.")
except (IOError, SystemError) as e:
    print("Error: The file '" + filename_bib + "' could not be found. \n" + str(e))

# ## Loop through publications
# 
# Now we are ready to loop through the publications in the TSV file.

for row, item in publications.iterrows():
    
    # Corrected Line: Convert pub_date to a string before slicing
    year = item.pub_date
    
    md_filename = str(year) + "-" + item.url_slug + ".md"
    html_filename = str(year) + "-" + item.url_slug
    
    # ## YAML Front Matter
    
    md = "---\ntitle: \""   + item.title + '"\n'
    
    md += "collection: publications" + "\n"
    
    md += "permalink: /publication/" + html_filename + "\n"
    
    if len(str(item.excerpt)) > 5:
        md += 'excerpt: "' + str(item.excerpt) + '"\n'
    
    md += "date: " + str(item.pub_date) + "\n"
    
    md += "venue: '" + str(item.venue) + "'\n"
    
    if len(str(item.paper_url)) > 5:
        md += "paperurl: '" + item.paper_url + "'\n"

    if len(str(item.slides_url)) > 5:
        md += "slidesurl: '" + item.slides_url + "'\n"
    
    md += "citation: '" + str(item.citation) + "'\n"
    
    md += "---\n"
    
    # ## Markdown Body
    
    md += "\n"
    
    if len(str(item.excerpt)) > 5:
        md += item.excerpt + "\n"
    
    if len(str(item.paper_url)) > 5:
        md += "\n<a href='" + item.paper_url + "'>Download paper here</a>\n"
        
    if len(str(item.slides_url)) > 5:
        md += "\n<a href='" + item.slides_url + "'>Download slides here</a>\n"
        
    md_filename = os.path.basename(md_filename)
    
    with open("../_publications/" + md_filename, 'w') as f:
        f.write(md)
