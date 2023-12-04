import speech_recognition as sr
import pyttsx3
import pyautogui
import datetime

mic_index = 1
# Initialize the recognizer and engine
r = sr.Recognizer()
engine = pyttsx3.init()

# Set the language settings
lang = 'ru-RU'
engine.setProperty('language', lang)

# Set the wake words
wake_words = ["стеша", "стешка", "стеш,"]

# Use the default microphone
mic = sr.Microphone()

daily_routine = {
    "7:00": "Wake up",
    "7:40": "Breakfast",
    "8:30": "Start School",
    "15:00": "End School",
    "15:30": "Homework",
    "18:00": "walk or cod",
    "22:00": "walk end and deaner",
    "23:00": "taking a shower",
    "00:00": "Bedtime"
}


# Function to listen for wake words
def listen_for_wake_words():
    with sr.Microphone() as mic_source:
        print("Жду слово для пробуждения...")
        r.adjust_for_ambient_noise(mic_source)
        audio = r.listen(mic_source)
        try:
            text = r.recognize_google(audio, language=lang)
            if any(word in text.lower() for word in wake_words):
                print("Слово задетекчено!")
                return True
        except sr.UnknownValueError:
            pass
    return False


def speak(text):
    engine.say(text)
    engine.runAndWait()


def handle_user_input():
    with sr.Microphone() as source:
        print("Слушаю...")
        speak("Я слушаю")  # Add this line to say "I'm listening"
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language=lang)
            print(f"You said: {text}")

            # Handle user input
            if "как дела" in text.lower():
                speak("У меня все хорошо, спасибо. А у вас?")
                with sr.Microphone() as mic_source:
                    r.adjust_for_ambient_noise(mic_source)
                    audio = r.listen(mic_source)
                    try:
                        text = r.recognize_google(audio, language=lang)
                        if "хорошо" in text.lower():
                            speak("Отлично! Чем я могу еще вам помочь?")
                        else:
                            speak("Надеюсь, у вас скоро все наладится. Чем я могу еще вам помочь?")
                    except sr.UnknownValueError:
                        speak("Извините, я не поняла.")
            elif "спасибо" in text.lower():
                speak("Всегда рада помочь. Чем еще могу быть полезна?")
            elif "следующий трек" in text.lower():
                speak("Переключаю на следующий трек.")
                pyautogui.hotkey('shift', 'n')
            elif "предыдущий трек" in text.lower():
                speak("Переключаю на предыдущий трек.")
                pyautogui.hotkey('shift', 'P')
            elif "пауза" in text.lower():
                speak("Ставлю трек на паузу.")
                pyautogui.press('space')
            elif "снять с паузы" in text.lower():
                speak("Снимаю трек с паузы.")
                pyautogui.press('space')  # Press space again to resume playback
            elif "планы" in text.lower():
                now = datetime.datetime.now()
                weekday_name = now.strftime("%A")
                weekday_name_russian = {
                    "Monday": "Понедельник",
                    "Tuesday": "Вторник",
                    "Wednesday": "Среда",
                    "Thursday": "Четверг",
                    "Friday": "Пятница",
                    "Saturday": "Суббота",
                    "Sunday": "Воскресенье"
                }.get(weekday_name, weekday_name)
                today = now.strftime(f"{weekday_name_russian}, %d %B %Y")

                speak(f"Ваши планы на {today} следующие:")
                # Here, you can manually enter your schedule for the day
                speak("7:00 Подъём")
                speak("8:30 Начало школы")
                speak("15:30 Окончание школы")
                speak("16:00 ДЗ")
                speak("18:00 Прогулки или кодинг")
                speak("22:00 Конец прогулки или кодинга, а потом ужин")
                speak("23:00 Принять душ")
                speak("00:00 Сон")

            else:
                speak("Извините, я не могу понять ваш запрос. Попробуйте еще раз.")


        except sr.UnknownValueError:
            print("Извините, я не поняла.")

while True:
    # Listen for wake words


    if listen_for_wake_words():
        # Handle user input
        handle_user_input()
