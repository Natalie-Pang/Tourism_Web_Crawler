# Tourism Web Crawler
Tourism Web Crawler is a Python web scraping script for getting desired information (Hotels, Attractions) for toruism. The information extracted will be saved as files with xlsx and csv extension. It is suitable for analysing the extracted data.

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all required packages for the script in terminal.

```bash
pip install -r requirements.txt
```

``` bash
playwright install chromium
```

# Usage
## Attraction Crawler Usage
This script gathers information about attractions in various cities using data from [tripadvisor.com](doc:linking-to-pages#anchor-links).

Navigate to the directory containing attraction_crawler.py
```bash
cd path/to/directory
```

Run the attraction crawler script
```bash
python3 attraction_crawler.py
```

Once the program start running, please choose a check in date and a check out date (please choose a date in the future otherwise it will not work). Then, enter the country name (eg. London, Sydney, Dubai) in the terminal and press return. After entering every information please check the results folder for the generated excel and csv files.

* You can adjust the number of pages to loop through by changing the value of variable max_page

* Please note that you need to either accept or reject cookies in order to get data from TripAdvisor.com.

## Hotel Crawler Usage
This script gathers information about attractions in various cities using data from [booking.com](doc:linking-to-pages#anchor-links).

Navigate to the directory containing hotel_crawler.py
```bash
cd path/to/directory
```

Run the hotel crawler script
```bash
python3 hotel_crawler.py
```

Once the program start running, please enter country name (eg. London, Sydney, Dubai) in the terminal and press return. After entering every information please check the results folder for the generated excel and csv files.

* You can adjust the number of pages to loop through by changing the value of variable max_page

** **

**Disclaimer:** This project is for educational purposes only. The data is obtained from TripAdvisor and Booking.com. Please review and comply with the terms of use of these websites before using this tool extensively.


---

### Note

This project is not affiliated with or endorsed by TripAdvisor or Booking.com. The use of data from these websites should adhere to their respective terms of service.
