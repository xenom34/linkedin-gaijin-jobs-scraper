from linkedin_export import LinkedInExporter
import json

def fix_html_file(html_file):
    """Corrige le fichier HTML pour éviter les erreurs de syntaxe JavaScript"""
    print(f"Correction du fichier HTML: {html_file}")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trouver la ligne problématique où les données JSON sont injectées
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'const jobsData =' in line:
            print(f"Ligne originale ({i+1}): {line}")
            
            # Extraire les données JSON
            json_start = line.find('=') + 1
            json_data = line[json_start:].strip().rstrip(';')
            
            # Vérifier que les données JSON sont valides
            try:
                # Essayer de parser les données pour valider
                parsed_data = json.loads(json_data)
                print("Les données JSON sont valides")
                
                # Remplacer la ligne par une version correcte
                lines[i] = f"                const jobsData = {json_data};"
                print(f"Nouvelle ligne: {lines[i]}")
            except json.JSONDecodeError as e:
                print(f"Erreur de décodage JSON: {e}")
                # Utiliser une approche alternative - sans utiliser de f-string pour l'échappement
                escaped_json = json_data.replace("'", r"\'")
                lines[i] = "                const jobsData = JSON.parse('" + escaped_json + "');"
                print(f"Nouvelle ligne (alternative): {lines[i]}")
    
    # Écrire le contenu corrigé
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"Fichier HTML corrigé: {html_file}")
    return html_file

def main():
    """Test l'exportation des données"""
    print("Création des données de test...")
    test_jobs = [
        {
            'title': 'Test Job 1',
            'company': 'Test Company A',
            'location': 'Tokyo, Japan',
            'url': 'https://linkedin.com/job/1',
            'is_gaijin_friendly': 'Oui',
            'score_total': 25,
            'score_japonais': 15,
            'score_international': 10,
            'score_avantages': 5,
            'score_conges': 0,
            'score_langue': 5,
            'score_sentiment': -10,
            'jours_conges': 15,
            'avantages': 'Transport, Logement'
        },
        {
            'title': 'Test Job 2',
            'company': 'Test Company B',
            'location': 'Osaka, Japan',
            'url': 'https://linkedin.com/job/2',
            'is_gaijin_friendly': 'Non',
            'score_total': 5,
            'score_japonais': -10,
            'score_international': 10,
            'score_avantages': 5,
            'score_conges': 0,
            'score_langue': 0,
            'score_sentiment': 0,
            'jours_conges': 'Non spécifié',
            'avantages': ''
        }
    ]
    
    print("Test de création du rapport HTML...")
    exporter = LinkedInExporter()
    html_file = exporter.create_html_report(test_jobs, filename="test_report.html")
    
    # Corriger le fichier HTML
    fixed_html = fix_html_file(html_file)
    
    print(f"Rapport HTML créé et corrigé: {fixed_html}")
    print("Le navigateur devrait s'ouvrir automatiquement pour afficher le rapport.")

if __name__ == "__main__":
    main() 