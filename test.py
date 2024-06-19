from model.model import Model

myModel = Model()
myModel._creaGrafo(1, "2017", 0.6)
print(myModel.getGraphDetails())
myModel.prodotti_redditizzi()
cammino, lunghezzaCammino = myModel.cammino()
for c in cammino:
    print(c)
print(lunghezzaCammino)

