def find_target(sentence):
    sentence=sentence.replace('$',' ')
    sentence=sentence.replace('\n',' ')
    sentence=sentence.replace(',',' ')
#     sentence=sentence.replace('.',' ')
    words=(sentence.split(' '))
#     print(words)
    for word in words:
    
        if word.endswith('.near'):
            return (word)
        else:
            pass

import re

# text = "This is a sample text with 123 numbers, 456 and 789."
def find_amount(text):
    text=text.replace(',','')
    amount=0
    try:
        numbers = re.findall(r'\$(\d+)', text)
        numbers=[int(x) for x in numbers]
        if (max(numbers)) >0:
            amount = max(numbers)
            return amount
        else:
            pass 
    except: 
        pass
    try:
        numbers = re.findall(r'\$ (\d+)', text)
        print(numbers)
        numbers=[int(x) for x in numbers]
        if (max(numbers)) >0:
            amount = max(numbers)
            return amount
        else:
            pass 
    except: 
        pass

    try:
        numbers = re.findall(r'(\d+)\$ ', text)
        print(numbers)
        numbers=[int(x) for x in numbers]
        if (max(numbers)) >0:
            amount = max(numbers)
            return amount
        else:
            pass 
    except:
        pass
    try:
        numbers = re.findall(r'(\d+)N', text)
        print(numbers)
        numbers=[int(x) for x in numbers]
        if (max(numbers)) >0:
            amount = max(numbers)
            return amount
        else:
            pass 
    except: 
        pass
    try:
        numbers = re.findall(r'\d+\d+\ USD', text)
        numbers=[int(x.strip('USD')) for x in numbers]
        if (max(numbers)) >0:
            amount = max(numbers)
            return amount
        else:
            pass 
    except:
        pass
    return amount
