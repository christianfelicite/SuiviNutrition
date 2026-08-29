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

### 2.1 `Aliment`

Référentiel. Un aliment est une **définition**, pas une consommation.

- Identité stable, indépendante de toute consommation.
- Porte une composition pour une quantité de référence : énergie, protéines,
  lipides, glucides.
- Peut porter des marqueurs qualitatifs : véhicule lipidique, saisonnalité,
  origine.
- N'est jamais dupliqué par consommation. Un même aliment consommé deux fois
  reste un seul enregistrement.

### 2.2 `LignePrise`

Table de jonction. **Porte la quantité.**

- Relie exactement un `Aliment` à exactement une `Prise`.
- Porte la quantité consommée, exprimée dans une unité de saisie
  (voir `protocole-saisie.md`).
- C'est la seule entité qui porte une quantité. Aucune autre.

> **Note d'implémentation.** L'instance de référence n'a pas encore cette table :
> la quantité y est portée par l'enregistrement de consommation lui-même, ce qui
> empêche de réutiliser un aliment sans dupliquer sa composition. C'est une dette
> connue, documentée dans `adaptateur-notion.md`. Le modèle correct est celui
> décrit ici : toute nouvelle instanciation doit implémenter la jonction.

### 2.3 `Prise`

Événement de consommation situé dans le temps.

- Porte un instant et un libellé.
- Agrège les `LignePrise` qui la composent.
- Une `Prise` appartient à un `Jour`.

**Invariant explicite :** une `LignePrise` peut être rattachée à plusieurs
`Prise`. Ce n'est pas une anomalie d'intégrité. Le cas se produit légitimement
lorsqu'une même préparation est consommée sur deux occasions distinctes, ou
qu'elle chevauche deux jours. Toute implémentation doit l'autoriser et aucun
contrôle de cohérence ne doit le signaler comme erreur.

### 2.4 `Jour`

Unité de bilan.

- Porte une date, un **type de jour** et une charge d'entraînement.
- Agrège les `Prise` de la journée.
- Porte les cibles calculées et l'écart signé à ces cibles.

### 2.5 `EntreeJournal`

Narratif : contexte, ressenti, événement de vie, écart assumé.

Le journal n'est pas un accessoire. Les valeurs chiffrées disent *quoi*, le
journal dit *pourquoi*. **Toute analyse du système doit s'appuyer sur les
entrées du journal** ; une analyse purement quantitative produit des
recommandations inapplicables au contexte réel.

## 3. Cardinalités

```
Aliment  1 ──── n  LignePrise  n ──── n  Prise  n ──── 1  Jour  1 ──── n  EntreeJournal
```

- `Aliment` → `LignePrise` : un aliment est référencé par un nombre quelconque de
  lignes. Sa composition n'est jamais recopiée.
- `LignePrise` → `Prise` : n..n. Cardinalité multiple **intentionnelle**, cf. §2.3.
- `Prise` → `Jour` : n..1. Une prise appartient à un seul jour.
- `Jour` → `EntreeJournal` : 1..n. Un jour peut porter plusieurs entrées.

## 4. Chaîne de calcul

Le calcul est **ascendant et strictement ordonné**. Chaque niveau agrège le
niveau inférieur ; aucun niveau ne recalcule ce qu'un autre a déjà agrégé.

```
LignePrise    composition(Aliment) × quantité
     ↓  Σ
Prise         totaux de la prise + franchissements de seuils par prise
     ↓  Σ
Jour          totaux du jour + cibles + écart signé
```

**Règle de lecture.** Les totaux d'un niveau se lisent dans l'agrégat de ce
niveau. Jamais par addition manuelle des éléments connus : les éléments non
interrogés seraient silencieusement omis, et l'erreur serait indétectable.

**Règle de correction.** Corriger dans l'ordre : ligne, puis prise, puis jour.
Corriger un total sans corriger sa source crée une divergence qui ne se signale
pas.

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

Les seuils s'évaluent **par prise**, pas par jour. C'est le point structurant :
un total journalier conforme peut masquer une répartition inopérante.

| Seuil | Nature | Clé |
|---|---|---|
| Synthèse protéique | plancher — en deçà, l'apport ne déclenche pas la synthèse | `proteines.seuil_synthese_par_prise` |
| Plafond lipidique | plafond par prise | `lipides.plafond_par_prise` |
| Véhicule lipidique | un seul véhicule autorisé par prise | `lipides.seuil_vehicule`, `lipides.vehicules_max_par_prise` |

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

## 8. Hors périmètre

Ce système est un instrument d'observation personnel. Il ne produit pas de
diagnostic et ne remplace pas un suivi médical ou diététique. Les paramètres par
défaut décrivent une configuration individuelle documentée, non une
recommandation généralisable : toute nouvelle instance doit les redéfinir avec
un professionnel de santé, en particulier en cas de pathologie, de grossesse,
d'antécédent de trouble du comportement alimentaire, ou pour un mineur.
