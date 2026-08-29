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
| `Aliment` | base des contenus | **fusionnée avec `LignePrise`** — voir §5 |
| `LignePrise` | *absente* | quantité portée par l'enregistrement de contenu |
| `Prise` | base des événements | conforme |
| `Jour` | base des jours | conforme |
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

C'est l'écart le plus coûteux entre la spécification et l'implémentation de
référence.

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

## 5. Dette identifiée : table de jonction

L'instance actuelle fusionne `Aliment` et `LignePrise`. Conséquence : la
composition d'un aliment est ressaisie à chaque consommation, ce qui rend
impossible toute correction rétroactive d'une valeur de composition.

**Cible :** table `Aliment` en référentiel, table de jonction `LignePrise`
portant la quantité.

**Statut :** différée. Motif : coût de migration des données existantes pendant
une période de suivi actif — pas un doute sur le design.

**Conséquence pour une nouvelle instance :** implémenter directement la
jonction. Ne pas reproduire ce compromis.

## 6. Feuille de route

- [ ] Migration vers la table de jonction (§5)
- [ ] Externalisation des seuils hors des formules (§2.8)
- [ ] Validation multi-utilisateurs sur un groupe test restreint
