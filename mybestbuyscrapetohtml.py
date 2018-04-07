import re
from urllib.request import urlopen

from bs4 import BeautifulSoup

file_name = "scrapedata\mybestbuy.html"
f = open(file_name, "w")
# headers = "product_name,link"
web_title = "From bestbuy"
headers = "Low Price Unlocked cellphones from bestbuy"

f.write("<title>" + web_title + "</title>" + '\n')
f.write("<h1>" + headers + "</h1>" + '\n')
f.write('*****************************************************************************************************' + '\n')

for i in range(1, 5):
    print("*************************************************************")
    print("This is page {}.".format(i))
    my_url = "https://www.bestbuy.com/site/searchpage.jsp?cp=" + str(
        i) + "&searchType=search&id=pcat17071&nrp=15&sp=%2Bcurrentprice%20skuidsaas&seeAll=&_dyncharset=UTF-8&ks=960&sc=Global&list=y&usc=All%20Categories&type=page&iht=n&browsedCategory=pcmcat156400050037&st=categoryid%24pcmcat156400050037&qp=category_facet%3DAll%20Unlocked%20Cell%20Phones~pcmcat311200050005"
    u_client = urlopen(my_url)
    page_html = u_client.read()
    u_client.close()
    page_soup = BeautifulSoup(page_html, "html.parser")
    match = page_soup.findAll("div", {"class": "list-item"})

    for i in match:
        i1 = str(i)

        list_i = i1.split(" ")
        regu = re.compile(r"(?s)data-attributes='{\"lowPriceGuaranteedProduct\":true}'")
        match1 = re.findall(regu, list_i[3])
        if len(match1) == 1:
            print("Found low price: ", match1)

            # get price
            regu_price = re.compile(r"pb-hero-price pb-purchase-price(.*?)(\d+\.?\d+)</span>")
            match_price = re.search(regu_price, str(i))
            my_price = "$" + match_price.group(2)

            # get link
            link_i = re.findall(r"(?s)(<h4><a.*?/a>)", i1)
            new_link = re.findall(r"(?s)href=\"(.*?)\"", str(link_i))
            st = str(new_link).strip('[\'\']')
            final_link = "https://www.bestbuy.com" + st
            print("Final link: ", final_link)

            # get name
            title = re.search(r"(?s)href=\"(.*?)\"+>(.*?)</a>", str(link_i))
            product_name = title.group(2).replace('amp;', "")
            print("Title is :", product_name)

            f.write('<br>')
            f.write("<h3>" + product_name + "</h3>" + '\n')
            f.write("Price: " + "<lable>" + my_price + "</lable>" + '\n')
            f.write('<br>')
            f.write("<a href=\"" + final_link + "\">Product Link</a>" + '\n')

f.close()
