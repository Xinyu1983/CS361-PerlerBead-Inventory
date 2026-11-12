# Perler Bead Inventory

A local website for keeping track of Perler bead colors and how many beads you have. The site is a Flask app. Bead colors and quantities are stored in `inventory.json`.

This is Milestone #1. It covers three tasks: add a bead color, view the inventory, and update a quantity.

## Run the website

Use Python 3.9 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000).

## What you can do

- View every saved color code and quantity on the Inventory page.
- Add a bead color with a starting quantity.
- Change a quantity with the + and - buttons, or type the final quantity yourself.
- Cancel either form to leave the saved inventory unchanged.

The inventory is saved in `inventory.json`. After adding or updating a bead color, the changes will still be there when the page is refreshed.

The Inventory page shows “Page loaded in X seconds.” after it finishes loading. That time should stay under 5 seconds.
