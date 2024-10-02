# Lexis Nexis Uni Web Scraper

Provided you have access to nexis uni (advanced.lexis.com) website, you can use this scraper to automatically download the articles instead of manually downloading 500 at a time.


Single Batch Process:
- First gets login cookie by accessing home page (happens auto if connected to vpn)
- next opens the given search query
- click actions -> changes grouping similarity level from off to high
- clicks download icon -> adds a range according to the batch size set
- checks the ms word option -> clicks download button
- monitors for "download ready" text that appears after processing is done.
- monitors for any active downloading that might be on by checking if chrome download temp files are present at the download location. (.crdownload)


