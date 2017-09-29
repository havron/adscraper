import csv, time, urlparse, os, ast
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", "Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0") # spoof mobile agent
browser = webdriver.Firefox(profile) # geckodriver needs to be in your PATH
browser.get('https://www.google.com')

# save data for later parsing/visual inspection... #noratelimitspls
with open('spyware_queries.csv', 'r') as file_handle:
    queries = csv.reader(file_handle, delimiter=',')
    for i in range(0,447):
        queries.next()
    for row in queries:
        row[1] = ast.literal_eval(row[1])
        for term in row[1]:
            query = browser.find_element_by_name('q')
            query.send_keys(term) # search by an actual spyware query
            query.send_keys(Keys.RETURN) # hit return after you enter search text
            term = term.replace(" ", "_") # make filenames cleaner
            time.sleep(2)
            path = "./ads/"+row[0]+"/"
            path = path.replace(" ", "_")
            if not os.path.exists(path):
                os.makedirs(path)

            browser.save_screenshot(path+term+".png")
            with open(path+term+".html", 'w') as hits_handle:
                hits_handle.write(browser.page_source.encode('utf-8').strip())

            print("Saved all hits for '"+path+term+"'...")
            browser.get('https://www.google.com')

        # TODO: here, parse out the ad links and store them in a new file/print them out
        # print(', '.join(row))
