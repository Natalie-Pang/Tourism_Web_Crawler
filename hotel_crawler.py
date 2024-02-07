import re
from playwright.sync_api import sync_playwright
import pandas as pd
import sys
from datetime import datetime
import time

def date_format(date_string):
    pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    return bool(pattern.match(date_string))

def city_choose(city_string):
    pattern = re.compile(r'^(Dubai|London|Amsterdam|Sydney|Dublin|Signapore)$', re.IGNORECASE)
    return bool(pattern.match(city_string))

def is_future_date(checkin_date, checkout_date):
    today = datetime.now().date()
    checkin = datetime.strptime(checkin_date, '%Y-%m-%d').date()
    checkout = datetime.strptime(checkout_date, '%Y-%m-%d').date()

    return checkin >= today and checkout > today

def main():
    with sync_playwright() as p:

        # User picks destination, check-in date, check-out date 
        print('Please enter a destination: (List of available cities: Dubai, London, Amsterdam, Sydney, Dublin, Signapore)')
        city = input()
        while not city_choose(city):
            print('Please only choosen from Dubai, London, Amsterdam, Sydney, Dublin, Signapore')
            city = input()

        print('Please enter a check-in date (yyyy-mm-dd):')
        checkin_date = input()
        while not date_format(checkin_date) or not is_future_date(checkin_date, checkin_date):
            if not date_format(checkin_date):
                print('Please enter a valid check-in date in format (yyyy-mm-dd)')
            else:
                print('Check-in date should be today or in the future.')
            checkin_date = input()

        print('Please enter a check-out date (yyyy-mm--dd):')
        checkout_date = input()
        while not date_format(checkout_date) or not is_future_date(checkin_date, checkout_date) or (datetime.strptime(checkout_date, '%Y-%m-%d').date() < datetime.strptime(checkin_date, '%Y-%m-%d').date()):
            if not date_format(checkout_date):
                print('Please enter a valid check-out date in format (yyyy-mm-dd)')
            elif not is_future_date(checkin_date, checkout_date):
                print('Check-out date should be today or in the future.')
            else:
                print('Check-out date should be after the check-in date.')
            checkout_date = input()
        
        # Web crawling for booking.com
        page_url = f'https://www.booking.com/searchresults.en-us.html?checkin={checkin_date}&checkout={checkout_date}&selected_currency=USD&ss={city}&ssne={city}&ssne_untouched={city}&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_type=city&group_adults=1&no_rooms=1&group_children=0&sb_travel_purpose=leisure'
        browser = p.chromium.launch(headless=False)

        page = browser.new_page()
        page.set_default_timeout(0)
        page.goto(page_url)

        page_counter = 0
        max_page = 5
        hotel_list = []

        while page_counter < max_page:
            time.sleep(10)
            hotels = page.locator('//div[@data-testid="property-card"]').all()

            for hotel in hotels:
                hotel_dict = {}
                hotel_dict['hotel'] = hotel.locator('//div[@data-testid="title"]').inner_text()
                hotel_dict['town'] = hotel.locator('//span[@data-testid="address"]').inner_text()
                hotel_dict['price(USD$)'] = hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text().replace('US$', '')
                hotel_dict['score'] = hotel.locator('//div[@data-testid="review-score"]/div[1]').inner_text()
                hotel_dict["review"] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[1]').inner_text()
                hotel_dict["reviews count"] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[2]').inner_text().replace(' reviews', '')

                hotel_list.append(hotel_dict)

            next_page_button = page.locator('//button[contains(@aria-label, "Next page")]')
            if not next_page_button:
                break

            next_page_button.click()
            page_counter += 1
        browser.close()
        df = pd.DataFrame(hotel_list)
        df.to_excel(f'./results/{city}_{checkin_date}_{checkout_date}_hotel_list.xlsx', index=False)
        df.to_csv(f'./results/{city}_{checkin_date}_{checkout_date}_hotel_list.csv', index=False)

if __name__ == '__main__':
    main()