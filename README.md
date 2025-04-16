# LinkedIn Gaijin Jobs Scraper

Un outil intelligent pour trouver des offres d'emploi adaptées aux étrangers ("gaijin-friendly") sur LinkedIn au Japon.

## 📋 Description

Ce projet permet de collecter automatiquement des offres d'emploi sur LinkedIn et d'analyser leur compatibilité avec les travailleurs étrangers au Japon. L'outil utilise une analyse avancée du texte pour détecter les offres qui ne nécessitent pas de compétences en japonais, offrent un support de visa, et proposent un environnement de travail international.

## ✨ Fonctionnalités

- **Scraping automatisé** des offres d'emploi sur LinkedIn
- **Analyse intelligente** pour évaluer si une offre est adaptée aux étrangers :
  - Détection des exigences linguistiques en japonais
  - Évaluation de l'environnement de travail international
  - Analyse des avantages pour expatriés (visa, logement, etc.)
  - Examen des politiques de congés
  - Détection de la langue utilisée dans l'offre
- **Génération de rapports** dans plusieurs formats :
  - Export CSV avec toutes les données
  - Export Excel formaté et filtrable
  - Rapport HTML interactif avec visualisations
- **Logging détaillé** pour le débogage et le suivi du processus

## 🔧 Installation

### Prérequis
- Python 3.8 ou supérieur
- Navigateur Firefox (utilisé par Selenium)

### Étapes d'installation

1. Clonez ce dépôt :
```bash
git clone https://github.com/votre-username/linkedin-gaijin-jobs-scraper.git
cd linkedin-gaijin-jobs-scraper
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Créez un fichier `.env` à la racine du projet avec vos identifiants LinkedIn :
```
LINKEDIN_EMAIL=votre_email@exemple.com
LINKEDIN_PASSWORD=votre_mot_de_passe
```

## 🚀 Utilisation

### Exécution du script principal

```bash
python linkedin_scraper.py
```

Le script va :
1. Se connecter à LinkedIn avec vos identifiants
2. Rechercher des offres d'emploi selon les critères configurés
3. Analyser chaque offre pour déterminer si elle est adaptée aux étrangers
4. Exporter les résultats dans différents formats

### Personnalisation de la recherche

Modifiez la fonction `main()` dans `linkedin_scraper.py` pour personnaliser votre recherche :

```python
def main():
    # ...
    keywords = ["Technical Consultant", "Software Consultant", "Professional Services"]
    scraper.search_jobs(keywords=keywords, location="Tokyo, Japan")
    # ...
```

## 📊 Résultats

Les résultats sont exportés dans le dossier `exports/` sous différents formats :

- **CSV** : Données brutes pour analyse
- **Excel** : Tableau formaté avec mise en forme conditionnelle
- **HTML** : Rapport interactif avec graphiques et filtres

Chaque offre contient les informations suivantes :
- Titre du poste
- Entreprise
- Localisation
- URL de l'offre
- Score de compatibilité "gaijin-friendly"
- Scores détaillés par catégorie
- Jours de congés détectés
- Avantages pour expatriés

## 🧩 Structure du projet

- `linkedin_scraper.py` : Script principal pour le scraping et l'analyse
- `linkedin_export.py` : Module pour l'export des données dans différents formats
- `requirements.txt` : Liste des dépendances
- `exports/` : Dossier contenant les fichiers exportés

## ⚙️ Comment ça fonctionne

L'analyse des offres d'emploi est basée sur un système de scoring multicritère :

1. **Analyse des exigences linguistiques en japonais** (détecte les mentions de JLPT, "native level", etc.)
2. **Évaluation de l'environnement international** (mentions d'équipe internationale, langue de travail, etc.)
3. **Analyse des avantages pour expatriés** (visa, logement, etc.)
4. **Examen des politiques de congés** (jours de congés, flexibilité, etc.)
5. **Détection de la langue** utilisée dans l'offre (une offre en anglais est généralement plus adaptée)

Chaque critère contribue à un score global qui détermine si l'offre est "gaijin-friendly".

## 🛡️ Avertissement légal

Ce projet est conçu à des fins éducatives et personnelles uniquement. L'utilisation de ce script doit respecter les conditions d'utilisation de LinkedIn. Une utilisation excessive peut entraîner des limitations de votre compte LinkedIn. Utilisez de manière responsable en respectant des délais raisonnables entre les requêtes.

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou soumettre une pull request.

1. Forkez le projet
2. Créez votre branche de fonctionnalité (`git checkout -b feature/amazing-feature`)
3. Committez vos changements (`git commit -m 'Add some amazing feature'`)
4. Poussez vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrez une Pull Request 