import requests
from flask import current_app

class APIService:
    @staticmethod
    def get_all(endpoint):
        url = f"{current_app.config['API_BASE_URL']}/{endpoint}"
        response = requests.get(url)
        return response.json() if response.ok else []
    
    @staticmethod
    def get_by_id(endpoint, id):
        url = f"{current_app.config['API_BASE_URL']}/{endpoint}/{id}"
        response = requests.get(url)
        return response.json() if response.ok else None
    
    @staticmethod
    def create(endpoint, data):
        url = f"{current_app.config['API_BASE_URL']}/{endpoint}"
        response = requests.post(url, json=data)
        return response.json() if response.ok else None
    
    @staticmethod
    def update(endpoint, id, data):
        url = f"{current_app.config['API_BASE_URL']}/{endpoint}/{id}"
        response = requests.put(url, json=data)
        return response.json() if response.ok else None
    
    @staticmethod
    def delete(endpoint, id):
        url = f"{current_app.config['API_BASE_URL']}/{endpoint}/{id}"
        response = requests.delete(url)
        return response.ok