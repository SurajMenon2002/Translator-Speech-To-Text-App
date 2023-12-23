from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QComboBox,QPushButton, QLabel, QHBoxLayout,QVBoxLayout,QFileDialog
from PyQt5.QtGui import QFont
from googletrans import Translator
import speech_recognition as sr
from languages import *

#class 
class Home(QWidget):
    #constructor
    def __init__(self):
        super().__init__()
        self.recognize_text=""
        self.initUI()
        self.setting()
        self.button_click() 


 #App object and design
    def initUI(self):
        self.input_box = QTextEdit()
        self.output_box =QTextEdit()
        self.reverse = QPushButton("Reverse")
        self.reset = QPushButton("Reset")
        self.submit = QPushButton("Translate Now")
        self.speak = QPushButton("Speak Now")
        self.save = QPushButton("Save Note")
        self.input_option = QComboBox()
        self.output_option = QComboBox()

        self.input_option.addItems(values)
        self.output_option.addItems(values)
        self.title = QLabel("PyLate")    
        self.title.setFont(QFont("Helvertica", 45))

        self.master = QHBoxLayout()

        col1 = QVBoxLayout()
        col2 = QVBoxLayout()

        col1.addWidget(self.title)
        col1.addWidget(self.input_option)
        col1.addWidget(self.output_option)
        col1.addWidget(self.submit)
        col1.addWidget(self.reset)
        col1.addWidget(self.speak)
        col1.addWidget(self.save)

        col2.addWidget(self.input_box)
        col2.addWidget(self.reverse)
        col2.addWidget(self.output_box)

        self.master.addLayout(col1 , 20)
        self.master.addLayout(col2, 80)

        self.setLayout(self.master)

        self.setStyleSheet("""
            QWidget {
                background-color: #333; /* Darker background color */
                color: #fff; /* Text color */
            }

            QPushButton {
                background-color: #66a3ff; /* Lighter background color for buttons */
                color: #333; /* Text color for buttons */
                border: 1px solid #fff; /* White border for buttons */
                border-radius: 5px; /* Rounded corners for buttons */
                padding: 5px 10px; /* Padding for buttons */
            }

            QPushButton:hover {
                background-color: #3399ff; /* Lighter background color for buttons on hover */
            }
        """)


 #app settings
    def setting(self):
        self.setWindowTitle("PyLate")
        self.setGeometry(200,250,600,500)


 #button events
    def button_click(self):
        self.submit.clicked.connect(self.translate_click)
        self.reverse.clicked.connect(self.reverse_click)
        self.reset.clicked.connect(self.reset_app)
        self.speak.clicked.connect(self.Speak_click)
        self.save.clicked.connect(self.save_click)

 #Speech event
    def get_speech(self):
        listener = sr.Recognizer()
        text = ""
        with sr.Microphone() as source:
            try:
                audio = listener.listen(source, timeout=2)
                text = listener.recognize_google(audio)
                print(text)
            except sr.UnknownValueError:
                print("Can't understand audio")
            except sr.RequestError as e:
                print(f"Can't request results from Google: {e}")
            except Exception as e:
                print(f"An error occured: {e}")
        self.recognize_text = text
        return text        

 #speak click
    def Speak_click(self):
        res = self.get_speech()
        print("Recognized Text:", res)  
        self.input_box.setPlainText(res)

  #Save click
    def save_click(self):
        content =self.output_box.toPlainText()
        file_path, _ = QFileDialog.getSaveFileName(self,"Save Note", '','Text Files (*.txt);;All Files (*)')
        if file_path:
            with open(file_path,'w')as files:
                files.write(content)
 #translate click
    def translate_click(self):
        value_to_key1 = self.output_option.currentText()
        value_to_key2 = self.input_option.currentText()

        key_to_value1 = [k for k,v in LANGUAGES.items() if v == value_to_key1]
        key_to_value2 = [k for k,v in LANGUAGES.items() if v == value_to_key2]

        self.script = self.translate_text(self.input_box.toPlainText(), key_to_value1[0], key_to_value2[0])
        self.output_box.setText(self.script)

 #reset app
    def reset_app(self):
        self.input_box.clear()
        self.output_box.clear()


 #translate text(google)
    def translate_text(self, text, dest_lang, src_lang):
        speaker = Translator()
        translation = speaker.translate(text,dest=dest_lang, src=src_lang)
        return translation.text
    

 #reverse translate
    def reverse_click(self):
        s1,l1 = self.input_box.toPlainText(),self.input_option.currentText()
        s2,l2 = self.output_box.toPlainText(),self.input_option.currentText()

        self.input_box.setText(s2)
        self.output_box.setText(s1)

        self.input_option.setCurrentText(l2)
        self.output_option.setCurrentText(l1)
                                    

#main run
if __name__ in "__main__":
    app=QApplication([])
    main=Home()
    main.show()
    app.exec_()    