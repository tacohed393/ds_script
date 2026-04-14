import pyautogui
import time
import sys

# НАСТРОЙКИ
# -----------------------------------------------------------------------------
# ВНИМАНИЕ: Используйте тройные кавычки для многострочного текста.
# Каждая новая строка будет отправлена как ОТДЕЛЬНОЕ сообщение.
MESSAGE_TEXT = """привет
как дела
что делаешь
бибабоба"""

CALL_BUTTON_X = 0  # Сюда вставить X координату кнопки звонка (замерить через --coords)
CALL_BUTTON_Y = 0  # Сюда вставить Y координату кнопки звонка

PAUSE_BETWEEN_MESSAGES = 2.0  # Пауза между сообщениями (сек). Не ставьте меньше 1.5!
TYPING_SPEED = 0.05           # Скорость печати букв (сек)
START_DELAY = 5               # Время до старта, чтобы успеть переключиться
# -----------------------------------------------------------------------------

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

def type_message_line_by_line(text):
    # Разбиваем текст на строки
    lines = text.strip().split('\n')
    print(f"Начинаю отправку {len(lines)} сообщений...")
    
    # Небольшая пауза перед стартом, чтобы убедиться, что фокус на поле ввода
    time.sleep(1)
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        pyautogui.write(line, interval=TYPING_SPEED)
        pyautogui.press('enter')
        time.sleep(PAUSE_BETWEEN_MESSAGES) # Пауза между сообщениями

def make_call(x, y):
    if x == 0 and y == 0:
        print("Координаты звонка не заданы. Пропускаю звонок.")
        return

    print(f"Попытка позвонить по координатам: {x}, {y}")
    # Сохраняем текущую позицию, чтобы вернуть курсор потом (опционально)
    current_x, current_y = pyautogui.position()
    
    pyautogui.moveTo(x, y, duration=0.5) # Плавно двигаем мышь
    time.sleep(0.5)
    pyautogui.click()
    
    # Возвращаем курсор обратно (необязательно)
    pyautogui.moveTo(current_x, current_y, duration=0.5)
    print("Клик выполнен.")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--coords":
        get_coordinates()
        return

    print("--- Discord Макрос ---")
    print(f"Текст (по строкам): {MESSAGE_TEXT}")
    print(f"Пауза между сообщениями: {PAUSE_BETWEEN_MESSAGES} сек")
    print(f"До старта осталось {START_DELAY} сек. Быстро переключитесь на окно Discord!")
    print("ВАЖНО: Не трогайте мышь и клавиатуру во время работы скрипта.")
    
    # Обратный отсчет
    for i in range(START_DELAY, 0, -1):
        print(f"{i}...", end=' ', flush=True)
        time.sleep(1)
    print("\nПоехали!")

    # 1. Отправка сообщений
    type_message_line_by_line(MESSAGE_TEXT)
    
    print("Сообщения отправлены.")
    
    # 2. Звонок (если заданы координаты)
    # Добавляем паузу перед звонком, чтобы последние сообщения ушли
    time.sleep(2)
    make_call(CALL_BUTTON_X, CALL_BUTTON_Y)

    print("Готово.")

if __name__ == "__main__":
    main()