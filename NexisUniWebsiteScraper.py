from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging

# Hanlding Logging CONFIGS
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)
# Set logging level for Selenium and other libraries to WARNING
logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

def debugx(*args):
    logger.debug(" ".join(map(str,args)))

def infox(*args):
    logger.info(" ".join(map(str,args)))


class NexisWebScrapper:
    def __init__(self):
        # maybe add btime, etime, query
        self.driver = webdriver.Chrome() # Initializing chrome selenium driver
        self.link = ""  # Link with query
        self.N = 0  # final number of articles

    def login(self):
        # Make sure VPN is active
        # Just visiting the home page when UCSD VPN is active,
        # stores the session cookie in your browser which auto logs you in
        self.driver.get("http://www.nexisuni.com/")

    def toggleHighSimilarity(self):
        # Actions button
        actionsButton = self.driver.find_element(By.XPATH, "//button[@id='resultlistactionmenubuttonhc-yk']")
        actionsButton.click()

        highSimiButton = self.driver.find_element(By.XPATH, "//ul[@class='nexisnewdedupe']//button[@data-action='changeduplicates' and @data-value='high']")
        highSimiButton.click()  # causes a ajax request
        
        
        ## WAITING FOR AJAX TO COMPLETE THE SOFT REFRESH BY MONITORING THE VALUE
        # Off by default
        debugx("Similarity Level", self.driver.find_element(By.XPATH, "//button[contains(@class, 'la-Correct')]").get_attribute("data-value"))
        turnedHigh = WebDriverWait(self.driver, 20).until(
            lambda driver: driver.find_element(By.XPATH, "//button[contains(@class, 'la-Correct')]")
                            .get_attribute("data-value") == "high"
        )
        infox("Turned High!")
        # Changed to High from Off
        debugx("Similarity Level", self.driver.find_element(By.XPATH, "//button[contains(@class, 'la-Correct')]").get_attribute("data-value"))


        self.updateNumberOfArticles()   # Update the number of articles


    def updateNumberOfArticles(self):
        # wait for any ajax request to complete
        N_span = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//span[@data-actualresultscount]"))
        )
        self.N = int(N_span.get_attribute("data-actualresultscount"))
        debugx("Updated Number of Articles to", self.N)

    def __call__(self):
        self.login()
        self.link = "https://advance.lexis.com/search/?pdmfid=1519360&crid=a907010f-8daf-4ab7-9725-f03cdd7d63ad&pdsearchterms=((Hate+W%2F2+Crime))+AND+((date+aft(06%2F01%2F2020))+AND+(DATE+BEF(12%2F31%2F2020)))+AND+new+york&pdstartin=hlct%3A1%3A1&pdcaseshlctselectedbyuser=false&pdtypeofsearch=searchboxclick&pdsearchtype=SearchBox&pdoriginatingpage=search&pdqttype=and&pdquerytemplateid=&ecomp=hcdxk&prid=ad6927ea-40c2-4c79-99ed-983e8f86fa13"
        self.driver.get(self.link)

        self.toggleHighSimilarity()

        
        #$x("//input[@id='SelectedRange' and @placeholder]")[0].value = 1000
        download_button = self.driver.find_element(By.XPATH, "//button[@data-qaid='toolbar_downloadopt']")
        download_button.click()


        # Debug
        input("waiting to close")
        self.driver.close()


if __name__ == "__main__":
    nexis = NexisWebScrapper()
    nexis()