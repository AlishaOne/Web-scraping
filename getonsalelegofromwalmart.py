# price-saving-block
# Out of stock
# class="product-sub-title-block product-out-of-stock"
# href="/ip/LEGO-Star-Wars-Imperial-Trooper-Battle-Pack-75165/55126217"


import re
from urllib.request import urlopen

from bs4 import BeautifulSoup

file_name = "scrapedata\legofromwalmart.csv"
f = open(file_name, "w")
headers = "Product_name,Link,Sale price"
f.write(headers + '\n')

#get pages from page1 to page i
for i in range(1, 5):
    print("*************************************************************")
    print("This is page {}.".format(i))
    my_url = "https://www.walmart.com/search/?cat_id=0&facet=retailer%3AWalmart.com&grid=true&page="+str(i)+"&query=star+wars+lego+sets+clearance&typeahead=star+wars+lego+sets&vertical_whitelist=home%2C#searchProductResult"
    u_client = urlopen(my_url)
    page_html = u_client.read()
    u_client.close()
    page_soup = BeautifulSoup(page_html, "html.parser")
    match = page_soup.find_all("ul", {"class": "search-result-gridview-items"})

    for i in match:
        for l in i.find_all("li"):

            save_price = l.find("span",
                                {"class": "display-inline-block arrange-fit Price u-textColor price-saving"})
            final_price = l.find("div", {"class": "price-main-block"})
            # print("final price ",final_price)

            get_link = l.find("a")
            print("*************************************************************")

            #only get data if price is onsale
            if save_price is not None:
                #get name
                name = l.div.div.span.text.strip()
                print("Name :", name)

                #get price
                price_list = str(final_price)
                get_price = re.findall(r"(?s)title=\"(\$\d+.\d+)\s?", price_list)
                price = get_price[0].strip()
                print("get price:", price)

                #get link
                link_list = str(get_link)
                match_link = re.findall(r"(?s)href=\"(.*?)\"", link_list)
                final_link = "https://www.walmart.com" + match_link[0]
                link=final_link.replace("amp;", "")
                print("link: ", link)

                f.write(name + ',' + link + ',' + price + '\n')

f.close()
