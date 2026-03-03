from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import random


class ActionMotivationQuote(Action):

    def name(self) -> Text:
        return "action_motivation_quote"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        quotes = [
            "Push yourself because no one else will do it for you.",
            "Dream it. Wish it. Do it.",
            "Success starts with self-discipline.",
            "Don’t stop until you're proud."
        ]

        dispatcher.utter_message(text=random.choice(quotes))
        return []


class ActionLoveQuote(Action):

    def name(self) -> Text:
        return "action_love_quote"

    def run(self, dispatcher, tracker, domain):

        quotes = [
            "Love is composed of a single soul inhabiting two bodies.",
            "Where there is love, there is life.",
            "Love recognizes no barriers.",
            "Love is not what you say, it’s what you do."
        ]

        dispatcher.utter_message(text=random.choice(quotes))
        return []


class ActionSuccessQuote(Action):

    def name(self) -> Text:
        return "action_success_quote"

    def run(self, dispatcher, tracker, domain):

        quotes = [
            "Success is not final, failure is not fatal.",
            "Success is the sum of small efforts repeated daily.",
            "Work hard in silence, let success make the noise.",
            "Don’t watch the clock; do what it does. Keep going."
        ]

        dispatcher.utter_message(text=random.choice(quotes))
        return []


class ActionFunnyQuote(Action):

    def name(self) -> Text:
        return "action_funny_quote"

    def run(self, dispatcher, tracker, domain):

        quotes = [
            "I am not lazy, I am on energy saving mode.",
            "I followed a diet but it didn’t follow me back.",
            "Why don’t scientists trust atoms? Because they make up everything!",
            "My bed and I are perfect for each other."
        ]

        dispatcher.utter_message(text=random.choice(quotes))
        return []