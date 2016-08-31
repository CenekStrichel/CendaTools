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
	"name": "Animation Constraint",
	"author": "Cenek Strichel",
	"version": (1, 0, 0),
	"blender": (2, 77, 0),
	"location": "View 3D Header",
	"description": "For baking helpers (ANIM) constraint",
	"category": "Cenda Tools"}

import bpy
#from bpy.props import StringProperty, IntProperty, BoolProperty
from bpy.props import EnumProperty
from bpy.types import Header #, Panel



class VIEW3D_HT_header_anim_constraint(Header):
	
	bl_space_type = 'VIEW_3D'


	def draw(self, context):
		
		bone = bpy.context.active_pose_bone
		
		animCountOn = 0
		animCountOff = 0
		
		if(bone != None):
			current_icon = ""
			
			# cycle all constraint
			for const in bone.constraints :
				
				if "ANIM" in const.name :
					
					if( const.mute ) :
						current_icon = 'CHECKBOX_DEHLT'
						animCountOn += 1
						
					else :	
						current_icon = 'CHECKBOX_HLT'
						animCountOff += 1
					
					# mixed states	
					if( animCountOn > 0 and animCountOff > 0):
						current_icon = 'QUESTION'
					
					
		layout = self.layout
		row = layout.row(align=True)
		row = layout.row(align=True)
		
		# buttons
		if( bone != None ):
			
			# anim constraint
			if( current_icon != "" ):
				row.operator("view3d.switch_anim_constraint", icon = current_icon).switchStyle = 'Toggle'
				
			# anim bake	
			if( current_icon == 'CHECKBOX_HLT' ):	
				row.operator("view3d.bake_anim_constraint")
				

		'''
		for area in bpy.context.screen.areas:
			if area.type == 'VIEW_3D':
			#	area.header_text_set("ahoj")
				area.tag_redraw()
		'''
				
				
		



class AnimConstraintSwitch(bpy.types.Operator):

	'''Switching for Animation Constraint'''
	bl_idname = "view3d.switch_anim_constraint"
	bl_label = "Anim Constraint"
	
	switchStyleEnum = [
	("Toggle", "Toggle", "", "", 0),
    ("On", "On", "", "", 1),
    ("Off", "Off", "", "", 2),
    ]

	switchStyle = EnumProperty(name="switchStyle", items=switchStyleEnum) 
	
	
	def execute(self, context):

		bone = bpy.context.active_pose_bone
		state = False
		
		
		# first state
		if(self.switchStyle == 'Toggle'):
			for const in bone.constraints :
				if "ANIM" in const.name :
					state = const.mute
				
				
		# cycle all constraint
		for const in bone.constraints :
			if "ANIM" in const.name :
				# Toggle / On / Off
				if(self.switchStyle == 'Toggle'):
					const.mute = not state
					
				elif(self.switchStyle == 'On'):
					const.mute = False
					
				elif(self.switchStyle == 'Off'):
					const.mute = True
				
				
		# redraw constraint state
		for area in bpy.context.screen.areas:
			if area.type == 'PROPERTIES':
				area.tag_redraw()
		
		
		return {'FINISHED'}


class AnimConstraintBake(bpy.types.Operator):

	'''Baking for Animation Constraint'''
	bl_idname = "view3d.bake_anim_constraint"
	bl_label = "Bake Constraint"
	
	def execute(self, context):

		if( bpy.context.scene.is_nla_tweakmode ): # sometimes it is not working well
			
			self.report({'ERROR'},"Can not bake in NLA Tweak mode")
			
		else:
			if(bpy.context.scene.use_preview_range):
				startFrame = bpy.context.scene.frame_preview_start
				endFrame = bpy.context.scene.frame_preview_end
			else:
				startFrame = bpy.context.scene.frame_start
				endFrame = bpy.context.scene.frame_end
			
			# bake by range
			bpy.ops.nla.bake( frame_start = startFrame , frame_end = endFrame, visual_keying=True, use_current_action=True, bake_types={'POSE'} )
			
			# turn off constraint (it is showed only with Anim Constraint)
			bpy.ops.view3d.switch_anim_constraint( switchStyle = 'Off')

		return {'FINISHED'}
	
################################################################
# register #

def register():
	bpy.utils.register_module(__name__)

def unregister():
	bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
	register()