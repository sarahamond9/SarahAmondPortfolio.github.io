# Sarah Amond
import json
import os
import matplotlib.pyplot as plt

# File to store data so it saves even when you close the program
DATA_FOLDER = os.environ.get("APPDATA", os.path.expanduser("~"))
DATA_FILE = os.path.join(DATA_FOLDER, "my_personal_expenses.json")


def load_expenses():
    """Loads expenses from a JSON file, or creates an empty dict if the file doesn't exist."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def save_expenses(expenses):
    """Saves the current expenses dictionary back to the JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)

def add_expense(expenses):
    """Prompts user for expense details and adds it to the tracking data."""
    print("\n--- Add New Expense ---")
    
    # 1. Get and validate amount
    while True:
        try:
            amount = float(input("Enter amount spent (€): "))
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    # 2. Select category
    categories = ["Food", "Transport", "Entertainment", "Bills", "Shopping", "Other"]
    print("\nAvailable Categories:")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
        
    while True:
        try:
            choice = int(input("Select category number: "))
            if 1 <= choice <= len(categories):
                category = categories[choice - 1]
                break
            print(f"Please select a number between 1 and {len(categories)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    description = input("Enter a brief description (optional): ").strip()

    # Create the expense item entry
    expense_item = {
        "amount": amount,
        "description": description if description else "No description"
    }

    # Group under the chosen category array
    if category not in expenses:
        expenses[category] = []
    
    expenses[category].append(expense_item)
    save_expenses(expenses)
    print(f"✅ Successfully added {amount} to {category}!")

def show_summary(expenses):
    """Calculates and displays textual summary of totals per category."""
    print("\n--- Expense Summary ---")
    if not expenses:
        print("No expenses recorded yet.")
        return

    total_overall = 0
    for category, items in expenses.items():
        category_total = sum(item["amount"] for item in items)
        total_overall += category_total
        print(f"📌 {category}: Total spent: {category_total:.2f}")
    
    print(f"\n💰 Grand Total Spent: {total_overall:.2f}")

def generate_pie_chart(expenses):
    """Generates a visual pie chart of spending categories using matplotlib."""
    if not expenses:
        print("\n⚠️ No data available to generate a chart. Add some expenses first!")
        return

    labels = []
    sizes = []

    # Calculate totals per category for the chart metrics
    for category, items in expenses.items():
        category_total = sum(item["amount"] for item in items)
        labels.append(category)
        sizes.append(category_total)

    # Plotting configuration
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, shadow=True)
    plt.title("Personal Spending Breakdown by Category")
    
    print("\n📊 Opening chart window... (Close the chart window to return to menu)")
    plt.show()

def main():
    expenses = load_expenses()

    while True:
        print("\n==============================")
        print("      EXPENSE TRACKER MENU    ")
        print("==============================")
        print("1. Add an Expense")
        print("2. View Expense Summary (Text)")
        print("3. View Visual Spending Chart (Pie Chart)")
        print("4. Exit")
        
        choice = input("\nChoose an option (1-4): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_summary(expenses)
        elif choice == "3":
            generate_pie_chart(expenses)
        elif choice == "4":
            print("\nGoodbye! Happy budgeting!")
            break
        else:
            print("Invalid selection. Please choose options 1 through 4.")

if __name__ == "__main__":
    main()
