import bs4
import re
import requests
import numpy as np
import pandas as pd
product_names = []
price_list = []
# product_names to be the final list to pass cleaned data once names are cleaned
url = 'https://leapfroglobal.com/products?page='
for i in range(1, 41):
    response = requests.get(url + str(i))
    response.raise_for_status()
    leap_frog = bs4.BeautifulSoup(response.text, 'html.parser')
    print("scraping page: ", i)

    # pulling names from each page of the website
    names = leap_frog.select('div.product-name > a')
    for name in names:
        product_names.append(name.getText())

    # pulling initial price data from website
    pricing = leap_frog.select('div.product-details')
    regex = "SGD\d+.\d\d|Out Of Stock"
    for price in pricing:
        if re.findall(regex, str(price)) == []:
            price_list.append("Missing Data")
        else:
            price_list.append(re.findall(regex, str(price))[0])

dataframe = pd.DataFrame(list(zip(product_names, price_list)), \
                         columns=['product_names', 'price_info'])
dataframe.to_csv('leapfrog.csv', index = False)


