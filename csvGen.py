import pandas as pd
import io

# Création d'un DataFrame pandas pour structurer les données de suivi des recommandations.
# Les colonnes sont définies selon les besoins évoqués dans la réunion.

# Définition des colonnes pour le suivi
columns = [
    "Date Recommandation", # Date à laquelle la recommandation a été faite
    "Membre Recommandant", # Nom du membre du club qui fait la recommandation
    "Membre Recommandé",   # Nom du membre du club qui est recommandé
    "Contact Recommandé (Nom/Société)", # Nom de la personne ou société externe recommandée
    "Détails/Besoin du Contact", # Brève description du besoin ou du contexte de la recommandation
    "Date Dernier Suivi", # Date de la dernière action ou mise à jour concernant cette recommandation
    "Statut",             # Statut actuel de la recommandation (ex: Nouveau, En cours, Succès, Échec, Abandonné)
    "Description Succès (Qualitatif)", # Si succès, description non chiffrée (ex: "Contrat signé pour X", "Mise en relation effectuée")
    "Notes"               # Espace pour des commentaires additionnels
]

# Création d'un DataFrame vide avec les colonnes définies
df_suivi_recos = pd.DataFrame(columns=columns)

# Ajout de quelques exemples pour illustrer l'utilisation
# Ces données sont fictives et servent de démonstration.
example_data = [
    ["2025-04-29", "Laurent Serres", "Marie Malagnou", "Société Exemple A", "Recherche de nouveaux bureaux 150m²", "2025-04-30", "En cours", "", "Premier contact établi."],
    ["2025-04-30", "Charles Mancini", "Aurélien Etienne", "Contact Pro B", "Besoin d'assurance RC Pro", "2025-04-30", "Nouveau", "", "Doit être contacté semaine prochaine."],
    ["2025-03-15", "Andric", "Charles Mancini", "Restaurant Le Sud", "Prestation de nettoyage post-travaux", "2025-04-10", "Succès", "Contrat de nettoyage signé", "Client satisfait."],
    ["2025-02-10", "Marie Malagnou", "Laurent Serres", "Startup Innovante C", "Besoin de coaching commercial", "2025-03-01", "Abandonné", "", "Le contact n'a plus donné suite."]
]

# Ajout des données d'exemple au DataFrame
for record in example_data:
    df_suivi_recos.loc[len(df_suivi_recos)] = record

# Conversion de la colonne 'Date Recommandation' et 'Date Dernier Suivi' au format datetime pour un meilleur traitement
# Note: Lors de l'import dans Google Sheets, le format de date devrait être reconnu automatiquement.
# df_suivi_recos['Date Recommandation'] = pd.to_datetime(df_suivi_recos['Date Recommandation'])
# df_suivi_recos['Date Dernier Suivi'] = pd.to_datetime(df_suivi_recos['Date Dernier Suivi'])

# Affichage des premières lignes du DataFrame pour vérification
print("Aperçu du DataFrame généré :")
print(df_suivi_recos.head())

# Création d'un buffer en mémoire pour le fichier CSV
output = io.StringIO()
df_suivi_recos.to_csv(output, index=False, sep=';', encoding='utf-8-sig') # Utilisation du point-virgule comme séparateur pour compatibilité Excel FR
csv_content = output.getvalue()
output.close()

# Sauvegarde du DataFrame en fichier CSV
# Le nom du fichier sera 'suivi_recommandations_club.csv'
# L'encodage 'utf-8-sig' assure une bonne compatibilité avec les caractères accentués dans Excel.
# Le séparateur ';' est souvent mieux géré par les versions françaises d'Excel/Sheets.
file_path = 'suivi_recommandations_club.csv'
df_suivi_recos.to_csv(file_path, index=False, sep=';', encoding='utf-8-sig')

print(f"\nLe fichier CSV '{file_path}' a été généré avec succès.")
print("Vous pouvez maintenant importer ce fichier dans Google Sheets.")

