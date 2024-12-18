import requests
from bs4 import BeautifulSoup
import json

# Step 1: Send request to PakWheels main page
url = "https://www.pakwheels.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

def get_used_cars_structure(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    cars = []
    car_elements = soup.find_all('div', class_='cards-content')

    for car in car_elements:
        title_tag = car.find('h3', class_='nomargin truncate')
        price_tag = car.find('div', class_='generic-green')
        location_tag = car.find('div', class_='generic-gray')

        if title_tag and price_tag and location_tag:
            title = title_tag.text.strip()
            price = price_tag.text.strip()
            location = location_tag.text.strip()

            cars.append({
                'Title': title,
                'Price': price,
                'Location': location
            })

    return cars

def scrape_car_data(url):
    car_data = []

    # Send a GET request to the webpage
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        car_listings = soup.find_all('li', class_='col-md-3')

        for car in car_listings:
            title = car.find('h3', class_='nomargin truncate').text.strip() if car.find('h3', class_='nomargin truncate') else "N/A"
            
            # Extract price
            price_element = car.find('div', class_='generic-green truncate fs14')
            price = price_element.text.strip() if price_element else "N/A"
            
            # Extract rating (if available)
            rating_element = car.find('span', class_='rating')
            rating_value = 0
            if rating_element:
                rating = rating_element.find_all('i')
                rating_value = sum(1 if 'fa-star' in str(r) else 0 for r in rating)

            # Extract review count (if available)
            reviews_count_element = car.find('span', class_='fs14 generic-gray ml5 dib')
            reviews_count = reviews_count_element.text.strip() if reviews_count_element else "N/A"

            car_data.append({
                'Title': title,
                'Price': price,
                'Rating': rating_value,
                'Reviews Count': reviews_count
            })
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
    
    return car_data

def scrape_bike_data(url):
    bike_data = []

    # Send a GET request to the webpage
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        bike_listings = soup.find_all('li', class_='col-md-3')

        for bike in bike_listings:
            title = bike.find('h3', class_='nomargin truncate').text.strip() if bike.find('h3', class_='nomargin truncate') else "N/A"
            
            # Extract price
            price_element = bike.find('div', class_='generic-green')
            price = price_element.text.strip() if price_element else "N/A"
            
            # Extract location
            location_element = bike.find('div', class_='generic-gray')
            location = location_element.text.strip() if location_element else "N/A"

            bike_data.append({
                'Title': title,
                'Price': price,
                'Location': location
            })
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
    
    return bike_data

# URLs for different sections
url_used_cars = "https://www.pakwheels.com/used-cars/"
url_new_cars = "https://www.pakwheels.com/new-cars/best-sedan/"
url_used_bikes = "https://www.pakwheels.com/used-bikes/"

# Scrape data from each section
used_cars_data = get_used_cars_structure(url_used_cars)
new_cars_data = scrape_car_data(url_new_cars)
bikes_data = scrape_bike_data(url_used_bikes)

# Save the data to JSON files
with open('used_cars.json', 'w') as f:
    json.dump(used_cars_data, f, indent=4)
with open('new_cars.json', 'w') as f:
    json.dump(new_cars_data, f, indent=4)
with open('bikes.json', 'w') as f:
    json.dump(bikes_data, f, indent=4)
