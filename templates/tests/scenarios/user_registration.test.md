# Scenario: User Registration

> Test conversation flow for new user signup

## Metadata

| Field | Value |
|-------|-------|
| scenario_name | user_registration |
| version | 1.0.0 |
| agent | Dev Agent |
| framework | [Jest/Pytest/Playwright] |
| estimated_duration | 45s |

## Description

Test that the registration system handles new user creation, validation, and confirmation correctly.

## Preconditions

- User is not logged in
- Database is clean or has known state
- Email service is mocked or test-ready

## Script

### Test Case 1: Successful Registration

```
USER: I want to create a new account
AGENT: [Should prompt for registration details]
USER: 
  - email: newuser@example.com
  - password: SecurePass123!
  - name: New User
AGENT: [Should validate and create account]
  -> VERIFY: user created in database
  -> VERIFY: confirmation email sent
  -> VERIFY: success message shown
  -> VERIFY: user NOT automatically logged in (email verification required)
```

### Test Case 2: Duplicate Email

```
USER: I want to register
AGENT: [Should prompt for details]
USER: email: existing@example.com (already in DB), password: Test123!
AGENT: [Should reject duplicate]
  -> VERIFY: error message about email already exists
  -> VERIFY: no account created
  -> VERIFY: password NOT in error message (security)
```

### Test Case 3: Invalid Email Format

```
USER: I want to register
AGENT: [Should prompt for details]
USER: email: not-an-email, password: Test123!
AGENT: [Should validate format]
  -> VERIFY: error about invalid email format
  -> VERIFY: no account created
```

### Test Case 4: Weak Password

```
USER: I want to register
AGENT: [Should prompt for details]
USER: email: valid@example.com, password: 123
AGENT: [Should reject weak password]
  -> VERIFY: error about password requirements
  -> VERIFY: no account created
```

### Test Case 5: Email Confirmation

```
USER: I've received my confirmation email
AGENT: [Should provide link or code input]
USER: Confirmation code: ABC123
AGENT: [Should verify and activate account]
  -> VERIFY: account marked as active
  -> VERIFY: user can now log in
```

## Success Criteria

- [ ] Valid registration creates account
- [ ] Duplicate email is rejected securely
- [ ] Invalid email format is rejected
- [ ] Weak passwords are rejected
- [ ] Email confirmation activates account
- [ ] Password requirements are enforced
- [ ] No sensitive data in error messages

## Security Checks

- Password not logged or exposed in errors
- Email enumeration prevention
- Rate limiting on registration attempts
- SQL injection prevention in form inputs

## Notes

This scenario covers the complete registration flow. Adjust validation rules based on project requirements.
