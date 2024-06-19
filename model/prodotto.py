from dataclasses import dataclass

@dataclass
class Prodotto:
    product_number: int
    ricavi_tot: float


    def __hash__(self):
        return hash(self.product_number)

    def __str__(self):
        return f"{self.product_number} - Ricavi: {self.ricavi_tot}"

