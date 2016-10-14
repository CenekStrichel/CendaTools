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
	"version": (1, 0, 1),
	"blender": (2, 78, 0),
	"location": "Tools > Offset Animation",
	"description": "Offset for animated object and bones",
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
#	bl_context = "posemode"
	

	bpy.types.Scene.showSetOffset = BoolProperty(name="ShowSetOffset",default=False) # is reference setted?
	bpy.types.Scene.autokeySetting = BoolProperty(name="AutoKey",default=True) # previous setting for autokey
	
	
	
	def draw(self, context):
		
		layout = self.layout
		
		# First button
		row = layout.row(align=True)
	#	row.scale_y = 2
		row.operator("anim.offset_animation_set", icon = "OUTLINER_DATA_ARMATURE" ,text="Reference").reference = True
		
		# Second button
		row = layout.row(align=True)
	#	row.scale_y = 2
		row.operator("anim.offset_animation_set", icon = "POSE_DATA", text="Offset").reference = False
		
		if( context.scene.showSetOffset ):
		#	ahoj.active = True
			row.enabled = True
		else:	
		#	ahoj.active = False
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
		
		bpy.types.Scene.QRotStart = FloatVectorProperty( name = "QRotStart", description = "", size = 4 )
		bpy.types.Scene.QRotEnd = FloatVectorProperty( name = "QRotEnd", description = "", size = 4 )
		bpy.types.Scene.QRotDifference = FloatVectorProperty( name = "QRotDifference", description = "", size = 4 )
		
		bpy.types.Scene.SclStart = FloatVectorProperty( name = "SclStart", description = "")
		bpy.types.Scene.SclEnd = FloatVectorProperty( name = "SclEnd", description = "")
		bpy.types.Scene.SclDifference = FloatVectorProperty( name = "SclDifference", description = "")
		

		# you need bone with action
		if(context.object.animation_data.action == None):
			self.report({'ERROR'},"No Action for Offset Found")
			return {'FINISHED'}

		# if bone is not selected, object is offseted
		selected = bpy.context.active_pose_bone
		if( selected == None ):
			selected = bpy.context.active_object
			
		# cycling all selected bones
#		for selectedBone in bpy.context.selected_pose_bones:

		currentLocation = selected.location
		currentRotation = Vector (( selected.rotation_euler[0], selected.rotation_euler[1], selected.rotation_euler[2] ))
		currentQRotation = Vector (( selected.rotation_quaternion[0], selected.rotation_quaternion[1], selected.rotation_quaternion[2], selected.rotation_quaternion[3] ))
		currentScale = Vector (( selected.scale[0], selected.scale[1], selected.scale[2] ))

		SaveRemoveOffset( self, context, currentLocation, currentRotation, currentScale, selected, currentQRotation )

		#	break # only first bone
			
		return {'FINISHED'}


def SaveRemoveOffset( self, context, currentLocation, currentRotation, currentScale, object, currentQRotation ):
	
	scn = context.scene
	
	# first reference
	if( self.reference ):
		
		scn.LocStart = currentLocation
		scn.RotStart = currentRotation
		scn.QRotStart = currentQRotation
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
		
		scn.QRotEnd = currentQRotation
		scn.QRotDifference = ( Vector(scn.QRotStart) - Vector(scn.QRotEnd) )
		
		# scale
		scn.SclEnd = currentScale
		scn.SclDifference = ( Vector(scn.SclStart) - Vector(scn.SclEnd) )
		
		# do offset
		OffsetAnimation( object )
		
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
		
		del scn["QRotStart"]
		del scn["QRotEnd"]
		del scn["QRotDifference"]
		
		del scn["SclStart"]
		del scn["SclEnd"]
		del scn["SclDifference"]
				
				
# autokey is turned off, so I have to redraw autokey button
def RedrawTimeline():
	
	# redraw autokey state
	for area in bpy.context.screen.areas:
		if area.type == 'TIMELINE':
			area.tag_redraw()
						
						
## ONLY FOR SET OFFSET ##############################################################
def OffsetAnimation( selected ):
	 
	
	scn = bpy.context.scene
	obj = bpy.context.object
	
	# get current action
	action = obj.animation_data.action
	
	locIndex = 0
	rotIndex = 0
	rotQIndex = 0
	sclIndex = 0
	
	
	# Current action
	if ( (obj.animation_data is not None) and (obj.animation_data.action is not None) ):
		
		# num of channels
		numCurves = len( action.fcurves )


		for i in range(numCurves):
			
			fcurveDataPath = action.fcurves[ i ].data_path

			###################################################	
			# BONE #
			###################################################
			if(bpy.context.active_pose_bone != None):
						
				# find bone by name
				if ( selected.name in fcurveDataPath ):
					
					
					# LOCATION # - TODO - Rewrite duplicity code
					if ( ".location" in fcurveDataPath ):
						
						numKeyframes = len( action.fcurves[ i ].keyframe_points )
						offset = scn.LocDifference[ locIndex ]
						locIndex += 1
						
						CurveOffset(action, i, offset, numKeyframes)
					
					
					# ROTATION #
					elif ( ".rotation_euler" in fcurveDataPath ):

						numKeyframes = len( action.fcurves[ i ].keyframe_points )
						offset = scn.RotDifference[ rotIndex ]
						rotIndex += 1

						CurveOffset(action, i, offset, numKeyframes)


					# Q ROTATION #
					elif ( ".rotation_quaternion" in fcurveDataPath ):

						numKeyframes = len( action.fcurves[ i ].keyframe_points )
						offset = scn.QRotDifference[ rotQIndex ]
						rotQIndex += 1

						CurveOffset(action, i, offset, numKeyframes)
							
							
					# SCALE #
					elif ( ".scale" in fcurveDataPath ):
							
						numKeyframes = len( action.fcurves[ i ].keyframe_points )
						offset = scn.SclDifference[ sclIndex ]
						sclIndex += 1

						CurveOffset(action, i, offset, numKeyframes)


	
			###################################################		
			# OBJECT #
			###################################################
			else:
				# LOCATION #
				if ( "location" in fcurveDataPath ):
					
					numKeyframes = len( action.fcurves[ i ].keyframe_points )
					offset = scn.LocDifference[ locIndex ]
					locIndex += 1
					
					CurveOffset(action, i, offset, numKeyframes)
				
				
				# ROTATION #
				elif ( "rotation_euler" in fcurveDataPath ):

					numKeyframes = len( action.fcurves[ i ].keyframe_points )
					offset = scn.RotDifference[ rotIndex ]
					rotIndex += 1

					CurveOffset(action, i, offset, numKeyframes)
						
						
				# Q ROTATION #
				elif ( "rotation_quaternion" in fcurveDataPath ):

					numKeyframes = len( action.fcurves[ i ].keyframe_points )
					offset = scn.QRotDifference[ rotQIndex ]
					rotQIndex += 1

					CurveOffset(action, i, offset, numKeyframes)


				# SCALE #
				elif ( "scale" in fcurveDataPath ):
						
					numKeyframes = len( action.fcurves[ i ].keyframe_points )
					offset = scn.SclDifference[ sclIndex ]
					sclIndex += 1

					CurveOffset(action, i, offset, numKeyframes)	


def CurveOffset(action, index, offset, numKeyframes):
	
	for j in range(numKeyframes):
		action.fcurves[ index ].keyframe_points[ j ].co.y -= offset
		action.fcurves[ index ].keyframe_points[ j ].handle_left.y -= offset
		action.fcurves[ index ].keyframe_points[ j ].handle_right.y -= offset				
			
			
			
################################################################
# register #
	
def register():
	bpy.utils.register_module(__name__)

def unregister():
	bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
	register()