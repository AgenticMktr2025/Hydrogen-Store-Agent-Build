import reflex as rx


class ShopifyService:
    def validate_credentials(self, domain: str, token: str) -> bool:
        return True

    def test_storefront_api(self, domain: str, token: str) -> bool:
        return True

    def get_store_info(self, domain: str, token: str) -> dict:
        return {"name": "Mock Store", "currency": "USD"}