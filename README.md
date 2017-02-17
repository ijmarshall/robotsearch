# RobotSearch

Software for filtering RCTs from a search result.

## How it works

RobotSearch uses machine learning as an alternative to string-based study design filters.

It works with MEDLINE searches exported from either PubMed or Ovid. 

1. You should conduct your search as normal (NB do not use any search terms or filters to restrict to RCTs at this stage!).

2. Then export your results in RIS format (see more detailed instrutions below on how to do this in PubMed and Ovid)

3. From the command line/terminal, run the robotsearch command:
`./robotsearch.py my_file.ris`

4. Your search results will be saved as `my_file_robotreviewer_RCTs.ris`

## Notes

By default, RobotReviewer runs a *sensitive* search (i.e. very high likelihood that *all* RCTs will be retrieved, at expense of sometimes including non-RCTs) - this is suitable for a systematic review.

To run a *precise* search (i.e. the retrieved articles have a very high likelihood of being RCTs, but at the expense of missing a tiny proportion), run with an extra `-p` flag, e.g.:

`./robotsearch.py my_file.ris -p`

## Exporting from PubMed

![How to export from PubMed](pubmed_export.png)

1. Select 'Send to' (located in the upper left of the search results)
2. Under 'Choose Destination' select File
3. Under 'Format', select 'MEDLINE' from the pulldown menu
4. Click the 'Create File' button

## Exporting from Ovid

![1. Exporting from Ovid - select 'All' in the top left, then click the Export text](ovid_export1.png)
![2. Exporting from Ovid - select 'EndNote' as the export format, then select 'Custom Fields', and click the 'Select Fields' button](ovid_export2.png) (**Endnote** format includes the 'publication type' field, the **RIS** format does not)
![2. Exporting from Ovid - select the following 3 fields to export: *ab*: Abstract, *pt*: Publication Type, and *ti*: Title](ovid_export3.png)

1. Click the tickbox next to **'All'** above the search results on the left hand side.
2. Click on Export
3. In the **'Export to'** pulldown menu, select 'RIS'
4. Under **'Select Fields to Display'** select 'Custom Fields', then click the 'Select Fields' button
5. In the **Select Fields** box, select the following fields: *ab*: Abstract, *pt*: Publication Type, and *ti*: Title. You may deselect any others.
6. Click 'Save' in the bottom left
7. Click 'Export Citation(s)' in the bottom right
8. The citations will be exported, but there may be a wait of a minute or two.

