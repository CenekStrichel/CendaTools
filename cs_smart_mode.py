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
	"name": "Smart Mode Switcher",
	"author": "Cenek Strichel",
	"version": (1, 0, 0),
	"blender": (2, 78, 0),
	"location": "object.smart_mode command",
	"description": "Smart switch between Object / Edit mode with change Properties",
	"category": "Cenda Tools"}


import bpy
from bpy.props import StringProperty #, IntProperty, BoolProperty, EnumProperty
#from bpy.types import Header, Panel

		
class SmartModeVariables(bpy.types.PropertyGroup):
	
	bpy.types.Scene.PreviousPanel = bpy.props.StringProperty( name = "Previous Panel", default = "" )


# change object mode by selection			
class SmartObjectMode(bpy.types.Operator):

	'''Smart Object Mode'''
	bl_idname = "object.smart_mode"
	bl_label = "Smart Object Mode"
	bl_options = {'REGISTER', 'UNDO'}


	def execute(self, context):
		
		obj = context.active_object
		print("Smart Mode Type: " + obj.type)
		
		#
		if(obj.type == "ARMATURE"):
			bpy.ops.object.posemode_toggle()
			SetPropertiesPanel( 'DATA' )
		
		#	
		elif(obj.type == "MESH"):
			bpy.ops.object.editmode_toggle()
		
		#	
		elif(obj.type == "LATTICE" or obj.type == "CURVE"):
			bpy.ops.object.editmode_toggle()
			SetPropertiesPanel( 'DATA' )
			
		#	
		elif(obj.type == "CAMERA" or obj.type == "EMPTY" or obj.type == "LAMP"):
			SetPropertiesPanel( 'DATA', onlyObjectMode = True )
			
		#
		else:
			bpy.ops.object.editmode_toggle()
			
		return {'FINISHED'}
	
	
def SetPropertiesPanel( panelName, onlyObjectMode = False ):
	
	# new is object mode
	if(bpy.context.active_object.mode == "OBJECT" and not onlyObjectMode):

		for area in bpy.context.screen.areas: # iterate through areas in current screen
			if area.type == 'PROPERTIES':
				for space in area.spaces: # iterate through all founded panels
					if space.type == 'PROPERTIES':
						
						if( len(bpy.context.scene.PreviousPanel) > 0 ):
							space.context = bpy.context.scene.PreviousPanel
		
	
	# new is some edit mode
	else:
		
		for area in bpy.context.screen.areas: # iterate through areas in current screen
			if area.type == 'PROPERTIES':
				for space in area.spaces: # iterate through all founded panels
					if space.type == 'PROPERTIES':
						
						if(not onlyObjectMode):
							if(space.context != panelName):
								bpy.context.scene.PreviousPanel = space.context
								
						space.context = panelName
			
			
	
# wm.context_toggle	
# bpy.context.tool_settings.use_uv_select_sync	

				
################################################################
# register #
############
def register():
	bpy.utils.register_module(__name__)
	
def unregister():
	bpy.utils.unregister_module(__name__)
	
if __name__ == "__main__":
	register()