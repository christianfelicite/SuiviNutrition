# Protocole de saisie

> Comment une consommation réelle devient une donnée. Portable : aucune
> dépendance à un support de stockage.

## 1. Principe du double canal

Un seul canal de capture produit un angle mort systématique. Deux canaux
complémentaires sont donc obligatoires.

| Canal | Capture | Angle mort |
|---|---|---|
| **Photographique** | solides, volumes, composition visible du plat | tout corps gras liquide |
| **Déclaratif** | huiles, sauces, matières grasses de cuisson, boissons | tout ce qui n'est pas verbalisé |

**Règle non négociable : une photo seule ne détecte pas une cuillère d'huile.**
Le canal déclaratif n'est pas un complément de confort, c'est la seule source
possible pour la classe d'apports qui constitue le principal mode de défaillance
du système.

Une prise saisie sans déclaration verbale est **incomplète par construction**,
même si la photo est nette et le plat identifiable.

## 2. Séquence de saisie

1. **Situer** — confirmer l'instant et le libellé de la prise avant toute autre
   opération. Une photo rattachée au mauvais moment est pire qu'une absence de
   photo : elle est fausse sans être détectable.
2. **Capturer** — photographier le solide avant consommation.
3. **Déclarer** — énoncer les matières grasses ajoutées, le mode de cuisson, les
   boissons.
4. **Quantifier** — traduire en unités de saisie (§3).
5. **Rattacher** — lier la prise au jour.

L'ordre compte. Situer en dernier conduit à des rattachements approximatifs.

## 3. Unités de saisie

### 3.1 Unité glucidique

Les glucides se saisissent en **UG**, unité de compte définie par
`glucides.grammes_par_ug`. Compter en unités plutôt qu'en grammes rend la saisie
possible sans balance, donc effectivement réalisée.

### 3.2 Portions à la main

La main est l'instrument de mesure : toujours disponible, proportionnée à son
porteur, utilisable au restaurant comme à table.

| Geste | Mesure |
|---|---|
| 🫴 main en coupe | féculents — une unité glucidique de référence |
| ✊ poing | légume non féculent |
| 👍 pouce | matière grasse — voir `portions.pouce_lipides_g` |
| ✋ paume | protéines |

**Règles d'usage**

- La main en coupe mesure le **volume total du plat**, pas chaque ingrédient
  séparément. Un plat mixte se mesure une fois.
- Les équivalences ne sont pas uniformes selon les aliments : les légumineuses
  ont un facteur de conversion propre, défini dans
  `portions.facteurs_conversion`.
- Les portions sont des **estimations assumées**. Leur intérêt est la constance,
  pas la justesse absolue. Une méthode approximative appliquée tous les jours
  détecte plus de dérives qu'une méthode exacte appliquée trois jours.

## 4. Types de jour

Le type de jour détermine les cibles et le protocole de placement.

| Code | Type |
|---|---|
| 🔵 | repos |
| 🟢 | footing |
| 🟡 | séance de qualité |
| 🔴 | course ou sortie longue |

## 5. Placement temporel

Les glucides se **placent**. Le placement est un paramètre de pilotage à part
entière, pas une conséquence.

- **Fenêtre de jeûne** — plage sans apport, appliquée selon le type de jour.
  Voir `jeune.*`. Levée sur les jours à charge élevée : la fenêtre ne doit jamais
  compromettre la disponibilité énergétique d'une sortie longue.
- **Charge pré-séance** — apport glucidique avant effort.
- **Recharge post-séance** — apport glucidique et protéique après effort.
- **Créneau de collation** — voir §6.

## 6. Modes de défaillance connus

Documentés parce qu'ils sont **récurrents et structurels**, non anecdotiques.
Les nommer est ce qui permet de les détecter tôt.

1. **Lipides invisibles.** Huiles, sauces, matières grasses de cuisson. Non
   capturables par photo. Contre-mesure : canal déclaratif obligatoire.
2. **Véhicules lipidiques concentrés.** Une liste courte et stable d'aliments
   produit l'essentiel des dépassements. Contre-mesure : un seul véhicule par
   prise.
3. **Doses protéiques sous le seuil.** Les protéines sont réparties en doses
   trop faibles pour déclencher la synthèse, alors que le total journalier est
   atteint. Contre-mesure : évaluer le seuil **par prise**, jamais par jour.
4. **Dissociation glucides/protéines.** Les deux macronutriments franchissent
   rarement leurs seuils respectifs dans la même occasion. Contre-mesure :
   contrôler la co-occurrence, pas seulement les totaux.
5. **Créneau de collation sauté.** Sauter la collation de fin d'après-midi
   produit une compensation en soirée, à l'heure la moins favorable. Contre-mesure :
   traiter ce créneau comme une prise planifiée, pas comme une option.

## 7. Contexte multi-convives

Le repas du soir est **partagé** et doit convenir à l'ensemble de la table, y
compris à des convives dont les besoins diffèrent de ceux du porteur du suivi
— notamment des adolescents et jeunes adultes en croissance ou en forte dépense.

Conséquences sur le modèle :

- Le plat commun n'est pas dimensionné sur les cibles du porteur du suivi. Ce
  sont **les portions individuelles** qui sont pilotées, pas la recette.
- Les seuils du système ne s'appliquent qu'à la ligne de saisie du porteur.
  Le système ne modélise pas les apports des autres convives et n'a pas vocation
  à le faire.
- Un plat commun ne doit jamais être restreint pour satisfaire une cible
  individuelle. La contrainte se résout par la portion, ou elle ne se résout pas.

## 8. Saisonnalité et approvisionnement

Préférence structurelle pour les fruits et légumes de saison et de production
locale. Ce n'est pas un critère nutritionnel : c'est un critère de sélection en
amont, qui contraint le référentiel `Aliment` sans intervenir dans la chaîne de
calcul.

Implication : le référentiel peut porter un marqueur de saisonnalité, exploité
en suggestion, jamais en contrainte de validation.
