from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, ConversationPaused, ConversationResumed, FollowupAction

class ActionResetSlots(Action):

    def name(self) -> str:
        return "action_reset_slots"

    def run(self, dispatcher, tracker, domain):
        # 슬롯 초기화
        events = [
            SlotSet("drink_type", None), 
            SlotSet("temperature", None), 
            SlotSet("quantity", None)
        ]

        # 새로운 주문 시작 안내 메시지 출력
        dispatcher.utter_message(text="새로운 주문을 시작합니다.")

        return events
  
class ActionSetDrinkTypeAndTemperature(Action):

    def name(self) -> str:
        return "action_set_drink_type_and_temperature"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        drink_type = tracker.get_slot("drink_type")

        if drink_type == "아아":
            dispatcher.utter_message(text="Setting drink type to 아메리카노 and temperature to 차갑게")
            return [
                SlotSet("drink_type", "아메리카노"), 
                SlotSet("temperature", "차갑게"), 
                FollowupAction("utter_ask_quantity")
            ]
        else:
            # 음료가 '아아'가 아닌 경우, 온도를 물어봄
            dispatcher.utter_message(response="utter_ask_temperature")
            return []

