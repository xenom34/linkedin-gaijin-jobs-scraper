import re

def modify_scraper_file():
    """Modifie le fichier linkedin_scraper.py pour exporter toutes les offres d'emploi."""
    try:
        print("Modification du scraper LinkedIn pour améliorer l'export...")
        
        # Lire le contenu du fichier
        with open('linkedin_scraper.py', 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Modifier la méthode scrape_jobs pour inclure toutes les offres (pas seulement gaijin-friendly)
        pattern_scrape_jobs = r"""                            # Analyser si l'offre est adaptée aux étrangers
                            is_gaijin_friendly, gaijin_details = self.is_gaijin_friendly\(description\)
                            
                            if is_gaijin_friendly:
                                logger.info\("✓ Offre adaptée aux étrangers trouvée!"\)
                                job_data = \{
                                    'title': title,
                                    'company': company,
                                    'location': location,
                                    'description': description\[:500\] \+ '\.\.\.' if len\(description\) > 500 else description,
                                    'url': job_url,
                                    'gaijin_score': gaijin_details\['score_total'\],
                                    'japanese_score': gaijin_details\['score_japonais'\],
                                    'international_score': gaijin_details\['score_international'\],
                                    'benefits_score': gaijin_details\['score_avantages'\],
                                    'leave_score': gaijin_details\['score_conges'\],
                                    'days_of_leave': gaijin_details\['jours_conges'\] if gaijin_details\['jours_conges'\] else 'Non spécifié',
                                    'additional_benefits': gaijin_details\['avantages'\]
                                \}
                                jobs.append\(job_data\)
                            else:
                                logger.info\("✗ Offre non adaptée aux étrangers"\)"""
        
        replacement_scrape_jobs = """                            # Analyser si l'offre est adaptée aux étrangers
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
                            jobs.append(job_data)"""
        
        content = re.sub(pattern_scrape_jobs, replacement_scrape_jobs, content)
        
        # Modifier la méthode save_to_csv pour mettre à jour le message de log
        pattern_log = r"logger.info\(f\"Scraping terminé. \{len\(jobs\)\} offres adaptées aux étrangers trouvées\"\)"
        replacement_log = "logger.info(f\"Scraping terminé. {len(jobs)} offres trouvées\")"
        content = re.sub(pattern_log, replacement_log, content)
        
        # Ajouter la méthode export_data
        pattern_close = r"    def close\(self\):"
        replacement_close = """    def export_data(self, jobs):
        \"\"\"Exporte les données dans tous les formats disponibles en utilisant l'exporteur dédié\"\"\"
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
    
    def close(self):"""
        
        content = re.sub(pattern_close, replacement_close, content)
        
        # Modifier la méthode main pour utiliser export_data
        pattern_main = r"""        jobs = scraper.scrape_jobs\(\)
        scraper.save_to_csv\(jobs\)
        logger.info\(f"\{len\(jobs\)\} offres adaptées aux étrangers ont été trouvées et sauvegardées dans gaijin_jobs.csv"\)"""
        
        replacement_main = """        jobs = scraper.scrape_jobs()
        
        # Utiliser le nouvel exporteur
        scraper.export_data(jobs)
        
        # Afficher les statistiques
        friendly_jobs = [job for job in jobs if job['is_gaijin_friendly'] == 'Oui']
        logger.info(f"Statistiques: {len(jobs)} offres au total, dont {len(friendly_jobs)} gaijin-friendly")"""
        
        content = re.sub(pattern_main, replacement_main, content)
        
        # Sauvegarder le fichier modifié
        with open('linkedin_scraper.py', 'w', encoding='utf-8') as file:
            file.write(content)
        
        print("Modification du scraper LinkedIn terminée avec succès!")
        return True
        
    except Exception as e:
        print(f"Erreur lors de la modification du scraper: {str(e)}")
        return False

if __name__ == "__main__":
    modify_scraper_file() 