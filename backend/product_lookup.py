import requests

def get_product_info(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)
    data = response.json()

    if data["status"] == 1:
        product = data["product"]
        return {
            "name": product.get("product_name", "Unknown Product"),
            "shelf_life_days": 7
        }

    return None