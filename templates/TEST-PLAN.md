# MDAN Template — Test Plan

---
**Artifact:** Test Plan
**Phase:** VERIFY
**Agent:** Test Agent v1.0.0
**Version:** [X.Y]
**Status:** Draft | Review | Validated
**Date:** [YYYY-MM-DD]
**Project:** [Project Name]
---

## 1. Test Strategy

| Type | Coverage Target | Tools | Automated |
|------|----------------|-------|-----------|
| Unit | 80%+ | [Jest/Vitest/Pytest/etc.] | Yes |
| Integration | Key flows | [Tool] | Yes |
| E2E | Critical paths | [Cypress/Playwright/etc.] | Yes |
| Performance | p95 < [Xms] @ [Y rps] | [k6/JMeter] | Yes |
| Security | OWASP Top 10 | [Tool] | Partial |
| Manual | Edge cases | N/A | No |

## 2. Test Cases

### Feature: [Feature Name]

#### Unit Tests
```[language]
describe('[Component/Function]', () => {
  it('should [expected behavior] when [condition]', () => {
    // Arrange
    const input = [...]
    // Act
    const result = functionCall(input)
    // Assert
    expect(result).toBe([expected])
  })

  it('should throw [error] when [invalid condition]', () => {
    expect(() => functionCall(invalidInput)).toThrow('[error message]')
  })
})
```

#### Integration Tests
```[language]
// Test que [Component A] + [Component B] fonctionnent ensemble
```

#### E2E Scenarios

**Scénario 1 — Happy Path : [Name]**
- Given: [Préconditions]
- When: [Actions utilisateur]
- Then: [Résultat attendu]

**Scénario 2 — Error Path : [Name]**
- Given: [Préconditions]
- When: [Action invalide]
- Then: [Gestion d'erreur attendue]

## 3. Edge Cases & Security Tests

| Cas | Input | Comportement attendu |
|-----|-------|---------------------|
| Input vide | `""` | Erreur : "Champ requis" |
| Longueur max | 10001 chars | Erreur : "Max 10000 chars" |
| SQL Injection | `"' OR 1=1"` | Input sanitisé, aucun accès DB |
| XSS | `"<script>..."` | Input échappé en sortie |
| Auth bypass | Token expiré | 401 Unauthorized |

## 4. Performance Test Scenarios

| Scénario | Charge | Durée | Critère de passage |
|----------|--------|-------|--------------------|
| Charge normale | 100 rps | 5 min | p95 < 200ms, erreurs < 0.1% |
| Pic de charge | 1000 rps | 1 min | p95 < 500ms, erreurs < 1% |

## 5. Test Data Requirements

[Données de test nécessaires, comment les générer, comment les reset après les tests]

## 6. Limitations connues

[Ce qui n'est PAS testé et pourquoi]

## 7. Résultats

| Type | Total | Passés | Échoués | Couverture |
|------|-------|--------|---------|-----------|
| Unit | — | — | — | —% |
| Integration | — | — | — | — |
| E2E | — | — | — | — |
| Performance | — | — | — | — |

*Test Plan validé par :* ________________ *Date :* ________________
