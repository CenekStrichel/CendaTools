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
	"name": "Change Frame",
	"author": "Cenek Strichel",
	"version": (1, 0, 0),
	"blender": (2, 77, 0),
	"location": "view3d.change_frame_drag",
	"description": "Change frame by dragging",
	"category": "Cenda Tools"}


import bpy
from bpy.props import IntProperty, FloatProperty, BoolProperty


class ChangeFrame(bpy.types.Operator):
	
	
	"""Change frame with dragging"""
	bl_idname = "view3d.change_frame_drag"
	bl_label = "Change Frame Drag"
	
	defaultSensitivity = FloatProperty( name = "Sensitivity", default = 5 )
	autoSensitivity = BoolProperty( name = "Auto Sensitivity" )

	
	global frameOffset
	global mouseOffset
	global sensitivity
#	global previousOnlyRender
	global previousManipulator
	
	
	def modal(self, context, event):
	
		# change frame
		if event.type == 'MOUSEMOVE':
			
			delta = self.mouseOffset - event.mouse_x
			bpy.context.scene.frame_current = (-delta * self.sensitivity) + self.frameOffset

		# end of modal
		elif event.type == 'RIGHTMOUSE' and event.value == 'RELEASE':
			
			# previous viewport setting
		#	bpy.context.space_data.show_only_render = self.previousOnlyRender
			bpy.context.space_data.show_manipulator = self.previousManipulator
			
			# cursor back
			bpy.context.window.cursor_set("DEFAULT")
			
			return {'FINISHED'}
			
		return {'RUNNING_MODAL'}


	def invoke(self, context, event):
		
		# hide viewport helpers
#		self.previousOnlyRender = bpy.context.space_data.show_only_render
		self.previousManipulator = bpy.context.space_data.show_manipulator
#		bpy.context.space_data.show_only_render = True
		bpy.context.space_data.show_manipulator = False
		
		# start modal
		self.frameOffset = bpy.context.scene.frame_current 
		self.mouseOffset = event.mouse_x
		
		# cursor
		bpy.context.window.cursor_set("SCROLL_X")
		
		context.window_manager.modal_handler_add(self)
		
		found = False
		
		# auto sensitivity
		if(self.autoSensitivity):
			if context.area.type == 'VIEW_3D':
				
				ratio = 1024 / context.area.width
				self.sensitivity = (ratio / 10)
				
				# finding end of frame range
				if(bpy.context.scene.use_preview_range):
					endFrame = bpy.context.scene.frame_preview_end
				else:
					endFrame = bpy.context.scene.frame_end

				self.sensitivity *= (endFrame/ 100)

				found = True

		# default
		if(not found):
			self.sensitivity = self.defaultSensitivity / 100
			
		return {'RUNNING_MODAL'}


###########################################################
def register():
	bpy.utils.register_module(__name__)

def unregister():
	bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
	register()