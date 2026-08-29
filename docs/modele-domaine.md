# Modèle de domaine

> Description portable du système. Rien dans ce document ne dépend d'un support
> de stockage particulier. Les paramètres numériques sont nommés ici et définis
> dans [`config/parametres-defaut.yaml`](../config/parametres-defaut.yaml).

## 1. Objet du système

Le système ne compte pas les calories. Il rend **observables les modes de
défaillance** d'une alimentation réelle, pour que la correction devienne un
réflexe plutôt qu'une décision.

Un mode de défaillance est un écart récurrent, structurel, invisible à
l'introspection. Exemples caractéristiques : lipides invisibles apportés par des
véhicules liquides, doses protéiques systématiquement sous le seuil de synthèse,
créneau de collation systématiquement sauté entraînant une compensation tardive.

Le système est donc d'abord un **instrument de détection**, ensuite un instrument
de pilotage.

## 2. Entités

Trois entités portent une composition nutritionnelle — `Ingrédient`, `Recette`,
`PriseLibre`. Elles se distinguent par leur **mode de définition**, pas par leur
usage : un `Événement` les traite indifféremment.

Les cinq attributs de composition sont, partout, les mêmes et tous additifs :
énergie, protéines, lipides, glucides en masse, glucides en unité de compte.

### 2.1 `Ingrédient`

Référentiel d'aliments atomiques.

- Identité stable, indépendante de toute consommation.
- Composition exprimée **pour une portion d'une personne**, jamais pour une masse
  normalisée. La portion de référence est une propriété obligatoire : sans elle,
  la ligne ne veut rien dire.
- Peut porter des marqueurs qualitatifs : véhicule lipidique, saisonnalité,
  origine.
- N'est jamais dupliqué par consommation, ni décliné en variantes de quantité.
  Dupliquer une ligne pour exprimer une quantité différente détruit le
  référentiel et rend inexploitable toute statistique de fréquence d'usage.

### 2.2 `Recette`

Préparation composée, définie une fois et réutilisée.

- Composition exprimée **pour une part d'une personne**. Une préparation
  familiale est divisée par le nombre de parts avant saisie.
- Sa relation vers les ingrédients qui la composent est **documentaire, pas
  calculatoire** : sa composition est saisie, pas dérivée. Toute modification
  d'une recette impose de recalculer ses valeurs ; rien ne le rappellera.
- Même règle de non-duplication que l'ingrédient.

### 2.3 `PriseLibre`

Apport ponctuel, sans définition préalable.

- Porte sa composition directement. Elle ne référence rien.
- C'est le canal des quantités variables et des plats composés non répétables.

**Règle d'aiguillage.** Les canaux `Ingrédient` et `Recette` servent aux apports
**stables et répétables**, consommés à leur portion de référence. Dès que la
quantité consommée s'écarte de cette portion, l'apport passe en `PriseLibre`,
avec sa valeur réelle.

### 2.4 `Événement`

Prise alimentaire située dans le temps. **Entité composite.**

- Porte un instant et un libellé.
- Contient `0..n` ingrédients, `0..n` recettes, `0..n` prises libres.
- **N'a pas de composition propre.** La sienne est la somme de ses composants,
  quelle que soit leur nature.
- Porte les franchissements de seuils qui s'évaluent à son niveau (§6).
- Appartient à un `Jour`.

### 2.5 `Jour`

Unité de bilan.

- Porte une date, un type de jour et une charge d'entraînement.
- Agrège les `Événement` de la journée.
- Porte les cibles calculées et l'écart signé à ces cibles.

### 2.6 `EntreeJournal`

Narratif : contexte, ressenti, événement de vie, écart assumé.

Le journal n'est pas un accessoire. Les valeurs chiffrées disent *quoi*, le
journal dit *pourquoi*. **Toute analyse du système doit s'appuyer sur les
entrées du journal** ; une analyse purement quantitative produit des
recommandations inapplicables au contexte réel.

## 3. Cardinalités

```
Ingrédient   0..n ──── 0..n ┐
Recette      0..n ──── 0..n ├── Événement ──n..1── Jour ──1..n── EntreeJournal
PriseLibre   0..n ──── 0..n ┘
```

- `Ingrédient` → `Événement` : n..n.
- `Recette` → `Événement` : n..n.
- `PriseLibre` → `Événement` : n..n.
- `Événement` → `Jour` : n..1. Un événement appartient à un seul jour.
- `Jour` → `EntreeJournal` : 1..n.

**Invariant explicite.** Un ingrédient, une recette ou une prise libre rattaché à
**plusieurs événements** est un choix de conception, pas une anomalie
d'intégrité. Le cas se produit légitimement lorsqu'un même apport est consommé à
deux occasions distinctes, ou qu'une préparation chevauche deux jours. Toute
implémentation doit l'autoriser, et aucun contrôle de cohérence ne doit le
signaler comme erreur.

> **Note d'implémentation.** L'implémentation de référence ne permet pas de
> rattacher deux fois le même enregistrement au même événement. Ce cas se traite
> par une `PriseLibre` portant la valeur réellement consommée — ce qui est de
> toute façon la règle d'aiguillage de §2.3. Écart documenté dans
> [`adaptateur-notion.md`](adaptateur-notion.md).

## 4. Chaîne de calcul

Le calcul est **ascendant et strictement ordonné**. Chaque niveau agrège le
niveau inférieur ; aucun niveau ne recalcule ce qu'un autre a déjà agrégé.

```
Ingrédient ─┐
Recette     ├─ Σ ─→  Événement  ─ Σ ─→  Jour
PriseLibre ─┘        totaux              totaux
                     + seuils            + cibles
                                         + écart signé
```

Pour chacun des cinq attributs :

```
Événement.attribut = Σ ingrédients + Σ recettes + Σ prises libres
Jour.attribut      = Σ événements
```

**L'addition est homogène.** Elle ne distingue pas la nature du composant. La
séparation en trois canaux est une distinction de définition, pas de calcul :
elle disparaît au premier niveau d'agrégation.

**Règle de lecture.** Les totaux d'un niveau se lisent dans l'agrégat de ce
niveau. Jamais par addition manuelle des éléments connus : les éléments non
interrogés seraient silencieusement omis, et l'erreur serait indétectable.

**Règle de correction.** Corriger dans l'ordre : composant, puis événement, puis
jour. Corriger un total sans corriger sa source crée une divergence qui ne se
signale pas.

## 5. Cibles

Les cibles sont **génératives** : calculées par formule à partir de la charge du
jour. Aucune table de correspondance jour-par-jour.

| Cible | Détermination | Clés de configuration |
|---|---|---|
| Énergie | base + coefficient × distance courue | `energie.base`, `energie.coefficient_par_km` |
| Protéines | plage journalière fixe | `proteines.cible_journaliere` |
| Lipides | plafond journalier fixe | `lipides.plafond_journalier` |
| Glucides | échelonnés sur la distance courue | `glucides.*` |

L'écart à la cible est exprimé **signé et en pourcentage**, par macronutriment.
Un écart non signé masque la direction de la dérive, qui est l'information utile.

## 6. Seuils

Les seuils s'évaluent **au niveau de l'événement**, pas du jour. C'est le point
structurant : un total journalier conforme peut masquer une répartition
inopérante.

| Seuil | Nature | Clé |
|---|---|---|
| Synthèse protéique | plancher — en deçà, l'apport ne déclenche pas la synthèse | `proteines.seuil_synthese_par_prise` |
| Plafond lipidique | plafond par événement | `lipides.plafond_par_prise` |
| Véhicule lipidique | un seul véhicule autorisé par événement | `lipides.seuil_vehicule`, `lipides.vehicules_max_par_prise` |

Un franchissement de seuil est **signalé, pas bloqué**. Le système décrit le
réel ; il ne le contraint pas.

## 7. Principes de conception

- **Génératif plutôt que tabulaire.** Une formule paramétrée plutôt qu'une table
  de correspondance. Une table se périme et diverge ; une formule se corrige en
  un point.
- **Minimalisme de schéma.** Ne conserver que ce qui n'est pas dérivable.
- **Explicite plutôt qu'inféré.** Ce qu'un canal de saisie ne peut pas capturer
  doit être déclaré. Ne jamais supposer.
- **Les glucides se placent, ils ne se réduisent pas.** Le levier du déficit est
  lipidique ; la quantité de glucides suit la charge, seule leur répartition
  temporelle est un paramètre de pilotage.

## 8. Évolution identifiée

Le modèle décrit ci-dessus porte deux limites assumées :

- la quantité consommée n'est pas un attribut du modèle — elle est figée dans la
  portion de référence, ou contournée par une `PriseLibre` ;
- un même composant ne peut pas être répété dans un même événement.

Les deux se lèvent par une **table de jonction** entre l'événement et le
composant, portant la quantité : composition du composant × quantité de la
ligne, sommée par l'événement. Les canaux `Ingrédient` et `Recette` deviennent
alors des cas de référencement, et la `PriseLibre` une ligne sans référence.

Statut : différée. Motif : coût de migration pendant une période de suivi actif,
pas un doute sur le design.

## 9. Hors périmètre

Ce système est un instrument d'observation personnel. Il ne produit pas de
diagnostic et ne remplace pas un suivi médical ou diététique. Les paramètres par
défaut décrivent une configuration individuelle documentée, non une
recommandation généralisable : toute nouvelle instance doit les redéfinir avec
un professionnel de santé, en particulier en cas de pathologie, de grossesse,
d'antécédent de trouble du comportement alimentaire, ou pour un mineur.
