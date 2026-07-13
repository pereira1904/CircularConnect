# CircularConnect

**AI-Powered Registration and Personalised Agenda Platform for a Circular Technology Summit**

This Flask web application for managing event registrations at a fictional Circular Technology Summit was created by Group 32 as a project for the Business Programming module of the Advanced Digital Technologies MSc.

---

## Project Overview

CircularConnect manages registrations for a fictional two-day summit focused on:

- Data-centre hardware reuse and recycling
- Reverse logistics
- Sustainable technology
- Digital product passports
- AI in circular supply chains
- Secure data erasure and responsible disposal

The fictional organisation **CircularConnect Technologies Ltd.** hosts the event at the Innovation Hub, Dublin, Ireland.

---

## Features

| Feature | Description |
|---------|-------------|
| Event Information Page | Home page displaying summit details and all sessions |
| Registration Form | Full form with validation, capacity checking, and duplicate detection |
| Database Storage | SQLite database with two related tables (events, registrations) |
| Registrations List | Searchable table of all registered participants |
| Registration Detail | Individual detail page for each registration |
| Edit Registration | Update participant details via a pre-populated form |
| Cancel Registration | Soft-cancel with status change (confirmed → cancelled) |
| Delete Registration | Permanent removal with confirmation modal |
| JavaScript Interactions | Live search/filter, AJAX capacity indicator, confirmation modals, auto-dismiss flash messages, client-side form validation, live stats dashboard |
| Responsive Design | Mobile-friendly layout with CSS Grid and Flexbox |

---

## Technologies

| Technology | Purpose |
|------------|---------|
| Python 3 | Backend programming language |
| Flask | Web framework |
| SQLite | Relational database |
| HTML5 | Page structure and content |
| CSS3 | Styling and responsive layout |
| JavaScript (ES6) | Client-side interactivity |

---

## Project Structure

```
CircularConnect/
├── app.py                  # Main Flask application (routes, database, logic)
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── circularconnect.db      # SQLite database (auto-created on first run)
├── static/
│   ├── css/
│   │   └── style.css       # Application stylesheet
│   └── js/
│       └── main.js         # JavaScript interactions
└── templates/
    ├── base.html           # Base template with navigation and footer
    ├── index.html          # Home page / event information
    ├── event_detail.html   # Individual event detail page
    ├── register.html       # Registration form
    ├── registrations.html  # List of all registrations
    ├── registration_detail.html  # Individual registration detail
    └── registration_edit.html    # Edit registration form
```

---

## Database Schema

The application uses two related tables:

### Events Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER (PK) | Auto-incrementing primary key |
| title | TEXT | Event title |
| description | TEXT | Event description |
| date | TEXT | Event date (YYYY-MM-DD) |
| time | TEXT | Event start time (HH:MM) |
| location | TEXT | Venue location |
| capacity | INTEGER | Maximum number of attendees |
| organiser | TEXT | Organising body |
| created_at | TEXT | Timestamp of record creation |

### Registrations Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER (PK) | Auto-incrementing primary key |
| event_id | INTEGER (FK) | Foreign key referencing events.id |
| first_name | TEXT | Participant's first name |
| last_name | TEXT | Participant's last name |
| email | TEXT | Participant's email address |
| organisation | TEXT | Participant's organisation |
| job_title | TEXT | Participant's job title |
| dietary_requirements | TEXT | Dietary needs |
| session_preference | TEXT | Preferred session topic |
| status | TEXT | Registration status (confirmed/cancelled) |
| registered_at | TEXT | Timestamp of registration |

**Relationship:** Each registration belongs to one event (many-to-one). The `event_id` foreign key enforces referential integrity.

---

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Extract the zip file** and navigate to the project directory:

   ```bash
   cd CircularConnect
   ```

2. **Create a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate      # On macOS/Linux
   venv\Scripts\activate         # On Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**

   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to:

   ```
   http://127.0.0.1:5000
   ```

The database (`circularconnect.db`) is automatically created and seeded with sample data on first run.

---

## Usage Guide

### Viewing Events
- The **Home** page displays all summit sessions with key details.
- Click **View Details** on any event card to see full information and registered participants.

### Registering for an Event
- Click **Register** in the navigation bar.
- Select an event from the dropdown (a live capacity bar appears via AJAX).
- Fill in the required fields (marked with *) and submit.
- The system validates input and checks for duplicate emails and capacity limits.

### Managing Registrations
- Click **Registrations** in the navigation bar to view all registrations.
- Use the **search box** to filter by name, email, or organisation (JavaScript live filter).
- Click **View** to see full registration details.
- Click **Edit** to modify registration information.
- Use **Cancel Registration** to change status to cancelled (soft delete).
- Use **Delete** to permanently remove a registration (with confirmation modal).

---

## JavaScript Interactions

The application includes the following JavaScript features:

1. **Live Search/Filter** — Instantly filters the registrations table as you type.
2. **AJAX Capacity Indicator** — Fetches event capacity data via the `/api/event/<id>/stats` endpoint and displays a progress bar when selecting an event on the registration form.
3. **Confirmation Modals** — Custom modal dialogs appear before cancel/delete actions.
4. **Auto-Dismiss Flash Messages** — Success/error notifications fade out after 5 seconds.
5. **Client-Side Form Validation** — Required fields are highlighted before submission.
6. **Live Stats Dashboard** — The home page loads registration statistics dynamically via AJAX.

---

## Sample Data

The application is pre-seeded with:

- **4 events** (main summit, workshop, panel discussion, seminar)
- **8 sample registrations** with fictional participants from various European and international organisations

All data is entirely fictional and created for demonstration purposes.

---

## Author

Business Programming Module - Group 32 - Advanced Digital Technologies MSc

---

## Licence

This project is submitted as academic coursework. All code is original and written for educational purposes.
