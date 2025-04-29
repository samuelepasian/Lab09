import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view:View, model:Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_analisiAerei(self,e):
        self._view.txt_result.clean()
        self._view.update_page()
        try:
            distanza_minima=int(self._view.txt_name.value)
            stringa=self._model.output_grafo(distanza_minima)
            self._view.txt_result.controls.append(ft.Text(stringa))
            self._view.update_page()
        except ValueError:
            self._view.create_alert("ERRORE")
            self._view.update_page()
