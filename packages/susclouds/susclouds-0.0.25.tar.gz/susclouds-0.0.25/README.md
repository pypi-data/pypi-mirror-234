# Wordcloud Scripts

## Description
This is a collection of scripts that manipulate report data files (downloaded from Susmon front-end) and other report data files created by researchers to create counts of the top words create word clouds.

Key scripts:

    main.py - Main program loop that determines actions to be taken and calls relevant methods
    esg.py - ESG word clouds. Works from the standard report data file downloaded from the database and from a bespoke report created by research
    netzero.py - Net Zero word clouds and word counts. Works from a filtered report file provide by research
    Other modules contain common fuctions used by both scripts


## Installation
Scripts are written in Python 3. Libraries and version identified in requirements.txt

There are two control files that must be in place for the scripts to run:

    stopwords.csv - generic words and phrases to be excluded from word clouds
    phrases.csv - word combinations that should be treated as phrases in word clouds 

These files can be uploaded and updated via the main code loop as decribed below.

## Usage
The code is run as follows:

    python -m src.clouds.main <input file> <action "create"/"update"> [--resource <"phrases"/"stopwords">] [--sector <sector name>] [--classification <"Environmental", "Social", "Governance">]

When used with the action argument "create", the program will use the "input file" to generate word clouds as follows:

    if <input file> name contains "NZ", or "Net Zero" a set of Net Zero word clouds will be created
    otherwise
    if a <sector name> is supplied, word clouds will be generated for each brand owners in that sector and each classification. In addition word clouds will be created for all brand owners comnined for each classification and for all brand owners across all classifications. The input file in this case should be a standard report data file downloaded from the database
    if no <sector name> is supplied and a <classification> other than "All" has been supplied, a word cloud will be created for the <classification> supplied for all brands in the input file combined. The input file in this case should be one provided for this purpose by the research team.
    if no <sector name> is supplied and a <classification> of "All" has been supplied, a word cloud will be created for the all classifications and all brands in the input file combined. The input file in this case should be one provided for this purpose by the research team.

When used with the action argument "update", the program will use the "input file" to update one of the two control files as determined by the resource argument "phrases", or "stopwords".
         
## Support
[to be written]
