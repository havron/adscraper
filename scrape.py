import csv, time, urlparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", "Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0") # spoof mobile agent
browser = webdriver.Firefox(profile) # geckodriver needs to be in your PATH
browser.get('https://www.google.com')

query = browser.find_element_by_name('q')
query.send_keys("toothbrush") # reliably returns ads for us to try to parse...
query.send_keys(Keys.RETURN) # hit return after you enter search text
browser.implicitly_wait(5)

##### beginning of attempt to parse links
links = browser.find_elements_by_xpath("//h3[@class='r']/a[@href]")
results = []
for link in links:
    title = link.text.encode('utf8')
    url = link.get_attribute('href')
    results.append((title, url[29:])) # take out 'https://www.google.com/url?q=' from string, which is 29 chars

for r in results:
    print(r)
##### end of attempt to parse links
exit(0) # TODO: remove this when ready to integrate actual spyware queries template code below

with open('spyware_queries.csv', 'r') as file_handle:
    queries = csv.reader(file_handle, delimiter=',')
    for row in queries:
        query = browser.find_element_by_name('q')
        query.send_keys(row[0]) # search by an actual spyware query
        query.send_keys(Keys.RETURN) # hit return after you enter search text
        browser.implicitly_wait(5)
        # TODO: here, parse out the ad links and store them in a new file/print them out
        browser.get('https://www.google.com') 
        # print(', '.join(row))
