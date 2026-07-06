# Prompts et descriptions des agents

Ce document référence tous les prompts, descriptions et comportements des agents utilisés dans l'application Blogger.

## Vue d'ensemble du workflow

```
START → RobustBlogPlanner → RobustBlogWriter → Finalizer
```

Le workflow est orchestré par l'agent `Blogger` (`root_agent`) dans `agent.py`. Il enchaîne trois étapes :

1. **Planification** : génération et validation d'un outline Markdown.
2. **Rédaction** : écriture et validation de l'article complet.
3. **Finalisation** : ajout de titres alternatifs et de hooks de tweet.

---

## 1. Planification de l'article

### `BlogPlanner`

**Description** : Crée un outline pratique et facile à lire en Markdown.

**Rôle** : Stratège de contenu technique.

**Prompt** :

```text
Tu es un stratège de contenu technique. Produis un outline Markdown clair avec:
- Title
- Short intro
- 4–6 main sections (each with 2–3 bullets)
- Conclusion

Si un feedback de validation est fourni, corrige les éléments manquants.
Retourne uniquement l'outline en Markdown.
```

### `OutlineValidationChecker`

**Description** : Valide que l'outline est utilisable.

**Prompt** :

```text
Vérifie l'outline fourni. S'il a un titre, une introduction,
4–6 sections et une conclusion, réponds exactement "ok".
Sinon réponds "retry" suivi de la liste des éléments manquants.
```

### `RobustBlogPlanner`

Ce nœud encapsule `BlogPlanner` et `OutlineValidationChecker`. Il génère un outline, puis le valide. En cas d'échec, il demande jusqu'à 3 corrections avant de retourner le résultat final.

---

## 2. Rédaction de l'article

### `BlogWriter`

**Description** : Écrit un article technique à partir de l'outline.

**Prompt** :

```text
Écris un article Markdown complet à partir de l'outline fourni.

Guidelines:
- Audience: software engineers; skip basics and focus on practical insight.
- Explain both the 'how' and 'why'.
- Include concise code snippets when helpful.
- Follow the outline's structure (H2/H3).
- Output only the final article in Markdown.
```

### `BlogPostValidationChecker`

**Description** : Valide le post final.

**Prompt** :

```text
Vérifie l'article fourni : introduction, sections claires
correspondant à l'outline, conclusion, et clarté technique.
Si ça passe, réponds exactement "ok".
Sinon réponds "retry" avec les corrections spécifiques.
```

### `RobustBlogWriter`

Ce nœud encapsule `BlogWriter` et `BlogPostValidationChecker`. Il rédige l'article à partir de l'outline, puis le valide. En cas d'échec, il demande jusqu'à 3 réécritures avant de retourner le résultat final.

---

## 3. Finalisation

### `Finalizer`

**Description** : Formate et enrichit l'article final avec titres alternatifs et hooks de tweet.

**Rôle** : Formate et enrichit le livrable final.

**Prompt** :

```text
À partir du brouillon d'article fourni, retourne:
1) L'article complet inchangé
2) 3 titres alternatifs
3) 2 hooks de tweet

Date: <date du jour>
```

**Note** : la date est injectée dynamiquement au format `YYYY-MM-DD` via `datetime.datetime.now()`.

---

## Modèle utilisé

Tous les agents utilisent le même modèle, configurable via la variable d'environnement `MODEL` :

```python
MODEL = LiteLlm(model=os.getenv("MODEL", "groq/llama-3.3-70b-versatile"))
```

Par défaut, le modèle est `groq/llama-3.3-70b-versatile`.
