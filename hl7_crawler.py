import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# pip3 install selenium bs4 requests

#================================================================================
class BeautifulSoup4:
	def __init__(self):
		#headers = {
		#	'Access-Control-Allow-Origin': '*',
		#	'Access-Control-Allow-Methods': 'GET',
		#	'Access-Control-Allow-Headers': 'Content-Type',
		#	'Access-Control-Max-Age': '3600',
		#	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
		#}
		#req = requests.get(url, headers)
		#html=req.content
		#----------------------------------------
		#browser = webdriver.PhantomJS()
		#browser.get(url)
		#html = browser.page_source
		#----------------------------------------
		self.chrome_options = Options()
		self.chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36")
		self.chrome_options.add_argument("--disable-extensions")
		self.chrome_options.add_argument("--disable-gpu")
		self.chrome_options.add_argument("--headless")
		# self.chrome_options.headless = True # also works
		#self.chrome_options.add_argument("--no-sandbox") # linux only
		self.driver = webdriver.Chrome(options=self.chrome_options)
	#--------------------------------------------------------------------------------
	def get(self, url):
		self.driver.get(url)
		import time
		# --- Scroll until no new content loads ---
		last_height = self.driver.execute_script("return document.body.scrollHeight")

		while True:
			# Scroll down to bottom
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			
			# Wait for new content to load
			time.sleep(2)  # adjust if the site is slow
			
			# Calculate new scroll height
			new_height = self.driver.execute_script("return document.body.scrollHeight")
			
			# Break if no more content
			if new_height == last_height:
				break
			last_height = new_height
		self.html = self.driver.page_source.encode("utf-8")
		#print(self.driver.page_source.encode("utf-8"))
		# b'<!DOCTYPE html><html xmlns="http://www....
		self.soup = BeautifulSoup(self.html, 'html.parser')
		return self.soup
	#--------------------------------------------------------------------------------
	def quit(self): self.driver.quit()
#================================================================================
bs4 = BeautifulSoup4()


# <a _ngcontent-cre-c161="" mat-list-item=""
#     class="mat-list-item mat-focus-indicator mat-2-line mat-list-item-avatar mat-list-item-with-avatar ng-star-inserted"
#     aria-label="HL7 v2.3 - ACC - Accident (Segment)" href="/v2/HL7v2.3/Segments/ACC" style="">
#     <div class="mat-list-item-content">
#         <div mat-ripple="" class="mat-ripple mat-list-item-ripple"></div><img _ngcontent-cre-c161="" matlistavatar=""
#             mattooltipposition="below" class="mat-list-avatar mat-tooltip-trigger"
#             src="assets/icons/segment.svg?v=8.0.0" alt="Segment" aria-describedby="cdk-describedby-message-643"
#             cdk-describedby-host=""><!---->
#         <div class="mat-list-text">
#             <h3 _ngcontent-cre-c161="" mat-line="" class="mat-line cx-h3 cx-link--gray"> ACC - Accident </h3>
#             <p _ngcontent-cre-c161="" mat-line="" mattooltipposition="below"
#                 class="mat-tooltip-trigger mat-line cx-body" aria-describedby="cdk-describedby-message-644"
#                 cdk-describedby-host=""> The ACC segment contains patient information relative to an accident in which
#                 the patient has been involved. </p><!---->
#         </div>
#     </div>
# </a>

version = "2.3"
url = f"https://hl7-definition.caristix.com/v2/HL7v{version}/Segments"
soup = bs4.get(url)
segments = soup.find_all("a")

#print(segments)
print(len(segments))
for segment in segments:
	try:
		segment_url = segment["href"]
		print(segment_url)
	except:
		pass
	# product_code=product_path.split("=")[1]
	# if(product_path):
	#     if(product_code not in ids):
	#         url = "https://eg.oriflame.com" + product_path
	#         getProductInfo(bs4, url)
	#     else:
	#         print(" | >>> Product is exist !")

bs4.quit()
#================================================================================