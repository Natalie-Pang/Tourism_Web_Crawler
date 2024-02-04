import re
from playwright.sync_api import sync_playwright
import pandas as pd
import sys

def city_choose(city_string):
    pattern = re.compile(r'^(Dubai|London|Amsterdam|Sydney|Dublin|Signapore)$', re.IGNORECASE)
    return bool(pattern.match(city_string))

def city_choose(city_string):
    city_mapping = {
        'london': 'g186338-Activities-oa0-London_England',
        'dubai': 'g186605-Activities-oa0-Dublin_County_Dublin',
        'amsterdam': 'g188590-Activities-oa0-Amsterdam_North_Holland_Province',
        'sydney': 'g255060-Activities-oa0-Sydney_New_South_Wales',
        'dublin': 'g186605-Activities-oa0-Dublin_County_Dublin',
        'singapore': 'g294265-Activities-oa0-Singapore',
    }

    normalized_city = city_string.lower()

    if normalized_city in city_mapping:
        return True, city_mapping[normalized_city]
    else:
        return False, None


def main():
    with sync_playwright() as p:

        # User picks destination, check-in date, check-out date 
        print('Please enter a destination: (List of available cities: Dubai, London, Amsterdam, Sydney, Dublin, Signapore)')
        city = input()
        valid_city, city_code = city_choose(city)
        while not valid_city:
            print('Please only choose from Dubai, London, Amsterdam, Sydney, Dublin, Singapore')
            city = input()
            valid_city, city_code = city_choose(city)
        print(f'TripAdvisor city code for {city.capitalize()}: {city_code}')
        # Web crawling for booking.com
        page_url = f'https://www.tripadvisor.co.uk/Attractions-{city_code}.html'

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()
        page.goto(page_url, timeout=60000)

        attractions = page.locator('.jemSU article.GTuVU').all()

        attraction_list = []
        for attraction in attractions:
            attraction_dict = {}
            attraction_dict['name'] = attraction.locator('.XfVdV').inner_text().lstrip('0123456789. ')
            attraction_dict['type'] = attraction.locator('.biGQs._P.pZUbB.hmDzD').first.inner_text()
            attraction_dict['location'] = attraction.locator('.biGQs._P.pZUbB.hmDzD').nth(1).inner_text().replace('Open now', 'Unknown')
            attraction_dict['reviews count'] = attraction.locator('.biGQs._P.pZUbB.osNWb').inner_text()

            attraction_list.append(attraction_dict)
        
        browser.close()
        df = pd.DataFrame(attraction_list)
        df.to_excel(f'./results/{city.lower()}_attraction_list.xlsx', index=False)
        df.to_csv(f'./results/{city.lower()}_attraction_list.csv', index=False)

if __name__ == '__main__':
    main()