# Module Import
import mariadb
import sys

# Adds account
def add_account(cur, first_name, last_name, email, amount):
   """Adds the given account to the accounts table"""

   cur.execute("INSERT INTO test.accounts(first_name, last_name, email, amount) VALUES (?, ?, ?, ?)",
      (first_name, last_name, email, amount))

# Update Last Name
def update_account_amount(cur, email, change):
   """Updates amount of an account in the table"""

   cur.execute("UPDATE test.accounts SET amount=(amount-?) WHERE email=?",
         (change, email))

# Instantiate Connection
try:
   conn = mariadb.connect(
      host="192.0.2.1",
      port=3306,
      user="db_user",
      password="USER_PASSWORD")

   cur = conn.cursor()

   new_account_fname = "John"
   new_account_lname = "Rockefeller"
   new_account_email = "john.rockefeller@example.com"
   new_account_amount = 418000000000.00

   add_account(cur,
      new_account_fname,
      new_account_lname,
      new_account_email,
      new_account_amount)

   new_account_change = 1000000.00

   update_account_amount(cur,
      new_account_email,
      new_account_change)

   conn.commit()
   conn.close()
except Exception as e:
   print(f"Error committing transaction: {e}")

   conn.rollback()