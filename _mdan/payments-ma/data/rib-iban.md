# RIB & IBAN Maroc — Structure, Clé, Conversion

Référence technique pour tout code de validation/génération de RIB et d'IBAN marocains. Les chiffres de structure (longueurs) sont des standards interbancaires stables ; en cas de doute sur un cas particulier (ex : banque avec format hérité), vérifier auprès de la banque concernée.

## 1. Structure du RIB marocain (24 chiffres)

| Bloc | Longueur | Contenu |
|------|----------|---------|
| Code banque | 3 chiffres | Identifiant de la banque (attribué par Bank Al-Maghrib) |
| Code ville/agence | 3 chiffres | Identifiant de la ville/agence |
| Numéro de compte | 16 chiffres | Numéro de compte, complété par des zéros à gauche si plus court |
| Clé RIB | 2 chiffres | Clé de contrôle mod-97 (voir §2) |
| **Total** | **24 chiffres** | |

Le RIB marocain suit la même logique que le RIB français (héritage du système bancaire), mais avec des longueurs de blocs différentes (3+3+16+2 = 24, contre 5+5+11+2 = 23 en France).

## 2. Algorithme de la clé RIB (mod 97)

La clé est calculée en traitant la concaténation `code_banque + code_ville + numero_compte` (22 chiffres) comme un grand nombre entier, en lui ajoutant deux zéros, puis en calculant le reste modulo 97 :

```
concat22 = code_banque(3) + code_ville(3) + numero_compte(16)   # 22 chiffres
reste = Number(concat22 + "00") mod 97
cle = 97 - reste
si cle == 0 : cle = 97   # convention ISO 7064 : jamais de clé "00"
```

En pratique, `concat22` dépasse la précision des entiers natifs — l'implémenter en traitant les chiffres un par un (réduction modulaire progressive), pas avec un simple `Number()` ou `parseInt()` :

```js
function mod97(digitString) {
  let rem = 0;
  for (const ch of digitString) rem = (rem * 10 + Number(ch)) % 97;
  return rem;
}
```

### Validation d'un RIB existant

Un RIB de 24 chiffres est valide si `mod97(rib24) === 0` (puisque la clé a été choisie pour annuler le reste).

## 3. IBAN Maroc (28 caractères)

Format : `MA` + 2 chiffres de contrôle IBAN + RIB (24 chiffres) = 28 caractères au total.

L'algorithme de calcul des 2 chiffres de contrôle suit la norme ISO 13616 (mod 97-10), commune à tous les IBAN :

1. Réarranger : `BBAN(24) + code_pays("MA") + "00"`
2. Convertir les lettres en chiffres : `A=10, B=11, ..., Z=35` (donc `M=22`, `A=10` → "MA" devient "2210")
3. Calculer `reste = mod97(chaîne_numérique_complète)`
4. `chiffres_de_contrôle = 98 - reste`, formaté sur 2 chiffres

```
iban = "MA" + chiffres_de_contrôle + rib24
```

### Validation d'un IBAN existant

Réarranger l'IBAN en déplaçant les 4 premiers caractères (`MA` + 2 chiffres de contrôle) à la fin, convertir les lettres restantes en chiffres, puis vérifier que `mod97(...) === 1`.

## 4. Exemple travaillé (calculé et vérifié avec Node.js — `mod97` ci-dessus)

Données d'entrée (fictives, à but illustratif uniquement) :
- Code banque : `230`
- Code ville : `780`
- Numéro de compte (avant complétion) : `0123456789012` → complété sur 16 chiffres : `0000123456789012`

Calcul :
- `concat22` = `230` + `780` + `0000123456789012` = `2307800000123456789012`
- `mod97(concat22 + "00")` = `15`
- `clé` = `97 - 15` = `82`
- **RIB** = `2307800000123456789012` + `82` = **`230780000012345678901282`** (24 chiffres)

IBAN :
- `BBAN + "MA" + "00"` converti (M=22, A=10) → mod97 = `34`
- Chiffres de contrôle = `98 - 34` = `64`
- **IBAN** = **`MA64230780000012345678901282`** (28 caractères)

Vérification indépendante : `mod97` de l'IBAN réarrangé (`230780000012345678901282` + `MA` converti + `64` → tout en fin) = `1`, ce qui confirme un IBAN valide selon ISO 13616.

## 5. Pièges d'implémentation

- **Ne jamais utiliser `Number()`/`BigInt` naïvement pour tout le calcul si le langage a des limites de précision** — utiliser la réduction modulaire digit-par-digit (`mod97` ci-dessus) qui fonctionne dans n'importe quel langage sans dépendance à l'arithmétique grands nombres.
- **Le numéro de compte doit être complété par des zéros à gauche** jusqu'à 16 chiffres avant le calcul de la clé — un compte "raccourci" sans padding donnera une clé fausse.
- **Une clé calculée à 0 doit être forcée à 97** (convention ISO 7064), sinon le RIB aurait une clé "00" qui n'est normalement pas émise.
- **Le code banque et le code ville sont attribués par Bank Al-Maghrib** — ne jamais les inventer ou les deviner pour une intégration réelle ; toujours les obtenir de la banque partenaire ou d'un référentiel officiel à jour.
- **Un RIB syntaxiquement valide (clé correcte) n'est pas nécessairement un compte existant** — la clé prouve seulement l'absence d'erreur de frappe, pas l'existence du compte. Toujours prévoir une vérification applicative (ex : appel à la banque, virement de 1 MAD de test) avant un premier virement significatif si le contexte l'exige.
