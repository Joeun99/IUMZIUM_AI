from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, ConversationPaused, ConversationResumed, FollowupAction, SessionStarted, ActionExecuted
import random

class ActionResetSlots(Action):

    def name(self) -> str:
        return "action_reset_slots"

    def run(self, dispatcher, tracker, domain):
        # 슬롯 초기화
        events = [
            SlotSet("drink_type", None), 
            SlotSet("temperature", None), 
            SlotSet("size", None),
            SlotSet("syrup", None),
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
                FollowupAction("utter_ask_size")
            ]
        else:
            # 음료가 '아아'가 아닌 경우, 온도를 물어봄
            dispatcher.utter_message(response="utter_ask_temperature")
            return []
        
        
class ActionRecommendMenu(Action):

    def name(self) -> str:
        return "action_recommend_menu"

    def run(self, dispatcher, tracker, domain):
        # 추천할 메뉴 리스트
        menu_options = ["아메리카노", "카페라떼", "카라멜 마끼아또", "연유라떼", "바닐라라떼", "리치캐모마일", "트리플민트"]
        
        # 랜덤으로 메뉴 선택
        recommended_menu = random.choice(menu_options)
        
        # 슬롯에 추천된 메뉴 설정
        dispatcher.utter_message(text=f"오늘의 추천 메뉴는 {recommended_menu}입니다! 한번 시도해보세요! 🍹")
        
        return [SlotSet("recommended_menu", recommended_menu)]
