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
	"name": "Render Region",
	"category": "Cenda Tools",
	"author": "Cenek Strichel",
	"description": "Rendering in viewport",
	"location": "Hotkey"
}


import bpy


class RenderRegion(bpy.types.Operator):
	
	bl_idname = "view3d.render_region"
	bl_label = "Render region"
	
	def execute(self, context):
		
		
		if( bpy.context.space_data.viewport_shade == 'RENDERED' ):
			bpy.context.space_data.viewport_shade = 'MATERIAL'
		else:
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
# register #
def register():
	bpy.utils.register_module(__name__)
	
def unregister():
	bpy.utils.unregister_module(__name__)
	
if __name__ == "__main__":
	register()