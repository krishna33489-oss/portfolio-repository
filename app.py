import os
from flask import Flask, render_template_string, request, jsonify
from textblob import TextBlob

app = Flask(__name__)

landing_page = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Sentiment Analysis</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #000000, #434343);
            color: white;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            text-align: center;
            background: rgba(0, 0, 0, 0.8);
            padding: 60px;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            max-width: 800px;
        }
        h1 {
            font-size: 3rem;
            font-weight: 600;
            color: #00d1b2;
        }
        p {
            font-size: 1.3rem;
            margin-bottom: 30px;
        }
        .btn-enter {
            background-color: #00d1b2;
            color: white;
            padding: 15px 40px;
            font-size: 1.1rem;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        .btn-enter:hover {
            background-color: #00b89c;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Sentiment Analysis</h1>
        <p>Analyze the sentiment of your text!</p>
        <a href="/analyze" class="btn-enter">Start Analyzing</a>
    </div>
</body>
</html>
'''

main_page = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sentiment Analysis</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #1f1c2c, #928dab);
            color: white;
            font-family: Arial, sans-serif;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: #ffffff;
            padding: 40px;
            border-radius: 15px;
            max-width: 800px;
            width: 100%;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
        }
        h1 {
            color: #1f1c2c;
            text-align: center;
            font-weight: bold;
            margin-bottom: 20px;
        }
        textarea {
            width: 100%;
            height: 200px;
            resize: none;
            border-radius: 10px;
            padding: 15px;
            font-size: 16px;
            background: #f9f9f9;
            border: 2px solid #e0e0e0;
        }
        .btn {
            width: 100%;
            padding: 15px;
            font-size: 1.2rem;
            margin-top: 10px;
            border-radius: 8px;
            transition: background-color 0.3s ease;
        }
        .btn-primary {
            background-color: #00d1b2;
            border: none;
        }
        .btn-primary:hover {
            background-color: #00b89c;
        }
        #output {
            margin-top: 30px;
            display: none;
        }
        .tile {
            padding: 20px;
            border-radius: 10px;
            color: white;
            margin-bottom: 15px;
            font-size: 18px;
            font-weight: bold;
        }
        .sentiment-tile {
            background: linear-gradient(135deg, #6a11cb, #2575fc);
        }
        .confidence-tile {
            background: linear-gradient(135deg, #ff512f, #dd2476);
            position: relative;
            overflow: hidden;
        }
        .confidence-bar {
            position: absolute;
            top: 0;
            left: 0;
            height: 100%;
            background-color: rgba(255, 255, 255, 0.2);
        }
        .description-tile {
            background: linear-gradient(135deg, #36d1dc, #5b86e5);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Sentiment Analysis</h1>
        <div class="mb-3">
            <textarea id="input_text" placeholder="Type or paste your text here..."></textarea>
        </div>
        <div class="d-grid">
            <button class="btn btn-primary" onclick="analyzeSentiment()">Analyze Sentiment</button>
        </div>
        <div id="output">
            <div class="tile sentiment-tile">
                Sentiment: <span id="sentiment"></span>
            </div>
            <div class="tile confidence-tile">
                Confidence Level: <span id="confidence"></span>
                <div class="confidence-bar" id="confidence-bar"></div>
            </div>
            <div class="tile description-tile">
                Description: <span id="description"></span>
            </div>
        </div>
    </div>

    <script>
        function analyzeSentiment() {
            const inputText = document.getElementById('input_text').value;
            if (inputText === '') {
                alert('Please enter some text.');
                return;
            }

            fetch('/perform_analysis', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `text=${encodeURIComponent(inputText)}`
            })
            .then(response => response.json())
            .then(data => {
                const output = document.getElementById('output');
                const sentiment = document.getElementById('sentiment');
                const confidence = document.getElementById('confidence');
                const description = document.getElementById('description');
                const confidenceBar = document.getElementById('confidence-bar');

                output.style.display = 'block';
                sentiment.innerText = data.sentiment;
                confidence.innerText = data.confidence + '%';

                confidenceBar.style.width = data.confidence + '%';
                confidenceBar.style.backgroundColor = `rgba(255, 255, 255, ${data.confidence / 100})`;

                description.innerText = data.description;
            })
            .catch(error => console.error('Error:', error));
        }
    </script>
</body>
</html>
'''

@app.route('/')
def landing():
    return render_template_string(landing_page)

@app.route('/analyze')
def analyze():
    return render_template_string(main_page)

@app.route('/perform_analysis', methods=['POST'])
def perform_analysis():
    text = request.form['text']
    analysis = TextBlob(text)

    polarity = analysis.sentiment.polarity
    confidence = abs(polarity) * 100

    if polarity > 0:
        sentiment = "Positive"
        description = f"The sentiment of the text is positive, indicating optimism and favorable feelings. Confidence is high due to the positive polarity of {polarity:.2f}."
    elif polarity < 0:
        sentiment = "Negative"
        description = f"The sentiment of the text is negative, showing pessimism or unfavorable feelings. Confidence is calculated based on the negative polarity of {polarity:.2f}."
    else:
        sentiment = "Neutral"
        description = "The sentiment of the text is neutral, neither positive nor negative. Confidence is low due to the balanced nature of the text."

    return jsonify({
        'sentiment': sentiment,
        'confidence': round(confidence, 2),
        'description': description
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
