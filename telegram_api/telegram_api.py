from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

api_id = '25434637'
api_hash = '48d14547ea6d56c1ce84161b690a863e'
phone_number = '+48791358089'

# Link do grupy, z której chcesz pobrać wiadomości
group_link = 'https://t.me/+NiXKcAp7n743N2Vk'  # Zastąp XXXXX odpowiednim kodem grupy

# Treść wiadomości do wysłania
message_to_send = "Hello from Tele"

with TelegramClient(phone_number, api_id, api_hash) as client:
    client.start()

    # Pobieranie wiadomości z grupy
    group_entity = client.get_entity(group_link)
    messages = client(GetHistoryRequest(
        peer=group_entity,
        limit=100,  # Maksymalna liczba wiadomości do pobrania
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))

    for message in messages.messages:
        if message.text:
            print(message.sender_id, message.text)
        elif message.media:
            if message.photo:
                print(message.sender_id, "[PHOTO]")
            elif message.document:
                if message.document.mime_type == "video/mp4":
                    print(message.sender_id, "[VIDEO]")
                else:
                    print(message.sender_id, "[DOCUMENT]")
            elif message.sticker:
                print(message.sender_id, "[STICKER]")
            # Możesz dodać więcej warunków dla innych typów mediów
        else:
            print(message.sender_id, "[UNKNOWN MESSAGE TYPE]")

    # Wysyłanie wiadomości do grupy
    client.send_message(group_entity, message_to_send)
