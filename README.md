# suivinutrition

Système de suivi nutritionnel et d'entraînement piloté par la donnée, construit sur Notion.

L'objectif n'est pas de compter les calories. C'est de **rendre observables les modes de défaillance** d'une alimentation réelle — famille de quatre au dîner, produits de saison, jeûne intermittent, charge d'entraînement de coureur — pour que la correction devienne un réflexe et non une décision.


## Principes du modèle nutritionnel

- **Cible calorique générative** : `2100 + 63 × km courus`. Pas de table de correspondance.
- **Glucides en UG** (1 UG = 40 g de glucides). Les glucides se **placent**, ils ne se réduisent pas.
- **Protéines** : 130–135 g/jour, seuil de 30 g par prise pour déclencher la synthèse.
- **Lipides** : plafond 55–60 g/jour, 15 g par prise, **un seul véhicule lipidique par repas**. Les lipides sont le levier du déficit, pas l'ennemi — le vrai mode de défaillance, ce sont les lipides invisibles (huiles, sauces).
- **Protocole double canal** : la photo capture les solides, la déclaration verbale capture les liquides gras. Une photo seule ne détecte pas une cuillère d'huile.

## Architecture

Quatre bases Notion, chaînées par relations et rollups :

```
🍽️ Ingrédients / Recettes / Prises libres
        │  (relations n..n)
        ▼
   ⌚ Événement de prise alimentaire     ← 15 rollups Σ, 5 formules d'agrégation
        │  (relation n..1)
        ▼
   🌞 Jour                                ← rollups de totaux + écart à la cible
        │
        ▼
   🗞️ Journal                             ← narratif, contexte, ressenti
```

Deux pages de référence portent le modèle lui-même : **⚙️ Modèle Nutrition — noyau génératif** et **📐 Annexes de conversion**.

Le système est en usage quotidien. Le journal narratif n'est pas un accessoire : toute analyse doit s'appuyer sur ses entrées, c'est lui qui rend le modèle adaptable au contexte réel.

## Documentation

- [`docs/modele-donnees.md`](docs/modele-donnees.md) — exigences, cardinalités, unités de saisie, chaîne de calcul, contraintes techniques de l'API Notion, évolutions différées.

## Règles de travail

- **Tester avant d'optimiser** : valider dans une colonne `ZZ test` avant de toucher une colonne de production.
- **Chercher avant de créer** : interroger la base sur plusieurs formats de titre avant de créer une page. Absence dans la recherche ≠ absence en base.
- **Minimalisme de schéma** : ne conserver que les colonnes non dérivables. Préférer une structure générative à une table de correspondance.
- **Propagation ascendante** : corriger les prises, puis les événements, puis le jour.
- Les totaux du jour se lisent dans les rollups. Jamais par addition manuelle.

## Conventions

- Pages Jour : `AAMMJJ` (ex. `260827`)
- Pages Événement : `AAMMJJHHMM`
- Portions à la main : 🫴 = 1 UG (féculents) · ✊ = légume · 👍 ≈ 5 g de lipides · ✋ = protéines
- Types de jour : 🔵 repos · 🟢 footing · 🟡 qualité · 🔴 course / sortie longue

## Feuille de route

- [ ] Confirmer le pattern de recharge glycogénique observé le 26/08 sur les prochaines séances de qualité
- [ ] Migration vers une table de jonction `Ligne de prise` portant la quantité (voir §6 du modèle de données)
- [ ] Validation multi-utilisateurs sur un petit groupe test — après le 15 novembre
