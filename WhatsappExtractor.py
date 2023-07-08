import re
from collections import defaultdict

def strip_emoji(text):
    return text.encode('ascii', 'ignore').decode('ascii')

def process_line(line, last_sender):
    match = re.search(r'\[(.*?), (.*?)\] (.*?): (.*)', line)
    if match:
        date, _, username, message = match.groups()
        message = strip_emoji(message)
        if username == "Replace with Your Whatsapp User Name":
            username = "You"
        return date, f'{username} said: {message}', username
    else:
        return None, strip_emoji(line.strip()), last_sender

def process_file(input_filename, output_filename):
    conversations = defaultdict(lambda: defaultdict(list)) # define a nested dictionary
    last_sender = None
    last_date = None
    with open(input_filename, 'r', encoding='utf-8', errors='ignore') as infile:
        line = infile.readline()
        while line:
            result = process_line(line, last_sender)
            if result:
                date, message, last_sender = result
                if date:
                    last_date = date[6:10]  # Extract the year from the date
                    last_month = date[3:5]  # Extract the month from the date
                    conversations[last_date][last_month].append(message)  # Use the year and month as the key
                else:
                    # if the date is None, then the message is a continuation of the previous message
                    # so we add it to the last message in the list for this sender
                    conversations[last_date][last_month][-1] += ' ' + message
            line = infile.readline()

    for year, months in conversations.items():
        word_count = 0
        file_count = 1
        outfile = open(f'{output_filename}_{year}_part{file_count}.txt', 'w', encoding='utf-8')
        for month in sorted(months.keys()):
            messages = months[month]
            month_message = f'In {month}, ' + ' '.join(messages) + '\n'
            word_count += len(month_message.split())
            if word_count > 500:
                outfile.close()
                file_count += 1
                outfile = open(f'{output_filename}_{year}_part{file_count}.txt', 'w', encoding='utf-8')
                word_count = len(month_message.split())
            outfile.write(month_message)
        outfile.close()

# example usage:
process_file('raw.txt', 'other_persons_name.txt')
