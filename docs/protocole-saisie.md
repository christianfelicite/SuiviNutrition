# Protocole de saisie

> Comment une consommation réelle devient une donnée. Portable : aucune
> dépendance à un support de stockage. Les entités citées sont définies dans
> [`modele-domaine.md`](modele-domaine.md).

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

Un événement saisi sans déclaration verbale est **incomplet par construction**,
même si la photo est nette et le plat identifiable.

## 2. Séquence de saisie

1. **Situer** — confirmer l'instant et le libellé de l'événement avant toute
   autre opération. Une photo rattachée au mauvais moment est pire qu'une absence
   de photo : elle est fausse sans être détectable.
2. **Capturer** — photographier le solide avant consommation.
3. **Déclarer** — énoncer les matières grasses ajoutées, le mode de cuisson, les
   boissons.
4. **Aiguiller** — pour chaque apport, choisir son canal de composition (§3).
5. **Quantifier** — traduire en unités de saisie (§4).
6. **Rattacher** — lier les composants à l'événement, l'événement au jour.

L'ordre compte. Situer en dernier conduit à des rattachements approximatifs.

## 3. Aiguillage des canaux de composition

Un événement se compose de trois natures d'apport. Le choix se fait à la saisie
et n'a **aucun effet sur le calcul** : les trois s'additionnent de la même façon.
Il n'engage que la réutilisabilité de la ligne.

| Apport | Canal | Condition |
|---|---|---|
| aliment atomique, consommé à sa portion de référence | `Ingrédient` | composition déjà définie ou définissable une fois pour toutes |
| préparation composée, répétable | `Recette` | composition saisie pour une part d'une personne |
| tout le reste | `PriseLibre` | quantité variable, plat composé non répétable, apport ponctuel |

**Critère unique : la répétabilité.** Les canaux `Ingrédient` et `Recette`
servent aux apports stables — le pot de skyr, la banane, le bol de flocons.
Dès que la quantité consommée s'écarte de la portion de référence, l'apport
passe en `PriseLibre` avec sa valeur réelle.

**Interdits de saisie**

- Créer une variante de quantité dans le référentiel — une ligne « riz ×2 » ou
  une duplication sous un autre nom. Cela dédouble le référentiel et rend
  inexploitable toute statistique de fréquence d'usage. Le cas se traite en
  `PriseLibre`.
- Modifier la composition d'un ingrédient ou d'une recette pour refléter une
  consommation particulière. Le référentiel décrit une définition, pas un repas.

## 4. Unités de saisie

### 4.1 Convention de portion

**Toute composition est saisie pour une personne.** Un ingrédient porte les
valeurs d'une portion d'une personne, jamais d'une masse normalisée. Une recette
porte les valeurs d'une part : une préparation familiale est divisée par le
nombre de parts avant saisie.

Sans portion de référence explicite, une ligne de référentiel ne veut rien dire.

### 4.2 Unité glucidique

Les glucides se saisissent en **UG**, unité de compte définie par
`glucides.grammes_par_ug`. Compter en unités plutôt qu'en grammes rend la saisie
possible sans balance, donc effectivement réalisée.

### 4.3 Portions à la main

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
  séparément. Un plat mixte se mesure une fois — et se saisit donc en
  `PriseLibre`, pas en somme d'ingrédients.
- Les équivalences ne sont pas uniformes selon les aliments : les légumineuses
  ont un facteur de conversion propre, défini dans
  `portions.facteurs_conversion`.
- Les portions sont des **estimations assumées**. Leur intérêt est la constance,
  pas la justesse absolue. Une méthode approximative appliquée tous les jours
  détecte plus de dérives qu'une méthode exacte appliquée trois jours.

## 5. Types de jour

Le type de jour détermine les cibles et le protocole de placement.

| Code | Type |
|---|---|
| 🔵 | repos |
| 🟢 | footing |
| 🟡 | séance de qualité |
| 🔴 | course ou sortie longue |

## 6. Placement temporel

Les glucides se **placent**. Le placement est un paramètre de pilotage à part
entière, pas une conséquence.

- **Fenêtre de jeûne** — plage sans apport, appliquée selon le type de jour.
  Voir `jeune.*`. Levée sur les jours à charge élevée : la fenêtre ne doit jamais
  compromettre la disponibilité énergétique d'une sortie longue.
- **Charge pré-séance** — apport glucidique avant effort.
- **Recharge post-séance** — apport glucidique et protéique après effort.
- **Créneau de collation** — voir §7.

Le placement est une décision de saisie autant que de nutrition : c'est le
découpage en événements qui rend le placement observable. Un apport fusionné
dans l'événement voisin devient invisible au contrôle de seuils.

## 7. Modes de défaillance connus

Documentés parce qu'ils sont **récurrents et structurels**, non anecdotiques.
Les nommer est ce qui permet de les détecter tôt.

1. **Lipides invisibles.** Huiles, sauces, matières grasses de cuisson. Non
   capturables par photo. Contre-mesure : canal déclaratif obligatoire.
2. **Véhicules lipidiques concentrés.** Une liste courte et stable d'aliments
   produit l'essentiel des dépassements. Contre-mesure : un seul véhicule par
   événement.
3. **Doses protéiques sous le seuil.** Les protéines sont réparties en doses
   trop faibles pour déclencher la synthèse, alors que le total journalier est
   atteint. Contre-mesure : évaluer le seuil **par événement**, jamais par jour.
4. **Dissociation glucides/protéines.** Les deux macronutriments franchissent
   rarement leurs seuils respectifs dans la même occasion. Contre-mesure :
   contrôler la co-occurrence, pas seulement les totaux.
5. **Créneau de collation sauté.** Sauter la collation de fin d'après-midi
   produit une compensation en soirée, à l'heure la moins favorable.
   Contre-mesure : traiter ce créneau comme un événement planifié, pas comme une
   option.
6. **Dérive du référentiel.** Le référentiel se peuple de variantes de quantité
   et de doublons de commodité, jusqu'à ce que la fréquence d'usage d'un aliment
   ne soit plus mesurable. Contre-mesure : les interdits de saisie du §3, et le
   recours systématique à la `PriseLibre` pour l'exceptionnel.

## 8. Contexte multi-convives

Le repas du soir est **partagé** et doit convenir à l'ensemble de la table, y
compris à des convives dont les besoins diffèrent de ceux du porteur du suivi
— notamment des adolescents et jeunes adultes en croissance ou en forte dépense.

Conséquences sur la saisie :

- Le plat commun n'est pas dimensionné sur les cibles du porteur du suivi. Ce
  sont **les portions individuelles** qui sont pilotées, pas la recette.
- Une recette est saisie **pour une part**. Le passage du plat commun à la part
  est une division faite à la saisie, jamais un calcul du système.
- Les seuils ne s'appliquent qu'aux composants rattachés aux événements du
  porteur. Le système ne modélise pas les apports des autres convives et n'a pas
  vocation à le faire.
- Un plat commun ne doit jamais être restreint pour satisfaire une cible
  individuelle. La contrainte se résout par la portion, ou elle ne se résout pas.

## 9. Saisonnalité et approvisionnement

Préférence structurelle pour les fruits et légumes de saison et de production
locale. Ce n'est pas un critère nutritionnel : c'est un critère de sélection en
amont, qui contraint les référentiels `Ingrédient` et `Recette` sans intervenir
dans la chaîne de calcul.

Implication : une ligne de référentiel peut porter un marqueur de saisonnalité,
exploité en suggestion, jamais en contrainte de validation.
