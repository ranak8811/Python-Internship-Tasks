import os
import certifi
import time
import csv
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


os.environ['SSL_CERT_FILE'] = certifi.where()

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    return driver

def get_text_by_spec(driver, spec_name):
    try:
        elem = driver.find_element(By.CSS_SELECTOR, f'[data-spec="{spec_name}"]')
        driver.execute_script("arguments[0].scrollIntoView(true);", elem)
        time.sleep(0.5) 
        return elem.text.strip()
    except:
        return "N/A"

def scrape_phone_details(driver, url):
    driver.get(url)
    time.sleep(2)
    
    # scrolling slowly to bottom to ensure everything loads
    total_height = int(driver.execute_script("return document.body.scrollHeight"))
    for i in range(1, total_height, 300):
        driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(0.05)
    
    details = {}
    
    try:
        details['Model'] = driver.find_element(By.CSS_SELECTOR, 'h1.specs-phone-name-title').text.strip()
    except:
        details['Model'] = "Unknown"
        
    details['Release Date'] = get_text_by_spec(driver, "year")
    details['Display Size'] = get_text_by_spec(driver, "displaysize")
    details['Display Res'] = get_text_by_spec(driver, "displayresolution")
    details['Battery'] = get_text_by_spec(driver, "batdescription1")
    details['Main Camera'] = get_text_by_spec(driver, "cam1modules")
    details['Selfie Camera'] = get_text_by_spec(driver, "cam2modules")
    details['Memory'] = get_text_by_spec(driver, "internalmemory")
    details['Price'] = get_text_by_spec(driver, "price")
    
    return details

def scrape_samsung_phones():
    driver = setup_driver()
    base_url = "https://www.gsmarena.com/samsung-phones-9.php"
    
    all_phones_data = []
    
    try:
        print(f"Navigating to {base_url}...")
        driver.get(base_url)
        time.sleep(3)
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        links = driver.find_elements(By.CSS_SELECTOR, '.makers ul li a')
        
        phone_urls = [link.get_attribute('href') for link in links[:27]]
        print(f"Found {len(phone_urls)} phones to scrape.")
        
        for i, url in enumerate(phone_urls, 1):
            print(f"[{i}/{len(phone_urls)}] Scraping {url}...")
            try:
                data = scrape_phone_details(driver, url)
                all_phones_data.append(data)
                print(f"   -> Scraped {data['Model']}")
            except Exception as e:
                print(f"   -> Failed to scrape {url}: {e}")
                
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        
    finally:
        driver.quit()
        
    if all_phones_data:
        csv_file = "samsung_specs.csv"
        headers = ['Model', 'Release Date', 'Display Size', 'Display Res', 'Battery', 'Main Camera', 'Selfie Camera', 'Memory', 'Price']
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(all_phones_data)
            
        print(f"\nSuccessfully saved {len(all_phones_data)} phones to {csv_file}")
    else:
        print("No data collected.")

if __name__ == "__main__":
    scrape_samsung_phones()