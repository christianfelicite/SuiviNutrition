# SuiviNutrition

Spécification d'un système de suivi nutritionnel et d'entraînement piloté par la
donnée, conçu pour être **instancié par d'autres**.

L'objectif n'est pas de compter les calories. C'est de rendre observables les
modes de défaillance d'une alimentation réelle — table partagée, produits de
saison, jeûne intermittent, charge d'entraînement — pour que la correction
devienne un réflexe et non une décision.

## Nature de ce dépôt

Ce dépôt contient **la structure de l'outil, jamais les données**. Les données
d'une instance — prises, journal, mesures — restent dans son support de
stockage. Le dépôt est public et ne contient aucun identifiant d'instance.

```
Aliment ── LignePrise ── Prise ── Jour ── EntreeJournal
   référentiel   quantité   événement   bilan   narratif
```

## Documents

| Document | Portée |
|---|---|
| [`docs/modele-domaine.md`](docs/modele-domaine.md) | Entités, cardinalités, chaîne de calcul, cibles et seuils. **Portable.** |
| [`docs/protocole-saisie.md`](docs/protocole-saisie.md) | Double canal, unités, placement, modes de défaillance. **Portable.** |
| [`docs/adaptateur-notion.md`](docs/adaptateur-notion.md) | Implémentation de référence et ses contournements. **Contingent.** |
| [`config/parametres-defaut.yaml`](config/parametres-defaut.yaml) | Toutes les valeurs numériques normatives. Surchargeables. |
| [`CLAUDE.md`](CLAUDE.md) | Règles de travail dans le dépôt. |

Lire les deux premiers pour comprendre le système. Le troisième n'est utile que
pour reconstruire l'instance Notion : sur un autre support, il est ignorable en
totalité.

## Instancier

1. Copier `config/parametres-defaut.yaml` et **redéfinir toutes les valeurs**.
   Celles fournies décrivent une configuration individuelle, pas une
   recommandation.
2. Implémenter les entités de `docs/modele-domaine.md`, jonction comprise.
3. Appliquer `docs/protocole-saisie.md` — le canal déclaratif n'est pas
   optionnel.

## Feuille de route

- [ ] Migration vers la table de jonction `LignePrise`
- [ ] Externalisation des seuils hors des formules de l'instance de référence
- [ ] Validation multi-utilisateurs sur un groupe test restreint

## Avertissement

Instrument d'observation personnel. Ne produit pas de diagnostic et ne remplace
pas un suivi médical ou diététique.
