from flask import Flask, request, jsonify, render_template
from main import correct_text, count_words  # Import the correct_text and count_words functions

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        data = request.json.get('text')  
        corrected_text = correct_text(data)  # Use the correct_text function
        word_count = count_words(data)  # Get word count
        return jsonify({
            'original_text': data,
            'corrected_text': corrected_text,
            'word_count': word_count  # Return word count
        })
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=6565)
