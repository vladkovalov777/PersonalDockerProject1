from apps.core.base_crud import BaseCRUDManager
from apps.products.models import Product


class ProductCRUDManager(BaseCRUDManager):
    def __init__(self):
        self.model = Product


product_manager = ProductCRUDManager()