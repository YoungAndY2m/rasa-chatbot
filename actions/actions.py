# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from weather import Weather, LatLngWeather
from bestguess import Detect_web, Find_location
import replicate
import re


class ActionTellWeather(Action):

    def name(self) -> Text:
        return "action_weather_api"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("reach here - action_weather_api")
        city = tracker.latest_message['text']
        weather_data = Weather(city)
        main = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        temp_min = int(weather_data['main']['temp_min']-273)
        temp_max = int(weather_data['main']['temp_max']-272)
        temp = int(weather_data['main']['temp']-273)
        dispatcher.utter_template("utter_temp", tracker, city=city, temp=temp,
                                  main=main, description=description, temp_min=temp_min, temp_max=temp_max)

        return [SlotSet('city', city), SlotSet('temp', temp)]


class ActionSpecificWeather(Action):

    def name(self) -> Text:
        return "action_latlng_weather_api"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("reach here - action_latlng_weather_api")
        lat = tracker.get_slot('lat')
        lng = tracker.get_slot('lng')
        weather_data = LatLngWeather(lat, lng)
        main = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        temp_min = int(weather_data['main']['temp_min']-273)
        temp_max = int(weather_data['main']['temp_max']-272)
        temp = int(weather_data['main']['temp']-273)
        dispatcher.utter_template("utter_spec", tracker, lat=lat, lng=lng, temp=temp,
                                  main=main, description=description, temp_min=temp_min, temp_max=temp_max)

        return [SlotSet('temp', temp)]


class ActionTravelTemp(Action):

    def name(self) -> Text:
        return "action_travel_suggestion"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("reach here - action_travel_suggestion")
        temp = tracker.get_slot('temp')
        if int(temp) > 25:
            dispatcher.utter_template("utter_temp_high", tracker)
        elif int(temp) > 10:
            dispatcher.utter_template("utter_temp_medium", tracker)
        else: 
            dispatcher.utter_template("utter_temp_low", tracker)
        dispatcher.utter_template("utter_help", tracker)

        return []


class ActionBestGuess(Action):

    def name(self) -> Text:
        return "action_google_guess"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("reach here - action_google_guess")
        path = tracker.latest_message['text']
        paths = [path]
        best_guess = Detect_web(paths)
        print(best_guess)
        result = best_guess[0][0]
        print(result)
        url = best_guess[1][0]
        print(url)
        dispatcher.utter_template("utter_image", tracker, url=url, img=url)
        dispatcher.utter_template("utter_guess", tracker, guess=result)

        return [SlotSet('label', result)]


class ActionGeocode(Action):

    def name(self) -> Text:
        return "action_google_geocode"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("reach here - action_google_geocode")
        place = tracker.get_slot('label')
        lat, lng = Find_location(place)
        print(lat)
        print(lng)
        dispatcher.utter_template(
            "utter_tell_location", tracker, lat=lat, lng=lng)

        return [SlotSet('lat', str(lat)), SlotSet('lng', str(lng))]


class ActionRecall(Action):

    def name(self) -> Text:
        return "action_recall_memory"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("reach here - action_recall_memory")
        place = tracker.get_slot('label')
        lat = tracker.get_slot('lat')
        lng = tracker.get_slot('lng')
        city = tracker.get_slot('city')
        print(f'{place} in lat: {lat} lng: {lng}\nCity is {city}')
        dispatcher.utter_template(
            "utter_recall", tracker, place=place, lat=lat, lng=lng, city=city)

        return []

class ActionPaintPicture(Action):

    def name(self) -> Text:
        return "action_paint_picture"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("reach here - action_paint_picture")
        sentence = tracker.latest_message['text']
        searchObj = re.search(r'(.*) [paint|image|dream] (.*)', sentence, re.M|re.I)
        model = replicate.models.get("stability-ai/stable-diffusion")
        image = model.predict(prompt=searchObj.group(2))[0]
        dispatcher.utter_template("utter_paint", tracker, img=image)

        return []


class ActionPaintCartoon(Action):

    def name(self) -> Text:
        return "action_paint_cartoon"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("reach here - action_paint_cartoon")
        place = tracker.get_slot('label')
        if place is None:
            dispatcher.utter_template("utter_confuse", tracker)
        else: 
            sentence = f"paint a cartoon {place}"
            model = replicate.models.get("stability-ai/stable-diffusion")
            image = model.predict(prompt=sentence)[0]
            dispatcher.utter_template("utter_paint", tracker, img=image)

        return []
