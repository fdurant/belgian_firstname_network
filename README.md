# Similarity Network of first names given in Belgium between 1995 and 2015

## Data source

Belgian Federal Public Service for Economy, SMEs, Self-Employed and Energy:

- [Names given to girls born in Belgium, 1995-2015](http://statbel.fgov.be/nl/binaries/Voornamen_meisjes_1995-2015_tcm325-239448.xls)
- [Names given to boys born in Belgium, 1995-2015](http://statbel.fgov.be/nl/binaries/Voornamen_Jongens_1995-2015_tcm325-239464.xls)

Download these *.xls files in your local _data_ folder, next to the _src_ folder

## Usage

    $ python src/build_firstname_network.py -h

    usage: build_firstname_network.py [-h] --inFileXls INFILEXLS [INFILEXLS ...]
                                      [--sheetName SHEETNAME]
                                      [--partOfCountry PARTOFCOUNTRY]
                                      [--startNumber STARTNUMBER]
                                      [--maxNrNames MAXNRNAMES]
                                      [--simThreshold SIMTHRESHOLD]
                                      [--degreeThreshold DEGREETHRESHOLD]
                                      [--rankThreshold RANKTHRESHOLD]
                                      [--bonusMultiplier BONUSMULTIPLIER]
                                      --outFileGraphML OUTFILEGRAPHML

    optional arguments:
      -h, --help            show this help message and exit
      --inFileXls INFILEXLS [INFILEXLS ...]
                            input file(s) with Belgian first names in MS Excel
                            format
      --sheetName SHEETNAME
                            name of the sheet - i.e. year - of interest, e.g. 2000
                            (default is 1995 through 2015)
      --partOfCountry PARTOFCOUNTRY
                            1 = whole of Belgium (DEFAULT); 2 = Brussels only;
                            3=Flanders only; 4=Wallonia only)
      --startNumber STARTNUMBER
                            rank number of the highest-ranked first name to
                            include in output graph
      --maxNrNames MAXNRNAMES
                            number of names to store in output network
      --simThreshold SIMTHRESHOLD
                            minimum inter-name similarity for a link to be created
      --degreeThreshold DEGREETHRESHOLD
                            minimum degree required for a node to be included in
                            the output graph
      --rankThreshold RANKTHRESHOLD
                            all nodes below this rank are guaranteed to be
                            included in the output graph
      --bonusMultiplier BONUSMULTIPLIER
                            the edge weights of the nodes below rankThreshold get
                            multiplied with this bonus to increase their chances
                            of survival
      --outFileGraphML OUTFILEGRAPHML
                            output file with Belgian first names in GraphML format
    

## How the GraphML files were built

    $ mkdir out
    $ python src/build_firstname_network.py --inFileXls data/Voornamen_Jongens_1995-2015_tcm325-239464.xls \\
                                            --outFileGraphML out/firstname.graphml \\
                                            --startNumber 1 --maxNrNames 3751 \\
                                            --simThreshold 0.55 \\
                                            --degreeThreshold 2 \\
                                            --rankThreshold 100

    $ python src/build_firstname_network.py --inFileXls data/Voornamen_meisjes_1995-2015_tcm325-239448.xls \\
                                            --outFileGraphML out/firstname.graphml \\
                                            --startNumber 1 \\
                                            --maxNrNames 4135 \\
                                            --simThreshold 0.55 \\
                                            --degreeThreshold 2 \\
                                            --rankThreshold 100

## Visualization with [Gephi](https://gephi.org)

- Load the produced GraphML file into Gephi
- Color the nodes via Appearance - Nodes - Attributes - Choose an attribute - community
- Arrange the nodes via Layout - Fruchterman Reingold with the following settings:
  - Area: 100000.0
  - Gravity: 0.5
  - Speed: 10.0
- Export to PDFs via Preview - Export PDF
- Export to interactive web page via File - Export - Sigma.js template

## Result files and full story

See my [blog article][http://frederikdurant.com/projects/firstname-network-belgium/]
