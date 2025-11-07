import frappe
import requests

@frappe.whitelist()
def fetch_articles():
    url = "http://localsite.localhost:8000/api/method/library_management.api.article.get_articles"
    response = requests.get(url)
    
    if response.status_code == 200:
        articles = response.json().get("message", [])
        return("Fetched Articles:", articles)
    else:
        return("Error:", response.text)

