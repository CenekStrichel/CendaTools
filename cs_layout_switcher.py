# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****


bl_info = {
	"name": "Layout Switcher",
	"author": "Cenek Strichel",
	"version": (1, 0, 1),
	"blender": (2, 79, 0),
	"location": "Info header",
	"description": "Switch layout with buttons on Info header",
	"category": "Cenda Tools"}


import bpy
from bpy.props import StringProperty
from bpy.types import Header, Panel

import platform
import ctypes


################
# AUTO IK CHAIN #
################

class SwitchLatout(bpy.types.Operator):

	'''Change layout'''
	bl_idname = "screen.switch_layout"
	bl_label = "Change layout"
	
	layoutName = StringProperty(name="Layout Name")
	
	
	def execute(self, context):

		bpy.context.window.screen = bpy.data.screens[ self.layoutName ]
		return {'FINISHED'}


def switchLayout(self, context):
	
	layout = self.layout
	row = layout.row(align=True)
	
	totalWidth = 0
	
	for area in bpy.context.screen.areas: # iterate through areas in current screen
		totalWidth = totalWidth + area.width
		
	# get resolution
	user32 = ctypes.windll.user32
	screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

	# my home station (1 big monitor)
	if( screensize[0] >= 2560 ):
		row = layout.row(align=True)
		row.operator(SwitchLatout.bl_idname, text = "Generic", icon = "VIEW3D").layoutName = "_1 Generic"
		row.operator(SwitchLatout.bl_idname, text = "Animation", icon = "IPO").layoutName = "_2 Animation"
		row.operator(SwitchLatout.bl_idname, text = "Composition", icon = "NODETREE").layoutName = "_3 Composition"
		
	# another station (3 monitors)
	else:
		row = layout.row(align=True)
		row.operator(SwitchLatout.bl_idname, text = "Generic", icon = "VIEW3D").layoutName = "1 Generic"
		row.operator(SwitchLatout.bl_idname, text = "Animation", icon = "IPO").layoutName = "2 Animation"
		row.operator(SwitchLatout.bl_idname, text = "Composition", icon = "NODETREE").layoutName = "3 Composition"




################################################################
# register 

def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_HT_header.prepend(switchLayout)

	
def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.INFO_HT_header(switchLayout)
	
if __name__ == "__main__":
	register()