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

This scraper will hopefully solve that problem by making a permanent JSON record of the notice of intent to award a sole-source contract.

And, there's another part too. The PDFs contain information about the estimated reasonable price, which is not accessible in the table. But, the PDF is text-searchable and follows a standard format, so it should be doable to extract that information and include it in the JSON.

To set it up, this is the crontab 
'crontab -e'; '0 * * * * full_path' runs 'full_path' on the hour every day

## Contract Solicitations
### OCP
### Rest of DC Government

