#DC Government Contracts
I'm building a scraper to get the latest data from the District Government site on public contracts.

## Sole Source
Pursuant to [D.C. Code s. 2-534.04](http://dccode.org/simple/sections/2-354.04.html), the DC Government must publish a notice of intent to enter into a sole-source contract "at least 10 days prior to award" on the internet. The OCP makes the information available at the following link: [http://app.ocp.dc.gov/intent_award/intent_award.asp](http://app.ocp.dc.gov/intent_award/intent_award.asp).

The following information is available on the site:
* Notice Date
* Response Due Date
* Caption and Description
* Vendor Name
* Agency
* Point of Contact
* Link to Determination and Findings

But, it is not a permanent site, so once the contract is awarded, the info goes away... =(

This scraper solves that problem by making a permanent JSON record of the notice of intent to award a sole-source contract (in 'scrapers/solesource.json').

And, there's another part too. The PDFs contain information about the estimated reasonable price, which is not accessible in the table. But, the PDF is text-searchable and follows a standard format, so it should be doable to extract that information and include it in the JSON.

The scraper is in the 'scrapers' directory.

To set it up, this is the crontab:

> 'crontab -e'; '0 * * * * full_path' runs 'full_path' on the hour every day

## Contract Solicitations
### OCP
OCP has two different types of solicitation formats: (1) electronic and (2) non-electronic. This repo now has a scraper for non-electronic contracts (which solves some of the same problems of sole-source contracts and suffers from some of the same limitations). The electronic solicitation looks much more complicated, with a whole system built for it. 
  
### Rest of DC Government

## Contract Appeals Board
The Contract Appeals Board is responsible for considering contract appeals and protests. Their web site is cab.dc.gov.

They have a decent database of all filings, and it's searchable. But, there's not a bulk data download. Nor is there a way to get notified of recently posted materials or upcoming hearings.

To appreciate the irony of all of this, consider the following footnote from a recent opinion: "Advantage Energy, LLC is currently pending publication in the D.C. Register and in commercial databases. In the interim, we have cited to the Board’s website, which is an acceptable alternative citation". Appeal of Adsystech, Inc., CAB No. D-1210, at 22 n.32 (Aug. 15, 2013) The problem is that **the cite to the Board's website** does not work because there are no permalinks to the actual decision! And that as-yet unpublished, but precedential decision was issued THREE years before the Adsystech opinion.

So, to get the underlying precedential opinions, you need to run the following shell command

> wget --post-data='from_date=&to_date=&search_type=fulltext&parmCount=2&parm1=49&parm2=83' http://app.cab.dc.gov/WorkSite/SearchDocs.asp?minLevel=0&OriginalURL=Published_Board_Decisions

To get the NEXT set of 15, you need to change to "minLevel=15" and so forth.

Then, there's the problem of actually extracting the URL for the underlying document.
