# Juice Shop login form

A small login page modeled on the OWASP Juice Shop login screen. It checks the email and password in the browser, then checks them again on the server.

## What it does

- Email and password fields
- The form cannot be submitted empty (`required` on both inputs, plus the same check in JavaScript)
- `validateLogin()` requires `@` in the email and at least 8 characters in the password
- `server.py` repeats those checks on `POST /login`
- The page inserts the server's message with `textContent`, so the reply is shown as text
- The server does not build a SQL statement from the input
- Responses include a Content-Security-Policy that allows scripts only from this site

There is no user database. A request that passes validation still gets `Invalid email or password.`

## Run it

From this directory:

```bash
python3 server.py
```

Open [http://127.0.0.1:8080](http://127.0.0.1:8080).

No packages to install. Python 3 is enough.
