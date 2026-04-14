import pyautogui
import time
import sys

# НАСТРОЙКИ
# Текст, который нужно отправить. Слова будут разделены переносом строки.
MESSAGE_TEXT = "привет как дела надеюсь у тебя все хорошо"
# Задержка между нажатиями клавиш (в секундах). Не ставьте 0, чтобы не забанили за спам.
TYPING_DELAY = 1.5 
# Задержка перед началом (чтобы успеть переключиться на окно Discord)
START_DELAY = 5

# Координаты кнопки звонка (ОЧЕНЬ ВАЖНО: их нужно узнать заранее)
# Если координаты (0, 0), скрипт пропустит шаг со звонком и просто напишет сообщения.
CALL_BUTTON_X = 0 
CALL_BUTTON_Y = 0

def get_coordinates():
    """Функция для получения координат мыши. Запустите скрипт с аргументом --coords чтобы использовать её."""
    print("Наведите мышку на кнопку звонка в Discord и нажмите Ctrl+C в этом окне через 5 секунд...")
    try:
        for i in range(5, 0, -1):
            print(f"{i}...", end=' ', flush=True)
            time.sleep(1)
        x, y = pyautogui.position()
        print(f"\nКоординаты: X={x}, Y={y}")
        print("Скопируйте эти значения в переменные CALL_BUTTON_X и CALL_BUTTON_Y в скрипте.")
    except KeyboardInterrupt:
        print("\nОтменено.")

def type_message_word_by_word(text):
    words = text.split()
    print(f"Начинаю отправку {len(words)} сообщений...")
    
    # В Discord работает быстрый переход через Ctrl+K (или Cmd+K на Mac)
    # Это универсальный способ найти человека без тыканья мышкой в лупу
    if sys.platform == 'darwin': # Mac
        pyautogui.hotkey('command', 'k')
    else: # Windows/Linux
        pyautogui.hotkey('ctrl', 'k')
    
    time.sleep(1)
    
    for word in words:
        pyautogui.write(word)
        pyautogui.press('enter')
        time.sleep(TYPING_DELAY) # Пауза между сообщениями

def make_call(x, y):
    if x == 0 and y == 0:
        print("[!] ОШИБКА: Координаты кнопки звонка не заданы!")
        print("Запустите скрипт с флагом --coords, чтобы узнать их.")
        return

    print("[4/6] Совершаем звонок...")
    time.sleep(1)
    
    # Двигаем мышь к кнопке
    pyautogui.moveTo(x, y, duration=1)
    time.sleep(0.5)
    
    # Кликаем
    pyautogui.click()
    print("Клик по кнопке звонка выполнен!")

def main():
    # Проверка аргументов
    if len(sys.argv) > 1 and sys.argv[1] == '--coords':
        get_coords_mode()
        return

    print("--- Discord Макрос ---")
    print(f"Текст: {MESSAGE_TEXT}")
    print(f"Задержка между словами: {TYPING_DELAY} сек")
    print(f"До старта осталось {START_DELAY} сек. Быстро переключитесь на окно Discord и кликните в поле ввода!")
    
    for i in range(3, 0, -1):
        print(i)
        time.sleep(1)
    print("\nПоехали!")

    # 1. Отправка сообщений
    type_message_word_by_word(MESSAGE_TEXT)
    
    print("Сообщения отправлены.")
    
    # 2. Звонок (если заданы координаты)
    # Добавляем паузу перед звонком, чтобы последние сообщения ушли
    time.sleep(2)
    make_call(CALL_BUTTON_X, CALL_BUTTON_Y)

    print("Готово.")

if __name__ == "__main__":
    main()