import sys
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pyqtgraph as pg
from scipy import integrate
import pandas as pd
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QToolBar, QAction
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter
import json
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QDialogButtonBox, QMenu
from PyQt5.QtWidgets import QToolBar, QSpinBox, QLabel
from numpy.linalg import inv
from cmath import rect, polar
import networkx as nx
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
from PyQt5.QtWidgets import QShortcut, QInputDialog, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QKeySequence

class GlassmorphicStyle:
    @staticmethod
    def apply(widget):
        widget.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 rgba(20, 20, 40, 0.95),
                    stop: 1 rgba(40, 40, 80, 0.95)
                );
            }
            QWidget {
                background-color: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                color: white;
            }
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 rgba(255, 255, 255, 0.1),
                    stop: 1 rgba(255, 255, 255, 0.05)
                );
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 8px 20px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 rgba(255, 255, 255, 0.2),
                    stop: 1 rgba(255, 255, 255, 0.1)
                );
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.15);
            }
            QLineEdit, QSpinBox, QDoubleSpinBox {
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 8px;
                color: white;
                selection-background-color: rgba(255, 255, 255, 0.2);
            }
            QComboBox {
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 8px;
                color: white;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QGroupBox {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 rgba(255, 255, 255, 0.08),
                    stop: 1 rgba(255, 255, 255, 0.05)
                );
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                margin-top: 1em;
                padding: 15px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                color: rgba(255, 255, 255, 0.8);
                background-color: rgba(40, 40, 80, 0.95);
            }
            QTabWidget::pane {
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                background-color: rgba(40, 40, 80, 0.95);
            }
            QTabBar::tab {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 rgba(255, 255, 255, 0.05),
                    stop: 1 rgba(255, 255, 255, 0.02)
                );
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 8px 15px;
                margin: 2px;
                color: rgba(255, 255, 255, 0.7);
            }
            QTabBar::tab:selected {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 rgba(255, 255, 255, 0.1),
                    stop: 1 rgba(255, 255, 255, 0.05)
                );
                color: white;
                font-weight: bold;
            }
            QGraphicsView {
                background: transparent;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
            }
            QTreeWidget {
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 5px;
            }
            QTreeWidget::item {
                padding: 5px;
                border-radius: 6px;
            }
            QTreeWidget::item:selected {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QTextEdit {
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 10px;
            }
            QToolBar {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 rgba(255, 255, 255, 0.05),
                    stop: 1 rgba(255, 255, 255, 0.02)
                );
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                spacing: 5px;
                padding: 5px;
            }
            QToolButton {
                background-color: transparent;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 5px;
            }
            QToolButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.05);
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.2);
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QSlider::groove:horizontal {
                border: 1px solid rgba(255, 255, 255, 0.1);
                height: 4px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 rgba(255, 255, 255, 0.8),
                    stop: 1 rgba(255, 255, 255, 0.6)
                );
                border: 1px solid rgba(255, 255, 255, 0.3);
                width: 16px;
                height: 16px;
                border-radius: 8px;
                margin: -6px 0;
            }
            QMenuBar {
                background: transparent;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            QMenuBar::item {
                background: transparent;
                padding: 8px 12px;
                border-radius: 6px;
            }
            QMenuBar::item:selected {
                background: rgba(255, 255, 255, 0.1);
            }
            QStatusBar {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 rgba(255, 255, 255, 0.05),
                    stop: 1 rgba(255, 255, 255, 0.02)
                );
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                color: rgba(255, 255, 255, 0.7);
            }
        """)

class PowerComponent:
    BUS = "bus"
    GENERATOR = "generator"
    LOAD = "load"
    TRANSFORMER = "transformer"
    LINE = "line"
    CAPACITOR = "capacitor"
    REACTOR = "reactor"
    SWITCH = "switch"
    BREAKER = "breaker"
    MEASUREMENT = "measurement"
    MOTOR = "motor"
    SOLAR = "solar"
    WIND = "wind"
    BATTERY = "battery"
    HVDC = "hvdc"

class NodeNumbering:
    def __init__(self):
        self.current_number = 1
        self.node_map = {}  # Maps components to node numbers
    
    def get_next_number(self):
        num = self.current_number
        self.current_number += 1
        return num
    
    def reset(self):
        self.current_number = 1
        self.node_map.clear()

class ComponentPropertiesDialog(QDialog):
    def __init__(self, component_type, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{component_type.title()} Properties")
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)
        
        # Create tab widget for different property categories
        tab_widget = QTabWidget()
        
        # Basic properties tab
        basic_tab = QWidget()
        form = QFormLayout(basic_tab)
        self.properties = {}
        
        if component_type == PowerComponent.BUS:
            # Basic Properties
            self.properties['name'] = QLineEdit("Bus 1")
            self.properties['voltage'] = QLineEdit("132")
            self.properties['type'] = QComboBox()
            self.properties['type'].addItems(["Slack", "PV", "PQ"])
            
            form.addRow("Bus Name:", self.properties['name'])
            form.addRow("Nominal Voltage (kV):", self.properties['voltage'])
            form.addRow("Bus Type:", self.properties['type'])
            
            # Advanced Properties
            self.properties['v_min'] = QLineEdit("0.95")
            self.properties['v_max'] = QLineEdit("1.05")
            self.properties['angle'] = QLineEdit("0.0")
            
            form.addRow("Minimum Voltage (p.u.):", self.properties['v_min'])
            form.addRow("Maximum Voltage (p.u.):", self.properties['v_max'])
            form.addRow("Initial Angle (degrees):", self.properties['angle'])
            
        elif component_type == PowerComponent.GENERATOR:
            # Basic Properties
            self.properties['name'] = QLineEdit("Gen 1")
            self.properties['power'] = QLineEdit("100")
            self.properties['voltage'] = QLineEdit("132")
            self.properties['pf'] = QLineEdit("0.85")
            
            form.addRow("Generator Name:", self.properties['name'])
            form.addRow("Active Power (MW):", self.properties['power'])
            form.addRow("Voltage (kV):", self.properties['voltage'])
            form.addRow("Power Factor:", self.properties['pf'])
            
            # Machine Parameters
            self.properties['xd'] = QLineEdit("1.5")
            self.properties['xq'] = QLineEdit("1.5")
            self.properties['xd_prime'] = QLineEdit("0.3")
            self.properties['h'] = QLineEdit("5.0")
            self.properties['d'] = QLineEdit("2.0")
            
            form.addRow("Direct Axis Reactance (p.u.):", self.properties['xd'])
            form.addRow("Quadrature Axis Reactance (p.u.):", self.properties['xq'])
            form.addRow("Transient Reactance (p.u.):", self.properties['xd_prime'])
            form.addRow("Inertia Constant (s):", self.properties['h'])
            form.addRow("Damping Coefficient:", self.properties['d'])
            
            # Operating Limits
            self.properties['p_max'] = QLineEdit("150")
            self.properties['p_min'] = QLineEdit("0")
            self.properties['q_max'] = QLineEdit("100")
            self.properties['q_min'] = QLineEdit("-100")
            
            form.addRow("Maximum Active Power (MW):", self.properties['p_max'])
            form.addRow("Minimum Active Power (MW):", self.properties['p_min'])
            form.addRow("Maximum Reactive Power (MVAR):", self.properties['q_max'])
            form.addRow("Minimum Reactive Power (MVAR):", self.properties['q_min'])
            
        elif component_type == PowerComponent.LOAD:
            # Basic Properties
            self.properties['name'] = QLineEdit("Load 1")
            self.properties['power'] = QLineEdit("50")
            self.properties['pf'] = QLineEdit("0.9")
            
            form.addRow("Load Name:", self.properties['name'])
            form.addRow("Active Power (MW):", self.properties['power'])
            form.addRow("Power Factor:", self.properties['pf'])
            
            # Load Model Parameters
            self.properties['model_type'] = QComboBox()
            self.properties['model_type'].addItems([
                "Constant Power", "Constant Current", 
                "Constant Impedance", "ZIP Model"
            ])
            self.properties['voltage_dependency'] = QLineEdit("1.0")
            self.properties['frequency_dependency'] = QLineEdit("0.0")
            
            form.addRow("Load Model:", self.properties['model_type'])
            form.addRow("Voltage Dependency:", self.properties['voltage_dependency'])
            form.addRow("Frequency Dependency:", self.properties['frequency_dependency'])
            
            # ZIP Model Parameters (if applicable)
            self.properties['z_percent'] = QLineEdit("30")
            self.properties['i_percent'] = QLineEdit("30")
            self.properties['p_percent'] = QLineEdit("40")
            
            form.addRow("Constant Z Component (%):", self.properties['z_percent'])
            form.addRow("Constant I Component (%):", self.properties['i_percent'])
            form.addRow("Constant P Component (%):", self.properties['p_percent'])
            
        elif component_type == PowerComponent.TRANSFORMER:
            # Basic Properties
            self.properties['name'] = QLineEdit("Tx 1")
            self.properties['rating'] = QLineEdit("100")
            self.properties['primary'] = QLineEdit("132")
            self.properties['secondary'] = QLineEdit("33")
            
            form.addRow("Transformer Name:", self.properties['name'])
            form.addRow("Rating (MVA):", self.properties['rating'])
            form.addRow("Primary Voltage (kV):", self.properties['primary'])
            form.addRow("Secondary Voltage (kV):", self.properties['secondary'])
            
            # Impedance Parameters
            self.properties['r'] = QLineEdit("0.02")
            self.properties['x'] = QLineEdit("0.08")
            self.properties['b'] = QLineEdit("0.0")
            self.properties['g'] = QLineEdit("0.0")
            
            form.addRow("Resistance (p.u.):", self.properties['r'])
            form.addRow("Reactance (p.u.):", self.properties['x'])
            form.addRow("Charging Susceptance (p.u.):", self.properties['b'])
            form.addRow("Conductance (p.u.):", self.properties['g'])
            
            # Tap Changer Properties
            self.properties['tap_pos'] = QSpinBox()
            self.properties['tap_pos'].setRange(-16, 16)
            self.properties['tap_pos'].setValue(0)
            self.properties['tap_step'] = QLineEdit("1.25")
            self.properties['tap_side'] = QComboBox()
            self.properties['tap_side'].addItems(["Primary", "Secondary"])
            
            form.addRow("Tap Position:", self.properties['tap_pos'])
            form.addRow("Tap Step Size (%):", self.properties['tap_step'])
            form.addRow("Tap Side:", self.properties['tap_side'])
            
        elif component_type == PowerComponent.LINE:
            # Basic Properties
            self.properties['name'] = QLineEdit("Line 1")
            self.properties['length'] = QLineEdit("10")
            self.properties['voltage'] = QLineEdit("132")
            
            form.addRow("Line Name:", self.properties['name'])
            form.addRow("Length (km):", self.properties['length'])
            form.addRow("Nominal Voltage (kV):", self.properties['voltage'])
            
            # Line Parameters
            self.properties['r1'] = QLineEdit("0.1")
            self.properties['x1'] = QLineEdit("0.4")
            self.properties['b1'] = QLineEdit("0.003")
            self.properties['r0'] = QLineEdit("0.3")
            self.properties['x0'] = QLineEdit("1.2")
            self.properties['b0'] = QLineEdit("0.002")
            
            form.addRow("Positive Sequence R (Ω/km):", self.properties['r1'])
            form.addRow("Positive Sequence X (Ω/km):", self.properties['x1'])
            form.addRow("Positive Sequence B (μS/km):", self.properties['b1'])
            form.addRow("Zero Sequence R (Ω/km):", self.properties['r0'])
            form.addRow("Zero Sequence X (Ω/km):", self.properties['x0'])
            form.addRow("Zero Sequence B (μS/km):", self.properties['b0'])
            
            # Thermal Limits
            self.properties['i_max'] = QLineEdit("800")
            self.properties['s_max'] = QLineEdit("200")
            
            form.addRow("Maximum Current (A):", self.properties['i_max'])
            form.addRow("Maximum Power (MVA):", self.properties['s_max'])
        
        # Add the form to a scroll area
        scroll = QScrollArea()
        scroll.setWidget(basic_tab)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        # Add buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def get_properties(self):
        """Get properties as dictionary"""
        result = {}
        for key, widget in self.properties.items():
            if isinstance(widget, QComboBox):
                result[key] = widget.currentText()
            elif isinstance(widget, QSpinBox):
                result[key] = str(widget.value())
            else:
                result[key] = widget.text()
        return result

    def create_generator_properties(self, form):
        """Create detailed generator properties"""
        # Basic Properties Tab
        basic_group = QGroupBox("Basic Properties")
        basic_layout = QFormLayout()
        
        self.properties['name'] = QLineEdit("Gen 1")
        self.properties['power'] = QLineEdit("100")
        self.properties['voltage'] = QLineEdit("132")
        self.properties['pf'] = QLineEdit("0.85")
        self.properties['type'] = QComboBox()
        self.properties['type'].addItems(["Synchronous", "Induction", "Inverter-Based"])
        
        basic_layout.addRow("Generator Name:", self.properties['name'])
        basic_layout.addRow("Rated Power (MVA):", self.properties['power'])
        basic_layout.addRow("Rated Voltage (kV):", self.properties['voltage'])
        basic_layout.addRow("Power Factor:", self.properties['pf'])
        basic_layout.addRow("Generator Type:", self.properties['type'])
        basic_group.setLayout(basic_layout)
        form.addWidget(basic_group)
        
        # Machine Parameters Tab
        machine_group = QGroupBox("Machine Parameters")
        machine_layout = QFormLayout()
        
        self.properties['xd'] = QLineEdit("1.5")
        self.properties['xq'] = QLineEdit("1.5")
        self.properties['xd_prime'] = QLineEdit("0.3")
        self.properties['xq_prime'] = QLineEdit("0.3")
        self.properties['xd_dprime'] = QLineEdit("0.2")
        self.properties['xq_dprime'] = QLineEdit("0.2")
        self.properties['xl'] = QLineEdit("0.15")
        self.properties['ra'] = QLineEdit("0.003")
        
        machine_layout.addRow("Direct Axis Reactance (Xd):", self.properties['xd'])
        machine_layout.addRow("Quadrature Axis Reactance (Xq):", self.properties['xq'])
        machine_layout.addRow("Transient Reactance X'd:", self.properties['xd_prime'])
        machine_layout.addRow("Transient Reactance X'q:", self.properties['xq_prime'])
        machine_layout.addRow("Subtransient Reactance X''d:", self.properties['xd_dprime'])
        machine_layout.addRow("Subtransient Reactance X''q:", self.properties['xq_dprime'])
        machine_layout.addRow("Leakage Reactance (Xl):", self.properties['xl'])
        machine_layout.addRow("Armature Resistance (Ra):", self.properties['ra'])
        machine_group.setLayout(machine_layout)
        form.addWidget(machine_group)
        
        # Time Constants Tab
        time_group = QGroupBox("Time Constants")
        time_layout = QFormLayout()
        
        self.properties['td0_prime'] = QLineEdit("6.0")
        self.properties['tq0_prime'] = QLineEdit("0.5")
        self.properties['td0_dprime'] = QLineEdit("0.05")
        self.properties['tq0_dprime'] = QLineEdit("0.05")
        self.properties['ta'] = QLineEdit("0.2")
        
        time_layout.addRow("D-axis Transient T'd0 (s):", self.properties['td0_prime'])
        time_layout.addRow("Q-axis Transient T'q0 (s):", self.properties['tq0_prime'])
        time_layout.addRow("D-axis Subtransient T''d0 (s):", self.properties['td0_dprime'])
        time_layout.addRow("Q-axis Subtransient T''q0 (s):", self.properties['tq0_dprime'])
        time_layout.addRow("Armature Time Constant (s):", self.properties['ta'])
        time_group.setLayout(time_layout)
        form.addWidget(time_group)
        
        # Mechanical Parameters
        mech_group = QGroupBox("Mechanical Parameters")
        mech_layout = QFormLayout()
        
        self.properties['h'] = QLineEdit("5.0")
        self.properties['d'] = QLineEdit("2.0")
        self.properties['poles'] = QSpinBox()
        self.properties['poles'].setRange(2, 32)
        self.properties['poles'].setValue(2)
        
        mech_layout.addRow("Inertia Constant H (s):", self.properties['h'])
        mech_layout.addRow("Damping Coefficient D:", self.properties['d'])
        mech_layout.addRow("Number of Poles:", self.properties['poles'])
        mech_group.setLayout(mech_layout)
        form.addWidget(mech_group)

    def create_transformer_properties(self, form):
        """Create detailed transformer properties"""
        # Basic Properties Tab
        basic_group = QGroupBox("Basic Properties")
        basic_layout = QFormLayout()
        
        self.properties['name'] = QLineEdit("Tx 1")
        self.properties['rating'] = QLineEdit("100")
        self.properties['primary'] = QLineEdit("132")
        self.properties['secondary'] = QLineEdit("33")
        self.properties['type'] = QComboBox()
        self.properties['type'].addItems([
            "Two-Winding", "Three-Winding", 
            "Auto-Transformer", "Phase Shifting"
        ])
        self.properties['connection'] = QComboBox()
        self.properties['connection'].addItems([
            "Wye-Wye", "Delta-Delta", 
            "Wye-Delta", "Delta-Wye"
        ])
        
        basic_layout.addRow("Transformer Name:", self.properties['name'])
        basic_layout.addRow("Rating (MVA):", self.properties['rating'])
        basic_layout.addRow("Primary Voltage (kV):", self.properties['primary'])
        basic_layout.addRow("Secondary Voltage (kV):", self.properties['secondary'])
        basic_layout.addRow("Transformer Type:", self.properties['type'])
        basic_layout.addRow("Connection Type:", self.properties['connection'])
        basic_group.setLayout(basic_layout)
        form.addWidget(basic_group)
        
        # Impedance Parameters
        imp_group = QGroupBox("Impedance Parameters")
        imp_layout = QFormLayout()
        
        self.properties['r'] = QLineEdit("0.02")
        self.properties['x'] = QLineEdit("0.08")
        self.properties['r0'] = QLineEdit("0.02")
        self.properties['x0'] = QLineEdit("0.08")
        self.properties['b'] = QLineEdit("0.0")
        self.properties['g'] = QLineEdit("0.0")
        
        imp_layout.addRow("Positive Sequence R (p.u.):", self.properties['r'])
        imp_layout.addRow("Positive Sequence X (p.u.):", self.properties['x'])
        imp_layout.addRow("Zero Sequence R (p.u.):", self.properties['r0'])
        imp_layout.addRow("Zero Sequence X (p.u.):", self.properties['x0'])
        imp_layout.addRow("Magnetizing B (p.u.):", self.properties['b'])
        imp_layout.addRow("Core Loss G (p.u.):", self.properties['g'])
        imp_group.setLayout(imp_layout)
        form.addWidget(imp_group)
        
        # Tap Changer Properties
        tap_group = QGroupBox("Tap Changer")
        tap_layout = QFormLayout()
        
        self.properties['tap_side'] = QComboBox()
        self.properties['tap_side'].addItems(["Primary", "Secondary"])
        self.properties['tap_pos'] = QSpinBox()
        self.properties['tap_pos'].setRange(-16, 16)
        self.properties['tap_pos'].setValue(0)
        self.properties['tap_step'] = QLineEdit("1.25")
        self.properties['tap_min'] = QLineEdit("0.9")
        self.properties['tap_max'] = QLineEdit("1.1")
        self.properties['tap_neutral'] = QLineEdit("1.0")
        
        tap_layout.addRow("Tap Side:", self.properties['tap_side'])
        tap_layout.addRow("Tap Position:", self.properties['tap_pos'])
        tap_layout.addRow("Step Size (%):", self.properties['tap_step'])
        tap_layout.addRow("Minimum Tap:", self.properties['tap_min'])
        tap_layout.addRow("Maximum Tap:", self.properties['tap_max'])
        tap_layout.addRow("Neutral Tap:", self.properties['tap_neutral'])
        tap_group.setLayout(tap_layout)
        form.addWidget(tap_group)
        
        # Grounding Properties
        ground_group = QGroupBox("Grounding")
        ground_layout = QFormLayout()
        
        self.properties['ground_primary'] = QComboBox()
        self.properties['ground_primary'].addItems([
            "Solid", "Resistance", "Reactance", "Ungrounded"
        ])
        self.properties['ground_secondary'] = QComboBox()
        self.properties['ground_secondary'].addItems([
            "Solid", "Resistance", "Reactance", "Ungrounded"
        ])
        self.properties['ground_r'] = QLineEdit("0.0")
        self.properties['ground_x'] = QLineEdit("0.0")
        
        ground_layout.addRow("Primary Grounding:", self.properties['ground_primary'])
        ground_layout.addRow("Secondary Grounding:", self.properties['ground_secondary'])
        ground_layout.addRow("Grounding Resistance (Ω):", self.properties['ground_r'])
        ground_layout.addRow("Grounding Reactance (Ω):", self.properties['ground_x'])
        ground_group.setLayout(ground_layout)
        form.addWidget(ground_group)

    def create_component_tabs(self, component_type):
        """Create tabbed interface for component properties"""
        tab_widget = QTabWidget()
        
        # Basic Properties Tab
        basic_tab = QWidget()
        basic_layout = QFormLayout(basic_tab)
        tab_widget.addTab(basic_tab, "Basic")
        
        # Advanced Properties Tab
        advanced_tab = QWidget()
        advanced_layout = QFormLayout(advanced_tab)
        tab_widget.addTab(advanced_tab, "Advanced")
        
        # Protection Settings Tab
        protection_tab = QWidget()
        protection_layout = QFormLayout(protection_tab)
        tab_widget.addTab(protection_tab, "Protection")
        
        # Cost & Maintenance Tab
        maintenance_tab = QWidget()
        maintenance_layout = QFormLayout(maintenance_tab)
        tab_widget.addTab(maintenance_tab, "Maintenance")
        
        if component_type == PowerComponent.CAPACITOR:
            self.setup_capacitor_properties(basic_layout, advanced_layout, protection_layout, maintenance_layout)
        elif component_type == PowerComponent.REACTOR:
            self.setup_reactor_properties(basic_layout, advanced_layout, protection_layout, maintenance_layout)
        elif component_type == PowerComponent.SWITCH:
            self.setup_switch_properties(basic_layout, advanced_layout, protection_layout, maintenance_layout)
        elif component_type == PowerComponent.BREAKER:
            self.setup_breaker_properties(basic_layout, advanced_layout, protection_layout, maintenance_layout)
        elif component_type == PowerComponent.MOTOR:
            self.setup_motor_properties(basic_layout, advanced_layout, protection_layout, maintenance_layout)
        elif component_type == PowerComponent.SOLAR:
            self.setup_solar_properties(basic_layout, advanced_layout, protection_layout, maintenance_layout)
        elif component_type == PowerComponent.WIND:
            self.setup_wind_properties(basic_layout, advanced_layout, protection_layout, maintenance_layout)
        elif component_type == PowerComponent.BATTERY:
            self.setup_battery_properties(basic_layout, advanced_layout, protection_layout, maintenance_layout)
        elif component_type == PowerComponent.HVDC:
            self.setup_hvdc_properties(basic_layout, advanced_layout, protection_layout, maintenance_layout)
        
        return tab_widget

    def setup_capacitor_properties(self, basic, advanced, protection, maintenance):
        # Basic Properties
        self.properties['name'] = QLineEdit("Cap 1")
        self.properties['rating'] = QLineEdit("10")
        self.properties['voltage'] = QLineEdit("132")
        self.properties['type'] = QComboBox()
        self.properties['type'].addItems(["Fixed", "Switched", "Variable"])
        
        basic.addRow("Name:", self.properties['name'])
        basic.addRow("Rating (MVAR):", self.properties['rating'])
        basic.addRow("Voltage (kV):", self.properties['voltage'])
        basic.addRow("Type:", self.properties['type'])
        
        # Advanced Properties
        self.properties['q_max'] = QLineEdit("12")
        self.properties['q_min'] = QLineEdit("0")
        self.properties['steps'] = QSpinBox()
        self.properties['steps'].setRange(1, 12)
        
        advanced.addRow("Max Reactive Power (MVAR):", self.properties['q_max'])
        advanced.addRow("Min Reactive Power (MVAR):", self.properties['q_min'])
        advanced.addRow("Number of Steps:", self.properties['steps'])
        
        # Protection Settings
        self.properties['overvoltage'] = QLineEdit("1.1")
        self.properties['overcurrent'] = QLineEdit("1.3")
        
        protection.addRow("Overvoltage Setting (p.u.):", self.properties['overvoltage'])
        protection.addRow("Overcurrent Setting (p.u.):", self.properties['overcurrent'])
        
        # Maintenance
        self.properties['install_date'] = QDateEdit()
        self.properties['last_maintenance'] = QDateEdit()
        
        maintenance.addRow("Installation Date:", self.properties['install_date'])
        maintenance.addRow("Last Maintenance:", self.properties['last_maintenance'])

    def setup_motor_properties(self, basic, advanced, protection, maintenance):
        # Basic Properties
        self.properties['name'] = QLineEdit("Motor 1")
        self.properties['power'] = QLineEdit("500")
        self.properties['voltage'] = QLineEdit("400")
        self.properties['speed'] = QLineEdit("1500")
        
        basic.addRow("Name:", self.properties['name'])
        basic.addRow("Power Rating (kW):", self.properties['power'])
        basic.addRow("Voltage (V):", self.properties['voltage'])
        basic.addRow("Rated Speed (RPM):", self.properties['speed'])
        
        # Advanced Properties
        self.properties['efficiency'] = QLineEdit("95")
        self.properties['power_factor'] = QLineEdit("0.85")
        self.properties['inertia'] = QLineEdit("2.5")
        self.properties['service_factor'] = QLineEdit("1.15")
        
        advanced.addRow("Efficiency (%):", self.properties['efficiency'])
        advanced.addRow("Power Factor:", self.properties['power_factor'])
        advanced.addRow("Inertia Constant (H):", self.properties['inertia'])
        advanced.addRow("Service Factor:", self.properties['service_factor'])
        
        # Protection Settings
        self.properties['overload_setting'] = QLineEdit("115")
        self.properties['locked_rotor_time'] = QLineEdit("5")
        
        protection.addRow("Overload Setting (%):", self.properties['overload_setting'])
        protection.addRow("Locked Rotor Time (s):", self.properties['locked_rotor_time'])
        
        # Maintenance
        self.properties['operating_hours'] = QLineEdit("0")
        self.properties['maintenance_interval'] = QLineEdit("8760")
        
        maintenance.addRow("Operating Hours:", self.properties['operating_hours'])
        maintenance.addRow("Maintenance Interval (h):", self.properties['maintenance_interval'])

    # Add similar setup methods for other components...

class DiagramScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent  # Store reference to main window
        self.setSceneRect(0, 0, 800, 600)
        self.current_component = None
        self.drawing_line = False
        self.line_start = None
        self.components = []
        self.component_properties = {}
    
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.handle_right_click(event)
        elif self.current_component:
            pos = event.scenePos()
            item = self.draw_component(self.current_component, pos)
            if item:
                item.setFlag(QGraphicsItem.ItemIsMovable)
                item.setFlag(QGraphicsItem.ItemIsSelectable)
                # Record add operation
                if hasattr(self.parent(), 'record_operation'):
                    self.parent().record_operation('add', item)
        else:
            super().mousePressEvent(event)
    
    def handle_right_click(self, event):
        item = self.itemAt(event.scenePos(), QTransform())
        if item:
            menu = QMenu()
            
            # Add element type and name to menu title
            for comp_type, comp_item in self.components:
                if comp_item == item:
                    name = self.component_properties.get(item, {}).get('name', '')
                    if not name:
                        if comp_type == PowerComponent.BUS:
                            name = f"Bus {self.get_node_number(item)}"
                        else:
                            name = f"{comp_type.title()}"
                    menu.addSection(name)
                    break
            
            edit_action = menu.addAction("Edit Properties")
            delete_action = menu.addAction("Delete")
            delete_action.setIcon(QIcon.fromTheme("edit-delete"))
            
            # Add separator
            menu.addSeparator()
            
            # Add "Delete Connected Lines" option for non-line elements
            if any(comp_item == item and comp_type != PowerComponent.LINE 
                   for comp_type, comp_item in self.components):
                delete_lines_action = menu.addAction("Delete Connected Lines")
            else:
                delete_lines_action = None
            
            action = menu.exec_(event.screenPos())
            
            if action == edit_action:
                self.edit_component_properties(item)
            elif action == delete_action:
                if self.main_window:  # Check if main window reference exists
                    self.main_window.delete_element(item)
            elif delete_lines_action and action == delete_lines_action:
                if self.main_window:  # Check if main window reference exists
                    self.main_window.delete_connected_lines(item)
    
    def edit_component_properties(self, item):
        for comp_type, comp_item in self.components:
            if comp_item == item:
                dialog = ComponentPropertiesDialog(comp_type, None)
                if item in self.component_properties:
                    for key, widget in dialog.properties.items():
                        if key in self.component_properties[item]:
                            widget.setText(self.component_properties[item][key])
                
                if dialog.exec_() == QDialog.Accepted:
                    self.component_properties[item] = dialog.get_properties()
                break
    
    def remove_component(self, item):
        # Record delete operation before removing
        if hasattr(self.parent(), 'record_operation'):
            self.parent().record_operation('delete', item)
        
        self.removeItem(item)
        self.components = [(t, i) for t, i in self.components if i != item]
        if item in self.component_properties:
            del self.component_properties[item]
    
    def save_diagram(self, filename):
        diagram_data = {
            'components': [],
            'connections': []
        }
        
        for comp_type, item in self.components:
            if comp_type != 'line':
                pos = item.pos()
                component_data = {
                    'type': comp_type,
                    'x': pos.x(),
                    'y': pos.y(),
                    'properties': self.component_properties.get(item, {})
                }
                diagram_data['components'].append(component_data)
            else:
                line = item
                diagram_data['connections'].append({
                    'x1': line.line().x1(),
                    'y1': line.line().y1(),
                    'x2': line.line().x2(),
                    'y2': line.line().y2()
                })
        
        with open(filename, 'w') as f:
            json.dump(diagram_data, f)
    
    def load_diagram(self, filename):
        self.clear()
        self.components.clear()
        self.component_properties.clear()
        
        with open(filename, 'r') as f:
            diagram_data = json.load(f)
        
        for component in diagram_data['components']:
            pos = QPointF(component['x'], component['y'])
            self.current_component = component['type']
            self.draw_component(component['type'], pos)
            if self.components:
                _, item = self.components[-1]
                self.component_properties[item] = component['properties']
        
        for connection in diagram_data['connections']:
            line = self.addLine(
                connection['x1'], connection['y1'],
                connection['x2'], connection['y2'],
                QPen(Qt.white, 2))  # Added closing parenthesis here
            self.components.append(('line', line))
    
    def draw_component(self, component_type, pos):
        item = None
        if component_type == PowerComponent.BUS:
            item = self.addRect(pos.x()-25, pos.y()-5, 50, 10,
                              QPen(Qt.white), QBrush(Qt.transparent))
            self.add_node_number(item, pos)
            self.components.append((component_type, item))
            
        elif component_type == PowerComponent.GENERATOR:
            item = self.addEllipse(pos.x()-15, pos.y()-15, 30, 30,
                                 QPen(Qt.white), QBrush(Qt.transparent))
            text = self.addText("G", QFont("Arial", 10))
            text.setDefaultTextColor(Qt.white)
            text.setPos(pos.x()-5, pos.y()-10)
            text.setParentItem(item)  # Make text move with generator
            self.components.append((component_type, item))
            
        elif component_type == PowerComponent.LOAD:
            polygon = QPolygonF([
                QPointF(pos.x(), pos.y()-20),
                QPointF(pos.x()-20, pos.y()+20),
                QPointF(pos.x()+20, pos.y()+20)
            ])
            item = self.addPolygon(polygon, QPen(Qt.white), QBrush(Qt.transparent))
            self.components.append((component_type, item))
            
        elif component_type == PowerComponent.TRANSFORMER:
            # Create a group for transformer components
            group = QGraphicsItemGroup()
            self.addItem(group)
            
            # Add primary and secondary windings
            circle1 = self.addEllipse(pos.x()-20, pos.y()-10, 20, 20,
                                    QPen(Qt.white), QBrush(Qt.transparent))
            circle2 = self.addEllipse(pos.x(), pos.y()-10, 20, 20,
                                    QPen(Qt.white), QBrush(Qt.transparent))
            
            # Add to group
            group.addToGroup(circle1)
            group.addToGroup(circle2)
            
            item = group
            self.components.append((component_type, item))
            
        elif component_type == PowerComponent.LINE:
            if self.drawing_line:
                if self.line_start:
                    item = self.addLine(
                        self.line_start.x(), self.line_start.y(),
                        pos.x(), pos.y(),
                        QPen(Qt.white, 2)
                    )  # Fixed closing parenthesis
                    self.components.append(('line', item))
                    self.line_start = None
                    self.drawing_line = False
                else:
                    self.line_start = pos
                    return None
        
        if item:
            item.setFlag(QGraphicsItem.ItemIsMovable)
            item.setFlag(QGraphicsItem.ItemIsSelectable)
            item.setAcceptHoverEvents(True)
        
        return item
    
    def add_node_number(self, item, pos):
        if not hasattr(self, 'node_numbering'):
            self.node_numbering = NodeNumbering()
        
        number = self.node_numbering.get_next_number()
        text = self.addText(str(number))
        text.setDefaultTextColor(Qt.white)
        text.setPos(pos.x() + 25, pos.y() - 25)
        self.node_numbering.node_map[item] = number
        return number
    
    def get_node_number(self, item):
        if hasattr(self, 'node_numbering'):
            return self.node_numbering.node_map.get(item)
        return None
    
    def mouseMoveEvent(self, event):
        if self.drawing_line and self.line_start:
            # Show temporary line while drawing
            if hasattr(self, 'temp_line'):
                self.removeItem(self.temp_line)
            self.temp_line = self.addLine(
                self.line_start.x(), self.line_start.y(),
                event.scenePos().x(), event.scenePos().y(),
                QPen(Qt.white, 2, Qt.DashLine)
            )
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        if hasattr(self, 'temp_line'):
            self.removeItem(self.temp_line)
            delattr(self, 'temp_line')
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key_Delete:
            if self.selectedItems():
                self.parent().delete_element()
        super().keyPressEvent(event)

class PowerFlowSolver:
    def __init__(self, diagram_scene):
        self.scene = diagram_scene
        self.buses = []
        self.y_bus = None
        self.voltage_magnitudes = {}
        self.voltage_angles = {}
        self.power_injections = {}
        
    def build_ybus(self):
        """Build Y-bus matrix from components"""
        # Create graph to analyze connectivity
        G = nx.Graph()
        self.buses = []  # Clear existing buses
        
        # First pass: collect all buses
        for comp_type, item in self.scene.components:
            if comp_type == PowerComponent.BUS:
                bus_num = self.scene.get_node_number(item)
                if bus_num is not None:
                    G.add_node(bus_num)
                    self.buses.append(bus_num)
        
        # Sort buses to ensure consistent indexing
        self.buses.sort()
        n_buses = len(self.buses)
        
        # Initialize Y-bus matrix
        self.y_bus = np.zeros((n_buses, n_buses), dtype=complex)
        
        # Second pass: add lines
        for comp_type, item in self.scene.components:
            if comp_type == PowerComponent.LINE:
                line = item
                start_pos = QPointF(line.line().x1(), line.line().y1())
                end_pos = QPointF(line.line().x2(), line.line().y2())
                
                start_bus = None
                end_bus = None
                
                # Find connected buses
                for bus_type, bus_item in self.scene.components:
                    if bus_type == PowerComponent.BUS:
                        bus_pos = bus_item.pos()
                        if (abs(bus_pos.x() - start_pos.x()) < 30 and 
                            abs(bus_pos.y() - start_pos.y()) < 30):
                            start_bus = self.scene.get_node_number(bus_item)
                        elif (abs(bus_pos.x() - end_pos.x()) < 30 and 
                              abs(bus_pos.y() - end_pos.y()) < 30):
                            end_bus = self.scene.get_node_number(bus_item)
                
                if start_bus is not None and end_bus is not None:
                    # Get indices in Y-bus matrix
                    i = self.buses.index(start_bus)
                    j = self.buses.index(end_bus)
                    
                    # Use typical line impedance
                    z = complex(1, 1)  # 1 + j1 ohm
                    y = 1/z
                    
                    # Add to Y-bus matrix
                    self.y_bus[i, i] += y
                    self.y_bus[j, j] += y
                    self.y_bus[i, j] -= y
                    self.y_bus[j, i] -= y
    
    def run_newton_raphson(self, max_iter=100, tolerance=1e-5):
        """Run Newton-Raphson power flow"""
        n = len(self.buses)
        
        # Initialize voltage magnitudes and angles
        for bus_num in self.buses:
            self.voltage_magnitudes[bus_num] = 1.0  # p.u.
            self.voltage_angles[bus_num] = 0.0  # radians
            
        # Set slack bus (first bus)
        slack_bus = self.buses[0]
        self.voltage_magnitudes[slack_bus] = 1.0
        self.voltage_angles[slack_bus] = 0.0
        
        # Get specified P and Q
        self.get_power_injections()
        
        # Newton-Raphson iteration
        for iteration in range(max_iter):
            # Calculate power mismatches
            delta_p, delta_q = self.calculate_power_mismatches()
            
            if max(abs(delta_p)) < tolerance and max(abs(delta_q)) < tolerance:
                return True  # Converged
            
            # Form Jacobian
            j = self.form_jacobian()
            
            # Solve for voltage magnitude and angle corrections
            corrections = np.linalg.solve(j, np.concatenate([delta_p, delta_q]))
            
            # Update voltage magnitudes and angles
            for i, bus_num in enumerate(self.buses[1:]):  # Skip slack bus
                self.voltage_angles[bus_num] += corrections[i]
                self.voltage_magnitudes[bus_num] *= (1 + corrections[i + n-1])
        
        return False  # Did not converge
    
    def get_power_injections(self):
        """Get power injections from components"""
        self.power_injections.clear()
        
        for comp_type, item in self.scene.components:
            if comp_type in [PowerComponent.GENERATOR, PowerComponent.LOAD]:
                # Find connected bus
                comp_pos = item.pos()
                for bus_type, bus_item in self.scene.components:
                    if bus_type == PowerComponent.BUS:
                        bus_pos = bus_item.pos()
                        if (abs(bus_pos.x() - comp_pos.x()) < 30 and 
                            abs(bus_pos.y() - comp_pos.y()) < 30):
                            bus_num = self.scene.get_node_number(bus_item)
                            if bus_num is not None:
                                props = self.scene.component_properties.get(item, {})
                                p = float(props.get('power', 0))
                                pf = float(props.get('pf', 0.9))
                                q = p * np.tan(np.arccos(pf))
                                
                                if comp_type == PowerComponent.LOAD:
                                    p = -p
                                    q = -q
                                
                                if bus_num in self.power_injections:
                                    self.power_injections[bus_num][0] += p
                                    self.power_injections[bus_num][1] += q
                                else:
                                    self.power_injections[bus_num] = [p, q]
    
    def calculate_power_mismatches(self):
        """Calculate power mismatches for Newton-Raphson"""
        n = len(self.buses)
        delta_p = np.zeros(n-1)  # Skip slack bus
        delta_q = np.zeros(n-1)  # Skip slack bus
        
        for i in range(1, n):  # Skip slack bus
            bus_num = self.buses[i]
            v_i = self.voltage_magnitudes[bus_num]
            theta_i = self.voltage_angles[bus_num]
            
            # Calculate P and Q at this bus
            p_calc = 0
            q_calc = 0
            
            for j in range(n):
                other_bus = self.buses[j]
                v_j = self.voltage_magnitudes[other_bus]
                theta_j = self.voltage_angles[other_bus]
                y_ij = self.y_bus[i, j]
                
                angle_diff = theta_i - theta_j
                p_calc += v_i * v_j * abs(y_ij) * np.cos(angle_diff - np.angle(y_ij))
                q_calc += v_i * v_j * abs(y_ij) * np.sin(angle_diff - np.angle(y_ij))
            
            # Get specified P and Q
            p_spec, q_spec = self.power_injections.get(bus_num, [0, 0])
            
            # Calculate mismatches
            delta_p[i-1] = p_spec - p_calc
            delta_q[i-1] = q_spec - q_calc
        
        return delta_p, delta_q
    
    def form_jacobian(self):
        """Form Jacobian matrix for Newton-Raphson"""
        n = len(self.buses)
        j = np.zeros((2*(n-1), 2*(n-1)))  # Skip slack bus
        
        for i in range(n-1):  # Skip slack bus
            bus_i = self.buses[i+1]
            v_i = self.voltage_magnitudes[bus_i]
            theta_i = self.voltage_angles[bus_i]
            
            for k in range(n-1):  # Skip slack bus
                bus_k = self.buses[k+1]
                v_k = self.voltage_magnitudes[bus_k]
                theta_k = self.voltage_angles[bus_k]
                y_ik = self.y_bus[i+1, k+1]
                
                if i == k:  # Diagonal elements
                    # dP/dθ
                    j[i, i] = v_i * v_i * abs(y_ik) * np.sin(np.angle(y_ik))
                    for m in range(n):
                        if m != i+1:
                            v_m = self.voltage_magnitudes[self.buses[m]]
                            y_im = self.y_bus[i+1, m]
                            angle_diff = theta_i - self.voltage_angles[self.buses[m]]
                            j[i, i] += v_i * v_m * abs(y_im) * np.sin(angle_diff - np.angle(y_im))
                    
                    # dQ/dV
                    j[i+n-1, i+n-1] = -v_i * abs(y_ik) * np.cos(np.angle(y_ik))
                    for m in range(n):
                        if m != i+1:
                            v_m = self.voltage_magnitudes[self.buses[m]]
                            y_im = self.y_bus[i+1, m]
                            angle_diff = theta_i - self.voltage_angles[self.buses[m]]
                            j[i+n-1, i+n-1] -= v_m * abs(y_im) * np.cos(angle_diff - np.angle(y_im))
                
                else:  # Off-diagonal elements
                    angle_diff = theta_i - theta_k
                    # dP/dθ
                    j[i, k] = v_i * v_k * abs(y_ik) * np.sin(angle_diff - np.angle(y_ik))
                    # dQ/dV
                    j[i+n-1, k] = -v_i * v_k * abs(y_ik) * np.cos(angle_diff - np.angle(y_ik))
        
        return j

class StabilityAnalyzer:
    def __init__(self, solver):
        self.solver = solver
        self.swing_equation_results = {}
        self.critical_clearing_times = {}
        
    def run_transient_stability(self, fault_bus, clearing_time):
        H = 5.0  # Inertia constant (typical value)
        delta_0 = 0.0  # Initial rotor angle
        omega_0 = 2 * np.pi * 60  # Nominal frequency
        
        # Time array for simulation
        t = np.linspace(0, 2.0, 1000)
        dt = t[1] - t[0]
        
        # Initialize arrays
        delta = np.zeros_like(t)
        omega = np.zeros_like(t)
        delta[0] = delta_0
        omega[0] = omega_0
        
        # Simulate swing equation
        for i in range(1, len(t)):
            if t[i] < clearing_time:
                # During fault
                P_e = 0.0
            else:
                # After fault cleared
                P_e = self.calculate_electrical_power(delta[i-1])
            
            # Mechanical power (assumed constant)
            P_m = 1.0
            
            # Swing equation
            d2delta = (omega_0/(2*H))*(P_m - P_e)
            omega[i] = omega[i-1] + d2delta*dt
            delta[i] = delta[i-1] + omega[i]*dt
        
        self.swing_equation_results = {
            'time': t,
            'delta': delta,
            'omega': omega
        }
        
        # Check stability
        return max(abs(delta)) < np.pi  # System is stable if angle difference is less than 180°
    
    def calculate_electrical_power(self, delta):
        # Simplified electrical power calculation
        E = 1.0  # Internal voltage
        V = 1.0  # Terminal voltage
        X = 0.4  # Reactance
        return (E * V / X) * np.sin(delta)
    
    def find_critical_clearing_time(self, fault_bus, tolerance=0.01):
        t_min = 0.0
        t_max = 1.0
        
        while (t_max - t_min) > tolerance:
            t_mid = (t_min + t_max) / 2
            if self.run_transient_stability(fault_bus, t_mid):
                t_min = t_mid
            else:
                t_max = t_mid
        
        self.critical_clearing_times[fault_bus] = t_min
        return t_min

class ProtectionCoordinator:
    def __init__(self, solver):
        self.solver = solver
        self.relay_settings = {}
        
    def calculate_relay_settings(self, bus_num):
        # Get fault current
        i_fault = self.calculate_fault_current(bus_num)
        
        # Calculate pickup current (typically 1.5 times load current)
        i_pickup = 1.5 * self.get_load_current(bus_num)
        
        # Calculate time dial setting
        TDS = self.calculate_time_dial(i_fault, i_pickup)
        
        self.relay_settings[bus_num] = {
            'pickup_current': i_pickup,
            'time_dial': TDS,
            'fault_current': i_fault
        }
        
        return self.relay_settings[bus_num]
    
    def calculate_fault_current(self, bus_num):
        # Get pre-fault voltage
        V = self.solver.voltage_magnitudes[bus_num]
        
        # Assume typical fault impedance
        Z_f = complex(0.01, 0.01)
        
        return abs(V / Z_f)
    
    def get_load_current(self, bus_num):
        if bus_num in self.solver.power_injections:
            P, Q = self.solver.power_injections[bus_num]
            S = complex(P, Q)
            V = self.solver.voltage_magnitudes[bus_num]
            return abs(S / V)
        return 0.0
    
    def calculate_time_dial(self, i_fault, i_pickup):
        # Using standard inverse time characteristic
        M = i_fault / i_pickup
        if M > 1:
            return 0.14 / ((M**0.02) - 1)
        return 1.0

class UndoRedoStack:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []
        self.max_size = 50  # Maximum number of operations to store
    
    def push(self, operation):
        self.undo_stack.append(operation)
        self.redo_stack.clear()  # Clear redo stack when new operation is added
        
        # Keep stack size under control
        if len(self.undo_stack) > self.max_size:
            self.undo_stack.pop(0)
    
    def undo(self):
        if self.undo_stack:
            operation = self.undo_stack.pop()
            self.redo_stack.append(operation)
            return operation
        return None
    
    def redo(self):
        if self.redo_stack:
            operation = self.redo_stack.pop()
            self.undo_stack.append(operation)
            return operation
        return None

class PowerSystemSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Power System Simulator")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set background with blur effect
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Apply glassmorphic style directly
        GlassmorphicStyle.apply(self)
        
        # Initialize undo/redo stack
        self.undo_redo_stack = UndoRedoStack()
        
        # Setup keyboard shortcuts
        self.setup_shortcuts()
        
        # Initialize UI
        self.init_ui()

    def init_ui(self):
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        # Create left panel for controls
        left_panel = QWidget()
        self.left_layout = QVBoxLayout(left_panel)  # Store as instance variable
        
        # Add component tree at the top
        self.component_tree = QTreeWidget()
        self.component_tree.setHeaderLabel("Components")
        self.component_tree.itemClicked.connect(self.navigate_to_component)
        self.left_layout.addWidget(self.component_tree)
        
        # Create root items for component tree
        self.bus_root = QTreeWidgetItem(self.component_tree, ["Buses"])
        self.generator_root = QTreeWidgetItem(self.component_tree, ["Generators"])
        self.load_root = QTreeWidgetItem(self.component_tree, ["Loads"])
        self.transformer_root = QTreeWidgetItem(self.component_tree, ["Transformers"])
        
        # Circuit Parameters Group
        params_group = QGroupBox("Circuit Parameters")
        params_layout = QFormLayout()
        
        self.voltage_input = QLineEdit("230")
        self.current_input = QLineEdit("10")
        self.frequency_input = QLineEdit("50")
        self.resistance_input = QLineEdit("100")
        self.inductance_input = QLineEdit("0.5")
        self.capacitance_input = QLineEdit("0.001")
        
        params_layout.addRow("Voltage (V):", self.voltage_input)
        params_layout.addRow("Current (A):", self.current_input)
        params_layout.addRow("Frequency (Hz):", self.frequency_input)
        params_layout.addRow("Resistance (Ω):", self.resistance_input)
        params_layout.addRow("Inductance (H):", self.inductance_input)
        params_layout.addRow("Capacitance (F):", self.capacitance_input)
        
        params_group.setLayout(params_layout)
        self.left_layout.addWidget(params_group)

        # Analysis Controls
        analysis_group = QGroupBox("Analysis Controls")
        analysis_layout = QVBoxLayout()
        
        self.analysis_type = QComboBox()
        self.analysis_type.addItems(["Load Flow", "Short Circuit", "Transient", "Harmonics"])
        
        self.simulate_btn = QPushButton("Simulate")
        self.simulate_btn.clicked.connect(self.run_simulation)
        
        analysis_layout.addWidget(self.analysis_type)
        analysis_layout.addWidget(self.simulate_btn)
        
        analysis_group.setLayout(analysis_layout)
        self.left_layout.addWidget(analysis_group)
        
        # Add left panel to main layout
        layout.addWidget(left_panel, stretch=1)

        # Create right panel for results
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Graph widget
        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground('transparent')
        self.graph_widget.showGrid(x=True, y=True)
        right_layout.addWidget(self.graph_widget)
        
        # Results text area
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        right_layout.addWidget(self.results_text)
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # Create and add the existing analysis tab
        analysis_tab = QWidget()
        analysis_layout = QVBoxLayout(analysis_tab)
        analysis_layout.addWidget(self.graph_widget)
        analysis_layout.addWidget(self.results_text)
        tab_widget.addTab(analysis_tab, "Analysis")
        
        # Create and add the single line diagram tab
        diagram_tab = QWidget()
        diagram_layout = QVBoxLayout(diagram_tab)
        
        # Add toolbar for diagram components
        toolbar = QToolBar()
        
        # Add component buttons
        bus_action = QAction("Bus", self)
        bus_action.triggered.connect(lambda: self.set_current_component(PowerComponent.BUS))
        toolbar.addAction(bus_action)
        
        generator_action = QAction("Generator", self)
        generator_action.triggered.connect(lambda: self.set_current_component(PowerComponent.GENERATOR))
        toolbar.addAction(generator_action)
        
        load_action = QAction("Load", self)
        load_action.triggered.connect(lambda: self.set_current_component(PowerComponent.LOAD))
        toolbar.addAction(load_action)
        
        transformer_action = QAction("Transformer", self)
        transformer_action.triggered.connect(lambda: self.set_current_component(PowerComponent.TRANSFORMER))
        toolbar.addAction(transformer_action)
        
        line_action = QAction("Line", self)
        line_action.triggered.connect(lambda: self.set_current_component(PowerComponent.LINE))
        toolbar.addAction(line_action)
        
        # Add Save/Load buttons to toolbar
        toolbar.addSeparator()
        
        save_action = QAction("Save Diagram", self)
        save_action.triggered.connect(self.save_diagram)
        toolbar.addAction(save_action)
        
        load_action = QAction("Load Diagram", self)
        load_action.triggered.connect(self.load_diagram)
        toolbar.addAction(load_action)
        
        # Add stability analysis button
        stability_action = QAction("Stability Analysis", self)
        stability_action.triggered.connect(self.run_stability_analysis)
        toolbar.addAction(stability_action)
        
        # Add report generation button
        report_action = QAction("Generate Report", self)
        report_action.triggered.connect(self.generate_report)
        toolbar.addAction(report_action)
        
        # Add demo button to toolbar
        demo_action = QAction("Load Demo", self)
        demo_action.triggered.connect(self.setup_demo_system)
        toolbar.addAction(demo_action)
        
        diagram_layout.addWidget(toolbar)
        
        # Create diagram scene and view
        self.diagram_scene = DiagramScene(self)  # Pass self as parent
        self.diagram_view = QGraphicsView(self.diagram_scene)
        self.diagram_view.setRenderHint(QPainter.Antialiasing)
        self.diagram_view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.diagram_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.diagram_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.diagram_view.setBackgroundBrush(QBrush(QColor(53, 53, 53)))
        
        diagram_layout.addWidget(self.diagram_view)
        tab_widget.addTab(diagram_tab, "Single Line Diagram")
        
        # Add tab widget to right panel
        right_layout.addWidget(tab_widget)

        # Add right panel to main layout
        layout.addWidget(right_panel, stretch=2)

        # Add simulation toolbar
        sim_toolbar = self.create_simulation_toolbar()
        diagram_layout.addWidget(sim_toolbar)

    def run_simulation(self):
        try:
            # Get parameters
            V = float(self.voltage_input.text())
            I = float(self.current_input.text())
            f = float(self.frequency_input.text())
            R = float(self.resistance_input.text())
            L = float(self.inductance_input.text())
            C = float(self.capacitance_input.text())
            
            # Time array
            t = np.linspace(0, 0.1, 1000)
            
            # Different analysis based on selection
            analysis = self.analysis_type.currentText()
            
            if analysis == "Load Flow":
                self.run_load_flow(V, I, R)
            elif analysis == "Short Circuit":
                self.run_short_circuit(V, I, R, L)
            elif analysis == "Transient":
                self.run_transient(t, V, R, L, C)
            elif analysis == "Harmonics":
                self.run_harmonics(t, V, f)
                
        except ValueError as e:
            QMessageBox.warning(self, "Error", "Please enter valid numerical values.")

    def run_load_flow(self, V, I, R):
        # Simple load flow calculation
        P = V * I
        Q = V * I * 0.8  # Assuming power factor of 0.8
        S = np.sqrt(P**2 + Q**2)
        
        # Plot results
        self.graph_widget.clear()
        self.graph_widget.plot([0, 1], [0, P], pen='g', name='Active Power')
        self.graph_widget.plot([0, 1], [0, Q], pen='r', name='Reactive Power')
        
        # Update results text
        results = f"""Load Flow Results:
        Active Power (P): {P:.2f} W
        Reactive Power (Q): {Q:.2f} VAR
        Apparent Power (S): {S:.2f} VA
        """
        self.results_text.setText(results)

    def run_short_circuit(self, V, I, R, L):
        # Short circuit calculation
        Z = complex(R, 2*np.pi*50*L)
        I_sc = V/abs(Z)
        
        # Plot results
        t = np.linspace(0, 0.1, 1000)
        i_t = I_sc * np.exp(-R*t/(2*L)) * np.sin(2*np.pi*50*t)
        
        self.graph_widget.clear()
        self.graph_widget.plot(t, i_t, pen='y', name='Short Circuit Current')
        
        results = f"""Short Circuit Results:
        Short Circuit Current: {I_sc:.2f} A
        Impedance: {abs(Z):.2f} Ω
        """
        self.results_text.setText(results)

    def run_transient(self, t, V, R, L, C):
        # RLC circuit transient response
        omega = 1/np.sqrt(L*C)
        alpha = R/(2*L)
        
        if alpha < omega:  # Underdamped
            omega_d = np.sqrt(omega**2 - alpha**2)
            v_t = V * (1 - np.exp(-alpha*t) * np.cos(omega_d*t))
        else:  # Overdamped
            v_t = V * (1 - np.exp(-alpha*t))
            
        self.graph_widget.clear()
        self.graph_widget.plot(t, v_t, pen='b', name='Voltage')
        
        results = f"""Transient Analysis Results:
        Natural Frequency: {omega/(2*np.pi):.2f} Hz
        Damping Factor: {alpha:.2f}
        """
        self.results_text.setText(results)

    def run_harmonics(self, t, V, f):
        # Generate harmonics up to 5th order
        fundamental = V * np.sin(2*np.pi*f*t)
        h3 = 0.2 * V * np.sin(2*np.pi*3*f*t)  # 3rd harmonic
        h5 = 0.1 * V * np.sin(2*np.pi*5*f*t)  # 5th harmonic
        
        total = fundamental + h3 + h5
        
        self.graph_widget.clear()
        self.graph_widget.plot(t, fundamental, pen='b', name='Fundamental')
        self.graph_widget.plot(t, total, pen='r', name='With Harmonics')
        
        results = """Harmonics Analysis Results:
        Included up to 5th harmonic
        3rd Harmonic: 20% of fundamental
        5th Harmonic: 10% of fundamental
        """
        self.results_text.setText(results)

    def set_current_component(self, component_type):
        self.diagram_scene.current_component = component_type
        if component_type == PowerComponent.LINE:
            self.diagram_scene.drawing_line = True
            self.diagram_scene.line_start = None

    def save_diagram(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Diagram", "",
            "Power System Diagram (*.psd);;All Files (*)"
        )
        if filename:
            self.diagram_scene.save_diagram(filename)

    def load_diagram(self, filename):
        self.clear()
        self.components.clear()
        self.component_properties.clear()
        
        with open(filename, 'r') as f:
            diagram_data = json.load(f)
        
        for component in diagram_data['components']:
            pos = QPointF(component['x'], component['y'])
            self.current_component = component['type']
            self.draw_component(component['type'], pos)
            if self.components:
                _, item = self.components[-1]
                self.component_properties[item] = component['properties']
        
        for connection in diagram_data['connections']:
            line = self.addLine(
                connection['x1'], connection['y1'],
                connection['x2'], connection['y2'],
                QPen(Qt.white, 2))  # Added closing parenthesis here
            self.components.append(('line', line))
    
    def draw_component(self, component_type, pos):
        item = None
        if component_type == PowerComponent.BUS:
            item = self.addRect(pos.x()-25, pos.y()-5, 50, 10,
                              QPen(Qt.white), QBrush(Qt.transparent))
            self.add_node_number(item, pos)
            self.components.append((component_type, item))
            
        elif component_type == PowerComponent.GENERATOR:
            item = self.addEllipse(pos.x()-15, pos.y()-15, 30, 30,
                                 QPen(Qt.white), QBrush(Qt.transparent))
            text = self.addText("G", QFont("Arial", 10))
            text.setDefaultTextColor(Qt.white)
            text.setPos(pos.x()-5, pos.y()-10)
            text.setParentItem(item)  # Make text move with generator
            self.components.append((component_type, item))
            
        elif component_type == PowerComponent.LOAD:
            polygon = QPolygonF([
                QPointF(pos.x(), pos.y()-20),
                QPointF(pos.x()-20, pos.y()+20),
                QPointF(pos.x()+20, pos.y()+20)
            ])
            item = self.addPolygon(polygon, QPen(Qt.white), QBrush(Qt.transparent))
            self.components.append((component_type, item))
            
        elif component_type == PowerComponent.TRANSFORMER:
            # Create a group for transformer components
            group = QGraphicsItemGroup()
            self.addItem(group)
            
            # Add primary and secondary windings
            circle1 = self.addEllipse(pos.x()-20, pos.y()-10, 20, 20,
                                    QPen(Qt.white), QBrush(Qt.transparent))
            circle2 = self.addEllipse(pos.x(), pos.y()-10, 20, 20,
                                    QPen(Qt.white), QBrush(Qt.transparent))
            
            # Add to group
            group.addToGroup(circle1)
            group.addToGroup(circle2)
            
            item = group
            self.components.append((component_type, item))
            
        elif component_type == PowerComponent.LINE:
            if self.drawing_line:
                if self.line_start:
                    item = self.addLine(
                        self.line_start.x(), self.line_start.y(),
                        pos.x(), pos.y(),
                        QPen(Qt.white, 2)
                    )  # Fixed closing parenthesis
                    self.components.append(('line', item))
                    self.line_start = None
                    self.drawing_line = False
                else:
                    self.line_start = pos
                    return None
        
        if item:
            item.setFlag(QGraphicsItem.ItemIsMovable)
            item.setFlag(QGraphicsItem.ItemIsSelectable)
            item.setAcceptHoverEvents(True)
        
        return item
    
    def add_node_number(self, item, pos):
        if not hasattr(self, 'node_numbering'):
            self.node_numbering = NodeNumbering()
        
        number = self.node_numbering.get_next_number()
        text = self.addText(str(number))
        text.setDefaultTextColor(Qt.white)
        text.setPos(pos.x() + 25, pos.y() - 25)
        self.node_numbering.node_map[item] = number
        return number
    
    def get_node_number(self, item):
        if hasattr(self, 'node_numbering'):
            return self.node_numbering.node_map.get(item)
        return None
    
    def mouseMoveEvent(self, event):
        if self.drawing_line and self.line_start:
            # Show temporary line while drawing
            if hasattr(self, 'temp_line'):
                self.removeItem(self.temp_line)
            self.temp_line = self.addLine(
                self.line_start.x(), self.line_start.y(),
                event.scenePos().x(), event.scenePos().y(),
                QPen(Qt.white, 2, Qt.DashLine)
            )
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        if hasattr(self, 'temp_line'):
            self.removeItem(self.temp_line)
            delattr(self, 'temp_line')
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key_Delete:
            if self.selectedItems():
                self.parent().delete_element()
        super().keyPressEvent(event)

class PowerFlowSolver:
    def __init__(self, diagram_scene):
        self.scene = diagram_scene
        self.buses = []
        self.y_bus = None
        self.voltage_magnitudes = {}
        self.voltage_angles = {}
        self.power_injections = {}
        
    def build_ybus(self):
        """Build Y-bus matrix from components"""
        # Create graph to analyze connectivity
        G = nx.Graph()
        self.buses = []  # Clear existing buses
        
        # First pass: collect all buses
        for comp_type, item in self.scene.components:
            if comp_type == PowerComponent.BUS:
                bus_num = self.scene.get_node_number(item)
                if bus_num is not None:
                    G.add_node(bus_num)
                    self.buses.append(bus_num)
        
        # Sort buses to ensure consistent indexing
        self.buses.sort()
        n_buses = len(self.buses)
        
        # Initialize Y-bus matrix
        self.y_bus = np.zeros((n_buses, n_buses), dtype=complex)
        
        # Second pass: add lines
        for comp_type, item in self.scene.components:
            if comp_type == PowerComponent.LINE:
                line = item
                start_pos = QPointF(line.line().x1(), line.line().y1())
                end_pos = QPointF(line.line().x2(), line.line().y2())
                
                start_bus = None
                end_bus = None
                
                # Find connected buses
                for bus_type, bus_item in self.scene.components:
                    if bus_type == PowerComponent.BUS:
                        bus_pos = bus_item.pos()
                        if (abs(bus_pos.x() - start_pos.x()) < 30 and 
                            abs(bus_pos.y() - start_pos.y()) < 30):
                            start_bus = self.scene.get_node_number(bus_item)
                        elif (abs(bus_pos.x() - end_pos.x()) < 30 and 
                              abs(bus_pos.y() - end_pos.y()) < 30):
                            end_bus = self.scene.get_node_number(bus_item)
                
                if start_bus is not None and end_bus is not None:
                    # Get indices in Y-bus matrix
                    i = self.buses.index(start_bus)
                    j = self.buses.index(end_bus)
                    
                    # Use typical line impedance
                    z = complex(1, 1)  # 1 + j1 ohm
                    y = 1/z
                    
                    # Add to Y-bus matrix
                    self.y_bus[i, i] += y
                    self.y_bus[j, j] += y
                    self.y_bus[i, j] -= y
                    self.y_bus[j, i] -= y
    
    def run_newton_raphson(self, max_iter=100, tolerance=1e-5):
        """Run Newton-Raphson power flow"""
        n = len(self.buses)
        
        # Initialize voltage magnitudes and angles
        for bus_num in self.buses:
            self.voltage_magnitudes[bus_num] = 1.0  # p.u.
            self.voltage_angles[bus_num] = 0.0  # radians
            
        # Set slack bus (first bus)
        slack_bus = self.buses[0]
        self.voltage_magnitudes[slack_bus] = 1.0
        self.voltage_angles[slack_bus] = 0.0
        
        # Get specified P and Q
        self.get_power_injections()
        
        # Newton-Raphson iteration
        for iteration in range(max_iter):
            # Calculate power mismatches
            delta_p, delta_q = self.calculate_power_mismatches()
            
            if max(abs(delta_p)) < tolerance and max(abs(delta_q)) < tolerance:
                return True  # Converged
            
            # Form Jacobian
            j = self.form_jacobian()
            
            # Solve for voltage magnitude and angle corrections
            corrections = np.linalg.solve(j, np.concatenate([delta_p, delta_q]))
            
            # Update voltage magnitudes and angles
            for i, bus_num in enumerate(self.buses[1:]):  # Skip slack bus
                self.voltage_angles[bus_num] += corrections[i]
                self.voltage_magnitudes[bus_num] *= (1 + corrections[i + n-1])
        
        return False  # Did not converge
    
    def get_power_injections(self):
        """Get power injections from components"""
        self.power_injections.clear()
        
        for comp_type, item in self.scene.components:
            if comp_type in [PowerComponent.GENERATOR, PowerComponent.LOAD]:
                # Find connected bus
                comp_pos = item.pos()
                for bus_type, bus_item in self.scene.components:
                    if bus_type == PowerComponent.BUS:
                        bus_pos = bus_item.pos()
                        if (abs(bus_pos.x() - comp_pos.x()) < 30 and 
                            abs(bus_pos.y() - comp_pos.y()) < 30):
                            bus_num = self.scene.get_node_number(bus_item)
                            if bus_num is not None:
                                props = self.scene.component_properties.get(item, {})
                                p = float(props.get('power', 0))
                                pf = float(props.get('pf', 0.9))
                                q = p * np.tan(np.arccos(pf))
                                
                                if comp_type == PowerComponent.LOAD:
                                    p = -p
                                    q = -q
                                
                                if bus_num in self.power_injections:
                                    self.power_injections[bus_num][0] += p
                                    self.power_injections[bus_num][1] += q
                                else:
                                    self.power_injections[bus_num] = [p, q]
    
    def calculate_power_mismatches(self):
        """Calculate power mismatches for Newton-Raphson"""
        n = len(self.buses)
        delta_p = np.zeros(n-1)  # Skip slack bus
        delta_q = np.zeros(n-1)  # Skip slack bus
        
        for i in range(1, n):  # Skip slack bus
            bus_num = self.buses[i]
            v_i = self.voltage_magnitudes[bus_num]
            theta_i = self.voltage_angles[bus_num]
            
            # Calculate P and Q at this bus
            p_calc = 0
            q_calc = 0
            
            for j in range(n):
                other_bus = self.buses[j]
                v_j = self.voltage_magnitudes[other_bus]
                theta_j = self.voltage_angles[other_bus]
                y_ij = self.y_bus[i, j]
                
                angle_diff = theta_i - theta_j
                p_calc += v_i * v_j * abs(y_ij) * np.cos(angle_diff - np.angle(y_ij))
                q_calc += v_i * v_j * abs(y_ij) * np.sin(angle_diff - np.angle(y_ij))
            
            # Get specified P and Q
            p_spec, q_spec = self.power_injections.get(bus_num, [0, 0])
            
            # Calculate mismatches
            delta_p[i-1] = p_spec - p_calc
            delta_q[i-1] = q_spec - q_calc
        
        return delta_p, delta_q
    
    def form_jacobian(self):
        """Form Jacobian matrix for Newton-Raphson"""
        n = len(self.buses)
        j = np.zeros((2*(n-1), 2*(n-1)))  # Skip slack bus
        
        for i in range(n-1):  # Skip slack bus
            bus_i = self.buses[i+1]
            v_i = self.voltage_magnitudes[bus_i]
            theta_i = self.voltage_angles[bus_i]
            
            for k in range(n-1):  # Skip slack bus
                bus_k = self.buses[k+1]
                v_k = self.voltage_magnitudes[bus_k]
                theta_k = self.voltage_angles[bus_k]
                y_ik = self.y_bus[i+1, k+1]
                
                if i == k:  # Diagonal elements
                    # dP/dθ
                    j[i, i] = v_i * v_i * abs(y_ik) * np.sin(np.angle(y_ik))
                    for m in range(n):
                        if m != i+1:
                            v_m = self.voltage_magnitudes[self.buses[m]]
                            y_im = self.y_bus[i+1, m]
                            angle_diff = theta_i - self.voltage_angles[self.buses[m]]
                            j[i, i] += v_i * v_m * abs(y_im) * np.sin(angle_diff - np.angle(y_im))
                    
                    # dQ/dV
                    j[i+n-1, i+n-1] = -v_i * abs(y_ik) * np.cos(np.angle(y_ik))
                    for m in range(n):
                        if m != i+1:
                            v_m = self.voltage_magnitudes[self.buses[m]]
                            y_im = self.y_bus[i+1, m]
                            angle_diff = theta_i - self.voltage_angles[self.buses[m]]
                            j[i+n-1, i+n-1] -= v_m * abs(y_im) * np.cos(angle_diff - np.angle(y_im))
                
                else:  # Off-diagonal elements
                    angle_diff = theta_i - theta_k
                    # dP/dθ
                    j[i, k] = v_i * v_k * abs(y_ik) * np.sin(angle_diff - np.angle(y_ik))
                    # dQ/dV
                    j[i+n-1, k] = -v_i * v_k * abs(y_ik) * np.cos(angle_diff - np.angle(y_ik))
        
        return j

class StabilityAnalyzer:
    def __init__(self, solver):
        self.solver = solver
        self.swing_equation_results = {}
        self.critical_clearing_times = {}
        
    def run_transient_stability(self, fault_bus, clearing_time):
        H = 5.0  # Inertia constant (typical value)
        delta_0 = 0.0  # Initial rotor angle
        omega_0 = 2 * np.pi * 60  # Nominal frequency
        
        # Time array for simulation
        t = np.linspace(0, 2.0, 1000)
        dt = t[1] - t[0]
        
        # Initialize arrays
        delta = np.zeros_like(t)
        omega = np.zeros_like(t)
        delta[0] = delta_0
        omega[0] = omega_0
        
        # Simulate swing equation
        for i in range(1, len(t)):
            if t[i] < clearing_time:
                # During fault
                P_e = 0.0
            else:
                # After fault cleared
                P_e = self.calculate_electrical_power(delta[i-1])
            
            # Mechanical power (assumed constant)
            P_m = 1.0
            
            # Swing equation
            d2delta = (omega_0/(2*H))*(P_m - P_e)
            omega[i] = omega[i-1] + d2delta*dt
            delta[i] = delta[i-1] + omega[i]*dt
        
        self.swing_equation_results = {
            'time': t,
            'delta': delta,
            'omega': omega
        }
        
        # Check stability
        return max(abs(delta)) < np.pi  # System is stable if angle difference is less than 180°
    
    def calculate_electrical_power(self, delta):
        # Simplified electrical power calculation
        E = 1.0  # Internal voltage
        V = 1.0  # Terminal voltage
        X = 0.4  # Reactance
        return (E * V / X) * np.sin(delta)
    
    def find_critical_clearing_time(self, fault_bus, tolerance=0.01):
        t_min = 0.0
        t_max = 1.0
        
        while (t_max - t_min) > tolerance:
            t_mid = (t_min + t_max) / 2
            if self.run_transient_stability(fault_bus, t_mid):
                t_min = t_mid
            else:
                t_max = t_mid
        
        self.critical_clearing_times[fault_bus] = t_min
        return t_min

class ProtectionCoordinator:
    def __init__(self, solver):
        self.solver = solver
        self.relay_settings = {}
        
    def calculate_relay_settings(self, bus_num):
        # Get fault current
        i_fault = self.calculate_fault_current(bus_num)
        
        # Calculate pickup current (typically 1.5 times load current)
        i_pickup = 1.5 * self.get_load_current(bus_num)
        
        # Calculate time dial setting
        TDS = self.calculate_time_dial(i_fault, i_pickup)
        
        self.relay_settings[bus_num] = {
            'pickup_current': i_pickup,
            'time_dial': TDS,
            'fault_current': i_fault
        }
        
        return self.relay_settings[bus_num]
    
    def calculate_fault_current(self, bus_num):
        # Get pre-fault voltage
        V = self.solver.voltage_magnitudes[bus_num]
        
        # Assume typical fault impedance
        Z_f = complex(0.01, 0.01)
        
        return abs(V / Z_f)
    
    def get_load_current(self, bus_num):
        if bus_num in self.solver.power_injections:
            P, Q = self.solver.power_injections[bus_num]
            S = complex(P, Q)
            V = self.solver.voltage_magnitudes[bus_num]
            return abs(S / V)
        return 0.0
    
    def calculate_time_dial(self, i_fault, i_pickup):
        # Using standard inverse time characteristic
        M = i_fault / i_pickup
        if M > 1:
            return 0.14 / ((M**0.02) - 1)
        return 1.0

class UndoRedoStack:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []
        self.max_size = 50  # Maximum number of operations to store
    
    def push(self, operation):
        self.undo_stack.append(operation)
        self.redo_stack.clear()  # Clear redo stack when new operation is added
        
        # Keep stack size under control
        if len(self.undo_stack) > self.max_size:
            self.undo_stack.pop(0)
    
    def undo(self):
        if self.undo_stack:
            operation = self.undo_stack.pop()
            self.redo_stack.append(operation)
            return operation
        return None
    
    def redo(self):
        if self.redo_stack:
            operation = self.redo_stack.pop()
            self.undo_stack.append(operation)
            return operation
        return None

class PowerSystemSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Power System Simulator")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set background with blur effect
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Apply glassmorphic style directly
        GlassmorphicStyle.apply(self)
        
        # Initialize undo/redo stack
        self.undo_redo_stack = UndoRedoStack()
        
        # Setup keyboard shortcuts
        self.setup_shortcuts()
        
        # Initialize UI
        self.init_ui()

    def init_ui(self):
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        # Create left panel for controls
        left_panel = QWidget()
        self.left_layout = QVBoxLayout(left_panel)  # Store as instance variable
        
        # Add component tree at the top
        self.component_tree = QTreeWidget()
        self.component_tree.setHeaderLabel("Components")
        self.component_tree.itemClicked.connect(self.navigate_to_component)
        self.left_layout.addWidget(self.component_tree)
        
        # Create root items for component tree
        self.bus_root = QTreeWidgetItem(self.component_tree, ["Buses"])
        self.generator_root = QTreeWidgetItem(self.component_tree, ["Generators"])
        self.load_root = QTreeWidgetItem(self.component_tree, ["Loads"])
        self.transformer_root = QTreeWidgetItem(self.component_tree, ["Transformers"])
        
        # Circuit Parameters Group
        params_group = QGroupBox("Circuit Parameters")
        params_layout = QFormLayout()
        
        self.voltage_input = QLineEdit("230")
        self.current_input = QLineEdit("10")
        self.frequency_input = QLineEdit("50")
        self.resistance_input = QLineEdit("100")
        self.inductance_input = QLineEdit("0.5")
        self.capacitance_input = QLineEdit("0.001")
        
        params_layout.addRow("Voltage (V):", self.voltage_input)
        params_layout.addRow("Current (A):", self.current_input)
        params_layout.addRow("Frequency (Hz):", self.frequency_input)
        params_layout.addRow("Resistance (Ω):", self.resistance_input)
        params_layout.addRow("Inductance (H):", self.inductance_input)
        params_layout.addRow("Capacitance (F):", self.capacitance_input)
        
        params_group.setLayout(params_layout)
        self.left_layout.addWidget(params_group)

        # Analysis Controls
        analysis_group = QGroupBox("Analysis Controls")
        analysis_layout = QVBoxLayout()
        
        self.analysis_type = QComboBox()
        self.analysis_type.addItems(["Load Flow", "Short Circuit", "Transient", "Harmonics"])
        
        self.simulate_btn = QPushButton("Simulate")
        self.simulate_btn.clicked.connect(self.run_simulation)
        
        analysis_layout.addWidget(self.analysis_type)
        analysis_layout.addWidget(self.simulate_btn)
        
        analysis_group.setLayout(analysis_layout)
        self.left_layout.addWidget(analysis_group)
        
        # Add left panel to main layout
        layout.addWidget(left_panel, stretch=1)

        # Create right panel for results
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Graph widget
        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground('transparent')
        self.graph_widget.showGrid(x=True, y=True)
        right_layout.addWidget(self.graph_widget)
        
        # Results text area
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        right_layout.addWidget(self.results_text)
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # Create and add the existing analysis tab
        analysis_tab = QWidget()
        analysis_layout = QVBoxLayout(analysis_tab)
        analysis_layout.addWidget(self.graph_widget)
        analysis_layout.addWidget(self.results_text)
        tab_widget.addTab(analysis_tab, "Analysis")
        
        # Create and add the single line diagram tab
        diagram_tab = QWidget()
        diagram_layout = QVBoxLayout(diagram_tab)
        
        # Add toolbar for diagram components
        toolbar = QToolBar()
        
        # Add component buttons
        bus_action = QAction("Bus", self)
        bus_action.triggered.connect(lambda: self.set_current_component(PowerComponent.BUS))
        toolbar.addAction(bus_action)
        
        generator_action = QAction("Generator", self)
        generator_action.triggered.connect(lambda: self.set_current_component(PowerComponent.GENERATOR))
        toolbar.addAction(generator_action)
        
        load_action = QAction("Load", self)
        load_action.triggered.connect(lambda: self.set_current_component(PowerComponent.LOAD))
        toolbar.addAction(load_action)
        
        transformer_action = QAction("Transformer", self)
        transformer_action.triggered.connect(lambda: self.set_current_component(PowerComponent.TRANSFORMER))
        toolbar.addAction(transformer_action)
        
        line_action = QAction("Line", self)
        line_action.triggered.connect(lambda: self.set_current_component(PowerComponent.LINE))
        toolbar.addAction(line_action)
        
        # Add Save/Load buttons to toolbar
        toolbar.addSeparator()
        
        save_action = QAction("Save Diagram", self)
        save_action.triggered.connect(self.save_diagram)
        toolbar.addAction(save_action)
        
        load_action = QAction("Load Diagram", self)
        load_action.triggered.connect(self.load_diagram)
        toolbar.addAction(load_action)
        
        # Add stability analysis button
        stability_action = QAction("Stability Analysis", self)
        stability_action.triggered.connect(self.run_stability_analysis)
        toolbar.addAction(stability_action)
        
        # Add report generation button
        report_action = QAction("Generate Report", self)
        report_action.triggered.connect(self.generate_report)
        toolbar.addAction(report_action)
        
        # Add demo button to toolbar
        demo_action = QAction("Load Demo", self)
        demo_action.triggered.connect(self.setup_demo_system)
        toolbar.addAction(demo_action)
        
        diagram_layout.addWidget(toolbar)
        
        # Create diagram scene and view
        self.diagram_scene = DiagramScene(self)  # Pass self as parent
        self.diagram_view = QGraphicsView(self.diagram_scene)
        self.diagram_view.setRenderHint(QPainter.Antialiasing)
        self.diagram_view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.diagram_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.diagram_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.diagram_view.setBackgroundBrush(QBrush(QColor(53, 53, 53)))
        
        diagram_layout.addWidget(self.diagram_view)
        tab_widget.addTab(diagram_tab, "Single Line Diagram")
        
        # Add tab widget to right panel
        right_layout.addWidget(tab_widget)

        # Add right panel to main layout
        layout.addWidget(right_panel, stretch=2)

        # Add simulation toolbar
        sim_toolbar = self.create_simulation_toolbar()
        diagram_layout.addWidget(sim_toolbar)

    def run_simulation(self):
        try:
            # Get parameters
            V = float(self.voltage_input.text())
            I = float(self.current_input.text())
            f = float(self.frequency_input.text())
            R = float(self.resistance_input.text())
            L = float(self.inductance_input.text())
            C = float(self.capacitance_input.text())
            
            # Time array
            t = np.linspace(0, 0.1, 1000)
            
            # Different analysis based on selection
            analysis = self.analysis_type.currentText()
            
            if analysis == "Load Flow":
                self.run_load_flow(V, I, R)
            elif analysis == "Short Circuit":
                self.run_short_circuit(V, I, R, L)
            elif analysis == "Transient":
                self.run_transient(t, V, R, L, C)
            elif analysis == "Harmonics":
                self.run_harmonics(t, V, f)
                
        except ValueError as e:
            QMessageBox.warning(self, "Error", "Please enter valid numerical values.")

    def run_load_flow(self, V, I, R):
        # Simple load flow calculation
        P = V * I
        Q = V * I * 0.8  # Assuming power factor of 0.8
        S = np.sqrt(P**2 + Q**2)
        
        # Plot results
        self.graph_widget.clear()
        self.graph_widget.plot([0, 1], [0, P], pen='g', name='Active Power')
        self.graph_widget.plot([0, 1], [0, Q], pen='r', name='Reactive Power')
        
        # Update results text
        results = f"""Load Flow Results:
        Active Power (P): {P:.2f} W
        Reactive Power (Q): {Q:.2f} VAR
        Apparent Power (S): {S:.2f} VA
        """
        self.results_text.setText(results)

    def run_short_circuit(self, V, I, R, L):
        # Short circuit calculation
        Z = complex(R, 2*np.pi*50*L)
        I_sc = V/abs(Z)
        
        # Plot results
        t = np.linspace(0, 0.1, 1000)
        i_t = I_sc * np.exp(-R*t/(2*L)) * np.sin(2*np.pi*50*t)
        
        self.graph_widget.clear()
        self.graph_widget.plot(t, i_t, pen='y', name='Short Circuit Current')
        
        results = f"""Short Circuit Results:
        Short Circuit Current: {I_sc:.2f} A
        Impedance: {abs(Z):.2f} Ω
        """
        self.results_text.setText(results)

    def run_transient(self, t, V, R, L, C):
        # RLC circuit transient response
        omega = 1/np.sqrt(L*C)
        alpha = R/(2*L)
        
        if alpha < omega:  # Underdamped
            omega_d = np.sqrt(omega**2 - alpha**2)
            v_t = V * (1 - np.exp(-alpha*t) * np.cos(omega_d*t))
        else:  # Overdamped
            v_t = V * (1 - np.exp(-alpha*t))
            
        self.graph_widget.clear()
        self.graph_widget.plot(t, v_t, pen='b', name='Voltage')
        
        results = f"""Transient Analysis Results:
        Natural Frequency: {omega/(2*np.pi):.2f} Hz
        Damping Factor: {alpha:.2f}
        """
        self.results_text.setText(results)

    def run_harmonics(self, t, V, f):
        # Generate harmonics up to 5th order
        fundamental = V * np.sin(2*np.pi*f*t)
        h3 = 0.2 * V * np.sin(2*np.pi*3*f*t)  # 3rd harmonic
        h5 = 0.1 * V * np.sin(2*np.pi*5*f*t)  # 5th harmonic
        
        total = fundamental + h3 + h5
        
        self.graph_widget.clear()
        self.graph_widget.plot(t, fundamental, pen='b', name='Fundamental')
        self.graph_widget.plot(t, total, pen='r', name='With Harmonics')
        
        results = """Harmonics Analysis Results:
        Included up to 5th harmonic
        3rd Harmonic: 20% of fundamental
        5th Harmonic: 10% of fundamental
        """
        self.results_text.setText(results)

    def set_current_component(self, component_type):
        self.diagram_scene.current_component = component_type
        if component_type == PowerComponent.LINE:
            self.diagram_scene.drawing_line = True
            self.diagram_scene.line_start = None

    def save_diagram(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Diagram", "",
            "Power System Diagram (*.psd);;All Files (*)"
        )
        if filename:
            self.diagram_scene.save_diagram(filename)

    def load_diagram(self, filename):
        self.clear()
        self.components.clear()
        self.component_properties.clear()
        
        with open(filename, 'r') as f:
            diagram_data = json.load(f)
        
        for component in diagram_data['components']:
            pos = QPointF(component['x'], component['y'])
            self.current_component = component['type']
            self.draw_component(component['type'], pos)
            if self.components:
                _, item = self.components[-1]
                self.component_properties[item] = component['properties']
        
        for connection in diagram_data['connections']:
            line = self.addLine(
                connection['x1'], connection['y1'],
                connection['x2'], connection['y2'],
                QPen(Qt.white, 2))  # Added closing parenthesis here
            self.components.append(('line', line))
    
    def draw_component(self, component_type, pos):
        item = None
        if component_type == PowerComponent.BUS:
            item = self.addRect(pos.x()-25, pos.y()-5, 50, 10,
                              QPen(Qt.white), QBrush(Qt.transparent))
            self.add_node_number(item, pos)
            self.components.append((component_type, item))
            
        elif component_type == PowerComponent.GENERATOR:
            item = self.addEllipse(pos.x()-15, pos.y()-15, 30, 30,
                                 QPen(Qt.white), QBrush(Qt.transparent))
            text = self.addText("G", QFont("Arial", 10))
            text.setDefaultTextColor(Qt.white)
            text.setPos(pos.x()-5, pos.y()-10)
            text.setParentItem(item)  # Make text move with generator
            self.components.append((component_type, item))
            
        elif component_type == PowerComponent.LOAD:
            polygon = QPolygonF([
                QPointF(pos.x(), pos.y()-20),
                QPointF(pos.x()-20, pos.y()+20),
                QPointF(pos.x()+20, pos.y()+20)
            ])
            item = self.addPolygon(polygon, QPen(Qt.white), QBrush(Qt.transparent))
            self.components.append((component_type, item))
            
        elif component_type == PowerComponent.TRANSFORMER:
            # Create a group for transformer components
            group = QGraphicsItemGroup()
            self.addItem(group)
            
            # Add primary and secondary windings
            circle1 = self.addEllipse(pos.x()-20, pos.y()-10, 20, 20,
                                    QPen(Qt.white), QBrush(Qt.transparent))
            circle2 = self.addEllipse(pos.x(), pos.y()-10, 20, 20,
                                    QPen(Qt.white), QBrush(Qt.transparent))
            
            # Add to group
            group.addToGroup(circle1)
            group.addToGroup(circle2)
            
            item = group
            self.components.append((component_type, item))
            
        elif component_type == PowerComponent.LINE:
            if self.drawing_line:
                if self.line_start:
                    item = self.addLine(
                        self.line_start.x(), self.line_start.y(),
                        pos.x(), pos.y(),
                        QPen(Qt.white, 2)
                    )  # Fixed missing closing parenthesis
                    self.components.append(('line', item))
                    self.line_start = None
                    self.drawing_line = False
                else:
                    self.line_start = pos
                    return None
        
        if item:
            item.setFlag(QGraphicsItem.ItemIsMovable)
            item.setFlag(QGraphicsItem.ItemIsSelectable)
            item.setAcceptHoverEvents(True)
        
        return item
    
    def add_node_number(self, item, pos):
        if not hasattr(self, 'node_numbering'):
            self.node_numbering = NodeNumbering()
        
        number = self.node_numbering.get_next_number()
        text = self.addText(str(number))
        text.setDefaultTextColor(Qt.white)
        text.setPos(pos.x() + 25, pos.y() - 25)
        self.node_numbering.node_map[item] = number
        return number
    
    def get_node_number(self, item):
        if hasattr(self, 'node_numbering'):
            return self.node_numbering.node_map.get(item)
        return None
    
    def mouseMoveEvent(self, event):
        if self.drawing_line and self.line_start:
            # Show temporary line while drawing
            if hasattr(self, 'temp_line'):
                self.removeItem(self.temp_line)
            self.temp_line = self.addLine(
                self.line_start.x(), self.line_start.y(),
                event.scenePos().x(), event.scenePos().y(),
                QPen(Qt.white, 2, Qt.DashLine)
            )
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        if hasattr(self, 'temp_line'):
            self.removeItem(self.temp_line)
            delattr(self, 'temp_line')
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key_Delete:
            if self.selectedItems():
                self.parent().delete_element()
        super().keyPressEvent(event)

    def create_simulation_toolbar(self):
        sim_toolbar = QToolBar("Simulation Controls")
        
        # Add simulation step control
        step_label = QLabel("Time Step (ms):")
        sim_toolbar.addWidget(step_label)
        
        self.time_step = QSpinBox()
        self.time_step.setRange(1, 1000)
        self.time_step.setValue(100)
        sim_toolbar.addWidget(self.time_step)
        
        # Add simulation control buttons
        self.start_sim = QPushButton("Start Simulation")
        self.start_sim.clicked.connect(self.start_simulation)
        sim_toolbar.addWidget(self.start_sim)
        
        self.stop_sim = QPushButton("Stop Simulation")
        self.stop_sim.clicked.connect(self.stop_simulation)
        self.stop_sim.setEnabled(False)
        sim_toolbar.addWidget(self.stop_sim)
        
        # Add simulation speed control
        speed_label = QLabel("Speed:")
        sim_toolbar.addWidget(speed_label)
        
        self.sim_speed = QSpinBox()
        self.sim_speed.setRange(1, 10)
        self.sim_speed.setValue(1)
        sim_toolbar.addWidget(self.sim_speed)
        
        return sim_toolbar

    def start_simulation(self):
        self.simulation_running = True
        self.start_sim.setEnabled(False)
        self.stop_sim.setEnabled(True)
        self.simulate_power_flow()

    def stop_simulation(self):
        self.simulation_running = False
        self.start_sim.setEnabled(True)
        self.stop_sim.setEnabled(False)

    def simulate_power_flow(self):
        if not self.simulation_running:
            return
        
        try:
            # Clear previous visualizations
            self.clear_visualizations()
            
            # Run power flow analysis
            solver = PowerFlowSolver(self.diagram_scene)
            solver.build_ybus()
            
            if solver.run_newton_raphson():
                # Format and display results
                self.display_simulation_results(solver)
                
                # Update visualizations
                if hasattr(self, 'show_arrows') and self.show_arrows.isChecked():
                    self.visualize_power_flows(solver)
                if hasattr(self, 'show_values') and self.show_values.isChecked():
                    self.visualize_voltage_levels(solver)
                
                # Update graph
                self.update_voltage_profile(solver)
            else:
                self.results_text.setText("Simulation Error: Power flow did not converge")
                self.stop_simulation()
                return
            
        except Exception as e:
            self.results_text.setText(f"Simulation Error: {str(e)}")
            self.stop_simulation()
            return
        
        # Schedule next update if auto-update is enabled
        if self.simulation_running and hasattr(self, 'auto_update') and self.auto_update.isChecked():
            QTimer.singleShot(self.update_interval.value(), self.simulate_power_flow)

    def display_simulation_results(self, solver):
        """Format and display comprehensive simulation results"""
        results = "Power System Simulation Results\n"
        results += "=" * 40 + "\n\n"
        
        # Bus Results
        results += "Bus Results:\n"
        results += "-" * 20 + "\n"
        for bus_num in solver.buses:
            v_mag = solver.voltage_magnitudes[bus_num]
            v_ang = np.degrees(solver.voltage_angles[bus_num])
            status = self.get_voltage_status(v_mag)
            results += f"Bus {bus_num:2d}: {v_mag:.3f} pu ∠{v_ang:6.2f}° {status}\n"
        
        # Generator Results
        results += "\nGenerator Results:\n"
        results += "-" * 20 + "\n"
        for comp_type, item in self.diagram_scene.components:
            if comp_type == PowerComponent.GENERATOR:
                props = self.diagram_scene.component_properties.get(item, {})
                name = props.get('name', 'Generator')
                power = float(props.get('power', 0))
                pf = float(props.get('pf', 0.95))
                q = power * np.tan(np.arccos(pf))
                results += f"{name}:\n"
                results += f"  Active Power: {power:.2f} MW\n"
                results += f"  Reactive Power: {q:.2f} MVAR\n"
                results += f"  Power Factor: {pf:.3f}\n"
        
        # Load Results
        results += "\nLoad Results:\n"
        results += "-" * 20 + "\n"
        for comp_type, item in self.diagram_scene.components:
            if comp_type == PowerComponent.LOAD:
                props = self.diagram_scene.component_properties.get(item, {})
                name = props.get('name', 'Load')
                power = float(props.get('power', 0))
                pf = float(props.get('pf', 0.9))
                q = power * np.tan(np.arccos(pf))
                results += f"{name}:\n"
                results += f"  Active Power: {power:.2f} MW\n"
                results += f"  Reactive Power: {q:.2f} MVAR\n"
                results += f"  Power Factor: {pf:.3f}\n"
        
        # Line Results
        results += "\nTransmission Line Results:\n"
        results += "-" * 20 + "\n"
        for comp_type, item in self.diagram_scene.components:
            if comp_type == PowerComponent.LINE:
                line = item
                start_pos = QPointF(line.line().x1(), line.line().y1())
                end_pos = QPointF(line.line().x2(), line.line().y2())
                
                # Find connected buses
                start_bus = None
                end_bus = None
                for bus_type, bus_item in self.diagram_scene.components:
                    if bus_type == PowerComponent.BUS:
                        bus_pos = bus_item.pos()
                        if (abs(bus_pos.x() - start_pos.x()) < 30 and 
                            abs(bus_pos.y() - start_pos.y()) < 30):
                            start_bus = self.diagram_scene.get_node_number(bus_item)
                        elif (abs(bus_pos.x() - end_pos.x()) < 30 and 
                              abs(bus_pos.y() - end_pos.y()) < 30):
                            end_bus = self.diagram_scene.get_node_number(bus_item)
                
                if start_bus and end_bus:
                    # Calculate power flow through line
                    v1 = solver.voltage_magnitudes[start_bus]
                    v2 = solver.voltage_magnitudes[end_bus]
                    theta1 = solver.voltage_angles[start_bus]
                    theta2 = solver.voltage_angles[end_bus]
                    
                    # Assume typical line parameters if not specified
                    z = complex(1, 1)  # 1 + j1 ohm
                    y = 1/z
                    p_flow = v1 * v2 * abs(y) * np.sin(theta1 - theta2)
                    q_flow = v1 * v2 * abs(y) * np.cos(theta1 - theta2) - v1**2 * abs(y)
                    
                    results += f"Line {start_bus}-{end_bus}:\n"
                    results += f"  Active Power Flow: {p_flow:.2f} MW\n"
                    results += f"  Reactive Power Flow: {q_flow:.2f} MVAR\n"
                    results += f"  Loading: {abs(complex(p_flow, q_flow)):.1f}%\n"
        
        # System Summary
        results += "\nSystem Summary:\n"
        results += "-" * 20 + "\n"
        total_gen = sum(float(self.diagram_scene.component_properties.get(item, {}).get('power', 0))
                        for comp_type, item in self.diagram_scene.components
                        if comp_type == PowerComponent.GENERATOR)
        total_load = sum(float(self.diagram_scene.component_properties.get(item, {}).get('power', 0))
                         for comp_type, item in self.diagram_scene.components
                         if comp_type == PowerComponent.LOAD)
        total_loss = total_gen - total_load
        
        results += f"Total Generation: {total_gen:7.2f} MW\n"
        results += f"Total Load:      {total_load:7.2f} MW\n"
        results += f"System Losses:   {total_loss:7.2f} MW\n"
        results += f"System Efficiency: {(total_load/total_gen*100 if total_gen > 0 else 0):.1f}%\n"
        
        self.results_text.setText(results)

    def get_voltage_status(self, voltage):
        """Get voltage status indicator"""
        if voltage < 0.95:
            return "(Low) ⚠️"
        elif voltage > 1.05:
            return "(High) ⚠️"
        else:
            return "(Normal) ✓"

    def update_voltage_profile(self, solver):
        """Update voltage profile graph"""
        self.graph_widget.clear()
        
        # Plot voltage profile
        bus_numbers = list(range(1, len(solver.buses) + 1))
        voltages = [solver.voltage_magnitudes[bus] for bus in solver.buses]
        
        # Add voltage limits
        self.graph_widget.addLine(y=1.0, pen=pg.mkPen('w', style=Qt.DashLine))
        self.graph_widget.addLine(y=0.95, pen=pg.mkPen('r', style=Qt.DashLine))
        self.graph_widget.addLine(y=1.05, pen=pg.mkPen('r', style=Qt.DashLine))
        
        # Plot voltage magnitudes
        self.graph_widget.plot(bus_numbers, voltages, 
                              pen=pg.mkPen('g', width=2),
                              symbol='o',
                              symbolPen='g',
                              symbolBrush='g',
                              symbolSize=10,
                              name='Bus Voltages')
        
        # Set labels and title
        self.graph_widget.setLabel('left', 'Voltage (per unit)')
        self.graph_widget.setLabel('bottom', 'Bus Number')
        self.graph_widget.setTitle('System Voltage Profile')
        
        # Add grid
        self.graph_widget.showGrid(x=True, y=True, alpha=0.3)

    def visualize_power_flows(self, solver):
        """Visualize power flows between components"""
        arrow_scale = self.arrow_size_slider.value() / 100.0
        
        for comp_type, item in self.diagram_scene.components:
            if comp_type in [PowerComponent.GENERATOR, PowerComponent.LOAD]:
                props = self.diagram_scene.component_properties.get(item, {})
                if 'power' in props:
                    power = float(props['power'])
                    if comp_type == PowerComponent.LOAD:
                        power = -power
                    
                    # Draw power flow arrow
                    pos = item.pos()
                    arrow_length = min(50 * abs(power) / 100, 100) * arrow_scale
                    
                    # Color based on power magnitude
                    color = self.get_power_flow_color(power)
                    
                    # Create arrow
                    arrow = self.diagram_scene.addLine(
                        pos.x(), 
                        pos.y(),
                        pos.x() + arrow_length, 
                        pos.y(),
                        QPen(color, 2))  # Added closing parenthesis here
                    
                    # Add power value label if enabled
                    if self.show_values.isChecked():
                        self.add_power_flow_label(pos, power, color)
                    else:
                        # Optional: Add a simple indicator without value
                        self.add_direction_indicator(pos, power, color)

    def get_power_flow_color(self, power):
        """Get color based on power flow magnitude"""
        abs_power = abs(power)
        if abs_power > 100:
            return QColor(255, 0, 0, 200)  # Red for high power
        elif abs_power > 50:
            return QColor(255, 165, 0, 200)  # Orange for medium power
        else:
            return QColor(0, 255, 0, 200)  # Green for low power

    def clear_visualizations(self):
        """Clear previous visualizations"""
        for item in self.diagram_scene.items():
            if isinstance(item, (QGraphicsLineItem, QGraphicsPolygonItem, QGraphicsTextItem)):
                if item not in [comp[1] for comp in self.diagram_scene.components]:
                    self.diagram_scene.removeItem(item)

    def run_power_flow(self):
        """Run power flow analysis"""
        solver = PowerFlowSolver(self.diagram_scene)
        
        # Build Y-bus matrix
        solver.build_ybus()
        
        # Run Newton-Raphson
        if solver.run_newton_raphson():
            self.show_power_flow_results(solver)
        else:
            QMessageBox.warning(self, "Error", "Power flow did not converge")

    def show_power_flow_results(self, solver):
        """Display power flow results"""
        results = "Power Flow Results:\n\n"
        results += "Bus Voltages:\n"
        
        for bus_num in solver.buses:
            v_mag = solver.voltage_magnitudes[bus_num]
            v_ang = np.degrees(solver.voltage_angles[bus_num])
            results += f"Bus {bus_num}: {v_mag:.3f}∠{v_ang:.2f}°\n"
        
        results += "\nPower Injections:\n"
        for bus_num, (p, q) in solver.power_injections.items():
            results += f"Bus {bus_num}: P = {p:.2f} MW, Q = {q:.2f} MVAR\n"
        
        self.results_text.setText(results)
        
        # Visualize results on diagram
        self.visualize_voltage_levels(solver)

    def visualize_voltage_levels(self, solver):
        """Color buses based on voltage levels"""
        for comp_type, item in self.diagram_scene.components:
            if comp_type == PowerComponent.BUS:
                bus_num = self.diagram_scene.get_node_number(item)
                if bus_num is not None:
                    v_mag = solver.voltage_magnitudes[bus_num]
                    
                    # Color based on voltage magnitude
                    if v_mag < 0.95:
                        color = QColor(255, 0, 0, 150)  # Red for low voltage
                    elif v_mag > 1.05:
                        color = QColor(255, 165, 0, 150)  # Orange for high voltage
                    else:
                        color = QColor(0, 255, 0, 150)  # Green for normal voltage
                    
                    item.setPen(QPen(color, 2))

    def run_stability_analysis(self):
        """Run transient stability analysis"""
        try:
            # Get selected bus for fault
            fault_bus = None
            for comp_type, item in self.diagram_scene.components:
                if comp_type == PowerComponent.BUS and item.isSelected():
                    fault_bus = self.diagram_scene.get_node_number(item)
                    break
            
            if fault_bus is None:
                QMessageBox.warning(self, "Error", "Please select a bus for stability analysis")
                return
            
            # Run power flow first
            solver = PowerFlowSolver(self.diagram_scene)
            solver.build_ybus()
            
            if not solver.run_newton_raphson():
                QMessageBox.warning(self, "Error", "Power flow did not converge")
                return
            
            # Run stability analysis
            stability_analyzer = StabilityAnalyzer(solver)
            critical_time = stability_analyzer.find_critical_clearing_time(fault_bus)
            
            # Show results
            self.show_stability_results(fault_bus, critical_time, stability_analyzer)
            
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def show_stability_results(self, fault_bus, critical_time, analyzer):
        """Display stability analysis results"""
        results = f"Stability Analysis Results (Bus {fault_bus}):\n\n"
        results += f"Critical Clearing Time: {critical_time:.3f} seconds\n\n"
        
        # Plot swing curve
        self.graph_widget.clear()
        t = analyzer.swing_equation_results['time']
        delta = analyzer.swing_equation_results['delta']
        self.graph_widget.plot(t, np.degrees(delta), pen='b', name='Rotor Angle')
        
        self.results_text.setText(results)

    def generate_report(self):
        """Generate PDF report with analysis results"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Report", "",
            "PDF Files (*.pdf);;All Files (*)"
        )
        
        if filename:
            try:
                c = canvas.Canvas(filename, pagesize=letter)
                width, height = letter
                
                # Add header
                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, height - 50, "Power System Analysis Report")
                c.setFont("Helvetica", 12)
                c.drawString(50, height - 70, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Add analysis results
                y = height - 100
                c.setFont("Helvetica-Bold", 14)
                c.drawString(50, y, "Analysis Results")
                
                # Add results text
                y -= 20
                text = self.results_text.toPlainText()
                for line in text.split('\n'):
                    if y < 50:  # Start new page if needed
                        c.showPage()
                        y = height - 50
                    c.setFont("Helvetica", 12)
                    c.drawString(50, y, line)
                    y -= 15
                
                c.save()
                QMessageBox.information(self, "Success", "Report generated successfully")
                
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to generate report: {str(e)}")

    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # File operations
        QShortcut(QKeySequence("Ctrl+S"), self, self.save_diagram)
        QShortcut(QKeySequence("Ctrl+O"), self, self.load_diagram)
        QShortcut(QKeySequence("Ctrl+N"), self, self.new_diagram)
        
        # Edit operations
        QShortcut(QKeySequence("Ctrl+Z"), self, self.undo)
        QShortcut(QKeySequence("Ctrl+Y"), self, self.redo)
        QShortcut(QKeySequence("Delete"), self, self.delete_selected)
        
        # Component shortcuts
        QShortcut(QKeySequence("B"), self, lambda: self.set_current_component(PowerComponent.BUS))
        QShortcut(QKeySequence("G"), self, lambda: self.set_current_component(PowerComponent.GENERATOR))
        QShortcut(QKeySequence("L"), self, lambda: self.set_current_component(PowerComponent.LOAD))
        QShortcut(QKeySequence("T"), self, lambda: self.set_current_component(PowerComponent.TRANSFORMER))
        QShortcut(QKeySequence("C"), self, lambda: self.set_current_component(PowerComponent.LINE))
        
        # Analysis shortcuts
        QShortcut(QKeySequence("F5"), self, self.run_simulation)
        QShortcut(QKeySequence("F6"), self, self.run_power_flow)
        QShortcut(QKeySequence("F7"), self, self.run_stability_analysis)
        
        # Navigation
        QShortcut(QKeySequence("Ctrl+F"), self, self.search_components)

    def navigate_to_component(self, item):
        """Center view on selected component"""
        if item.parent():  # If it's not a root item
            # Find the component
            component_name = item.text(0)
            for comp_type, comp_item in self.diagram_scene.components:
                props = self.diagram_scene.component_properties.get(comp_item, {})
                if props.get('name', '') == component_name:
                    # Center view on component
                    self.diagram_view.centerOn(comp_item)
                    # Select the component
                    comp_item.setSelected(True)
                    break

    def search_components(self):
        """Search for components by name"""
        text, ok = QInputDialog.getText(self, "Search Components", "Enter component name:")
        if ok and text:
            found = False
            for comp_type, item in self.diagram_scene.components:
                props = self.diagram_scene.component_properties.get(item, {})
                name = props.get('name', '')
                if text.lower() in name.lower():
                    self.diagram_view.centerOn(item)
                    item.setSelected(True)
                    found = True
                    break
            
            if not found:
                QMessageBox.information(self, "Search Result", "No matching components found.")

    def new_diagram(self):
        """Create new diagram"""
        reply = QMessageBox.question(self, "New Diagram",
                                   "Are you sure you want to create a new diagram? Unsaved changes will be lost.",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.diagram_scene.clear()
            self.diagram_scene.components.clear()
            self.diagram_scene.component_properties.clear()
            if hasattr(self.diagram_scene, 'node_numbering'):
                self.diagram_scene.node_numbering.reset()
            self.update_component_tree()

    def delete_selected(self):
        """Delete selected components"""
        selected_items = self.diagram_scene.selectedItems()
        if selected_items:
            for item in selected_items:
                self.diagram_scene.remove_component(item)
            self.update_component_tree()

    def undo(self):
        """Undo last operation"""
        operation = self.undo_redo_stack.undo()
        if operation:
            if operation['type'] == 'add':
                # Remove the added component
                self.diagram_scene.remove_component(operation['item'])
            elif operation['type'] == 'delete':
                # Restore the deleted component
                self.diagram_scene.addItem(operation['item'])
                self.diagram_scene.components.append((operation['comp_type'], operation['item']))
                if 'properties' in operation:
                    self.diagram_scene.component_properties[operation['item']] = operation['properties']
            elif operation['type'] == 'move':
                # Restore previous position
                operation['item'].setPos(operation['old_pos'])
            
            self.update_component_tree()

    def redo(self):
        """Redo last undone operation"""
        operation = self.undo_redo_stack.redo()
        if operation:
            if operation['type'] == 'add':
                # Re-add the component
                self.diagram_scene.addItem(operation['item'])
                self.diagram_scene.components.append((operation['comp_type'], operation['item']))
                if 'properties' in operation:
                    self.diagram_scene.component_properties[operation['item']] = operation['properties']
            elif operation['type'] == 'delete':
                # Re-delete the component
                self.diagram_scene.remove_component(operation['item'])
            elif operation['type'] == 'move':
                # Restore new position
                operation['item'].setPos(operation['new_pos'])
            
            self.update_component_tree()

    def record_operation(self, operation_type, item, **kwargs):
        """Record an operation for undo/redo"""
        operation = {
            'type': operation_type,
            'item': item,
            'comp_type': next((t for t, i in self.diagram_scene.components if i == item), None),
        }
        
        if operation_type == 'add':
            if item in self.diagram_scene.component_properties:
                operation['properties'] = self.diagram_scene.component_properties[item].copy()
        elif operation_type == 'delete':
            if item in self.diagram_scene.component_properties:
                operation['properties'] = self.diagram_scene.component_properties[item].copy()
        elif operation_type == 'move':
            operation.update(kwargs)  # Should include 'old_pos' and 'new_pos'
        
        self.undo_redo_stack.push(operation)

    def update_component_tree(self):
        """Update component navigation tree"""
        # Clear existing items
        self.bus_root.takeChildren()
        self.generator_root.takeChildren()
        self.load_root.takeChildren()
        self.transformer_root.takeChildren()
        
        # Add components to tree
        for comp_type, item in self.diagram_scene.components:
            props = self.diagram_scene.component_properties.get(item, {})
            if comp_type == PowerComponent.BUS:
                name = props.get('name', f"Bus {self.diagram_scene.get_node_number(item)}")
                QTreeWidgetItem(self.bus_root, [name])
            elif comp_type == PowerComponent.GENERATOR:
                name = props.get('name', "Generator")
                QTreeWidgetItem(self.generator_root, [name])
            elif comp_type == PowerComponent.LOAD:
                name = props.get('name', "Load")
                QTreeWidgetItem(self.load_root, [name])
            elif comp_type == PowerComponent.TRANSFORMER:
                name = props.get('name', "Transformer")
                QTreeWidgetItem(self.transformer_root, [name])

    def setup_demo_system(self):
        """Create a demo power system"""
        # Create buses
        bus1_pos = QPointF(100, 100)
        bus2_pos = QPointF(300, 100)
        bus3_pos = QPointF(200, 250)
        
        bus1 = self.diagram_scene.draw_component(PowerComponent.BUS, bus1_pos)
        bus2 = self.diagram_scene.draw_component(PowerComponent.BUS, bus2_pos)
        bus3 = self.diagram_scene.draw_component(PowerComponent.BUS, bus3_pos)
        
        # Add generator at bus 1
        gen_pos = QPointF(50, 100)
        generator = self.diagram_scene.draw_component(PowerComponent.GENERATOR, gen_pos)
        self.diagram_scene.component_properties[generator] = {
            'name': 'Generator 1',
            'power': '100',
            'voltage': '132',
            'pf': '0.95'
        }
        
        # Add loads at bus 2 and 3
        load2_pos = QPointF(350, 100)
        load3_pos = QPointF(200, 300)
        
        load2 = self.diagram_scene.draw_component(PowerComponent.LOAD, load2_pos)
        load3 = self.diagram_scene.draw_component(PowerComponent.LOAD, load3_pos)
        
        self.diagram_scene.component_properties[load2] = {
            'name': 'Load 2',
            'power': '40',
            'pf': '0.9'
        }
        self.diagram_scene.component_properties[load3] = {
            'name': 'Load 3',
            'power': '30',
            'pf': '0.85'
        }
        
        # Connect components with lines
        self.diagram_scene.current_component = PowerComponent.LINE
        self.diagram_scene.drawing_line = True
        
        # Bus 1 to Bus 2
        self.diagram_scene.line_start = bus1_pos
        self.diagram_scene.draw_component(PowerComponent.LINE, bus2_pos)
        
        # Bus 2 to Bus 3
        self.diagram_scene.line_start = bus2_pos
        self.diagram_scene.draw_component(PowerComponent.LINE, bus3_pos)
        
        # Bus 1 to Bus 3
        self.diagram_scene.line_start = bus1_pos
        self.diagram_scene.draw_component(PowerComponent.LINE, bus3_pos)
        
        # Update component tree
        self.update_component_tree()
        
        # Add demo instructions
        demo_text = """Demo Power System:
        - Bus 1: Slack bus with generator (100 MW)
        - Bus 2: Load bus (40 MW)
        - Bus 3: Load bus (30 MW)
        
        To run simulation:
        1. Click 'Start Simulation' button
        2. Watch power flows and voltage levels
        3. Click 'Stop Simulation' to end
        
        Try these analyses:
        - Load Flow: Shows power distribution
        - Short Circuit: Fault analysis
        - Stability: System response to disturbances
        """
        self.results_text.setText(demo_text)

    def create_advanced_controls(self):
        """Create advanced control panel"""
        control_panel = QGroupBox("Advanced Controls")
        layout = QVBoxLayout()
        
        # Simulation Quality Control
        quality_group = QGroupBox("Simulation Quality")
        quality_layout = QFormLayout()
        
        self.iteration_count = QSpinBox()
        self.iteration_count.setRange(100, 10000)
        self.iteration_count.setValue(1000)
        quality_layout.addRow("Iterations:", self.iteration_count)
        
        self.tolerance = QDoubleSpinBox()
        self.tolerance.setRange(0.00001, 0.1)
        self.tolerance.setValue(0.00001)
        self.tolerance.setDecimals(5)
        quality_layout.addRow("Tolerance:", self.tolerance)
        
        quality_group.setLayout(quality_layout)
        layout.addWidget(quality_group)
        
        # Visualization Controls
        visual_group = QGroupBox("Visualization")
        visual_layout = QVBoxLayout()
        
        self.show_arrows = QCheckBox("Show Power Flow Arrows")
        self.show_arrows.setChecked(True)
        visual_layout.addWidget(self.show_arrows)
        
        self.show_values = QCheckBox("Show Values on Diagram")
        self.show_values.setChecked(True)
        visual_layout.addWidget(self.show_values)
        
        arrow_size_layout = QHBoxLayout()
        arrow_size_layout.addWidget(QLabel("Arrow Size:"))
        self.arrow_size_slider = QSlider(Qt.Horizontal)
        self.arrow_size_slider.setRange(50, 200)
        self.arrow_size_slider.setValue(100)
        arrow_size_layout.addWidget(self.arrow_size_slider)
        visual_layout.addLayout(arrow_size_layout)
        
        visual_group.setLayout(visual_layout)
        layout.addWidget(visual_group)
        
        # Analysis Options
        analysis_group = QGroupBox("Analysis Options")
        analysis_layout = QVBoxLayout()
        
        self.auto_update = QCheckBox("Auto Update Results")
        self.auto_update.setChecked(True)
        analysis_layout.addWidget(self.auto_update)
        
        update_interval_layout = QHBoxLayout()
        update_interval_layout.addWidget(QLabel("Update Interval (ms):"))
        self.update_interval = QSpinBox()
        self.update_interval.setRange(100, 5000)
        self.update_interval.setValue(1000)
        update_interval_layout.addWidget(self.update_interval)
        analysis_layout.addLayout(update_interval_layout)
        
        analysis_group.setLayout(analysis_layout)
        layout.addWidget(analysis_group)
        
        # Export Options
        export_group = QGroupBox("Export Options")
        export_layout = QVBoxLayout()
        
        self.export_format = QComboBox()
        self.export_format.addItems(["PDF", "CSV", "JSON"])
        export_layout.addWidget(self.export_format)
        
        export_button = QPushButton("Export Results")
        export_button.clicked.connect(self.export_results)
        export_layout.addWidget(export_button)
        
        export_group.setLayout(export_layout)
        layout.addWidget(export_group)
        
        control_panel.setLayout(layout)
        return control_panel

    def export_results(self):
        """Export results in selected format"""
        format_type = self.export_format.currentText()
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Results",
            "",
            f"{format_type} Files (*.{format_type.lower()});;All Files (*)"
        )
        
        if filename:
            try:
                if format_type == "PDF":
                    self.generate_report(filename)
                elif format_type == "CSV":
                    self.export_to_csv(filename)
                elif format_type == "JSON":
                    self.export_to_json(filename)
                
                QMessageBox.information(self, "Success", 
                                      f"Results exported successfully to {format_type}")
            except Exception as e:
                QMessageBox.warning(self, "Error", 
                                  f"Failed to export results: {str(e)}")

    def export_to_csv(self, filename):
        """Export results to CSV format"""
        with open(filename, 'w') as f:
            f.write("Power System Analysis Results\n\n")
            f.write(self.results_text.toPlainText())

    def export_to_json(self, filename):
        """Export results to JSON format"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'results': self.results_text.toPlainText(),
            'components': [
                {
                    'type': comp_type,
                    'properties': self.diagram_scene.component_properties.get(item, {})
                }
                for comp_type, item in self.diagram_scene.components
            ]
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def delete_element(self, item=None):
        """Delete selected or specified element with confirmation"""
        items_to_delete = []
        
        if item:
            items_to_delete.append(item)
        else:
            items_to_delete = self.diagram_scene.selectedItems()
        
        if not items_to_delete:
            QMessageBox.information(self, "Delete", "No elements selected for deletion")
            return
        
        # Get element names for confirmation
        element_names = []
        for item in items_to_delete:
            for comp_type, comp_item in self.diagram_scene.components:
                if comp_item == item:
                    name = self.diagram_scene.component_properties.get(item, {}).get('name', '')
                    if not name:
                        if comp_type == PowerComponent.BUS:
                            name = f"Bus {self.diagram_scene.get_node_number(item)}"
                        else:
                            name = f"{comp_type.title()}"
                    element_names.append(name)
                    break
        
        # Show confirmation dialog
        msg = "Are you sure you want to delete the following elements?\n\n"
        msg += "\n".join(f"- {name}" for name in element_names)
        reply = QMessageBox.question(self, "Confirm Delete", msg,
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            for item in items_to_delete:
                self.delete_element_and_connections(item)
            
            # Update component tree and scene
            self.update_component_tree()
            self.diagram_scene.update()

    def delete_element_and_connections(self, item):
        """Delete an element and its connected lines"""
        # First, find and delete connected lines
        lines_to_delete = []
        item_pos = item.pos()
        
        for comp_type, comp_item in self.diagram_scene.components:
            if comp_type == PowerComponent.LINE:
                line = comp_item
                start_pos = QPointF(line.line().x1(), line.line().y1())
                end_pos = QPointF(line.line().x2(), line.line().y2())
                
                # Check if line is connected to the item being deleted
                if ((abs(start_pos.x() - item_pos.x()) < 30 and 
                     abs(start_pos.y() - item_pos.y()) < 30) or
                    (abs(end_pos.x() - item_pos.x()) < 30 and 
                     abs(end_pos.y() - item_pos.y()) < 30)):
                    lines_to_delete.append(comp_item)
        
        # Delete connected lines
        for line in lines_to_delete:
            self.diagram_scene.remove_component(line)
        
        # Delete the element itself
        self.diagram_scene.remove_component(item)
        
        # Record delete operation for undo/redo
        self.record_operation('delete', item)

    def delete_connected_lines(self, item):
        """Delete all lines connected to an element"""
        lines_to_delete = []
        item_pos = item.pos()
        
        for comp_type, comp_item in self.diagram_scene.components:
            if comp_type == PowerComponent.LINE:
                line = comp_item
                start_pos = QPointF(line.line().x1(), line.line().y1())
                end_pos = QPointF(line.line().x2(), line.line().y2())
                
                if ((abs(start_pos.x() - item_pos.x()) < 30 and 
                     abs(start_pos.y() - item_pos.y()) < 30) or
                    (abs(end_pos.x() - item_pos.x()) < 30 and 
                     abs(end_pos.y() - item_pos.y()) < 30)):
                    lines_to_delete.append(comp_item)
        
        if lines_to_delete:
            msg = f"Delete {len(lines_to_delete)} connected line(s)?"
            reply = QMessageBox.question(self, "Confirm Delete", msg,
                                       QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                for line in lines_to_delete:
                    self.diagram_scene.remove_component(line)
                self.update_component_tree()
                self.diagram_scene.update()

    # Add this helper method to PowerSystemSimulator class
    def add_power_flow_label(self, pos, power, color):
        """Add power flow value label"""
        text = self.diagram_scene.addText(f"{abs(power):.1f} MW")
        text.setDefaultTextColor(color)
        text.setPos(pos.x() + 5, pos.y() - 20)
        return text

    def add_direction_indicator(self, pos, power, color):
        """Add direction indicator without value"""
        if power > 0:
            # Add arrowhead for generator
            points = [
                QPointF(pos.x() + 10, pos.y() - 5),
                QPointF(pos.x() + 20, pos.y()),
                QPointF(pos.x() + 10, pos.y() + 5)
            ]
        else:
            # Add arrowhead for load
            points = [
                QPointF(pos.x() - 10, pos.y() - 5),
                QPointF(pos.x() - 20, pos.y()),
                QPointF(pos.x() - 10, pos.y() + 5)
            ]
        
        polygon = QPolygonF(points)
        arrow_head = self.diagram_scene.addPolygon(polygon, QPen(color), QBrush(color))
        return arrow_head

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Set fusion style for better appearance
    app.setStyle("Fusion")
    
    # Set dark palette
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)
    
    window = PowerSystemSimulator()
    window.show()
    sys.exit(app.exec_()) 
