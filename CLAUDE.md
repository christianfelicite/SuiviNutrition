# CLAUDE.md

Règles de travail dans ce dépôt.

## Nature du dépôt

Ce dépôt documente **la structure** d'un système de suivi nutritionnel et
d'entraînement. Il ne contient **aucune donnée** : ni prise alimentaire, ni
journal, ni mesure, ni identifiant d'instance. Les données vivent dans
l'instance de l'utilisateur.

Le dépôt est **public**. Tout ajout est publié.

## Séparation à respecter

| Fichier | Contient | Ne contient jamais |
|---|---|---|
| `docs/modele-domaine.md` | entités, invariants, chaîne de calcul | contraintes d'un support particulier |
| `docs/protocole-saisie.md` | méthode de saisie, unités, moments | schéma technique |
| `docs/adaptateur-notion.md` | mapping vers Notion, contournements | règles de domaine |
| `config/parametres-defaut.yaml` | seuils, cibles, conversions | logique |

Si une information hésite entre deux fichiers, c'est qu'elle est mal formulée.
La reformuler jusqu'à ce que sa place soit évidente.

## Interdits

- Aucun UUID, identifiant de collection, URL d'espace de travail, nom de fichier
  d'export ou donnée personnelle. Vérifier avant chaque commit.
- Aucune valeur numérique normative dans un `.md`. Elles vivent dans le YAML et
  sont référencées par nom de clé.
- Aucun `TODO` ni « à compléter » dans un document de référence. Ouvrir une issue.

## Méthode

- **Tester avant d'optimiser.** Valider sur une copie ou une branche avant de
  toucher un fichier de référence.
- **Chercher avant de créer.** Vérifier qu'un document ne couvre pas déjà le
  sujet. Absence dans la recherche ≠ absence dans le dépôt.
- **Minimalisme.** Ne conserver que ce qui n'est pas dérivable d'autre chose.
  Préférer une règle générative à une table de correspondance.
- **Propagation ascendante.** Corriger la source, puis les documents qui en
  dérivent, puis l'index.

## Style

Français. Direct, sans édulcoration. Ton professionnel, pas promotionnel.
Phrases courtes. Si un raisonnement est faux, le dire.
