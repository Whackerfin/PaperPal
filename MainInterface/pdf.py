import sys,os
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QTextEdit,
    QLineEdit,
    QSlider,#
    QDialog,QTableWidget,QTableWidgetItem,
    QAbstractItemView  #
)
from PySide6.QtCore import Qt, QTimer # Added QTextCursor import
import fitz
import extra_functions
from PySide6 import QtGui,QtWidgets
from PySide6.QtGui import QTextBlockFormat, QFont, QTextCursor ,QTextCharFormat,QColor
class CustomButton(QPushButton):
    def __init__(self, label):
        super().__init__()
        font = QFont()
        font.setFamilies([u"JetBrains Mono NL"])
        font.setBold(True)
        self.setFont(font)
        self.setText(label)
        self.setFixedSize(160, 40)# Adjust the size as needed
        self.setStyleSheet("""
            QPushButton {
                background-color:  #353535;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #282828;
            }
            QPushButton:pressed {
                background-color: #4c4c4c;
            }
        """)

class CustomButton_2(QPushButton):
    def __init__(self, label):
        super().__init__()
        font = QFont()
        font.setFamilies([u"JetBrains Mono NL"])
        font.setBold(True)
        self.setFont(font)
        self.setText(label)
        self.setFixedSize(160, 80)  # Adjust the size as needed
        self.setStyleSheet("""
            QPushButton {
                background-color:  #353535;
                color: white;
                border: none;
                border-radius: 5px;
                text-align: center; /* Center align text */
            }
            QPushButton:hover {
                background-color: #282828;
            }
            QPushButton:pressed {
                background-color: #4c4c4c;
            }
        """)



class PDFView(QWidget):
    def __init__(self, path):
        super().__init__()
        self.pdf_path = path
        self.text_edit = QTextEdit()
        self.extract_text()
        self.setup_ui()

    def extract_text(self):
        doc = fitz.open(self.pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        self.text_edit.setPlainText(text)
        # Center align the text
        cursor = self.text_edit.textCursor()
        cursor.select(QTextCursor.Document)
        block_format = QTextBlockFormat()
        block_format.setAlignment(Qt.AlignCenter)
        cursor.mergeBlockFormat(block_format)
        self.text_edit.setTextCursor(cursor)
        # Set cursor position to the beginning of the text
        self.text_edit.moveCursor(QtGui.QTextCursor.Start)

    def setup_ui(self): #UI Layout Function
        self.text_edit.setReadOnly(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.text_edit)

    def get_selected_text(self):
        return self.text_edit.textCursor().selectedText()
    
class InfoLabel(QWidget):
    def __init__(self):
        super().__init__()
        self.information = QLabel("Info Appears here")
        self.information.setMaximumHeight(100)
        self.information.setStyleSheet("""background-color:#d7d7d7;
                                         border-radius: 15px;
                                       """)

    def print_data(self, message):
        self.information.setText(message)


class ButtonHolder(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.stored_signal=None

        self.meaning_button = CustomButton("Meaning")
        self.meaning_button.clicked.connect(self.on_meaning_button_clicked)

        self.synonym_button = CustomButton("Synonym")
        self.synonym_button.clicked.connect(self.on_synonym_button_clicked)
        
        # Creating the zoom in button 
        self.zoomInButton = CustomButton("+")
        self.zoomInButton.clicked.connect(self.zoomIn)
        self.zoomInButton.setFixedSize(60,40) # Defining the size of the button

        # Creating the zoom out button 
        self.zoomOutButton = CustomButton("-")
        self.zoomOutButton.clicked.connect(self.zoomOut)
        self.zoomOutButton.setFixedSize(60,40) # Defining the size of the button
    
        self.speech_button = CustomButton("Read Aloud")
        self.speech_button.clicked.connect(self.on_speech_button_clicked)
        
        self.auto_scroll_button = CustomButton("Auto-Scroll")
        self.auto_scroll_button.setCheckable(True)
        self.auto_scroll_button.toggled.connect(self.on_auto_scroll_toggled)

        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(1, 10)
        self.speed_slider.setValue(5)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.setMaximumWidth(120)  # Set maximum width to match button
        self.speed_slider.valueChanged.connect(self.on_speed_changed)

        self.close_button = CustomButton("Close")
        self.close_button.clicked.connect(self.main_window.close)
        font = QFont()
        font.setFamilies([u"JetBrains Mono NL"])
        font.setBold(True)
        self.autoscroll_label = QLabel("Auto-Scroll Speed:")
        self.autoscroll_label.setStyleSheet("""color:#ffffff;
                                            font-size: 8pt;""")
        self.autoscroll_label.setFont(font)
        
        self.search_label = QLabel("Search:")
        self.search_box = QLineEdit()
        self.search_button = CustomButton("Search")
        self.search_button.clicked.connect(self.search_pdf)

        self.next_button = CustomButton(">")
        self.next_button.clicked.connect(self.next_occurrence)
        self.next_button.setFixedSize(60,40)

        self.prev_button = CustomButton("<")
        self.prev_button.clicked.connect(self.prev_occurrence)
        self.prev_button.setFixedSize(60,40)

        self.add_bookmark_button = CustomButton_2("Bookmarks \n (Select a text )") 
        self.add_bookmark_button.clicked.connect(self.add_bookmark)

        self.go_to_bookmark_button= CustomButton("Go to Bookmark")
        self.go_to_bookmark_button.clicked.connect(self.go_to_bookmark)

        # Creating a highlight button 
        self.highlight = CustomButton('Highlight')
        self.highlight.clicked.connect(self.highlight_text)


        # Loading the highlights done in the previous session 
        self.load_highlighted_text()

        # Creating a remove highlighting button 
        self.remove = CustomButton('Clear')
        self.remove.clicked.connect(self.remove_text)

        self.navigate_layout=QHBoxLayout()
        self.navigate_layout.addWidget(self.prev_button)
        self.navigate_layout.addWidget(self.next_button)

        # Creating the layout for zooming buttons
        self.zoom = QHBoxLayout()
        self.zoom.addWidget(self.zoomInButton)
        self.zoom.addWidget(self.zoomOutButton)

        # Creating the border for the zooming button layout
        self.border = QWidget()
        self.border.setLayout(self.zoom)
        self.border.setStyleSheet("QWidget { border: 2px solid red; }")

        self.search_results = []
        self.search_result=[]
        self.current_pos = -1
        self.container = QVBoxLayout()
        self.container.addWidget(self.meaning_button)
        self.container.addWidget(self.synonym_button)
        self.container.addWidget(self.speech_button)
        self.container.addWidget(self.auto_scroll_button)
        self.container.addWidget(self.autoscroll_label)
        self.container.addWidget(self.speed_slider)
        self.container.addWidget(self.search_label)
        self.container.addWidget(self.search_box)
        self.container.addWidget(self.search_button)
        self.container.addLayout(self.navigate_layout)
        self.container.addWidget(self.add_bookmark_button)
        self.container.addWidget(self.go_to_bookmark_button)
        self.container.addWidget(self.border) # Adding the border for the zooming buttons
        self.container.addLayout(self.zoom) # Adding the layout for the zooming buttons
        self.container.addWidget(self.highlight) # Adding the highlighting button
        self.container.addWidget(self.remove) # Adding the remove highlighting button
        self.container.addWidget(self.close_button)
        self.container.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(self.container)

    def on_meaning_button_clicked(self):
        selected_text = self.main_window.pdf_view.get_selected_text()
        if selected_text:
            definition = extra_functions.get_definition(selected_text)
            self.main_window.information.print_data(f"Meaning of {selected_text} : {definition}")

    def on_synonym_button_clicked(self):
        selected_text = self.main_window.pdf_view.get_selected_text()
        if selected_text:
            synonyms = extra_functions.get_synonyms(selected_text)
            if synonyms:
                self.main_window.information.print_data(f"Synonym of {selected_text} : {synonyms[0]}")

    def on_speech_button_clicked(self):
        selected_text = self.main_window.pdf_view.get_selected_text()
        if selected_text:
            extra_functions.get_word_pronunciation(selected_text)

    def on_auto_scroll_toggled(self, checked):
        if checked:
            self.main_window.start_auto_scroll()
        else:
            self.main_window.stop_auto_scroll()
    
    def zoomIn(self):
        font = self.main_window.pdf_view.text_edit.font() 
        font_size = font.pointSize() # Getting the font size
        font.setPointSize(font_size + 1) # Increasing the font size for zooming In
        self.main_window.pdf_view.text_edit.setFont(font) # Applying the changes

    def zoomOut(self):
        font = self.main_window.pdf_view.text_edit.font()
        font_size = font.pointSize() # Getting the font size
        font.setPointSize(font_size - 1) # Increasing the font size for zooming out
        self.main_window.pdf_view.text_edit.setFont(font) # Applying the changes
    
    def highlight_text(self):
        selected_text = self.main_window.pdf_view.get_selected_text() # Getting the selected text
        if selected_text:
            # Get the current page number based on the cursor position
            cursor = self.main_window.pdf_view.text_edit.textCursor()
            start_index = cursor.selectionStart()
            end_index = cursor.selectionEnd()
            color = "red"
             # Creating a cursor to navigate the document
            format = QTextCharFormat() # Creating a format to apply on the text
            format.setBackground(QColor("red")) 
            cursor.mergeCharFormat(format) # Applying the formating on the selected text
            file_path = "highlights.txt"
            L = [] # Appending the details in a list
            L.append([start_index,end_index,color]) 
            file_path = "highlights.txt"  # Save highlights to a text file
            with open(file_path, "a+",encoding="utf-8") as file:
                for i in L:
                    for j in i:
                        file.write(str(j) +" ")
                    file.write("\n")
        else:
            QMessageBox.information(self,"No Text selected ","Select a portion of the document") # Prompting the user to select some text


    def remove_text(self):
        selected_text = self.main_window.pdf_view.get_selected_text() # Getting the selected text
        if selected_text:
            # Get the current page number based on the cursor position
            cursor = self.main_window.pdf_view.text_edit.textCursor()
            start_index = cursor.selectionStart()
            end_index = cursor.selectionEnd()
            color = "Transparent" # Creating a cursor to navigate the document
            format = QTextCharFormat() # Creating the default format to apply on the text
            format.setBackground(QColor(color))   
            cursor.mergeCharFormat(format)
            file_path = "highlights.txt"
            L = [] # Appending the details in a list
            L.append([start_index,end_index,color]) 
            # L.extend(selected_text.split("\u2029"))
            file_path = "highlights.txt"  # Save highlights to a text file
            with open(file_path, "a+",encoding="utf-8") as file:
                for i in L:
                    for j in i:
                        file.write(str(j) +" ")
                    file.write("\n") # Applying the formating on the selected text
        else:
            QMessageBox.information(self,"No Text selected ","Select a portion of the document") # Prompting the user to select some text

    def load_highlighted_text(self):
        try:
            cursor = self.main_window.pdf_view.text_edit.textCursor()
            # Reading the file in which highlights are stored and appending to a list
            loaded_highlights = []
            file_path = "highlights.txt"
            with open(file_path, "r", encoding="utf-8") as file:
                for i in file.readlines():
                    loaded_highlights.append(i)
            # Reading the list and applying the formating 
            for i in loaded_highlights:
                L = i.split(" ")
                start_index = int(L[0])
                end_index = int(L[1])
                color = L[2]
                format = QTextCharFormat() # Creating the default format to apply on the text
                format.setBackground(QColor(color)) # Moving the cursor the location of selected text
                cursor.setPosition(start_index)
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, end_index - start_index)
                cursor.setCharFormat(format)

        except FileNotFoundError:
            pass  # No highlighted text information available


    def on_speed_changed(self, value):
        self.main_window.set_auto_scroll_speed(value)


    def search_pdf(self):
        search_query = self.search_box.text()
        if search_query:
            # Set the cursor to the start of the document
            cursor = self.main_window.pdf_view.text_edit.textCursor()
            cursor.setPosition(0)
            self.main_window.pdf_view.text_edit.setTextCursor(cursor)
            
            # Clear previous search results
            self.search_results.clear()
            self.current_pos = -1
            
            # Search for all occurrences of the word
            while True:
                found_cursor = self.main_window.pdf_view.text_edit.document().find(search_query, cursor)
                if found_cursor.isNull():
                    break
                self.search_results.append(found_cursor)
                cursor = found_cursor

            if self.search_results:
                # Move the cursor to the first occurrence
                self.current_pos = 0
                self.main_window.pdf_view.text_edit.setTextCursor(self.search_results[self.current_pos])
                # Ensure the found word is visible
                self.main_window.pdf_view.text_edit.ensureCursorVisible()
            else:
                self.main_window.information.print_data("Search query not found.")

    def next_occurrence(self):
        if self.search_results:
            self.current_pos = (self.current_pos + 1) % len(self.search_results)
            self.main_window.pdf_view.text_edit.setTextCursor(self.search_results[self.current_pos])
            self.main_window.pdf_view.text_edit.ensureCursorVisible()

    
   
    def prev_occurrence(self):
        if self.search_results:
            self.current_pos = (self.current_pos - 1) % len(self.search_results)
            self.main_window.pdf_view.text_edit.setTextCursor(self.search_results[self.current_pos])
            self.main_window.pdf_view.text_edit.ensureCursorVisible()


   # Function to add a bookmark
    def add_bookmark(self):
        # Get selected text from PDF view
        selected_text = self.main_window.pdf_view.get_selected_text()
        # If text is selected
        if selected_text:
            # Get current page number based on cursor position
            cursor = self.main_window.pdf_view.text_edit.textCursor()
            s_cursor = cursor.selectionStart()
            e_cursor = cursor.selectionEnd()
            # Get current directory
            current_dir = os.getcwd()   
            # Extract PDF name from path
            pdf_name = os.path.splitext(os.path.basename(self.main_window.pdf_view.pdf_path))[0]
            # Create bookmark window with required inputs
            bookmark_window = Add_bookmark(pdf_name, current_dir, s_cursor,e_cursor)


            # Execute the window event loop
            a = bookmark_window.exec()
        else:
            # Show message if no text is selected
            QMessageBox.information(self, "No Text selected", "Please select a text to add bookmark")
    
    
     # Function to go to a bookmark in the PDF
    def go_to_bookmark(self):
        # Get current directory
        current_dir = os.getcwd()   
        # Extract PDF name from path
        pdf_name = os.path.splitext(os.path.basename(self.main_window.pdf_view.pdf_path))[0]
        # Open bookmark dialog
        dialog = open_bookmark(pdf_name, current_dir)
        # Execute dialog and get result
        result = dialog.exec()
        # If dialog is accepted
        if result == QDialog.Accepted:
            # Get the required inputs from dialog
            s_cursor,e_cursor = dialog.get_selected_bookmark()
            if s_cursor is not None:
                # Search for bookmark
                #print(e_cursor,s_cursor)
                self.search_bookmark(s_cursor,e_cursor)
    
    # Function to search for a bookmarked word
    def search_bookmark(self, s_cursor, e_cursor):
       # If cursors exist
       if s_cursor is not None and e_cursor is not None:
           # Set cursor to start and end positions
           cursor = self.main_window.pdf_view.text_edit.textCursor()
           cursor.setPosition(s_cursor)
           cursor.setPosition(e_cursor, QTextCursor.KeepAnchor)  # Select text between start and end positions
           self.main_window.pdf_view.text_edit.setTextCursor(cursor)
       else:
           # Print message if bookmark not found
           self.main_window.information.print_data("Bookmark not found.")

# Class for representing a bookmark data object
class Data_Bookmark:
    def __init__(self, bookmark_name, notes, s_cursor,e_cursor):
        self.bookmark_name = bookmark_name
        self.notes = notes
        self.s_cursor=s_cursor
        self.e_cursor=e_cursor
#Class for adding bookmarks
class Add_bookmark(QDialog):
    def __init__(self,pdf_name,current_dir,s_cursor,e_cursor):
        super().__init__()
        self.pdf_name=pdf_name
        self.current_dir=current_dir
        self.s_cursor=s_cursor
        self.e_cursor = e_cursor
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Bookmark Manager")

        # Create QTableWidget for displaying bookmarks
        self.table_widget = QtWidgets.QTableWidget(self)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Bookmark Name", "Notes", "s_cursor", "e_cursor"])

        # Set size policy for the table widget
        self.table_widget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        # Set selection mode to select entire rows
        self.table_widget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        # Set column widths
        self.table_widget.setColumnWidth(0, 300)  # Bookmark Name
        self.table_widget.setColumnWidth(1, 300)  # Page Number
        self.table_widget.setColumnWidth(2, 0)  # 
        self.table_widget.setColumnWidth(3, 0)  #

        # Set row height for better visibility of multi-line notes
        self.table_widget.verticalHeader().setDefaultSectionSize(50)

        # Create QPushButton for adding, editing, and removing bookmarks
        self.add_button = QtWidgets.QPushButton("Add Bookmark", self)
        self.add_button.clicked.connect(self.add_bookmark)

        self.edit_button = QtWidgets.QPushButton("Edit Bookmark", self)
        self.edit_button.clicked.connect(self.edit_bookmark)

        self.remove_button = QtWidgets.QPushButton("Remove Bookmark", self)
        self.remove_button.clicked.connect(self.remove_bookmark)

        self.close_button = QtWidgets.QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)

        # Create layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.table_widget)
        layout.addWidget(self.add_button)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.remove_button)
        layout.addWidget(self.close_button)

        # Load bookmarks from file
        self.load_bookmarks()

        self.setFixedSize(700,400)

    def add_bookmark(self):
        # Get bookmark name from user input
        bookmark_name, ok = QtWidgets.QInputDialog.getText(self, "Input Dialog", "Enter Bookmark name:")
        if not ok:
            return
        
        # Get notes from user input
        notes, ok = QtWidgets.QInputDialog.getText(self, "Input Dialog", "Enter notes:")
        if not ok:
            return

        # Create bookmark object
        bookmark = Data_Bookmark(bookmark_name, notes, self.s_cursor,self.e_cursor)

        # Add bookmark to the table
        self.add_bookmark_to_table(bookmark)

        # Save bookmarks to file
        self.save_bookmarks()

    def edit_bookmark(self):
        # Get selected item
        selected_item = self.table_widget.selectedItems()
        if not selected_item:
            return

        row = selected_item[0].row()

        # Retrieve bookmark details from the selected row
        bookmark_name = self.table_widget.item(row, 0).text()
        notes = self.table_widget.item(row, 1).text()

        # Prompt user to edit bookmark details
        new_bookmark_name, ok = QtWidgets.QInputDialog.getText(self, "Edit Bookmark", "Enter new bookmark name:", text=bookmark_name)
        if not ok:
            return

        new_notes, ok = QtWidgets.QInputDialog.getText(self, "Edit Bookmark", "Enter new notes:", text=notes)
        if not ok:
            return

        # Update bookmark details in the table
        self.table_widget.item(row, 0).setText(new_bookmark_name)
        self.table_widget.item(row, 1).setText(new_notes)

        # Save bookmarks to file
        self.save_bookmarks()

    def remove_bookmark(self):
        # Get selected item
        selected_item = self.table_widget.selectedItems()
        if not selected_item:
            return

        row = selected_item[0].row()

        # Remove selected row from the table
        self.table_widget.removeRow(row)

        # Save bookmarks to file
        self.save_bookmarks()

    def add_bookmark_to_table(self, bookmark):
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)

        # Insert bookmark's details into the table
        self.table_widget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(bookmark.bookmark_name))
        self.table_widget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(bookmark.notes))
        self.table_widget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(bookmark.s_cursor)))
        self.table_widget.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(bookmark.e_cursor)))

    def save_bookmarks(self):
        # Define the file name based on the PDF name
        filename = f"{self.pdf_name}_bookmarks.txt"
        # Get the current directory
        filepath = os.path.join(self.current_dir, filename)
        # Open the file in write mode
        with open(filepath , "w", encoding="utf-8") as file:
            # Write all bookmarks to the file
            for row in range(self.table_widget.rowCount()):
                bookmark_name = self.table_widget.item(row, 0).text()
                notes = self.table_widget.item(row, 1).text().replace('\n', '<br>')# Replace newline with a placeholder
                s_cursor =int(self.table_widget.item(row, 2).text()) 
                e_cursor = int(self.table_widget.item(row, 3).text())  
                file.write(f"{bookmark_name};*;#%{notes};*;#%{s_cursor};*;#%{e_cursor}\n")

    def load_bookmarks(self):
        # Define the file name based on the PDF name
        filename = f"{self.pdf_name}_bookmarks.txt"
        # Get the current directory
        filepath = os.path.join(self.current_dir, filename)
        # Open the file in read mode
        try:
            with open(filepath, "r+", encoding="utf-8") as file:
                # Read each line from the file
                for line in file:
                    # Split the line into bookmark details
                    bookmark_name, notes, s_cursor,e_cursor = line.strip().split(';*;#%')
                    s_cursor = int(s_cursor)
                    e_cursor = int(e_cursor)
                    # Replace placeholder with newline character
                    notes = notes.replace('<br>', '\n')
                    # Create bookmark object
                    bookmark = Data_Bookmark(bookmark_name,  notes, s_cursor,e_cursor)
                    # Add bookmark to the table
                    self.add_bookmark_to_table(bookmark)

        except FileNotFoundError:
            # If the file doesn't exist, create it
            with open(filepath, "w", encoding="utf-8"):
                pass  # Do nothing, file created

# Class for displaying and managing bookmarks dialog
class open_bookmark(QDialog):
    def __init__(self, pdf_name, current_dir):
        super().__init__()
        self.pdf_name = pdf_name
        self.current_dir = current_dir
        self.setup_ui()

    def setup_ui(self):
        # Set dialog title
        self.setWindowTitle("Open Bookmark")

        # Create table widget for displaying bookmarks
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Bookmark Name",  "Notes", "s_cursor","e_cursor"])

        # Set column widths
        self.table_widget.setColumnWidth(0, 300)  # Bookmark Name
        self.table_widget.setColumnWidth(1, 300)  # Page Number
        self.table_widget.setColumnWidth(2, 0)  # end_cursor
        self.table_widget.setColumnWidth(3, 0)  # start_cursor

        # Set row height for better visibility of multi-line notes
        self.table_widget.verticalHeader().setDefaultSectionSize(50)

        # Set selection mode to select entire rows
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Create button for opening selected bookmark
        self.open_button = QPushButton("Open Bookmark", self)
        self.open_button.clicked.connect(self.accept)

        # Set up layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.table_widget)
        layout.addWidget(self.open_button)

        # Load bookmarks into the table
        self.load_bookmarks()

        # Set fixed dialog size
        self.setFixedSize(700, 400)

    def add_bookmark_to_table(self, bookmark):
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)

        # Insert bookmark's details into the table
        self.table_widget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(bookmark.bookmark_name))
        self.table_widget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(bookmark.notes))
        self.table_widget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(bookmark.s_cursor)))
        self.table_widget.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(bookmark.e_cursor)))

    def load_bookmarks(self):
        # Define the file name based on the PDF name
        filename = f"{self.pdf_name}_bookmarks.txt"
        # Get the current directory
        filepath = os.path.join(self.current_dir, filename)
        # Open the file in read mode
        try:
            with open(filepath, "r+", encoding="utf-8") as file:
                # Read each line from the file
                for line in file:
                    # Split the line into bookmark details
                    bookmark_name, notes, s_cursor,e_cursor = line.strip().split(';*;#%')
                    s_cursor = int(s_cursor)
                    e_cursor = int(e_cursor)
                    # Replace placeholder with newline character
                    notes = notes.replace('<br>', '\n')
                    # Create bookmark object
                    bookmark = Data_Bookmark(bookmark_name,  notes, s_cursor,e_cursor)
                    # Add bookmark to the table
                    self.add_bookmark_to_table(bookmark)

        except FileNotFoundError:
            # If the file doesn't exist, create it
            with open(filepath, "w", encoding="utf-8"):
                pass  # Do nothing, file created

    def get_selected_bookmark(self):
        selected_items = self.table_widget.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            s_cursor = int(self.table_widget.item(row, 2).text())
            e_cursor = int(self.table_widget.item(row, 3).text())
            return [s_cursor,e_cursor]
        return None

class MainWindow(QWidget):


    def __init__(self, path):
        super().__init__()
        self.setWindowTitle("PySide6 PDF Viewer")
        self.pdf_view = PDFView(path)
        self.information = InfoLabel()
        self.button_holder = ButtonHolder(self)

            

        self.qlayout = QVBoxLayout()
        self.qlayout.addWidget(self.pdf_view.text_edit, 10)
        self.qlayout.addWidget(self.information.information, 1)
        self.hlayout = QHBoxLayout()
        self.hlayout.addLayout(self.qlayout, 10)
        self.hlayout.addWidget(self.button_holder, 1)
        self.hlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hlayout)

        self.setWindowState(Qt.WindowFullScreen)
        self.setStyleSheet("""
            QWidget#pdf_view{
                background-color:#e0e0e0;
                color-black;
            }
            QWidget{
                background-color:#333333;
            }              
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333333;
            }
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
                background-color:  #353535;
                border: 1px solid black;             
                padding: 10px;
            }
            QPushButton:hover {
                background-color:#282828;
            }
            QPushButton:pressed {
                background-color: #555555;
            }
            QLineEdit {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 5px;
            }
        """)

        # Initialize QTimer for auto-scroll
        self.auto_scroll_timer = QTimer(self)
        self.auto_scroll_timer.timeout.connect(self.auto_scroll)
        self.auto_scroll_speed = 50  # Default auto-scroll speed
        self.is_auto_scrolling = False

    def start_auto_scroll(self):
        self.is_auto_scrolling = True
        self.auto_scroll_timer.start(1000 // self.auto_scroll_speed)

    def stop_auto_scroll(self):
        self.is_auto_scrolling = False
        self.auto_scroll_timer.stop()

    def set_auto_scroll_speed(self, speed):
        self.auto_scroll_speed = speed * 10
        if self.is_auto_scrolling:
            self.auto_scroll_timer.setInterval(1000 // speed)

    def auto_scroll(self):
        # Calculate the maximum scroll position
        max_scroll = self.pdf_view.text_edit.verticalScrollBar().maximum()
        # Increment scroll position
        current_scroll = self.pdf_view.text_edit.verticalScrollBar().value()
        new_scroll = current_scroll + 1
        if new_scroll > max_scroll:
            new_scroll = 0
        # Set new scroll position
        self.pdf_view.text_edit.verticalScrollBar().setValue(new_scroll)



    




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow("test.pdf")
    window.show()
    sys.exit(app.exec())
