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
	"name": "Offset Animation",
	"author": "Cenek Strichel",
	"version": (1, 0, 0),
	"blender": (2, 77, 0),
	"location": "Tools > Offset Animation (Pose Mode)",
	"description": "Offset for animated object",
	"category": "Cenda Tools"}
	

import bpy
from bpy.props import BoolProperty, FloatVectorProperty, FloatProperty
from mathutils import *
from math import *


## PANEL ##############################################################
class OffsetAnimationPanel(bpy.types.Panel):
	
	
	bl_label = "Offset Animation"
	bl_idname = "OFFSET_ANIMATION_PANEL"
	
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "Tools"
	bl_context = "posemode"
	

	bpy.types.Scene.showSetOffset = BoolProperty(name="ShowSetOffset",default=False) # is reference setted?
	bpy.types.Scene.autokeySetting = BoolProperty(name="AutoKey",default=True) # previous setting for autokey
	
	
	
	def draw(self, context):
		
		layout = self.layout
		
		# First button
		row = layout.row(align=True)
		row.scale_y = 2
		row.operator("anim.offset_animation_set", icon = "OUTLINER_DATA_ARMATURE" ,text="Set Reference").reference = True
		
		# Second button
		row = layout.row(align=True)
		row.scale_y = 2
		row.operator("anim.offset_animation_set", icon = "POSE_DATA", text="Set Offset").reference = False
		
		if( context.scene.showSetOffset ):
			row.enabled = True
		else:	
			row.enabled = False	
		
		
################################################################
class OffsetAnimationSet(bpy.types.Operator):


	bl_idname = "anim.offset_animation_set"
	bl_label = "Offset Animation Set"

	reference = BoolProperty(name="Reference",default=True) #  setting reference
	
	
	def execute(self, context):

		# saving
		bpy.types.Scene.LocStart = FloatVectorProperty( name = "LocStart", description = "")
		bpy.types.Scene.LocEnd = FloatVectorProperty( name = "LocEnd", description = "")
		bpy.types.Scene.LocDifference = FloatVectorProperty( name = "LocDifference", description = "")

		bpy.types.Scene.RotStart = FloatVectorProperty( name = "RotStart", description = "")
		bpy.types.Scene.RotEnd = FloatVectorProperty( name = "RotEnd", description = "")
		bpy.types.Scene.RotDifference = FloatVectorProperty( name = "RotDifference", description = "")
		
		bpy.types.Scene.SclStart = FloatVectorProperty( name = "SclStart", description = "")
		bpy.types.Scene.SclEnd = FloatVectorProperty( name = "SclEnd", description = "")
		bpy.types.Scene.SclDifference = FloatVectorProperty( name = "SclDifference", description = "")
		

		# you need bone with action
		if(bpy.context.object.animation_data.action == None):
			self.report({'ERROR'},"No Action for Offset Found")
			return {'FINISHED'}
		
		
		scn = context.scene
		
		# cycling all selected bones
		for selectedBone in bpy.context.selected_pose_bones:

			currentLocation = selectedBone.location
			currentRotation = Vector (( selectedBone.rotation_euler[0], selectedBone.rotation_euler[1], selectedBone.rotation_euler[2] ))
			currentScale= Vector (( selectedBone.scale[0], selectedBone.scale[1], selectedBone.scale[2] ))

					
			# first reference
			if( self.reference ):
				
				scn.LocStart = currentLocation
				scn.RotStart = currentRotation
				scn.SclStart = currentScale
				
				# autokey setting
				bpy.types.Scene.autokeySetting = scn.tool_settings.use_keyframe_insert_auto
				scn.tool_settings.use_keyframe_insert_auto = False
				RedrawTimeline()

				bpy.types.Scene.showSetOffset = True


			# second for offset
			else:
				
				self.reference = False
				
				# location
				scn.LocEnd = currentLocation
				scn.LocDifference = ( Vector(scn.LocStart) - Vector(scn.LocEnd) )
				
				# rotation
				scn.RotEnd = currentRotation
				scn.RotDifference = ( Vector(scn.RotStart) - Vector(scn.RotEnd) )
				
				# scale
				scn.SclEnd = currentScale
				scn.SclDifference = ( Vector(scn.SclStart) - Vector(scn.SclEnd) )
				
				# do offset
				OffsetAnimation( selectedBone )
				
				# autokey setting
				scn.tool_settings.use_keyframe_insert_auto = bpy.types.Scene.autokeySetting
				RedrawTimeline()
						
				# for button
				bpy.types.Scene.showSetOffset = False
				
				# delete after load
				del scn["LocStart"]
				del scn["LocEnd"]
				del scn["LocDifference"]
			
				del scn["RotStart"]
				del scn["RotEnd"]
				del scn["RotDifference"]
				
				del scn["SclStart"]
				del scn["SclEnd"]
				del scn["SclDifference"]
				
			break # only first bone
			
		return {'FINISHED'}
	

# autokey is turned off, so I have to redraw autokey button
def RedrawTimeline():
	
	# redraw autokey state
	for area in bpy.context.screen.areas:
		if area.type == 'TIMELINE':
			area.tag_redraw()
						
						
## ONLY FOR SET OFFSET ##############################################################
def OffsetAnimation( selectedBone ):
	 
	scn = bpy.context.scene
	obj = bpy.context.object
	
	# get current action
	action = obj.animation_data.action
	
	locIndex = 0
	rotIndex = 0
	sclIndex = 0
	
	# Current action
	if ( (obj.animation_data is not None) and (obj.animation_data.action is not None) ):
		
		# num of channels
		numCurves = len( action.fcurves )

		for i in range(numCurves):
			
			fcurveDataPath = action.fcurves[ i ].data_path
			
			# find bone by name
			if( selectedBone.name in fcurveDataPath ):
			
				# LOCATION #
				if ( ".location" in fcurveDataPath ):
					
					numKeyframes = len( action.fcurves[ i ].keyframe_points )
					offset = scn.LocDifference[ locIndex ]
					locIndex += 1
					
					for j in range(numKeyframes):
						
						action.fcurves[ i ].keyframe_points[ j ].co.y -= offset
						action.fcurves[ i ].keyframe_points[ j ].handle_left.y -= offset
						action.fcurves[ i ].keyframe_points[ j ].handle_right.y -= offset
				
				
				# ROTATION #
				elif ( ".rotation_euler" in fcurveDataPath ):

					numKeyframes = len( action.fcurves[ i ].keyframe_points )
					offset = scn.RotDifference[ rotIndex ]
					rotIndex += 1

					for j in range(numKeyframes):
						
						action.fcurves[ i ].keyframe_points[ j ].co.y -= offset
						action.fcurves[ i ].keyframe_points[ j ].handle_left.y -= offset
						action.fcurves[ i ].keyframe_points[ j ].handle_right.y -= offset

	
				# SCALE #
				elif ( ".scale" in fcurveDataPath ):
						
					numKeyframes = len( action.fcurves[ i ].keyframe_points )
					offset = scn.SclDifference[ sclIndex ]
					sclIndex += 1

					for j in range(numKeyframes):
						
						action.fcurves[ i ].keyframe_points[ j ].co.y -= offset
						action.fcurves[ i ].keyframe_points[ j ].handle_left.y -= offset
						action.fcurves[ i ].keyframe_points[ j ].handle_right.y -= offset		

	
################################################################
# register #
	
def register():
	bpy.utils.register_module(__name__)

def unregister():
	bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
	register()