import json
import os

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_PATH = os.path.join(BASE_DIR, "inventory.json")


def load_inventory():
    if not os.path.exists(INVENTORY_PATH):
        return {}

    with open(INVENTORY_PATH, encoding="utf-8") as inventory_file:
        data = json.load(inventory_file)

    if not isinstance(data, dict):
        return {}
    return data


def save_inventory(inventory):
    with open(INVENTORY_PATH, "w", encoding="utf-8") as inventory_file:
        json.dump(inventory, inventory_file, indent=4)
        inventory_file.write("\n")


def find_color(inventory, color_code):
    for saved_code in inventory:
        if saved_code.lower() == color_code.lower():
            return saved_code
    return None


def parse_quantity(value):
    try:
        quantity = int(value)
    except (ValueError, TypeError):
        return None, "Quantity must be a whole number."

    if quantity < 0:
        return None, "Quantity cannot be below 0."

    return quantity, None


@app.route("/")
def inventory_page():
    inventory = load_inventory()
    return render_template("inventory.html", inventory=inventory)


@app.route("/add", methods=["GET", "POST"])
def add_color():
    error = None
    color_code = ""
    quantity = ""

    if request.method == "POST":
        color_code = request.form.get("color_code", "").strip()
        quantity = request.form.get("quantity", "").strip()
        inventory = load_inventory()
        quantity_value, quantity_error = parse_quantity(quantity)

        if color_code == "":
            error = "Color code cannot be empty."
        elif find_color(inventory, color_code) is not None:
            error = "That color code already exists."
        elif quantity_error is not None:
            error = quantity_error
        else:
            inventory[color_code] = quantity_value
            save_inventory(inventory)
            return redirect(url_for("inventory_page"))

    return render_template(
        "add_color.html",
        error=error,
        color_code=color_code,
        quantity=quantity,
    )


@app.route("/update", methods=["GET", "POST"])
def update_quantity():
    inventory = load_inventory()
    color_code = request.values.get("color_code", "").strip()
    saved_code = find_color(inventory, color_code)

    if saved_code is None:
        return redirect(url_for("inventory_page"))

    error = None
    direct_quantity = ""
    new_quantity = inventory[saved_code]

    if request.method == "POST":
        direct_quantity = request.form.get("direct_quantity", "").strip()
        adjusted_quantity = request.form.get("new_quantity", "").strip()
        chosen = direct_quantity if direct_quantity != "" else adjusted_quantity
        quantity_value, quantity_error = parse_quantity(chosen)

        if quantity_error is not None:
            error = quantity_error
            if chosen != "":
                new_quantity = chosen
        else:
            inventory[saved_code] = quantity_value
            save_inventory(inventory)
            return redirect(url_for("inventory_page"))

    return render_template(
        "update_quantity.html",
        color_code=saved_code,
        current_quantity=inventory[saved_code],
        new_quantity=new_quantity,
        direct_quantity=direct_quantity,
        error=error,
    )


if __name__ == "__main__":
    app.run(debug=True)
