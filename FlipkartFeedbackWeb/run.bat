@echo off
cd /d "%~dp0"
title Flipkart Customer Feedback Analysis
where java >nul 2>nul
if errorlevel 1 (
  echo Java was not found. Install JDK 17 or newer first.
  pause
  exit /b 1
)
where javac >nul 2>nul
if errorlevel 1 (
  echo javac was not found. Install a JDK, not only a JRE.
  pause
  exit /b 1
)
echo Compiling the application...
javac --add-modules jdk.httpserver CustomerFeedbackWeb.java
if errorlevel 1 (pause & exit /b 1)
echo Starting the application at http://localhost:8080
java --add-modules jdk.httpserver CustomerFeedbackWeb
pause
