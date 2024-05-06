import sys
import json
import base64
import psutil
import secrets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QInputDialog, QComboBox
from PyQt5.QtCore import Qt

class UrunTakipSistemi(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ürün Takip Sistemi")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.urun_ad_label = QLabel("Ürün Adı:")
        self.urun_ad_input = QLineEdit()
        self.fiyat_label = QLabel("Fiyatı:")
        self.fiyat_input = QLineEdit()
        self.yang_label = QLabel("Yang:")
        self.yang_input = QLineEdit()
        self.durum_label = QLabel("Durum:")
        self.durum_combobox = QComboBox()
        self.durum_combobox.addItems(["Satıldı", "Satılmadı"])

        self.ekle_button = QPushButton("Ekle")
        self.ekle_button.clicked.connect(self.urun_ekle)

        self.urun_layout = QHBoxLayout()
        self.urun_layout.addWidget(self.urun_ad_label)
        self.urun_layout.addWidget(self.urun_ad_input)
        self.urun_layout.addWidget(self.fiyat_label)
        self.urun_layout.addWidget(self.fiyat_input)
        self.urun_layout.addWidget(self.yang_label)
        self.urun_layout.addWidget(self.yang_input)
        self.urun_layout.addWidget(self.durum_label)
        self.urun_layout.addWidget(self.durum_combobox)
        self.urun_layout.addWidget(self.ekle_button)

        self.layout.addLayout(self.urun_layout)

        self.tablo = QTableWidget()
        self.tablo.setColumnCount(6)
        self.tablo.setHorizontalHeaderLabels(["Ürün Adı", "Fiyatı", "Yang", "Durum", "", ""])
        self.layout.addWidget(self.tablo)

        self.toplam_label = QLabel()
        self.layout.addWidget(self.toplam_label)

        self.bellek_button = QPushButton("Bellek Tüketimini Göster")
        self.bellek_button.clicked.connect(self.bellek_kullanimini_goster)
        self.layout.addWidget(self.bellek_button)

        self.veriyi_yukle()

    def veriyi_yukle(self):
        try:
            with open('urunler.json', 'r') as dosya:
                self.veri = json.load(dosya)
                self.tabloyu_doldur()
        except FileNotFoundError:
            self.veri = []

    def veriyi_kaydet(self):
        with open('urunler.json', 'w') as dosya:
            json.dump(self.veri, dosya, separators=(',', ':'))

    def tabloyu_doldur(self):
        self.tablo.setRowCount(len(self.veri))
        toplam_fiyat = 0
        toplam_yang = 0
        for satir, urun in enumerate(self.veri):
            ad_item = QTableWidgetItem(self.base64_coz(self.veri[satir]['ad'], self.veri[satir]['urun_kodu']))
            fiyat_item = QTableWidgetItem(self.base64_coz(self.veri[satir]['fiyat'], self.veri[satir]['urun_kodu']))
            yang_item = QTableWidgetItem(self.base64_coz(self.veri[satir]['yang'], self.veri[satir]['urun_kodu']))
            durum_item = QTableWidgetItem(self.base64_coz(self.veri[satir]['durum'], self.veri[satir]['urun_kodu']))

            self.tablo.setItem(satir, 0, ad_item)
            self.tablo.setItem(satir, 1, fiyat_item)
            self.tablo.setItem(satir, 2, yang_item)
            self.tablo.setItem(satir, 3, durum_item)

            duzenle_button = QPushButton("Düzenle")
            duzenle_button.clicked.connect(lambda _, satir=satir: self.urun_duzenle(satir))
            self.tablo.setCellWidget(satir, 4, duzenle_button)

            kaldır_button = QPushButton("Kaldır")
            kaldır_button.clicked.connect(lambda _, satir=satir: self.urun_kaldir(satir))
            self.tablo.setCellWidget(satir, 5, kaldır_button)

            toplam_fiyat += float(self.base64_coz(self.veri[satir]['fiyat'], self.veri[satir]['urun_kodu']))
            toplam_yang += float(self.base64_coz(self.veri[satir]['yang'], self.veri[satir]['urun_kodu']))

        self.toplam_label.setText(f"Toplam Fiyat: {self.format_toplam(toplam_fiyat)} - Toplam Yang: {self.format_toplam(toplam_yang)}")

    def urun_ekle(self):
        urun_ad = self.urun_ad_input.text()
        fiyat = self.fiyat_input.text()
        yang = self.yang_input.text()
        durum = self.durum_combobox.currentText()

        if urun_ad and fiyat:
            try:
                float_fiyat = float(fiyat)
                float_yang = float(yang)
                if float_fiyat >= 0 and float_yang >= 0:
                    urun_kodu = secrets.token_hex(16)
                    self.veri.append({"ad": self.base64_yap(urun_ad, urun_kodu),
                                      "fiyat": self.base64_yap(fiyat, urun_kodu),
                                      "yang": self.base64_yap(yang, urun_kodu),
                                      "durum": self.base64_yap(durum, urun_kodu),
                                      "urun_kodu": urun_kodu})
                    self.veriyi_kaydet()
                    self.tabloyu_doldur()
                    self.urun_ad_input.clear()
                    self.fiyat_input.clear()
                    self.yang_input.clear()
                else:
                    QMessageBox.warning(self, "Uyarı", "Fiyat ve Yang sıfırdan büyük olmalıdır.")
            except ValueError:
                QMessageBox.warning(self, "Uyarı", "Fiyat ve Yang alanlarına sadece rakam girilmelidir.")
        else:
            QMessageBox.warning(self, "Uyarı", "Ürün adı, fiyat ve yang giriniz.")

    def urun_duzenle(self, satir):
        urun = self.veri[satir]
        eski_ad = urun["ad"]
        eski_fiyat = self.base64_coz(urun["fiyat"], urun["urun_kodu"])
        eski_yang = self.base64_coz(urun["yang"], urun["urun_kodu"])
        eski_durum = self.base64_coz(urun["durum"], urun["urun_kodu"])

        urun_ad, ok1 = QInputDialog.getText(self, "Ürün Adı", "Ürün Adı:", text=self.base64_coz(urun["ad"], urun["urun_kodu"]))
        fiyat, ok2 = QInputDialog.getDouble(self, "Fiyatı", "Fiyatı:", value=float(eski_fiyat))
        yang, ok3 = QInputDialog.getText(self, "Yang", "Yang:", text=eski_yang)
        durum, ok4 = QInputDialog.getItem(self, "Durum", "Durum:", ["Satıldı", "Satılmadı"], current=0 if eski_durum == "Satıldı" else 1)

        if ok1 or ok2 or ok3 or ok4:
            try:
                if ok1:
                    urun["ad"] = self.base64_yap(urun_ad, urun["urun_kodu"])
                if ok2:
                    float_fiyat = float(fiyat)
                    if float_fiyat >= 0:
                        urun["fiyat"] = self.base64_yap(str(fiyat), urun["urun_kodu"])
                    else:
                        QMessageBox.warning(self, "Uyarı", "Fiyat sıfırdan büyük olmalıdır.")
                        return
                if ok3:
                    float_yang = float(yang)
                    if float_yang >= 0:
                        urun["yang"] = self.base64_yap(yang, urun["urun_kodu"])
                    else:
                        QMessageBox.warning(self, "Uyarı", "Yang sıfırdan büyük olmalıdır.")
                        return
                if ok4:
                    urun["durum"] = self.base64_yap(durum, urun["urun_kodu"])

                self.veriyi_kaydet()
                self.tabloyu_doldur()
            except ValueError:
                QMessageBox.warning(self, "Uyarı", "Fiyat ve Yang alanlarına sadece rakam girilmelidir.")
        else:
            urun["ad"] = eski_ad

            self.veriyi_kaydet()
            self.tabloyu_doldur()

    def urun_kaldir(self, satir):
        del self.veri[satir]
        self.veriyi_kaydet()
        self.tabloyu_doldur()

    def base64_coz(self, veri, urun_kodu):
        return base64.b64decode(veri).decode('utf-8').replace(urun_kodu, '')

    def base64_yap(self, veri, urun_kodu):
        return base64.b64encode((veri + urun_kodu).encode('utf-8')).decode('utf-8')

    def format_toplam(self, deger):
        return "{:,.2f}".format(deger).replace(",", ".")

    def bellek_kullanimini_goster(self):
        bellek_kullanimi = psutil.Process().memory_info().rss / (1024 ** 2)
        QMessageBox.information(self, "Bellek Kullanımı", f"Bellek Kullanımı: {bellek_kullanimi:.2f} MB")

uygulama = QApplication(sys.argv)
pencere = UrunTakipSistemi()
pencere.show()
sys.exit(uygulama.exec_())
