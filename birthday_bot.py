import os
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError
from datetime import datetime
from zoneinfo import ZoneInfo
import asyncio
import random

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = int(os.environ["TELEGRAM_CHAT_ID"])

MONTHS = {
    "january": 1, "february": 2, "march": 3,
    "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9,
    "october": 10, "november": 11, "december": 12
}

async def check_birthdays_async():
    bot = Bot(token=BOT_TOKEN)
    today = datetime.now(ZoneInfo("Asia/Singapore"))
    today_day = today.day
    today_month = today.month
    
    print(f"📅 Checking birthdays for {today_day} {list(MONTHS.keys())[today_month-1]}")
    
    birthday_people = []  # Collect all birthday names
    
    try:
        async with bot:
            with open("asebirthdaylist.txt", "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        name_part, date_part = line.split("-")
                        name = name_part.strip()
                        
                        day_str, month_str = date_part.strip().split()
                        day = int(day_str)
                        month = MONTHS[month_str.lower()]
                        
                        print(f"  Checking: {name} - {day} {month_str}")
                        
                        if day == today_day and month == today_month:
                            birthday_people.append(name)
                            
                    except Exception as e:
                        print(f"⚠️ Error processing line '{line}': {e}")
            
            # Send one message with all birthday people
            if birthday_people:
                if len(birthday_people) == 1:
                    names = birthday_people[0]
                elif len(birthday_people) == 2:
                    names = f"{birthday_people[0]} and {birthday_people[1]}"
                else:
                    names = ", ".join(birthday_people[:-1]) + f", and {birthday_people[-1]}"
                
                # Get month name for the URL
                month_name = list(MONTHS.keys())[today_month - 1]
                florida_link = f"https://floridamanbirthday.org/{month_name}-{today_day}"
                
                # Random Florida man messages
                florida_messages = [
                    f"Another year older — and already doing better than this Florida man ({florida_link})",
                    f"It's your birthday! Things could be worse… you could be this Florida man ({florida_link})",
                    f"Birthday check: still less wild than this Florida man's day ({florida_link})",
                    f"Today is your birthday. This Florida man had a very different day ({florida_link})",
                    f"One more year wiser. One Florida man, not so much ({florida_link})",
                    f"Your birthday energy > this Florida man's energy ({florida_link})",
                    f"Celebrating you today — not whatever this Florida man was doing ({florida_link})",
                    f"Cake, candles, and zero headlines. Unlike this Florida man ({florida_link})",
                    f"Birthday vibes only. Florida man vibes… elsewhere ({florida_link})",
                    f"Another year older and still doing better than this florida man ({florida_link})",
                    f"birthday status: safer than this florida man's choices ({florida_link})",
                    f"congrats on surviving another year — this florida man struggled ({florida_link})",
                    f"It's your birthday! Let's keep it less chaotic than this Florida man ({florida_link})",
                    f"You made it another year without becoming a Florida Man headline ({florida_link})",
                    f"Celebrate responsibly. This Florida man did not ({florida_link})",
                    f"Big birthday energy. Small Florida man decisions ({florida_link})"
                ]
                
                selected_message = random.choice(florida_messages)
                
                message = (
                    f"🎉🎂 Happy Birthday {names}! 🎂🎉\n"
                    f"{selected_message}"
                )
                await bot.send_message(chat_id=CHAT_ID, text=message)
                print(f"✅ Sent birthday message for: {names}")

            else:
                print("ℹ️ No birthdays today")
                        
    except FileNotFoundError:
        print("❌ Birthday list file not found!")
    except TelegramError as e:
        print(f"❌ Telegram error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def check_birthdays():
    """Synchronous wrapper for scheduler"""
    try:
        asyncio.run(check_birthdays_async())
    except RuntimeError:
        # If event loop already exists
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(check_birthdays_async())
        finally:
            loop.close()

if __name__ == "__main__":
    check_birthdays()
    