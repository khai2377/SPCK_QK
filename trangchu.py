from PyQt6 import QtWidgets, QtCore

class CarManager(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản lý ô tô")
        

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        layout = QtWidgets.QVBoxLayout()

        # Form thêm ô tô
        form_layout = QtWidgets.QFormLayout()
        self.txt_bienso = QtWidgets.QLineEdit()

        self.cmb_hangxe = QtWidgets.QComboBox()
        self.cmb_hangxe.setEditable(True)
        self.cmb_hangxe.addItems(["Toyota", "Honda", "Ford", "Mazda", "Kia"])

        self.txt_namsx = QtWidgets.QSpinBox()
        self.txt_namsx.setRange(1990, 2050)

        self.txt_gia = QtWidgets.QLineEdit()

        self.cmb_trangthai = QtWidgets.QComboBox()
        self.cmb_trangthai.addItems(["Đang sử dụng", "Đã bán", "Hết hạn đăng kiểm"])

        form_layout.addRow("Biển số:", self.txt_bienso)
        form_layout.addRow("Hãng xe:", self.cmb_hangxe)
        form_layout.addRow("Năm SX:", self.txt_namsx)
        form_layout.addRow("Giá gốc:", self.txt_gia)
        form_layout.addRow("Trạng thái:", self.cmb_trangthai)

        btn_add = QtWidgets.QPushButton("Thêm ô tô")
        btn_add.clicked.connect(self.them_oto)

        btn_delete = QtWidgets.QPushButton("Xoá ô tô")
        btn_delete.clicked.connect(self.xoa_oto)

        btn_sell = QtWidgets.QPushButton("Bán ô tô")
        btn_sell.clicked.connect(self.ban_oto)

        layout.addLayout(form_layout)
        layout.addWidget(btn_add)
        layout.addWidget(btn_delete)
        layout.addWidget(btn_sell)

        # Lọc hãng xe
        self.cmb_filter_hang = QtWidgets.QComboBox()
        self.cmb_filter_hang.addItem("Tất cả hãng")
        self.cmb_filter_hang.currentTextChanged.connect(self.loc_theo_hang)
        layout.addWidget(QtWidgets.QLabel("Lọc theo hãng xe:"))
        layout.addWidget(self.cmb_filter_hang)

        # Bảng danh sách ô tô
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Biển số", "Hãng", "Năm SX", "Giá gốc", "Trạng thái", "Giá bán"])
        layout.addWidget(self.table)

        central_widget.setLayout(layout)

        self.data = []  # Danh sách ô tô, mỗi ô tô là tuple có thêm giá bán

    def them_oto(self):
        bien_so = self.txt_bienso.text()
        hang = self.cmb_hangxe.currentText()
        namsx = str(self.txt_namsx.value())
        gia = self.txt_gia.text()
        trangthai = "Đang sử dụng"  # Mặc định
        giaban = ""  # Chưa bán

        if not bien_so or not hang or not gia:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return

        oto = (bien_so, hang, namsx, gia, trangthai, giaban)
        self.data.append(oto)

        if hang not in [self.cmb_filter_hang.itemText(i) for i in range(self.cmb_filter_hang.count())]:
            self.cmb_filter_hang.addItem(hang)
        if hang not in [self.cmb_hangxe.itemText(i) for i in range(self.cmb_hangxe.count())]:
            self.cmb_hangxe.addItem(hang)

        self.hien_thi_du_lieu()

        

    def xoa_oto(self):
        selected = self.table.currentRow()
        if selected >= 0:
            del self.data[selected]
            self.hien_thi_du_lieu()
        else:
            QtWidgets.QMessageBox.warning(self, "Chưa chọn", "Vui lòng chọn dòng để xoá.")

    def ban_oto(self):
        selected = self.table.currentRow()
        if selected < 0:
         QtWidgets.QMessageBox.warning(self, "Chưa chọn", "Vui lòng chọn xe để bán.")
         return

        oto = list(self.data[selected])

        if oto[4] == "Đã bán":
            QtWidgets.QMessageBox.information(self, "Thông báo", "Xe này đã được bán rồi.")
            return

        giaban, ok = QtWidgets.QInputDialog.getText(self, "Nhập giá bán", "Giá bán thực tế:")
        if ok and giaban:
            oto[4] = "Đã bán"   # cập nhật trạng thái
            oto[5] = giaban     # cập nhật giá bán
            self.data[selected] = tuple(oto)  # lưu lại vào danh sách
            self.hien_thi_du_lieu()
        elif ok:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Giá bán không được để trống.")


    def hien_thi_du_lieu(self, filter_hang="Tất cả hãng"):
        self.table.setRowCount(0)
        for oto in self.data:
            if filter_hang != "Tất cả hãng" and oto[1] != filter_hang:
                continue
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, value in enumerate(oto):
                self.table.setItem(row, col, QtWidgets.QTableWidgetItem(value))

    def loc_theo_hang(self, text):
        self.hien_thi_du_lieu(text)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = CarManager()
    window.show()
    sys.exit(app.exec())