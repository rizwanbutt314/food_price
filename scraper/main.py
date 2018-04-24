import pythonLib
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sqlite3
from common.constants import DATABASE

#Constants
url_filename = "urls.txt"


def insert_data(data):
    print("Inserting data to database...")
    con = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    # Fill the table
    cur.executemany("""insert into business(url, business_name, rating,
                        cuisines, address, p_name, p_sub_name, p_category,
                        p_description, p_price) values (?,?,?,?,?,?,?,?,?,?)""", data)
    conn.commit()
    conn.close()
    print("Completed!")
    

def parse_page(url, soup):
    print("Extracting Data...")
    name = soup.find('h1', {'itemprop': 'name'}).get_text().strip()
    rating = soup.find('meta', {'itemprop': 'ratingValue'})['content']
    cuisines = soup.find('p', {'class': 'cuisines'}).get_text().strip()
    address = soup.find('p', {'itemprop': 'address'}).get_text().strip()

    #Extracting menu items
    menu_container = soup.find('div', {'id': 'menu'})
    products = menu_container.find_all('div', {'class': 'product'})

    products_data = []
    for product in products:
        try:
            category = product.find_previous('h3', {'class': 'categoryName '}).get_text().strip()
            if 'withSynonyms' in product['class']:
                temp_tag = product.find('h4', {'class': 'name '})
                p_name = ""
                s_name = ""
                if temp_tag:
                    p_name = temp_tag.get_text().strip()

                if p_name:
                    s_name = product.find('h5', {'class': 'synonymName '}).get_text().strip()
                else:
                    p_name = product.find('h5', {'class': 'synonymName '}).get_text().strip()
                p_description = ''
                p_price = product.find('p', {'class': 'price '}).get_text().strip()
            else:
                p_name = product.find('h4', {'class': 'name '}).get_text().strip()
                s_name = ""
                p_description  = product.find('p', {'class': 'description '}).get_text().strip()
                p_price = product.find('p', {'class': 'price '}).get_text().strip()

            products_data.append({
                'name': p_name,
                "sub_name": s_name,
                'category': category,
                'description': p_description,
                'price': p_price,
            })
            products_data.append((
                url, name, rating, cuisines, address, p_name, s_name, category, p_description, p_price
                ))
        except Exception as error:
            pass

    insert_data(products_data)
    

def main():
    urls = pythonLib.read_url_file(url_filename)
    driver = webdriver.PhantomJS()
    for url in urls:
        print("URL: "+url)
        driver.get(url)
        time.sleep(3)
        soup = pythonLib.source_to_soup(driver.page_source)
        parse_page(url, soup)

        break


main()
