This file is a glossary of all the necessary environment variables for the application to run.

The following is a list of all available environment variables used by the bot:

| Variable       | Required | Description                                                                                                                                                                  |
|----------------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `SECRET_KEY`   | Always   | The key that Django will use for cryptographic signing/validation.                                                                                                           |
| `DEBUG`        | Always   | A boolean that determines whether we run the server in a development setup or not. When True, we'll use an `sqlite` database to run tests etc, otherwise a Postgres database |
| `DATABASE_URL` | Optional | The URL of the Postgres database to connect to. This only required when Debug=False                                                                                          |


These variables can either be configured as real environment varilabes, or put in an `.env` at the root of the `backend` folder.
