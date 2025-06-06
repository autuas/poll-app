# Poll App

This is a simple polling web application built using [Django](https://www.djangoproject.com/) 4.2. 

## Features

- User registration and login
- Poll creation by logged-in users
- Voting
- Poll closing and result display
- Security flaw demonstrations and fixes

## Requirements

- Python >= 3.8
- Django >= 4.2

## Setup

- In your terminal, navigate to your preferred directory and run: `git clone https://github.com/autuas/poll-app`
- Change into the project directory and apply migrations: `python3 manage.py migrate`
- (Optional) At the same project directory, create a superuser to access the admin interface: `python3 manage.py createsuperuser`

## Run
- While at the project directory, start the app by running: `python3 manage.py runserver`
- When the app is running, go to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser

## Use

- The app starts at the login page
- To register as a new user, click the *register here* link and follow the instructions
- To fully explore how the app works, create at least two users
- Log in with one user to create polls and add choices. Log out, then log in with another user to vote on polls created by the first user
- Poll owners can end or delete their polls. Ending a poll declares a winner if at least one vote was cast

## Security Flaws

This project demonstrates five different security flaws with corresponding fixes. The fixes can be applied by commenting out the vulnerable code and/or uncommenting the safe code. The flaws, except for the fifth one, are based on the [OWASP Top 10 - 2021 list](https://owasp.org/Top10/):

1. A01:2021-Broken Access Control
2. A03:2021-Injection
3. A05:2021-Security Misconfiguration
4. A09:2021-Security Logging and Monitoring Failures
5. Cross-Site Request Forgery (CSRF)

Screenshots for the flaws and fixes are available in the [`screenshots`](https://github.com/autuas/poll-app/tree/main/screenshots) folder.

## Additional Security Note

This project contains a secret key in `settings.py`. The key is publicly visible for demonstration purposes only. In real projects, a secret key must not be exposed in production, and needs to be stored securely.

## License

This project is licensed under the [MIT License](LICENSE).

