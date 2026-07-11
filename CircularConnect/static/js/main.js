/**
 * CircularConnect — JavaScript Interactions
 * Provides dynamic functionality for the registration platform.
 */

document.addEventListener('DOMContentLoaded', function () {

    // ─── Flash Message Auto-Dismiss ───────────────────────────────────────────
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(function (flash) {
        setTimeout(function () {
            flash.style.opacity = '0';
            flash.style.transform = 'translateY(-10px)';
            setTimeout(function () {
                flash.remove();
            }, 300);
        }, 5000);
    });

    // ─── Registration Search / Filter ─────────────────────────────────────────
    const searchInput = document.getElementById('search-registrations');
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const query = this.value.toLowerCase();
            const rows = document.querySelectorAll('#registrations-table tbody tr');

            rows.forEach(function (row) {
                const text = row.textContent.toLowerCase();
                if (text.includes(query)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });

            // Update visible count
            const visibleCount = document.querySelectorAll(
                '#registrations-table tbody tr:not([style*="display: none"])'
            ).length;
            const countEl = document.getElementById('visible-count');
            if (countEl) {
                countEl.textContent = visibleCount + ' registration(s) shown';
            }
        });
    }

    // ─── Confirmation Modal for Cancel/Delete ─────────────────────────────────
    const cancelBtns = document.querySelectorAll('[data-confirm]');
    cancelBtns.forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();

            const message = this.getAttribute('data-confirm');
            const form = this.closest('form');

            // Create modal overlay
            const overlay = document.createElement('div');
            overlay.className = 'modal-overlay active';
            overlay.innerHTML = `
                <div class="modal">
                    <h3>Confirm Action</h3>
                    <p>${message}</p>
                    <div class="btn-group">
                        <button class="btn btn-outline" id="modal-cancel">No, Go Back</button>
                        <button class="btn btn-danger" id="modal-confirm">Yes, Proceed</button>
                    </div>
                </div>
            `;

            document.body.appendChild(overlay);

            // Handle modal buttons
            document.getElementById('modal-cancel').addEventListener('click', function () {
                overlay.remove();
            });

            document.getElementById('modal-confirm').addEventListener('click', function () {
                form.submit();
            });

            // Close on overlay click
            overlay.addEventListener('click', function (e) {
                if (e.target === overlay) {
                    overlay.remove();
                }
            });
        });
    });

    // ─── Live Capacity Check (AJAX) ──────────────────────────────────────────
    const eventSelect = document.getElementById('event-select');
    const capacityInfo = document.getElementById('capacity-info');

    if (eventSelect && capacityInfo) {
        eventSelect.addEventListener('change', function () {
            const eventId = this.value;

            if (!eventId) {
                capacityInfo.innerHTML = '';
                capacityInfo.style.display = 'none';
                return;
            }

            fetch('/api/event/' + eventId + '/stats')
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {
                    if (data.error) {
                        capacityInfo.innerHTML = '<span style="color: var(--danger);">Event not found.</span>';
                    } else {
                        const percentage = Math.round((data.confirmed / data.capacity) * 100);
                        let barColor = 'var(--primary)';
                        if (percentage > 80) barColor = 'var(--warning)';
                        if (percentage >= 100) barColor = 'var(--danger)';

                        capacityInfo.innerHTML = `
                            <div style="margin-top: 0.5rem; padding: 0.75rem; background: var(--primary-light); border-radius: var(--radius);">
                                <strong>${data.confirmed}</strong> of <strong>${data.capacity}</strong> places filled
                                (${data.available} available)
                                <div style="margin-top: 0.5rem; background: var(--border); border-radius: 10px; height: 8px; overflow: hidden;">
                                    <div style="width: ${percentage}%; background: ${barColor}; height: 100%; border-radius: 10px; transition: width 0.5s ease;"></div>
                                </div>
                            </div>
                        `;
                        capacityInfo.style.display = 'block';
                    }
                })
                .catch(function (err) {
                    capacityInfo.innerHTML = '<span style="color: var(--danger);">Could not load capacity data.</span>';
                    capacityInfo.style.display = 'block';
                });
        });
    }

    // ─── Form Validation Feedback ─────────────────────────────────────────────
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            let valid = true;
            const requiredFields = form.querySelectorAll('[required]');

            requiredFields.forEach(function (field) {
                // Remove previous error styling
                field.style.borderColor = '';

                if (!field.value.trim()) {
                    field.style.borderColor = 'var(--danger)';
                    valid = false;
                }
            });

            // Email validation
            const emailField = form.querySelector('input[type="email"]');
            if (emailField && emailField.value) {
                const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailPattern.test(emailField.value)) {
                    emailField.style.borderColor = 'var(--danger)';
                    valid = false;
                }
            }

            if (!valid) {
                e.preventDefault();
                // Show a brief message
                let msg = form.querySelector('.js-validation-msg');
                if (!msg) {
                    msg = document.createElement('div');
                    msg.className = 'flash flash-error js-validation-msg';
                    msg.textContent = 'Please fill in all required fields correctly.';
                    form.prepend(msg);
                }
                // Auto-remove after 4 seconds
                setTimeout(function () {
                    if (msg) msg.remove();
                }, 4000);
            }
        });
    });

    // ─── Event Stats Dashboard (Home Page) ────────────────────────────────────
    const statsContainer = document.getElementById('event-stats-dashboard');
    if (statsContainer) {
        const eventId = statsContainer.getAttribute('data-event-id');
        if (eventId) {
            fetch('/api/event/' + eventId + '/stats')
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {
                    if (!data.error) {
                        statsContainer.innerHTML = `
                            <div class="stats-grid">
                                <div class="stat-item">
                                    <div class="stat-number">${data.capacity}</div>
                                    <div class="stat-label">Total Capacity</div>
                                </div>
                                <div class="stat-item">
                                    <div class="stat-number">${data.confirmed}</div>
                                    <div class="stat-label">Confirmed</div>
                                </div>
                                <div class="stat-item">
                                    <div class="stat-number">${data.available}</div>
                                    <div class="stat-label">Available</div>
                                </div>
                                <div class="stat-item">
                                    <div class="stat-number">${data.cancelled}</div>
                                    <div class="stat-label">Cancelled</div>
                                </div>
                            </div>
                        `;
                    }
                })
                .catch(function (err) {
                    statsContainer.innerHTML = '<p style="color: var(--text-light);">Could not load statistics.</p>';
                });
        }
    }

});
