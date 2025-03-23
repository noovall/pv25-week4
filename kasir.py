import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic

class KasirApp(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("kasir.ui", self)

        self.produk_harga = {
            "Tahu": 2000,
            "Tempe": 4000,
            "Ikan": 10000
        }

        self.btnAdd.clicked.connect(self.tambah_ke_keranjang)
        self.btnClr.clicked.connect(self.clear_keranjang)

    def tambah_ke_keranjang(self):
        produk_text = self.comboBoxProduk.currentText()
        jumlah_text = self.lineEditJumlah.text().strip()
        diskon_text = self.comboBoxDiskon.currentText().replace("%", "").strip()

        if not jumlah_text.isdigit() or int(jumlah_text) <= 0:
            QMessageBox.warning(self, "Error", "Masukkan jumlah yang valid!")
            return

        jumlah = int(jumlah_text)

        if not diskon_text.isdigit():
            QMessageBox.warning(self, "Error", "Diskon tidak valid!")
            return

        diskon = int(diskon_text)

        produk = produk_text.split(" (")[0]

        if produk not in self.produk_harga:
            QMessageBox.warning(self, "Error", "Produk tidak valid!")
            return

        harga_satuan = self.produk_harga[produk]
        total_harga = jumlah * harga_satuan
        total_harga -= total_harga * (diskon / 100)
        total_harga = int(total_harga)

        self.textBrowser.append(f"{produk} x {jumlah} = Rp. {total_harga:,}")

        self.update_total()

    def update_total(self):
        total = 0
        for line in self.textBrowser.toPlainText().split("\n"):
            if "= Rp." in line:
                try:
                    harga_str = line.split("= Rp.")[-1].replace(",", "").strip()
                    harga = int(harga_str)
                    total += harga
                except ValueError:
                    continue 

        self.labelTotal.setText(f"Total Rp. {total:,}")

    def clear_keranjang(self):
        self.textBrowser.clear()
        self.labelTotal.setText("Total Rp. 0")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KasirApp()
    window.show()
    sys.exit(app.exec_())
