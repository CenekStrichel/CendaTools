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
	"name": "UV Tools",
	"author": "Cenek Strichel",
	"version": (1, 0, 0),
	"blender": (2, 78, 0),
	"location": "Many commands",
	"description": "Smart switch mode and components for UV Editor",
	"category": "Cenda Tools"}


import bpy
from bpy.props import StringProperty, EnumProperty #, IntProperty, BoolProperty, EnumProperty
#from bpy.types import Header, Panel


# change object mode by selection			
class SmartUVMode(bpy.types.Operator):

	'''Smart UV Mode'''
	bl_idname = "uv.smart_mode"
	bl_label = "Smart UV Mode"
	bl_options = {'REGISTER', 'UNDO'}


	def execute(self, context):

		if(bpy.context.active_object.mode == 'OBJECT'):
			bpy.ops.object.mode_set(mode = 'EDIT')
			
		else:
			if(not bpy.context.tool_settings.use_uv_select_sync):
				bpy.context.tool_settings.use_uv_select_sync = True
			else:
				bpy.context.tool_settings.use_uv_select_sync = False
				bpy.ops.mesh.select_all(action='SELECT')
		
			
		return {'FINISHED'}
	
	
class SmartUVComponentMode(bpy.types.Operator):

	'''Smart UV Component Mode'''
	bl_idname = "uv.smart_component_mode"
	bl_label = "Smart UV Component Mode"
	bl_options = {'REGISTER', 'UNDO'}


	ComponentTypeEnum = [
		("Vertex", "Vertex", "", "", 0),
	    ("Edge", "Edge", "", "", 100),
		("Face", "Face", "", "", 200)
	    ]
	
	component = EnumProperty( name = "Component", description = "", items=ComponentTypeEnum )

	
	def execute(self, context):

		if( bpy.context.tool_settings.use_uv_select_sync ):
			
			if(self.component == 'Vertex'):
				bpy.context.tool_settings.mesh_select_mode = (True, False, False)
				
			elif(self.component == 'Edge'):
				bpy.context.tool_settings.mesh_select_mode = (False, True, False)
				
			elif(self.component == 'Face'):
				bpy.context.tool_settings.mesh_select_mode = (False, False, True)	
				
		else:
			
			if(self.component == 'Vertex'):
				bpy.context.scene.tool_settings.uv_select_mode = 'VERTEX'
				
			elif(self.component == 'Edge'):
				bpy.context.scene.tool_settings.uv_select_mode = 'EDGE'
				
			elif(self.component == 'Face'):
				bpy.context.scene.tool_settings.uv_select_mode = 'FACE'
		
			
		return {'FINISHED'}

				
################################################################
# register #
############
def register():
	bpy.utils.register_module(__name__)
	
def unregister():
	bpy.utils.unregister_module(__name__)
	
if __name__ == "__main__":
	register()