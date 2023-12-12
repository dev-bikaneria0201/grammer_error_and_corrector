# # app.py
# from flask import Flask, render_template, request, jsonify
# import requests

# app = Flask(__name__)

# # Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
# OPENAI_API_KEY = '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'
# OPENAI_ENDPOINT = 'https://api.openai.com/v1/completions'

# def get_completion(text):
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {OPENAI_API_KEY}',
#     }

#     data = {
#         'prompt': text,
#         'max_tokens': 150,
#     }

#     try:
#         response = requests.post(OPENAI_ENDPOINT, json=data, headers=headers)
#         response.raise_for_status()  # Raise an exception for bad responses
#         completed_text = response.json()['choices'][0]['text']
#         return completed_text
#     except requests.exceptions.HTTPError as errh:
#         return f"HTTP Error: {errh}"
#     except requests.exceptions.ConnectionError as errc:
#         return f"Error Connecting: {errc}"
#     except requests.exceptions.Timeout as errt:
#         return f"Timeout Error: {errt}"
#     except requests.exceptions.RequestException as err:
#         return f"Error: {err}"

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/complete', methods=['POST'])
# def complete_text():
#     input_text = request.form['text']
#     completed_text = get_completion(input_text)
#     return jsonify({'completed_text': completed_text})

# if __name__ == '__main__':
#     app.run(debug=True)










# from flask import Flask, request, render_template
# import nltk
# from nltk import sent_tokenize, word_tokenize, pos_tag
# from nltk.corpus import wordnet
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer

# app = Flask(__name__)

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('stopwords')

# def get_wordnet_pos(tag):
#     if tag.startswith('N'):
#         return wordnet.NOUN
#     elif tag.startswith('V'):
#         return wordnet.VERB
#     elif tag.startswith('R'):
#         return wordnet.ADV
#     elif tag.startswith('J'):
#         return wordnet.ADJ
#     else:
#         return wordnet.NOUN

# def correct_grammar(paragraph):
#     sentences = sent_tokenize(paragraph)
#     corrected_sentences = []

#     for sentence in sentences:
#         words = word_tokenize(sentence)
#         tagged_words = pos_tag(words)

#         lemmatizer = WordNetLemmatizer()
#         corrected_words = []

#         for word, tag in tagged_words:
#             if word.lower() not in set(stopwords.words('english')):
#                 pos = get_wordnet_pos(tag)
#                 lemma = lemmatizer.lemmatize(word, pos=pos)
#                 corrected_words.append(lemma)

#         corrected_sentence = ' '.join(corrected_words)
#         corrected_sentences.append(corrected_sentence)

#     corrected_paragraph = ' '.join(corrected_sentences)
#     return corrected_paragraph

# # Simple conversation handler
# def respond_to_user(input_text):
#     if "hello" in input_text.lower():
#         return "Hi there! How can I help you today?"
#     elif "how are you" in input_text.lower():
#         return "I'm just a computer program, but thanks for asking!"
#     else:
#         return "I'm not sure how to respond to that. Can you ask me something else?"

# # Chatbot endpoint
# @app.route('/chatbot', methods=['POST'])
# def chatbot():
#     user_message = request.form['user_message']
#     corrected_message = correct_grammar(user_message)
#     bot_response = respond_to_user(corrected_message)
#     return render_template('index.html', user_message=user_message, corrected_message=corrected_message, bot_response=bot_response)

# # Web page with a simple form to interact with the chatbot
# @app.route('/')
# def index():
#     return render_template('index.html', user_message='', corrected_message='', bot_response='')

# if __name__ == '__main__':
#     app.run(debug=True)

















# from flask import Flask, render_template, request

# import openai

# app = Flask(__name__)

# # Set your OpenAI API key
# openai.api_key = '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'

# def grammar_and_spelling_check(user_text):
#     # Use OpenAI GPT-3 for text correction
#     prompt = f"Correct the following text:\n'{user_text}'\n"
#     response = openai.Completion.create(
#         engine="text-davinci-002",  # Choose an appropriate engine
#         prompt=prompt,
#         temperature=0.7,  # Adjust temperature for creativity vs. accuracy
#         max_tokens=150  # Adjust as needed
#     )

#     corrected_text = response.choices[0].text.strip()

#     # Counting the number of changes (basic approach)
#     changes = len([1 for original, corrected in zip(user_text.split(), corrected_text.split()) if original != corrected])

#     return corrected_text, changes

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         user_text = request.form['user_text']
#         corrected_text, changes = grammar_and_spelling_check(user_text)
#         return render_template('index.html', user_text=user_text, corrected_text=corrected_text, changes=changes)
#     else:
#         return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)







# ..........................................







from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = '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'

def grammar_and_spelling_check(user_text):
    # Use OpenAI GPT-3 for text correction
    prompt = f"Correct the following text:\n'{user_text}'\n"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=150
    )

    corrected_text = response.choices[0].text.strip()

    # Counting different types of errors
    user_words = user_text.split()
    corrected_words = corrected_text.split()

    grammar_errors = sum(1 for orig, corr in zip(user_words, corrected_words) if orig != corr and orig.isalpha())
    spelling_errors = sum(1 for orig, corr in zip(user_words, corrected_words) if orig != corr and not orig.isalpha())
    punctuation_errors = sum(1 for orig, corr in zip(user_words, corrected_words) if orig != corr and orig.isalpha() and not corr.isalpha())

    return corrected_text, grammar_errors, spelling_errors, punctuation_errors

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_text = request.form['user_text']
        corrected_text, grammar_errors, spelling_errors, punctuation_errors = grammar_and_spelling_check(user_text)
        return render_template('index.html', user_text=user_text, corrected_text=corrected_text,
                               grammar_errors=grammar_errors, spelling_errors=spelling_errors,
                               punctuation_errors=punctuation_errors)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


# import openai
# from flask import Flask, render_template, request
# app = Flask(__name__)
# # Set your OpenAI API key
# openai.api_key ='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'

# def grammar_and_spelling_check(user_text):
#     # Use OpenAI GPT-3 for text correction
#     prompt = f"Please remove all the grammatical, spelling and punctuation error from the following paragraph and return the corrected paragraph with number of grammatical, spelling and punctuation error found in original paragraph seperately.\n{user_text}\n"
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=150
#     )
#     corrected_text = response.choices[0].text.strip()
#     # Counting different types of errors
#     # user_words = user_text.split()
#     # corrected_words = corrected_text.split()
#     return corrected_text

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         user_text = request.form['user_text']
#         corrected_text= grammar_and_spelling_check(user_text)
#         return render_template('index.html', user_text=user_text, corrected_text=corrected_text)
#     else:
#         return render_template('index.html')

# if __name__== '__main__':
#     app.run(debug=True)



# from flask import Flask, render_template, request
# import openai

# app = Flask(__name__)

# # Set your OpenAI API key
# openai.api_key = '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'

# def grammar_and_spelling_check(user_text, word_limit=100):
#     # Check if the input exceeds the word limit
#     if len(user_text.split()) > word_limit:
#         return "Input exceeds the word limit. Please enter a shorter text."

#     # Use OpenAI GPT-3 for text correction
#     prompt = f"Correct the following text:\n'{user_text}'\n"
#     response = openai.Completion.create(
#         engine="text-davinci-002",
#         prompt=prompt,
#         temperature=0.7,
#         max_tokens=150
#     )

#     corrected_text = response.choices[0].text.strip()

#     # Counting different types of errors
#     user_words = user_text.split()
#     corrected_words = corrected_text.split()

#     grammar_errors = sum(1 for orig, corr in zip(user_words, corrected_words) if orig != corr and orig.isalpha())
#     spelling_errors = sum(1 for orig, corr in zip(user_words, corrected_words) if orig != corr and not orig.isalpha())
#     punctuation_errors = sum(1 for orig, corr in zip(user_words, corrected_words) if orig != corr and orig.isalpha() and not corr.isalpha())

#     return corrected_text, grammar_errors, spelling_errors, punctuation_errors

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         user_text = request.form['user_text']
#         corrected_text, grammar_errors, spelling_errors, punctuation_errors = grammar_and_spelling_check(user_text)
#         return render_template('index.html', user_text=user_text, corrected_text=corrected_text,
#                                grammar_errors=grammar_errors, spelling_errors=spelling_errors,
#                                punctuation_errors=punctuation_errors)
#     else:
#         return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)
