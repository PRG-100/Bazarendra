# Bazarendra (Simple Django E‑commerce)

A minimal e‑commerce site for Nepali local products.
Backend: **Django (SQLite)** • Frontend: **HTML + CSS** • Primary color: **#55a656**

## Quick Start
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

# (Optional) create an admin user to add products
python manage.py createsuperuser

# Load sample products
python manage.py loaddata sample_products.json

# Run the dev server
python manage.py runserver
```

Visit http://127.0.0.1:8000/ for the shop and http://127.0.0.1:8000/admin/ for admin.
In admin, add/edit products. Cart uses sessions (no login required). Checkout creates an Order and OrderItems.

## Notes
- Payments are not integrated; checkout just stores an order.
- Static files are served from `/static/` in development.
- This code is intentionally simple for learning/demo purposes.
