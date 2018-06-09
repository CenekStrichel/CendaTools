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
	"name": "Batch Render",
	"author": "Cenek Strichel",
	"version": (1, 0, 0),
	"blender": (2, 7, 9),
	"location": "Render > Create BAT File",
	"description": "Create BAT file for easy rendering",
	"category": "Cenda Tools",
	"wiki_url": "https://github.com/CenekStrichel/CendaTools/wiki",
	"tracker_url": "https://github.com/CenekStrichel/CendaTools/issues"
	}


import bpy
import os
from platform import system as currentOS
from bpy.types import Header, Menu
from bpy.props import StringProperty, BoolProperty


# change object mode by selection			
class BatchRender(bpy.types.Operator):

	'''Batch Render'''
	bl_idname = "screen.batch_render"
	bl_label = "Create BAT file"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		
		if( len(bpy.data.filepath) == 0 ):
			self.report({'ERROR'}, ("Scene must be saved!") )
			return {'FINISHED'}
			
		if( bpy.context.scene.camera == None ):
			self.report({'ERROR'}, ("Set camera in Scene!") )
			return {'FINISHED'}
			
		# render command #
		command = 'start "Render" /b /low /wait '
		command += "\"" + bpy.app.binary_path + "\""
		command += " --background" + " \"" + bpy.data.filepath + "\""
		command += " --render-anim"
		command += " --scene " + "\"" + bpy.context.scene.name + "\""

		# delete bat #
		batFile = bpy.data.filepath.replace(".blend", ".bat")
		command += "\n"
		command += "del \"" + batFile + "\""
		
		# save bat #
		batContent = open( batFile, 'w' )
		batContent.write( command )	
		batContent.close()
		
		# open path to folder #
		filepath = bpy.data.filepath
		relpath = bpy.path.relpath(filepath)
		path = filepath[0: -1 * (relpath.__len__() - 2)]

		bpy.ops.wm.path_open( filepath = path )

		return {'FINISHED'}


def menu_func(self, context):
	self.layout.separator()
	self.layout.operator( "screen.batch_render", icon="LINENUMBERS_ON" )
	
	
################################################################
# register #
############
def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_render.append(menu_func)
		
def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.INFO_MT_render.remove(menu_func)
		
if __name__ == "__main__":
	register()