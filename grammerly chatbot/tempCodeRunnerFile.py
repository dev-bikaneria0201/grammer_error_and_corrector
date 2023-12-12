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
