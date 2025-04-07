from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QFileDialog,
    QLineEdit, QTextEdit, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QDialog, QPushButton, QDialogButtonBox
)
from PyQt5.QtCore import Qt
import sys
import os

class SettingsDialog(QDialog):
    def __init__(self, title, items=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        layout = QVBoxLayout()

        if items:
            self.combo = QComboBox()
            self.combo.addItems(items)
            layout.addWidget(self.combo)
            self.input_mode = False
        else:
            self.line_edit = QLineEdit()
            layout.addWidget(self.line_edit)
            self.input_mode = True

        self.setLayout(layout)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setFixedSize(300, 150)

    def get_selected(self):
        if self.input_mode:
            return self.line_edit.text()
        else:
            return self.combo.currentText()

class PhotoLogGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nikon Photo Log")

        # 参数保存（必须放在前面，以便 QLabel 初始化时可以使用）
        self.author = "Harlan"
        self.border = "basic"

        screen = QApplication.primaryScreen().size()
        w = int(screen.width() * 0.5)
        h = int(screen.height() * 0.5)
        self.setFixedSize(w, h)

        # 布局初始化
        central_widget = QWidget()
        layout = QVBoxLayout()

        # 第一行：输入路径
        input_layout = QHBoxLayout()
        input_btn = QLabel("Input File/Folder:")
        input_btn.setMinimumWidth(150)
        self.input_path = QLineEdit()
        self.input_path.setReadOnly(True)
        select_file_btn = QPushButton("Select File")
        select_file_btn.clicked.connect(self.select_input_file)
        select_folder_btn = QPushButton("Select Folder")
        select_folder_btn.clicked.connect(self.select_input_folder)
        input_layout.addWidget(input_btn)
        input_layout.addWidget(self.input_path)
        input_layout.addWidget(select_file_btn)
        input_layout.addWidget(select_folder_btn)
        layout.addLayout(input_layout)

        # 第二行：输出路径
        output_layout = QHBoxLayout()
        output_btn = QLabel("Output File/Folder:")
        output_btn.setMinimumWidth(150)
        self.output_path = QLineEdit()
        self.output_path.setReadOnly(True)
        select_output_folder_btn = QPushButton("Select Folder")
        select_output_folder_btn.clicked.connect(self.select_output_folder)
        output_layout.addWidget(output_btn)
        output_layout.addWidget(self.output_path)
        output_layout.addWidget(select_output_folder_btn)
        layout.addLayout(output_layout)

        # 第三行：输出后缀
        suffix_layout = QHBoxLayout()
        suffix_label = QLabel("Output Suffix:")
        suffix_label.setMinimumWidth(150)
        self.suffix_input = QLineEdit()
        self.suffix_input.setPlaceholderText("e.g., _processed")
        self.suffix_input.setText("_processed")
        suffix_layout.addWidget(suffix_label)
        suffix_layout.addWidget(self.suffix_input)
        layout.addLayout(suffix_layout)

        # 第四行：作者名（弹窗选择）
        author_btn = QPushButton("Author")
        author_btn.clicked.connect(self.set_author)
        layout.addWidget(author_btn)

        # 第五行：边框风格（弹窗选择）
        border_btn = QPushButton("Border")
        border_btn.clicked.connect(self.set_border)
        layout.addWidget(border_btn)

        # 第六行：运行按钮
        run_btn = QPushButton("RUN!")
        run_btn.setStyleSheet("background-color: red; color: white; font-weight: bold; font-size: 18px;")
        run_btn.clicked.connect(self.run_process)
        layout.addWidget(run_btn, alignment=Qt.AlignHCenter)

        # 第七行：日志框
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        layout.addWidget(self.log_box)

        self.author_label = QLabel(f"Current Author: {self.author}")
        layout.addWidget(self.author_label)

        self.border_label = QLabel(f"Current Border: {self.border}")
        layout.addWidget(self.border_label)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def select_input_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Input File", "", "Images (*.nef *.NEF *.jpg);;All Files (*)")
        if path:
            self.input_path.setText(path)

    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if folder:
            self.input_path.setText(folder)

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_path.setText(folder)

    def set_author(self):
        dialog = SettingsDialog("Enter Author Name", parent=self)
        if dialog.exec_() == QDialog.Accepted:
            self.author = dialog.get_selected()
            self.author_label.setText(f"Current Author: {self.author}")
            self.log_box.append(f"✅ Author set to: {self.author}")

    def set_border(self):
        dialog = SettingsDialog("Select Border", ["basic", "blur"], self)
        if dialog.exec_() == QDialog.Accepted:
            self.border = dialog.get_selected()
            self.border_label.setText(f"Current Border: {self.border}")
            self.log_box.append(f"✅ Border style set to: {self.border}")

    def update_progress(self, current, total):
        percent = int((current / total) * 100)
        self.log_box.append(f"📸 Progress: {current}/{total} ({percent}%)")

    def run_process(self):
        input_path = self.input_path.text()
        output_path = self.output_path.text()

        if not input_path or not output_path:
            self.log_box.append("❌ Please select input and output paths first.")
            return

        suffix = self.suffix_input.text()
        if not suffix.startswith("_"):
            suffix = "_" + suffix
        output_path = os.path.join(
            output_path,
            os.path.splitext(os.path.basename(input_path))[0] + f"{suffix}.jpg"
        )

        self.log_box.append("🚀 Running photolog process...")
        self.log_box.append(f"Input: {input_path}")
        self.log_box.append(f"Output: {output_path}")
        self.log_box.append(f"Author: {self.author}, Border: {self.border}")

        try:
            from main import process_single_file, batch_process_images
            
            if os.path.isfile(input_path) and os.path.isdir(output_path):
                output_path = os.path.join(output_path, os.path.splitext(os.path.basename(input_path))[0] + "_processed.jpg")

            if os.path.isfile(input_path):
                process_single_file(input_path, output_path, self.author, self.border)
            elif os.path.isdir(input_path):
                batch_process_images(input_path, output_path, self.author, self.border, self.update_progress)
            else:
                self.log_box.append("❌ Invalid input path.")
                return

            self.log_box.append("✅ Done!")
        except Exception as e:
            self.log_box.append(f"❌ Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhotoLogGUI()
    window.show()
    sys.exit(app.exec_())