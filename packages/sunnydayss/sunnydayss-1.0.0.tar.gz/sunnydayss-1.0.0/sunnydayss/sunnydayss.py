import requests

url = "http://api.openweathermap.org/data/2.5/forecast?q=Madrid&APPID=63a51b04a353632e715191c9e629e3de&units=metric"
url2 = "http://api.openweathermap.org/data/2.5/forecast?lat=40.1&lon=3.4&APPID=63a51b04a353632e715191c9e629e3de&units=metric"


class Weather:
    """Creates a Weather object getting an apikey as input
    and either a city name or lat and lon coordinates

    Package use example:

    # Create a weather object using a city name:
    # The api key below is not guaranteed to work
    # Get your own api key from https://openweathermap.org
    # And wait up to a couple of hours for the api key to be activated

    >>> weather1 = Weather(apikey = "63a51b04a353632e715191c9e629e3de", city = "Madrid")

    # Using latituse and longitude coordinates
    >>> weather2 = Weather(apikey = "63a51b04a353632e715191c9e629e3de", lat = 41.1, lon = -4.1)

    # Get complete weather data for the next 12 hours:
    >>> weather1.next_12h()

    # Simplified data for the next 12 hours:
    >>> weather1.next12h_simplified()
    """
    def __init__(self, apikey, city=None, lat=None, lon=None):
        if city:
            url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&APPID={apikey}&units=metric"
            r = requests.get(url)
            self.data = r.json()
        elif lat and lon:
            url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&APPID={apikey}&units=metric"
            r = requests.get(url)
            self.data = r.json()
        else:
            raise TypeError("provide either a city or lat and lon arguments")

        if city and lat and lon:
            print("\nNote: ignoring lat and lon because city argument is present\n")

        if self.data["cod"] != "200":
            raise ValueError(self.data["message"])

    def next_12h(self):
        """Returns 3-hour data for the next 12 hours as a dict.
        """
        return self.data["list"][:4]

    def next_12h_simplified(self):
        """Returns date, temperature, and sky condition every 3 hours
         for the next 12 hours as a tuple of tuples.
         """
        simple_data = []
        for diction in self.data['list'][:4]:
            simple_data.append((diction['dt_txt'], diction['main']['temp'], diction['weather'][0]['description']))
        return simple_data
