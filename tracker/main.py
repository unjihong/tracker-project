# ui_layout_only.py
import sys
from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QDockWidget, QDateEdit, QPushButton, QSplitter, QTableWidget, QTableWidgetItem
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ScreenTime – Layout Only")
        self.resize(1200, 750)

        self._init_left_dock()       # 왼쪽 메뉴 영역
        self._init_right_layout()    # 오른쪽 상단 그래프 + 하단 테이블

        self._apply_style()          # 영역이 잘 보이도록 테두리/배경만 적용(선택)

    # --- 왼쪽: 메뉴/날짜/알람 버튼 ---
    def _init_left_dock(self):
        dock = QDockWidget("메뉴", self)
        dock.setFeatures(QDockWidget.NoDockWidgetFeatures)

        cont = QWidget()
        v = QVBoxLayout(cont)
        title = QLabel("기본 정보 / 날짜")
        title.setStyleSheet("font-weight:600;")
        v.addWidget(title)

        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        v.addWidget(self._wrap_box("날짜 선택", self.date_edit))

        self.btn_alarm = QPushButton("알람 / 제한 설정")
        v.addWidget(self._wrap_box("알람 버튼", self.btn_alarm))

        v.addStretch()
        dock.setWidget(cont)
        dock.setMinimumWidth(260)
        dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    # --- 오른쪽: 상단 그래프 영역 + 하단 프로그램 리스트 ---
    def _init_right_layout(self):
        # 상단 그래프 placeholder
        top = QWidget()
        top_lay = QVBoxLayout(top)
        lab_chart = QLabel("그래프 영역 (차트 위젯 자리)")
        lab_chart.setObjectName("chartBox")
        lab_chart.setAlignment(Qt.AlignCenter)
        top_lay.addWidget(lab_chart)

        # 하단 테이블 placeholder
        bottom = QWidget()
        bot_lay = QVBoxLayout(bottom)
        lab_table_title = QLabel("프로그램 리스트 (테이블)")
        lab_table_title.setStyleSheet("font-weight:600; margin-bottom:4px;")
        bot_lay.addWidget(lab_table_title)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["앱 이름", "오늘(분)", "Active(분)", "Watching(분)", "Idle(분)", "최근 사용"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        # 예시 행 2개(레이아웃 확인용)
        self._append_demo_row("chrome.exe", "120", "90", "25", "5", "13:42")
        self._append_demo_row("code.exe", "80", "80", "0", "0", "12:10")
        bot_lay.addWidget(self.table)

        # 상/하 splitter
        split_v = QSplitter(Qt.Vertical)
        split_v.addWidget(top)
        split_v.addWidget(bottom)
        split_v.setSizes([self.height()//2, self.height()//2])

        # 중앙 위젯에 배치
        root = QWidget()
        root_lay = QHBoxLayout(root)
        root_lay.addWidget(split_v)
        self.setCentralWidget(root)

    def _append_demo_row(self, *cols):
        r = self.table.rowCount()
        self.table.insertRow(r)
        for c, txt in enumerate(cols):
            self.table.setItem(r, c, QTableWidgetItem(txt))

    # --- 보이기 쉽게만 스타일 ---
    def _apply_style(self):
        self.setStyleSheet("""
    QWidget { color: #222; background: #fafafa; }
    QLabel#chartBox {
        background:#ffffff; border:1px dashed #999;
        color:#222; padding:18px; font-size:14px;
    }
    QTableWidget { background:#ffffff; gridline-color:#ccc; color:#222; }
""")


    # 유틸: 라벨+위젯을 박스로 감싸 가독성
    def _wrap_box(self, caption, widget):
        w = QWidget()
        v = QVBoxLayout(w); v.setContentsMargins(0,0,0,0)
        lab = QLabel(caption); lab.setStyleSheet("color:#666;")
        v.addWidget(lab); v.addWidget(widget)
        return w

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
