from flask import Flask, jsonify, render_template, request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import logging
from logging.handlers import RotatingFileHandler
import traceback
import time


app = Flask(__name__)

# List to store received messages
received_messages = []

# Zapisuje wiadomość do pliku tekstowego
def save_to_txt_file(message):
    with open('received_messages.txt', 'a') as file:
        file.write(message + '\n')

# Wyświetla stronę główną z odebranymi wiadomościami
@app.route('/')
def index():
    return render_template('index.html', messages=received_messages)

# Endpoint do monitorowania wiadomości na WhatsApp
@app.route('/monitor', methods=['GET'])
def monitor_messages():
    try:
        target_name = "Test"  # -> Zamienic nazwą uzytkownika lub grupy
        send_and_monitor_whatsapp_message(target_name, "Hello from Flask!")
        app.logger.info(f"Monitoring started for contact: {target_name}")
        return jsonify({"status": "Monitoring started for contact: " + target_name})
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({"status": f"Error: {e}"}), 500

# Inicjalizuje webdriver dla Chrome
def initialize_webdriver():
    service = Service(executable_path='/home/qwe/Pulpit/asystent/wp_api/chromedriver') # do readme.md dodac, ze może być z tym błąd chmod +x /home/qwe/Pulpit/asystent/wp_api/chromedriver3
    options = webdriver.ChromeOptions()
    return webdriver.Chrome(service=service, options=options)

# Otwiera WhatsApp, czeka na zeskanowanie kodu QR i wciśnięcie ENTER
def open_whatsapp_and_scan_qr(driver):
    driver.get('https://web.whatsapp.com/')
    input('Press Enter after scanning QR code..')

# Wybiera czat na podstawie podanej nazwy uzytkownika lub grupy
def select_chat(driver, target):
    chat = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, f"//span[@title='{target}']"))
    )
    chat.click()

# Wysyla wiadomosc do wybranego czatu
def send_message(driver, message):
    message_input = WebDriverWait(driver, 6).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[5]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'))
    )
    message_input.send_keys(message + Keys.ENTER)

# Monitoruje nadchodzace wiadomosci w wybranym czacie
def monitor_incoming_messages(driver):
    last_messages_count = 0
    while True:
        try:
            all_messages = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span._11JPr.selectable-text.copyable-text'))
            )
            
            if len(all_messages) > last_messages_count:
                new_messages = all_messages[last_messages_count:]
                for msg in new_messages:
                    msg_text = msg.text
                    received_messages.append(msg_text)
                    save_to_txt_file(msg_text)
                    app.logger.info(f"Received Message: {msg_text}")
                last_messages_count = len(all_messages)
            
            time.sleep(30)

        except Exception as e:
            app.logger.error(f"Error in monitor_incoming_messages: {e}")
            print(f"Error in monitor_incoming_messages: {e}")
            time.sleep(30)


def send_and_monitor_whatsapp_message(target, message):
    driver = initialize_webdriver()
    try:
        open_whatsapp_and_scan_qr(driver)
        select_chat(driver, target)
        send_message(driver, message)
        monitor_incoming_messages(driver)
    except Exception as e:
        app.logger.error(f"An error occurred in send_and_monitor_whatsapp_message: {e}")
        print(f"An error occurred: {e}")
        print(traceback.format_exc())
    finally:
        driver.quit()


if __name__ == '__main__':
    # Logging configuration
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    log_file = 'server.log'

    log_handler = RotatingFileHandler(log_file, maxBytes=100000, backupCount=10)
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(logging.INFO)

    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(log_handler)
    
    app.run(debug=True)
