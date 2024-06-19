import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDAnno(self):
        anni = ["2015", "2016", "2017", "2018"]
        for a in anni:
            self._view._ddAnno.options.append(ft.dropdown.Option(data=a, text=a, on_click=self.selectAnno))
        self._view.update_page()

    def fillDDMetodi(self):
        metodi = self._model._metodi
        for m in metodi:
            self._view._ddMetodi.options.append(ft.dropdown.Option(data=m[0], text=m[1], on_click=self.selectMetodo))
        self._view.update_page()

    def selectAnno(self, e):
        if e.control.data is None:
            self._choiceAnno = None
        else:
            self._choiceAnno = e.control.data

    def selectMetodo(self, e):
        if e.control.data is None:
            self._choiceMetodo = None
        else:
            self._choiceMetodo = e.control.data

    def handle_graph(self, e):
        s = self._view._txtS.value
        try:
            floatS = float(s)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Errore valore S inserito non numerico"))
            self._view.update_page()
            return
        self._model._creaGrafo(self._choiceMetodo, self._choiceAnno, floatS)
        nNodi, nArchi = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato. "
                                                      f"Il grafo ha {nNodi} nodi e {nArchi} archi."))
        self._view.update_page()

    def handle_prodotti_redditizzi(self, e):
        prodotti = self._model.prodotti_redditizzi()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("I prodotti più redditizzi sono"))
        for p in prodotti:
            self._view.txt_result.controls.append(ft.Text(f"Prodotto {p[0]}, archi entranti {p[1]}"))
        self._view.update_page()

    def handle_cammino(self, e):
        cammino, lunghezza_cammino = self._model.cammino()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Cammino massimo lungo {lunghezza_cammino} archi."))
        for c in cammino:
            self._view.txt_result.controls.append(ft.Text(f"{c[0]} ---> {c[1]}"))
        self._view.update_page()

