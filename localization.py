"""
Localization module for the LinkedIn Jobs Scraper.
This module provides translation support for the application.
"""

class Localization:
    """
    Handles localization for the LinkedIn Scraper.
    Supports multiple languages with fallback to English.
    """
    
    # Available languages
    ENGLISH = 'en'
    FRENCH = 'fr'
    
    # Default language
    DEFAULT_LANGUAGE = ENGLISH
    
    def __init__(self, language=DEFAULT_LANGUAGE):
        """
        Initialize the localization with the specified language.
        
        Args:
            language (str): Language code ('en' for English, 'fr' for French)
        """
        self.language = language if language in [self.ENGLISH, self.FRENCH] else self.DEFAULT_LANGUAGE
        self._translations = self._load_translations()
    
    def _load_translations(self):
        """Load all translations for the supported languages."""
        return {
            # Log messages
            'script_start': {
                self.ENGLISH: "Starting the script",
                self.FRENCH: "Démarrage du script"
            },
            'script_end': {
                self.ENGLISH: "Script finished",
                self.FRENCH: "Script terminé"
            },
            'error_occurred': {
                self.ENGLISH: "An error occurred: {0}",
                self.FRENCH: "Une erreur est survenue: {0}"
            },
            'scraper_init': {
                self.ENGLISH: "Initializing LinkedIn scraper...",
                self.FRENCH: "Initialisation du scraper LinkedIn..."
            },
            'config_driver': {
                self.ENGLISH: "Configuring Firefox driver...",
                self.FRENCH: "Configuration du driver Firefox..."
            },
            'driver_success': {
                self.ENGLISH: "Firefox driver configured successfully",
                self.FRENCH: "Driver Firefox configuré avec succès"
            },
            'driver_error': {
                self.ENGLISH: "Failed to configure driver: {0}",
                self.FRENCH: "Échec de la configuration du driver: {0}"
            },
            'login_attempt': {
                self.ENGLISH: "Attempting to log in to LinkedIn...",
                self.FRENCH: "Tentative de connexion à LinkedIn..."
            },
            'login_field_found': {
                self.ENGLISH: "Login field found",
                self.FRENCH: "Champ de connexion trouvé"
            },
            'login_page_error': {
                self.ENGLISH: "The login page could not be loaded",
                self.FRENCH: "La page de connexion n'a pas pu être chargée"
            },
            'missing_credentials': {
                self.ENGLISH: "LinkedIn credentials are not configured in the .env file",
                self.FRENCH: "Les identifiants LinkedIn ne sont pas configurés dans le fichier .env"
            },
            'email_entered': {
                self.ENGLISH: "Email entered",
                self.FRENCH: "Email saisi"
            },
            'password_entered': {
                self.ENGLISH: "Password entered",
                self.FRENCH: "Mot de passe saisi"
            },
            'login_button_clicked': {
                self.ENGLISH: "Login button clicked",
                self.FRENCH: "Bouton de connexion cliqué"
            },
            'verification_page': {
                self.ENGLISH: "Verification page detected",
                self.FRENCH: "Page de vérification détectée"
            },
            'manual_verification': {
                self.ENGLISH: "Please complete the security verification manually, then press Enter...",
                self.FRENCH: "Veuillez compléter la vérification de sécurité manuellement, puis appuyez sur Entrée..."
            },
            'login_check': {
                self.ENGLISH: "Checking successful login...",
                self.FRENCH: "Vérification de la connexion réussie..."
            },
            'current_url': {
                self.ENGLISH: "Current URL: {0}",
                self.FRENCH: "URL actuelle: {0}"
            },
            'still_on_login': {
                self.ENGLISH: "We are still on the login page",
                self.FRENCH: "Nous sommes toujours sur la page de connexion"
            },
            'login_failed': {
                self.ENGLISH: "Login failed - we are still on the login page",
                self.FRENCH: "La connexion a échoué - nous sommes toujours sur la page de connexion"
            },
            'element_found': {
                self.ENGLISH: "Element found with selector: {0}",
                self.FRENCH: "Élément trouvé avec le sélecteur: {0}"
            },
            'no_nav_element': {
                self.ENGLISH: "No navigation element found, but login seems successful",
                self.FRENCH: "Aucun élément de navigation trouvé, mais la connexion semble réussie"
            },
            'continue_with_url': {
                self.ENGLISH: "Continue with current URL",
                self.FRENCH: "Continuer avec l'URL actuelle"
            },
            'login_success': {
                self.ENGLISH: "Successfully logged in to LinkedIn",
                self.FRENCH: "Connexion à LinkedIn réussie"
            },
            'login_error': {
                self.ENGLISH: "Error during login: {0}",
                self.FRENCH: "Erreur lors de la connexion: {0}"
            },
            
            # Job search messages
            'search_jobs': {
                self.ENGLISH: "Searching for jobs with keywords: {0}",
                self.FRENCH: "Recherche d'offres avec les mots-clés: {0}"
            },
            'search_location': {
                self.ENGLISH: "Location: {0}",
                self.FRENCH: "Localisation: {0}"
            },
            'search_url': {
                self.ENGLISH: "Search URL: {0}",
                self.FRENCH: "URL de recherche: {0}"
            },
            'navigate_results': {
                self.ENGLISH: "Navigating to results page...",
                self.FRENCH: "Navigation vers la page de résultats..."
            },
            'cookie_closed': {
                self.ENGLISH: "Cookie popup closed",
                self.FRENCH: "Popup de cookies fermé"
            },
            'no_cookie_popup': {
                self.ENGLISH: "No cookie popup detected",
                self.FRENCH: "Pas de popup de cookies détecté"
            },
            'page_load_wait': {
                self.ENGLISH: "Waiting for page to fully load...",
                self.FRENCH: "Attente du chargement complet de la page..."
            },
            
            # Job scraping messages
            'begin_scraping': {
                self.ENGLISH: "Beginning scraping on {0} pages maximum",
                self.FRENCH: "Début du scraping sur {0} pages maximum"
            },
            'analyzing_page': {
                self.ENGLISH: "Analyzing page {0}",
                self.FRENCH: "Analyse de la page {0}"
            },
            'scrolling_page': {
                self.ENGLISH: "Scrolling page to load all job listings...",
                self.FRENCH: "Défilement de la page pour charger toutes les offres..."
            },
            'scrolling_done': {
                self.ENGLISH: "Scrolling complete, all job listings should be loaded",
                self.FRENCH: "Défilement terminé, toutes les offres devraient être chargées"
            },
            'searching_job_links': {
                self.ENGLISH: "Searching for job listing links...",
                self.FRENCH: "Recherche des liens de titres d'offres..."
            },
            'job_links_found': {
                self.ENGLISH: "Number of job links found with primary selector: {0}",
                self.FRENCH: "Nombre de liens d'offres trouvés avec le sélecteur principal: {0}"
            },
            'trying_alt_selectors': {
                self.ENGLISH: "Trying alternative selectors...",
                self.FRENCH: "Essai avec des sélecteurs alternatifs..."
            },
            'selector_links_found': {
                self.ENGLISH: "Selector {0}: {1} links found",
                self.FRENCH: "Sélecteur {0}: {1} liens trouvés"
            },
            'no_job_links': {
                self.ENGLISH: "No job links found, checking current URL...",
                self.FRENCH: "Aucun lien d'offre trouvé, vérification de l'URL actuelle..."
            },
            'not_on_search_page': {
                self.ENGLISH: "We are not on the jobs search page!",
                self.FRENCH: "Nous ne sommes plus sur la page de recherche d'emplois!"
            },
            'return_to_search': {
                self.ENGLISH: "Attempting to return to search page...",
                self.FRENCH: "Tentative de retour à la page de recherche..."
            },
            'after_redirect': {
                self.ENGLISH: "After redirection: {0} links found",
                self.FRENCH: "Après redirection: {0} liens trouvés"
            },
            'cannot_find_links': {
                self.ENGLISH: "Unable to find job listing links. Moving to next page.",
                self.FRENCH: "Impossible de trouver des liens d'offres d'emploi. Passage à la page suivante."
            },
            
            # Analyzing individual jobs
            'analyzing_job': {
                self.ENGLISH: "Analyzing job {0}/{1}",
                self.FRENCH: "Analyse de l'offre {0}/{1}"
            },
            'click_job': {
                self.ENGLISH: "Clicking job to display details",
                self.FRENCH: "Clic sur l'offre pour afficher les détails"
            },
            'waiting_details': {
                self.ENGLISH: "Waiting for details panel to load...",
                self.FRENCH: "Attente du chargement du panneau de détails..."
            },
            'details_loaded': {
                self.ENGLISH: "Details panel loaded",
                self.FRENCH: "Panneau de détails chargé"
            },
            'details_timeout': {
                self.ENGLISH: "Timeout waiting for details panel",
                self.FRENCH: "Timeout en attendant le panneau de détails"
            },
            'info_extracted': {
                self.ENGLISH: "Information extracted: {0} | {1} | {2}",
                self.FRENCH: "Informations extraites: {0} | {1} | {2}"
            },
            'description_length': {
                self.ENGLISH: "Description length: {0} characters",
                self.FRENCH: "Longueur de la description: {0} caractères"
            },
            'url_extraction_error': {
                self.ENGLISH: "Error extracting URL: {0}",
                self.FRENCH: "Erreur lors de l'extraction de l'URL: {0}"
            },
            'current_job_id': {
                self.ENGLISH: "URL extracted from currentJobId: {0}",
                self.FRENCH: "URL extraite depuis currentJobId: {0}"
            },
            'current_job_id_error': {
                self.ENGLISH: "Error extracting currentJobId: {0}",
                self.FRENCH: "Erreur lors de l'extraction du currentJobId: {0}"
            },
            'url_from_selector': {
                self.ENGLISH: "URL extracted with selector {0}: {1}",
                self.FRENCH: "URL extraite avec sélecteur {0}: {1}"
            },
            'url_from_current': {
                self.ENGLISH: "URL extracted from current URL: {0}",
                self.FRENCH: "URL extraite de l'URL actuelle: {0}"
            },
            'url_from_id': {
                self.ENGLISH: "URL constructed from ID: {0}",
                self.FRENCH: "URL construite à partir de l'ID: {0}"
            },
            'id_extraction_error': {
                self.ENGLISH: "Error extracting job ID: {0}",
                self.FRENCH: "Erreur lors de l'extraction de l'ID de l'offre: {0}"
            },
            'final_url': {
                self.ENGLISH: "Final job URL: {0}",
                self.FRENCH: "URL finale de l'offre: {0}"
            },
            'no_url': {
                self.ENGLISH: "Unable to extract job URL",
                self.FRENCH: "Impossible d'extraire l'URL de l'offre"
            },
            'gaijin_friendly': {
                self.ENGLISH: "✓ Job suitable for foreigners",
                self.FRENCH: "✓ Offre adaptée aux étrangers"
            },
            'not_gaijin_friendly': {
                self.ENGLISH: "✗ Job not suitable for foreigners",
                self.FRENCH: "✗ Offre non adaptée aux étrangers"
            },
            'job_extraction_error': {
                self.ENGLISH: "Error extracting job information: {0}",
                self.FRENCH: "Erreur lors de l'extraction des informations: {0}"
            },
            'job_analysis_error': {
                self.ENGLISH: "Error analyzing job {0}: {1}",
                self.FRENCH: "Erreur lors de l'analyse de l'offre {0}: {1}"
            },
            'global_scraping_error': {
                self.ENGLISH: "Global error during scraping: {0}",
                self.FRENCH: "Erreur globale lors du scraping: {0}"
            },
            
            # Pagination
            'next_page_attempt': {
                self.ENGLISH: "Attempting to move to page {0}",
                self.FRENCH: "Tentative de passage à la page {0}"
            },
            'pagination_found': {
                self.ENGLISH: "Pagination bar found",
                self.FRENCH: "Barre de pagination trouvée"
            },
            'button_found': {
                self.ENGLISH: "Button for page {0} found by {1}",
                self.FRENCH: "Bouton pour la page {0} trouvé par {1}"
            },
            'click_page_button': {
                self.ENGLISH: "Clicking button for page {0}",
                self.FRENCH: "Clic sur le bouton de la page {0}"
            },
            'page_button_error': {
                self.ENGLISH: "Error clicking pagination button: {0}",
                self.FRENCH: "Erreur lors du clic sur le bouton de pagination: {0}"
            },
            'js_click': {
                self.ENGLISH: "JavaScript click on button for page {0}",
                self.FRENCH: "Clic avec JavaScript sur le bouton de la page {0}"
            },
            'js_click_error': {
                self.ENGLISH: "JavaScript click failed: {0}",
                self.FRENCH: "Échec du clic avec JavaScript: {0}"
            },
            'direct_navigation': {
                self.ENGLISH: "Direct navigation to page {0}: {1}",
                self.FRENCH: "Navigation directe vers la page {0}: {1}"
            },
            'direct_nav_error': {
                self.ENGLISH: "Direct navigation failed: {0}",
                self.FRENCH: "Échec de la navigation directe: {0}"
            },
            'page_button_not_found': {
                self.ENGLISH: "Button for page {0} not found",
                self.FRENCH: "Bouton pour la page {0} non trouvé"
            },
            'pagination_error': {
                self.ENGLISH: "Error finding pagination: {0}",
                self.FRENCH: "Erreur lors de la recherche de la pagination: {0}"
            },
            
            # Scraping completion
            'scraping_complete': {
                self.ENGLISH: "Scraping complete. {0} jobs found",
                self.FRENCH: "Scraping terminé. {0} offres trouvées"
            },
            'saving_jobs': {
                self.ENGLISH: "Saving {0} jobs to {1}",
                self.FRENCH: "Sauvegarde des {0} offres dans {1}"
            },
            'save_complete': {
                self.ENGLISH: "Save complete",
                self.FRENCH: "Sauvegarde terminée"
            },
            'exporting_data': {
                self.ENGLISH: "Exporting data...",
                self.FRENCH: "Export des données..."
            },
            'export_complete': {
                self.ENGLISH: "Data export completed successfully",
                self.FRENCH: "Export des données terminé avec succès"
            },
            'csv_file': {
                self.ENGLISH: "CSV: {0}",
                self.FRENCH: "CSV: {0}"
            },
            'excel_file': {
                self.ENGLISH: "Excel: {0}",
                self.FRENCH: "Excel: {0}"
            },
            'html_report': {
                self.ENGLISH: "HTML Report: {0}",
                self.FRENCH: "Rapport HTML: {0}"
            },
            'export_error': {
                self.ENGLISH: "Error during export: {0}",
                self.FRENCH: "Erreur lors de l'export: {0}"
            },
            'using_traditional': {
                self.ENGLISH: "Using traditional save method",
                self.FRENCH: "Utilisation de la méthode de sauvegarde traditionnelle"
            },
            'closing_driver': {
                self.ENGLISH: "Closing Firefox driver",
                self.FRENCH: "Fermeture du driver Firefox"
            },
            'stats_summary': {
                self.ENGLISH: "Statistics: {0} jobs total, of which {1} are gaijin-friendly",
                self.FRENCH: "Statistiques: {0} offres au total, dont {1} gaijin-friendly"
            },
            
            # Gaijin-friendly analysis
            'gaijin_score': {
                self.ENGLISH: "Gaijin-friendly score: {0}",
                self.FRENCH: "Score gaijin-friendly: {0}"
            },
            'score_details': {
                self.ENGLISH: "Japanese: {0}, International: {1}, Benefits: {2}, Leave: {3}, Language: {4}, Sentiment: {5}",
                self.FRENCH: "Japonais: {0}, International: {1}, Avantages: {2}, Congés: {3}, Langue: {4}, Sentiment: {5}"
            },
            'leave_days': {
                self.ENGLISH: "Leave days: {0}",
                self.FRENCH: "Jours de congés: {0}"
            },
            'additional_benefits': {
                self.ENGLISH: "Additional benefits: {0}",
                self.FRENCH: "Avantages supplémentaires: {0}"
            },
            'positive_expr': {
                self.ENGLISH: "Positive expressions found ({0}): {1}",
                self.FRENCH: "Expressions positives trouvées ({0}): {1}"
            },
            'negative_expr': {
                self.ENGLISH: "Negative expressions found ({0}): {1}",
                self.FRENCH: "Expressions négatives trouvées ({0}): {1}"
            },
            'jlpt_high': {
                self.ENGLISH: "High JLPT requirement: {0}",
                self.FRENCH: "Exigence JLPT élevée: {0}"
            },
            'jlpt_mid': {
                self.ENGLISH: "Intermediate JLPT requirement: {0}",
                self.FRENCH: "Exigence JLPT intermédiaire: {0}"
            },
            'jlpt_basic': {
                self.ENGLISH: "Basic JLPT requirement: {0}",
                self.FRENCH: "Exigence JLPT basique: {0}"
            },
            'positive_context': {
                self.ENGLISH: "Positive context found: {0}",
                self.FRENCH: "Contexte positif trouvé: {0}"
            },
            'negative_context': {
                self.ENGLISH: "Negative context found: {0}",
                self.FRENCH: "Contexte négatif trouvé: {0}"
            },
            'multi_pos_bonus': {
                self.ENGLISH: "Bonus: Multiple positive indicators without negatives",
                self.FRENCH: "Bonus: Multiples indicateurs positifs sans négatifs"
            },
            'international_indicators': {
                self.ENGLISH: "International environment indicators found ({0}): {1}",
                self.FRENCH: "Indicateurs d'environnement international trouvés ({0}): {1}"
            },
            'global_keywords_bonus': {
                self.ENGLISH: "Bonus: {0} global keywords found",
                self.FRENCH: "Bonus: {0} mots-clés globaux trouvés"
            },
            'expat_benefits': {
                self.ENGLISH: "Expat benefits found ({0}): {1}",
                self.FRENCH: "Avantages pour expatriés trouvés ({0}): {1}"
            },
            'benefits_context': {
                self.ENGLISH: "Benefits context found: {0}",
                self.FRENCH: "Contexte d'avantages trouvé: {0}"
            },
            'leave_policies': {
                self.ENGLISH: "Favorable leave policies found ({0}): {1}",
                self.FRENCH: "Politiques de congés favorables trouvées ({0}): {1}"
            },
            'leave_days_mentioned': {
                self.ENGLISH: "Leave days mentioned: {0}",
                self.FRENCH: "Nombre de jours de congés mentionné: {0}"
            },
            'high_leave_bonus': {
                self.ENGLISH: "High bonus for {0} leave days",
                self.FRENCH: "Bonus élevé pour {0} jours de congés"
            },
            'significant_leave_bonus': {
                self.ENGLISH: "Significant bonus for {0} leave days",
                self.FRENCH: "Bonus important pour {0} jours de congés"
            },
            'moderate_leave_bonus': {
                self.ENGLISH: "Bonus for {0} leave days",
                self.FRENCH: "Bonus pour {0} jours de congés"
            },
            'small_leave_bonus': {
                self.ENGLISH: "Small bonus for {0} leave days",
                self.FRENCH: "Petit bonus pour {0} jours de congés"
            },
            'leave_keywords_bonus': {
                self.ENGLISH: "Bonus: {0} leave keywords found",
                self.FRENCH: "Bonus: {0} mots-clés de congés trouvés"
            },
            'french_indices': {
                self.ENGLISH: "French language indicators found ({0}): {1}",
                self.FRENCH: "Indices de français trouvés ({0}): {1}"
            },
            'job_in_english': {
                self.ENGLISH: "Job listing written in English",
                self.FRENCH: "Offre rédigée en anglais"
            },
            'job_in_french': {
                self.ENGLISH: "Job listing written in French",
                self.FRENCH: "Offre rédigée en français"
            },
            'job_in_japanese': {
                self.ENGLISH: "Job listing written in Japanese",
                self.FRENCH: "Offre rédigée en japonais"
            },
            'lang_detect_error': {
                self.ENGLISH: "Unable to detect job listing language",
                self.FRENCH: "Impossible de détecter la langue de l'offre"
            },
            'positives_for_foreigners': {
                self.ENGLISH: "Positive expressions for foreigners found ({0}): {1}",
                self.FRENCH: "Expressions positives pour étrangers trouvées ({0}): {1}"
            },
            'negatives_for_foreigners': {
                self.ENGLISH: "Negative expressions for foreigners found ({0}): {1}",
                self.FRENCH: "Expressions négatives pour étrangers trouvées ({0}): {1}"
            },
            'general_positive': {
                self.ENGLISH: "Generally positive sentiment: {0} positive words vs {1} negative",
                self.FRENCH: "Sentiment général positif: {0} mots positifs vs {1} négatifs"
            },
            'general_negative': {
                self.ENGLISH: "Generally negative sentiment: {0} negative words vs {1} positive",
                self.FRENCH: "Sentiment général négatif: {0} mots négatifs vs {1} positifs"
            },
            'additional_benefit_detected': {
                self.ENGLISH: "Additional benefit detected: {0}",
                self.FRENCH: "Avantage supplémentaire détecté: {0}"
            },
            
            # Configuration messages
            'config_info': {
                self.ENGLISH: "Configuration: {0} pages, keywords: {1}, location: {2}",
                self.FRENCH: "Configuration: {0} pages, mots-clés: {1}, localisation: {2}"
            },
        }
    
    def get(self, key, *args):
        """
        Get the translation for the specified key and format it with the given arguments.
        
        Args:
            key (str): The translation key
            *args: Arguments to format the translation string
            
        Returns:
            str: The translated string
        """
        if key not in self._translations:
            # Return the key itself if not found (helps with debugging)
            return key if not args else key.format(*args)
        
        # Get the translation for the current language, fallback to English
        translation = self._translations[key].get(self.language, self._translations[key].get(self.DEFAULT_LANGUAGE, key))
        
        # Format the translation if arguments are provided
        if args:
            try:
                return translation.format(*args)
            except:
                return translation
        return translation

# Create a singleton instance
i18n = Localization() 