# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
	"name": "Render Tools",
	"category": "Cenda Tools",
	"author": "Cenek Strichel",
	"description": "Render Region & Render without file output",
	"location": "Hotkey (commands)",
	"version": (1, 0, 2),
	"blender": (2, 79, 0),
	"wiki_url": "https://github.com/CenekStrichel/CendaTools/wiki",
	"tracker_url": "https://github.com/CenekStrichel/CendaTools/issues"
}


import bpy

from bpy.app.handlers import persistent
from bpy.props import StringProperty


################################################################
# RENDER REGION #
################################################################
class RenderRegion(bpy.types.Operator):
	
	
	bl_idname = "view3d.render_region"
	bl_label = "Render region"
	
	bpy.types.Scene.ViewportShading = StringProperty( 
	name = "", 
	default = "",
	description = "")
	
	
	def execute(self, context):
		
		
		if( bpy.context.space_data.viewport_shade == 'RENDERED' ):
			bpy.context.space_data.viewport_shade = context.scene.ViewportShading # 'MATERIAL'
			bpy.ops.view3d.clear_render_border()

		else:
			context.scene.ViewportShading = bpy.context.space_data.viewport_shade
			bpy.ops.view3d.render_border('INVOKE_DEFAULT')
			bpy.context.space_data.viewport_shade = 'RENDERED'
			
		'''	
		global shadeSetting

		if(bpy.context.space_data.use_render_border) :
			
			bpy.ops.view3d.clear_render_border()
			bpy.context.space_data.viewport_shade = shadeSetting
			
		else:
			
			bpy.ops.view3d.render_border('INVOKE_DEFAULT')
			shadeSetting = bpy.context.space_data.viewport_shade
			bpy.context.space_data.viewport_shade = 'RENDERED'
		'''
		
		return {'FINISHED'}
	
	
################################################################
# RENDER WITHOUT FILE OUTPUT
################################################################
class RenderWithoutFileOutput(bpy.types.Operator):


	bl_idname = "render.render_without_fileoutput"
	bl_label = "Render without File Output"
	bl_options = {'REGISTER'}
	
	bpy.types.Scene.FileOutput = StringProperty( 
	name = "", 
	default = "",
	description = "")
	
	def execute(self, context):
		
		# switch on nodes and get reference #
		if(bpy.context.scene.use_nodes):

			# disable all output
			for node in bpy.context.scene.node_tree.nodes:
				if( node.type == "OUTPUT_FILE" ):
					if(node.mute == False):	
						context.scene.FileOutput += node.name + ";"	# saved all except disabled
						node.mute = True
				
		# rendering #
		bpy.ops.render.render("INVOKE_DEFAULT", animation=False, write_still=False, use_viewport=False )
		
		return {'FINISHED'}


@persistent
def render_handler(scene):
	
    # enable back output #	
	if(bpy.context.scene.use_nodes):
		
		if(len(bpy.context.scene.FileOutput) > 0):

			fileOutputs = bpy.context.scene.FileOutput.split(";")
			
			for f in fileOutputs:
				for node in bpy.context.scene.node_tree.nodes:
					if( node.type == "OUTPUT_FILE" ):
						if(node.name == f):
							node.mute = False
									
			bpy.context.scene.FileOutput = ""


################################################################
# register #
def register():
	bpy.utils.register_module(__name__)
	bpy.app.handlers.render_post.append(render_handler)
	
def unregister():
	bpy.utils.unregister_module(__name__)
	
if __name__ == "__main__":
	register()