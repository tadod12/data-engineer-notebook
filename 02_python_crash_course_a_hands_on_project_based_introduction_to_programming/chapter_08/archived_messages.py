def send_messages(messages):
    sent_messages = []
    while messages:
        message = messages.pop(0)  # first in the list
        print(message)
        sent_messages.append(message)
    return sent_messages


messages = [
    'hi',
    'how are you?',
    'nice to meet you'
]
print(send_messages(messages[:]))
print(messages)
