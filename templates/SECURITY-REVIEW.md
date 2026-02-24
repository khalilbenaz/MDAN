# MDAN Template — Security Review

---
**Artifact:** Security Review
**Phase:** VERIFY
**Agent:** Security Agent v1.0.0
**Version:** [X.Y]
**Status:** Draft | Review | Signed Off
**Date:** [YYYY-MM-DD]
**Project:** [Project Name]
---

## 1. Threat Model (STRIDE)

### Assets à protéger
| Asset | Sensibilité | Localisation |
|-------|-------------|--------------|
| Credentials utilisateurs | Critique | DB (hashés) |
| Données personnelles | Élevée | DB |
| Clés API | Critique | Variables d'environnement |

### Surface d'attaque
| Point d'entrée | Description | Niveau de risque |
|---------------|-------------|-----------------|
| API REST | Endpoints HTTP publics | Élevé |
| Interface admin | Dashboard interne | Moyen |

### Analyse STRIDE
| Menace | Composant | Mitigation |
|--------|-----------|-----------|
| Spoofing | Auth | JWT + refresh tokens |
| Tampering | API inputs | Validation stricte |
| Repudiation | Actions user | Audit logging |
| Info Disclosure | API responses | Filtrage des réponses |
| DoS | Endpoints publics | Rate limiting |
| Elevation of Privilege | RBAC | Vérification sur chaque endpoint |

## 2. Findings

### 🔴 CRITICAL — Bloquer la release

#### VULN-001: [Nom]
- **Type :** [Catégorie OWASP]
- **Localisation :** [Fichier/Endpoint]
- **Description :** [Ce que c'est]
- **Impact :** [Ce qu'un attaquant peut faire]
- **Reproduction :** [Comment reproduire]
- **Remédiation :** [Fix exact avec code si applicable]
- **Statut :** ⏳ Open | ✅ Fixed | ⚠️ Accepted

### 🟠 HIGH — Corriger avant release

### 🟡 MEDIUM — Corriger dans le prochain sprint

### 🔵 LOW — Tracker et corriger éventuellement

## 3. Security Checklist

### Authentification
- [ ] Mots de passe hashés avec bcrypt/argon2 (cost factor ≥ 12)
- [ ] Tokens JWT avec expiration + refresh
- [ ] Protection brute force (rate limiting sur /auth)
- [ ] Invalidation de session au logout

### Autorisation
- [ ] Vérification auth sur CHAQUE endpoint protégé
- [ ] Contrôle d'accès horizontal (user A ne peut pas accéder aux données de user B)
- [ ] RBAC implémenté correctement
- [ ] Fonctions admin séparément protégées

### Validation des inputs
- [ ] Tous les inputs validés côté serveur
- [ ] Requêtes SQL paramétrées (jamais d'interpolation)
- [ ] Uploads : validation type, taille, stockage hors web root
- [ ] Encoding des outputs pour prévenir XSS

### Protection des données
- [ ] HTTPS enforced partout
- [ ] Données sensibles non loggées
- [ ] PII traité selon exigences réglementaires
- [ ] Backups chiffrés

### Dépendances
- [ ] Aucune CVE critique connue dans les dépendances
- [ ] Lockfile commité
- [ ] Scan CVE automatisé en CI/CD

## 4. Sign-Off

| Findings | Total | Résolus | Acceptés | Restants |
|----------|-------|---------|----------|---------|
| Critical | — | — | — | — |
| High | — | — | — | — |
| Medium | — | — | — | — |
| Low | — | — | — | — |

**Security sign-off :** ________________ **Date :** ________________

*Conditions de sign-off : 0 Critical open, 0 High open (ou acceptés avec justification documentée)*
