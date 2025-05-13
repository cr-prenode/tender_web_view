import requests
import json

# ChromaDB API endpoint
CHROMADB_URL = 'http://localhost:8000'

def fetch_all_collections():
    """Fetch all collections from ChromaDB and display them."""
    try:
        response = requests.get(f'{CHROMADB_URL}/collections')
        response.raise_for_status()
        collections = response.json()
        
        if collections:
            print(f"Found {len(collections)} collections:")
            for collection in collections:
                print(f"- Collection ID: {collection.get('id')}, Name: {collection.get('name')}")
        else:
            print("No collections found.")
    
    except requests.RequestException as e:
        print(f"Error fetching collections: {e}")

def fetch_collection_data(collection_id):
    """Fetch data from a specific collection by its ID."""
    try:
        response = requests.get(f'{CHROMADB_URL}/collections/{collection_id}/items')
        response.raise_for_status()
        items = response.json()
        
        if items:
            print(f"Data for Collection {collection_id}:")
            print(json.dumps(items, indent=4))
        else:
            print("No data found in this collection.")
    
    except requests.RequestException as e:
        print(f"Error fetching collection data: {e}")

if __name__ == '__main__':
    print("Fetching all collections from ChromaDB...")
    fetch_all_collections()
    
    collection_id = input("\nEnter the Collection ID to fetch its contents (or press Enter to skip): ")
    if collection_id:
        fetch_collection_data(collection_id)