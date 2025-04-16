# Guide de contribution

Merci de considérer la contribution au projet LinkedIn Gaijin Jobs Scraper ! Ce document vous guidera à travers le processus de contribution.

## Comment contribuer

### Signaler des bugs

Si vous trouvez un bug, veuillez ouvrir une issue en fournissant :

1. Une description claire du bug
2. Les étapes pour reproduire le problème
3. Le comportement attendu
4. Des captures d'écran si possible
5. Votre environnement (OS, version de Python, etc.)

### Suggérer des améliorations

Les suggestions d'amélioration sont toujours les bienvenues. Pour en proposer :

1. Ouvrez une issue avec le tag "enhancement"
2. Décrivez clairement la fonctionnalité souhaitée
3. Expliquez pourquoi cette fonctionnalité serait utile pour le projet

### Soumettre des modifications

Pour soumettre des modifications au code :

1. Forkez le dépôt
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/amazing-feature`)
3. Committez vos changements (`git commit -m 'Add some amazing feature'`)
4. Poussez vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrez une Pull Request

### Style de code

Veuillez suivre ces conventions de style pour assurer la cohérence du code :

- Suivez les conventions PEP 8 pour Python
- Utilisez des noms de variables et de fonctions explicites
- Commentez votre code de manière claire et concise
- Ajoutez des docstrings pour les fonctions et les classes
- Gardez les lignes à moins de 100 caractères

## Processus de développement

### Environnement de développement

Pour configurer votre environnement de développement :

```bash
# Cloner le dépôt
git clone https://github.com/votre-username/linkedin-gaijin-jobs-scraper.git
cd linkedin-gaijin-jobs-scraper

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer le fichier .env pour les tests
cp .env.example .env
# Modifiez .env avec vos identifiants
```

### Tests

Avant de soumettre une pull request, assurez-vous que votre code passe tous les tests :

```bash
python test_export.py
```

### Documentation

Si vous ajoutez de nouvelles fonctionnalités, n'oubliez pas de mettre à jour la documentation :

- Mettez à jour le README.md si nécessaire
- Ajoutez des docstrings pour les nouvelles fonctions ou classes
- Documentez les paramètres et valeurs de retour

## Reconnaissance des contributions

Tous les contributeurs seront ajoutés à une section "Contributeurs" dans le README. Nous apprécions tous les types de contributions, qu'il s'agisse de code, de documentation, de design ou d'idées !

## Code de conduite

En participant à ce projet, vous vous engagez à maintenir un environnement respectueux et inclusif. Soyez respectueux envers les autres contributeurs et utilisateurs. Tout comportement inapproprié ne sera pas toléré. 