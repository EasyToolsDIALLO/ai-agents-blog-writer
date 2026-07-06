# Google ADK Blogger Agent

Application multi-agent basée sur **Google Agent Development Kit (ADK)** pour planifier et rédiger des articles de blog automatiquement.

## Stack technique

- **Python** : 3.14
- **Google ADK** : 2.3.0
- **Google GenAI** : 2.10.0

## Prérequis

- Python 3.14 installé
- Un compte [Groq](https://console.groq.com) avec une clé API
- Une clé API Google (Gemini / Vertex AI) si nécessaire pour les agents Google

## Prise en main

### 1. Cloner le projet

```bash
git clone <url-du-repo>
cd ai-agents-blog-writer
```

### 2. Créer et activer un environnement virtuel

**Windows (PowerShell)** :

```powershell
python -m venv venv314
.\venv314\Scripts\Activate.ps1
```

**Windows (CMD)** :

```cmd
python -m venv venv314
venv314\Scripts\activate.bat
```

**macOS / Linux** :

```bash
python3 -m venv venv314
source venv314/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Créer une clé API Groq

1. Rendez-vous sur [https://console.groq.com/keys](https://console.groq.com/keys)
2. Connectez-vous ou créez un compte
3. Générez une nouvelle clé API
4. Copiez la clé dans le presse-papiers

### 5. Configurer les variables d'environnement

Le projet utilise un fichier `.env` pour stocker les clés API. Un modèle est fourni via `.env.example`.

**Copiez le fichier d'exemple** :

```bash
cp .env.example .env
```

**Windows (PowerShell)** :

```powershell
copy .env.example .env
```

**Windows (CMD)** :

```cmd
copy .env.example .env
```

Ouvrez ensuite le fichier `.env` et remplacez les valeurs par vos clés :

```env
GOOGLE_API_KEY=AQ.votre_cle_google
GROQ_API_KEY=votre_cle_groq
```

### 6. Lancer l'application

```bash
adk web
```

L'interface web sera accessible dans votre navigateur à l'adresse indiquée dans le terminal (généralement `http://localhost:8000` ou `http://127.0.0.1:8000`).

## Structure du projet

```
ai-agents-blog-writer/
├── agent.py              # Point d'entrée de l'agent ADK
├── blogPlannerAgent.py   # Agent de planification de contenu
├── blogWriterAgent.py    # Agent de rédaction d'articles
├── requirements.txt      # Dépendances Python
├── .env.example        # Modèle de configuration des clés API
└── .env                # Configuration locale (non versionnée)
```

## Bonnes pratiques

- Ne jamais commiter le fichier `.env` : il est déjà ignoré par `.gitignore`.
- Vérifiez que votre environnement virtuel est activé avant chaque session de développement.
- Pour ajouter une nouvelle dépendance, mettez à jour `requirements.txt` et réinstallez avec `pip install -r requirements.txt`.

## Dépannage

- **Erreur `ModuleNotFoundError` :** assurez-vous que l'environnement virtuel est activé et que `requirements.txt` a bien été installé.
- **Erreur de clé API :** vérifiez que les variables `GOOGLE_API_KEY` et `GROQ_API_KEY` sont bien renseignées dans `.env`.
- **Port déjà utilisé :** lancez `adk web` avec une option de port différent si nécessaire (consultez `adk web --help`).
