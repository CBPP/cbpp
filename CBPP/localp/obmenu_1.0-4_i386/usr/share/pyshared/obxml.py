#  obxml.py
#
#  Openbox Menu Editor 1.0 beta
# 
#  Copyright 2005 Manuel Colmenero 
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


# ObMenu can be used as a module in python scripts, for example, to
# Generate dynamic menus (pipemenus)

import xml.dom.minidom

class ObMenu:
	
	# Internal functions =============================================
	# (These mess with the xml tree)
		
	# given its ID, and its parent (or None for top-level)
	# returns the dom tree of the menu. Recursively.
	def _get_dom_menu(self, menu, parent=None):
		if not menu: return None
		if not parent: parent = self.dom.documentElement
		
		for item in parent.childNodes:
			if item.nodeName == "menu" and item.hasChildNodes():
				if item.attributes["id"].nodeValue == menu: return item
				else:
					b = self._get_dom_menu(menu, item)
					if b: return b
		return None

	# given its ID, and its parent (or None for top-level)
	# returns the dom tree of the menu. Recursively.
	def _get_dom_ref(self, menu, parent):
		if not parent: parent = self.dom.documentElement
		for item in parent.childNodes:
			if item.nodeName == "menu":
				if not item.hasChildNodes():
					if item.attributes["id"].nodeValue == menu: return item
				else:
					b = self._get_dom_menu(menu, item)
					if b: return b
		return None
	
	# Get an item of 'menu', given its number (order)
	def _get_dom_item(self,menu,num):
		if not menu:
			item = self.dom.documentElement
		else:
			item = self._get_dom_menu(menu)
			if not item: return None
		i = 0
		for it in item.childNodes:
			if it.nodeType == 1:
				if i == num: return it
				i += 1
	
	# Insert a node in the xml tree
	def _put_dom_item(self, menu, nodo, pos=None):
		parent = self._get_dom_menu(menu)
		if not parent: parent = self.dom.documentElement
		
		if pos == None or pos > self._get_menu_len(menu):
			parent.appendChild(nodo)
		elif pos >= 0:
			ant = self._get_dom_item(menu, pos)
			parent.insertBefore(nodo, ant)
	
	# Get the number of items of a menu
	def _get_menu_len(self,menu):
		if menu:
			item = self._get_dom_menu(menu)
		else:
			item = self.dom.documentElement
		i = 0
		for it in item.childNodes:
			if it.nodeType == 1:
				i += 1
		return i
	
	# Get "real" item number (counting with comments, text, etc in the xml)
	def _get_real_num(self,menu,num):
		if menu:
			item = self._get_dom_menu(menu)
		else:
			item = self.dom.documentElement
		i = 0
		n = 0
		for it in item.childNodes:
			if it.nodeType == 1:
				if i == num: return n
				i += 1
			n += 1
	
	# get the properties of an item from the xml, and returns them as a
	# dictionary.
	def _get_item_props(self,node):
		etiqueta = node.attributes["label"].nodeValue
		accion = ""
		param = ""
		for it in node.childNodes:
			if it.nodeType == 1:
				accion = it.attributes["name"].nodeValue
				if accion.lower() == "execute":
					for itm in it.childNodes:
						if itm.nodeType == 1 and itm.nodeName.lower() == "command":
							for item in itm.childNodes:
								if item.nodeType == 3:
									param = item.nodeValue.strip()
		return { "type": "item", "label": etiqueta, "action": accion, "execute": param }
	
	# get the properties of a menu from the xml, and returns them as a
	# dictionary.
	def _get_menu_props(self, node):
		lb = ""
		ex = ""
		act = ""
		mid = node.attributes["id"].nodeValue
		if node.hasAttribute("label"):
			lb = node.attributes["label"].nodeValue
		else:
			mnu = self._get_dom_menu(mid)
			if mnu: lb = mnu.attributes["label"].nodeValue
			else: lb = mid
		if not node.hasChildNodes():
			if node.hasAttribute("execute"):
				ex = node.attributes["execute"].nodeValue
				act = "Pipemenu"
			else:
				act = "Link"
		if node.hasAttribute("execute"): ex = node.attributes["execute"].nodeValue
		return { "type": "menu", "label": lb, "action": act, "execute": ex, "id": mid }

	# Public functions ===================================================
	# Most of them are self-explanatory
				
	def loadMenu(self, filename):
		fil = open(filename)
		self.dom = xml.dom.minidom.parseString(fil.read())
		fil.close()
	
	def newMenu(self):
		self.dom = xml.dom.minidom.parseString(
		"<?xml version=\"1.0\" ?><openbox_menu></openbox_menu>")
		#self.dom._set_async(False)

	def newPipe(self):
		self.dom = xml.dom.minidom.parseString(
		"<?xml version=\"1.0\" ?><openbox_pipe_menu></openbox_pipe_menu>")
	
	def saveMenu(self, filename):
		output = open(filename, "w")
		for line in self.dom.toprettyxml("\t","\n","utf-8").splitlines():
			if line.strip() != "":
				output.write("%s\n" %(line))
		output.close()
	
	def printXml(self):
		for line in self.dom.toprettyxml("\t","\n","utf-8").splitlines():
			if line.strip() != "":
				print line
	
	def getXml(self):
		res = ""
		for line in self.dom.toprettyxml("\t","\n","utf-8").splitlines():
			if line.strip() != "":
				res = res + "%s\n" % (line)
		return res
				
	def removeItem(self,menu, num):
		if menu:
			dom_mnu = self._get_dom_menu(menu)
		else:
			dom_mnu = self.dom.documentElement
		item = self._get_dom_item(menu,num)
		dom_mnu.removeChild(item)
		item.unlink()
	
	def removeMenu(self,menu):
		dom_mnu = self._get_dom_menu(menu)
		if not dom_mnu.parentNode:
			self.dom.documentElement.removeChild(dom_mnu)
		else:
			dom_mnu.parentNode.removeChild(dom_mnu)
		dom_mnu.unlink()
	
	def createSep(self, menu, pos=None):		
		nodo = self.dom.createElement("separator")
		self._put_dom_item(menu, nodo, pos)
			
	def createItem(self, menu, label, action, execute, pos=None):
		nodo = self.dom.createElement("item")
		nodo.attributes["label"] = label
		accion = self.dom.createElement("action")
		accion.attributes["name"] = "Execute"
		exe = self.dom.createElement("command")
		txt = self.dom.createTextNode("")
		txt.nodeValue = execute
		exe.appendChild(txt)
		accion.appendChild(exe)
		nodo.appendChild(accion)
		self._put_dom_item(menu, nodo, pos)
	
	def createLink(self, menu, mid, pos=None):
		nodo = self.dom.createElement("menu")
		nodo.attributes["id"] = mid
		self._put_dom_item(menu, nodo, pos)

	def createPipe(self, menu, mid, label, execute, pos=None):
		nodo = self.dom.createElement("menu")
		nodo.attributes["id"] = mid
		nodo.attributes["label"] = label
		nodo.attributes["execute"] = execute
		
		self._put_dom_item(menu, nodo, pos)
		
	def createMenu(self, menu, label, mid, pos=None):
		nodo = self.dom.createElement("menu")
		nodo.attributes["label"] = label
		nodo.attributes["id"] = mid
		txt = self.dom.createTextNode("")
		txt.nodeValue = "\n"
		nodo.appendChild(txt)
		self._put_dom_item(menu, nodo, pos)
		
	def interchange(self, menu, n1, n2):
		if not menu:
			dom_mnu = self.dom.documentElement
		else:
			dom_mnu = self._get_dom_menu(menu)
		i1 = self._get_real_num(menu, n1)
		i2 = self._get_real_num(menu, n2)
		uno = dom_mnu.childNodes[i1]
		dom_mnu.childNodes[i1] = dom_mnu.childNodes[i2]
		dom_mnu.childNodes[i2] = uno
	
	def setItemProps(self, menu, n, label, action, exe):
		itm = self._get_dom_item(menu,n)
		itm.attributes["label"].nodeValue = label
		for it in itm.childNodes:
			if it.nodeType == 1:
				it.attributes["name"].nodeValue = action
				if action == "Execute":
					if not it.childNodes:
						elm = xml.dom.minidom.Element("command")
						txt = xml.dom.minidom.Text()
						txt.nodeValue = exe
						elm.appendChild(txt)
						it.appendChild(elm)
					else:
						for i in it.childNodes:
							if i.nodeType == 1 and i.nodeName == "command":
								for item in i.childNodes:
									if item.nodeType == 3:
										item.nodeValue = exe
				else:
					for item in it.childNodes:
						it.removeChild(item)
	
	def setMenuLabel(self, menu, label):
		mnu = self._get_dom_menu(menu)
		if mnu: mnu.attributes["label"].nodeValue = label
	
	def getMenuLabel(self,menu):
		mnu = self._get_dom_menu(menu)
		if mnu: return mnu.attributes["label"].nodeValue

	def setRefLabel(self, parent, mid, label):
		prnt = self._get_dom_menu(parent)
		if prnt: mnu = self._get_dom_ref(mid, prnt)
		if mnu: mnu.setAttribute("label", label)

	def setRefId(self, parent, mid, new_id):
		prnt = self._get_dom_menu(parent)
		if prnt: mnu = self._get_dom_ref(mid, prnt)
		if mnu: mnu.setAttribute("id", new_id)
	
	def setMenuExecute(self, parent, mid, execute):
		prnt = self._get_dom_menu(parent)
		if prnt: mnu = self._get_dom_ref(mid, prnt)
		if mnu: mnu.setAttribute("execute", execute)
	
	# Return just an item, given its parent menu an its number
	def getItem(self,menu,num):
		mnu = self._get_dom_menu(menu)
		if not mnu: return
		n = 0
		for i in mnu.childNodes:
			if i.nodeType == 1:
				if n == num:
					if i.nodeName == "menu":
						return self._get_menu_props(i)
					elif i.nodeName == "separator":
						return { "type": "separator" }
					elif i.nodeName == "item":
						return self.get_item_props(i)
				n += 1
	
	# Is menu? Returns True if it's an existing ID
	def isMenu(self,menu):
		dom = self._get_dom_menu(menu)
		if dom:
			return True
		else:
			return False
		
	
	# Returns a whole menu, as a list of dictionaries.
	# Each dictionary has the items properties.
	def getMenu(self,menu):
		lst = []
		if menu:
			mnu = self._get_dom_menu(menu)
			if not mnu: return
		else:
			mnu = self.dom.documentElement
		for i in mnu.childNodes:
			if i.nodeType == 1:
				if i.nodeName == "menu":
					d = self._get_menu_props(i)
					d["parent"] = menu
					lst.append(d)
				elif i.nodeName == "separator":
					lst.append({"type": "separator", "parent": menu})
				elif i.nodeName == "item":
					d = self._get_item_props(i)
					d["parent"] = menu		
					lst.append(d)
		return lst

	# replace all old_id's in file with new_id's
	# parent shuld start with None	
	def replaceId(self, old_id, new_id, parent=None):
		if not parent: parent = self.dom.documentElement
		for item in parent.childNodes:
			if item.nodeName == "menu":
				if item.attributes["id"].nodeValue == old_id:
					item.setAttribute("id", new_id)
				elif item.hasChildNodes():
					self.replaceId(old_id, new_id, item)

if __name__ == "__main__":
	print "This is a module. Use obmenu instead."
	exit(0)
