from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon("assets/icon.png"))

        self.setGeometry(450, 150, 900, 500)
        self.setWindowTitle("Resistor Identifier")

        self.initUI()

        # Resistor color values
        self.color_values = {
            "Black": 0,
            "Brown": 1,
            "Red": 2,
            "Orange": 3,
            "Yellow": 4,
            "Green": 5,
            "Blue": 6,
            "Violet": 7,
            "Gray": 8,
            "White": 9
        }

        # Multiplier values
        self.multiplier_values = {
            "Black": 1,
            "Brown": 10,
            "Red": 100,
            "Orange": 1000,
            "Yellow": 10000,
            "Green": 100000,
            "Blue": 1000000,
            "Violet": 10000000,
            "Gray": 100000000,
            "White": 1000000000
        }

        # Tolerance values
        self.tolerance_values = {
            "Brown ±1%": 1,
            "Red ±2%": 2,
            "Gold ±5%": 5,
            "Silver ±10%": 10
        }

        # Update enabled/disabled bands
        self.bands_combo.currentIndexChanged.connect(self.update_band_visibility)

        # Set default state
        self.update_band_visibility()

    # ========== UI ==========
    def initUI(self):

        # ---------- Central Widget ----------

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # ---------- Main Layout ----------

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 1)

        # ========== LEFT PANEL ==========
        display_panel = QFrame()
        display_panel.setObjectName("displayPanel")

        display_layout = QVBoxLayout(display_panel)

        # ---------- resistor image (preview) ----------

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumHeight(250)

        resistor_image = QPixmap("assets/resistor.png")

        self.image_label.setPixmap(
            resistor_image.scaled(
                500,
                250,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

        display_layout.addWidget(self.image_label)

        # ---------- calculation result ----------

        self.result_label = QLabel("Resistance:\n ")

        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setMinimumHeight(50)

        display_layout.addWidget(self.result_label)

        # ---------- information ----------

        self.info_label = QLabel("Choose the resistor colors to see information.")

        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setWordWrap(True)
        self.info_label.setMinimumHeight(150)

        display_layout.addWidget(self.info_label)

        # ---------- add left panel ----------

        main_layout.addWidget(display_panel)

        # ========== RIGHT PANEL ===========
        control_panel = QFrame()
        control_panel.setObjectName("controlPanel")

        control_layout = QVBoxLayout(control_panel)

        # ========== number of bands ==========
        bands_label = QLabel("Number of Bands")

        self.bands_combo = QComboBox()

        self.bands_combo.addItems([
            "3 Bands",
            "4 Bands",
            "5 Bands",
            "6 Bands"
        ])

        # Default = 3 Bands
        self.bands_combo.setCurrentIndex(0)

        control_layout.addWidget(bands_label)
        control_layout.addWidget(self.bands_combo)

        # ========== BAND 1 ==========
        self.band1_label = QLabel("Band 1")

        self.band1_combo = QComboBox()

        self.add_color_items(self.band1_combo)

        control_layout.addWidget(self.band1_label)
        control_layout.addWidget(self.band1_combo)

        # ========== BAND 2 ==========
        self.band2_label = QLabel("Band 2")

        self.band2_combo = QComboBox()

        self.add_color_items(self.band2_combo)

        control_layout.addWidget(self.band2_label)
        control_layout.addWidget(self.band2_combo)

        # ========== BAND 3 ==========
        self.band3_label = QLabel("Band 3")

        self.band3_combo = QComboBox()

        self.add_color_items(self.band3_combo)

        control_layout.addWidget(self.band3_label)
        control_layout.addWidget(self.band3_combo)

        # ========== MULTIPLIER ==========
        self.multiplier_label = QLabel("Multiplier")

        self.multiplier_combo = QComboBox()

        self.add_color_items(self.multiplier_combo)

        control_layout.addWidget(self.multiplier_label)
        control_layout.addWidget(self.multiplier_combo)

        # ========== TOLERANCE ==========
        self.tolerance_label = QLabel("Tolerance")

        self.tolerance_combo = QComboBox()

        tolerances = {
            "Brown ±1%": "#8B4513",
            "Red ±2%": "#FF0000",
            "Gold ±5%": "#D4AF37",
            "Silver ±10%": "#C0C0C0"
        }

        for name, color in tolerances.items():

            self.tolerance_combo.addItem(name)

            index = self.tolerance_combo.count() - 1

            # Background
            self.tolerance_combo.setItemData(
                index,
                QColor(color),
                Qt.BackgroundRole
            )

            # text calibration
            if name in ["Gold ±5%", "Silver ±10%"]:
                text_color = "#000000"
            else:
                text_color = "#FFFFFF"

            self.tolerance_combo.setItemData(
                index,
                QColor(text_color),
                Qt.ForegroundRole
            )

        control_layout.addWidget(self.tolerance_label)
        control_layout.addWidget(self.tolerance_combo)

        # ========== TEMPERATURE ==========
        self.temperature_label = QLabel("Temperature")

        self.temperature_combo = QComboBox()

        temperatures = {
            "Black 250 ppm/K": "#000000",
            "Brown 100 ppm/K": "#8B4513",
            "Red 50 ppm/K": "#FF0000",
            "Orange 15 ppm/K": "#FFA500",
            "Yellow 25 ppm/K": "#FFFF00",
            "Green 20 ppm/K": "#008000",
            "Blue 10 ppm/K": "#0000FF",
            "Violet 5 ppm/K": "#800080",
            "Gray 1 ppm/K": "#808080",
        }

        for name, color in temperatures.items():

            self.temperature_combo.addItem(name)
            index = self.temperature_combo.count() - 1

            # Background color
            self.temperature_combo.setItemData(
                index,
                QColor(color),
                Qt.BackgroundRole
            )

            # text calibration
            if name in ["Yellow 25 ppm/K"]:
                text_color = "#000000"
            else:
                text_color = "#FFFFFF"

            self.temperature_combo.setItemData(
                index,
                QColor(text_color),
                Qt.ForegroundRole
            )

        control_layout.addWidget(self.temperature_label)
        control_layout.addWidget(self.temperature_combo)

        # ========== CALCULATE ==========
        self.calculate_button = QPushButton("CALCULATE")

        control_layout.addWidget(self.calculate_button)

        # ---------- Add Right Panel ----------

        main_layout.addWidget(control_panel)

        # ---------- Button Connection ----------

        self.calculate_button.clicked.connect(self.calculate)

    # ========== add colored combo items ==========
    def add_color_items(self, combo):

        colors = {
            "Black": "#000000",
            "Brown": "#8B4513",
            "Red": "#FF0000",
            "Orange": "#FFA500",
            "Yellow": "#FFFF00",
            "Green": "#008000",
            "Blue": "#0000FF",
            "Violet": "#800080",
            "Gray": "#808080",
            "White": "#FFFFFF"
        }

        for name, color in colors.items():

            combo.addItem(name)
            index = combo.count() - 1

            # Background color
            combo.setItemData(
                index,
                QColor(color),
                Qt.BackgroundRole
            )

            # text calibration
            if name in ["Yellow", "White"]:
                text_color = "#000000"
            else:
                text_color = "#FFFFFF"

            combo.setItemData(
                index,
                QColor(text_color),
                Qt.ForegroundRole
            )

    # ========== update band visibility ==========
    def update_band_visibility(self):

        bands = int(self.bands_combo.currentText()[0])

        # Band 1 and Band 2 are ALWAYS enabled
        self.band1_label.setEnabled(True)
        self.band1_combo.setEnabled(True)

        self.band2_label.setEnabled(True)
        self.band2_combo.setEnabled(True)

        # Band 3
        self.band3_label.setEnabled(bands >= 5)
        self.band3_combo.setEnabled(bands >= 5)

        # Tolerance
        self.tolerance_label.setEnabled(bands >= 4)
        self.tolerance_combo.setEnabled(bands >= 4)

        # Temperature Coefficient
        self.temperature_label.setEnabled(bands >= 6)
        self.temperature_combo.setEnabled(bands >= 6)

    # ========== get colors ==========
    def get_selected_color(self, combo):

        colors = {
            "Black": "#000000",
            "Brown": "#8B4513",
            "Red": "#FF0000",
            "Orange": "#FFA500",
            "Yellow": "#FFFF00",
            "Green": "#008000",
            "Blue": "#0000FF",
            "Violet": "#800080",
            "Gray": "#808080",
            "White": "#FFFFFF"
        }

        return colors[combo.currentText()]

    def get_selected_bands(self):

        bands = int(self.bands_combo.currentText()[0])
        colors = []

        # Band 1
        colors.append(self.get_selected_color(self.band1_combo))
        # Band 2
        colors.append(self.get_selected_color(self.band2_combo))
        # Band 3
        if bands >= 5:
            colors.append(self.get_selected_color(self.band3_combo))
        # Multiplier
        colors.append(self.get_selected_color(self.multiplier_combo))
        # Tolerance
        if bands >= 4:
            tolerance_colors = {
                "Brown ±1%": "#8B4513",
                "Red ±2%": "#FF0000",
                "Gold ±5%": "#D4AF37",
                "Silver ±10%": "#C0C0C0"
            }
            colors.append(tolerance_colors[self.tolerance_combo.currentText()])
        # Temperature coefficient
        if bands >= 6:
            temperature_colors = {
                "Black 250 ppm/K": "#000000",
                "Brown 100 ppm/K": "#8B4513",
                "Red 50 ppm/K": "#FF0000",
                "Orange 15 ppm/K": "#FFA500",
                "Yellow 25 ppm/K": "#FFFF00",
                "Green 20 ppm/K": "#008000",
                "Blue 10 ppm/K": "#0000FF",
                "Violet 5 ppm/K": "#800080",
                "Gray 1 ppm/K": "#808080"
            }
            colors.append(temperature_colors[self.temperature_combo.currentText()])

        return colors

    # ========== draw bands ==========
    def draw_resistor_bands(self, colors):

        pixmap = QPixmap("assets/resistor.png")
        painter = QPainter(pixmap)

        # X position of each band
        band_positions = {
            0: 210,  # Band 1
            1: 245,  # Band 2
            2: 280,  # Band 3
            3: 315,  # Multiplier
            4: 420,  # Tolerance
            5: 455   # Temperature coefficient
        }

        band_width = 12

        body_top = 108
        band_height = 135

        for i, color in enumerate(colors):
            x = band_positions[i]

            painter.setBrush(QColor(color))
            painter.setPen(Qt.NoPen)

            painter.drawRect(
                x - band_width // 2,
                body_top,
                band_width,
                band_height
            )

        painter.end()

        self.image_label.setPixmap(
            pixmap.scaled(
                500,
                250,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

    # ========== INFORMATION ==========
    def format_resistance(self, resistance):

        if resistance >= 1_000_000:

            value = resistance / 1_000_000
            return f"{value:g} MΩ"

        elif resistance >= 1_000:

            value = resistance / 1_000
            return f"{value:g} kΩ"

        else:

            return f"{resistance:g} Ω"

    def get_application_info(self, resistance):

        if resistance < 1:
            return (
                "Suitable for current sensing, "
                "shunt resistors and high-current "
                "applications."
            )

        elif resistance < 10:
            return (
                "Suitable for current sensing, "
                "current limiting and low-resistance "
                "power applications."
            )

        elif resistance < 100:
            return (
                "Suitable for transistor biasing, "
                "current limiting and low-resistance "
                "circuits."
            )

        elif resistance < 1_000:
            return (
                "Suitable for LED circuits, transistor "
                "biasing and general-purpose electronics."
            )

        elif resistance < 100_000:
            return (
                "Suitable for microcontroller circuits, "
                "sensor modules, LED circuits and "
                "general-purpose electronics."
            )

        elif resistance < 1_000_000:
            return (
                "Suitable for pull-up/pull-down resistors, "
                "signal circuits and sensor modules."
            )

        else:
            return (
                "Suitable for high-impedance signal circuits, "
                "voltage sensing and high-value pull-up "
                "applications."
            )

    def update_info(self, resistance, tolerance):

        # Calculate resistance range
        minimum = resistance * (1 - tolerance / 100)
        maximum = resistance * (1 + tolerance / 100)

        # Format values
        resistance_text = self.format_resistance(resistance)
        minimum_text = self.format_resistance(minimum)
        maximum_text = self.format_resistance(maximum)

        application = self.get_application_info(resistance)

        info = (f"⚠️ {application}")

        self.info_label.setText(info)

    # ========== calculate function ==========
    def calculate(self):

        # number of bands
        bands = int(self.bands_combo.currentText()[0])

        # Get first two digits
        digit1 = self.color_values[self.band1_combo.currentText()]
        digit2 = self.color_values[self.band2_combo.currentText()]

        # calculate base value
        if bands >= 5:
            digit3 = self.color_values[self.band3_combo.currentText()]

            base_value = (digit1 * 100 + digit2 * 10 + digit3)

        else:

            base_value = (digit1 * 10 + digit2)

        # get multiplier
        multiplier = self.multiplier_values[self.multiplier_combo.currentText()]

        # final resistance
        resistance = base_value * multiplier

        # get tolerance
        if bands >= 4:
            tolerance = self.tolerance_values[self.tolerance_combo.currentText()]
        else:
            # 3-band resistor → ±20%
            tolerance = 20

        resistance_text = self.format_resistance(resistance)
        # add tolerance
        resistance_text += f" ±{tolerance}%"

        # display result
        self.result_label.setText(f"Resistance:\n{resistance_text}")

        # draw resistor
        colors = self.get_selected_bands()
        self.draw_resistor_bands(colors)

        # update information
        self.update_info(resistance, tolerance)
