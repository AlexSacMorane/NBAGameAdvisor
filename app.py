from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyse', methods=['POST'])
def analyse():
    # Exemple simple avec pandas
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    stats = df.describe().to_html()
    return stats

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
