# Scenario: User Authentication

> Test conversation flow for basic authentication functionality

## Metadata

| Field | Value |
|-------|-------|
| scenario_name | basic_authentication |
| version | 1.0.0 |
| agent | Dev Agent |
| framework | [Jest/Pytest/Playwright] |
| estimated_duration | 30s |

## Description

Test that the authentication system handles login, logout, and session management correctly.

## Preconditions

- User is not logged in
- Database contains test users
- Auth service is running

## Script

### Test Case 1: Successful Login

```
USER: I want to log in with my account
AGENT: [Should prompt for credentials or display login form]
USER: My email is test@example.com and password is Test123!
AGENT: [Should validate credentials]
  -> VERIFY: auth_token received
  -> VERIFY: user object returned with correct email
USER: What's my username?
AGENT: [Should return 'test@example.com' from session]
  -> VERIFY: response contains correct username
```

### Test Case 2: Invalid Credentials

```
USER: I want to log in
AGENT: [Should prompt for credentials]
USER: email: wrong@example.com, password: wrongpass
AGENT: [Should reject with error message]
  -> VERIFY: error message does NOT reveal if email exists
  -> VERIFY: no auth_token in response
```

### Test Case 3: Logout

```
USER: I'm logged in and want to log out
AGENT: [Should clear session]
  -> VERIFY: session cleared
  -> VERIFY: confirmation message shown
USER: Can I see my profile?
AGENT: [Should deny access]
  -> VERIFY: 401 or redirect to login
```

## Success Criteria

- [ ] Login with valid credentials succeeds
- [ ] Login with invalid credentials fails with secure error
- [ ] Logout clears session completely
- [ ] Protected routes redirect unauthenticated users
- [ ] Session expires after configured timeout

## Failure Handling

If any step fails, the scenario should:
1. Capture the actual response
2. Compare with expected behavior
3. Log the difference for debugging
4. Fail the test with descriptive error

## Notes

This scenario tests the authentication flow end-to-end. Use with Playwright for browser-based testing or Pytest for API-based testing.
