import sys

from PyQt4.QtCore import Qt
import PyQt4.QtGui as QtGui

from abstract_app import AbstractApplication
from fat_fs_lib.entries import FileEntry, DirEntry


class MyTable(QtGui.QTableWidget):
    def __init__(self, entries, *args):
        """Represent table with entries"""
        self.headers = ['Name', 'Size', 'Attributes',
                        'Date modified', 'Date created']
        QtGui.QTableWidget.__init__(self, 0, len(self.headers))
        self.entries = entries
        self.verticalHeader().hide()
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setHorizontalHeaderLabels(self.headers)
        self.initUI()

    def initUI(self):
        self.refresh_data()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.update()

    def refresh_data(self):
        """Fill table with new data"""
        row = 0
        needed_entries = []
        for entry in self.entries:
            if type(entry) in {FileEntry, DirEntry}:
                needed_entries.append(entry)
        self.setRowCount(len(needed_entries))
        for entry in needed_entries:
            name = QtGui.QTableWidgetItem(entry.get_name())
            self.setItem(row, 0, name)
            if entry.is_dir():
                size = QtGui.QTableWidgetItem("<DIR>")
            else:
                size = QtGui.QTableWidgetItem(str(entry.file_size))
            self.setItem(row, 1, size)
            attrib = QtGui.QTableWidgetItem(self.attrib(entry))
            self.setItem(row, 2, attrib)
            create_dt = self.format_dt(entry.creating_dt)
            self.setItem(row, 3, QtGui.QTableWidgetItem(create_dt))
            mod_dt = QtGui.QTableWidgetItem(self.format_dt(entry.write_dt))
            self.setItem(row, 4, mod_dt)
            row += 1

    def format_dt(self, dt):
        """Formatting datetime if possible"""
        if dt:
            return dt.strftime("%d.%m.%y %H:%M")
        else:
            return None

    def get_width(self):
        """Return true width of table"""
        width = 0
        for i in range(self.columnCount()):
            width += self.columnWidth(i)
        return width

    def attrib(self, entry):
        """Return string represent of attributes"""
        attributes = ['-'] * 5
        if entry.is_dir():
            attributes[0] = 'd'
        if not entry.is_readonly():
            attributes[1] = 'w'
        if entry.is_archive():
            attributes[2] = 'a'
        if entry.is_long_file_name():
            attributes[3] = 'l'
        if entry.is_system():
            attributes[4] = 's'
        return ''.join(attributes)


class MyApp(QtGui.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.controller = None
        self.table = MyTable({})
        self.table.doubleClicked.connect(self.element_clicked)
        self.initUI()

    def element_clicked(self, item):
        """Catch the click on table and decide what to do next"""
        needed_entry = None
        name = item.data()
        for entry in self.controller.pwd_entry.entries:
            if name == entry.get_name():
                needed_entry = entry
                break
        if type(needed_entry) is DirEntry:
            self.process_dir(needed_entry)
        else:
            self.process_file(needed_entry)

    def process_dir(self, entry):
        """If dir was clicked - change dir there"""
        self.controller.cd(entry)
        self.table.entries = self.controller.pwd_entry.entries
        self.table.refresh_data()
        self.table.update()

    def process_file(self, entry):
        """If file was clikced - ask what to do with this file"""
        box = QtGui.QMessageBox()
        box.setText("What do you to do with this file?")
        box.deleteLater()
        save_btn = box.addButton("Save", QtGui.QMessageBox.ActionRole)
        cat_btn = box.addButton("Cat", QtGui.QMessageBox.ActionRole)
        close_btn = box.addButton("Close", QtGui.QMessageBox.DestructiveRole)
        box.exec_()
        if box.clickedButton() == save_btn:
            self.gui_save(entry)
        if box.clickedButton() == cat_btn:
            self.gui_cat(entry)
        if box.clickedButton() == close_btn:
            box.close()

    def gui_save(self, entry):
        """Progress bar for saving"""
        prog_diag = QtGui.QProgressDialog("Saving", "Stop", 0, 100, self)
        prog_diag.setWindowModality(Qt.WindowModal)
        prog_diag.show()
        for percentage in self.controller.save(entry):
            prog_diag.setValue(percentage)
            if prog_diag.wasCanceled():
                break
        prog_diag.destroy()

    def gui_cat(self, entry):
        """Message box for cat"""
        box = QtGui.QMessageBox()
        text = ' '
        for part in self.controller.cat(entry):
            text += part
        box.setText("It might be very slow on big files")
        box.setDetailedText(text)
        box.exec_()

    def initUI(self):
        self.resize(600, 400)
        centralWidget = QtGui.QWidget()
        gridLayout = QtGui.QGridLayout(centralWidget)
        self.setCentralWidget(centralWidget)
        btn = QtGui.QPushButton('Choose the image', self)
        btn.clicked.connect(self.open_image)
        gridLayout.addWidget(btn)
        gridLayout.addWidget(self.table)
        centralWidget.show()
        self.show()

    def open_image(self):
        """Open file dialog to choose image file"""
        if self.controller:
            self.controller.raw.close()
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Choose the image')
        raw = open(fname, 'rb')
        self.controller = AbstractApplication(raw)
        self.table.entries = self.controller.pwd_entry.entries
        self.table.initUI()
        self.resize(self.table.get_width() + 30, 400)


def main(args):
    app = QtGui.QApplication(args)
    myapp = MyApp()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv)
