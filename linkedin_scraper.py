import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from dotenv import load_dotenv
import pandas as pd
from langdetect import detect
import re
import logging
import argparse

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class LinkedInScraper:
    def __init__(self):
        logger.info("Initialisation du scraper LinkedIn...")
        load_dotenv()
        self.driver = None
        self.setup_driver()
        
    def setup_driver(self):
        """Configure le driver Firefox avec les options nécessaires"""
        logger.info("Configuration du driver Firefox...")
        options = webdriver.FirefoxOptions()
        # Désactiver le mode headless pour le débogage
        # options.add_argument('--headless')
        options.add_argument('--width=1920')
        options.add_argument('--height=1080')
        
        try:
            service = Service(GeckoDriverManager().install())
            self.driver = webdriver.Firefox(service=service, options=options)
            self.driver.maximize_window()  # Maximiser la fenêtre
            logger.info("Driver Firefox configuré avec succès")
        except Exception as e:
            logger.error(f"Échec de la configuration du driver: {str(e)}")
            raise
                
    def login(self):
        """Se connecte à LinkedIn"""
        logger.info("Tentative de connexion à LinkedIn...")
        self.driver.get('https://www.linkedin.com/login')
        time.sleep(5)  # Attendre que la page se charge complètement
        
        # Vérifier que la page de connexion est bien chargée
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, 'username'))
            )
            logger.info("Champ de connexion trouvé")
        except TimeoutException:
            logger.error("La page de connexion n'a pas pu être chargée")
            self.driver.save_screenshot("debug_login_page.png")
            raise
            
        email = os.getenv('LINKEDIN_EMAIL')
        password = os.getenv('LINKEDIN_PASSWORD')
        
        if not email or not password:
            logger.error("Les identifiants LinkedIn ne sont pas configurés dans le fichier .env")
            raise ValueError("Les identifiants LinkedIn ne sont pas configurés dans le fichier .env")
            
        # Saisir les identifiants
        try:
            email_field = self.driver.find_element(By.ID, 'username')
            email_field.clear()
            email_field.send_keys(email)
            logger.info("Email saisi")
            
            password_field = self.driver.find_element(By.ID, 'password')
            password_field.clear()
            password_field.send_keys(password)
            logger.info("Mot de passe saisi")
            
            login_button = self.driver.find_element(By.CSS_SELECTOR, '.login__form_action_container button')
            login_button.click()
            logger.info("Bouton de connexion cliqué")
            
            # Attendre que la connexion soit traitée
            time.sleep(10)  # Augmenter le temps d'attente
            
            # Vérifier si nous sommes sur une page de vérification
            current_url = self.driver.current_url
            if "checkpoint" in current_url:
                logger.info("Page de vérification détectée")
                self.driver.save_screenshot("debug_verification_page.png")
                
                # Attendre que l'utilisateur complète la vérification
                input("Veuillez compléter la vérification de sécurité manuellement, puis appuyez sur Entrée...")
                
                # Attendre que la vérification soit terminée
                time.sleep(5)
            
            # Vérifier que la connexion a réussi de plusieurs façons
            logger.info("Vérification de la connexion réussie...")
            
            # Vérifier l'URL actuelle
            current_url = self.driver.current_url
            logger.info(f"URL actuelle: {current_url}")
            
            # Vérifier si nous sommes sur une page valide après connexion
            if "login" in current_url:
                logger.error("Nous sommes toujours sur la page de connexion")
                self.driver.save_screenshot("debug_still_on_login.png")
                raise Exception("La connexion a échoué - nous sommes toujours sur la page de connexion")
            
            # Essayer plusieurs sélecteurs pour vérifier la connexion
            selectors = [
                "nav.global-nav",
                "div.global-nav__content",
                "div.feed-identity-module",
                "div.artdeco-card"
            ]
            
            connected = False
            for selector in selectors:
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    logger.info(f"Élément trouvé avec le sélecteur: {selector}")
                    connected = True
                    break
                except:
                    continue
            
            if not connected:
                logger.warning("Aucun élément de navigation trouvé, mais la connexion semble réussie")
                logger.info("Continuer avec l'URL actuelle")
            
            logger.info("Connexion à LinkedIn réussie")
                
        except Exception as e:
            logger.error(f"Erreur lors de la connexion: {str(e)}")
            self.driver.save_screenshot("debug_login_error.png")
            raise
        
    def search_jobs(self, keywords=None, location="Tokyo, Japan"):
        """Recherche des offres d'emploi sur LinkedIn"""
        if keywords is None:
            keywords = ["Technical Consultant", "Software Consultant", "Professional Services"]
        
        logger.info(f"Recherche d'offres avec les mots-clés: {keywords}")
        logger.info(f"Localisation: {location}")
        
        # Construire l'URL de recherche
        base_url = "https://www.linkedin.com/jobs/search"
        
        # Encoder les mots-clés pour l'URL
        search_query = " OR ".join(keywords)
        encoded_query = search_query.replace(" ", "+")
        
        # ID géographique pour Tokyo, Japan
        geo_id = "101355337"  # ID pour Tokyo, Japan
        
        # Construire l'URL complète
        search_url = f"{base_url}?keywords={encoded_query}&distance=25&geoId={geo_id}"
        logger.info(f"URL de recherche: {search_url}")
        
        # Naviguer vers l'URL de recherche
        logger.info("Navigation vers la page de résultats...")
        self.driver.get(search_url)
        
        # Attendre plus longtemps pour le chargement initial
        time.sleep(10)
        
        # Gérer les pop-ups de cookies si présents
        try:
            cookie_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-control-name='ga-cookie.consent.accept.v2']"))
            )
            cookie_button.click()
            logger.info("Popup de cookies fermé")
            time.sleep(2)
        except:
            logger.info("Pas de popup de cookies détecté")
        
        # Attendre que la page charge complètement
        logger.info("Attente du chargement complet de la page...")
        time.sleep(10)
        
        # Vérification que la page contient des offres
        try:
            # Vérifier la présence d'éléments li (on utilise une approche plus générique)
            list_items = self.driver.find_elements(By.CSS_SELECTOR, "li")
            logger.info(f"Nombre d'éléments li trouvés: {len(list_items)}")
            
            # Vérifier la présence d'éléments spécifiques aux jobs
            job_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-job-id]")
            logger.info(f"Nombre d'éléments avec data-job-id trouvés: {len(job_elements)}")
            
            # Vérifier les éléments avec classes contenant 'job'
            job_class_elements = self.driver.find_elements(By.CSS_SELECTOR, "[class*='job']")
            logger.info(f"Nombre d'éléments avec classe 'job' trouvés: {len(job_class_elements)}")
            
            # Prendre une capture d'écran pour analyse visuelle
            self.driver.save_screenshot("search_results_loaded.png")
            logger.info("Capture d'écran sauvegardée dans search_results_loaded.png")
            
            if len(job_elements) == 0 and len(job_class_elements) == 0:
                logger.error("Aucun élément d'offre d'emploi trouvé")
                raise Exception("Aucun élément d'offre d'emploi trouvé")
            
            logger.info("Page de résultats chargée avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors de la vérification des résultats: {str(e)}")
            self.driver.save_screenshot("debug_search_results.png")
            raise
        
    def is_gaijin_friendly(self, description):
        """
        Détermine si l'offre est adaptée aux étrangers en utilisant une approche multicritère
        Retourne un tuple contenant (resultat, score_total, scores_détails, jours_congés, avantages)
        """
        # Score de base
        score = 0
        days_of_leave = None
        
        # Analyse du niveau de japonais requis
        japanese_score = self.analyze_japanese_requirements(description)
        score += japanese_score
        
        # Analyse de l'environnement international
        international_score = self.analyze_international_environment(description)
        score += international_score
        
        # Analyse des avantages pour expatriés
        benefits_score = self.analyze_expat_benefits(description)
        score += benefits_score
        
        # Analyse des politiques de congés
        leave_policy_score, days_of_leave = self.analyze_leave_policy(description)
        score += leave_policy_score
        
        # Analyse de la langue utilisée dans l'offre
        language_score = self.analyze_language(description)
        score += language_score
        
        # Analyse générale de sentiment
        sentiment_score = self.analyze_sentiment(description)
        score += sentiment_score
        
        # Détecter les avantages supplémentaires
        additional_benefits = self.detect_additional_benefits(description)
        
        # Journaliser le score final
        logger.info(f"Score gaijin-friendly: {score}")
        logger.info(f"Japonais: {japanese_score}, International: {international_score}, "
                    f"Avantages: {benefits_score}, Congés: {leave_policy_score}, "
                    f"Langue: {language_score}, Sentiment: {sentiment_score}")
        if days_of_leave:
            logger.info(f"Jours de congés: {days_of_leave}")
        if additional_benefits:
            logger.info(f"Avantages supplémentaires: {', '.join(additional_benefits)}")
        
        # Créer un dictionnaire des détails pour le CSV
        details = {
            'score_total': score,
            'score_japonais': japanese_score,
            'score_international': international_score,
            'score_avantages': benefits_score,
            'score_conges': leave_policy_score,
            'score_langue': language_score,
            'score_sentiment': sentiment_score,
            'jours_conges': days_of_leave,
            'avantages': ', '.join(additional_benefits) if additional_benefits else ''
        }
        
        # Une offre est considérée comme gaijin-friendly si le score est supérieur à 15 
        # ET le score japonais n'est pas fortement négatif
        is_friendly = score > 15 and japanese_score > -10
        return is_friendly, details

    def analyze_japanese_requirements(self, description):
        """
        Analyse les exigences linguistiques japonaises
        Retourne un score: positif si peu/pas de japonais requis, négatif si japonais avancé requis
        """
        score = 0
        
        # Expressions positives (pas de japonais ou japonais basique requis)
        positive_patterns = [
            # Pas de japonais requis
            r'(?i)no\s+japanese\s+(language\s+)?(required|needed)',
            r'(?i)japanese\s+(language\s+)?(not|isn\'t|isn t|isnt)\s+(required|needed|necessary)',
            r'(?i)japanese\s+(language\s+)?is\s+(not|optional)',
            r'(?i)without\s+japanese\s+language',
            r'(?i)english(\s+)(speaking|environment|workplace)',
            r'(?i)english\s+(as|is)\s+(the|a|an|our)\s+(primary|main|official|working|company|business|corporate)\s+language',
            r'(?i)(primary|main|official|working|company|business|corporate)\s+language\s+is\s+english',
            r'(?i)japanese\s+is\s+a\s+plus',
            r'(?i)japanese\s+is\s+not\s+required',
            
            # Langues alternatives
            r'(?i)english\s+(only|speaking)',
            r'(?i)(speak|communication\s+in)\s+english',
            r'(?i)(proficient|fluent)\s+in\s+english',
            r'(?i)english\s+(proficiency|fluency)',
            r'(?i)english\s+language\s+skills',
            
            # Mots-clés positifs supplémentaires
            r'(?i)foreigner\s+friendly',
            r'(?i)gaijin\s+friendly',
            r'(?i)international\s+candidates',
            r'(?i)overseas\s+applicants',
            r'(?i)foreign\s+nationals\s+(welcome|encouraged)',
            r'(?i)open\s+to\s+(foreigners|expats|expatriates)',
            r'(?i)welcome\s+(foreigners|expats|expatriates)'
        ]
        
        # Expressions négatives (japonais requis)
        negative_patterns = [
            r'(?i)japanese\s+(language|fluency)\s+(required|needed|mandatory|essential)',
            r'(?i)(proficient|fluent)\s+in\s+japanese',
            r'(?i)japanese\s+(proficiency|fluency)',
            r'(?i)japanese\s+language\s+skills',
            r'(?i)(high|strong)\s+level\s+of\s+japanese',
            r'(?i)ビジネスレベル.*日本語',
            r'(?i)日本語.*ビジネスレベル',
            r'(?i)日本語必須',
            r'(?i)(native|business)\s+level\s+japanese',
            r'(?i)jlpt\s*(n1|n2)',
            r'(?i)(must|should)\s+(be\s+)?(able\s+to\s+)?(speak|understand|read|write)\s+japanese',
            r'(?i)native\s+japanese\s+speaker',
            r'(?i)fluent\s+japanese',
            r'(?i)advanced\s+japanese',
            
            # Nouveaux patterns pour résoudre les problèmes identifiés
            r'(?i)both\s+.*japanese\s+and\s+english.*mandatory',
            r'(?i)both\s+.*japanese\s+and\s+english.*required',
            r'(?i)(skills|communication).*japanese\s+and\s+english',
            r'(?i)japanese\s+and\s+english\s+(skills|communication)',
            r'(?i)(skills|communication).*in\s+.*japanese.*is\s+a\s+must',
            r'(?i)(skills|communication).*in\s+.*japanese.*required',
            r'(?i)(skills|communication).*in\s+.*japanese.*necessary',
            r'(?i)(english\s+and\s+japanese|japanese\s+and\s+english).*is\s+a\s+must',
            r'(?i)(english\s+and\s+japanese|japanese\s+and\s+english).*required',
            r'(?i)fluent\s+in\s+.*japanese',
            r'(?i)fluent\s+in\s+.*english\s+and\s+japanese',
            r'(?i)fluent\s+in\s+.*japanese\s+and\s+english',
            r'(?i)language\s+proficiency.*japanese',
            r'(?i)proficiency\s+in\s+.*japanese',
            r'(?i)strong\s+.*communication\s+skills.*japanese',
            r'(?i)excellent\s+.*communication\s+skills.*japanese',
            
            # Nouveaux patterns spécifiques pour le cas signalé et similaires
            r'(?i)native\s+japanese\s+speaker',
            r'(?i)native\s+japanese.*fluent\s+in\s+english',
            r'(?i)native\s+japanese.*english\s+fluent',
            r'(?i)native\s+japanese.*english\s+speaker',
            r'(?i)japanese\s+native\s+speaker',
            r'(?i)fluent\s+japanese\s+language',
            r'(?i)native\s+level\s+japanese',
            r'(?i)japanese\s+at\s+native\s+level',
            r'(?i)japanese\s+at\s+a\s+native\s+level',
            r'(?i)native\s+or\s+near-native\s+japanese',
            r'(?i)near-native\s+japanese',
            r'(?i)japanese\s+mother\s+tongue',
            r'(?i)mother\s+tongue\s+japanese',
            r'(?i)japanese\s+as\s+(a\s+)?mother\s+tongue',
            r'(?i)spoken\s+and\s+written\s+japanese',
            r'(?i)read\s+and\s+write\s+japanese',
            r'(?i)japanese\s+reading\s+and\s+writing',
            r'(?i)(speaking|communicating)\s+in\s+japanese\s+with',
            r'(?i)communicate\s+.*in\s+japanese',
            r'(?i)communication\s+.*in\s+japanese',
            r'(?i)japanese\s+speaker',
            r'(?i)need\s+to\s+(speak|understand)\s+japanese',
            r'(?i)requires\s+japanese\s+language',
            r'(?i)japanese\s+language\s+is\s+(mandatory|required|a must)',
            r'(?i)strong\s+japanese\s+language\s+skills',
            r'(?i)strong\s+command\s+of\s+japanese',
            r'(?i)command\s+of\s+japanese',
            r'(?i)excellent\s+japanese',
            r'(?i)proficient\s+japanese',
            r'(?i)japanese\s+proficient',
            r'(?i)competent\s+in\s+japanese',
            r'(?i)japanese\s+competency'
        ]
        
        # Détection des niveaux JLPT
        jlpt_patterns = {
            'N1': r'(?i)jlpt\s*n1|日本語検定1級|native\s+level\s+japanese',
            'N2': r'(?i)jlpt\s*n2|日本語検定2級|business\s+level\s+japanese',
            'N3': r'(?i)jlpt\s*n3|日本語検定3級|intermediate\s+japanese',
            'N4': r'(?i)jlpt\s*n4|日本語検定4級|basic\s+japanese',
            'N5': r'(?i)jlpt\s*n5|日本語検定5級|elementary\s+japanese'
        }
        
        # Vérifier les expressions positives
        positives_found = []
        for pattern in positive_patterns:
            matches = re.finditer(pattern, description)
            for match in matches:
                positives_found.append(match.group(0))
                score += 10  # Réduit de 15 à 10 points, mais plus de patterns
        
        # Loguer les expressions positives trouvées
        if positives_found:
            logger.info(f"Expressions positives trouvées ({len(positives_found)}): {', '.join(positives_found[:3])}")
        
        # Vérifier les expressions négatives
        negatives_found = []
        for pattern in negative_patterns:
            matches = re.finditer(pattern, description)
            for match in matches:
                negatives_found.append(match.group(0))
                score -= 10  # Réduit de 15 à 10 points négatifs
        
        # Loguer les expressions négatives trouvées
        if negatives_found:
            logger.info(f"Expressions négatives trouvées ({len(negatives_found)}): {', '.join(negatives_found[:3])}")
        
        # Vérifier les niveaux JLPT
        for level, pattern in jlpt_patterns.items():
            if re.search(pattern, description):
                if level in ['N1', 'N2']:
                    score -= 10
                    logger.info(f"Exigence JLPT élevée: {level}")
                elif level == 'N3':
                    score -= 5
                    logger.info(f"Exigence JLPT intermédiaire: {level}")
                else:  # N4 ou N5
                    score += 5
                    logger.info(f"Exigence JLPT basique: {level}")
        
        # Analyse contextuelle avancée pour détecter les situations ambiguës
        # Par exemple, "Japanese language skills a plus" est positif malgré la mention de japonais
        context_patterns = {
            'positif': [
                r'(?i)japanese\s+language\s+is\s+a\s+plus',
                r'(?i)japanese\s+would\s+be\s+(a\s+plus|helpful|beneficial)',
                r'(?i)japanese\s+is\s+not\s+mandatory',
                r'(?i)japanese\s+skills\s+are\s+optional',
                r'(?i)basic\s+japanese\s+is\s+sufficient',
                r'(?i)willing\s+to\s+learn\s+japanese'
            ],
            'négatif': [
                r'(?i)daily\s+communication\s+in\s+japanese',
                r'(?i)work\s+environment\s+is\s+(primarily|mainly)\s+japanese',
                r'(?i)must\s+communicate\s+with\s+japanese\s+clients',
                r'(?i)japanese\s+team\s+members',
                r'(?i)japanese\s+documentation',
                r'(?i)native\s+level\s+of\s+japanese',
                r'(?i)bilingual\s+.*japanese\s+and\s+english',
                r'(?i)fluent\s+in\s+both\s+japanese\s+and\s+english',
                r'(?i)fluent\s+in\s+both\s+english\s+and\s+japanese'
            ]
        }
        
        # Vérifier les patterns contextuels positifs
        for pattern in context_patterns['positif']:
            if re.search(pattern, description):
                score += 5
                logger.info(f"Contexte positif trouvé: {pattern}")
        
        # Vérifier les patterns contextuels négatifs
        for pattern in context_patterns['négatif']:
            if re.search(pattern, description):
                score -= 5
                logger.info(f"Contexte négatif trouvé: {pattern}")
        
        # Bonus: si plusieurs indicateurs positifs sans négatifs
        if len(positives_found) >= 3 and len(negatives_found) == 0:
            score += 10
            logger.info("Bonus: Multiples indicateurs positifs sans négatifs")
        
        return score

    def analyze_international_environment(self, description):
        """
        Analyse si l'environnement de travail est international
        """
        score = 0
        
        international_indicators = [
            # Environnement de travail
            r'(?i)international\s+(team|office|environment|company|organization|culture|workplace|firm)',
            r'(?i)diverse\s+(team|workplace|culture|environment|workforce)',
            r'(?i)multicultural\s+(environment|team|company|workplace|setting)',
            r'(?i)english\s+as\s+(the|a)\s+working\s+language',
            r'(?i)global\s+(company|team|organization|culture|firm|player|business)',
            r'(?i)foreign\s+(employees|workers|staff|colleagues)',
            r'(?i)(team|staff|colleagues|employees)\s+from\s+(all\s+over|many|various|different)\s+(the\s+world|countries|backgrounds)',
            
            # Structure organisationnelle
            r'(?i)expatriates',
            r'(?i)multinational\s+(corporation|company|organization|environment)',
            r'(?i)offices\s+in\s+\d+\s+countries',
            r'(?i)presence\s+in\s+\d+\s+countries',
            r'(?i)global\s+presence',
            r'(?i)worldwide\s+operations',
            
            # Clients et projets
            r'(?i)international\s+(clients|projects|assignments|business)',
            r'(?i)global\s+(clients|projects|market|customers)',
            r'(?i)cross\s*-\s*border',
            r'(?i)(work|collaborate)\s+with\s+(international|global|worldwide)\s+(teams|colleagues|clients)',
            
            # Culture d'entreprise
            r'(?i)inclusive\s+(environment|workplace|culture)',
            r'(?i)diversity\s+and\s+inclusion',
            r'(?i)equal\s+opportunity\s+employer',
            r'(?i)cross\s*-\s*cultural',
            
            # Pratiques commerciales
            r'(?i)global\s+(mindset|outlook|perspective)',
            r'(?i)international\s+(travel|exposure|experience)',
            r'(?i)global\s+mobility',
            r'(?i)relocation\s+opportunities'
        ]
        
        # Compteur de patterns trouvés
        patterns_found = []
        
        for indicator in international_indicators:
            matches = re.finditer(indicator, description)
            for match in matches:
                patterns_found.append(match.group(0))
                score += 5
        
        # Loguer les patterns trouvés
        if patterns_found:
            logger.info(f"Indicateurs d'environnement international trouvés ({len(patterns_found)}): {', '.join(patterns_found[:5])}")
        
        # Analyse contextuelle supplémentaire
        global_keywords = ['global', 'international', 'worldwide', 'multinational']
        keyword_count = sum(1 for keyword in global_keywords if keyword.lower() in description.lower())
        
        # Bonus si multiples mentions de mots-clés globaux
        if keyword_count >= 3:
            score += 5
            logger.info(f"Bonus: {keyword_count} mots-clés globaux trouvés")
        
        # Limiter le score maximum pour cette catégorie
        return min(score, 20)  # Augmenté de 15 à 20 pour être plus généreux

    def analyze_expat_benefits(self, description):
        """
        Analyse les avantages spécifiques pour les expatriés
        """
        score = 0
        
        expat_benefits = [
            # Visa et immigration
            r'(?i)visa\s+(sponsorship|support|assistance)',
            r'(?i)sponsor\s+(working\s+visa|work\s+visa|visa)',
            r'(?i)work\s+permit\s+(support|assistance)',
            r'(?i)immigration\s+(support|assistance)',
            
            # Relocation et logement
            r'(?i)relocation\s+(package|assistance|support|help|allowance)',
            r'(?i)housing\s+(allowance|assistance|support|subsidy|benefit)',
            r'(?i)(help|assist)\s+with\s+(finding|securing)\s+accommodation',
            r'(?i)temporary\s+housing',
            r'(?i)accommodation\s+(support|assistance|allowance)',
            
            # Transport et voyage
            r'(?i)flight\s+(tickets|reimbursement|allowance)',
            r'(?i)air\s+fare',
            r'(?i)travel\s+(allowance|expense|reimbursement)',
            r'(?i)home\s+travel\s+allowance',
            r'(?i)transportation\s+(allowance|benefit)',
            r'(?i)commuting\s+allowance',
            
            # Installation et adaptation
            r'(?i)settling(-|\s+)in\s+allowance',
            r'(?i)home\s+leave',
            r'(?i)language\s+lessons',
            r'(?i)japanese\s+lessons',
            r'(?i)cultural\s+training',
            r'(?i)cross-cultural\s+training',
            r'(?i)orientation\s+program',
            
            # Santé et assurance
            r'(?i)international\s+health\s+insurance',
            r'(?i)global\s+health\s+coverage',
            r'(?i)medical\s+insurance\s+for\s+expatriates',
            r'(?i)private\s+health\s+insurance',
            
            # Avantages financiers
            r'(?i)expatriate\s+package',
            r'(?i)expat\s+benefits',
            r'(?i)moving\s+expenses',
            r'(?i)cost\s+of\s+living\s+adjustment',
            r'(?i)expatriate\s+premium',
            r'(?i)hardship\s+allowance',
            r'(?i)tax\s+(assistance|consultation)',
            
            # Support familial
            r'(?i)family\s+relocation',
            r'(?i)dependent\s+visa\s+support',
            r'(?i)spouse\s+(support|assistance|program)',
            r'(?i)education\s+allowance\s+for\s+children',
            r'(?i)international\s+school\s+fees'
        ]
        
        # Compteur des patterns trouvés
        benefits_found = []
        
        for benefit in expat_benefits:
            matches = re.finditer(benefit, description)
            for match in matches:
                benefits_found.append(match.group(0))
                score += 5
        
        # Loguer les avantages trouvés
        if benefits_found:
            logger.info(f"Avantages pour expatriés trouvés ({len(benefits_found)}): {', '.join(benefits_found[:5])}")
        
        # Analyse contextuelle supplémentaire
        # Si "package" ou "benefits" est mentionné à proximité de mots comme "expat", "international", "relocation"
        context_patterns = [
            r'(?i)(comprehensive|attractive|competitive)\s+(package|benefits|perks|compensation)',
            r'(?i)(package|benefits|perks)\s+include',
            r'(?i)(full|complete)\s+support\s+for\s+(foreigners|expatriates|international\s+candidates)'
        ]
        
        for pattern in context_patterns:
            if re.search(pattern, description):
                score += 5
                logger.info(f"Contexte d'avantages trouvé: {pattern}")
        
        # Limiter le score maximum pour cette catégorie
        return min(score, 20)  # Augmenté de 15 à 20

    def analyze_leave_policy(self, description):
        """
        Analyse la politique de congés pour identifier les entreprises offrant des conditions
        plus généreuses que le standard japonais (10 jours après 6 mois)
        Retourne (score, jours_de_congés)
        """
        score = 0
        days_of_leave = None
        
        # Recherche de mentions de jours de congés généreux
        generous_leave_patterns = [
            # Nombre de jours de congés supérieur à la norme japonaise
            r'(?i)(\d{2,})\s+(days|business days)\s+(of|for)\s+(annual|paid)\s+leave',
            r'(?i)(annual|paid)\s+leave\s+(\d{2,})\s+(days|business days)',
            r'(?i)(\d{2,})\s+(days|business days)\s+(vacation|holiday|time off|leave|pto)',
            r'(?i)(vacation|holiday|time off|leave|pto)\s+(\d{2,})\s+(days|business days)',
            r'(?i)(up\s+to|min|minimum|maximum|max|more\s+than)\s+(\d{2,})\s+(days|business days)',
            
            # Mentions spécifiques de politiques généreuses
            r'(?i)generous\s+(vacation|leave|time off|holiday|pto)',
            r'(?i)flexible\s+(vacation|leave|time off|holiday|pto)',
            r'(?i)unlimited\s+(vacation|leave|time off|holiday|pto)',
            r'(?i)work(-|\s+)life\s+balance',
            r'(?i)above\s+statutory\s+(leave|vacation|holidays)',
            r'(?i)competitive\s+(leave|vacation|holiday)\s+policy',
            
            # Types de congés spécifiques
            r'(?i)sabbatical\s+leave',
            r'(?i)parental\s+leave',
            r'(?i)paternity\s+leave',
            r'(?i)maternity\s+leave',
            r'(?i)sick\s+leave',
            r'(?i)personal\s+days',
            r'(?i)mental\s+health\s+days',
            r'(?i)volunteer\s+days',
            r'(?i)bereavement\s+leave',
            r'(?i)summer\s+holidays',
            r'(?i)winter\s+holidays',
            r'(?i)golden\s+week',
            r'(?i)summer\s+break',
            r'(?i)winter\s+break',
            
            # Flexibilité horaire
            r'(?i)flexible\s+(working\s+hours|schedule|work\s+arrangements)',
            r'(?i)flex\s+time',
            r'(?i)remote\s+work',
            r'(?i)work\s+from\s+home',
            r'(?i)hybrid\s+work',
            r'(?i)flextime',
            r'(?i)4-day\s+work\s+week',
            r'(?i)compressed\s+work\s+week',
            
            # Jours fériés
            r'(?i)(all|global|international|local)\s+public\s+holidays',
            r'(?i)public\s+holidays\s+plus',
            r'(?i)national\s+holidays\s+plus'
        ]
        
        # Recherche des patterns et calcul du score
        leave_patterns_found = []
        
        for pattern in generous_leave_patterns:
            matches = re.finditer(pattern, description)
            for match in matches:
                leave_patterns_found.append(match.group(0))
                score += 5
        
        # Loguer les patterns trouvés
        if leave_patterns_found:
            logger.info(f"Politiques de congés favorables trouvées ({len(leave_patterns_found)}): {', '.join(leave_patterns_found[:5])}")
        
        # Essayer d'extraire le nombre de jours de congés
        # Recherche de patterns comme "20 days", "20 vacation days", etc.
        days_patterns = [
            r'(?i)(\d{2,})\s+days\s+(?:of\s+)?(?:annual|paid)?\s*(?:leave|vacation|holiday|time\s+off|pto)',
            r'(?i)(?:annual|paid)?\s*(?:leave|vacation|holiday|time\s+off|pto)\s+(?:of\s+)?(\d{2,})\s+days',
            r'(?i)(?:up\s+to|min|minimum|maximum|max|more\s+than)\s+(\d{2,})\s+days'
        ]
        
        for pattern in days_patterns:
            days_match = re.search(pattern, description)
            if days_match:
                try:
                    days = int(days_match.group(1))
                    logger.info(f"Nombre de jours de congés mentionné: {days}")
                    days_of_leave = days
                    
                    # Bonus pour les congés vraiment généreux
                    if days >= 25:
                        score += 10
                        logger.info(f"Bonus élevé pour {days} jours de congés")
                    elif days >= 20:
                        score += 7
                        logger.info(f"Bonus important pour {days} jours de congés")
                    elif days >= 15:
                        score += 5
                        logger.info(f"Bonus pour {days} jours de congés")
                    elif days > 10:
                        score += 3
                        logger.info(f"Petit bonus pour {days} jours de congés")
                except:
                    pass
        
        # Bonus pour des combinaisons de mots-clés liés aux congés
        leave_keywords = ['flexible', 'generous', 'work-life balance', 'unlimited', 'paid time off']
        leave_keyword_count = sum(1 for keyword in leave_keywords if keyword.lower() in description.lower())
        
        if leave_keyword_count >= 2:
            score += 5
            logger.info(f"Bonus: {leave_keyword_count} mots-clés de congés trouvés")
        
        # Limiter le score maximum pour cette catégorie
        return min(score, 20), days_of_leave  # Augmenté de 15 à 20

    def analyze_language(self, description):
        """
        Analyse la langue utilisée dans l'offre et détecte les mentions de français
        qui peuvent indiquer une entreprise francophone
        """
        score = 0
        
        # Détection du français
        french_patterns = [
            r'(?i)french\s+(speaking|speaker)',
            r'(?i)fluent\s+in\s+french',
            r'(?i)french\s+(language|fluency)',
            r'(?i)speak\s+french',
            r'(?i)french\s+skills',
            r'(?i)knowledge\s+of\s+french',
            r'(?i)french\s+a\s+plus',
            r'(?i)french\s+company',
            r'(?i)french\s+firm',
            r'(?i)francophone',
            r'(?i)france\s+based',
            r'(?i)headquartered\s+in\s+france',
            # Expressions en français
            r'(?i)parle\s+français',
            r'(?i)français\s+courant',
            r'(?i)maîtrise\s+du\s+français',
            r'(?i)entreprise\s+française',
            r'(?i)société\s+française'
        ]
        
        french_matches = []
        for pattern in french_patterns:
            matches = re.finditer(pattern, description)
            for match in matches:
                french_matches.append(match.group(0))
                score += 5
        
        if french_matches:
            logger.info(f"Indices de français trouvés ({len(french_matches)}): {', '.join(french_matches)}")
            score += 5  # Bonus supplémentaire pour du français
        
        # Analyse de la langue de rédaction
        try:
            from langdetect import detect
            lang = detect(description[:1000])  # Limiter à 1000 caractères pour la détection
            
            if lang == 'en':
                score += 10
                logger.info("Offre rédigée en anglais")
            elif lang == 'fr':
                score += 10
                logger.info("Offre rédigée en français")
            elif lang == 'ja':
                score -= 10
                logger.info("Offre rédigée en japonais")
        except:
            logger.warning("Impossible de détecter la langue de l'offre")
        
        return min(score, 15)  # Maximum 15 points pour cette catégorie

    def analyze_sentiment(self, description):
        """
        Analyse le sentiment général de l'offre vis-à-vis des étrangers
        """
        score = 0
        
        # Phrases positives qui indiquent une ouverture aux étrangers
        positive_phrases = [
            r'(?i)we\s+welcome\s+(international|foreign|overseas|global)\s+(candidates|applicants|talents)',
            r'(?i)(ideal|perfect)\s+for\s+(international|foreign|overseas|global)\s+candidates',
            r'(?i)(great|excellent|good)\s+opportunity\s+for\s+(international|foreign|overseas|global)\s+candidates',
            r'(?i)we\s+value\s+diversity',
            r'(?i)we\s+are\s+an\s+equal\s+opportunity\s+employer',
            r'(?i)we\s+embrace\s+cultural\s+diversity',
            r'(?i)diverse\s+perspectives\s+are\s+valued',
            r'(?i)we\s+celebrate\s+diversity',
            r'(?i)(join|joining)\s+our\s+(international|global|diverse)\s+team',
            r'(?i)background\s+is\s+not\s+important',
            r'(?i)regardless\s+of\s+(nationality|background)',
            r'(?i)we\s+are\s+committed\s+to\s+diversity',
            r'(?i)we\s+are\s+building\s+a\s+diverse\s+team',
            r'(?i)applicants\s+of\s+all\s+backgrounds',
            r'(?i)applicants\s+from\s+all\s+countries',
            r'(?i)no\s+prior\s+experience\s+in\s+japan\s+required'
        ]
        
        # Phrases négatives qui peuvent indiquer des difficultés pour les étrangers
        negative_phrases = [
            r'(?i)must\s+understand\s+japanese\s+business\s+culture',
            r'(?i)must\s+be\s+familiar\s+with\s+japanese\s+(business|work)\s+(culture|practices|customs)',
            r'(?i)knowledge\s+of\s+japanese\s+market\s+required',
            r'(?i)experience\s+in\s+japan\s+required',
            r'(?i)must\s+be\s+able\s+to\s+adapt\s+to\s+japanese\s+work\s+environment',
            r'(?i)candidates\s+must\s+already\s+be\s+in\s+japan',
            r'(?i)no\s+visa\s+sponsorship',
            r'(?i)no\s+relocation\s+support',
            r'(?i)must\s+already\s+have\s+valid\s+work\s+permit',
            r'(?i)must\s+be\s+eligible\s+to\s+work\s+in\s+japan'
        ]
        
        # Comptage des phrases positives
        positive_found = []
        for phrase in positive_phrases:
            matches = re.finditer(phrase, description)
            for match in matches:
                positive_found.append(match.group(0))
                score += 5
        
        if positive_found:
            logger.info(f"Expressions positives pour étrangers trouvées ({len(positive_found)}): {', '.join(positive_found[:3])}")
        
        # Comptage des phrases négatives
        negative_found = []
        for phrase in negative_phrases:
            matches = re.finditer(phrase, description)
            for match in matches:
                negative_found.append(match.group(0))
                score -= 5
        
        if negative_found:
            logger.info(f"Expressions négatives pour étrangers trouvées ({len(negative_found)}): {', '.join(negative_found[:3])}")
        
        # Analyse simple des sentiments basée sur des mots-clés
        positive_sentiment_words = [
            'welcome', 'opportunity', 'diversity', 'inclusive', 'global', 'international',
            'support', 'assist', 'help', 'flexible', 'open', 'multicultural', 'diverse'
        ]
        
        negative_sentiment_words = [
            'required', 'must', 'essential', 'mandatory', 'necessary', 'expected',
            'no sponsorship', 'no support', 'no relocation', 'already in Japan'
        ]
        
        # Compter les occurrences de mots positifs et négatifs
        positive_word_count = sum(1 for word in positive_sentiment_words if re.search(r'(?i)\b' + word + r'\b', description))
        negative_word_count = sum(1 for word in negative_sentiment_words if re.search(r'(?i)\b' + word + r'\b', description))
        
        # Bonus si beaucoup de mots positifs
        if positive_word_count > negative_word_count + 5:
            score += 5
            logger.info(f"Sentiment général positif: {positive_word_count} mots positifs vs {negative_word_count} négatifs")
        
        # Malus si beaucoup de mots négatifs
        if negative_word_count > positive_word_count:
            score -= 5
            logger.info(f"Sentiment général négatif: {negative_word_count} mots négatifs vs {positive_word_count} positifs")
        
        return min(score, 15)  # Maximum 15 points

    def detect_additional_benefits(self, description):
        """
        Détecte d'autres avantages qui pourraient être intéressants pour les expatriés
        Cette fonction est utilisée pour information uniquement et n'affecte pas le score
        """
        benefits = []
        
        benefit_patterns = {
            'Flexibilité horaire': r'(?i)flexible\s+(working\s+hours|schedule)',
            'Télétravail': r'(?i)(remote\s+work|work\s+from\s+home|hybrid\s+work)',
            'Formation continue': r'(?i)(training|education)\s+(allowance|program|opportunities)',
            'Assurance santé': r'(?i)health\s+insurance',
            'Retraite/401k': r'(?i)(retirement|pension|401k)',
            'Bonus': r'(?i)(bonus|incentive)',
            'Stock options': r'(?i)(stock\s+options|equity)',
            'Remboursement transport': r'(?i)(transportation|commuting)\s+(allowance|benefit)',
            'Activités team building': r'(?i)(team\s+building|social\s+events)',
            'Gym/Fitness': r'(?i)(gym|fitness|wellness)\s+(membership|allowance|program)',
            'Primes bi-annuelles': r'(?i)(bi-annual|twice\s+a\s+year)\s+(bonus|payment)',
            'Smartphone fourni': r'(?i)(company|provided)\s+(phone|smartphone|mobile)',
            'Ordinateur portable fourni': r'(?i)(company|provided)\s+(laptop|computer)',
            'Repas fournis': r'(?i)(free|provided|subsidized)\s+(meals|lunch|dinner|food)',
            'Café/Snacks gratuits': r'(?i)(free|complimentary)\s+(coffee|drinks|snacks)',
            'Allocation repas': r'(?i)(meal|lunch)\s+allowance',
            'Prime de démarrage': r'(?i)(signing|welcome|starting)\s+bonus',
            'Frais de déménagement': r'(?i)moving\s+expenses',
            'Indemnité journalière': r'(?i)per\s+diem',
            'Garde d\'enfants': r'(?i)(childcare|daycare)\s+(allowance|benefit|support)',
            'Espace de co-working': r'(?i)(co-working|coworking)\s+space',
            'Évènements sociaux': r'(?i)(social|company)\s+events',
            'Jours supplémentaires de congés': r'(?i)extra\s+(vacation|leave|holiday)\s+days',
            'Journées bien-être': r'(?i)wellness\s+days',
            'Remboursement formation': r'(?i)(education|tuition)\s+reimbursement',
            'Cours de japonais': r'(?i)japanese\s+(lessons|classes|training)'
        }
        
        for benefit_name, pattern in benefit_patterns.items():
            if re.search(pattern, description):
                benefits.append(benefit_name)
                logger.info(f"Avantage supplémentaire détecté: {benefit_name}")
        
        return benefits

    def scrape_jobs(self, max_pages=5):
        """Scrape les offres d'emploi et les filtre"""
        logger.info(f"Début du scraping sur {max_pages} pages maximum")
        jobs = []
        
        for page in range(max_pages):
            logger.info(f"Analyse de la page {page + 1}")
            
            # Faire défiler la page pour charger toutes les offres
            logger.info("Défilement de la page pour charger toutes les offres...")
            
            # Défiler progressivement pour s'assurer que toutes les offres sont chargées
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            for _ in range(5):  # Faire plusieurs défilements
                # Défiler vers le bas
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Attendre le chargement des éléments
                
                # Calculer la nouvelle hauteur
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break  # Si la hauteur n'a pas changé, on a atteint le bas de la page
                last_height = new_height
            
            logger.info("Défilement terminé, toutes les offres devraient être chargées")
            
            # Recherche de tous les liens de titres d'offres après défilement
            logger.info("Recherche des liens de titres d'offres...")
            
            # Attendre que la page soit complètement chargée
            time.sleep(3)
            
            try:
                # Sélecteur spécifique pour les liens de titres d'offres
                job_links = self.driver.find_elements(By.CSS_SELECTOR, "a.job-card-list__title--link")
                initial_job_count = len(job_links)
                logger.info(f"Nombre de liens d'offres trouvés avec le sélecteur principal: {initial_job_count}")
                
                # Si aucun lien n'est trouvé, essayer des sélecteurs alternatifs
                if initial_job_count == 0:
                    logger.info("Essai avec des sélecteurs alternatifs...")
                    
                    # Essayer d'autres sélecteurs
                    alternative_selectors = [
                        ".job-card-container__link",
                        "a[href*='/jobs/view/']",
                        ".job-card-list a[class*='title']",
                        "h3 a"
                    ]
                    
                    for selector in alternative_selectors:
                        job_links = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        logger.info(f"Sélecteur {selector}: {len(job_links)} liens trouvés")
                        if len(job_links) > 0:
                            break
                
                # Si on a toujours pas trouvé de liens
                if len(job_links) == 0:
                    logger.warning("Aucun lien d'offre trouvé, vérification de l'URL actuelle...")
                    current_url = self.driver.current_url
                    logger.info(f"URL actuelle: {current_url}")
                    
                    # Si nous sommes redirigés vers le feed ou une autre page
                    if "/jobs/search" not in current_url:
                        logger.warning("Nous ne sommes plus sur la page de recherche d'emplois!")
                        # Revenir à la page de recherche
                        logger.info("Tentative de retour à la page de recherche...")
                        base_url = "https://www.linkedin.com/jobs/search"
                        search_query = "Technical+Consultant+OR+Software+Consultant+OR+Professional+Services"
                        geo_id = "101355337"  # ID pour Tokyo, Japan
                        search_url = f"{base_url}?keywords={search_query}&distance=25&geoId={geo_id}"
                        self.driver.get(search_url)
                        time.sleep(10)
                        # Essayer à nouveau
                        job_links = self.driver.find_elements(By.CSS_SELECTOR, "a.job-card-list__title--link, .job-card-container__link")
                        logger.info(f"Après redirection: {len(job_links)} liens trouvés")
                
                # Continuer seulement si on a des liens
                if len(job_links) == 0:
                    logger.error("Impossible de trouver des liens d'offres d'emploi. Passage à la page suivante.")
                    break
                
                # Capturer le nombre définitif de liens d'offres
                final_job_count = len(job_links)
                if initial_job_count != final_job_count and initial_job_count > 0:
                    logger.warning(f"Le nombre d'offres a changé: initial={initial_job_count}, final={final_job_count}")
                
                # Analyser chaque offre en cliquant sur l'élément et en analysant le panneau de droite
                logger.info(f"Analyse des {final_job_count} offres trouvées")
                
                # Stockage de la liste originale des liens pour éviter toute modification pendant le traitement
                job_links_to_process = job_links.copy() if hasattr(job_links, 'copy') else list(job_links)
                
                for i, link in enumerate(job_links_to_process):
                    try:
                        logger.info(f"Analyse de l'offre {i+1}/{final_job_count}")
                        
                        # Faire défiler pour rendre le lien visible
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
                        time.sleep(1)
                        
                        # Cliquer sur le lien pour afficher les détails sur le côté droit
                        logger.info("Clic sur l'offre pour afficher les détails")
                        link.click()
                        
                        # Attendre que le panneau de détails se charge
                        logger.info("Attente du chargement du panneau de détails...")
                        try:
                            WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "div.job-view-layout.jobs-details"))
                            )
                            logger.info("Panneau de détails chargé")
                        except TimeoutException:
                            logger.warning("Timeout en attendant le panneau de détails")
                            continue
                        
                        # Faire une pause pour s'assurer que tout est chargé
                        time.sleep(3)
                        
                        # Extraire les informations depuis le panneau de détails
                        try:
                            # Titre de l'offre
                            title_selectors = [
                                "h2.jobs-unified-top-card__job-title", 
                                "h1.job-title", 
                                "h1[class*='job']", 
                                ".jobs-unified-top-card h1",
                                ".job-details-jobs-unified-top-card__job-title"
                            ]
                            title = "Titre inconnu"
                            for selector in title_selectors:
                                try:
                                    title_elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                                    title = title_elem.text.strip()
                                    if title:
                                        break
                                except:
                                    continue
                            
                            # Entreprise
                            company_selectors = [
                                "a.jobs-unified-top-card__company-name",
                                "span.jobs-unified-top-card__company-name",
                                ".jobs-unified-top-card__subtitle a",
                                ".jobs-unified-top-card__subtitle span",
                                "[class*='company-name']"
                            ]
                            company = "Entreprise inconnue"
                            for selector in company_selectors:
                                try:
                                    company_elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                                    company = company_elem.text.strip()
                                    if company:
                                        break
                                except:
                                    continue
                            
                            # Localisation - Amélioration pour capturer la localisation
                            location_selectors = [
                                "span.jobs-unified-top-card__bullet",
                                "span.jobs-unified-top-card__workplace-type",
                                ".jobs-unified-top-card__metadata-container span",
                                ".t-black--light.job-details-jobs-unified-top-card__tertiary-description-container span.tvm__text:first-child",
                                "[class*='location']"
                            ]
                            location = "Localisation inconnue"
                            for selector in location_selectors:
                                try:
                                    location_elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                                    location_text = location_elem.text.strip()
                                    if location_text and not location_text.startswith("il y a") and not location_text.startswith("·"):
                                        location = location_text
                                        break
                                except:
                                    continue
                            
                            # Description - Faire défiler jusqu'à la description pour s'assurer qu'elle est chargée
                            try:
                                description_container = self.driver.find_element(By.CSS_SELECTOR, "div.jobs-description__content")
                                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", description_container)
                                time.sleep(1)  # Attendre que le contenu se charge après le défilement
                            except:
                                logger.warning("Impossible de faire défiler jusqu'à la description")
                            
                            # Maintenant essayer d'extraire la description
                            description_selectors = [
                                "div.jobs-description__content",
                                "div.jobs-description-content",
                                ".jobs-description",
                                "[class*='description-content']",
                                "#job-details"
                            ]
                            description = "Description non disponible"
                            for selector in description_selectors:
                                try:
                                    description_elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                                    description = description_elem.text.strip()
                                    if description:
                                        break
                                except:
                                    continue
                            
                            logger.info(f"Informations extraites: {title} | {company} | {location}")
                            logger.info(f"Longueur de la description: {len(description)} caractères")
                            
                            # Obtenir l'URL de l'offre - Amélioration
                            job_url = ""
                            try:
                                # Extraire l'ID de l'offre actuelle depuis l'URL avec currentJobId
                                current_url = self.driver.current_url
                                logger.info(f"URL actuelle: {current_url}")
                                
                                if "currentJobId=" in current_url:
                                    try:
                                        # Extraire l'ID de l'offre actuelle
                                        job_id = re.search(r'currentJobId=(\d+)', current_url).group(1)
                                        # Construire une URL propre
                                        job_url = f"https://www.linkedin.com/jobs/view/{job_id}/"
                                        logger.info(f"URL extraite depuis currentJobId: {job_url}")
                                    except Exception as e:
                                        logger.error(f"Erreur lors de l'extraction du currentJobId: {str(e)}")
                                
                                # Si pas de currentJobId, essayer d'autres méthodes
                                if not job_url:
                                    # Méthodes alternatives avec les sélecteurs
                                    url_selectors = [
                                        "a.job-details-jobs-unified-top-card__job-title-link",
                                        ".jobs-unified-top-card__content a[href*='/jobs/view/']",
                                        "a[data-tracking-control-name='public_jobs_topcard-title-link']"
                                    ]
                                    
                                    for selector in url_selectors:
                                        try:
                                            url_elem = self.driver.find_element(By.CSS_SELECTOR, selector)
                                            potential_url = url_elem.get_attribute("href")
                                            if potential_url and "/jobs/view/" in potential_url:
                                                job_url = potential_url
                                                logger.info(f"URL extraite avec sélecteur {selector}: {job_url}")
                                                break
                                        except:
                                            continue
                                    
                                    # Si on est directement sur une page d'offre
                                    if not job_url and "/jobs/view/" in current_url:
                                        job_url = current_url
                                        logger.info(f"URL extraite de l'URL actuelle: {job_url}")
                                
                            except Exception as e:
                                logger.error(f"Erreur lors de l'extraction de l'URL: {str(e)}")
                            
                            # Si l'URL est toujours vide, utiliser des méthodes de secours
                            if not job_url:
                                try:
                                    # Chercher des éléments avec data-job-id
                                    job_id_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-job-id]")
                                    if job_id_elements:
                                        job_id = job_id_elements[0].get_attribute("data-job-id")
                                        if job_id:
                                            job_url = f"https://www.linkedin.com/jobs/view/{job_id}/"
                                            logger.info(f"URL construite à partir de l'ID: {job_url}")
                                except Exception as e:
                                    logger.error(f"Erreur lors de l'extraction de l'ID de l'offre: {str(e)}")
                            
                            if job_url:
                                logger.info(f"URL finale de l'offre: {job_url}")
                            else:
                                logger.warning("Impossible d'extraire l'URL de l'offre")
                            
                            # Analyser si l'offre est adaptée aux étrangers
                            is_gaijin_friendly, gaijin_details = self.is_gaijin_friendly(description)
                            
                            # On ajoute l'offre au CSV, qu'elle soit gaijin-friendly ou non
                            logger.info(f"{'✓ Offre adaptée aux étrangers' if is_gaijin_friendly else '✗ Offre non adaptée aux étrangers'}")
                            job_data = {
                                'title': title,
                                'company': company,
                                'location': location,
                                'url': job_url,
                                'is_gaijin_friendly': 'Oui' if is_gaijin_friendly else 'Non',
                                'score_total': gaijin_details['score_total'],
                                'score_japonais': gaijin_details['score_japonais'],
                                'score_international': gaijin_details['score_international'],
                                'score_avantages': gaijin_details['score_avantages'],
                                'score_conges': gaijin_details['score_conges'],
                                'score_langue': gaijin_details['score_langue'],
                                'score_sentiment': gaijin_details['score_sentiment'],
                                'jours_conges': gaijin_details['jours_conges'] if gaijin_details['jours_conges'] else 'Non spécifié',
                                'avantages': gaijin_details['avantages']
                            }
                            jobs.append(job_data)
                            
                        except Exception as e:
                            logger.error(f"Erreur lors de l'extraction des informations: {str(e)}")
                        
                        # Faire une courte pause entre chaque offre
                        time.sleep(2)
                        
                    except Exception as e:
                        logger.error(f"Erreur lors de l'analyse de l'offre {i+1}: {str(e)}")
                
            except Exception as e:
                logger.error(f"Erreur globale lors du scraping: {str(e)}")
            
            # Passer à la page suivante en utilisant les boutons de pagination numérotés
            if page < max_pages - 1:  # Si ce n'est pas la dernière page
                logger.info(f"Tentative de passage à la page {page + 2}")
                
                # Défiler vers le bas pour s'assurer que la pagination est visible
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                # Vérifier que la pagination existe
                try:
                    pagination = self.driver.find_element(By.CSS_SELECTOR, "ul.artdeco-pagination__pages")
                    logger.info("Barre de pagination trouvée")
                    
                    # Chercher le bouton pour la page suivante (page + 2 car on est à la page page + 1)
                    next_page_button = None
                    
                    # Approche 1: chercher par data-test-pagination-page-btn
                    try:
                        next_page_button = self.driver.find_element(By.CSS_SELECTOR, f"li[data-test-pagination-page-btn='{page + 2}'] button")
                        logger.info(f"Bouton pour la page {page + 2} trouvé par data-test-pagination-page-btn")
                    except:
                        logger.info("Bouton non trouvé par data-test-pagination-page-btn, essai d'autres approches")
                    
                    # Approche 2: chercher par aria-label
                    if not next_page_button:
                        try:
                            next_page_button = self.driver.find_element(By.CSS_SELECTOR, f"button[aria-label='Page {page + 2}']")
                            logger.info(f"Bouton pour la page {page + 2} trouvé par aria-label")
                        except:
                            logger.info("Bouton non trouvé par aria-label, essai d'autres approches")
                    
                    # Approche 3: chercher par le texte dans le span
                    if not next_page_button:
                        page_buttons = self.driver.find_elements(By.CSS_SELECTOR, "li.artdeco-pagination__indicator--number button")
                        for btn in page_buttons:
                            try:
                                span_text = btn.find_element(By.TAG_NAME, "span").text
                                if span_text == str(page + 2):
                                    next_page_button = btn
                                    logger.info(f"Bouton pour la page {page + 2} trouvé par texte")
                                    break
                            except:
                                continue
                    
                    if next_page_button:
                        # Faire défiler pour voir le bouton
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", next_page_button)
                        time.sleep(1)
                        
                        # Essayer de cliquer sur le bouton
                        try:
                            next_page_button.click()
                            logger.info(f"Clic sur le bouton de la page {page + 2}")
                            time.sleep(5)  # Attendre que la page se charge
                        except Exception as e:
                            logger.error(f"Erreur lors du clic sur le bouton de pagination: {str(e)}")
                            
                            # Essayer avec JavaScript si le clic normal échoue
                            try:
                                self.driver.execute_script("arguments[0].click();", next_page_button)
                                logger.info(f"Clic avec JavaScript sur le bouton de la page {page + 2}")
                                time.sleep(5)  # Attendre que la page se charge
                            except Exception as e:
                                logger.error(f"Échec du clic avec JavaScript: {str(e)}")
                                
                                # Dernière tentative: construire l'URL directement
                                try:
                                    base_url = "https://www.linkedin.com/jobs/search"
                                    search_query = "Technical+Consultant+OR+Software+Consultant+OR+Professional+Services"
                                    geo_id = "101355337"  # ID pour Tokyo, Japan
                                    page_start = page * 25 + 25  # 25 offres par page
                                    next_url = f"{base_url}?keywords={search_query}&distance=25&geoId={geo_id}&start={page_start}"
                                    
                                    logger.info(f"Navigation directe vers la page {page + 2}: {next_url}")
                                    self.driver.get(next_url)
                                    time.sleep(5)
                                except Exception as e:
                                    logger.error(f"Échec de la navigation directe: {str(e)}")
                                    break
                    else:
                        logger.error(f"Bouton pour la page {page + 2} non trouvé")
                        
                        # Utiliser la navigation directe par URL si le bouton n'est pas trouvé
                        try:
                            base_url = "https://www.linkedin.com/jobs/search"
                            search_query = "Technical+Consultant+OR+Software+Consultant+OR+Professional+Services"
                            geo_id = "101355337"  # ID pour Tokyo, Japan
                            page_start = page * 25 + 25  # 25 offres par page
                            next_url = f"{base_url}?keywords={search_query}&distance=25&geoId={geo_id}&start={page_start}"
                            
                            logger.info(f"Navigation directe vers la page {page + 2}: {next_url}")
                            self.driver.get(next_url)
                            time.sleep(5)
                        except Exception as e:
                            logger.error(f"Échec de la navigation directe: {str(e)}")
                            break
                            
                except Exception as e:
                    logger.error(f"Erreur lors de la recherche de la pagination: {str(e)}")
                    
                    # Utiliser la navigation directe par URL si la pagination n'est pas trouvée
                    try:
                        base_url = "https://www.linkedin.com/jobs/search"
                        search_query = "Technical+Consultant+OR+Software+Consultant+OR+Professional+Services"
                        geo_id = "101355337"  # ID pour Tokyo, Japan
                        page_start = page * 25 + 25  # 25 offres par page
                        next_url = f"{base_url}?keywords={search_query}&distance=25&geoId={geo_id}&start={page_start}"
                        
                        logger.info(f"Navigation directe vers la page {page + 2}: {next_url}")
                        self.driver.get(next_url)
                        time.sleep(5)
                    except Exception as e:
                        logger.error(f"Échec de la navigation directe: {str(e)}")
                        break
        
        logger.info(f"Scraping terminé. {len(jobs)} offres trouvées")
        return jobs
        
    def save_to_csv(self, jobs, filename='linkedin_jobs.csv'):
        """Sauvegarde les offres dans un fichier CSV (méthode obsolète, utilisée pour compatibilité)"""
        logger.info(f"Sauvegarde des {len(jobs)} offres dans {filename}")
        df = pd.DataFrame(jobs)
        df.to_csv(filename, index=False, encoding='utf-8')
        logger.info("Sauvegarde terminée")
        
    def export_data(self, jobs):
        """Exporte les données dans tous les formats disponibles en utilisant l'exporteur dédié"""
        try:
            # Importer l'exporteur
            from linkedin_export import LinkedInExporter
            exporter = LinkedInExporter()
            
            # Exporter les données
            export_files = exporter.export_all(jobs)
            
            logger.info("Export des données terminé avec succès")
            logger.info(f"CSV: {export_files['csv']}")
            logger.info(f"Excel: {export_files['excel']}")
            logger.info(f"Rapport HTML: {export_files['html']}")
            
            return export_files
        except Exception as e:
            logger.error(f"Erreur lors de l'export: {str(e)}")
            # Utiliser la méthode de sauvegarde traditionnelle en cas d'erreur
            logger.info("Utilisation de la méthode de sauvegarde traditionnelle")
            self.save_to_csv(jobs)
            return None
    
    def close(self):
        """Ferme le driver"""
        if self.driver:
            logger.info("Fermeture du driver Firefox")
            self.driver.quit()
            
def main():
    # Configurer le parser d'arguments
    parser = argparse.ArgumentParser(description="LinkedIn Gaijin Jobs Scraper")
    parser.add_argument("--pages", type=int, default=5, help="Nombre de pages à scraper (défaut: 5)")
    parser.add_argument("--keywords", type=str, default="Technical Consultant,Software Consultant,Professional Services",
                      help="Mots-clés de recherche séparés par des virgules (défaut: 'Technical Consultant,Software Consultant,Professional Services')")
    parser.add_argument("--location", type=str, default="Tokyo, Japan",
                      help="Localisation pour la recherche (défaut: 'Tokyo, Japan')")
    
    # Parser les arguments
    args = parser.parse_args()
    
    # Convertir la chaîne de mots-clés en liste
    keywords = [keyword.strip() for keyword in args.keywords.split(",")]
    
    logger.info("Démarrage du script")
    logger.info(f"Configuration: {args.pages} pages, mots-clés: {keywords}, localisation: {args.location}")
    
    scraper = LinkedInScraper()
    try:
        scraper.login()
        # Recherche avec les mots-clés et localisation spécifiés
        scraper.search_jobs(keywords=keywords, location=args.location)
        
        # Utiliser le nombre de pages spécifié
        jobs = scraper.scrape_jobs(max_pages=args.pages)
        
        # Utiliser le nouvel exporteur
        scraper.export_data(jobs)
        
        # Afficher les statistiques
        friendly_jobs = [job for job in jobs if job['is_gaijin_friendly'] == 'Oui']
        logger.info(f"Statistiques: {len(jobs)} offres au total, dont {len(friendly_jobs)} gaijin-friendly")
    except Exception as e:
        logger.error(f"Une erreur est survenue: {str(e)}")
    finally:
        scraper.close()
        logger.info("Script terminé")

if __name__ == "__main__":
    main() 