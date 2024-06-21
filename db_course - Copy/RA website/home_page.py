from flask import Flask, render_template, request
import pandas as pd
from pathlib import Path
import sqlite3

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('home_page.html')

@app.route('/customers', methods=['GET', 'POST'])
def customers():
    if request.method == 'POST':
        # Read the form data
        emp_id = request.form.get('employee_id')

        # Use pathlib to construct the database file path
        db_file = Path(__file__).resolve().parent.parent / "retail_app"

        # Connect to the database
        conn = sqlite3.connect(db_file)

        # Use Pandas to retrieve the employee information from the employee table
        query = "SELECT * FROM employee WHERE employee_id=?"
        df = pd.read_sql_query(query, conn, params=(emp_id,))

        # Close the database connection
        conn.close()

        if df.empty:
            message = f'Employee with ID {emp_id} does not exist.'
            return render_template('customers.html', employee_info=message)
        else:
            # Convert DataFrame to a list of dictionaries for easy rendering in the template
            employee_info = df.to_html(index=False)
            return render_template('customers.html', employee_info=employee_info)
    else:
        return render_template('customers.html')

@app.route('/products', methods=['GET', 'POST'])
def products():
    # Render the template with the initial form
    return render_template('products.html')

@app.route('/get_products', methods=['GET', 'POST'])
def get_products():
    if request.method == 'POST':
        id = request.form.get('product_id')

        current_dir = Path(__file__).parent
        parent_dir = current_dir.parent

        db_file = parent_dir / "retail_app"

        # connect to the database
        conn = sqlite3.connect(db_file)
        
        query = "SELECT * FROM product where product_id=?"
        
        df = pd.read_sql_query(query, conn, params=(id,))
        conn.close()

        if len(df) == 0:
            message = 'Product with ID {id} does not exist.'.format(id)
            return render_template('get_products.html', product_info=message)
        else:
            product_info = df.to_html(index=False)
            return render_template('get_products.html', product_info=product_info)
    # Render the template with the initial form
    return render_template('get_products.html')

@app.route('/get_customers', methods=['GET', 'POST'])
def get_customers():
    if request.method == 'POST':
        # Read the form data
        customer_first_name = request.form.get('customer_first_name')
        customer_last_name = request.form.get('customer_last_name')
        customer_gender = request.form.get('customer_gender')
        customer_dob = request.form.get('customer_dob')

        # File paths
        current_dir = Path(__file__).parent
        parent_dir = current_dir.parent
        db_file = parent_dir / "retail_app"

        # Connect to the database
        conn = sqlite3.connect(db_file)

        # Use Pandas to retrieve the maximum customer_id from the customer table
        query = "SELECT MAX(customer_id) FROM customer"
        max_customer_id = pd.read_sql_query(query, conn).iloc[0, 0]

        # If the table is empty, start with customer_id = 1
        if pd.isnull(max_customer_id):
            customer_id = 1
        else:
            customer_id = max_customer_id + 1

        # Create a DataFrame with the new record
        new_customer = pd.DataFrame({
            'customer_id': [customer_id],
            'customer_first_name': [customer_first_name],
            'customer_last_name': [customer_last_name],
            'customer_gender': [customer_gender],
            'customer_dob': [customer_dob]
        })

        # Use Pandas to insert the new record into the customer table
        new_customer.to_sql('customer', conn, if_exists='append', index=False)

        # Commit the transaction and close the database connection
        conn.commit()
        conn.close()

        # Return a response to the user
        return '<h1>Success</h1>The customer record has been successfully added to the database.'
    # Render the template with the initial form
    return render_template('get_customers.html')

if __name__ == '__main__':
    app.run(debug=True)
