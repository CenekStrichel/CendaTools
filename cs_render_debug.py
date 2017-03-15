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
	"name": "Render Debug",
	"author": "Cenek Strichel",
	"version": (1, 0, 0),
	"blender": (2, 78, 0),
	"location": "Render settings panel",
	"description": "Warnings dialog before render",
	"category": "Cenda Tools"}


import bpy
#from bpy.props import StringProperty, IntProperty, BoolProperty, EnumProperty
from bpy.types import Header, Panel


class RenderDebugPanel(bpy.types.Panel):
	
	"""Render debug information"""
	bl_label = "Render Debug"
	bl_idname = "RENDER_debug_panel"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "render"


	def draw(self, context):
		
		layout = self.layout
		
		# warning tests #
		w_simplify = context.scene.render.use_simplify
		w_resolution = True if bpy.context.scene.render.resolution_percentage != 100 else False
		w_device = True if context.scene.cycles.device == 'GPU' else False

		w_layer = False
		for i in range(0,20):    
			if(bpy.context.scene.layers[i] == False):
				w_layer = True
				break
			

		box = layout.box()
		    
		# warning #
		if( w_simplify or w_resolution or w_device or w_layer ):

			if( w_simplify ):
				row = box.row()
				row.label(" Simplify is Enabled", icon="CANCEL")
		      
			if( w_resolution ):
				row = box.row()
				row.label(" Render resolution is not 100%", icon="CANCEL")
			
			if( w_layer ):
				row = box.row()
				row.label(" All render layers are not visible", icon="CANCEL")
				
			if( w_device ):
				row = box.row()
				row.label(" Render device is GPU", icon="ERROR")
					
		# ok dialog #
		else:
			row = box.row()
			row.label("Everything is OK", icon="INFO")
				
				
				
################################################################
# register #
############
def register():
	bpy.utils.register_module(__name__)

def unregister():
	bpy.utils.unregister_module(__name__)
	
if __name__ == "__main__":
	register()