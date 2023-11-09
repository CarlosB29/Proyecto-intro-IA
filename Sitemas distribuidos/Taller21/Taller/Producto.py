import pickle

class Producto:
    def __init__(self, name, category, precio):
        self.name = name
        self.category = category
        self.precio = precio

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_category(self):
        return self.category

    def set_category(self, category):
        self.category = category

    def get_precio(self):
        return self.precio

    def set_precio(self, precio):
        self.precio = precio

if __name__ == '__main__':
    # Puedes agregar aquí un ejemplo para probar la clase Producto si lo deseas
    pass
