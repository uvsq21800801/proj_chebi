import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sqlite3

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5 import QtCore, QtWidgets

from pyface.qt import QtGui, QtCore
import sys

import os


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.id1 = ''
        self.id2 = ''

        # barre de recherche et table affichée
        self.edit = QtWidgets.QLineEdit()
        
        self.combo = QtWidgets.QComboBox()
        self.table = QtWidgets.QTableWidget()
        self.but_valid_filtre = QPushButton('Valider les filtres', self)
        self.info_barre_de_recherche = QLabel("Barre de recherche:", self)

        header = self.table.horizontalHeader()       
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)       
        
        self.table.selectionModel().selectionChanged.connect(
            self.on_selectionChanged
        )

        # on cherche dans le fichier de config
        f = 'config_bd.txt'
        text_file = open(f, "r")
        lines = text_file.read().split('\n')
        self.global_min = int(lines[0])
        self.global_max = int(lines[1])
        min_max_txt = 'Filtres:\n1- Choix des tailles d\'entités (nombre d\'atome)\nTaille Min et Taille Max\n(veuillez choisir des valeurs entre '+str(lines[0])+' et '+str(lines[1])+')'
        # label du filtre de recherche par taille
        self.info_min_max = QLabel(min_max_txt, self)

        # radio/toggle chaines
        self.info_structure = QLabel("2-Choix du type de structure de l'entité", self)
        #self.radio_choice = QtWidgets.QWidget(Widget)
        self.group_radio = QButtonGroup()
        self.group_radio.setExclusive(False)
        self.group_radio.buttonClicked.connect(self.check_radio)
        self.radio_chaine = QtWidgets.QRadioButton("chaine")
        self.radio_tree = QtWidgets.QRadioButton("arbre")
        self.radio_cycle = QtWidgets.QRadioButton("contient cycle élémentaire (<= 6 sommets)")
        self.radio_autre = QtWidgets.QRadioButton("non_classifié")
        self.group_radio.addButton(self.radio_chaine)
        self.group_radio.addButton(self.radio_tree)
        self.group_radio.addButton(self.radio_cycle)
        self.group_radio.addButton(self.radio_autre)
        
        
        # slider pour le choix de taille de molécule
        self.min = QtWidgets.QLineEdit()
        self.max = QtWidgets.QLineEdit()

        # bouton de validation des filtes

        #### selection et exec nauty
        #label iso info
        self.info_iso = QLabel("Entités à selectionner pour tester l'iomorphisme:\n(vous pouvez n'en sélectionner qu'un pour tester son isomorphisme à lui-même)", self)
        
        # molécule 1 choisie
        self.mol_1 = QLabel("Entité 1: id = ,nom =", self)

        # molécule 2 choisie
        self.mol_2 = QLabel("| Entité 2: id = ,nom =", self)

        # bouton pour vider les deux label molécules
        self.but_reset_choice = QPushButton('Vider la séléction', self)
        
        # bouton pour lancer l'isomorphsime
        self.but_iso = QPushButton('Tester l\'isomorphisme', self)
        
        #label resultat isomorphisme
        self.resultat_iso = QLabel("[Lire le résultat dans le terminal]", self)
        

        # remplissage de la grille de widgets
        grid = QtWidgets.QGridLayout(self)
        grid.addWidget(self.info_min_max, 3, 0)
        grid.addWidget(self.min, 4, 0)
        grid.addWidget(self.max, 4, 1)
        grid.addWidget(self.info_structure,5,0)
        grid.addWidget(self.radio_chaine,6,0)
        grid.addWidget(self.radio_tree,6,1)
        grid.addWidget(self.radio_cycle,6,2)
        grid.addWidget(self.radio_autre,6,3)
        
        grid.addWidget(self.but_valid_filtre, 9, 0)
        grid.addWidget(self.info_barre_de_recherche,11,0)
        grid.addWidget(self.edit, 12, 0)
        grid.addWidget(self.combo, 12, 1)
        grid.addWidget(self.table, 13, 0, 45, 3)
        # isomorphisme
        grid.addWidget(self.info_iso ,60,0)
        grid.addWidget(self.mol_1,61,0)
        grid.addWidget(self.mol_2,61,1)
        grid.addWidget(self.but_reset_choice,61,2)
        grid.addWidget(self.but_iso,61,3)

        grid.addWidget(self.resultat_iso,62,0,1,3)

        self.connection = sqlite3.connect("index.db")

        self.populate_table("SELECT * FROM entity")
        self.edit.textChanged.connect(self.filter_table)
        # self something filter
        self.but_valid_filtre.clicked.connect(self.on_click)
        self.but_iso.clicked.connect(self.iso_exec)
        self.but_reset_choice.clicked.connect(self.reset_choice)
  
    def populate_table(self, query, values=None):
        cursor = self.connection.cursor()
        if values is None:
            cursor.execute(query)
        else:
            cursor.execute(query, values)

        name_of_columns = [e[0] for e in cursor.description]
        self.table.setColumnCount(len(name_of_columns))
        self.table.setRowCount(0)
        self.table.setHorizontalHeaderLabels(name_of_columns)
        self.combo.clear()
        self.combo.addItems(name_of_columns)

        for i, row_data in enumerate(cursor.fetchall()):
            self.table.insertRow(self.table.rowCount())
            for j, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem()
                item.setData(QtCore.Qt.DisplayRole, value)
                self.table.setItem(i, j, item)
    
    def filter_table(self, text):
        if text:
            filter_column = self.combo.currentIndex()

            for i in range(self.table.rowCount()):
                item = self.table.item(i, filter_column)
                if self.filter_row(item, text):
                    self.table.showRow(i)
                else:
                    self.table.hideRow(i)
        else:
            for i in range(self.table.rowCount()):
                self.table.showRow(i)

    def filter_row(self, item, text):
        return text in item.text()

    # applique les filtres
    @pyqtSlot()
    def on_click(self):
        
        # vide la barre de recherche car la recherche est réinitialisée
        self.edit.setText('')  
        
        c = self.connection.cursor()

        final_command = 'SELECT * FROM entity'

        min = self.min.text()
        max = self.max.text()
        # Pour savoir si on filtre la taille
        # on vérifie que les valeurs entrées sont des entiers
        if max.isdigit() and min.isdigit():
            # on vérifie que les deux valeurs sont valides
            min = int(min)
            max = int(max)
            if min<=max and min>= self.global_min and max <= self.global_max:
                
                # get table?
                
                # for min to max value selected agregate ids
                select_taille_SQL = 'SELECT * FROM taille_'+str(min)
                for i in range(min+1, max+1):
                    select_taille_SQL += '\nUNION\nSELECT * FROM taille_'+str(i)
                
                c.execute("""CREATE TABLE IF NOT EXISTS merged AS
                SELECT taille_All.e_id, taille_All.name
                FROM ({taille_unions}) AS taille_All"""
                        .format(taille_unions=select_taille_SQL))

                final_command+="""\nINTERSECT
                            SELECT * FROM merged"""
                
        # Filtre structure 
        if self.radio_chaine.isChecked():
            final_command+="""\nINTERSECT
                            SELECT * FROM chaines"""
        elif self.radio_tree.isChecked():
            final_command+="""\nINTERSECT
                            SELECT * FROM arbre"""
        elif self.radio_cycle.isChecked():
            final_command+="""\nINTERSECT
                            SELECT * FROM contains_cycle_elem"""
        elif self.radio_autre.isChecked():
            final_command+="""\nINTERSECT
                            SELECT * FROM non_class"""

        
        c.execute(final_command)

        name_of_columns = [e[0] for e in c.description]
        self.table.setColumnCount(len(name_of_columns))
        self.table.setRowCount(0)
        self.table.setHorizontalHeaderLabels(name_of_columns)
        self.combo.clear()
        self.combo.addItems(name_of_columns)
        
        for i, row_data in enumerate(c.fetchall()):
            self.table.insertRow(self.table.rowCount())
            for j, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem()
                item.setData(QtCore.Qt.DisplayRole, value)
                self.table.setItem(i, j, item)
                
        # destruction de la table merged après utilisation car elle est temportaire
        listOfTables = c.execute(
        """SELECT name FROM sqlite_master WHERE type='table'
        AND name='merged'; """).fetchall()
        if listOfTables != []:
            c.execute("""DROP TABLE merged;""")
            
        

    def check_radio(self, radioButton):
        # Uncheck every other button in this group
        for button in self.group_radio.buttons():
            if button is not radioButton:
                button.setChecked(False)


    @QtCore.pyqtSlot(QtCore.QItemSelection, QtCore.QItemSelection)
    def on_selectionChanged(self, selected, deselected):
        id = self.table.item(selected.indexes()[0].row(), 0).text()
        nom = self.table.item(selected.indexes()[0].row(), 1).text()
        if self.mol_1.text() == "Entité 1: id = ,nom =":
            self.id1 = id
            self.mol_1.setText("Entité 1: id = "+str(id)+" ,nom = "+str(nom))
        elif self.mol_2.text() == "| Entité 2: id = ,nom =":
            self.id2 = id
            self.mol_2.setText("| Entité 2: id = "+str(id)+" ,nom = "+str(nom))


    def reset_choice(self):
        self.mol_1.setText("Entité 1: id = ,nom =")
        self.mol_2.setText("| Entité 2: id = ,nom =")
        self.id1 = ''
        self.id2 = ''
        
    def iso_exec(self):
        if self.id2 != '' and self.id1 != '':
            os.system("./sparse_run "+self.id1+" "+self.id2)
        elif self.id1 != '':
            os.system("./sparse_run "+self.id1+" "+self.id1)
            
def main():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ex = Widget()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()