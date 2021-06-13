from typing import Any, Text, Dict, List
from rasa_sdk.events import AllSlotsReset,SlotSet
from rasa_sdk import Action, Tracker,events,FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from typing import Dict, Text, Any, List, Union, Optional
import json
from rasa_sdk.types import DomainDict
import re
import requests


## Below is the action for reseting all slots which are previously filled.

class ActionAllSlotReset(Action):

     def name(self) -> Text:
            return "action_all_slot_reset"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         return [AllSlotsReset()]

## Below action validate that the entered country for checking capital is available in country list or not if country is not available in country list then it shows the alert message.

class ValidateCapitalForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_capital_form"

    def validate_countryname(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Optional[Text]:
    	countr_name = tracker.get_slot('countryname')
    	URL ='https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/getCountries'
    	countr_name = tracker.get_slot('countryname')
    	resp_check_countries = requests.get(url=URL)
    	check_countries = resp_check_countries.json()
    	check_cntr_list = check_countries["body"]
    	if (countr_name in check_cntr_list):
    		return {"countryname" : value}
    	else :
    		dispatcher.utter_message(text="It seems that you have entered wrong country name")
    		return{"countryname" : None}

## Below action validate that the entered country for checking population is available in country list or not if country is not available in country list then it shows the alert message.

class ValidatePopulationForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_population_form"

    def validate_countryname(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Optional[Text]:
    	URL ='https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/getCountries'
    	country_name = tracker.get_slot('countryname')
    	resp_check_country = requests.get(url=URL)
    	check_country = resp_check_country.json()
    	check_country_list = check_country["body"]
    	if (country_name in check_country_list):
    		return {"countryname" : value}
    	else :
    		dispatcher.utter_message(text="It seems that you have entered wrong country name")
    		return{"countryname" : None}

        
## Action for gettting country list and setting the country list to the countries slot.

class ActionGetCountries(Action):

     def name(self) -> Text:
            return "action_get_countries"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
     	URL = 'https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/getCountries'

     	response_countries = requests.get(url=URL)

     	countries_data = response_countries.json()

     	countries_list = countries_data["body"]
     	
     	return [SlotSet('countries',countries_list)]

## Action for fetching the capital of entered country

class ActionGetCapital(Action):

     def name(self) -> Text:
            return "action_know_capital"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
     	 url = 'https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/getCapital'
     	 capital_countryname = tracker.get_slot('countryname')
     	 payload = {'country': capital_countryname}
     	 headers = {'content-type': 'application/json'}
     	 response_capital = requests.post(url, data= json.dumps(payload), headers=headers)
     	 capital_json = response_capital.json()
     	 if capital_json["success"] ==1 :
     	 	countryOne = capital_json["body"]["country"]
     	 	capital = capital_json["body"]["capital"]
     	 	dispatcher.utter_message(text ="Capital of"+" "+countryOne+" "+"is"+" "+capital+" "+".")
     	 else :
     	 	dispatcher.utter_message(text="Sorry we wont be able to found population for"+population_countryname+ " "+"country")
     	 return []

## Action for checking the population of country

class ActionGetPopulation(Action):

     def name(self) -> Text:
            return "action_know_population"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
     	 url = 'https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/getPopulation'
     	 population_countryname = tracker.get_slot('countryname')
     	 payload = {'country': population_countryname}
     	 headers = {'content-type': 'application/json'}
     	 response_population = requests.post(url, data= json.dumps(payload),headers=headers)
     	 population_json = response_population.json()
     	 if population_json["success"] ==1 :
     	 	countryTwo = population_json["body"]["country"]
     	 	population = population_json["body"]["population"]
     	 	dispatcher.utter_message(text="Population of"+" "+countryTwo+" "+"is" +" "+population +" "+".")
     	 else:
     	 	dispatcher.utter_message(text ="Sorry we wont be able to found population for"+population_countryname+ " "+"country")
     	 return []


