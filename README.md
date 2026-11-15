# QuickBite – Member 1: Shopping Cart

An independently runnable Flask shopping-cart application demonstrating the **Command Design Pattern**.

## Features
- Browse sample food items
- Add items and increase/decrease quantities
- Remove items
- Calculate subtotal
- Undo the most recent add/remove action
- Cart is stored in the Flask session (separate per browser session)

## Setup (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5001

## Run tests
```powershell
pytest -q
```

## Command Pattern mapping
- `Command`: abstract command interface
- `AddItemCommand`, `RemoveItemCommand`, `ChangeQuantityCommand`: concrete commands
- `CartInvoker`: invokes commands
- `Cart`: receiver that performs cart operations

This is a standalone academic demo. It does not process payments or persist orders to a database.
