#!/usr/bin/env python

#**************************************************************************
# Tintwizard
#
# Copyright (C) 2009 Euan Freeman <euan04@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License version 3
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#*************************************************************************/
# Last modified: 14th June 2010

import pygtk
pygtk.require('2.0')
import gtk
import os
import sys
import signal
import webbrowser
import math
import shutil

# Project information
NAME = "tintwizard"
AUTHORS = ["Euan Freeman <euan04@gmail.com>"]
VERSION = "0.3.4"
COMMENTS = "tintwizard generates config files for the lightweight panel replacement tint2"
WEBSITE = "http://code.google.com/p/tintwizard/"

# Default values for text entry fields
BG_ROUNDING = "0"
BG_BORDER = "0"
PANEL_SIZE_X = "0"
PANEL_SIZE_Y = "40"
PANEL_MARGIN_X = "0"
PANEL_MARGIN_Y = "0"
PANEL_PADDING_X = "0"
PANEL_PADDING_Y = "0"
PANEL_MONITOR = "all"
PANEL_ITEMS = "TSC"
PANEL_AUTOHIDE_SHOW = "0.0"
PANEL_AUTOHIDE_HIDE = "0.0"
PANEL_AUTOHIDE_HEIGHT = "0"
TASKBAR_PADDING_X = "0"
TASKBAR_PADDING_Y = "0"
TASKBAR_SPACING = "0"
TASK_BLINKS = "7"
TASK_MAXIMUM_SIZE_X = "200"
TASK_MAXIMUM_SIZE_Y = "32"
TASK_PADDING_X = "0"
TASK_PADDING_Y = "0"
TASK_SPACING = "0"
TRAY_PADDING_X = "0"
TRAY_PADDING_Y = "0"
TRAY_SPACING = "0"
TRAY_MAX_ICON_SIZE = "0"
TRAY_ICON_ALPHA = "100"
TRAY_ICON_SAT = "0"
TRAY_ICON_BRI = "0"
ICON_ALPHA = "100"
ICON_SAT = "0"
ICON_BRI = "0"
ACTIVE_ICON_ALPHA = "100"
ACTIVE_ICON_SAT = "0"
ACTIVE_ICON_BRI = "0"
URGENT_ICON_ALPHA = "100"
URGENT_ICON_SAT = "0"
URGENT_ICON_BRI = "0"
ICONIFIED_ICON_ALPHA = "100"
ICONIFIED_ICON_SAT = "0"
ICONIFIED_ICON_BRI = "0"
CLOCK_FMT_1 = "%H:%M"
CLOCK_FMT_2 = "%a %d %b"
CLOCK_TOOLTIP = ""
CLOCK_TIME1_TIMEZONE = ""
CLOCK_TIME2_TIMEZONE = ""
CLOCK_TOOLTIP_TIMEZONE = ""
CLOCK_PADDING_X = "0"
CLOCK_PADDING_Y = "0"
CLOCK_LCLICK = ""
CLOCK_RCLICK = ""
TOOLTIP_PADDING_X = "0"
TOOLTIP_PADDING_Y = "0"
TOOLTIP_SHOW_TIMEOUT = "0"
TOOLTIP_HIDE_TIMEOUT = "0"
BATTERY_LOW = "20"
BATTERY_HIDE = "90"
BATTERY_ACTION = 'notify-send "battery low"'
BATTERY_PADDING_X = "0"
BATTERY_PADDING_Y = "0"

class TintWizardPrefGUI(gtk.Window):
	"""The dialog window which lets the user change the default preferences."""
	def __init__(self, tw):
		"""Create and shows the window."""
		self.tw = tw
		
		# Create top-level window
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		
		self.set_title("Preferences")
		self.connect("delete_event", self.quit)
		
		self.layout = gtk.Table(2, 2, False)
		
		self.table = gtk.Table(5, 2, False)
		self.table.set_row_spacings(5)
		self.table.set_col_spacings(5)
		
		createLabel(self.table, text="Default Font", gridX=0, gridY=0)
		self.font = gtk.FontButton(self.tw.defaults["font"])
		self.font.set_alignment(0, 0.5)
		self.table.attach(self.font, 1, 2, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		createLabel(self.table, text="Default Background Color", gridX=0, gridY=1)
		self.bgColor = gtk.ColorButton(gtk.gdk.color_parse(self.tw.defaults["bgColor"]))
		self.bgColor.set_alignment(0, 0.5)
		self.table.attach(self.bgColor, 1, 2, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		createLabel(self.table, text="Default Foreground Color", gridX=0, gridY=2)
		self.fgColor = gtk.ColorButton(gtk.gdk.color_parse(self.tw.defaults["fgColor"]))
		self.fgColor.set_alignment(0, 0.5)
		self.table.attach(self.fgColor, 1, 2, 2, 3, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		createLabel(self.table, text="Default Border Color", gridX=0, gridY=3)
		self.borderColor = gtk.ColorButton(gtk.gdk.color_parse(self.tw.defaults["borderColor"]))
		self.borderColor.set_alignment(0, 0.5)
		self.table.attach(self.borderColor, 1, 2, 3, 4, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)

		createLabel(self.table, text="Number of background styles", gridX=0, gridY=4)
		self.bgCount = createEntry(self.table, maxSize=6, width=8, text=str(self.tw.defaults["bgCount"]), gridX=1, gridY=4, xExpand=True, yExpand=True)

		self.layout.attach(self.table, 0, 2, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND, xpadding=20, ypadding=5)
		
		createButton(self.layout, text="Save", stock=gtk.STOCK_SAVE, name="save", gridX=0, gridY=1, xExpand=True, yExpand=True, handler=self.save)
		createButton(self.layout, text="Cancel", stock=gtk.STOCK_CANCEL, name="cancel", gridX=1, gridY=1, xExpand=True, yExpand=True, handler=self.quit)
		
		self.add(self.layout)

		self.show_all()

	def quit(self, widget=None, event=None):
		"""Destroys the window."""
		self.destroy()

	def save(self, action=None):
		"""Called when the Save button is clicked."""
		if confirmDialog(self, "Overwrite configuration file?") == gtk.RESPONSE_YES:
			self.tw.defaults["font"] = self.font.get_font_name()
			self.tw.defaults["bgColor"] = rgbToHex(self.bgColor.get_color().red, self.bgColor.get_color().green, self.bgColor.get_color().blue)
			self.tw.defaults["fgColor"] = rgbToHex(self.fgColor.get_color().red, self.fgColor.get_color().green, self.fgColor.get_color().blue)
			self.tw.defaults["borderColor"] = rgbToHex(self.borderColor.get_color().red, self.borderColor.get_color().green, self.borderColor.get_color().blue)

			try:
				self.tw.defaults["bgCount"] = int(self.bgCount.get_text())
			except:
				errorDialog(self, "Invalid value for background count")
				return

			self.tw.writeConf()

			self.quit()

class TintWizardGUI(gtk.Window):
	"""The main window for the application."""
	def __init__(self):
		"""Create and show the window."""
		self.filename = None
		self.curDir = None
		self.toSave = False

		if len(sys.argv) > 1:
			self.filename = sys.argv[1]
			self.oneConfigFile = True
		else:
			self.oneConfigFile = False

		# Read conf file and set default values
		self.readConf()

		if self.defaults["bgColor"] in [None, "None"]:
			self.defaults["bgColor"] = "#000000"

		if self.defaults["fgColor"] in [None, "None"]:
			self.defaults["fgColor"] = "#ffffff"

		if self.defaults["borderColor"] in [None, "None"]:
			self.defaults["borderColor"] = "#ffffff"

		if os.path.exists(os.path.expandvars("${HOME}") + "/.config/tint2"):
			self.curDir = os.path.expandvars("${HOME}") + "/.config/tint2"
		else:
			errorDialog("$HOME/.config/tint2/ directory not found! Is tint2 installed correctly?")
			Sys.exit(1)

		try:
			self.defaults["bgCount"] = int(self.defaults["bgCount"])
		except:
			self.defaults["bgCount"] = 2

		# Get the full location of the tint2 binary
		which = os.popen('which tint2')

		self.tint2Bin = which.readline().strip()

		which.close()

		if len(self.tint2Bin) == 0:
			errorDialog(self, "tint2 could not be found. Are you sure it is installed?")
			sys.exit(1)

		# Create top-level window
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)

		self.set_title("tintwizard")

		self.connect("delete_event", self.quit)

		# self.table is our main layout manager
		self.table = gtk.Table(4, 1, False)
		
		# Set up the dictionary to hold all registered widgets
		self.propUI = {}

		# Create menus and toolbar items
		ui = """
		<ui>
			<menubar name="MenuBar">
				<menu action="File">
					<menuitem action="New" />
					<menuitem action="Open" />
					<separator />
					<menuitem action="Save" />
					<menuitem action="Save As..." />
					<separator />
					<menuitem action="Quit" />
				</menu>
				<menu action="Tint2">
					<menuitem action="OpenDefault" />
					<menuitem action="SaveDefault" />
					<separator />
					<menuitem action="Apply" />
				</menu>
				<menu action="Tools">
					<menuitem action="FontChange" />
					<separator />
					<menuitem action="Defaults" />
				</menu>
				<menu action="HelpMenu">
					<menuitem action="Help" />
					<menuitem action="Report Bug" />
					<separator />
					<menuitem action="About" />
				</menu>
			</menubar>
			<toolbar name="ToolBar">
				<toolitem action="New" />
				<toolitem action="Open" />
				<toolitem action="Save" />
				<separator />
				<toolitem action="Apply" />
			</toolbar>
		</ui>
		"""

		# Set up UI manager
		self.uiManager = gtk.UIManager()

		accelGroup = self.uiManager.get_accel_group()
		self.add_accel_group(accelGroup)

		self.ag = gtk.ActionGroup("File")
		self.ag.add_actions([("File", None, "_File"),
						("New",gtk.STOCK_NEW, "_New", None, "Create a new config", self.new),
						("Open", gtk.STOCK_OPEN, "_Open", None, "Open an existing config", self.openFile),
						("Save", gtk.STOCK_SAVE, "_Save", None, "Save the current config", self.save),
						("Save As...", gtk.STOCK_SAVE_AS, "Save As", None, "Save the current config as...", self.saveAs),
						("SaveDefault", None, "Save As tint2 Default", None, "Save the current config as the tint2 default", self.saveAsDef),
						("OpenDefault", None, "Open tint2 Default", None, "Open the current tint2 default config", self.openDef),
						("Apply", gtk.STOCK_APPLY, "Apply Config", None, "Apply the current config to tint2", self.apply),
						("Quit", gtk.STOCK_QUIT, "_Quit", None, "Quit the program", self.quit),
						("Tools", None, "_Tools"),
						("Tint2", None, "Tint_2"),
						("HelpMenu", None, "_Help"),
						("FontChange",gtk.STOCK_SELECT_FONT, "Change All Fonts", None, "Change all fonts at once.", self.changeAllFonts),
						("Defaults",gtk.STOCK_PREFERENCES, "Change Defaults", None, "Change tintwizard defaults.", self.changeDefaults),
						("Help",gtk.STOCK_HELP, "_Help", None, "Get help with tintwizard", self.help),
						("Report Bug",None, "Report Bug", None, "Report a problem with tintwizard", self.reportBug),
						("About",gtk.STOCK_ABOUT, "_About Tint Wizard", None, "Find out more about Tint Wizard", self.about)])

		# Add main UI
		self.uiManager.insert_action_group(self.ag, -1)
		self.uiManager.add_ui_from_string(ui)

		if not self.oneConfigFile:
			# Attach menubar and toolbar to main window
			self.table.attach(self.uiManager.get_widget("/MenuBar"), 0, 4, 0, 1)
			self.table.attach(self.uiManager.get_widget("/ToolBar"), 0, 4, 1, 2)

		# Create notebook
		self.notebook = gtk.Notebook()
		self.notebook.set_tab_pos(gtk.POS_TOP)

		# Create notebook pages
		# Background Options
		self.tableBgs = gtk.Table(rows=1, columns=1, homogeneous=False)
		self.tableBgs.set_row_spacings(5)
		self.tableBgs.set_col_spacings(5)

		self.bgNotebook = gtk.Notebook()
		self.bgNotebook.set_scrollable(True)

		self.tableBgs.attach(self.bgNotebook, 0, 2, 0, 1)

		self.bgs = []

		# Add buttons for adding/deleting background styles
		createButton(self.tableBgs, text="New Background", stock=gtk.STOCK_NEW, name="addBg", gridX=0, gridY=1, xExpand=True, yExpand=True, handler=self.addBgClick)
		createButton(self.tableBgs, text="Delete Background", stock=gtk.STOCK_DELETE, name="delBg", gridX=1, gridY=1, xExpand=True, yExpand=True, handler=self.delBgClick)
		
		# Panel
		self.createPanelDisplayWidgets()
		self.createPanelSettingsWidgets()
		self.createPanelAutohideWidgets()
		
		# Taskbar
		self.createTaskbarWidgets()
		
		# Tasks
		self.createTaskSettingsWidgets()
		self.createNormalTasksWidgets()
		self.createActiveTasksWidgets()
		self.createUrgentTasksWidgets()
		self.createIconifiedTasksWidgets()
		
		# System Tray
		self.createSystemTrayWidgets()
		
		# Clock
		self.createClockDisplayWidgets()
		self.createClockSettingsWidgets()
		
		# Mouse
		self.createMouseWidgets()
		
		# Tooltips
		self.createTooltipsWidgets()
		
		# Battery
		self.createBatteryWidgets()
		
		# View Config
		self.configArea = gtk.ScrolledWindow()
		self.configBuf = gtk.TextBuffer()
		self.configTextView = gtk.TextView(self.configBuf)
		self.configArea.add_with_viewport(self.configTextView)

		# Add backgrounds to notebooks
		for i in range(self.defaults["bgCount"]):
			self.addBgClick(None, init=True)

		self.bgNotebook.set_current_page(0)

		# Create sub-notebooks
		self.panelNotebook = gtk.Notebook()
		self.panelNotebook.set_tab_pos(gtk.POS_TOP)
		self.panelNotebook.set_current_page(0)
		
		self.panelNotebook.append_page(self.tablePanelDisplay, gtk.Label("Panel Display"))
		self.panelNotebook.append_page(self.tablePanelSettings, gtk.Label("Panel Settings"))
		self.panelNotebook.append_page(self.tablePanelAutohide, gtk.Label("Panel Autohide"))
		
		self.taskNotebook = gtk.Notebook()
		self.taskNotebook.set_tab_pos(gtk.POS_TOP)
		self.taskNotebook.set_current_page(0)

		self.taskNotebook.append_page(self.tableTask, gtk.Label("Task Settings"))
		self.taskNotebook.append_page(self.tableTaskDefault, gtk.Label("Normal Tasks"))
		self.taskNotebook.append_page(self.tableTaskActive, gtk.Label("Active Tasks"))
		self.taskNotebook.append_page(self.tableTaskUrgent, gtk.Label("Urgent Tasks"))
		self.taskNotebook.append_page(self.tableTaskIconified, gtk.Label("Iconified Tasks"))
		
		self.clockNotebook = gtk.Notebook()
		self.clockNotebook.set_tab_pos(gtk.POS_TOP)
		self.clockNotebook.set_current_page(0)

		self.clockNotebook.append_page(self.tableClockDisplays, gtk.Label("Clock Display"))
		self.clockNotebook.append_page(self.tableClockSettings, gtk.Label("Clock Settings"))

		# Add pages to notebook
		self.notebook.append_page(self.tableBgs, gtk.Label("Backgrounds"))
		self.notebook.append_page(self.panelNotebook, gtk.Label("Panel"))
		self.notebook.append_page(self.tableTaskbar, gtk.Label("Taskbar"))
		self.notebook.append_page(self.taskNotebook, gtk.Label("Tasks"))
		self.notebook.append_page(self.tableTray, gtk.Label("System Tray"))
		self.notebook.append_page(self.clockNotebook, gtk.Label("Clock"))
		self.notebook.append_page(self.tableMouse, gtk.Label("Mouse"))
		self.notebook.append_page(self.tableTooltip, gtk.Label("Tooltips"))
		self.notebook.append_page(self.tableBattery, gtk.Label("Battery"))
		self.notebook.append_page(self.configArea, gtk.Label("View Config"))

		self.notebook.connect("switch-page", self.switchPage)

		# Add notebook to window and show
		self.table.attach(self.notebook, 0, 4, 2, 3, xpadding=5, ypadding=5)

		if self.oneConfigFile:
			# Add button Apply and Close
			self.box1 = gtk.HBox(False, 20)
			self.table.attach(self.box1, 0, 4, 3, 4, xpadding=5, ypadding=5)
			temp = gtk.Button("Apply", gtk.STOCK_APPLY)
			temp.set_name("applyBg")
			temp.connect("clicked", self.apply)
			self.box1.pack_start(temp, True, True, 0)
			temp = gtk.Button("Close", gtk.STOCK_CLOSE)
			temp.set_name("closeBg")
			temp.connect("clicked", self.quit)
			self.box1.pack_start(temp, True, True, 0)

		# Create and add the status bar to the bottom of the main window
		self.statusBar = gtk.Statusbar()
		self.statusBar.set_has_resize_grip(True)
		self.updateStatusBar("New Config File [*]")
		self.table.attach(self.statusBar, 0, 4, 4, 5)

		self.add(self.table)

		self.show_all()
		
		# If tintwizard was launched with a tint2 config filename
		# as an argument, load that config.
		if self.oneConfigFile:
			self.readTint2Config()

		self.generateConfig()
	
	def createPanelDisplayWidgets(self):
		"""Create the Panel Display widgets."""
		self.tablePanelDisplay = gtk.Table(rows=7, columns=3, homogeneous=False)
		self.tablePanelDisplay.set_row_spacings(5)
		self.tablePanelDisplay.set_col_spacings(5)
		
		createLabel(self.tablePanelDisplay, text="Position", gridX=0, gridY=0, xPadding=10)
		self.panelPosY = createComboBox(self.tablePanelDisplay, ["bottom", "top", "center"], gridX=1, gridY=0, handler=self.changeOccurred)
		self.panelPosX = createComboBox(self.tablePanelDisplay, ["left", "right", "center"], gridX=2, gridY=0, handler=self.changeOccurred)
		# Note: registered below
		
		createLabel(self.tablePanelDisplay, text="Panel Orientation", gridX=0, gridY=1, xPadding=10)
		self.panelOrientation = createComboBox(self.tablePanelDisplay, ["horizontal", "vertical"], gridX=1, gridY=1, handler=self.changeOccurred)
		self.registerComponent("panel_position", (self.panelPosY, self.panelPosX, self.panelOrientation))
		
		createLabel(self.tablePanelDisplay, text="Panel Items", gridX=0, gridY=2, xPadding=10)
		self.panelItems = createEntry(self.tablePanelDisplay, maxSize=7, width=8, text=PANEL_ITEMS, gridX=1, gridY=2, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("panel_items", self.panelItems)
		
		self.panelSizeLabel = createLabel(self.tablePanelDisplay, text="Size (width, height)", gridX=0, gridY=3, xPadding=10)
		self.panelSizeX = createEntry(self.tablePanelDisplay, maxSize=6, width=8, text=PANEL_SIZE_X, gridX=1, gridY=3, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.panelSizeY = createEntry(self.tablePanelDisplay, maxSize=6, width=8, text=PANEL_SIZE_Y, gridX=2, gridY=3, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("panel_size", (self.panelSizeX, self.panelSizeY))
		
		createLabel(self.tablePanelDisplay, text="Margin (x, y)", gridX=0, gridY=4, xPadding=10)
		self.panelMarginX = createEntry(self.tablePanelDisplay, maxSize=6, width=8, text=PANEL_MARGIN_X, gridX=1, gridY=4, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.panelMarginY = createEntry(self.tablePanelDisplay, maxSize=6, width=8, text=PANEL_MARGIN_Y, gridX=2, gridY=4, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("panel_margin", (self.panelMarginX, self.panelMarginY))
		
		createLabel(self.tablePanelDisplay, text="Padding (x, y)", gridX=0, gridY=5, xPadding=10)
		self.panelPadX = createEntry(self.tablePanelDisplay, maxSize=6, width=8, text=PANEL_PADDING_X, gridX=1, gridY=5, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.panelPadY = createEntry(self.tablePanelDisplay, maxSize=6, width=8, text=PANEL_PADDING_Y, gridX=2, gridY=5, xExpand=True, yExpand=False, handler=self.changeOccurred)
		# Note: added below
		
		createLabel(self.tablePanelDisplay, text="Horizontal Spacing", gridX=0, gridY=6, xPadding=10)
		self.panelSpacing = createEntry(self.tablePanelDisplay, maxSize=6, width=8, text=TASKBAR_SPACING, gridX=1, gridY=6, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("panel_padding", (self.panelPadX, self.panelPadY, self.panelSpacing))
		
		createLabel(self.tablePanelDisplay, text="Panel Background ID", gridX=0, gridY=7, xPadding=10)
		self.panelBg = createComboBox(self.tablePanelDisplay, ["0 (fully transparent)"] + range(1, len(self.bgs)), gridX=1, gridY=7, handler=self.changeOccurred)
		self.registerComponent("panel_background_id", self.panelBg)
		
	def createPanelSettingsWidgets(self):
		"""Create the Panel Settings widgets."""
		self.tablePanelSettings = gtk.Table(rows=5, columns=3, homogeneous=False)
		self.tablePanelSettings.set_row_spacings(5)
		self.tablePanelSettings.set_col_spacings(5)
		
		createLabel(self.tablePanelSettings, text="Window Manager Menu", gridX=0, gridY=0, xPadding=10)
		self.panelMenu = createCheckButton(self.tablePanelSettings, active=False, gridX=1, gridY=0, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("wm_menu", self.panelMenu)
		
		createLabel(self.tablePanelSettings, text="Place In Window Manager Dock", gridX=0, gridY=1, xPadding=10)
		self.panelDock = createCheckButton(self.tablePanelSettings, active=False, gridX=1, gridY=1, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("panel_dock", self.panelDock)
		
		createLabel(self.tablePanelSettings, text="Panel Layer", gridX=0, gridY=2, xPadding=10)
		self.panelLayer = createComboBox(self.tablePanelSettings, ["bottom", "top", "normal"], gridX=1, gridY=2, handler=self.changeOccurred)
		self.registerComponent("panel_layer", self.panelLayer)
		
		createLabel(self.tablePanelSettings, text="Strut Policy", gridX=0, gridY=3, xPadding=10)
		self.panelAutohideStrut = createComboBox(self.tablePanelSettings, ["none", "minimum", "follow_size"], gridX=1, gridY=3, handler=self.changeOccurred)
		self.registerComponent("strut_policy", self.panelAutohideStrut)
		
		createLabel(self.tablePanelSettings, text="Panel Monitor (all, 1, 2, ...)", gridX=0, gridY=4, xPadding=10)
		self.panelMonitor = createEntry(self.tablePanelSettings, maxSize=6, width=8, text=PANEL_MONITOR, gridX=1, gridY=4, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("panel_monitor", self.panelMonitor)
		
	def createPanelAutohideWidgets(self):
		"""Create the Panel Autohide widgets."""
		self.tablePanelAutohide = gtk.Table(rows=4, columns=3, homogeneous=False)
		self.tablePanelAutohide.set_row_spacings(5)
		self.tablePanelAutohide.set_col_spacings(5)
		
		createLabel(self.tablePanelAutohide, text="Autohide Panel", gridX=0, gridY=0, xPadding=10)
		self.panelAutohide = createCheckButton(self.tablePanelAutohide, active=False, gridX=1, gridY=0, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("autohide", self.panelAutohide)
		
		createLabel(self.tablePanelAutohide, text="Autohide Show Timeout (seconds)", gridX=0, gridY=1, xPadding=10)
		self.panelAutohideShow = createEntry(self.tablePanelAutohide, maxSize=6, width=8, text=PANEL_AUTOHIDE_SHOW, gridX=1, gridY=1, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("autohide_show_timeout", self.panelAutohideShow)
		
		createLabel(self.tablePanelAutohide, text="Autohide Hide Timeout (seconds)", gridX=0, gridY=2, xPadding=10)
		self.panelAutohideHide = createEntry(self.tablePanelAutohide, maxSize=6, width=8, text=PANEL_AUTOHIDE_HIDE, gridX=1, gridY=2, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("autohide_hide_timeout", self.panelAutohideHide)
		
		createLabel(self.tablePanelAutohide, text="Autohide Hidden Height", gridX=0, gridY=3, xPadding=10)
		self.panelAutohideHeight = createEntry(self.tablePanelAutohide, maxSize=6, width=8, text=PANEL_AUTOHIDE_HEIGHT, gridX=1, gridY=3, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("autohide_height", self.panelAutohideHeight)
	
	def createTaskbarWidgets(self):
		"""Create the Taskbar widgets."""
		self.tableTaskbar = gtk.Table(rows=5, columns=3, homogeneous=False)
		self.tableTaskbar.set_row_spacings(5)
		self.tableTaskbar.set_col_spacings(5)
		
		createLabel(self.tableTaskbar, text="Taskbar Mode", gridX=0, gridY=0, xPadding=10)
		self.taskbarMode = createComboBox(self.tableTaskbar, ["single_desktop", "multi_desktop"], gridX=1, gridY=0, handler=self.changeOccurred)
		self.registerComponent("taskbar_mode", self.taskbarMode)
		
		createLabel(self.tableTaskbar, text="Padding (x, y)", gridX=0, gridY=1, xPadding=10)
		self.taskbarPadX = createEntry(self.tableTaskbar, maxSize=6, width=8, text=TASKBAR_PADDING_X, gridX=1, gridY=1, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.taskbarPadY = createEntry(self.tableTaskbar, maxSize=6, width=8, text=TASKBAR_PADDING_Y, gridX=2, gridY=1, xExpand=True, yExpand=False, handler=self.changeOccurred)
		# Note: added below
		
		createLabel(self.tableTaskbar, text="Horizontal Spacing", gridX=0, gridY=2, xPadding=10)
		self.taskbarSpacing = createEntry(self.tableTaskbar, maxSize=6, width=8, text=TASK_SPACING, gridX=1, gridY=2, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("taskbar_padding", (self.taskbarPadX, self.taskbarPadY, self.taskbarSpacing))
		
		createLabel(self.tableTaskbar, text="Taskbar Background ID", gridX=0, gridY=3, xPadding=10)
		self.taskbarBg = createComboBox(self.tableTaskbar, ["0 (fully transparent)"] + range(1, len(self.bgs)), gridX=1, gridY=3, handler=self.changeOccurred)
		self.registerComponent("taskbar_background_id", self.taskbarBg)
		
		createLabel(self.tableTaskbar, text="Active Taskbar Background ID", gridX=0, gridY=4, xPadding=10)
		self.taskbarActiveBg = createComboBox(self.tableTaskbar, ["0 (fully transparent)"] + range(1, len(self.bgs)), gridX=1, gridY=4, handler=self.changeOccurred)
		self.registerComponent("taskbar_active_background_id", self.taskbarActiveBg)
	
	def createTaskSettingsWidgets(self):
		"""Create the Task Settings widgets."""
		self.tableTask = gtk.Table(rows=12, columns=3, homogeneous=False)
		self.tableTask.set_row_spacings(5)
		self.tableTask.set_col_spacings(5)
		
		createLabel(self.tableTask, text="Number of 'Blinks' on Urgent Event", gridX=0, gridY=0, xPadding=10)
		self.taskBlinks = createEntry(self.tableTask, maxSize=6, width=8, text=TASK_BLINKS, gridX=1, gridY=0, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("urgent_nb_of_blink", self.taskBlinks)
		
		createLabel(self.tableTask, text="Show Icons", gridX=0, gridY=1, xPadding=10)
		self.taskIconCheckButton = createCheckButton(self.tableTask, active=True, gridX=1, gridY=1, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("task_icon", self.taskIconCheckButton)
		
		createLabel(self.tableTask, text="Show Text", gridX=0, gridY=2, xPadding=10)
		self.taskTextCheckButton = createCheckButton(self.tableTask, active=True, gridX=1, gridY=2, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("task_text", self.taskTextCheckButton)
		
		createLabel(self.tableTask, text="Centre Text", gridX=0, gridY=3, xPadding=10)
		self.taskCentreCheckButton = createCheckButton(self.tableTask, active=True, gridX=1, gridY=3, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("task_centered", self.taskCentreCheckButton)
		
		createLabel(self.tableTask, text="Font", gridX=0, gridY=4, xPadding=10)
		self.fontButton = gtk.FontButton()
		
		if self.defaults["font"] in [None, "None"]:						# If there was no font specified in the config file
			self.defaults["font"] = self.fontButton.get_font_name()		# Use the gtk default
		
		self.fontButton = createFontButton(self.tableTask, font=self.defaults["font"], gridX=1, gridY=4, handler=self.changeOccurred)
		self.registerComponent("task_font", self.fontButton)
		
		createLabel(self.tableTask, text="Show Font Shadow", gridX=0, gridY=5, xPadding=10)
		self.fontShadowCheckButton = createCheckButton(self.tableTask, active=False, gridX=1, gridY=5, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("font_shadow", self.fontShadowCheckButton)
		
		createLabel(self.tableTask, text="Maximum Size (x, y)", gridX=0, gridY=6, xPadding=10)
		self.taskMaxSizeX = createEntry(self.tableTask, maxSize=6, width=8, text=TASK_MAXIMUM_SIZE_X, gridX=1, gridY=6, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.taskMaxSizeY = createEntry(self.tableTask, maxSize=6, width=8, text=TASK_MAXIMUM_SIZE_Y, gridX=2, gridY=6, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("task_maximum_size", (self.taskMaxSizeX, self.taskMaxSizeY))
		
		createLabel(self.tableTask, text="Padding (x, y)", gridX=0, gridY=7, xPadding=10)
		self.taskPadX = createEntry(self.tableTask, maxSize=6, width=8, text=TASK_PADDING_X, gridX=1, gridY=7, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.taskPadY = createEntry(self.tableTask, maxSize=6, width=8, text=TASK_PADDING_Y, gridX=2, gridY=7, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("task_padding", (self.taskPadX, self.taskPadY))
		
	def createNormalTasksWidgets(self):
		"""Create the Normal Tasks widgets."""
		self.tableTaskDefault = gtk.Table(rows=6, columns=3, homogeneous=False)
		self.tableTaskDefault.set_row_spacings(5)
		self.tableTaskDefault.set_col_spacings(5)
		
		createLabel(self.tableTaskDefault, text="Normal Task Background ID", gridX=0, gridY=0, xPadding=10)
		self.taskBg = createComboBox(self.tableTaskDefault, ["0 (fully transparent)"] + range(1, len(self.bgs)), gridX=1, gridY=0, handler=self.changeOccurred)
		self.registerComponent("task_background_id", self.taskBg)
		
		createLabel(self.tableTaskDefault, text="Note: Default values of 0 for each of these settings leaves icons unchanged!", gridX=0, gridY=1, sizeX=3, xPadding=10)
		
		createLabel(self.tableTaskDefault, text="Normal Icon Alpha (0 to 100)", gridX=0, gridY=2, xPadding=10)
		self.iconHue = createEntry(self.tableTaskDefault, maxSize=6, width=8, text=ICON_ALPHA, gridX=1, gridY=2, xExpand=True, yExpand=False, handler=self.changeOccurred)
		# Note: added below
		
		createLabel(self.tableTaskDefault, text="Normal Icon Saturation (-100 to 100)", gridX=0, gridY=3, xPadding=10)
		self.iconSat = createEntry(self.tableTaskDefault, maxSize=6, width=8, text=ICON_SAT, gridX=1, gridY=3, xExpand=True, yExpand=False, handler=self.changeOccurred)
		# Note: added below
		
		createLabel(self.tableTaskDefault, text="Normal Icon Brightness (-100 to 100)", gridX=0, gridY=4, xPadding=10)
		self.iconBri = createEntry(self.tableTaskDefault, maxSize=6, width=8, text=ICON_BRI, gridX=1, gridY=4, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("task_icon_asb", (self.iconHue, self.iconSat, self.iconBri))
		
		createLabel(self.tableTaskDefault, text="Normal Font Color", gridX=0, gridY=5, xPadding=10)
		self.fontCol = createEntry(self.tableTaskDefault, maxSize=7, width=9, text="", gridX=1, gridY=5, xExpand=True, yExpand=False, handler=None, name="fontCol")
		self.fontCol.connect("activate", self.colorTyped)
		self.fontColButton = createColorButton(self.tableTaskDefault, color=self.defaults["fgColor"], useAlpha=True, name="fontCol", gridX=2, gridY=5, handler=self.colorChange)
		self.fontCol.set_text(self.defaults["fgColor"])
		# Add this AFTER we set color to avoid "changed" event
		self.fontCol.connect("changed", self.changeOccurred)
		self.registerComponent("task_font_color", (self.fontCol, self.fontColButton))
		
	def createActiveTasksWidgets(self):
		"""Create the Active Tasks widgets."""
		self.tableTaskActive = gtk.Table(rows=6, columns=3, homogeneous=False)
		self.tableTaskActive.set_row_spacings(5)
		self.tableTaskActive.set_col_spacings(5)
		
		createLabel(self.tableTaskActive, text="Active Task Background ID", gridX=0, gridY=0, xPadding=10)
		self.taskActiveBg = createComboBox(self.tableTaskActive, ["0 (fully transparent)"] + range(1, len(self.bgs)), gridX=1, gridY=0, handler=self.changeOccurred)
		self.registerComponent("task_active_background_id", self.taskActiveBg)
		
		createLabel(self.tableTaskActive, text="Note: Default values of 0 for each of these settings leaves icons unchanged!", gridX=0, gridY=1, sizeX=3, xPadding=10)
		
		createLabel(self.tableTaskActive, text="Active Icon Alpha (0 to 100)", gridX=0, gridY=2, xPadding=10)
		self.activeIconHue = createEntry(self.tableTaskActive, maxSize=6, width=8, text=ACTIVE_ICON_ALPHA, gridX=1, gridY=2, xExpand=True, yExpand=False, handler=self.changeOccurred)
		# Note: added below
		
		createLabel(self.tableTaskActive, text="Active Icon Saturation (-100 to 100)", gridX=0, gridY=3, xPadding=10)
		self.activeIconSat = createEntry(self.tableTaskActive, maxSize=6, width=8, text=ACTIVE_ICON_SAT, gridX=1, gridY=3, xExpand=True, yExpand=False, handler=self.changeOccurred)
		# Note: added below
		
		createLabel(self.tableTaskActive, text="Active Icon Brightness (-100 to 100)", gridX=0, gridY=4, xPadding=10)
		self.activeIconBri = createEntry(self.tableTaskActive, maxSize=6, width=8, text=ACTIVE_ICON_BRI, gridX=1, gridY=4, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("task_active_icon_asb", (self.activeIconHue, self.activeIconSat, self.activeIconBri))
		
		createLabel(self.tableTaskActive, text="Active Font Color", gridX=0, gridY=5, xPadding=10)
		self.fontActiveCol = createEntry(self.tableTaskActive, maxSize=7, width=9, text="", gridX=1, gridY=5, xExpand=True, yExpand=False, handler=None, name="fontActiveCol")
		self.fontActiveCol.connect("activate", self.colorTyped)
		self.fontActiveColButton = createColorButton(self.tableTaskActive, color=self.defaults["fgColor"], useAlpha=True, name="fontActiveCol", gridX=2, gridY=5, handler=self.colorChange)
		self.fontActiveCol.set_text(self.defaults["fgColor"])
		# Add this AFTER we set color to avoid "changed" event
		self.fontActiveCol.connect("changed", self.changeOccurred)
		self.registerComponent("task_active_font_color", (self.fontActiveCol, self.fontActiveColButton))
		
	def createUrgentTasksWidgets(self):
		"""Create the Urgent Tasks widgets."""
		self.tableTaskUrgent = gtk.Table(rows=6, columns=3, homogeneous=False)
		self.tableTaskUrgent.set_row_spacings(5)
		self.tableTaskUrgent.set_col_spacings(5)
		
		createLabel(self.tableTaskUrgent, text="Urgent Task Background ID", gridX=0, gridY=0, xPadding=10)
		self.taskUrgentBg = createComboBox(self.tableTaskUrgent, ["0 (fully transparent)"] + range(1, len(self.bgs)), gridX=1, gridY=0, handler=self.changeOccurred)
		self.registerComponent("task_urgent_background_id", self.taskUrgentBg)
		
		createLabel(self.tableTaskUrgent, text="Note: Default values of 0 for each of these settings leaves icons unchanged!", gridX=0, gridY=1, sizeX=3, xPadding=10)
		
		createLabel(self.tableTaskUrgent, text="Urgent Icon Alpha (0 to 100)", gridX=0, gridY=2, xPadding=10)
		self.urgentIconHue = createEntry(self.tableTaskUrgent, maxSize=6, width=8, text=URGENT_ICON_ALPHA, gridX=1, gridY=2, xExpand=True, yExpand=False, handler=self.changeOccurred)
		# Note: added below
		
		createLabel(self.tableTaskUrgent, text="Urgent Icon Saturation (-100 to 100)", gridX=0, gridY=3, xPadding=10)
		self.urgentIconSat = createEntry(self.tableTaskUrgent, maxSize=6, width=8, text=URGENT_ICON_SAT, gridX=1, gridY=3, xExpand=True, yExpand=False, handler=self.changeOccurred)
		# Note: added below
		
		createLabel(self.tableTaskUrgent, text="Urgent Icon Brightness (-100 to 100)", gridX=0, gridY=4, xPadding=10)
		self.urgentIconBri = createEntry(self.tableTaskUrgent, maxSize=6, width=8, text=URGENT_ICON_BRI, gridX=1, gridY=4, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("task_urgent_icon_asb", (self.urgentIconHue, self.urgentIconSat, self.urgentIconBri))
		
		createLabel(self.tableTaskUrgent, text="Urgent Font Color", gridX=0, gridY=5, xPadding=10)
		self.fontUrgentCol = createEntry(self.tableTaskUrgent, maxSize=7, width=9, text="", gridX=1, gridY=5, xExpand=True, yExpand=False, handler=None, name="fontUrgentCol")
		self.fontUrgentCol.connect("activate", self.colorTyped)
		self.fontUrgentColButton = createColorButton(self.tableTaskUrgent, color=self.defaults["fgColor"], useAlpha=True, name="fontUrgentCol", gridX=2, gridY=5, handler=self.colorChange)
		self.fontUrgentCol.set_text(self.defaults["fgColor"])
		# Add this AFTER we set color to avoid "changed" event
		self.fontUrgentCol.connect("changed", self.changeOccurred)
		self.registerComponent("task_urgent_font_color", (self.fontUrgentCol, self.fontUrgentColButton))
		
	def createIconifiedTasksWidgets(self):
		"""Create the Iconified Tasks widgets."""
		self.tableTaskIconified = gtk.Table(rows=6, columns=3, homogeneous=False)
		self.tableTaskIconified.set_row_spacings(5)
		self.tableTaskIconified.set_col_spacings(5)
		
		createLabel(self.tableTaskIconified, text="Iconified Task Background ID", gridX=0, gridY=0, xPadding=10)
		self.taskIconifiedBg = createComboBox(self.tableTaskIconified, ["0 (fully transparent)"] + range(1, len(self.bgs)), gridX=1, gridY=0, handler=self.changeOccurred)
		self.registerComponent("task_iconified_background_id", self.taskIconifiedBg)
		
		createLabel(self.tableTaskIconified, text="Note: Default values of 0 for each of these settings leaves icons unchanged!", gridX=0, gridY=1, sizeX=3, xPadding=10)
		
		createLabel(self.tableTaskIconified, text="Iconified Icon Alpha (0 to 100)", gridX=0, gridY=2, xPadding=10)
		self.iconifiedIconHue = createEntry(self.tableTaskIconified, maxSize=6, width=8, text=ICONIFIED_ICON_ALPHA, gridX=1, gridY=2, xExpand=True, yExpand=False, handler=self.changeOccurred)
		# Note: added below
		
		createLabel(self.tableTaskIconified, text="Iconified Icon Saturation (-100 to 100)", gridX=0, gridY=3, xPadding=10)
		self.iconifiedIconSat = createEntry(self.tableTaskIconified, maxSize=6, width=8, text=ICONIFIED_ICON_SAT, gridX=1, gridY=3, xExpand=True, yExpand=False, handler=self.changeOccurred)
		# Note: added below
		
		createLabel(self.tableTaskIconified, text="Iconified Icon Brightness (-100 to 100)", gridX=0, gridY=4, xPadding=10)
		self.iconifiedIconBri = createEntry(self.tableTaskIconified, maxSize=6, width=8, text=ICONIFIED_ICON_BRI, gridX=1, gridY=4, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("task_iconified_icon_asb", (self.iconifiedIconHue, self.iconifiedIconSat, self.iconifiedIconBri))
		
		createLabel(self.tableTaskIconified, text="Iconified Font Color", gridX=0, gridY=5, xPadding=10)
		self.fontIconifiedCol = createEntry(self.tableTaskIconified, maxSize=7, width=9, text="", gridX=1, gridY=5, xExpand=True, yExpand=False, handler=None, name="fontIconifiedCol")
		self.fontIconifiedCol.connect("activate", self.colorTyped)
		self.fontIconifiedColButton = createColorButton(self.tableTaskIconified, color=self.defaults["fgColor"], useAlpha=True, name="fontIconifiedCol", gridX=2, gridY=5, handler=self.colorChange)
		self.fontIconifiedCol.set_text(self.defaults["fgColor"])
		# Add this AFTER we set color to avoid "changed" event
		self.fontIconifiedCol.connect("changed", self.changeOccurred)
		self.registerComponent("task_iconified_font_color", (self.fontIconifiedCol, self.fontIconifiedColButton))
	
	def createSystemTrayWidgets(self):
		"""Create the System Tray widgets."""
		self.tableTray = gtk.Table(rows=9, columns=3, homogeneous=False)
		self.tableTray.set_row_spacings(5)
		self.tableTray.set_col_spacings(5)
				
		createLabel(self.tableTray, text="Padding (x, y)", gridX=0, gridY=1, xPadding=10)
		self.trayPadX = createEntry(self.tableTray, maxSize=6, width=8, text=TRAY_PADDING_X, gridX=1, gridY=1, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.trayPadY = createEntry(self.tableTray, maxSize=6, width=8, text=TRAY_PADDING_Y, gridX=2, gridY=1, xExpand=True, yExpand=False, handler=self.changeOccurred)
		# Note: added below
		
		createLabel(self.tableTray, text="Horizontal Spacing", gridX=0, gridY=2, xPadding=10)
		self.traySpacing = createEntry(self.tableTray, maxSize=6, width=8, text=TRAY_SPACING, gridX=1, gridY=2, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("systray_padding", (self.trayPadX, self.trayPadY, self.traySpacing))
		
		createLabel(self.tableTray, text="System Tray Background ID", gridX=0, gridY=3, xPadding=10)
		self.trayBg = createComboBox(self.tableTray, ["0 (fully transparent)"] + range(1, len(self.bgs)), gridX=1, gridY=3, handler=self.changeOccurred)
		self.registerComponent("systray_background_id", self.trayBg)
		
		createLabel(self.tableTray, text="Icon Ordering", gridX=0, gridY=4, xPadding=10)
		self.trayOrder = createComboBox(self.tableTray, ["ascending", "descending", "left2right", "right2left"], gridX=1, gridY=4, handler=self.changeOccurred)
		self.registerComponent("systray_sort", self.trayOrder)
		
		createLabel(self.tableTray, text="Maximum Icon Size (0 for automatic size)", gridX=0, gridY=5, xPadding=10)
		self.trayMaxIconSize = createEntry(self.tableTray, maxSize=6, width=8, text=TRAY_MAX_ICON_SIZE, gridX=1, gridY=5, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("systray_icon_size", self.trayMaxIconSize)
		
		createLabel(self.tableTray, text="System Tray Icon Alpha (0 to 100)", gridX=0, gridY=6, xPadding=10)
		self.trayIconHue = createEntry(self.tableTray, maxSize=6, width=8, text=TRAY_ICON_ALPHA, gridX=1, gridY=6, xExpand=True, yExpand=False, handler=self.changeOccurred)
		# Note: added below
		
		createLabel(self.tableTray, text="System Tray Icon Saturation (-100 to 100)", gridX=0, gridY=7, xPadding=10)
		self.trayIconSat = createEntry(self.tableTray, maxSize=6, width=8, text=TRAY_ICON_SAT, gridX=1, gridY=7, xExpand=True, yExpand=False, handler=self.changeOccurred)
		# Note: added below
		
		createLabel(self.tableTray, text="System Tray Icon Brightness (-100 to 100)", gridX=0, gridY=8, xPadding=10)
		self.trayIconBri = createEntry(self.tableTray, maxSize=6, width=8, text=TRAY_ICON_BRI, gridX=1, gridY=8, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("systray_icon_asb", (self.trayIconHue, self.trayIconSat, self.trayIconBri))
		
	def createClockDisplayWidgets(self):
		"""Create the Clock Display widgets."""
		self.tableClockDisplays = gtk.Table(rows=3, columns=3, homogeneous=False)
		self.tableClockDisplays.set_row_spacings(5)
		self.tableClockDisplays.set_col_spacings(5)
		
		createLabel(self.tableClockDisplays, text="Time 1 Format", gridX=0, gridY=1, xPadding=10)
		self.clock1Format = createEntry(self.tableClockDisplays, maxSize=50, width=20, text=CLOCK_FMT_1, gridX=1, gridY=1, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("time1_format", self.clock1Format)
		
		createLabel(self.tableClockDisplays, text="Time 1 Font", gridX=0, gridY=2, xPadding=10)
		self.clock1FontButton = createFontButton(self.tableClockDisplays, font=self.defaults["font"], gridX=1, gridY=2, handler=self.changeOccurred)
		self.registerComponent("time1_font", self.clock1FontButton)
		
		createLabel(self.tableClockDisplays, text="Time 2 Format", gridX=0, gridY=3, xPadding=10)
		self.clock2Format = createEntry(self.tableClockDisplays, maxSize=50, width=20, text=CLOCK_FMT_2, gridX=1, gridY=3, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("time2_format", self.clock2Format)
		
		createLabel(self.tableClockDisplays, text="Time 2 Font", gridX=0, gridY=4, xPadding=10)
		self.clock2FontButton = createFontButton(self.tableClockDisplays, font=self.defaults["font"], gridX=1, gridY=4, handler=self.changeOccurred)
		self.registerComponent("time2_font", self.clock2FontButton)
		
		createLabel(self.tableClockDisplays, text="Tooltip Format", gridX=0, gridY=5, xPadding=10)
		self.clockTooltipFormat = createEntry(self.tableClockDisplays, maxSize=50, width=20, text=CLOCK_TOOLTIP, gridX=1, gridY=5, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("clock_tooltip", self.clockTooltipFormat)
		
		self.clockArea = gtk.ScrolledWindow()
		self.clockBuf = gtk.TextBuffer()
		self.clockTextView = gtk.TextView(self.clockBuf)
		self.clockBuf.insert_at_cursor("%H 00-23 (24-hour)    %I 01-12 (12-hour)    %l 1-12 (12-hour)    %M 00-59 (minutes)\n%S 00-59 (seconds)    %P am/pm    %b Jan-Dec    %B January-December\n%a Sun-Sat    %A Sunday-Saturday    %d 01-31 (day)    %e 1-31 (day)\n%y 2 digit year, e.g. 09    %Y 4 digit year, e.g. 2009")
		self.clockTextView.set_editable(False)
		self.clockArea.add_with_viewport(self.clockTextView)
		self.tableClockDisplays.attach(self.clockArea, 0, 3, 6, 7, xpadding=10)
		
	def createClockSettingsWidgets(self):
		"""Create the Clock Settings widgets."""
		self.tableClockSettings = gtk.Table(rows=3, columns=3, homogeneous=False)
		self.tableClockSettings.set_row_spacings(5)
		self.tableClockSettings.set_col_spacings(5)
		
		createLabel(self.tableClockSettings, text="Clock Font Color", gridX=0, gridY=0, xPadding=10)
		self.clockFontCol = createEntry(self.tableClockSettings, maxSize=7, width=9, text="", gridX=1, gridY=0, xExpand=True, yExpand=False, handler=None, name="clockFontCol")
		self.clockFontCol.connect("activate", self.colorTyped)
		self.clockFontColButton = createColorButton(self.tableClockSettings, color=self.defaults["fgColor"], useAlpha=True, name="clockFontCol", gridX=2, gridY=0, handler=self.colorChange)
		self.clockFontCol.set_text(self.defaults["fgColor"])
		# Add this AFTER we set color to avoid "changed" event
		self.clockFontCol.connect("changed", self.changeOccurred)
		self.registerComponent("clock_font_color", (self.clockFontCol, self.clockFontColButton))
		
		createLabel(self.tableClockSettings, text="Padding (x, y)", gridX=0, gridY=1, xPadding=10)
		self.clockPadX = createEntry(self.tableClockSettings, maxSize=6, width=8, text=CLOCK_PADDING_X, gridX=1, gridY=1, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.clockPadY = createEntry(self.tableClockSettings, maxSize=6, width=8, text=CLOCK_PADDING_Y, gridX=2, gridY=1, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("clock_padding", (self.clockPadX, self.clockPadY))
		
		createLabel(self.tableClockSettings, text="Clock Background ID", gridX=0, gridY=2, xPadding=10)
		self.clockBg = createComboBox(self.tableClockSettings, ["0 (fully transparent)"] + range(1, len(self.bgs)), gridX=1, gridY=2, handler=self.changeOccurred)
		self.registerComponent("clock_background_id", self.clockBg)
		
		createLabel(self.tableClockSettings, text="Left Click Command", gridX=0, gridY=3, xPadding=10)
		self.clockLClick = createEntry(self.tableClockSettings, maxSize=50, width=20, text=CLOCK_LCLICK, gridX=1, gridY=3, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("clock_lclick_command", self.clockLClick)
		
		createLabel(self.tableClockSettings, text="Right Click Command", gridX=0, gridY=4, xPadding=10)
		self.clockRClick = createEntry(self.tableClockSettings, maxSize=50, width=20, text=CLOCK_RCLICK, gridX=1, gridY=4, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("clock_rclick_command", self.clockRClick)
		
		createLabel(self.tableClockSettings, text="Time 1 Timezone", gridX=0, gridY=5, xPadding=10)
		self.clockTime1Timezone = createEntry(self.tableClockSettings, maxSize=50, width=20, text=CLOCK_TIME1_TIMEZONE, gridX=1, gridY=5, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("time1_timezone", self.clockTime1Timezone)
		
		createLabel(self.tableClockSettings, text="Time 2 Timezone", gridX=0, gridY=6, xPadding=10)
		self.clockTime2Timezone = createEntry(self.tableClockSettings, maxSize=50, width=20, text=CLOCK_TIME2_TIMEZONE, gridX=1, gridY=6, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("time2_timezone", self.clockTime2Timezone)
		
		createLabel(self.tableClockSettings, text="Tooltip Timezone", gridX=0, gridY=7, xPadding=10)
		self.clockTooltipTimezone = createEntry(self.tableClockSettings, maxSize=50, width=20, text=CLOCK_TOOLTIP_TIMEZONE, gridX=1, gridY=7, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("clock_tooltip_timezone", self.clockTooltipTimezone)
		
	def createMouseWidgets(self):
		"""Creates the Mouse widgets."""
		self.tableMouse = gtk.Table(rows=4, columns=3, homogeneous=False)
		self.tableMouse.set_row_spacings(5)
		self.tableMouse.set_col_spacings(5)
		
		mouseCmds = ["none", "close", "toggle", "iconify", "shade", "toggle_iconify", "maximize_restore", "desktop_left", "desktop_right", "next_task", "prev_task"]
		
		createLabel(self.tableMouse, text="Middle Mouse Click Action", gridX=0, gridY=0, xPadding=10)
		self.mouseMiddle = createComboBox(self.tableMouse, mouseCmds, gridX=1, gridY=0, handler=self.changeOccurred)
		self.registerComponent("mouse_middle", self.mouseMiddle)
		
		createLabel(self.tableMouse, text="Right Mouse Click Action", gridX=0, gridY=1, xPadding=10)
		self.mouseRight = createComboBox(self.tableMouse, mouseCmds, gridX=1, gridY=1, handler=self.changeOccurred)
		self.registerComponent("mouse_right", self.mouseRight)
		
		createLabel(self.tableMouse, text="Mouse Wheel Scroll Up Action", gridX=0, gridY=2, xPadding=10)
		self.mouseUp = createComboBox(self.tableMouse, mouseCmds, gridX=1, gridY=2, handler=self.changeOccurred)
		self.registerComponent("mouse_scroll_up", self.mouseUp)
		
		createLabel(self.tableMouse, text="Mouse Wheel Scroll Down Action", gridX=0, gridY=3, xPadding=10)
		self.mouseDown = createComboBox(self.tableMouse, mouseCmds, gridX=1, gridY=3, handler=self.changeOccurred)
		self.registerComponent("mouse_scroll_down", self.mouseDown)
	
	def createTooltipsWidgets(self):
		"""Creates the Tooltips widgets."""
		self.tableTooltip = gtk.Table(rows=7, columns=3, homogeneous=False)
		self.tableTooltip.set_row_spacings(5)
		self.tableTooltip.set_col_spacings(5)
		
		createLabel(self.tableTooltip, text="Show Tooltips", gridX=0, gridY=0, xPadding=10)
		self.tooltipShow = createCheckButton(self.tableTooltip, active=False, gridX=1, gridY=0, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("tooltip", self.tooltipShow)
		
		createLabel(self.tableTooltip, text="Padding (x, y)", gridX=0, gridY=1, xPadding=10)
		self.tooltipPadX = createEntry(self.tableTooltip, maxSize=6, width=8, text=TOOLTIP_PADDING_X, gridX=1, gridY=1, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.tooltipPadY = createEntry(self.tableTooltip, maxSize=6, width=8, text=TOOLTIP_PADDING_Y, gridX=2, gridY=1, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("tooltip_padding", (self.tooltipPadX, self.tooltipPadY))
		
		createLabel(self.tableTooltip, text="Tooltip Show Timeout (seconds)", gridX=0, gridY=2, xPadding=10)
		self.tooltipShowTime = createEntry(self.tableTooltip, maxSize=6, width=8, text=TOOLTIP_SHOW_TIMEOUT, gridX=1, gridY=2, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("tooltip_show_timeout", self.tooltipShowTime)
		
		createLabel(self.tableTooltip, text="Tooltip Hide Timeout (seconds)", gridX=0, gridY=3, xPadding=10)
		self.tooltipHideTime = createEntry(self.tableTooltip, maxSize=6, width=8, text=TOOLTIP_HIDE_TIMEOUT, gridX=1, gridY=3, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("tooltip_hide_timeout", self.tooltipHideTime)
		
		createLabel(self.tableTooltip, text="Tooltip Background ID", gridX=0, gridY=4, xPadding=10)
		self.tooltipBg = createComboBox(self.tableTooltip, ["0 (fully transparent)"] + range(1, len(self.bgs)), gridX=1, gridY=4, handler=self.changeOccurred)
		self.registerComponent("tooltip_background_id", self.tooltipBg)
		
		createLabel(self.tableTooltip, text="Tooltip Font", gridX=0, gridY=5, xPadding=10)
		self.tooltipFont = createFontButton(self.tableTooltip, font=self.defaults["font"], gridX=1, gridY=5, handler=self.changeOccurred)
		self.registerComponent("tooltip_font", self.tooltipFont)
		
		createLabel(self.tableTooltip, text="Tooltip Font Color", gridX=0, gridY=6, xPadding=10)
		self.tooltipFontCol = createEntry(self.tableTooltip, maxSize=7, width=9, text="", gridX=1, gridY=6, xExpand=True, yExpand=False, handler=None, name="tooltipFontCol")
		self.tooltipFontCol.connect("activate", self.colorTyped)
		self.tooltipFontColButton = createColorButton(self.tableTooltip, color=self.defaults["fgColor"], useAlpha=True, name="tooltipFontCol", gridX=2, gridY=6, handler=self.colorChange)
		self.tooltipFontCol.set_text(self.defaults["fgColor"])
		# Add this AFTER we set color to avoid "changed" event
		self.tooltipFontCol.connect("changed", self.changeOccurred)
		self.registerComponent("tooltip_font_color", (self.tooltipFontCol, self.tooltipFontColButton))
	
	def createBatteryWidgets(self):
		"""Creates the Battery widgets."""
		self.tableBattery = gtk.Table(rows=8, columns=3, homogeneous=False)
		self.tableBattery.set_row_spacings(5)
		self.tableBattery.set_col_spacings(5)
				
		createLabel(self.tableBattery, text="Battery Low Status (%)", gridX=0, gridY=1, xPadding=10)
		self.batteryLow = createEntry(self.tableBattery, maxSize=6, width=8, text=BATTERY_LOW, gridX=1, gridY=1, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("battery_low_status", self.batteryLow)
		
		createLabel(self.tableBattery, text="Battery Low Action", gridX=0, gridY=2, xPadding=10)
		self.batteryLowAction = createEntry(self.tableBattery, maxSize=150, width=32, text=BATTERY_ACTION, gridX=1, gridY=2, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("battery_low_cmd", self.batteryLowAction)
		
		createLabel(self.tableBattery, text="Battery Hide (0 to 100)", gridX=0, gridY=3, xPadding=10)
		self.batteryHide = createEntry(self.tableBattery, maxSize=6, width=8, text=BATTERY_HIDE, gridX=1, gridY=3, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("battery_hide", self.batteryHide)
		
		createLabel(self.tableBattery, text="Battery 1 Font", gridX=0, gridY=4, xPadding=10)
		self.bat1FontButton = createFontButton(self.tableBattery, font=self.defaults["font"], gridX=1, gridY=4, handler=self.changeOccurred)
		self.registerComponent("bat1_font", self.bat1FontButton)
		
		createLabel(self.tableBattery, text="Battery 2 Font", gridX=0, gridY=5, xPadding=10)
		self.bat2FontButton = createFontButton(self.tableBattery, font=self.defaults["font"], gridX=1, gridY=5, handler=self.changeOccurred)
		self.registerComponent("bat2_font", self.bat2FontButton)
		
		createLabel(self.tableBattery, text="Battery Font Color", gridX=0, gridY=6, xPadding=10)
		self.batteryFontCol = createEntry(self.tableBattery, maxSize=7, width=9, text="", gridX=1, gridY=6, xExpand=True, yExpand=False, handler=None, name="batteryFontCol")
		self.batteryFontCol.connect("activate", self.colorTyped)
		self.batteryFontColButton = createColorButton(self.tableBattery, color=self.defaults["fgColor"], useAlpha=True, name="batteryFontCol", gridX=2, gridY=6, handler=self.colorChange)
		self.batteryFontCol.set_text(self.defaults["fgColor"])
		# Add this AFTER we set color to avoid "changed" event
		self.batteryFontCol.connect("changed", self.changeOccurred)
		self.registerComponent("battery_font_color", (self.batteryFontCol, self.batteryFontColButton))
		
		createLabel(self.tableBattery, text="Padding (x, y)", gridX=0, gridY=7, xPadding=10)
		self.batteryPadX = createEntry(self.tableBattery, maxSize=6, width=8, text=BATTERY_PADDING_X, gridX=1, gridY=7, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.batteryPadY = createEntry(self.tableBattery, maxSize=6, width=8, text=BATTERY_PADDING_Y, gridX=2, gridY=7, xExpand=True, yExpand=False, handler=self.changeOccurred)
		self.registerComponent("battery_padding", (self.batteryPadX, self.batteryPadY))
		
		createLabel(self.tableBattery, text="Battery Background ID", gridX=0, gridY=8, xPadding=10)
		self.batteryBg = createComboBox(self.tableBattery, ["0 (fully transparent)"] + range(1, len(self.bgs)), gridX=1, gridY=8, handler=self.changeOccurred)
		self.registerComponent("battery_background_id", self.batteryBg)
		
	def registerComponent(self, configProperty, component):
		"""Registers a component with a particular property from
		a tint2 config. Note: a component may be a double or
		triple if that property has more than one value associated
		with it."""
		self.propUI[configProperty] = component
	
	def getComponent(self, configProperty):
		"""Fetches the component associated with a tint2 property."""
		return self.propUI[configProperty] if configProperty in self.propUI else None
	
	def about(self, action=None):
		"""Displays the About dialog."""
		about = gtk.AboutDialog()
		about.set_program_name(NAME)
		about.set_version(VERSION)
		about.set_authors(AUTHORS)
		about.set_comments(COMMENTS)
		about.set_website(WEBSITE)
		gtk.about_dialog_set_url_hook(self.aboutLinkCallback)
		about.run()
		about.destroy()

	def aboutLinkCallback(dialog, link, data=None):
		"""Callback for when a URL is clicked in an About dialog."""
		try:
			webbrowser.open(link)
		except:
			errorDialog(self, "Your default web-browser could not be opened.\nPlease visit %s" % link)

	def addBg(self):
		"""Adds a new background to the list of backgrounds."""
		self.bgs += [gtk.Table(4, 3, False)]
		
		createLabel(self.bgs[-1], text="Corner Rounding (px)", gridX=0, gridY=0, xPadding=10)
		createEntry(self.bgs[-1], maxSize=7, width=9, text=BG_ROUNDING, gridX=1, gridY=0, xExpand=True, yExpand=False, handler=self.changeOccurred, name="rounded")
		
		createLabel(self.bgs[-1], text="Background Color", gridX=0, gridY=1, xPadding=10)
		temp = gtk.Entry(7)
		temp.set_width_chars(9)
		temp.set_name("bgColEntry")
		temp.set_text(self.defaults["bgColor"])
		temp.connect("changed", self.changeOccurred)
		temp.connect("activate", self.colorTyped)
		self.bgs[-1].attach(temp, 1, 2, 1, 2, xoptions=gtk.EXPAND)
		temp = gtk.ColorButton(gtk.gdk.color_parse(self.defaults["bgColor"]))
		temp.set_use_alpha(True)
		temp.set_name("bgCol")
		temp.connect("color-set", self.colorChange)
		self.bgs[-1].attach(temp, 2, 3, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		
		createLabel(self.bgs[-1], text="Border Width (px)", gridX=0, gridY=2, xPadding=10)
		createEntry(self.bgs[-1], maxSize=7, width=9, text=BG_BORDER, gridX=1, gridY=2, xExpand=True, yExpand=False, handler=self.changeOccurred, name="border")
		
		createLabel(self.bgs[-1], text="Border Color", gridX=0, gridY=3, xPadding=10)
		temp = gtk.Entry(7)
		temp.set_width_chars(9)
		temp.set_name("borderColEntry")
		temp.connect("activate", self.colorTyped)
		temp.set_text(self.defaults["borderColor"])
		temp.connect("changed", self.changeOccurred)
		self.bgs[-1].attach(temp, 1, 2, 3, 4, xoptions=gtk.EXPAND)
		temp = gtk.ColorButton(gtk.gdk.color_parse(self.defaults["borderColor"]))
		temp.set_use_alpha(True)
		temp.set_name("borderCol")
		temp.connect("color-set", self.colorChange)
		self.bgs[-1].attach(temp, 2, 3, 3, 4, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)

	# Note: Only set init to True when initialising background styles.
	# This prevents unwanted calls to changeOccurred()
	def addBgClick(self, widget=None, init=False):
		"""Creates a new background and adds a new tab to the notebook."""
		n = self.bgNotebook.get_n_pages()

		if n > (self.defaults["bgCount"] + 2):
			if confirmDialog(self, "You already have %d background styles. Are you sure you would like another?" % n) == gtk.RESPONSE_NO:
				return

		self.addBg()

		newId = len(self.bgs)

		self.bgNotebook.append_page(self.bgs[newId-1], gtk.Label("Background ID %d" % (newId)))

		self.bgNotebook.show_all()

		self.updateComboBoxes(n, "add")

		self.bgNotebook.set_current_page(n)

		if not init:
			self.changeOccurred()
	
	def addBgDefs(self, bgDefs):
		"""Add interface elements for a list of background style definitions. bgDefs
		should be a list containing dictionaries with the following keys: rounded,
		border_width, background_color, border_color"""
		for d in bgDefs:
			self.addBg()

			for child in self.bgs[-1].get_children():
				if child.get_name() == "rounded":
					child.set_text(d["rounded"])
				elif child.get_name() == "border":
					child.set_text(d["border_width"])
				elif child.get_name() == "bgColEntry":
					child.set_text(d["background_color"].split(" ")[0].strip())
					child.activate()
				elif child.get_name() == "borderColEntry":
					child.set_text(d["border_color"].split(" ")[0].strip())
					child.activate()
				elif child.get_name() == "bgCol":
					list = d["background_color"].split(" ")
					if len(list) > 1:
						child.set_alpha(int(int(list[1].strip()) * 65535 / 100.0))
					else:
						child.set_alpha(65535)
				elif child.get_name() == "borderCol":
					list = d["border_color"].split(" ")
					if len(list) > 1:
						child.set_alpha(int(int(list[1].strip()) * 65535 / 100.0))
					else:
						child.set_alpha(65535)

			newId = len(self.bgs)

			self.bgNotebook.append_page(self.bgs[newId-1], gtk.Label("Background ID %d" % (newId)))

			self.bgNotebook.show_all()

			self.updateComboBoxes(newId-1, "add")

			self.bgNotebook.set_current_page(newId)
	
	def apply(self, widget, event=None, confirmChange=True):
		"""Applies the current config to tint2."""
		# Check if tint2 is running
		procs = os.popen('pgrep -x "tint2"')			# Check list of active processes for tint2
		pids = []										# List of process ids for tint2

		for proc in procs.readlines():
			pids += [int(proc.strip().split(" ")[0])]

		procs.close()

		if self.oneConfigFile:
			# Save and copy as default
			self.save()
			tmpSrc = self.filename
			tmpDest = os.path.expandvars("${HOME}") + "/.config/tint2/tint2rc"
			try:
				shutil.copyfile(tmpSrc, tmpDest)
			except shutil.Error:
				pass
			# Ask tint2 to reload config
			for pid in pids:
				os.kill(pid, signal.SIGUSR1)
		else:
			if confirmDialog(self, "This will terminate all currently running instances of tint2 before applying config. Continue?") == gtk.RESPONSE_YES:
				if not self.save():
					return

				#shutil.copyfile(self.filename, self.filename+".backup")		# Create backup

				# If it is - kill it
				for pid in pids:
					os.kill(pid, signal.SIGTERM)

				# Lastly, start it
				os.spawnv(os.P_NOWAIT, self.tint2Bin, [self.tint2Bin, "-c", self.filename])

				if confirmChange and self.filename != (os.path.expandvars("${HOME}") + "/.config/tint2/tint2rc") and confirmDialog(self, "Use this as default tint2 config?") == gtk.RESPONSE_YES:
					tmp = self.filename
					self.filename = os.path.expandvars("${HOME}") + "/.config/tint2/tint2rc"
					try:
						shutil.copyfile(tmp, self.filename)
					except shutil.Error:
						pass

				#if confirmChange and confirmDialog(self, "Keep this config?") == gtk.RESPONSE_NO:
				#	shutil.copyfile(self.filename+".backup", self.filename)		# Create backup
				#	self.apply(widget, event, False)

	def changeAllFonts(self, widget):
		"""Changes all fonts at once."""
		dialog = gtk.FontSelectionDialog("Select Font")

		dialog.set_font_name(self.defaults["font"])

		if dialog.run() == gtk.RESPONSE_OK:
			newFont = dialog.get_font_name()

			self.clock1FontButton.set_font_name(newFont)
			self.clock2FontButton.set_font_name(newFont)
			self.bat1FontButton.set_font_name(newFont)
			self.bat2FontButton.set_font_name(newFont)
			self.fontButton.set_font_name(newFont)

		dialog.destroy()

		self.generateConfig()
		self.changeOccurred()

	def changeDefaults(self, widget=None):
		"""Shows the style preferences widget."""
		TintWizardPrefGUI(self)

	def changeOccurred(self, widget=None):
		"""Called when the user changes something, i.e. entry value"""
		self.toSave = True

		self.updateStatusBar(change=True)

		if widget == self.panelOrientation:
			if self.panelOrientation.get_active_text() == "horizontal":
				self.panelSizeLabel.set_text("Size (width, height)")
			else:
				self.panelSizeLabel.set_text("Size (height, width)")

	def colorChange(self, widget):
		"""Update the text entry when a color button is updated."""
		r = widget.get_color().red
		g = widget.get_color().green
		b = widget.get_color().blue

		label = self.getColorLabel(widget)

		# No label found
		if not label:
			return

		label.set_text(rgbToHex(r, g, b))

		self.changeOccurred()

	def colorTyped(self, widget):
		"""Update the color button when a valid value is typed into the entry."""
		s = widget.get_text()

		# The color button associated with this widget.
		colorButton = self.getColorButton(widget)

		# Just a precautionary check - this situation should never arise.
		if not colorButton:
			#print "Error in colorTyped() -- unrecognised entry widget."
			return

		# If the entered value is invalid, set textbox to the current
		# hex value of the associated color button.
		buttonHex = self.getHexFromWidget(colorButton)

		if len(s) != 7:
			errorDialog(self, "Invalid color specification: [%s]" % s)
			widget.set_text(buttonHex)
			return

		try:
			col = gtk.gdk.Color(s)
		except:
			errorDialog(self, "Invalid color specification: [%s]" % s)
			widget.set_text(buttonHex)
			return

		colorButton.set_color(col)

	# Note: only set init to True when removing backgrounds for a new config
	# This prevents unwanted calls to changeOccurred()
	def delBgClick(self, widget=None, prompt=True, init=False):
		"""Deletes the selected background after confirming with the user."""
		selected = self.bgNotebook.get_current_page()

		if selected == -1:			# Nothing to remove
			return

		if prompt:
			if confirmDialog(self, "Remove this background?") != gtk.RESPONSE_YES:
				return

		self.bgNotebook.remove_page(selected)
		self.bgs.pop(selected)

		for i in range(self.bgNotebook.get_n_pages()):
			self.bgNotebook.set_tab_label_text(self.bgNotebook.get_nth_page(i), "Background ID %d" % (i+1))

		self.bgNotebook.show_all()

		self.updateComboBoxes(len(self.bgs) + 1, "remove")

		if not init:
			self.changeOccurred()

	def generateConfig(self):
		"""Reads values from each widget and generates a config."""
		self.configBuf.delete(self.configBuf.get_start_iter(), self.configBuf.get_end_iter())
		self.configBuf.insert(self.configBuf.get_end_iter(), "# Tint2 config file\n")
		self.configBuf.insert(self.configBuf.get_end_iter(), "# Generated by tintwizard (http://code.google.com/p/tintwizard/)\n")
		self.configBuf.insert(self.configBuf.get_end_iter(), "# For information on manually configuring tint2 see http://code.google.com/p/tint2/wiki/Configure\n\n")
		if not self.oneConfigFile:
			self.configBuf.insert(self.configBuf.get_end_iter(), "# To use this as default tint2 config: save as $HOME/.config/tint2/tint2rc\n\n")

		self.configBuf.insert(self.configBuf.get_end_iter(), "# Background definitions\n")
		for i in range(len(self.bgs)):
			self.configBuf.insert(self.configBuf.get_end_iter(), "# ID %d\n" % (i + 1))

			for child in self.bgs[i].get_children():
				if child.get_name() == "rounded":
					rounded = child.get_text() if child.get_text() else BG_ROUNDING
				elif child.get_name() == "border":
					borderW = child.get_text() if child.get_text() else BG_BORDER
				elif child.get_name() == "bgCol":
					bgCol = self.getHexFromWidget(child)
					bgAlpha = int(child.get_alpha() / 65535.0 * 100)
				elif child.get_name() == "borderCol":
					borderCol = self.getHexFromWidget(child)
					borderAlpha = int(child.get_alpha() / 65535.0 * 100)

			self.configBuf.insert(self.configBuf.get_end_iter(), "rounded = %s\n" % (rounded))
			self.configBuf.insert(self.configBuf.get_end_iter(), "border_width = %s\n" % (borderW))
			self.configBuf.insert(self.configBuf.get_end_iter(), "background_color = %s %d\n" % (bgCol, bgAlpha))
			self.configBuf.insert(self.configBuf.get_end_iter(), "border_color = %s %d\n\n" % (borderCol, borderAlpha))

		self.configBuf.insert(self.configBuf.get_end_iter(), "# Panel\n")
		self.configBuf.insert(self.configBuf.get_end_iter(), "panel_monitor = %s\n" % (self.panelMonitor.get_text() if self.panelMonitor.get_text() else PANEL_MONITOR))
		self.configBuf.insert(self.configBuf.get_end_iter(), "panel_position = %s %s %s\n" % (self.panelPosY.get_active_text(), self.panelPosX.get_active_text(), self.panelOrientation.get_active_text()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "panel_size = %s %s\n" % (self.panelSizeX.get_text() if self.panelSizeX.get_text() else PANEL_SIZE_X,
															self.panelSizeY.get_text() if self.panelSizeY.get_text() else PANEL_SIZE_Y))
		self.configBuf.insert(self.configBuf.get_end_iter(), "panel_margin = %s %s\n" % (self.panelMarginX.get_text() if self.panelMarginX.get_text() else PANEL_MARGIN_X,
															self.panelMarginY.get_text() if self.panelMarginY.get_text() else PANEL_MARGIN_Y))
		self.configBuf.insert(self.configBuf.get_end_iter(), "panel_padding = %s %s %s\n" % (self.panelPadX.get_text() if self.panelPadX.get_text() else PANEL_PADDING_X,
															self.panelPadY.get_text() if self.panelPadY.get_text() else PANEL_PADDING_Y,
															self.panelSpacing.get_text() if self.panelSpacing.get_text() else TASKBAR_SPACING))
		self.configBuf.insert(self.configBuf.get_end_iter(), "panel_dock = %s\n" % int(self.panelDock.get_active()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "wm_menu = %s\n" % int(self.panelMenu.get_active()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "panel_layer = %s\n" % (self.panelLayer.get_active_text()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "panel_background_id = %s\n" % (self.panelBg.get_active()))
		
		self.configBuf.insert(self.configBuf.get_end_iter(), "\n# Panel Autohide\n")
		self.configBuf.insert(self.configBuf.get_end_iter(), "autohide = %s\n" % int(self.panelAutohide.get_active()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "autohide_show_timeout = %s\n" % (self.panelAutohideShow.get_text() if self.panelAutohideShow.get_text() else PANEL_AUTOHIDE_SHOW))
		self.configBuf.insert(self.configBuf.get_end_iter(), "autohide_hide_timeout = %s\n" % (self.panelAutohideHide.get_text() if self.panelAutohideHide.get_text() else PANEL_AUTOHIDE_HIDE))
		self.configBuf.insert(self.configBuf.get_end_iter(), "autohide_height = %s\n" % (self.panelAutohideHeight.get_text() if self.panelAutohideHeight.get_text() else PANEL_AUTOHIDE_HEIGHT))
		self.configBuf.insert(self.configBuf.get_end_iter(), "strut_policy = %s\n" % (self.panelAutohideStrut.get_active_text() if self.panelAutohideStrut.get_active_text() else PANEL_AUTOHIDE_STRUT))
		
		self.configBuf.insert(self.configBuf.get_end_iter(), "\n# Taskbar\n")
		self.configBuf.insert(self.configBuf.get_end_iter(), "taskbar_mode = %s\n" % (self.taskbarMode.get_active_text()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "taskbar_padding = %s %s %s\n" % (self.taskbarPadX.get_text() if self.taskbarPadX.get_text() else TASKBAR_PADDING_X,
															self.taskbarPadY.get_text() if self.taskbarPadY.get_text() else TASKBAR_PADDING_X,
															self.taskbarSpacing.get_text() if self.taskbarSpacing.get_text() else TASK_SPACING))
		self.configBuf.insert(self.configBuf.get_end_iter(), "taskbar_background_id = %s\n" % (self.taskbarBg.get_active()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "taskbar_active_background_id = %s\n" % (self.taskbarActiveBg.get_active()))

		self.configBuf.insert(self.configBuf.get_end_iter(), "\n# Tasks\n")
		self.configBuf.insert(self.configBuf.get_end_iter(), "urgent_nb_of_blink = %s\n" % (self.taskBlinks.get_text() if self.taskBlinks.get_text() else TASK_BLINKS))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_icon = %s\n" % int(self.taskIconCheckButton.get_active()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_text = %s\n" % int(self.taskTextCheckButton.get_active()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_centered = %s\n" % int(self.taskCentreCheckButton.get_active()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_maximum_size = %s %s\n" % (self.taskMaxSizeX.get_text() if self.taskMaxSizeX.get_text() else TASK_MAXIMUM_SIZE_X, self.taskMaxSizeY.get_text() if self.taskMaxSizeY.get_text() else TASK_MAXIMUM_SIZE_Y))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_padding = %s %s\n" % (self.taskPadX.get_text() if self.taskPadX.get_text() else TASK_PADDING_X,
															self.taskPadY.get_text() if self.taskPadY.get_text() else TASK_PADDING_Y))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_background_id = %s\n" % (self.taskBg.get_active()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_active_background_id = %s\n" % (self.taskActiveBg.get_active()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_urgent_background_id = %s\n" % (self.taskUrgentBg.get_active()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_iconified_background_id = %s\n" % (self.taskIconifiedBg.get_active()))
		
		self.configBuf.insert(self.configBuf.get_end_iter(), "\n# Task Icons\n")
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_icon_asb = %s %s %s\n" % (self.iconHue.get_text() if self.iconHue.get_text() else ICON_ALPHA,
															self.iconSat.get_text() if self.iconSat.get_text() else ICON_SAT,
															self.iconBri.get_text() if self.iconBri.get_text() else ICON_BRI))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_active_icon_asb = %s %s %s\n" % (self.activeIconHue.get_text() if self.activeIconHue.get_text() else ACTIVE_ICON_ALPHA,
															self.activeIconSat.get_text() if self.activeIconSat.get_text() else ACTIVE_ICON_SAT,
															self.activeIconBri.get_text() if self.activeIconBri.get_text() else ACTIVE_ICON_BRI))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_urgent_icon_asb = %s %s %s\n" % (self.urgentIconHue.get_text() if self.urgentIconHue.get_text() else URGENT_ICON_ALPHA,
															self.urgentIconSat.get_text() if self.urgentIconSat.get_text() else URGENT_ICON_SAT,
															self.urgentIconBri.get_text() if self.urgentIconBri.get_text() else URGENT_ICON_BRI))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_iconified_icon_asb = %s %s %s\n" % (self.iconifiedIconHue.get_text() if self.iconifiedIconHue.get_text() else ICONIFIED_ICON_ALPHA,
															self.iconifiedIconSat.get_text() if self.iconifiedIconSat.get_text() else ICONIFIED_ICON_SAT,
															self.iconifiedIconBri.get_text() if self.iconifiedIconBri.get_text() else ICONIFIED_ICON_BRI))
															
		self.configBuf.insert(self.configBuf.get_end_iter(), "\n# Fonts\n")
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_font = %s\n" % (self.fontButton.get_font_name()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_font_color = %s %s\n" % (self.getHexFromWidget(self.fontColButton),
															int(self.fontColButton.get_alpha() / 65535.0 * 100)))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_active_font_color = %s %s\n" % (self.getHexFromWidget(self.fontActiveColButton),
															int(self.fontActiveColButton.get_alpha() / 65535.0 * 100)))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_urgent_font_color = %s %s\n" % (self.getHexFromWidget(self.fontUrgentColButton),
															int(self.fontUrgentColButton.get_alpha() / 65535.0 * 100)))
		self.configBuf.insert(self.configBuf.get_end_iter(), "task_iconified_font_color = %s %s\n" % (self.getHexFromWidget(self.fontIconifiedColButton),
															int(self.fontIconifiedColButton.get_alpha() / 65535.0 * 100)))
		self.configBuf.insert(self.configBuf.get_end_iter(), "font_shadow = %s\n" % int(self.fontShadowCheckButton.get_active()))

		self.configBuf.insert(self.configBuf.get_end_iter(), "\n# System Tray\n")
		self.configBuf.insert(self.configBuf.get_end_iter(), "systray_padding = %s %s %s\n" % (self.trayPadX.get_text() if self.trayPadX.get_text() else TRAY_PADDING_X,
															self.trayPadY.get_text() if self.trayPadY.get_text() else TRAY_PADDING_Y,
															self.traySpacing.get_text() if self.traySpacing.get_text() else TRAY_SPACING))
		self.configBuf.insert(self.configBuf.get_end_iter(), "systray_sort = %s\n" % (self.trayOrder.get_active_text()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "systray_background_id = %s\n" % (self.trayBg.get_active()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "systray_icon_size = %s\n" % (self.trayMaxIconSize.get_text() if self.trayMaxIconSize.get_text() else TRAY_MAX_ICON_SIZE))
		self.configBuf.insert(self.configBuf.get_end_iter(), "systray_icon_asb = %s %s %s\n" % (self.trayIconHue.get_text() if self.trayIconHue.get_text() else TRAY_ICON_ALPHA,
															self.trayIconSat.get_text() if self.trayIconSat.get_text() else TRAY_ICON_SAT,
															self.trayIconBri.get_text() if self.trayIconBri.get_text() else TRAY_ICON_BRI))
		
		self.configBuf.insert(self.configBuf.get_end_iter(), "\n# Clock\n")
		self.configBuf.insert(self.configBuf.get_end_iter(), "time1_format = %s\n" % (self.clock1Format.get_text() if self.clock1Format.get_text() else CLOCK_FMT_1))
		self.configBuf.insert(self.configBuf.get_end_iter(), "time1_font = %s\n" % (self.clock1FontButton.get_font_name()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "time2_format = %s\n" % (self.clock2Format.get_text() if self.clock2Format.get_text() else CLOCK_FMT_2))
		self.configBuf.insert(self.configBuf.get_end_iter(), "time2_font = %s\n" % (self.clock2FontButton.get_font_name()))
		
		self.configBuf.insert(self.configBuf.get_end_iter(), "clock_font_color = %s %s\n" % (self.getHexFromWidget(self.clockFontColButton),
														int(self.clockFontColButton.get_alpha() / 65535.0 * 100)))
	
		self.configBuf.insert(self.configBuf.get_end_iter(), "clock_tooltip = %s\n" % (self.clockTooltipFormat.get_text() if self.clockTooltipFormat.get_text() else CLOCK_TOOLTIP))
		self.configBuf.insert(self.configBuf.get_end_iter(), "clock_padding = %s %s\n" % (self.clockPadX.get_text() if self.clockPadX.get_text() else CLOCK_PADDING_X,
														self.clockPadY.get_text() if self.clockPadY.get_text() else CLOCK_PADDING_Y))
		self.configBuf.insert(self.configBuf.get_end_iter(), "clock_background_id = %s\n" % (self.clockBg.get_active()))
		if self.clockLClick.get_text():
			self.configBuf.insert(self.configBuf.get_end_iter(), "clock_lclick_command = %s\n" % (self.clockLClick.get_text()))
		if self.clockRClick.get_text():
			self.configBuf.insert(self.configBuf.get_end_iter(), "clock_rclick_command = %s\n" % (self.clockRClick.get_text()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "time1_timezone = %s\n" % (self.clockTime1Timezone.get_text() if self.clockTime1Timezone.get_text() else CLOCK_TIME1_TIMEZONE))
		self.configBuf.insert(self.configBuf.get_end_iter(), "time2_timezone = %s\n" % (self.clockTime2Timezone.get_text() if self.clockTime2Timezone.get_text() else CLOCK_TIME2_TIMEZONE))
		self.configBuf.insert(self.configBuf.get_end_iter(), "clock_tooltip_timezone = %s\n" % (self.clockTooltipTimezone.get_text() if self.clockTooltipTimezone.get_text() else CLOCK_TOOLTIP_TIMEZONE))
			
			
		self.configBuf.insert(self.configBuf.get_end_iter(), "\n# Tooltips\n")
		self.configBuf.insert(self.configBuf.get_end_iter(), "tooltip = %s\n" % int(self.tooltipShow.get_active()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "tooltip_padding = %s %s\n" % (self.tooltipPadX.get_text() if self.tooltipPadX.get_text() else TOOLTIP_PADDING_Y,
															self.tooltipPadY.get_text() if self.tooltipPadY.get_text() else TOOLTIP_PADDING_Y))
		self.configBuf.insert(self.configBuf.get_end_iter(), "tooltip_show_timeout = %s\n" % (self.tooltipShowTime.get_text() if self.tooltipShowTime.get_text() else TOOLTIP_SHOW_TIMEOUT))
		self.configBuf.insert(self.configBuf.get_end_iter(), "tooltip_hide_timeout = %s\n" % (self.tooltipHideTime.get_text() if self.tooltipHideTime.get_text() else TOOLTIP_HIDE_TIMEOUT))
		self.configBuf.insert(self.configBuf.get_end_iter(), "tooltip_background_id = %s\n" % (self.tooltipBg.get_active()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "tooltip_font = %s\n" % (self.tooltipFont.get_font_name()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "tooltip_font_color = %s %s\n" % (self.getHexFromWidget(self.tooltipFontColButton),
															int(self.tooltipFontColButton.get_alpha() / 65535.0 * 100)))

		self.configBuf.insert(self.configBuf.get_end_iter(), "\n# Mouse\n")
		self.configBuf.insert(self.configBuf.get_end_iter(), "mouse_middle = %s\n" % (self.mouseMiddle.get_active_text()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "mouse_right = %s\n" % (self.mouseRight.get_active_text()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "mouse_scroll_up = %s\n" % (self.mouseUp.get_active_text()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "mouse_scroll_down = %s\n" % (self.mouseDown.get_active_text()))

		self.configBuf.insert(self.configBuf.get_end_iter(), "\n# Battery\n")
		self.configBuf.insert(self.configBuf.get_end_iter(), "battery_low_status = %s\n" % (self.batteryLow.get_text() if self.batteryLow.get_text() else BATTERY_LOW))
		self.configBuf.insert(self.configBuf.get_end_iter(), "battery_low_cmd = %s\n" % (self.batteryLowAction.get_text() if self.batteryLowAction.get_text() else BATTERY_ACTION))
		self.configBuf.insert(self.configBuf.get_end_iter(), "battery_hide = %s\n" % (self.batteryHide.get_text() if self.batteryHide.get_text() else BATTERY_HIDE))
		self.configBuf.insert(self.configBuf.get_end_iter(), "bat1_font = %s\n" % (self.bat1FontButton.get_font_name()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "bat2_font = %s\n" % (self.bat2FontButton.get_font_name()))
		self.configBuf.insert(self.configBuf.get_end_iter(), "battery_font_color = %s %s\n" % (self.getHexFromWidget(self.batteryFontColButton),
															int(self.batteryFontColButton.get_alpha() / 65535.0 * 100)))
		self.configBuf.insert(self.configBuf.get_end_iter(), "battery_padding = %s %s\n" % (self.batteryPadX.get_text() if self.batteryPadX.get_text() else BATTERY_PADDING_Y,
															self.batteryPadY.get_text() if self.batteryPadY.get_text() else BATTERY_PADDING_Y))
		self.configBuf.insert(self.configBuf.get_end_iter(), "battery_background_id = %s\n" % (self.batteryBg.get_active()))

		self.configBuf.insert(self.configBuf.get_end_iter(), "\n# End of config")

	def getColorButton(self, widget):
		"""Returns the color button associated with widget."""
		if widget.get_name() == "fontCol":
			return self.fontColButton
		elif widget.get_name() == "fontActiveCol":
			return self.fontActiveColButton
		elif widget.get_name() == "fontUrgentCol":
			return self.fontUrgentColButton
		elif widget.get_name() == "fontIconifiedCol":
			return self.fontIconifiedColButton
		elif widget.get_name() == "clockFontCol":
			return self.clockFontColButton
		elif widget.get_name() == "batteryFontCol":
			return self.batteryFontColButton
		elif widget.get_name() == "tooltipFontCol":
			return self.tooltipFontColButton
		elif widget.get_name() == "bgColEntry":
			bgID = self.bgNotebook.get_current_page()

			for child in self.bgs[bgID].get_children():
				if child.get_name() == "bgCol":

					return child
		elif widget.get_name() == "borderColEntry":
			bgID = self.bgNotebook.get_current_page()

			for child in self.bgs[bgID].get_children():
				if child.get_name() == "borderCol":

					return child

		# No button found which matches label
		return None

	def getColorLabel(self, widget):
		"""Gets the color label associated with a color button."""
		if widget.get_name() == "fontCol":
			return self.fontCol
		elif widget.get_name() == "fontActiveCol":
			return self.fontActiveCol
		elif widget.get_name() == "fontUrgentCol":
			return self.fontUrgentCol
		elif widget.get_name() == "fontIconifiedCol":
			return self.fontIconifiedCol
		elif widget.get_name() == "clockFontCol":
			return self.clockFontCol
		elif widget.get_name() == "batteryFontCol":
			return self.batteryFontCol
		elif widget.get_name() == "tooltipFontCol":
			return self.tooltipFontCol
		elif widget.get_name() == "bgCol":
			bgID = self.bgNotebook.get_current_page()

			for child in self.bgs[bgID].get_children():
				if child.get_name() == "bgColEntry":

					return child
		elif widget.get_name() == "borderCol":
			bgID = self.bgNotebook.get_current_page()

			for child in self.bgs[bgID].get_children():
				if child.get_name() == "borderColEntry":

					return child

		# No label found which matches color button
		return None

	def getHexFromWidget(self, widget):
		"""Returns the #RRGGBB value of a widget."""
		r = widget.get_color().red
		g = widget.get_color().green
		b = widget.get_color().blue

		return rgbToHex(r, g, b)

	def help(self, action=None):
		"""Opens the Help wiki page in the default web browser."""
		try:
			webbrowser.open("http://code.google.com/p/tintwizard/wiki/Help")
		except:
			errorDialog(self, "Your default web-browser could not be opened.\nPlease visit http://code.google.com/p/tintwizard/wiki/Help")
	
	def main(self):
		"""Enters the main loop."""
		gtk.main()
	
	def new(self, action=None):
		"""Prepares a new config."""
		if self.toSave:
			self.savePrompt()
		
		self.toSave = True
		self.filename = None

		self.resetConfig()

		self.generateConfig()
		self.updateStatusBar("New Config File [*]")

	def openDef(self, widget=None):
		"""Opens the default tint2 config."""
		self.openFile(default=True)

	def openFile(self, widget=None, default=False):
		"""Reads from a config file. If default=True, open the tint2 default config."""
		self.new()

		if not default:
			chooser = gtk.FileChooserDialog("Open Config File", self, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
			chooser.set_default_response(gtk.RESPONSE_OK)

			if self.curDir != None:
				chooser.set_current_folder(self.curDir)

			chooserFilter = gtk.FileFilter()
			chooserFilter.set_name("All files")
			chooserFilter.add_pattern("*")
			chooser.add_filter(chooserFilter)
			chooser.show()

			response = chooser.run()

			if response == gtk.RESPONSE_OK:
				self.filename = chooser.get_filename()
				self.curDir = os.path.dirname(self.filename)
			else:
				chooser.destroy()
				return

			chooser.destroy()
		else:
			self.filename = os.path.expandvars("$HOME/.config/tint2/tint2rc")
			self.curDir = os.path.expandvars("$HOME/.config/tint2")

		self.readTint2Config()
		self.generateConfig()
		self.updateStatusBar()

	def parseBgs(self, string):
		"""Parses the background definitions from a string."""
		s = string.split("\n")

		bgDefs = []
		cur = -1
		bgKeys = ["border_width", "background_color", "border_color"]
		newString = ""

		for line in s:
			data = [token.strip() for token in line.split("=")]

			if data[0] == "rounded":					# It may be considered bad practice to
				bgDefs += [{"rounded": data[1]}]		# find each style definition with an
			elif data[0] in bgKeys:						# arbitrary value, but tint2 does the same.
				bgDefs[cur][data[0]] = data[1]			# This means that any existing configs must
			else:										# start with 'rounded'.
				newString += "%s\n" % line

		self.addBgDefs(bgDefs)

		return newString

	def parseConfig(self, string):
		"""Parses the contents of a config file."""
		for line in string.split("\n"):
			s = line.split("=")												# Create a list with KEY and VALUE

			e = s[0].strip()												# Strip whitespace from KEY

			if e == "time1_format":											# Set the VALUE of KEY
				self.parseProp(self.getComponent(e), s[1], True, "time1")
			elif e == "time2_format":
				self.parseProp(self.getComponent(e), s[1], True, "time2")
			elif e == "clock_tooltip":
				self.parseProp(self.getComponent(e), s[1], True, "clock_tooltip")
			elif e == "time1_timezone":
				self.parseProp(self.getComponent(e), s[1], True, "time1_timezone")
			elif e == "time2_timezone":
				self.parseProp(self.getComponent(e), s[1], True, "time2_timezone")
			elif e == "clock_tooltip_timezone":
				self.parseProp(self.getComponent(e), s[1], True, "tooltip_timezone")
			elif e == "systray_padding":
				self.parseProp(self.getComponent(e), s[1], True, "tray")
			elif e == "taskbar_active_background_id":
				self.parseProp(self.getComponent(e), s[1], True, "activeBg")
			else:
				component = self.getComponent(e)
				if component != None:
					self.parseProp(self.getComponent(e), s[1])

	def parseProp(self, prop, string, special=False, propType=""):
		"""Parses a variable definition from the conf file and updates the correct UI widget."""
		string = string.strip()										# Remove whitespace from the VALUE
		eType = type(prop)											# Get widget type

		if eType == gtk.Entry:
			prop.set_text(string)
			prop.activate()
		elif eType == gtk.ComboBox:
			# This allows us to select the correct combo-box value.
			if string in ["bottom", "top", "left", "right", "center", "single_desktop", "multi_desktop", "single_monitor",
							"none", "close", "shade", "iconify", "toggle", "toggle_iconify", "maximize_restore",
							"desktop_left", "desktop_right", "horizontal", "vertical", "ascending", "descending",
							"left2right", "right2left", "next_task", "prev_task", "minimum", "follow_size", "normal"]:
				if string in ["bottom", "left", "single_desktop", "none", "horizontal", "ascending"]:
					i = 0
				elif string in ["top", "right", "multi_desktop", "close", "vertical", "descending", "minimum"]:
					i = 1
				elif string in ["center", "single_monitor", "toggle", "left2right", "follow_size", "normal"]:
					i = 2
				elif string in ["right2left"]:
					i = 3
				else:
					i = ["none", "close", "toggle", "iconify", "shade", "toggle_iconify", "maximize_restore",
						"desktop_left", "desktop_right", "next_task", "prev_task"].index(string)

				prop.set_active(i)
			else:
				prop.set_active(int(string))
		elif eType == gtk.CheckButton:
			prop.set_active(bool(int(string)))
		elif eType == gtk.FontButton:
			prop.set_font_name(string)
		elif eType == gtk.ColorButton:
			prop.set_alpha(int(int(string) * 65535 / 100.0))
		elif eType == tuple:									# If a property has more than 1 value, for example the x and y co-ords
			s = string.split(" ")								# of the padding properties, then just we use recursion to set the
			for i in range(len(prop)):							# value of each associated widget.
				if i >= len(s):
					self.parseProp(prop[i], "0")
				else:
					self.parseProp(prop[i], s[i])

	def quit(self, widget, event=None):
		"""Asks if user would like to save file before quitting, then quits the program."""
		if self.toSave:
			if self.oneConfigFile:
				response = gtk.RESPONSE_YES
			else:
				dialog = gtk.Dialog("Save config?", self, gtk.DIALOG_MODAL, (gtk.STOCK_YES, gtk.RESPONSE_YES, gtk.STOCK_NO, gtk.RESPONSE_NO, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
				dialog.get_content_area().add(gtk.Label("Save config before quitting?"))
				dialog.get_content_area().set_size_request(300, 100)
				dialog.show_all()
				response = dialog.run()
				dialog.destroy()

			if response == gtk.RESPONSE_CANCEL:
				return True							# Return True to stop it quitting when we hit "Cancel"
			elif response == gtk.RESPONSE_NO:
				gtk.main_quit()
			elif response == gtk.RESPONSE_YES:
				self.save()
				gtk.main_quit()
		else:
			gtk.main_quit()

	def readConf(self):
		"""Reads the tintwizard configuration file - NOT tint2 config files."""
		self.defaults = {"font": None, "bgColor": None, "fgColor": None, "borderColor": None, "bgCount": None}

		if self.oneConfigFile:
			# don't need tintwizard.conf
			return

		pathName = os.path.expandvars("${HOME}") + "/.config/tint2/"

		if not os.path.exists(pathName + "tintwizard.conf"):
			self.writeConf()
			return

		f = open(pathName + "tintwizard.conf", "r")

		for line in f:
			if "=" in line:
				l = line.split("=")

				if self.defaults.has_key(l[0].strip()):
					self.defaults[l[0].strip()] = l[1].strip()

	def readTint2Config(self):
		"""Reads in from a config file."""
		f = open(self.filename, "r")

		string = ""

		for line in f:
			if (line[0] != "#") and (len(line) > 2):
				string += line

		f.close()

		# Remove all background styles so we can create new ones as we read them
		for i in range(len(self.bgs)):
			self.delBgClick(None, False)

		# As we parse background definitions, we build a new string
		# without the background related stuff. This means we don't
		# have to read through background defs AGAIN when parsing
		# the other stuff.
		noBgDefs = self.parseBgs(string)

		self.parseConfig(noBgDefs)
	
	def reportBug(self, action=None):
		"""Opens the bug report page in the default web browser."""
		try:
			webbrowser.open("http://code.google.com/p/tintwizard/issues/entry")
		except:
			errorDialog(self, "Your default web-browser could not be opened.\nPlease visit http://code.google.com/p/tintwizard/issues/entry")

	
	def resetConfig(self):
		"""Resets all the widgets to their default values."""
		# Backgrounds
		for i in range(len(self.bgs)):
			self.delBgClick(prompt=False, init=True)

		for i in range(self.defaults["bgCount"]):
			self.addBgClick(init=True)

		self.bgNotebook.set_current_page(0)

		# Panel
		self.panelPosY.set_active(0)
		self.panelPosX.set_active(0)
		self.panelOrientation.set_active(0)
		self.panelItems.set_text(PANEL_ITEMS)
		self.panelSizeX.set_text(PANEL_SIZE_X)
		self.panelSizeY.set_text(PANEL_SIZE_Y)
		self.panelMarginX.set_text(PANEL_MARGIN_X)
		self.panelMarginY.set_text(PANEL_MARGIN_Y)
		self.panelPadX.set_text(PANEL_PADDING_Y)
		self.panelPadY.set_text(PANEL_PADDING_Y)
		self.panelSpacing.set_text(TASKBAR_SPACING)
		self.panelBg.set_active(0)
		self.panelMenu.set_active(0)
		self.panelDock.set_active(0)
		self.panelLayer.set_active(0)
		self.panelMonitor.set_text(PANEL_MONITOR)
		self.panelAutohide.set_active(0)
		self.panelAutohideShow.set_text(PANEL_AUTOHIDE_SHOW)
		self.panelAutohideHide.set_text(PANEL_AUTOHIDE_HIDE)
		self.panelAutohideHeight.set_text(PANEL_AUTOHIDE_HEIGHT)
		self.panelAutohideStrut.set_active(0)
		# Taskbar
		self.taskbarMode.set_active(0)
		self.taskbarPadX.set_text(TASKBAR_PADDING_X)
		self.taskbarPadY.set_text(TASKBAR_PADDING_Y)
		self.taskbarSpacing.set_text(TASK_SPACING)
		self.taskbarBg.set_active(0)
		self.taskbarActiveBg.set_active(0)
		# Tasks
		self.taskBlinks.set_text(TASK_BLINKS)
		self.taskCentreCheckButton.set_active(True)
		self.taskTextCheckButton.set_active(True)
		self.taskIconCheckButton.set_active(True)
		self.taskMaxSizeX.set_text(TASK_MAXIMUM_SIZE_X)
		self.taskMaxSizeY.set_text(TASK_MAXIMUM_SIZE_Y)
		self.taskPadX.set_text(TASK_PADDING_X)
		self.taskPadY.set_text(TASK_PADDING_Y)
		self.taskBg.set_active(0)
		self.taskActiveBg.set_active(0)
		self.taskUrgentBg.set_active(0)
		self.taskIconifiedBg.set_active(0)
		# Icons
		self.iconHue.set_text(ICON_ALPHA)
		self.iconSat.set_text(ICON_SAT)
		self.iconBri.set_text(ICON_BRI)
		self.activeIconHue.set_text(ACTIVE_ICON_ALPHA)
		self.activeIconSat.set_text(ACTIVE_ICON_SAT)
		self.activeIconBri.set_text(ACTIVE_ICON_BRI)
		self.urgentIconHue.set_text(URGENT_ICON_ALPHA)
		self.urgentIconSat.set_text(URGENT_ICON_SAT)
		self.urgentIconBri.set_text(URGENT_ICON_BRI)
		self.iconifiedIconHue.set_text(ICONIFIED_ICON_ALPHA)
		self.iconifiedIconSat.set_text(ICONIFIED_ICON_SAT)
		self.iconifiedIconBri.set_text(ICONIFIED_ICON_BRI)
		# Fonts
		self.fontButton.set_font_name(self.defaults["font"])
		self.fontColButton.set_alpha(65535)
		self.fontColButton.set_color(gtk.gdk.color_parse(self.defaults["fgColor"]))
		self.fontCol.set_text(self.defaults["fgColor"])
		self.fontActiveColButton.set_alpha(65535)
		self.fontActiveColButton.set_color(gtk.gdk.color_parse(self.defaults["fgColor"]))
		self.fontActiveCol.set_text(self.defaults["fgColor"])
		self.fontUrgentColButton.set_alpha(65535)
		self.fontUrgentColButton.set_color(gtk.gdk.color_parse(self.defaults["fgColor"]))
		self.fontUrgentCol.set_text(self.defaults["fgColor"])
		self.fontIconifiedColButton.set_alpha(65535)
		self.fontIconifiedColButton.set_color(gtk.gdk.color_parse(self.defaults["fgColor"]))
		self.fontIconifiedCol.set_text(self.defaults["fgColor"])
		self.fontShadowCheckButton.set_active(False)
		# System Tray
		self.trayPadX.set_text(TRAY_PADDING_X)
		self.trayPadY.set_text(TRAY_PADDING_X)
		self.traySpacing.set_text(TRAY_SPACING)
		self.trayOrder.set_active(0)
		self.trayBg.set_active(0)
		self.trayMaxIconSize.set_text(TRAY_MAX_ICON_SIZE)
		self.trayIconHue.set_text(TRAY_ICON_ALPHA)
		self.trayIconSat.set_text(TRAY_ICON_SAT)
		self.trayIconBri.set_text(TRAY_ICON_BRI)
		# Clock
		self.clock1Format.set_text(CLOCK_FMT_1)
		self.clock1FontButton.set_font_name(self.defaults["font"])
		self.clock2Format.set_text(CLOCK_FMT_2)
		self.clockTooltipFormat.set_text(CLOCK_TOOLTIP)
		self.clock2FontButton.set_font_name(self.defaults["font"])
		self.clockFontColButton.set_alpha(65535)
		self.clockFontColButton.set_color(gtk.gdk.color_parse(self.defaults["fgColor"]))
		self.clockFontCol.set_text(self.defaults["fgColor"])
		self.clockPadX.set_text(CLOCK_PADDING_X)
		self.clockPadY.set_text(CLOCK_PADDING_Y)
		self.clockBg.set_active(0)
		self.clockLClick.set_text(CLOCK_LCLICK)
		self.clockRClick.set_text(CLOCK_RCLICK)
		self.clockTime1Timezone.set_text(CLOCK_TIME1_TIMEZONE)
		self.clockTime2Timezone.set_text(CLOCK_TIME2_TIMEZONE)
		self.clockTooltipTimezone.set_text(CLOCK_TOOLTIP_TIMEZONE)
		# Tooltips
		self.tooltipShow.set_active(False)
		self.tooltipPadX.set_text(TOOLTIP_PADDING_X)
		self.tooltipPadY.set_text(TOOLTIP_PADDING_Y)
		self.tooltipShowTime.set_text(TOOLTIP_SHOW_TIMEOUT)
		self.tooltipHideTime.set_text(TOOLTIP_HIDE_TIMEOUT)
		self.tooltipBg.set_active(0)
		self.tooltipFont.set_font_name(self.defaults["font"])
		self.tooltipFontColButton.set_alpha(65535)
		self.tooltipFontColButton.set_color(gtk.gdk.color_parse(self.defaults["fgColor"]))
		self.tooltipFontCol.set_text(self.defaults["fgColor"])
		# Mouse
		self.mouseMiddle.set_active(0)
		self.mouseRight.set_active(0)
		self.mouseUp.set_active(0)
		self.mouseDown.set_active(0)
		# Battery
		self.batteryLow.set_text(BATTERY_LOW)
		self.batteryLowAction.set_text(BATTERY_ACTION)
		self.batteryHide.set_text(BATTERY_HIDE)
		self.bat1FontButton.set_font_name(self.defaults["font"])
		self.bat2FontButton.set_font_name(self.defaults["font"])
		self.batteryFontColButton.set_alpha(65535)
		self.batteryFontColButton.set_color(gtk.gdk.color_parse(self.defaults["fgColor"]))
		self.batteryFontCol.set_text(self.defaults["fgColor"])
		self.batteryPadX.set_text(BATTERY_PADDING_Y)
		self.batteryPadY.set_text(BATTERY_PADDING_Y)
		self.batteryBg.set_active(0)
	
	def save(self, widget=None, event=None):
		"""Saves the generated config file."""

		# This function returns the boolean status of whether or not the
		# file saved, so that the apply() function knows if it should
		# kill the tint2 process and apply the new config.

		# If no file has been selected, force the user to "Save As..."
		if self.filename == None:
			return self.saveAs()
		else:
			self.generateConfig()
			self.writeFile()

			return True

	def saveAs(self, widget=None, event=None):
		"""Prompts the user to select a file and then saves the generated config file."""
		self.generateConfig()

		chooser = gtk.FileChooserDialog("Save Config File As...", self, gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
		chooser.set_default_response(gtk.RESPONSE_OK)

		if self.curDir != None:
			chooser.set_current_folder(self.curDir)

		chooserFilter = gtk.FileFilter()
		chooserFilter.set_name("All files")
		chooserFilter.add_pattern("*")
		chooser.add_filter(chooserFilter)
		chooser.show()

		response = chooser.run()

		if response == gtk.RESPONSE_OK:
			self.filename = chooser.get_filename()

			if os.path.exists(self.filename):
				overwrite = confirmDialog(self, "This file already exists. Overwrite this file?")

				if overwrite == gtk.RESPONSE_YES:
					self.writeFile()
					chooser.destroy()
					return True
				else:
					self.filename = None
					chooser.destroy()
					return False
			else:
				self.writeFile()
				chooser.destroy()
				return True
		else:
			self.filename = None
			chooser.destroy()
			return False

	def saveAsDef(self, widget=None, event=None):
		"""Saves the config as the default tint2 config."""
		if confirmDialog(self, "Overwrite current tint2 default config?") == gtk.RESPONSE_YES:
			self.filename = os.path.expandvars("${HOME}") + "/.config/tint2/tint2rc"
			self.curDir = os.path.expandvars("${HOME}") + "/.config/tint2"

			# If, for whatever reason, tint2 has no default config - create one.
			if not os.path.isfile(self.filename):
				f = open(self.filename, "w")
				f.write("# tint2rc")
				f.close()

			self.generateConfig()
			self.writeFile()

			return True

	def savePrompt(self):
		"""Prompt the user to save before creating a new file."""
		if confirmDialog(self, "Save current config?") == gtk.RESPONSE_YES:
			self.save(None)

	def switchPage(self, notebook, page, page_num):
		"""Handles notebook page switch events."""

		# If user selects the 'View Config' tab, update the textarea within this tab.
		if notebook.get_tab_label_text(notebook.get_nth_page(page_num)) == "View Config":
			self.generateConfig()

	def updateComboBoxes(self, i, action="add"):
		"""Updates the contents of a combo box when a background style has been added/removed."""
		cbs = [self.batteryBg, self.clockBg, self.taskbarBg, self.taskbarActiveBg, self.trayBg, self.taskActiveBg, self.taskBg, self.panelBg, self.tooltipBg, self.taskUrgentBg, self.taskIconifiedBg]

		if action == "add":
			for cb in cbs:
				cb.append_text(str(i+1))
		else:
			for cb in cbs:
				if cb.get_active() == i:		# If background is selected, set to a different value
					cb.set_active(0)

				cb.remove_text(i)

	def updateStatusBar(self, message="", change=False):
		"""Updates the message on the statusbar. A message can be provided,
		and if change is set to True (i.e. something has been modified) then
		an appropriate symbol [*] is shown beside filename."""
		contextID = self.statusBar.get_context_id("")

		self.statusBar.pop(contextID)

		if not message:
			message = "%s %s" % (self.filename or "New Config File", "[*]" if change else "")

		self.statusBar.push(contextID, message)

	def writeConf(self):
		"""Writes the tintwizard configuration file."""
		confStr = "#Start\n[defaults]\n"

		for key in self.defaults:
			confStr += "%s = %s\n" % (key, str(self.defaults[key]))
		
		confStr += "#End\n"
		
		pathName = os.path.expandvars("${HOME}") + "/.config/tint2/"
		
		f = open(pathName+"tintwizard.conf", "w")
		
		f.write(confStr)
		
		f.close()

	def writeFile(self):
		"""Writes the contents of the config text buffer to file."""
		try:
			f = open(self.filename, "w")

			f.write(self.configBuf.get_text(self.configBuf.get_start_iter(), self.configBuf.get_end_iter()))

			f.close()

			self.toSave = False

			self.curDir = os.path.dirname(self.filename)

			self.updateStatusBar()
		except IOError:
			errorDialog(self, "Could not save file")

# General use functions
def createLabel(parent, text="", gridX=0, gridY=0, sizeX=1, sizeY=1, xPadding=0):
	"""Creates a label and adds it to a parent widget."""
	
	temp = gtk.Label(text)
	temp.set_alignment(0, 0.5)
	parent.attach(temp, gridX, gridX+sizeX, gridY, gridY+sizeY, xpadding=xPadding)
	return temp

def createComboBox(parent, choices=["null"], active=0, gridX=0, gridY=0, sizeX=1, sizeY=1, xExpand=True, yExpand=True, handler=None):
	"""Creates a combo box with text choices and adds it to a parent widget."""
	temp = gtk.combo_box_new_text()
	
	for choice in choices:
		temp.append_text(choice)
	
	temp.set_active(active)
	
	if handler != None:
		temp.connect("changed", handler)
	
	parent.attach(temp, gridX, gridX+sizeX, gridY, gridY+sizeY, xoptions=gtk.EXPAND if xExpand else 0, yoptions=gtk.EXPAND if yExpand else 0)
	
	return temp

def createEntry(parent, maxSize, width, text="", gridX=0, gridY=0, sizeX=1, sizeY=1, xExpand=True, yExpand=True, handler=None, name=""):
	"""Creates a text entry widget and adds it to a parent widget."""
	temp = gtk.Entry(maxSize)
	temp.set_width_chars(width)
	temp.set_text(text)
	temp.set_name(name)
	
	if handler != None:
		temp.connect("changed", handler)
	
	parent.attach(temp, gridX, gridX+sizeX, gridY, gridY+sizeY, xoptions=gtk.EXPAND if xExpand else 0, yoptions=gtk.EXPAND if yExpand else 0)
	
	return temp

def createCheckButton(parent, text="", active=False, gridX=0, gridY=0, sizeX=1, sizeY=1, xExpand=True, yExpand=True, handler=None):
	"""Creates a checkbox widget and adds it to a parent widget."""
	temp = gtk.CheckButton(text if text != "" else None)
	temp.set_active(active)
	temp.connect("toggled", handler)
	
	parent.attach(temp, gridX, gridX+sizeX, gridY, gridY+sizeY, xoptions=gtk.EXPAND if xExpand else 0, yoptions=gtk.EXPAND if yExpand else 0)
	
	return temp

def createButton(parent, text="", stock=None, name="", gridX=0, gridY=0, sizeX=1, sizeY=1, xExpand=True, yExpand=True, handler=None):
	"""Creates a button widget and adds it to a parent widget."""
	if stock:
		temp = gtk.Button(text, stock)
	else:
		temp = gtk.Button(text)
	
	temp.set_name(name)
	temp.connect("clicked", handler)
	
	parent.attach(temp, gridX, gridX+sizeX, gridY, gridY+sizeY, xoptions=gtk.EXPAND if xExpand else 0, yoptions=gtk.EXPAND if yExpand else 0)
	
	return temp

def createFontButton(parent, font, gridX=0, gridY=0, sizeX=1, sizeY=1, xExpand=True, yExpand=True, handler=None):
	"""Creates a font button widget and adds it to a parent widget."""
	temp = gtk.FontButton()
	temp.set_font_name(font)
	temp.connect("font-set", handler)
	
	parent.attach(temp, gridX, gridX+sizeX, gridY, gridY+sizeY, xoptions=gtk.EXPAND if xExpand else 0, yoptions=gtk.EXPAND if yExpand else 0)
	
	return temp

def createColorButton(parent, color="#000000", useAlpha=True, name="", gridX=0, gridY=0, sizeX=1, sizeY=1, xExpand=True, yExpand=True, handler=None):
	temp = gtk.ColorButton(gtk.gdk.color_parse(color))
	temp.set_use_alpha(useAlpha)
	temp.set_name(name)
	temp.connect("color-set", handler)
	
	parent.attach(temp, gridX, gridX+sizeX, gridY, gridY+sizeY, xoptions=gtk.EXPAND if xExpand else 0, yoptions=gtk.EXPAND if yExpand else 0)
	
	return temp

def confirmDialog(parent, message):
	"""Creates a confirmation dialog and returns the response."""
	dialog = gtk.MessageDialog(parent, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, message)
	dialog.show()
	response = dialog.run()
	dialog.destroy()
	return response

def errorDialog(parent=None, message="An error has occured!"):
	"""Creates an error dialog."""
	dialog = gtk.MessageDialog(parent, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)
	dialog.show()
	dialog.run()
	dialog.destroy()

def numToHex(n):
	"""Convert integer n in range [0, 15] to hex."""
	try:
		return ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"][n]
	except:
		return -1

def rgbToHex(r, g, b):
	"""Constructs a 6 digit hex representation of color (r, g, b)."""
	r2 = trunc(r / 65535.0 * 255)
	g2 = trunc(g / 65535.0 * 255)
	b2 = trunc(b / 65535.0 * 255)

	return "#%s%s%s%s%s%s" % (numToHex(r2 / 16), numToHex(r2 % 16), numToHex(g2 / 16), numToHex(g2 % 16), numToHex(b2 / 16), numToHex(b2 % 16))

def trunc(n):
	"""Truncate a floating point number, rounding up or down appropriately."""
	c = math.fabs(math.ceil(n) - n)
	f = math.fabs(math.floor(n) - n)

	if c < f:
		return int(math.ceil(n))
	else:
		return int(math.floor(n))

# Direct execution of application
if __name__ == "__main__":
	if len(sys.argv) > 1 and sys.argv[1] == "-version":
		print NAME, VERSION
		exit()
	
	tw = TintWizardGUI()
	tw.main()

