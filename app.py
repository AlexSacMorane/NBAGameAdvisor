from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Page d'accueil avec le formulaire
@app.route('/')
def home():
    return render_template('index.html')

# Traitement du formulaire
@app.route('/analyse', methods=['POST'])
def analyse():
    # Récupère la valeur envoyée depuis le champ "valeurs"
    valeurs_str = request.form['valeurs']  # Ex: "1,2,3,4"
    
    # Convertit la chaîne en liste de nombres
    try:
        valeurs = [float(x.strip()) for x in valeurs_str.split(',')]
    except ValueError:
        return "Erreur : veuillez entrer uniquement des nombres séparés par des virgules."

    # Crée un DataFrame pandas et analyse les données
    df = pd.DataFrame({'Valeurs': valeurs})
    resultat_html = df.describe().to_html(classes="table")

    return render_template('index.html', resultat=resultat_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
