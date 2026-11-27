# Adaptateur Notion

> Implémentation de référence du modèle décrit dans
> [`modele-domaine.md`](modele-domaine.md). **Tout ce qui figure ici est
> contingent** : il s'agit de contournements de limites propres à Notion. Une
> autre implémentation n'a aucune raison de les reproduire.
>
> Ce document existe pour deux raisons : permettre de reconstruire l'instance
> Notion, et permettre à un implémenteur sur un autre support d'identifier
> immédiatement ce qu'il peut ignorer.

## 1. Correspondance des entités

| Entité de domaine | Réalisation Notion | Écart |
|---|---|---|
| `Ingredient` | base des aliments, en référentiel | conforme |
| `Recette` | base des recettes | composition saisie — §6, écart 7 |
| `ComposantRecette` | *absente* | une base de compositions de référence fait foi pour les macros d'une recette, sans quantité par ingrédient — §6, écart 7 |
| `LignePrise` | base des prises alimentaires | jonction réalisée — voir §5 ; exclusivité des sources non contrainte — §6, écart 5 |
| `Prise` | base des événements | conforme |
| `Seance` | base des entraînements | la séance planifiée porte aussi le type de jour |
| `TypeDeJour` | attribut de la séance planifiée | pas de base dédiée |
| `Jour` | base des jours | cible recalculée localement — §6, écart 1 |
| `Semaine` | base des semaines | — |
| `Cible` | base des cibles du modèle | lue par `Jour` |
| `EntreeJournal` | base du journal | conforme |

## 2. Contournements structurels

### 2.1 Titres porteurs de la date

Notion n'offre pas de clé primaire typée exploitable en formule. La date est
donc encodée dans le titre de la page, en format compact :

- pages `Jour` : `AAMMJJ`
- pages `Prise` : `AAMMJJHHMM`

Reconstruction d'une date depuis un titre : découper la chaîne par positions
fixes et recomposer une date ISO avant analyse. Le décalage saisonnier doit être
calculé explicitement, aucune fonction native ne le fournit de façon fiable dans
ce contexte.

> **Un autre support n'a pas besoin de ceci.** Un champ date typé rend
> l'ensemble de cette section sans objet.

### 2.2 Agrégation par rollups

Notion n'a pas de couche de calcul. L'agrégation d'un niveau vers le suivant est
réalisée par une quinzaine de colonnes de sommation et quelques formules
d'agrégation, maintenues manuellement.

### 2.3 Traversée de relations limitée à un saut

Il n'est pas possible, via l'API, de traverser deux relations successives
(contenu → événement → jour).

**Contournement :** calculer dans la table de base, exposer le résultat dans la
table intermédiaire par une colonne de sommation, puis consommer cette colonne
au niveau supérieur.

### 2.4 Lecture du titre d'une page liée

Dans une formule, le formatage direct de la propriété de relation est fiable ;
l'accès à la propriété de la page liée à l'intérieur d'une itération ne l'est
pas. Utiliser la première forme.

### 2.5 Rollups non utilisables comme axe

Une colonne de sommation ne peut pas servir d'axe à une vue calendrier. Passer
par une formule intermédiaire.

### 2.6 Parenthèses dans les chaînes de formule

Dans une définition de schéma, les parenthèses à l'intérieur d'une chaîne de
formule sont interprétées comme du code. Utiliser un séparateur neutre — `/`
par exemple — dans les libellés.

### 2.7 Absence de suppression programmatique

L'API ne permet pas la mise à la corbeille. Neutralisation par renommage avec un
préfixe d'alerte explicite, suppression manuelle ensuite.

### 2.8 Seuils codés en dur

Les valeurs de seuil sont actuellement écrites en clair dans les formules. Toute
modification de `config/parametres-defaut.yaml` doit être **répercutée
manuellement** dans les formules concernées. Il n'existe pas de mécanisme de
propagation.

## 3. Règles opératoires

- **Chercher avant de créer.** Interroger la base sur plusieurs formats de titre
  avant de créer une page. Absence dans la recherche ≠ absence en base.
- **Tester avant d'optimiser.** Valider dans une colonne de test dédiée avant de
  modifier une colonne de production.
- **Lire les totaux dans les rollups.** Jamais par addition des éléments connus :
  les éléments non interrogés seraient silencieusement omis.
- **Ne modifier le schéma que sur demande explicite.** Une modification de schéma
  non demandée casse les vues et les formules dépendantes sans avertissement.
- **Propagation ascendante.** Contenu, puis événement, puis jour.

## 4. Ce qui ne figure pas ici

Les identifiants de bases, d'espace de travail et de pages sont des **données
d'instance**. Ils ne doivent jamais être versionnés : ce dépôt est public, et ces
identifiants n'ont aucune valeur pour une autre instanciation.

Une instance se reconstruit à partir de ce document ; elle ne se clone pas.

## 5. Jonction `LignePrise`

La base des prises alimentaires réalise la jonction : chaque enregistrement
référence un ingrédient ou une recette du référentiel, porte la quantité
consommée, et calcule ses valeurs à partir de la composition de la source.

Elle conserve aussi des champs de composition saisis directement, hérités de
l'époque où contenu et quantité étaient fusionnés.

**Conséquence pour une nouvelle instance :** implémenter la jonction sans ces
champs. Une composition saisie relève de `PriseLibre`, pas de `LignePrise`.

## 6. Écarts avec le modèle de domaine

Ce que l'instance de référence ne réalise pas encore comme le prévoit
[`modele-domaine.md`](modele-domaine.md). Un écart se documente ici ; sa
résorption se suit dans une issue.

| # | Écart | Conséquence | Suivi |
|---|---|---|---|
| 1 | La cible est recalculée localement au niveau `Jour` en plus d'être lue dans `Cible` (domaine §4.11). | Deux chemins de calcul coexistent et peuvent diverger. | issue #6 |
| 2 | Les seuils sont codés en dur dans les formules d'évaluation. | Voir §2.8. | issue #2 |
| 3 | `vehicule_lipidique` n'est pas renseigné sur l'ensemble du référentiel. | `nb_vehicules_lipidiques` sous-compte **sans le signaler**. | issue #7 |
| 4 | `mode`, `cible` et `axe_hydrique` ne sont pas renseignés sur les jours antérieurs à leur création. | Agrégats incomplets sur la période de bascule. | issue #8 |
| 5 | L'exclusivité des trois canaux (domaine §3.4) n'est pas contrainte. | Une ligne peut référencer deux sources. | issue #9 |
| 6 | `Jour.distance_courue` est saisie alors que le modèle la dérive de `Seance`. | Elle doit **rester saisie** tant que `Seance` n'est pas peuplée. Bascule en une fois, jamais en double. | issue #10 |
| 7 | `ComposantRecette` n'existe pas en tant que jonction ; `Recette` porte une composition saisie au lieu d'être dérivée (domaine §4.3, §4.4). | Une correction d'ingrédient ne se propage pas aux recettes. | issue #11 |
| 8 | `frequence_cardiaque_moyenne` n'a pas d'historique. | Le signal d'arrêt n°2 reste indisponible tant que `pilotage.fenetre_tendance` semaines ne sont pas accumulées. | Délai, pas défaut : aucune action. |
