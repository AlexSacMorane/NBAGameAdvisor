from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
 return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
 return render_template('500.html'), 500

# Page d'accueil avec le formulaire
@app.route('/')
def home():
    return render_template('index.html')

# Traitement du formulaire
@app.route('/analyse', methods=['POST'])
def analyse():
    # Date du jour à interroger (format MM/DD/YYYY)
    game_date = datetime.now() - timedelta(days=1)

    # Endpoint NBA Stats
    url = 'https://stats.nba.com/stats/scoreboardv2'

    # Paramètres requis
    params = {
        'GameDate': game_date,
        'LeagueID': '00',
        'DayOffset': '0'
    }

    # En-têtes importants pour éviter d'être bloqué
    headers = {
        'Host': 'stats.nba.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="120", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.nba.com/',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://www.nba.com'
    }

    # Requête GET
    response = requests.get(url, headers=headers, params=params, timeout=10)

    if response.status_code == 200:
        data = response.json()

    # Extraire les scores par équipe
    line_score = next(rs for rs in data['resultSets'] if rs['name'] == 'LineScore')
    df_line = pd.DataFrame(line_score['rowSet'], columns=line_score['headers'])

    # Regrouper les lignes deux par deux (home/away)
    games = df_line.groupby('GAME_ID')

    # check there are games
    if len(games) != 0:
        result_html = ''
        
        for game_id, game_df in games:
            if len(game_df) == 2:
                team1 = game_df.iloc[0]
                team2 = game_df.iloc[1]

                result_html = result_html + f"\t{team1['TEAM_ABBREVIATION']} @ {team2['TEAM_ABBREVIATION']} \n"

    return render_template('index.html', resultat=result_html)


# Traitement du formulaire (template)
@app.route('/analyse_old', methods=['POST'])
def analyse_old():
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
