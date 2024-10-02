# Lexis Nexis Uni Web Scraper

Provided you have access to nexis uni (advanced.lexis.com) website, you can use this scraper to automatically download the articles instead of manually downloading 500 at a time.


## Single Batch Process:
- First gets login cookie by accessing home page (happens auto if connected to vpn)
- next opens the given search query
- click actions -> changes grouping similarity level from off to high
- clicks download icon -> adds a range according to the batch size set
- checks the ms word option -> clicks download button
- monitors for "download ready" text that appears after processing is done.
- monitors for any active downloading that might be on by checking if chrome download temp files are present at the download location. (.crdownload)


## Overview Architecture
- Run selenium half way to get the number of total articles,
- divide it into batch sizes,
- run the single batch process on each (Could be optimized in future by introducing multithreading)
- Each run creates and stores a docx of the batch size
- Found a great R library which helps convert the docx into csv files so used that.

## TODO:
- Python script to merge the csv files
- Ready!

### Future TODO:
- Add multithreading to single batch process of the scraper