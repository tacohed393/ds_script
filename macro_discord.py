import pyautogui
import time
import sys
import os

# ================= НАСТРОЙКИ =================

# Имя друга точно так, как оно написано в списке контактов Discord
FRIEND_NAME = "pvnc"

# Текст сообщения. 
# Каждая новая строка будет отправлена как ОТДЕЛЬНОЕ сообщение.
# Пишите прямо так, с переносами:
MESSAGE_TEXT = """
умри
в муках
свинья
йобаная
глухая
пидораска"""

# Задержка между отправкой отдельных сообщений (в секундах)
# Важно: не ставьте меньше 1.5-2.0, иначе Discord может заблокировать спамом
MESSAGE_DELAY = 1

# Координаты кнопки звонка (узнаются через --coords)
# Если не знаете, запустите сначала с флагом --coords
CALL_BUTTON_X = 1360
CALL_BUTTON_Y = 72

# Скорость печати букв (чем меньше, тем быстрее, но лучше не мельчить)
TYPING_SPEED = 0.05

# =============================================

def get_coords_mode():
    print("--- РЕЖИМ ПОЛУЧЕНИЯ КООРДИНАТ ---")
    print("У вас есть 5 секунд, чтобы навести курсор на кнопку звонка в Discord.")
    print("НЕ НАЖИМАЙТЕ ничего, просто наведите!")
    
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    x, y = pyautogui.position()
    print("\n=================================")
    print(f"Координаты получены: X={x}, Y={y}")
    print("Откройте файл macro_discord.py и вставьте эти числа в переменные:")
    print(f"CALL_BUTTON_X = {x}")
    print(f"CALL_BUTTON_Y = {y}")
    print("=================================")

def press_key_combo(keys):
    """Нажимает комбинацию клавиш (например, Win)"""
    if keys == 'win':
        pyautogui.press('win')
    else:
        pyautogui.hotkey(*keys.split())

def find_and_open_discord():
    print("[1/6] Открываем меню Пуск и ищем Discord...")
    
    # Открываем пуск
    pyautogui.press('win')
    time.sleep(1.5)
    
    # Печатаем "discord"
    pyautogui.write('discord', interval=0.1)
    time.sleep(2) # Ждем пока поиск найдет приложение
    
    # Нажимаем Enter, чтобы открыть
    pyautogui.press('enter')
    print("Discord запущен (или активирован). Ждем загрузки...")
    time.sleep(5) # Даем время приложению полностью прогрузиться

def find_friend(friend_name):
    print(f"[2/6] Ищем контакт: {friend_name}...")
    
    # В Discord работает быстрый переход через Ctrl+K (или Cmd+K на Mac)
    # Это универсальный способ найти человека без тыканья мышкой в лупу
    if sys.platform == 'darwin': # Mac
        pyautogui.hotkey('command', 'k')
    else: # Windows/Linux
        pyautogui.hotkey('ctrl', 'k')
    
    time.sleep(1)
    
    # Печатаем имя друга
    pyautogui.write(friend_name, interval=0.1)
    time.sleep(1.5)
    
    # Нажимаем Enter, чтобы перейти в чат
    pyautogui.press('enter')
    time.sleep(1)
    print("Перешли в чат с другом.")

def send_messages_multiline(text):
    print("[3/6] Начинаем отправку сообщений построчно...")
    
    # Разбиваем текст на строки
    lines = text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        print(f"  -> Отправляю: '{line}'")
        
        # Печатаем текст строки
        pyautogui.write(line, interval=TYPING_SPEED)
        
        # Небольшая пауза перед отправкой
        time.sleep(0.5)
        
        # Нажимаем Enter (отправка сообщения)
        pyautogui.press('enter')
        
        # Ждем перед следующим сообщением (защита от спама)
        time.sleep(MESSAGE_DELAY)
        
    print("Все сообщения отправлены!")

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

    print("=== ЗАПУСК МАКРОСА DISCORD ===")
    print("ВНИМАНИЕ: У вас есть 3 секунды, чтобы свернуть все лишнее и быть готовым.")
    print("Не трогайте мышь и клавиатуру после старта!")
    
    for i in range(3, 0, -1):
        print(i)
        time.sleep(1)

    try:
        # 1. Открыть Дискорд
        find_and_open_discord()
        
        # 2. Найти друга
        find_friend(FRIEND_NAME)
        
        # 3. Отправить сообщения (каждая строка - отдельное сообщение)
        send_messages_multiline(MESSAGE_TEXT)
        
        # 4. Позвонить
        make_call(CALL_BUTTON_X, CALL_BUTTON_Y)
        
        print("=== ГОТОВО ===")
        
    except KeyboardInterrupt:
        print("\nПрервано пользователем.")
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")
        print("Убедитесь, что разрешение экрана не менялось и Discord открыт.")

if __name__ == "__main__":
    main()