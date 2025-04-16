"""
Example of using the localization system in the LinkedIn Scraper.
This demonstrates how to switch between languages and use translations.
"""

import logging
from localization import i18n, Localization

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def demo_english():
    """Demonstrate the scraper with English localization"""
    # Set localization to English
    i18n.language = Localization.ENGLISH
    
    # Log some sample messages
    logger.info(i18n.get('script_start'))
    logger.info(i18n.get('config_info', 5, ['Software Engineer', 'Data Scientist'], 'Tokyo, Japan'))
    logger.info(i18n.get('search_jobs', ['Software Engineer', 'Data Scientist']))
    logger.info(i18n.get('analyzing_page', 1))
    logger.info(i18n.get('job_links_found', 25))
    
    # Example of analyzing a job
    logger.info(i18n.get('analyzing_job', 1, 25))
    logger.info(i18n.get('info_extracted', 'Software Engineer', 'Google', 'Tokyo'))
    
    # Example of gaijin-friendly analysis
    logger.info(i18n.get('gaijin_score', 20))
    logger.info(i18n.get('score_details', 5, 10, 5, 5, 5, -10))
    logger.info(i18n.get('gaijin_friendly'))
    
    logger.info(i18n.get('stats_summary', 25, 15))
    logger.info(i18n.get('script_end'))

def demo_french():
    """Demonstrate the scraper with French localization"""
    # Set localization to French
    i18n.language = Localization.FRENCH
    
    # Log the same sample messages, now in French
    logger.info(i18n.get('script_start'))
    logger.info(i18n.get('config_info', 5, ['Software Engineer', 'Data Scientist'], 'Tokyo, Japan'))
    logger.info(i18n.get('search_jobs', ['Software Engineer', 'Data Scientist']))
    logger.info(i18n.get('analyzing_page', 1))
    logger.info(i18n.get('job_links_found', 25))
    
    # Example of analyzing a job
    logger.info(i18n.get('analyzing_job', 1, 25))
    logger.info(i18n.get('info_extracted', 'Software Engineer', 'Google', 'Tokyo'))
    
    # Example of gaijin-friendly analysis
    logger.info(i18n.get('gaijin_score', 20))
    logger.info(i18n.get('score_details', 5, 10, 5, 5, 5, -10))
    logger.info(i18n.get('gaijin_friendly'))
    
    logger.info(i18n.get('stats_summary', 25, 15))
    logger.info(i18n.get('script_end'))

if __name__ == "__main__":
    print("=== English Demo ===")
    demo_english()
    
    print("\n=== French Demo ===")
    demo_french() 