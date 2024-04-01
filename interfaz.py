import tkinter as tk
import requests

class InterfazGrafica(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Pedidos de Platos Gratis")

        self.btn_pedir_plato = tk.Button(self, text="Pedir Plato", command=self.pedir_plato)
        self.btn_pedir_plato.pack()

        self.lista_ordenes = tk.Listbox(self)
        self.lista_ordenes.pack()

        self.lbl_ingredientes = tk.Label(self, text="Ingredientes disponibles en la bodega de alimentos:")
        self.lbl_ingredientes.pack()

        self.lbl_historial_compras = tk.Label(self, text="Historial de compras en la plaza de alimentos:")
        self.lbl_historial_compras.pack()

        self.lbl_historial_pedidos = tk.Label(self, text="Historial de pedidos realizados a la cocina:")
        self.lbl_historial_pedidos.pack()

        self.lbl_recetas = tk.Label(self, text="Recetas con ingredientes y cantidades:")
        self.lbl_recetas.pack()

        self.actualizar_datos()

    def pedir_plato(self):
        response = requests.get('http://localhost:5000/mesero/recibir_plato')
        if response.status_code == 200:
            self.lista_ordenes.insert(tk.END, "Nuevo pedido de plato")

    def actualizar_datos(self):
        response_bodega = requests.get('http://localhost:5000/bodega/consultar')
        if response_bodega.status_code == 200:
            ingredientes = response_bodega.json()
            self.lbl_ingredientes.config(text="Ingredientes disponibles en la bodega de alimentos:\n" + str(ingredientes))

        response_compras = requests.get('http://localhost:5000/marketplace')
        if response_compras.status_code == 200:
            historial_compras = response_compras.json()
            self.lbl_historial_compras.config(text="Historial de compras en la plaza de alimentos:\n" + str(historial_compras))

        response_recetas = requests.get('http://localhost:5000/cocina/recetas')
        if response_recetas.status_code == 200:
            recetas = response_recetas.json()
            self.lbl_recetas.config(text="Recetas con ingredientes y cantidades:\n" + str(recetas))

        self.after(10000, self.actualizar_datos)

if __name__ == "__main__":
    app = InterfazGrafica()
    app.mainloop()
