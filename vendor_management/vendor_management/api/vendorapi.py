import frappe
from frappe import auth

# this code for when, we login and and want that authentication inside the pages
@frappe.whitelist(allow_guest=True)
def login(usr, pwd):
    try:
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(user=usr, pwd=pwd)
        login_manager.post_login()
    except frappe.exceptions.AuthenticationError:
        frappe.clear_messages()
        frappe.response["message"] = {
            "success_key": 0,
            "message": "Authentication Error!"
        }
        return
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Login Failed")
        frappe.response["message"] = {
            "success_key": 0,
            "message": "Login failed due to server error."
        }
        return

    api_generate = generate_keys(frappe.session.user)
    user = frappe.get_doc('User', frappe.session.user)

    frappe.response["message"] = {
        "success_key": 1,
        "message": "Authentication success",
        "sid": frappe.session.sid,
        "api_key": user.api_key,
        "api_secret": api_generate,
        "username": user.username,
        "email": user.email
    }

#To generate keys
def generate_keys(user):
    user_details = frappe.get_doc('User', user)

    if not user_details.api_key:
        user_details.api_key = frappe.generate_hash(length=15)

    if not user_details.api_secret:
        user_details.api_secret = frappe.generate_hash(length=15)

    user_details.save()

    return user_details.api_secret

# Retrieving vendors data from db using get api
@frappe.whitelist()
def get_vendors():
    # Your custom logic here
    data = frappe.frappe.db.get_all('Vendor', fields={"vendor_name","address"})
    return data

# Creating vendors on db using post(insert) api
@frappe.whitelist()
def create_user():
    doc = frappe.get_doc({
      'doctype': 'Vendor',
      'vendor_name': 'Rame',
      'dob': '',    
      'address': 'Ramechhap',
      'gender': 'Male',
      'business_type': 'Electronics'
    })
    doc.insert()
    frappe.db.commit()
    return "User added"

# deleting vendor data from db using delete api
@frappe.whitelist(allow_guest=True)
def delete_user():
    frappe.db.delete("Vendor",{"address": 'kln'})
    return "Deletes vendor!"

# editing vendor data from db using put(set_value) api
@frappe.whitelist(allow_guest=True)
def edit_user():
    frappe.db.set_value('Vendor', 'V-0002', {
    'vendor_name': 'Sita',
    'address': 'Lalitpur'
    })
    return "Vendor edited"

#getting orders of sepecific vendor using join query
@frappe.whitelist()
def orders_status(name):
    
    if (frappe.db.exists("Vendor", {"name": name})):
        sql_query = """SELECT v.vendor_name, o.completed_order, o.high_valued_order, o.pending_order, o.canceled_order """ \
                    """FROM tabVendor v JOIN tabOrder_que o ON v.name = o.id WHERE v.name = %s ;"""
        
        order_status = frappe.db.sql(sql_query, values=name, as_dict=True)
        return order_status
    else:
        return f"Vendor {name} not found"

#ordering vendors basde on the highest completed orders
@frappe.whitelist(allow_guest=True)
def top_vendors():
    sql_query = """SELECT v.vendor_name, o.completed_order """\
                """FROM tabVendor v JOIN tabOrder_que o ON v.name = o.id """\
                """ORDER BY o.completed_order DESC LIMIT 5;"""
    top_vendors = frappe.db.sql(sql_query, as_dict=True)
    return top_vendors

# getting total number of vendors
@frappe.whitelist(allow_guest=True)
def total_vendors():
    total = frappe.db.count('Vendor')
    return {"total_vendors": total}

