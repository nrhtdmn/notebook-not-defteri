import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QMessageBox, QTabWidget, QWidget, QVBoxLayout
)
from PyQt5.QtGui import QIcon, QFont, QTextCharFormat, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QSyntaxHighlighter
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.token import Keyword, Name, Comment, String, Number, Operator

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)
        self.lexer = PythonLexer()

    def highlightBlock(self, text):
        self.setCurrentBlockState(0)
        tokens = self.lexer.get_tokens(text)

        for ttype, value in tokens:
            length = len(value)
            if ttype in Keyword:
                self.setFormat(self.currentBlock().position() + text.index(value), length, self.getFormat(QColor("#0000ff")))
            elif ttype in Name:
                self.setFormat(self.currentBlock().position() + text.index(value), length, self.getFormat(QColor("#008000")))
            elif ttype in String:
                self.setFormat(self.currentBlock().position() + text.index(value), length, self.getFormat(QColor("#ff4500")))
            elif ttype in Comment:
                self.setFormat(self.currentBlock().position() + text.index(value), length, self.getFormat(QColor("#808080")))
            elif ttype in Number:
                self.setFormat(self.currentBlock().position() + text.index(value), length, self.getFormat(QColor("#ff00ff")))
            elif ttype in Operator:
                self.setFormat(self.currentBlock().position() + text.index(value), length, self.getFormat(QColor("#000000")))

    def getFormat(self, color):
        _format = QTextCharFormat()
        _format.setForeground(color)
        return _format

class NotDefteri(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Python Not Defteri')
        self.setGeometry(100, 100, 800, 600)
        
        # Sekme widget'ı
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        
        # Menü çubuğu
        menubar = self.menuBar()
        dosya_menu = menubar.addMenu('Dosya')
        
        # Dosya açma
        ac_action = QAction(QIcon('open.png'), 'Aç', self)
        ac_action.setShortcut('Ctrl+O')
        ac_action.triggered.connect(self.dosya_ac)
        dosya_menu.addAction(ac_action)
        
        # Dosya kaydetme
        kaydet_action = QAction(QIcon('save.png'), 'Kaydet', self)
        kaydet_action.setShortcut('Ctrl+S')
        kaydet_action.triggered.connect(self.dosya_kaydet)
        dosya_menu.addAction(kaydet_action)
        
        # Yeni dosya
        yeni_action = QAction(QIcon('new.png'), 'Yeni', self)
        yeni_action.setShortcut('Ctrl+N')
        yeni_action.triggered.connect(self.yeni_dosya)
        dosya_menu.addAction(yeni_action)
        
        # Çıkış
        cikis_action = QAction(QIcon('exit.png'), 'Çıkış', self)
        cikis_action.setShortcut('Ctrl+Q')
        cikis_action.triggered.connect(self.cikis_yap)
        dosya_menu.addAction(cikis_action)

        # Çalıştır
        # calistir_action = QAction(QIcon('run.png'), 'Çalıştır', self)
        # calistir_action.setShortcut('Ctrl+R')
        # calistir_action.triggered.connect(self.dosya_calistir)
        # dosya_menu.addAction(calistir_action)
        
        # QSS stili uygula
        self.setStyleSheet(self.qss_stili())
        
        self.show()
    
    def yeni_dosya(self):
        yeni_sekme = QWidget()
        layout = QVBoxLayout()
        
        textEdit = QTextEdit()
        layout.addWidget(textEdit)
        
        yeni_sekme.setLayout(layout)
        self.tab_widget.addTab(yeni_sekme, "Yeni Dosya")
        
        highlighter = PythonHighlighter(textEdit.document())
        textEdit.setFont(QFont('Courier', 12))
    
    def dosya_ac(self):
        dosya_adi, _ = QFileDialog.getOpenFileName(self, 'Dosya Aç', '', 'Python Dosyaları (*.py);;Tüm Dosyalar (*)')
        
        if dosya_adi:
            with open(dosya_adi, 'r', encoding='utf-8') as dosya:
                dosya_icerigi = dosya.read()
            
            yeni_sekme = QWidget()
            layout = QVBoxLayout()
            
            textEdit = QTextEdit()
            textEdit.setText(dosya_icerigi)
            layout.addWidget(textEdit)
            
            yeni_sekme.setLayout(layout)
            self.tab_widget.addTab(yeni_sekme, dosya_adi.split('/')[-1])
            
            highlighter = PythonHighlighter(textEdit.document())
            textEdit.setFont(QFont('Courier', 12))
    
    def dosya_kaydet(self):
        current_widget = self.tab_widget.currentWidget()
        if current_widget:
            textEdit = current_widget.findChild(QTextEdit)
            dosya_adi, _ = QFileDialog.getSaveFileName(self, 'Dosya Kaydet', '', 'Python Dosyaları (*.py);;Tüm Dosyalar (*)')
            
            if dosya_adi:
                with open(dosya_adi, 'w', encoding='utf-8') as dosya:
                    dosya.write(textEdit.toPlainText())
                self.tab_widget.setTabText(self.tab_widget.currentIndex(), dosya_adi.split('/')[-1])
    
    def dosya_calistir(self):
        current_widget = self.tab_widget.currentWidget()
        if current_widget:
            textEdit = current_widget.findChild(QTextEdit)
            kod = textEdit.toPlainText()
            dosya_adi, _ = QFileDialog.getSaveFileName(self, 'Dosya Kaydet ve Çalıştır', '', 'Python Dosyaları (*.py);;Tüm Dosyalar (*)')
            
            if dosya_adi:
                with open(dosya_adi, 'w', encoding='utf-8') as dosya:
                    dosya.write(kod)
                self.tab_widget.setTabText(self.tab_widget.currentIndex(), dosya_adi.split('/')[-1])
                try:
                    sonuc = subprocess.run(['python', dosya_adi], capture_output=True, text=True)
                    QMessageBox.information(self, 'Çalıştırma Sonucu', sonuc.stdout + '\n' + sonuc.stderr)
                except Exception as e:
                    QMessageBox.critical(self, 'Hata', str(e))
    
    def cikis_yap(self):
        reply = QMessageBox.question(self, 'Uyarı', 'Çıkmak istiyor musunuz? Kaydedilmemiş veriler kaybolacak.',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.instance().quit()
    
    def qss_stili(self):
        return """
        QMainWindow {
            background-color: #f0f0f0;
        }
        QTextEdit {
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 10px;
            background-color: white;
        }
        QMenuBar {
            background-color: #333;
            color: white;
        }
        QMenuBar::item {
            background-color: #333;
            color: white;
        }
        QMenuBar::item:selected {
            background-color: #555;
        }
        QMenu {
            background-color: #333;
            color: white;
        }
        QMenu::item {
            background-color: #333;
            color: white;
        }
        QMenu::item:selected {
            background-color: #555;
        }
        QAction {
            color: white;
        }
        """
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    not_defteri = NotDefteri()
    not_defteri.yeni_dosya()  # Başlangıçta bir sekme ekle
    sys.exit(app.exec_())
