"""
Examen: Gestión de Inventario con Persistencia JSON y Programación Orientada a Objetos
Autor/a: _______________________________________
Fecha: __________________________________________

Objetivo:
Desarrollar una aplicación orientada a objetos que gestione un inventario de productos
con persistencia de datos en ficheros JSON y uso de listas y diccionarios anidados.

Clases requeridas:
- Proveedor
- Producto
- Inventario

"""

import json
import os


# ======================================================
# Clase Proveedor
# ======================================================

class Proveedor:
    def __init__(self, codigo:str, nombre:str, contacto:str)->None:
        self.codigo=codigo
        self.nombre=nombre
        self.contacto=contacto

    def obtener_codigo_proveedor(self)->str:
        self.codigo

    def obtener_nombre_proveedor(self)->str:
        self.nombre
    
    def obtener_contacto_proveedor(self)->str:
        self.contacto
    
    def __str__(self)->str:
        return f"Codigo: {self.codigo}, Nombre: {self.nombre}, Contacto: {self.contacto}"

    def to_dict(self)->dict:
        return {
            "codigo":self.codigo,
            "nombre":self.nombre,
            "contacto":self.contacto
        }
    
    def from_dict(cls,datos:dict)->"Proveedor":
        return cls(datos["codigo"],datos["nombre"],datos["contacto"])

# ======================================================
# Clase Producto
# ======================================================

class Producto:
    def __init__(self, codigo:str, nombre:str, precio:float, stock:int,proveedor):
        self.codigo=codigo
        self.nombre=nombre
        self.precio=precio
        self.stock=stock
        self.proveedor=Proveedor
    
    def __str__(self)->str:
        return f"[{self.codigo}] {self.nombre} - {self.precio} ({self.stock} | Proveedor: {self.proveedor.obtener_nombre_proveedor(self)} ({self.proveedor.obtener_contacto_proveedor()}))"
        # Ejemplo: "[P001] Teclado - 45.99 € (10 uds.) | Proveedor: TechZone (ventas@techzone.com)"

    def to_dict(self)->dict:
        return {
            "codigo":self.codigo,
            "nombre":self.nombre,
            "precio":self.precio,
            "stock":self.stock,
            "proveedor":self.proveedor
        }
    
    def from_dict(cls,datos:dict)->"Producto":
        return cls(datos["codigo"],datos["nombre"],datos["precio"],datos["stock"],datos["proveedor"])

# ======================================================
# Clase Inventario
# ======================================================

class Inventario:
    def __init__(self, nombre_fichero:str)->None:
        self.productos:list[Producto]=[]
        self.nombre_fichero=nombre_fichero

    def cargar(self):
        fichero=self.nombre_fichero

        if not os.path.exists(fichero):
            print("El fichero no existe")
        try:
            with open(fichero,"r",encoding="UTF-8") as c:
                list_dict=json.load(c)
                self.productos=[Producto.from_dict(datos)for datos in list_dict]
        except Exception as e:
            print(f"Error: {e}")


    def guardar(self):
        fichero=self.nombre_fichero
        try:
            with open(fichero,"w",encoding="UTF-8") as f:
                diccionario=self.productos.__dict__()
                json.dump(diccionario,f,ensure_ascii=False)
        except Exception as e:
            print(f"Error: {e}")

    def buscar(self, codigo:str)->list[Producto]:
       return [prod for prod in self.productos if prod.codigo.lower()==codigo.lower()]

    def existe_producto(self,codigo)->bool:
        for prod in self.productos:
            if prod.codigo.lower()==codigo.lower():
                return True
            else:
                return False
            
    def anadir_producto(self, producto:Producto)->None:
        existe=self.existe_producto(producto.codigo)
        if existe:
            return print("El producto ya estaba en la lista")
        else:
            self.productos.append(producto)
            return print("Producto añadido")

    def mostrar(self)->None:
        for prod in self.productos:
            return print(prod)


    def modificar(self, codigo, nombre=None, precio=None, stock=None):
        existe=self.buscar(codigo)
        if existe:
            for prod in self.productos:
                if  prod.codigo.lower()==codigo:
                    prod.nombre=nombre
                    prod.precio=precio
                    prod.stock=stock
        else:
            return print("El producto no está en la lista")

    def eliminar(self, codigo:str)->None:
        existe=self.existe_producto(codigo)
        prod=self.buscar(codigo)
        if existe:
            producto=prod[0]
            self.productos.remove(producto)
            return print("Producto eliminado")
        else:
            return print("El producto no se ha encontrado")


    def valor_total(self)->int:
        return sum(prod.precio*prod.stock for prod in self.productos)
    
    def mostrar_por_proveedor(self, codigo_proveedor:str):
        for prod in self.productos:
            codigo_proveedor=prod.proveedor.obtener_codigo_proveedor()
            if (codigo_proveedor.lower()==codigo_proveedor.lower()):
                return print(prod.__str__())
        

# ======================================================
# Función principal (menú de la aplicación)
# ======================================================

def main():
    inventario=Inventario("inventario.json")
    inventario.cargar()
    while True:
        print("\n=== GESTIÓN DE INVENTARIO ===")
        print("1. Añadir producto")
        print("2. Mostrar inventario")
        print("3. Buscar producto")
        print("4. Modificar producto")
        print("5. Eliminar producto")
        print("6. Calcular valor total")
        print("7. Mostrar productos de un proveedor")
        print("8. Guardar y salir")

        opcion = int(input("Seleccione una opción: "))

        if opcion==1:
            codigo=input("Codigo producto: ")
            nombre=input("Nombre producto: ")
            precio=float(input("Precio producto: "))
            stock=int(input("Stock producto: "))
            codigo_prov=input("Codigo proveedor: ")
            nombre_prov=input("Nombre proveedor: ")
            contacto_prov=input("Contacto proveedor: ")
            
            producto=Producto(codigo,nombre,precio,stock,Proveedor(codigo_prov,nombre_prov,contacto_prov))
            
            inventario.anadir_producto(producto)
            
        
        elif opcion==2:
            
            inventario.mostrar()
            return

        elif opcion==3:
            codigo=input("Codigo  del producto:")
            inventario.buscar(codigo)
            
            
        
        elif opcion==4:
            codigo=input("Codigo producto: ")
            nombre=input("Nombre producto: ")
            precio=float(input("Precio producto: "))
            stock=int(input("Stock producto: "))
            
            inventario.modificar(codigo,nombre,precio,stock)
            
        
        elif opcion==5:
            codigo=input("Codigo producto: ")
            inventario.eliminar(codigo)
        
        elif opcion==6:
            res=inventario.valor_total()
            print(res)
            
        
        elif opcion==7:
            codigo_prov=input("Codigo proveedor: ")
            inventario.mostrar_por_proveedor(codigo_prov)
        
        elif opcion==8:
            inventario.guardar()
            print("Guardando.")
        
        else:
            print("Opcion incorrecta")

if __name__ == "__main__":
    main()
