import os
import pandas as pd
import logging
import webbrowser
from datetime import datetime
import re
import json

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class LinkedInExporter:
    def __init__(self):
        self.export_dir = "exports"
        # Créer le dossier des exports s'il n'existe pas
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)
    
    def prepare_filename(self, base_name):
        """Prépare un nom de fichier avec timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{self.export_dir}/{base_name}_{timestamp}"
    
    def export_to_csv(self, jobs, filename=None):
        """Exporter les offres en CSV"""
        if not filename:
            filename = self.prepare_filename("linkedin_jobs") + ".csv"
        
        logger.info(f"Exportation de {len(jobs)} offres vers CSV: {filename}")
        
        # Créer un DataFrame et exporter
        df = pd.DataFrame(jobs)
        df.to_csv(filename, index=False, encoding='utf-8')
        
        logger.info(f"Export CSV terminé: {filename}")
        return filename
    
    def export_to_excel(self, jobs, filename=None):
        """Exporter les offres en Excel avec formatage avancé"""
        if not filename:
            filename = self.prepare_filename("linkedin_jobs") + ".xlsx"
            
        logger.info(f"Exportation de {len(jobs)} offres vers Excel: {filename}")
        
        # Créer un DataFrame
        df = pd.DataFrame(jobs)
        
        try:
            # Créer un writer Excel avec XlsxWriter
            writer = pd.ExcelWriter(filename, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Offres LinkedIn', index=False)
            
            # Obtenir le classeur et la feuille
            workbook = writer.book
            worksheet = writer.sheets['Offres LinkedIn']
            
            # Définir les formats
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1
            })
            
            gaijin_yes_format = workbook.add_format({
                'bg_color': '#C6EFCE',
                'font_color': '#006100'
            })
            
            gaijin_no_format = workbook.add_format({
                'bg_color': '#FFC7CE',
                'font_color': '#9C0006'
            })
            
            score_high_format = workbook.add_format({
                'bg_color': '#C6EFCE',
                'font_color': '#006100'
            })
            
            score_medium_format = workbook.add_format({
                'bg_color': '#FFEB9C',
                'font_color': '#9C5700'
            })
            
            score_low_format = workbook.add_format({
                'bg_color': '#FFC7CE',
                'font_color': '#9C0006'
            })
            
            # Formater les en-têtes
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # Ajuster la largeur des colonnes
            worksheet.set_column('A:C', 20)  # Titre, Entreprise, Localisation
            worksheet.set_column('D:D', 40)  # URL
            worksheet.set_column('E:E', 15)  # Gaijin-friendly
            worksheet.set_column('F:L', 12)  # Scores
            worksheet.set_column('M:N', 30)  # Jours de congés et avantages
            
            # Ajouter le formatage conditionnel
            # Colonne is_gaijin_friendly
            is_gaijin_col = df.columns.get_loc("is_gaijin_friendly")
            if is_gaijin_col >= 0:
                worksheet.conditional_format(1, is_gaijin_col, len(df), is_gaijin_col, {
                    'type': 'text',
                    'criteria': 'containing',
                    'value': 'Oui',
                    'format': gaijin_yes_format
                })
                
                worksheet.conditional_format(1, is_gaijin_col, len(df), is_gaijin_col, {
                    'type': 'text',
                    'criteria': 'containing',
                    'value': 'Non',
                    'format': gaijin_no_format
                })
            
            # Colonnes de scores
            score_cols = ['score_total', 'score_japonais', 'score_international', 
                         'score_avantages', 'score_conges', 'score_langue', 'score_sentiment']
            
            for col_name in score_cols:
                if col_name in df.columns:
                    col_idx = df.columns.get_loc(col_name)
                    
                    # Format pour scores élevés (>10)
                    worksheet.conditional_format(1, col_idx, len(df), col_idx, {
                        'type': 'cell',
                        'criteria': '>',
                        'value': 10,
                        'format': score_high_format
                    })
                    
                    # Format pour scores moyens (0-10)
                    worksheet.conditional_format(1, col_idx, len(df), col_idx, {
                        'type': 'cell',
                        'criteria': 'between',
                        'minimum': 0,
                        'maximum': 10,
                        'format': score_medium_format
                    })
                    
                    # Format pour scores négatifs (<0)
                    worksheet.conditional_format(1, col_idx, len(df), col_idx, {
                        'type': 'cell',
                        'criteria': '<',
                        'value': 0,
                        'format': score_low_format
                    })
            
            # Ajouter un autofiltre
            worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)
            
            # Figer la première ligne
            worksheet.freeze_panes(1, 0)
            
            # Fermer le writer pour sauvegarder le fichier
            writer.close()
            
            logger.info(f"Export Excel terminé: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Erreur lors de l'export Excel: {str(e)}")
            return None
    
    def create_html_report(self, jobs, output_file):
        """Crée un rapport HTML interactif à partir des données d'offres d'emploi"""
        try:
            logger.info(f"Création du rapport HTML pour {len(jobs)} offres")
            
            # Vérifier si on a des données
            if not jobs:
                logger.warning("Aucune offre d'emploi disponible pour le rapport HTML")
                df = pd.DataFrame()
            else:
                # Convertir en dataframe pour traitement
                df = pd.DataFrame(jobs)
                logger.info(f"Nombre d'offres disponibles pour le rapport HTML: {len(df)}")
            
            # Préparer les données pour le JavaScript - Correction: utiliser json.dumps directement
            json_data = json.dumps(jobs)
            logger.info(f"Taille des données JSON: {len(json_data)} caractères")
            
            # S'assurer que le fichier de sortie a une extension .html
            if not output_file.endswith('.html'):
                output_file = output_file + '.html'
            
            # Créer le contenu HTML
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport des offres d'emploi LinkedIn</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 20px; }}
        .jobs-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        .jobs-table th, .jobs-table td {{ padding: 10px; border: 1px solid #ddd; text-align: left; }}
        .jobs-table th {{ background-color: #f2f2f2; }}
        .jobs-table tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .chart-container {{ display: flex; flex-wrap: wrap; margin-top: 30px; gap: 20px; }}
        .chart {{ flex: 1; min-width: 300px; min-height: 300px; padding: 15px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        .filter-container {{ margin: 20px 0; padding: 10px; background-color: #f2f2f2; border-radius: 5px; }}
        .filter-row {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 10px; }}
        .filter-item {{ flex: 1; min-width: 200px; }}
        label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
        select, input {{ width: 100%; padding: 8px; box-sizing: border-box; }}
        .job-card {{ border: 1px solid #ddd; margin-bottom: 20px; padding: 15px; border-radius: 5px; }}
        .job-title {{ font-size: 18px; font-weight: bold; margin: 0 0 5px 0; }}
        .job-company {{ font-weight: bold; color: #555; }}
        .job-location {{ color: #777; }}
        .job-score {{ margin-top: 10px; font-weight: bold; }}
        .job-score.high {{ color: green; }}
        .job-score.medium {{ color: orange; }}
        .job-score.low {{ color: red; }}
        .job-link {{ display: inline-block; margin-top: 10px; padding: 5px 10px; background-color: #0077b5; color: white; text-decoration: none; border-radius: 3px; }}
        .job-link:hover {{ background-color: #005582; }}
        .score-details {{ margin-top: 10px; padding: 10px; background-color: #f9f9f9; border-radius: 3px; }}
        .score-details h4 {{ margin: 0 0 5px 0; }}
        .score-item {{ margin-bottom: 3px; }}
        .toggle-details {{ cursor: pointer; color: #0077b5; margin-top: 5px; display: inline-block; }}
        .toggle-details:hover {{ text-decoration: underline; }}
        .hidden {{ display: none; }}
        .date-info {{ text-align: right; color: #777; margin-top: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Rapport des offres d'emploi LinkedIn</h1>
            <p>Date de génération: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
        
        <div class="filter-container">
            <h3>Filtres</h3>
            <div class="filter-row">
                <div class="filter-item">
                    <label for="company-filter">Entreprise</label>
                    <select id="company-filter">
                        <option value="all">Toutes</option>
                    </select>
                </div>
                <div class="filter-item">
                    <label for="location-filter">Lieu</label>
                    <select id="location-filter">
                        <option value="all">Tous</option>
                    </select>
                </div>
                <div class="filter-item">
                    <label for="score-filter">Score minimum</label>
                    <input type="number" id="score-filter" min="0" max="100" value="0">
                </div>
            </div>
            <div class="filter-row">
                <div class="filter-item">
                    <label for="gaijin-filter">Gaijin Friendly</label>
                    <select id="gaijin-filter">
                        <option value="all">Tous</option>
                        <option value="Oui">Oui</option>
                        <option value="Non">Non</option>
                    </select>
                </div>
                <div class="filter-item">
                    <label for="text-filter">Recherche textuelle</label>
                    <input type="text" id="text-filter" placeholder="Rechercher...">
                </div>
            </div>
        </div>
        
        <div id="jobs-container"></div>
        
        <div class="chart-container">
            <div class="chart">
                <canvas id="scoreDistributionChart"></canvas>
            </div>
            <div class="chart">
                <canvas id="categoryScoresChart"></canvas>
            </div>
        </div>
    </div>
    
    <script>
        // Les données des offres d'emploi - CORRECTION: assigner directement sans JSON.parse
        const jobsData = {json_data};
        
        // Fonction pour créer les graphiques
        function createCharts() {{
            // Graphique de distribution des scores
            const scoreRanges = {{'0-20': 0, '21-40': 0, '41-60': 0, '61-80': 0, '81-100': 0}};
            
            // Graphique des scores par catégorie
            const categoryScores = {{'Japonais': 0, 'International': 0, 'Avantages': 0, 'Congés': 0, 'Langue': 0, 'Sentiment': 0}};
            const categoryCount = {{'Japonais': 0, 'International': 0, 'Avantages': 0, 'Congés': 0, 'Langue': 0, 'Sentiment': 0}};
            
            // Calculer les moyennes et les distributions
            jobsData.forEach(job => {{
                // Distribution des scores
                const score = job.score_total || 0;
                if (score <= 20) scoreRanges['0-20']++;
                else if (score <= 40) scoreRanges['21-40']++;
                else if (score <= 60) scoreRanges['41-60']++;
                else if (score <= 80) scoreRanges['61-80']++;
                else scoreRanges['81-100']++;
                
                // Scores par catégorie
                if (job.score_japonais !== undefined) {{
                    categoryScores['Japonais'] += job.score_japonais;
                    categoryCount['Japonais']++;
                }}
                if (job.score_international !== undefined) {{
                    categoryScores['International'] += job.score_international;
                    categoryCount['International']++;
                }}
                if (job.score_avantages !== undefined) {{
                    categoryScores['Avantages'] += job.score_avantages;
                    categoryCount['Avantages']++;
                }}
                if (job.score_conges !== undefined) {{
                    categoryScores['Congés'] += job.score_conges;
                    categoryCount['Congés']++;
                }}
                if (job.score_langue !== undefined) {{
                    categoryScores['Langue'] += job.score_langue;
                    categoryCount['Langue']++;
                }}
                if (job.score_sentiment !== undefined) {{
                    categoryScores['Sentiment'] += job.score_sentiment;
                    categoryCount['Sentiment']++;
                }}
            }});
            
            // Calculer les moyennes pour les scores par catégorie
            Object.keys(categoryScores).forEach(key => {{
                if (categoryCount[key] > 0) {{
                    categoryScores[key] = categoryScores[key] / categoryCount[key];
                }}
            }});
            
            // Créer le graphique de distribution des scores
            const ctxDist = document.getElementById('scoreDistributionChart').getContext('2d');
            new Chart(ctxDist, {{
                type: 'bar',
                data: {{
                    labels: Object.keys(scoreRanges),
                    datasets: [{{
                        label: 'Nombre d\'offres',
                        data: Object.values(scoreRanges),
                        backgroundColor: 'rgba(54, 162, 235, 0.5)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }}]
                }},
                options: {{
                    responsive: true,
                    plugins: {{
                        legend: {{ display: false }},
                        title: {{
                            display: true,
                            text: 'Distribution des scores totaux'
                        }}
                    }}
                }}
            }});
            
            // Créer le graphique des scores par catégorie
            const ctxCat = document.getElementById('categoryScoresChart').getContext('2d');
            new Chart(ctxCat, {{
                type: 'radar',
                data: {{
                    labels: Object.keys(categoryScores),
                    datasets: [{{
                        label: 'Score moyen',
                        data: Object.values(categoryScores),
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }}]
                }},
                options: {{
                    elements: {{
                        line: {{ borderWidth: 3 }}
                    }},
                    plugins: {{
                        title: {{
                            display: true,
                            text: 'Scores moyens par catégorie'
                        }}
                    }},
                    scales: {{
                        r: {{
                            suggestedMin: -10,
                            suggestedMax: 20
                        }}
                    }}
                }}
            }});
        }}
        
        // Fonction pour afficher les offres d'emploi
        function displayJobs(jobs) {{
            const container = document.getElementById('jobs-container');
            container.innerHTML = '';
            
            if (jobs.length === 0) {{
                container.innerHTML = '<p>Aucune offre d\'emploi ne correspond à vos critères.</p>';
                return;
            }}
            
            jobs.forEach(job => {{
                const scoreClass = job.score_total >= 60 ? 'high' : (job.score_total >= 30 ? 'medium' : 'low');
                
                const jobCard = document.createElement('div');
                jobCard.className = 'job-card';
                
                jobCard.innerHTML = `
                    <h3 class="job-title">${{job.title || 'Titre inconnu'}}</h3>
                    <div class="job-company">${{job.company || 'Entreprise inconnue'}}</div>
                    <div class="job-location">${{job.location || 'Lieu inconnu'}}</div>
                    <div class="job-score ${{scoreClass}}">Score: ${{job.score_total || 0}}/100</div>
                    <div class="job-gaijin">Gaijin Friendly: ${{job.is_gaijin_friendly || 'Non spécifié'}}</div>
                    <a href="${{job.url || '#'}}" target="_blank" class="job-link">Voir l'offre</a>
                    <div class="toggle-details" onclick="toggleDetails(this)">Voir les détails des scores</div>
                    <div class="score-details hidden">
                        <h4>Détails des scores</h4>
                        <div class="score-item">Japonais: ${{job.score_japonais || 0}}/100</div>
                        <div class="score-item">International: ${{job.score_international || 0}}/100</div>
                        <div class="score-item">Avantages: ${{job.score_avantages || 0}}/100</div>
                        <div class="score-item">Congés: ${{job.score_conges || 0}}/100</div>
                        <div class="score-item">Langue: ${{job.score_langue || 0}}/100</div>
                        <div class="score-item">Sentiment: ${{job.score_sentiment || 0}}/100</div>
                        <div class="score-item">Jours de congés: ${{job.jours_conges || 'Non spécifié'}}</div>
                        <div class="score-item">Avantages: ${{job.avantages || 'Non spécifié'}}</div>
                    </div>
                `;
                
                container.appendChild(jobCard);
            }});
        }}
        
        // Fonction pour basculer l'affichage des détails
        function toggleDetails(element) {{
            const details = element.nextElementSibling;
            if (details.classList.contains('hidden')) {{
                details.classList.remove('hidden');
                element.textContent = 'Masquer les détails des scores';
            }} else {{
                details.classList.add('hidden');
                element.textContent = 'Voir les détails des scores';
            }}
        }}
        
        // Fonction pour filtrer les offres
        function filterJobs() {{
            const companyFilter = document.getElementById('company-filter').value;
            const locationFilter = document.getElementById('location-filter').value;
            const scoreFilter = parseInt(document.getElementById('score-filter').value);
            const gaijinFilter = document.getElementById('gaijin-filter').value;
            const textFilter = document.getElementById('text-filter').value.toLowerCase();
            
            const filteredJobs = jobsData.filter(job => {{
                if (companyFilter !== 'all' && job.company !== companyFilter) return false;
                if (locationFilter !== 'all' && job.location !== locationFilter) return false;
                if (job.score_total < scoreFilter) return false;
                if (gaijinFilter !== 'all' && job.is_gaijin_friendly !== gaijinFilter) return false;
                
                if (textFilter) {{
                    const searchFields = [
                        job.title, job.company, job.location, job.avantages,
                        job.is_gaijin_friendly
                    ].map(field => field ? field.toLowerCase() : '');
                    
                    return searchFields.some(field => field.includes(textFilter));
                }}
                
                return true;
            }});
            
            displayJobs(filteredJobs);
        }}
        
        // Initialiser les filtres
        function initFilters() {{
            const companies = new Set();
            const locations = new Set();
            const gaijinOptions = new Set();
            
            jobsData.forEach(job => {{
                if (job.company) companies.add(job.company);
                if (job.location) locations.add(job.location);
                if (job.is_gaijin_friendly) gaijinOptions.add(job.is_gaijin_friendly);
            }});
            
            const companyFilter = document.getElementById('company-filter');
            companies.forEach(company => {{
                const option = document.createElement('option');
                option.value = company;
                option.textContent = company;
                companyFilter.appendChild(option);
            }});
            
            const locationFilter = document.getElementById('location-filter');
            locations.forEach(location => {{
                const option = document.createElement('option');
                option.value = location;
                option.textContent = location;
                locationFilter.appendChild(option);
            }});
            
            // Ajouter les écouteurs d'événements
            companyFilter.addEventListener('change', filterJobs);
            locationFilter.addEventListener('change', filterJobs);
            document.getElementById('score-filter').addEventListener('input', filterJobs);
            document.getElementById('gaijin-filter').addEventListener('change', filterJobs);
            document.getElementById('text-filter').addEventListener('input', filterJobs);
        }}
        
        // Initialiser la page
        window.onload = function() {{
            createCharts();
            displayJobs(jobsData);
            initFilters();
        }};
    </script>
</body>
</html>"""

            # Enregistrer le fichier HTML
            os.makedirs(self.export_dir, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Rapport HTML créé: {output_file}")
            return output_file
        
        except Exception as e:
            logger.error(f"Erreur lors de la création du rapport HTML: {str(e)}")
            return None
    
    def export_all(self, jobs):
        """Exporte les données dans tous les formats disponibles"""
        logger.info(f"Export des données pour {len(jobs)} offres dans tous les formats")
        
        # Préparer les données pour l'export 
        # (supprimer la description longue si présente, elle n'est pas nécessaire)
        export_jobs = []
        for job in jobs:
            # Créer une copie du dictionnaire sans la description
            export_job = {k: v for k, v in job.items() if k != 'description'}
            export_jobs.append(export_job)
            
        # Exporter dans tous les formats
        csv_file = self.export_to_csv(export_jobs)
        excel_file = self.export_to_excel(export_jobs)
        html_file = self.create_html_report(export_jobs, self.prepare_filename("linkedin_report"))
        
        # Corriger les erreurs potentielles dans le HTML
        html_file = self.fix_html_report(html_file)
        
        # Retourner tous les fichiers créés
        return {
            'csv': csv_file,
            'excel': excel_file,
            'html': html_file
        }
        
    def fix_html_report(self, html_file):
        """Corrige les potentielles erreurs de syntaxe dans le HTML généré"""
        if not os.path.exists(html_file):
            logger.warning(f"Fichier HTML introuvable: {html_file}")
            return html_file

        try:
            with open(html_file, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # Corriger spécifiquement les problèmes dans les configurations de graphiques Chart.js
            # 1. Cas où il manque une virgule entre les objets data et options
            content = re.sub(r'(data:\s*\{[^}]*}\s*)\n(\s*options:)', r'\1,\n\2', content)
            
            # 2. Cas où il y a un espace entre data : (avec espace)
            content = re.sub(r'data\s+:', r'data:', content)
            
            # 3. Correction des virgules superflues dans la configuration du graphique
            content = re.sub(r'(\]\s*})\s*,\s*(\n\s*options:)', r'\1\2', content)
            
            # Écrire le contenu corrigé
            with open(html_file, 'w', encoding='utf-8') as file:
                file.write(content)
                
            logger.info(f"Fichier HTML corrigé: {html_file}")
            return html_file
            
        except Exception as e:
            logger.error(f"Erreur lors de la correction du fichier HTML: {str(e)}")
            return html_file

def main():
    """Exemple d'utilisation"""
    # Créer des données de test
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
    
    # Créer l'exporteur et exporter les données
    exporter = LinkedInExporter()
    export_files = exporter.export_all(test_jobs)
    
    # Afficher les résultats
    logger.info("Export terminé")
    logger.info(f"CSV: {export_files['csv']}")
    logger.info(f"Excel: {export_files['excel']}")
    logger.info(f"HTML: {export_files['html']}")

if __name__ == "__main__":
    main() 