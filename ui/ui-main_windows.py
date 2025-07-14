from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QListWidget, QFileDialog, QInputDialog, QMessageBox
)
import json
import os

class MainWindow(QWidget):
    def __init__(self, profile_path="profiles.json"):
        super().__init__()
        self.setWindowTitle("Dofus Launcher - Prototype")
        self.resize(500, 400)
        self.profile_path = profile_path

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.profile_list = QListWidget()
        self.layout.addWidget(self.profile_list)

        self.load_profiles()

        btn_add = QPushButton("Ajouter un profil")
        btn_remove = QPushButton("Supprimer le profil sélectionné")
        btn_save = QPushButton("Sauvegarder")

        btn_add.clicked.connect(self.add_profile)
        btn_remove.clicked.connect(self.remove_profile)
        btn_save.clicked.connect(self.save_profiles)

        self.layout.addWidget(btn_add)
        self.layout.addWidget(btn_remove)
        self.layout.addWidget(btn_save)

    def load_profiles(self):
        self.profiles = []
        if os.path.exists(self.profile_path):
            with open(self.profile_path, "r") as f:
                self.profiles = json.load(f)
        self.refresh_list()

    def refresh_list(self):
        self.profile_list.clear()
        for profile in self.profiles:
            self.profile_list.addItem(profile["name"])

    def add_profile(self):
        name, ok = QInputDialog.getText(self, "Nom du profil", "Entrer un nom:")
        if not ok or not name:
            return

        game_path, _ = QFileDialog.getOpenFileName(self, "Chemin de Dofus.exe")
        if not game_path:
            return

        # Valeurs par défaut, à modifier plus tard
        profile = {
            "name": name,
            "proxy_ip": "127.0.0.1",
            "proxy_port": 5555,
            "mac": "00:00:00:00:00:00",
            "hdd_serial": "XXXXXX",
            "game_path": game_path
        }
        self.profiles.append(profile)
        self.refresh_list()

    def remove_profile(self):
        index = self.profile_list.currentRow()
        if index >= 0:
            confirm = QMessageBox.question(self, "Confirmation", "Supprimer ce profil ?")
            if confirm == QMessageBox.StandardButton.Yes:
                self.profiles.pop(index)
                self.refresh_list()

    def save_profiles(self):
        with open(self.profile_path, "w") as f:
            json.dump(self.profiles, f, indent=2)
        QMessageBox.information(self, "Sauvegarde", "Profils enregistrés avec succès.")
