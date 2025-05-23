# app.py
import flask
import json
import os
from datetime import datetime
from flask import request, redirect, url_for, session, render_template_string

# Initialisation de l'application Flask
app = flask.Flask(__name__)
app.secret_key = 'supersecretkey' # Important pour les messages flash
ADMIN_PASSWORD = "Lolompl34"

# Chemin vers le fichier de données JSON
DATA_FILE = 'data.json'

# Liste prédéfinie des activités MISE À JOUR
PREDEFINED_ACTIVITIES = [
    "Randonnée", "Course à pied", "Vélo", "Yoga", "Promener son chien",
    "Natation", "Lecture", "Jeux de société", "Cuisine", "Dégustation de vins",
    "Instrument de musique", "Jardinage", "Théâtre / cinéma",
    "Jeux de cartes (belote, tarot…)", "Échecs", "Sorties culturelles (musées, expositions…)",
    "Bricolage", "Voyages",
    "Pêche", # Ajouté
    "Wakeboard", # Ajouté
    "Sortie nautique", # Ajouté
    "Football", # Ajouté
    "Squash", # Ajouté
    "Paddle", # Ajouté
    "Badminton" # Ajouté
]

def load_data():
    """Charge les données depuis le fichier JSON. Retourne une liste vide si le fichier n'existe pas."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError: # Gère le cas où le fichier est vide ou malformé
        return []

def save_data(data):
    """Sauvegarde les données dans le fichier JSON."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    """Affiche le formulaire principal."""
    # Passer la fonction now() au template pour l'année en cours dans le footer
    return flask.render_template('index.html', activities=PREDEFINED_ACTIVITIES, now=datetime.utcnow)

@app.route('/submit', methods=['POST'])
def submit_form():
    """Traite les données soumises par le formulaire."""
    try:
        data = flask.request.get_json()

        # Validation simple (peut être étendue)
        required_fields = ['nom', 'prenom', 'email', 'entreprise', 'telephone']
        for field in required_fields:
            if not data.get(field):
                return flask.jsonify({'success': False, 'message': f'Le champ "{field}" est obligatoire.'}), 400

        # Préparation des données à sauvegarder
        member_data = {
            'nom': data.get('nom'),
            'prenom': data.get('prenom'),
            'email': data.get('email'),
            'entreprise': data.get('entreprise'),
            'telephone': data.get('telephone'),
            'activities': {},
            'autres_activites': data.get('autres_activites', ''),
            'chien': data.get('chien', False),
            'enfants_bas_age': data.get('enfants_bas_age', False),
            'enfants_babysitting': data.get('enfants_babysitting', False),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # Récupération des notes pour les activités prédéfinies
        for activity in PREDEFINED_ACTIVITIES:
            # Création d'une clé normalisée pour JavaScript et HTML
            activity_key_js = f"activity_{activity.replace(' ', '_').replace('(', '').replace(')', '').replace('…', '').replace('/', '_')}"
            member_data['activities'][activity] = int(data.get(activity_key_js, 0))


        # Sauvegarde des données
        all_data = load_data()
        all_data.append(member_data)
        save_data(all_data)

        return flask.jsonify({'success': True, 'message': 'Vos informations ont été enregistrées avec succès !'})

    except Exception as e:
        app.logger.error(f"Erreur lors de la soumission: {e}")
        app.logger.error(flask.request.data) # Log raw data for debugging
        return flask.jsonify({'success': False, 'message': f'Une erreur est survenue: {str(e)}'}), 500

@app.route('/admin', methods=['GET', 'POST'])
def admin_view():
    if 'admin_authenticated' not in session:
        if request.method == 'POST':
            password = request.form.get('password', '')
            if password == ADMIN_PASSWORD:
                session['admin_authenticated'] = True
                return redirect(url_for('admin_view'))
            else:
                error = "Mot de passe incorrect."
                return render_template_string('''
                    <form method="post" class="max-w-sm mx-auto mt-16 bg-white p-8 rounded shadow">
                        <h2 class="text-xl font-bold mb-4">Accès Admin</h2>
                        <input type="password" name="password" placeholder="Mot de passe" class="form-input w-full mb-4" required>
                        <button type="submit" class="btn-submit">Se connecter</button>
                        <p class="text-red-600 mt-2">{{ error }}</p>
                    </form>
                ''', error=error)
        return render_template_string('''
            <form method="post" class="max-w-sm mx-auto mt-16 bg-white p-8 rounded shadow">
                <h2 class="text-xl font-bold mb-4">Accès Admin</h2>
                <input type="password" name="password" placeholder="Mot de passe" class="form-input w-full mb-4" required>
                <button type="submit" class="btn-submit">Se connecter</button>
            </form>
        ''')
    data = load_data()
    current_activities_header = PREDEFINED_ACTIVITIES[:]
    return flask.render_template('admin.html', members=data, activities_header=current_activities_header, now=datetime.utcnow)


@app.route('/download')
def download_data():
    """Permet de télécharger les données au format JSON."""
    data = load_data()
    return flask.jsonify(data)

# Point d'entrée pour exécuter l'application
if __name__ == '__main__':
    # Création du dossier templates s'il n'existe pas
    if not os.path.exists('templates'):
        os.makedirs('templates')

    # Message pour indiquer où trouver le fichier HTML (si l'utilisateur doit le créer)
    html_example_path = os.path.join('templates', 'index.html')
    admin_html_example_path = os.path.join('templates', 'admin.html')

    print("Assurez-vous que les fichiers HTML suivants existent dans le dossier 'templates':")
    print(f"- {html_example_path}")
    print(f"- {admin_html_example_path}")
    print("Vous pouvez copier le contenu HTML fourni dans ces fichiers.")
    print(f"Exécutez l'application avec: python {os.path.basename(__file__)}")
    print(f"Accédez au formulaire à l'adresse: http://127.0.0.1:5001/")
    print(f"Accédez à la page admin à l'adresse: http://127.0.0.1:5001/admin")
    
    app.run(debug=True, port=5001) # Utilisation du port 5001 au lieu de 5000
