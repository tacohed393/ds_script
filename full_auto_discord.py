import pyautogui
import time
import sys
import os

# ================= НАСТРОЙКИ =================
# Имя пользователя точно так, как оно написано в списке контактов Discord
TARGET_USER = "ИмяПользователя"

# Текст сообщения (слова разделяются пробелами, скрипт сам поставит переносы)
MESSAGE_TEXT = "привет как дела у тебя все хорошо"

# Задержка между действиями (увеличьте, если ПК медленный или Дискорд тормозит)
PAUSE_BETWEEN_ACTIONS = 1.5
TYPING_SPEED = 0.1  # Скорость печати букв

# Координаты кнопки звонка (УЗНАТЬ ЧЕРЕЗ РЕЖИМ --find-coords)
# Пример: CALL_BUTTON_X = 1800, CALL_BUTTON_Y = 150
CALL_BUTTON_X = None
CALL_BUTTON_Y = None

# =============================================

def type_word_by_word(text):
    """Пишет текст по одному слову с нажатием Enter после каждого"""
    words = text.split()
    for word in words:
        pyautogui.write(word, interval=TYPING_SPEED)
        pyautogui.press('enter')
        time.sleep(PAUSE_BETWEEN_ACTIONS) # Пауза чтобы не забанили за спам

def find_discord_app():
    """Ищет приложение Discord через меню Пуск"""
    print("[*] Открываю поиск Windows...")
    pyautogui.press('win')
    time.sleep(1)
    pyautogui.write('discord')
    time.sleep(1)
    pyautogui.press('enter')
    print("[*] Запускаю Discord...")
    
    # Ждем пока дискорд откроется (можно настроить время)
    time.sleep(5) 
    print("[*] Discord должен быть открыт.")

def search_user_in_discord(username):
    """Использует встроенный поиск Discord (Ctrl+K)"""
    print(f"[*] Ищу пользователя: {username}")
    
    # Горячая клавиша быстрого перехода в Discord
    pyautogui.hotkey('ctrl', 'k')
    time.sleep(0.5)
    
    # Печатаем имя
    pyautogui.write(username, interval=0.1)
    time.sleep(1)
    
    # Выбираем первого в списке (обычно это нужный человек)
    pyautogui.press('enter')
    print("[*] Перехожу в чат...")
    time.sleep(1)

def make_call(x, y):
    """Нажимает на кнопку звонка по координатам"""
    if x is None or y is None:
        print("[!] ОШИБКА: Координаты кнопки звонка не заданы!")
        print("[!] Запустите скрипт с флагом --find-coords, чтобы узнать их.")
        return False
    
    print(f"[*] Навожу курсор на кнопку звонка (координаты: {x}, {y})...")
    pyautogui.moveTo(x, y, duration=1)
    time.sleep(0.5)
    pyautogui.click()
    print("[*] ЗВОНОК НАЧАТ!")
    return True

def calibrate_coordinates():
    """Режим калибровки координат"""
    print("=== РЕЖИМ КАЛИБРОВКИ ===")
    print("1. Откройте Discord вручную.")
    print("2. Зайдите в ЛЮБОЙ чат с человеком.")
    print("3. Наведите курсор мыши на кнопку видеозвонка (или аудиозвонка).")
    print("4. НЕ НАЖИМАЙТЕ ничего, просто держите курсор.")
    print("Координаты будут выведены через 5 секунд...")
    
    for i in range(5, 0, -1):
        print(f"{i}...", end=" ", flush=True)
        time.sleep(1)
    print()
    
    x, y = pyautogui.position()
    print("\n=========================")
    print(f"ВАШИ КООРДИНАТЫ: X={x}, Y={y}")
    print("Скопируйте эти числа в файл скрипта в переменные CALL_BUTTON_X и CALL_BUTTON_Y")
    print("=========================")

def main():
    # Проверка флагов запуска
    if len(sys.argv) > 1 and sys.argv[1] == "--find-coords":
        calibrate_coordinates()
        return

    # Проверка настроенных координат
    if CALL_BUTTON_X is None or CALL_BUTTON_Y is None:
        print("[!] Ошибка: Сначала настройте координаты кнопки звонка!")
        print("[!] Запустите: python full_auto_discord.py --find-coords")
        print("[!] Затем отредактируйте файл и вставьте значения в CALL_BUTTON_X и CALL_BUTTON_Y")
        return

    # Настройка безопасности PyAutoGUI
    pyautogui.FAILSAFE = True # Если дернуть мышку в угол экрана - скрипт остановится
    pyautogui.PAUSE = 0.5     # Стандартная пауза между командами

    print("--- ЗАПУСК АВТОМАТИЗАЦИИ ---")
    print("У вас есть 3 секунды, чтобы свернуть лишние окна (не обязательно)...")
    time.sleep(3)

    try:
        # Шаг 1: Открыть Дискорд
        find_discord_app()
        
        # Шаг 2: Найти пользователя
        search_user_in_discord(TARGET_USER)
        
        # Небольшая пауза, чтобы интерфейс обновился
        time.sleep(1)
        
        # Фокус на поле ввода (иногда нужно кликнуть в центр экрана чата сначала)
        # Эмуляция клика в центр текущего окна (примерно) чтобы активировать ввод
        screen_w, screen_h = pyautogui.size()
        pyautogui.click(screen_w // 2, screen_h // 2 + 100) 
        time.sleep(0.5)

        # Шаг 3: Отправить сообщения
        print("[*] Начинаю отправку сообщений...")
        type_word_by_word(MESSAGE_TEXT)
        
        # Шаг 4: Позвонить
        time.sleep(1)
        make_call(CALL_BUTTON_X, CALL_BUTTON_Y)
        
        print("--- ГОТОВО ---")
        
    except KeyboardInterrupt:
        print("\n[!] Прервано пользователем")
    except Exception as e:
        print(f"\n[!] Произошла ошибка: {e}")
        print("Убедитесь, что у скрипта есть права на управление экраном (особенно на Mac/Linux).")

if __name__ == "__main__":
    main()