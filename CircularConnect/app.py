"""
CircularConnect — AI-Powered Registration and Personalised Agenda Platform
for the Circular Technology Summit.

A Flask web application for managing event registrations.
Business Programming Module — Advanced Digital Technologies MSc.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'circularconnect_secret_key_2024'

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'circularconnect.db')


def get_db():
    """Get a database connection with row factory enabled."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Initialise the database schema."""
    conn = get_db()
    cursor = conn.cursor()

    # Create Events table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            location TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            organiser TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create Registrations table (related to Events)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            organisation TEXT,
            job_title TEXT,
            dietary_requirements TEXT,
            session_preference TEXT,
            status TEXT DEFAULT 'confirmed',
            registered_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (event_id) REFERENCES events(id)
        )
    ''')

    conn.commit()
    conn.close()


def seed_data():
    """Insert seed data if the database is empty."""
    conn = get_db()
    cursor = conn.cursor()

    # Check if events already exist
    cursor.execute("SELECT COUNT(*) FROM events")
    if cursor.fetchone()[0] == 0:
        # Insert the main event
        cursor.execute('''
            INSERT INTO events (title, description, date, time, location, capacity, organiser)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            'Circular Technology Summit 2026',
            'A two-day summit exploring the future of circular technology, '
            'data-centre hardware reuse, reverse logistics, sustainable technology, '
            'digital product passports, AI in circular supply chains, and secure '
            'data erasure. Join industry leaders, researchers, and innovators as '
            'we shape a sustainable digital future.',
            '2026-09-15',
            '09:00',
            'Innovation Hub, Dublin, Ireland',
            200,
            'CircularConnect Technologies Ltd.'
        ))

        # Insert additional sessions/events
        cursor.execute('''
            INSERT INTO events (title, description, date, time, location, capacity, organiser)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            'Workshop: Digital Product Passports',
            'Hands-on workshop covering the implementation of digital product '
            'passports for electronic equipment. Learn how to track component '
            'lifecycle, material composition, and recycling potential.',
            '2026-09-15',
            '14:00',
            'Workshop Room A, Innovation Hub, Dublin',
            40,
            'CircularConnect Technologies Ltd.'
        ))

        cursor.execute('''
            INSERT INTO events (title, description, date, time, location, capacity, organiser)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            'Panel: AI in Circular Supply Chains',
            'Expert panel discussion on leveraging artificial intelligence to '
            'optimise reverse logistics, predict equipment end-of-life, and '
            'automate sorting and grading of returned hardware.',
            '2026-09-16',
            '10:30',
            'Main Auditorium, Innovation Hub, Dublin',
            150,
            'CircularConnect Technologies Ltd.'
        ))

        cursor.execute('''
            INSERT INTO events (title, description, date, time, location, capacity, organiser)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            'Seminar: Secure Data Erasure Standards',
            'An in-depth seminar on certified data erasure methods, GDPR compliance '
            'in hardware disposal, and emerging standards for responsible data '
            'destruction in circular economies.',
            '2026-09-16',
            '14:00',
            'Seminar Room B, Innovation Hub, Dublin',
            60,
            'CircularConnect Technologies Ltd.'
        ))

        # Insert sample registrations
        sample_registrations = [
            (1, 'Aoife', 'Murphy', 'aoife.murphy@techrecycle.ie', 'TechRecycle Ireland',
             'Sustainability Director', 'Vegetarian', 'AI in Circular Supply Chains', 'confirmed'),
            (1, 'Liam', 'O\'Brien', 'liam.obrien@greendata.eu', 'GreenData Solutions',
             'CTO', 'None', 'Digital Product Passports', 'confirmed'),
            (1, 'Sofia', 'Andersson', 'sofia.andersson@nordicloop.se', 'NordicLoop AB',
             'Research Lead', 'Vegan', 'Secure Data Erasure', 'confirmed'),
            (1, 'Marcus', 'Weber', 'marcus.weber@circularit.de', 'CircularIT GmbH',
             'Operations Manager', 'None', 'Reverse Logistics', 'confirmed'),
            (1, 'Priya', 'Sharma', 'priya.sharma@ecocompute.in', 'EcoCompute India',
             'Data Scientist', 'Vegetarian', 'AI in Circular Supply Chains', 'confirmed'),
            (1, 'James', 'Kelly', 'james.kelly@reusehub.ie', 'ReUse Hub',
             'Founder', 'Gluten-free', 'Hardware Reuse and Recycling', 'confirmed'),
            (2, 'Elena', 'Rossi', 'elena.rossi@passporttech.it', 'PassportTech Italia',
             'Product Manager', 'None', 'Digital Product Passports', 'confirmed'),
            (3, 'Chen', 'Wei', 'chen.wei@ailogistics.cn', 'AI Logistics Corp',
             'Senior Engineer', 'None', 'AI in Circular Supply Chains', 'confirmed'),
        ]

        cursor.executemany('''
            INSERT INTO registrations
            (event_id, first_name, last_name, email, organisation, job_title,
             dietary_requirements, session_preference, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_registrations)

    conn.commit()
    conn.close()


# ─── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Home page with event information."""
    conn = get_db()
    events = conn.execute('SELECT * FROM events ORDER BY date, time').fetchall()
    conn.close()
    return render_template('index.html', events=events)


@app.route('/event/<int:event_id>')
def event_detail(event_id):
    """Detail page for a specific event."""
    conn = get_db()
    event = conn.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()
    registrations = conn.execute(
        'SELECT * FROM registrations WHERE event_id = ? ORDER BY registered_at DESC',
        (event_id,)
    ).fetchall()
    registration_count = len(registrations)
    conn.close()

    if event is None:
        flash('Event not found.', 'error')
        return redirect(url_for('index'))

    return render_template('event_detail.html', event=event,
                           registrations=registrations,
                           registration_count=registration_count)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration form and processing."""
    conn = get_db()
    events = conn.execute('SELECT * FROM events ORDER BY date, time').fetchall()

    if request.method == 'POST':
        # Collect form data
        event_id = request.form.get('event_id')
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        organisation = request.form.get('organisation', '').strip()
        job_title = request.form.get('job_title', '').strip()
        dietary_requirements = request.form.get('dietary_requirements', '').strip()
        session_preference = request.form.get('session_preference', '').strip()

        # Validation
        errors = []
        if not event_id:
            errors.append('Please select an event.')
        if not first_name:
            errors.append('First name is required.')
        if not last_name:
            errors.append('Last name is required.')
        if not email:
            errors.append('Email is required.')
        elif '@' not in email or '.' not in email:
            errors.append('Please enter a valid email address.')

        # Check capacity
        if event_id:
            event = conn.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()
            if event:
                count = conn.execute(
                    'SELECT COUNT(*) FROM registrations WHERE event_id = ? AND status = "confirmed"',
                    (event_id,)
                ).fetchone()[0]
                if count >= event['capacity']:
                    errors.append('This event is at full capacity.')

            # Check for duplicate email per event
            existing = conn.execute(
                'SELECT id FROM registrations WHERE event_id = ? AND email = ? AND status = "confirmed"',
                (event_id, email)
            ).fetchone()
            if existing:
                errors.append('This email is already registered for this event.')

        if errors:
            for error in errors:
                flash(error, 'error')
            conn.close()
            return render_template('register.html', events=events,
                                   form_data=request.form)

        # Insert registration
        conn.execute('''
            INSERT INTO registrations
            (event_id, first_name, last_name, email, organisation, job_title,
             dietary_requirements, session_preference)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (event_id, first_name, last_name, email, organisation,
              job_title, dietary_requirements, session_preference))
        conn.commit()
        conn.close()

        flash('Registration successful! You are now registered for the event.', 'success')
        return redirect(url_for('registrations_list'))

    conn.close()
    return render_template('register.html', events=events, form_data={})


@app.route('/registrations')
def registrations_list():
    """List of all registered participants."""
    conn = get_db()
    registrations = conn.execute('''
        SELECT r.*, e.title as event_title
        FROM registrations r
        JOIN events e ON r.event_id = e.id
        ORDER BY r.registered_at DESC
    ''').fetchall()
    conn.close()
    return render_template('registrations.html', registrations=registrations)


@app.route('/registration/<int:reg_id>')
def registration_detail(reg_id):
    """Detail page for a specific registration."""
    conn = get_db()
    registration = conn.execute('''
        SELECT r.*, e.title as event_title, e.date as event_date,
               e.time as event_time, e.location as event_location
        FROM registrations r
        JOIN events e ON r.event_id = e.id
        WHERE r.id = ?
    ''', (reg_id,)).fetchone()
    conn.close()

    if registration is None:
        flash('Registration not found.', 'error')
        return redirect(url_for('registrations_list'))

    return render_template('registration_detail.html', registration=registration)


@app.route('/registration/<int:reg_id>/edit', methods=['GET', 'POST'])
def registration_edit(reg_id):
    """Edit a registration."""
    conn = get_db()
    registration = conn.execute('SELECT * FROM registrations WHERE id = ?', (reg_id,)).fetchone()
    events = conn.execute('SELECT * FROM events ORDER BY date, time').fetchall()

    if registration is None:
        flash('Registration not found.', 'error')
        conn.close()
        return redirect(url_for('registrations_list'))

    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        organisation = request.form.get('organisation', '').strip()
        job_title = request.form.get('job_title', '').strip()
        dietary_requirements = request.form.get('dietary_requirements', '').strip()
        session_preference = request.form.get('session_preference', '').strip()

        # Validation
        errors = []
        if not first_name:
            errors.append('First name is required.')
        if not last_name:
            errors.append('Last name is required.')
        if not email:
            errors.append('Email is required.')
        elif '@' not in email or '.' not in email:
            errors.append('Please enter a valid email address.')

        if errors:
            for error in errors:
                flash(error, 'error')
            conn.close()
            return render_template('registration_edit.html',
                                   registration=registration, events=events)

        conn.execute('''
            UPDATE registrations
            SET first_name = ?, last_name = ?, email = ?, organisation = ?,
                job_title = ?, dietary_requirements = ?, session_preference = ?
            WHERE id = ?
        ''', (first_name, last_name, email, organisation, job_title,
              dietary_requirements, session_preference, reg_id))
        conn.commit()
        conn.close()

        flash('Registration updated successfully.', 'success')
        return redirect(url_for('registration_detail', reg_id=reg_id))

    conn.close()
    return render_template('registration_edit.html',
                           registration=registration, events=events)


@app.route('/registration/<int:reg_id>/cancel', methods=['POST'])
def registration_cancel(reg_id):
    """Cancel a registration."""
    conn = get_db()
    registration = conn.execute('SELECT * FROM registrations WHERE id = ?', (reg_id,)).fetchone()

    if registration is None:
        flash('Registration not found.', 'error')
        conn.close()
        return redirect(url_for('registrations_list'))

    conn.execute('UPDATE registrations SET status = "cancelled" WHERE id = ?', (reg_id,))
    conn.commit()
    conn.close()

    flash('Registration has been cancelled.', 'success')
    return redirect(url_for('registrations_list'))


@app.route('/registration/<int:reg_id>/delete', methods=['POST'])
def registration_delete(reg_id):
    """Delete a registration permanently."""
    conn = get_db()
    conn.execute('DELETE FROM registrations WHERE id = ?', (reg_id,))
    conn.commit()
    conn.close()

    flash('Registration has been deleted.', 'success')
    return redirect(url_for('registrations_list'))


# ─── API endpoint for JavaScript interaction ───────────────────────────────────

@app.route('/api/event/<int:event_id>/stats')
def event_stats(event_id):
    """Return event registration statistics as JSON (for JS interaction)."""
    conn = get_db()
    event = conn.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()

    if event is None:
        conn.close()
        return jsonify({'error': 'Event not found'}), 404

    confirmed = conn.execute(
        'SELECT COUNT(*) FROM registrations WHERE event_id = ? AND status = "confirmed"',
        (event_id,)
    ).fetchone()[0]

    cancelled = conn.execute(
        'SELECT COUNT(*) FROM registrations WHERE event_id = ? AND status = "cancelled"',
        (event_id,)
    ).fetchone()[0]

    conn.close()

    return jsonify({
        'event_title': event['title'],
        'capacity': event['capacity'],
        'confirmed': confirmed,
        'cancelled': cancelled,
        'available': event['capacity'] - confirmed
    })


# ─── Initialisation ───────────────────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    seed_data()
    app.run(debug=True, port=5000)
