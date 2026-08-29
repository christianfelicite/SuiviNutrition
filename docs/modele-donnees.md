# Modèle de données — SuiviNutrition

> Document de référence technique pour les quatre bases Notion et leur chaînage. Complète le modèle décrit dans `⚙️ Modèle Nutrition — noyau génératif` et `📐 Annexes de conversion`.

## 1. Vue d'ensemble

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

## 2. Exigences

_À compléter : exigences fonctionnelles et non fonctionnelles portées par le modèle._

## 3. Cardinalités

_À compléter : relations n..n et n..1 entre les quatre bases, contraintes d'intégrité._

## 4. Unités de saisie

_À compléter : UG (glucides), g (protéines/lipides), portions à la main (🫴 ✊ 👍 ✋)._

## 5. Chaîne de calcul

_À compléter : formules et rollups, de la prise alimentaire au totaux du jour._

## 6. Contraintes techniques de l'API Notion

_À compléter : limites de rollups, formules, relations, pagination._

## 7. Évolutions différées

- Migration vers une table de jonction `Ligne de prise` portant la quantité.
- Validation multi-utilisateurs sur un petit groupe test — après le 15 novembre 2026.
