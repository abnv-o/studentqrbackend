# Student QR Backend with Visual Cryptography

This project is a secure backend system for a student management application that uses **Visual Cryptography** to protect student QR codes. The system splits each QR code into two shares, which are meaningless on their own but reveal the original QR code when overlaid.

---

## Table of Contents

- [Project Title & Description](#project-title--description)
- [Key Features](#key-features)
- [Visual Cryptography](#visual-cryptography)
- [Architecture Overview](#architecture-overview)
- [API Documentation](#api-documentation)
- [Installation Instructions](#installation-instructions)
- [Configuration](#configuration)
- [Development Setup](#development-setup)
- [Deployment](#deployment)
- [Security Analysis](#security-analysis)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Project Title & Description

**Student QR Backend with Visual Cryptography** is a server-side application designed for a modern student management system. The core of this project is to provide a secure way to store and manage student QR codes by splitting them into two encrypted shares using a (2,2) visual cryptography scheme.

This system is perfect for educational institutions that want to enhance the security of their student identification and tracking systems.

### Key Features

* **Student Management:** Complete CRUD (Create, Read, Update, Delete) functionality for student records.
* **Visual Cryptography:** Splits each QR code into two secure shares.
* **API Endpoints:** A RESTful API to manage students and generate QR code shares.
* **Database Integration:** Uses a relational database to store student information and paths to the QR code shares.
* **Django Framework:** Built on the robust and scalable Django web framework.

---

## Visual Cryptography

This project implements a **(2,2) visual cryptography scheme** to secure student QR codes. Here's how it works:

* Each pixel of the QR code is converted into a 2x2 block of subpixels in two separate shares.
* A **white pixel** is represented by the same pattern in both shares.
* A **black pixel** is represented by opposite patterns in the two shares.
* When the two shares are overlaid, the original QR code is revealed.

This ensures that a single share provides no information about the QR code, and both are required for decryption.

---

## Architecture Overview

The project is built using the **Django** web framework and follows a standard monolithic architecture.

* **Django Application:** The core of the application, handling requests, database interactions, and business logic.
* **Models (`models.py`):** Defines the database schema for students, including their personal information and the paths to their QR code shares.
* **Views/API (`views.py`):** Contains the API endpoints for managing students and generating the visual cryptography shares.
* **Visual Cryptography Class (`VisualCryptography`):** A dedicated class that handles the logic for creating and reconstructing the QR code shares.
* **Configuration (`settings.py`):** Manages the application's settings, including database connections and media file paths.

---

## API Documentation

The following API endpoint is available for generating the QR code shares:

### Generate Shares

* **`POST /api/generate-shares/<student_id>/`**

    This endpoint generates two visual cryptography shares for a given student's QR code.

    * **URL Parameters:**
        * `student_id`: The ID of the student.
    * **Response:**
        ```json
        {
          "share1": "media/shares/1_share1.png",
          "share2": "media/shares/1_share2.png"
        }
        ```

---

## Installation Instructions

To get a local copy up and running, follow these steps.

### Prerequisites

* Python 3.x
* pip (Python package installer)
* A virtual environment tool (like `venv`)

### Step-by-Step Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/abnv-o/studentqrbackend.git](https://github.com/abnv-o/studentqrbackend.git)
    cd studentqrbackend
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Run database migrations:**
    ```sh
    python manage.py migrate
    ```

---

## Configuration

The application's configuration is managed in the `settings.py` file. You will need to configure the following:

* **`SECRET_KEY`**: A secret key for the Django application.
* **`DATABASES`**: The database connection settings.
* **`MEDIA_ROOT`** and **`MEDIA_URL`**: The paths for storing and accessing media files, such as the QR code shares.

---

## Development Setup

### Running the Application

To run the application locally for development, use the following command:

```sh
python manage.py runserver
