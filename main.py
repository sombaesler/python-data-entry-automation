import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver

CHROME_DRIVER_PATH = "/Users/orangejuice/Documents/Web Development/chromedriver"
ZILLOW_URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
GOOGLE_FORM_URL = "https://forms.gle/8nrC9ARXh6E5gL5E6"

header = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"
}

response = requests.get(ZILLOW_URL, headers=header)
response.raise_for_status()
result = response.text

soup = BeautifulSoup(result, "html.parser")

all_links = [item.find(class_="list-card-link").get("href") for item in soup.find_all(class_="list-card-info")]
all_prices = [item.find(class_="list-card-price").text for item in soup.find_all(class_="list-card-info")]
address_list = [item.find(class_="list-card-addr").text for item in soup.find_all(class_="list-card-info")]

link_list = []
price_list = []

# FORMAT LINKS #
for link in all_links:
    if "http" not in link:
        link = "https://www.zillow.com" + link
    link_list.append(link)

# FORMAT PRICES #
for price in all_prices:
    if "+" in price:
        price = price.split("+")[0]
    elif "/" in price:
        price = price.split("/")[0]
    elif " " in price:
        price = price.split(" ")[0]
    price_list.append(price)

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
driver.get(GOOGLE_FORM_URL)

for item in range(len(address_list)):
    time.sleep(1)
    address_input = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')

    address_input.send_keys(address_list[item])
    price_input.send_keys(price_list[item])
    link_input.send_keys(link_list[item])
    submit_button.click()

    time.sleep(1)
    submit_another = driver.find_element_by_link_text("Submit another response")
    submit_another.click()

driver.quit()
