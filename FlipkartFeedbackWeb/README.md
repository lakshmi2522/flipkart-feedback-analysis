# Flipkart Customer Feedback Analysis — Public Deployment Package

This is an educational project inspired by a customer-feedback workflow. It is **not an official Flipkart service**. The app analyzes text entered by a visitor and does not store submissions in a database. Avoid entering sensitive personal information.

## Deploy it publicly with Render (no local server needed)

1. Sign in to GitHub and create a **new public repository** named `flipkart-feedback-analysis`.
2. Extract this ZIP. Open the `FlipkartFeedbackWeb` folder. Upload the *contents* of this folder to the repository (including `Dockerfile`, `render.yaml`, `CustomerFeedbackWeb.java`, and the `public` folder).
3. Sign in to Render and choose **New + → Web Service**.
4. Connect your GitHub repository.
5. Select **Docker** as the runtime if prompted. The included `Dockerfile` builds and runs the Java app.
6. Create the service. Wait until deployment shows **Live**.
7. Open the `onrender.com` URL Render displays and share that URL.

Render may ask you to sign in or approve repository access. Never share your account password or access token in chat. On free hosting, the service may sleep after inactivity and take a short time to wake up.

## Run locally on Windows

1. Install JDK 17 or newer.
2. Double-click `run.bat`.
3. Open `http://localhost:8080`.

## What the app does

- Validates the customer name and feedback (1–500 characters).
- Counts characters and words.
- Counts case-insensitive keyword substring occurrences.
- Does not permanently save feedback or connect to Flipkart systems.

## Public deployment files

- `Dockerfile` — builds the Java server for hosting.
- `render.yaml` — Render service configuration.
- `CustomerFeedbackWeb.java` — backend API and static-file server; uses the hosting platform's `PORT` environment variable.
- `public/` — frontend files.
