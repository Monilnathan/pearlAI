from flask import Flask, render_template, request, jsonify
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import os
import re  
import math
from nlp_processor import perform_nlp 

app = Flask(__name__)

EXPLICIT_WORDS = ['pornography', 'adult content', 'explicit', 'xxx', 'porn', 'nsfw', 'sex', 'nude', 'xxx-rated', 'erotic', 'vulgar', 'obscene', 'naked', 'sexual', 'fetish', 'kinky', 'lust', 'seduce', 'orgasm', 'bikini', 'striptease', 'sensual', 'dirty', 'intimate', 'pleasure', 's&m', 'kama sutra', 'dirty talk', 'playboy']



AI_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'AI')

@app.route('/')
def chat():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['message'].lower()  
    response = generate_response(query)
    return jsonify({'response': response})

def generate_response(query):
   
    greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
   
    if any(explicit_word in query for explicit_word in EXPLICIT_WORDS):
        return "I'm sorry, I can't respond to that."
    
    if any(greeting in query for greeting in greetings):
        return "Hello! How can I assist you today?"
    
    
    if 'ampire technologies' in query:
        return "Ampire Technologies is a technological company based and headquartered in Uganda-Kampala located in Katwe Solar House, Level 3. I am one of their products."
    if 'who made you' in query:
        return "I was created by Monil Nathan Wamala, a developer and software engineer in Uganda. He is the CEO of Ampire Technologies Uganda Ltd, the managing director of Monat Media Uganda, and the manager of NAN Cleaning and Fumigation Services."
    elif 'who are your developers' in query:
        return "My developer is Monil Nathan Wamala, a skilled software engineer based in Uganda."
    elif 'who is your father' in query:
        return "My creator and developer is Monil Nathan Wamala."
    elif 'who are you' in query:
        return "Am an AI Assitant. My name is Pearl Bot, inspired that my developer MONIL NATHAN is a Ugandan and Uganda is the Pearl of Africa."
    elif 'what is your name' in query:
        return "My name is Pearl Bot, inspired that my developer MONIL NATHAN is a Ugandan and Uganda is the Pearl of Africa."
    
    elif 'your name' in query:
        return "My name is Pearl Bot, inspired by Uganda, known as the Pearl of Africa."
    elif 'who is tina' in query:
        return "Tina is beautiful angel that fell from heaven."
    elif 'how old are you' in query:
        start_date = datetime(2024, 4, 25, 9, 43)
        current_date = datetime.now()
        age = current_date - start_date
        days = age.days
        minutes = age.seconds // 60
        return f"I am {days} days and {minutes} minutes old."
    elif any(op in query for op in ['+', '-', '*', '/']):
        return calculate(query)
    elif 'are you human' in query or 'are you a human' in query:
        return "No, I am not a human. I am an AI chatbot."
    elif 'location' in query or 'personal data' in query or 'privacy' in query:
        return "I don't have access to your location or any personal data unless you explicitly provide it to me in our conversation. Your privacy and security are important, so I don't retain any personal information about users. How can I assist you today?"
    else:
        tokens, pos_tags, entities = perform_nlp(query)  
        if 'PERSON' in [ent[1] for ent in entities]:
            return "It seems like you're asking about a person. Let me find more information for you."
        else:
            search_results = google_search(query)
            if search_results and is_straight_answer(search_results):
                return make_links_clickable(search_results)
            elif search_results:
                return "-" + make_links_clickable(search_results)
            else:
                return "Sorry, I couldn't find any relevant information for your query."






def make_links_clickable(text):
   
    url_regex = r'(https?://\S+)'

    clickable_text = re.sub(url_regex, r'<a href="\1" target="_blank">\1</a>', text)
    return clickable_text

def evaluate_arithmetic_expression(query):
    arithmetic_pattern = r'(?:what is|calculate|add|subtract|multiply|product of|divide)\s*(\d+)\s*(plus|\+)\s*(\d+)'
    match = re.search(arithmetic_pattern, query)
    if match:
        num1 = int(match.group(1))
        operator = match.group(2)
        num2 = int(match.group(3))

        if operator in {'plus', '+'}:
            return str(num1 + num2)
        elif operator in {'subtract', '-'}:
            return str(num1 - num2)
        elif operator in {'multiply', 'product of', '*'}:
            return str(num1 * num2)
        elif operator == 'divide':
            if num2 == 0:
                return "Division by zero is not allowed."
            else:
                return str(num1 / num2)
    else:
        return None

def calculate(query):

    tokens = re.findall(r'(\d+|\+|\-|\*|\/|sin|cos|tan|sqrt|\^)', query)
    if not tokens:
        return "Invalid arithmetic operation format."

    numbers = []
    functions = []
    for token in tokens:
        if token.isdigit():
            numbers.append(float(token))
        elif token in {'+', '-', '*', '/'}:
            numbers.append(token)
        elif token in {'sin', 'cos', 'tan', 'sqrt'}:
            functions.append(token)
        elif token == '^':
            functions.append('^')

    if '^' in functions:
        index = functions.index('^')
        base = numbers[index]
        exponent = numbers[index + 1]
        result = base ** exponent
        numbers[index] = result
        del numbers[index + 1]
        del functions[index]

    for function in functions:
        if function == 'sin':
            angle = numbers.pop(0)
            numbers.insert(0, math.sin(math.radians(angle)))
        elif function == 'cos':
            angle = numbers.pop(0)
            numbers.insert(0, math.cos(math.radians(angle)))
        elif function == 'tan':
            angle = numbers.pop(0)
            numbers.insert(0, math.tan(math.radians(angle)))
        elif function == 'sqrt':
            operand = numbers.pop(0)
            numbers.insert(0, math.sqrt(operand))

    result = numbers[0]
    for i in range(1, len(numbers), 2):
        operator = numbers[i]
        operand = numbers[i + 1]
        if operator == '+':
            result += operand
        elif operator == '-':
            result -= operand
        elif operator == '*':
            result *= operand
        elif operator == '/':
            if operand == 0:
                return "Division by zero is not allowed."
            result /= operand

    return str(result)


def google_search(query):
    url = f'https://www.google.com/search?q={query}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd')
    if search_results:
        result_text = '\n'.join([result.get_text() for result in search_results])
        return result_text
    else:
        return None

def is_straight_answer(text):
    sentences = text.split('.')
    if len(sentences) == 1:
        return True
    else:
        return False

if __name__ == '__main__':
    app.run(debug=True)