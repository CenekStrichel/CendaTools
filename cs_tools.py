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
	"name": "Tools",
	"author": "Cenek Strichel",
	"version": (1, 0, 0),
	"blender": (2, 77, 0),
	"location": "Many commands",
	"description": "Many tools",
	"category": "Cenda Tools"}

import bpy
from bpy.props import StringProperty, IntProperty, BoolProperty, EnumProperty
from bpy.types import Header, Panel

'''
class VIEW3D_PT_options_bone(bpy.types.Panel):
	
	bl_label = "Bone Settings"
	bl_idname = "BONE_SETTINGS_PANEL"
	
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "Options"
	
	bl_context = "armature_edit"


	def draw(self, context):
		bone = context.selected_bones
		
	#	if not bone:
	#		bone = context.edit_bone
			
		self.layout.prop(bone, "use_deform", text="")
'''

class VIEW3D_PT_view3d_display_view_side(Panel):
	
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = "View Side"
	
	def draw(self, context):
		
		layout = self.layout
		
		row = layout.row(align = True)
		row.operator("view3d.viewnumpad", text="Top").type='TOP'
		
		box = layout.box()
		row = box.row(align = True)
		row.operator("view3d.viewnumpad", text="Front" ).type='FRONT'
		
		row = box.row(align = True)
		row.operator("view3d.viewnumpad", text="Left" ).type='LEFT'
		row.operator("view3d.viewnumpad", text="Right" ).type='RIGHT'
		
		row = box.row(align = True)
		row.operator("view3d.viewnumpad", text="Back" ).type='BACK'
	
	
############################ GUI ####################################
class TIMELINE_HT_header_camShot(Header):
	
	bl_space_type = 'TIMELINE'


	def draw(self, context):

		layout = self.layout

		row = layout.row(align=True)
		row = layout.row(align=True)
		row.operator( "scene.change_cam_shot" , icon = "FRAME_PREV", text = "Previous Shot").forward = False
		row.operator( "scene.change_cam_shot" , icon = "FRAME_NEXT", text = "Next Shot").forward = True
			
		
				
class ChangeCamShot(bpy.types.Operator):


	bl_label = "Change Cam Shot"
	bl_idname = "scene.change_cam_shot"
	
	
	forward = BoolProperty(name="Forward",default=True)
	
	
	def execute(self, context):
		
		# I am using only preview
		bpy.context.scene.use_preview_range = True

		# start frame for detection
		bpy.context.scene.frame_current = ( bpy.context.scene.frame_preview_start + bpy.context.scene.frame_preview_end ) / 2
			
		last = False	
		
		# FORWARD #
		if(self.forward):

			# is it last?
			markerStatus = bpy.ops.screen.marker_jump(next = True)
			if(markerStatus == {'CANCELLED'} ):	
				self.report({'INFO'},"Last Shot Reached")
				last = True
				
			else:		
				bpy.context.scene.frame_preview_start = bpy.context.scene.frame_current
			
				# start range
				markerStatus = bpy.ops.screen.marker_jump(next = True)
				if(markerStatus == {'CANCELLED'} ):
					bpy.context.scene.frame_preview_end += 200
				else:	
					bpy.context.scene.frame_preview_end = bpy.context.scene.frame_current
					
	
		# BACKWARD #
		else:
			
			# is it last?
			markerStatus = bpy.ops.screen.marker_jump(next = False)
			if(markerStatus == {'CANCELLED'} ):	
				self.report({'INFO'},"First Shot Reached") # TODO: not working well

			else:		
				bpy.context.scene.frame_preview_end = bpy.context.scene.frame_current
			
				# start range
				markerStatus = bpy.ops.screen.marker_jump(next = False)
				if(markerStatus == {'CANCELLED'} ):
					bpy.context.scene.frame_preview_start = 0
				else:	
					bpy.context.scene.frame_preview_start = bpy.context.scene.frame_current
	
	
		# change after setting shot
		bpy.context.scene.frame_current	= bpy.context.scene.frame_preview_start
		if(not last):
			bpy.context.scene.frame_preview_end -= 1 # I dont want show next marker shot
		
		# frame timeline
		for area in bpy.context.screen.areas:
			FrameForEditor( area, 'TIMELINE')

		return{'FINISHED'}
			
			
################################################################
# play animation and stop with restore time position
class AnimationPlayRestore(bpy.types.Operator):

	bl_idname = "screen.animation_play_restore"
	bl_label = "Play Animation Restore"
	
	onlyRender = BoolProperty(name="Only Render",default=False)
	
	def execute(self, context):
		
		# HACK - blender is switching this to false, but dont know why
		bpy.context.scene.show_keys_from_selected_only = True

		# playing
		isplaying = bpy.context.screen.is_animation_playing
		
		# stop / play					
		if( isplaying ):
			bpy.ops.screen.animation_cancel(restore_frame=True)
		else:
			bpy.ops.screen.animation_play()	
			
		# change only current
		'''	
		space = bpy.context.space_data
		
		if space.type == 'VIEW_3D': # check if space is a 3D view
			# Previs Play
			if self.onlyRender :
				space.show_only_render = not isplaying
				space.show_manipulator = isplaying
				space.fx_settings.use_ssao = not isplaying
			# Normal Play
			else :
				space.show_only_render = False
				space.show_manipulator = isplaying
				space.fx_settings.use_ssao = False
	
		
		else:
		'''
		# areas #
		for area in bpy.context.screen.areas: # iterate through areas in current screen
			if area.type == 'VIEW_3D':
				for space in area.spaces: # iterate through spaces in current VIEW_3D area
					if space.type == 'VIEW_3D': # check if space is a 3D view
						
						if(space.region_3d.view_perspective == 'CAMERA'):
							break # I dont want to change view with camera
						
						# Previs Play
						if self.onlyRender :
							space.show_only_render = not isplaying
							space.show_manipulator = isplaying
							space.fx_settings.use_ssao = not isplaying
							
						# Normal Play
						else :
							space.show_only_render = False
							space.show_manipulator = isplaying
							space.fx_settings.use_ssao = False

		return {'FINISHED'}
		
	
############		
# CHANNELS #
############		
class SelectAndFrame(bpy.types.Operator):
	
	bl_idname = "graph.channels_select_and_frame"
	bl_label = "Select and Frame"
	
	extend = BoolProperty(name="Extend", default=False)

#	@classmethod
#	def poll(cls, context):
#		return context.area.type == 'GRAPH_EDITOR'

	def execute(self, context):
		
		# Graph Editor
		if( context.area.type == 'GRAPH_EDITOR' ):
			
			bpy.ops.anim.channels_click('INVOKE_DEFAULT', extend = self.extend)
			bpy.ops.anim.channel_select_keys('INVOKE_DEFAULT', extend = self.extend)
		
			bpy.ops.graph.view_selected('EXEC_REGION_WIN')

			'''
			bpy.ops.screen.region_flip('EXEC_REGION_CHANNELS')		
			bpy.ops.view2d.zoom_out('EXEC_REGION_WIN', zoomfacx = -0.05, zoomfacy = -0.05)
			bpy.ops.screen.region_flip('EXEC_REGION_CHANNELS')
			'''
	#		
	#		bpy.ops.graph.select_all_toggle()
			bpy.ops.anim.channels_expand(all=False)
			
			
			
		# Dope & NLA
		else:

			bpy.ops.anim.channels_click('INVOKE_DEFAULT', extend = self.extend)
			bpy.ops.anim.channels_expand(all=False)
				
		return {'FINISHED'}

		
class ResetExpand(bpy.types.Operator):
	
	bl_idname = "anim.reset_expand"
	bl_label = "Reset Expand"

	def execute(self, context):
		
			
		if( context.area.type == 'GRAPH_EDITOR' ):
			
			bpy.ops.anim.channels_collapse(all=True)
			bpy.ops.anim.channels_expand(all=True)
			bpy.ops.anim.channels_expand(all=True)

		else:

			space_data = bpy.context.space_data
			
			if space_data.type == 'DOPESHEET_EDITOR': # check if space is a 3D view
			
				bpy.ops.anim.channels_collapse(all=True)
				
				# Action editor is not using this
				if (bpy.context.space_data.mode == 'DOPESHEET') :
					bpy.ops.anim.channels_expand(all=True)
					bpy.ops.anim.channels_expand(all=True)
					
				# if summary is on, you need one expand more
				if space_data.dopesheet.show_summary :
					bpy.ops.anim.channels_expand(all=True)
				
		return {'FINISHED'}
	
	
################		
# GRAPH EDITOR #
################
# Double G	
class FrameCurve(bpy.types.Operator):
	
	bl_idname = "graph.frame_curve"
	bl_label = "Frame Curve"

	@classmethod
	def poll(cls, context):
		return context.area.type == 'GRAPH_EDITOR'

	def execute(self, context):
		bpy.ops.graph.select_linked()
		bpy.ops.graph.view_selected()
	#	bpy.ops.view2d.zoom_out(zoomfacx=-0.5, zoomfacy=-0.5)
		
		return {'FINISHED'}	


# MATERIAL / SOLID / TEXTURE
class DisplaySwitcher(bpy.types.Operator):
	
	bl_idname = "view3d.display_switcher"
	bl_label = "Display Switcher"

	forward = BoolProperty(name="Forward Cycling",default=False)
	
	def execute(self, context):
		
		if(self.forward) :

			if bpy.context.space_data.viewport_shade == 'WIREFRAME' :
				bpy.context.space_data.viewport_shade = 'SOLID'
				
			elif bpy.context.space_data.viewport_shade == 'SOLID' :
				bpy.context.space_data.viewport_shade = 'TEXTURED'
				
			elif bpy.context.space_data.viewport_shade == 'TEXTURED' :
				bpy.context.space_data.viewport_shade = 'MATERIAL'
	
		else :

			if bpy.context.space_data.viewport_shade == 'MATERIAL' :
				bpy.context.space_data.viewport_shade = 'TEXTURED'
				
			elif bpy.context.space_data.viewport_shade == 'TEXTURED' :
				bpy.context.space_data.viewport_shade = 'SOLID'
				
			elif bpy.context.space_data.viewport_shade == 'SOLID' :
				bpy.context.space_data.viewport_shade = 'WIREFRAME'
						
		return {'FINISHED'}	
	
	
# Show / hide manipulator (Translate/Rotate) vs Hide
class ManipulatorSwitcher(bpy.types.Operator):
	
	bl_idname = "view3d.manipulator_switcher"
	bl_label = "Manipulator Switcher"

	def execute(self, context):
			
		if( bpy.context.space_data.show_manipulator and (bpy.context.space_data.transform_manipulators == {'TRANSLATE', 'ROTATE'} ) ) :
			bpy.context.space_data.show_manipulator = False
		else :
			bpy.context.space_data.show_manipulator = True
			bpy.context.space_data.transform_manipulators = {'TRANSLATE', 'ROTATE'}
		
		return {'FINISHED'}

'''
class OrientationSwitcher(bpy.types.Operator):
	
	bl_idname = "view3d.orientation_switcher"
	bl_label = "Orientation Switcher"

	def execute(self, context):
		
		manipulators = bpy.context.space_data.transform_manipulators
		rotate = False
		orientation = bpy.context.space_data.transform_orientation
		
		for m in manipulators :
			if(m == 'ROTATE') :
				rotate = True
		
		locked = True # there must be one unlocked			
		ob = bpy.context.active_object
		
		# only for POSE mode
		if ob and ob.mode == 'POSE' :
			for bone in bpy.context.selected_pose_bones :
				# Quaternion
				if bone.rotation_mode == 'QUATERNION' :			
					if(not bone.lock_rotation_w):
						locked = False
		
				# Euler	+ Quaternion rest				
				for i in range(3):
					if(not bone.lock_rotation[i]):
						locked = False
	#	else :
	#		locked = False	
		
		# switching manipulators
		# with GIMBAL		
		if(rotate and not locked) :
			
			if orientation == "LOCAL" :
				orientation = "GLOBAL"
				
			elif orientation == "GLOBAL" :
				orientation = "GIMBAL"
				
			elif orientation == "GIMBAL" :
				orientation = "LOCAL"
		
		# LOCAL / GLOBAL	
		else :
			print('neni')
			if orientation == "LOCAL" :
				orientation = "GLOBAL"
			else :
				orientation = "LOCAL"
		
		bpy.context.space_data.transform_orientation = orientation
		
		return {'FINISHED'}
'''	

# my isolate version
class IsolateObject(bpy.types.Operator):
	
	bl_idname = "view3d.isolate_object"
	bl_label = "Isolate Object"

	def execute(self, context):
		
		obj = bpy.context.selected_objects
		if(len(obj) > 0):
			bpy.ops.view3d.localview()
			if(bpy.context.object.type == 'MESH'):
				bpy.ops.object.select_all(action='TOGGLE')
			
			for o in obj :
				o.select = True

		else:
			bpy.ops.view3d.localview()	
				 
		return {'FINISHED'}
	
	
################	
class NLAToolsButtons(Header):
	
	bl_space_type = 'NLA_EDITOR'

	def draw(self, context):
		
		layout = self.layout
		col = layout.column()
		col = layout.column()
		row = col.row(align = True)

		row.operator( "nla.cut_strip" , icon = "NLA")	


################
class TextToolsButtons(Header):
	
	bl_space_type = 'TEXT_EDITOR'

	def draw(self, context):
		
		currentIcon = ""
		
		if( bpy.app.debug_wm ):
			currentIcon = "CHECKBOX_HLT"
		else:
			currentIcon = "CHECKBOX_DEHLT"

		layout = self.layout
		row = layout.row()
		row = layout.row(align=True)
		row.operator( "text.show_all_op" , icon = currentIcon)	

				
class ShowAllOp(bpy.types.Operator):

	'''Show all commands in Info output'''
	bl_idname = "text.show_all_op"
	bl_label = "Show All Operators"
#	bl_options = {'REGISTER', 'UNDO'}

	
	def execute(self, context):
		bpy.app.debug_wm = not bpy.app.debug_wm
		return {'FINISHED'}	
	
				
################
# POSE ANIMATION FLIPPED #
################

# copy and flip pose in one step
class CutStrip(bpy.types.Operator):

	'''Cut strip by scene setting'''
	bl_idname = "nla.cut_strip"
	bl_label = "Cut Strip"
	bl_options = {'REGISTER', 'UNDO'}

	
	def execute(self, context):

		try:
		    selected_strips = [strip for strip in bpy.context.object.animation_data.nla_tracks.active.strips if strip.select]
		except AttributeError:
		    selected_strips = []

		if bpy.context.scene.use_preview_range :
			
			startFrame = bpy.context.scene.frame_preview_start
			endFrame = bpy.context.scene.frame_preview_end

			for strip in selected_strips :
				strip.action_frame_start = startFrame
				strip.action_frame_end = endFrame
				
		# redraw 
		for area in bpy.context.screen.areas:
			if area.type == 'NLA_EDITOR':
				area.tag_redraw()
			
		return {'FINISHED'}	
	
	
# NLA Tweak mode #
class NLATweakRangeToggle(bpy.types.Operator):

	'''Tweak and Range Toggle'''
	bl_idname = "nla.tweak_and_range"
	bl_label = "Tweak and Range Toggle"


	preview = BoolProperty(name="Set Preview",default=True)
	
	
	def execute(self, context):
		
		# Enter #
		if( not bpy.context.scene.is_nla_tweakmode ):
			
			bpy.ops.nla.tweakmode_enter()
			
			if(self.preview):
				bpy.ops.nla.previewrange_set()
			
			# set timeline to frame range
			for area in bpy.context.screen.areas:
				
				FrameForEditor( area, 'TIMELINE')
				FrameForEditor( area, 'DOPESHEET_EDITOR')
				FrameForEditor( area, 'GRAPH_EDITOR')
				bpy.ops.nla.view_selected()

		# Exit # TODO: not working
		else:
			bpy.ops.nla.tweakmode_exit()
			bpy.context.scene.use_preview_range = False
			bpy.ops.nla.view_selected()

		return {'FINISHED'}


def FrameForEditor( currentArea, testedArea ):
	
	if currentArea.type == testedArea:
		for region in currentArea.regions:
			if region.type == 'WINDOW':
				ctx = bpy.context.copy()
				ctx[ 'area'] = currentArea
				ctx['region'] = region
				
				if(testedArea == 'TIMELINE'):
					bpy.ops.time.view_all(ctx)
					
				elif(testedArea == 'DOPESHEET_EDITOR'):
					bpy.ops.action.view_all(ctx)
					
				elif(testedArea == 'GRAPH_EDITOR'):
					bpy.ops.graph.view_all(ctx)
						
				break
	

class VIEW3D_HT_header_cenda(Header):
	
	bl_space_type = 'VIEW_3D'


	def draw(self, context):
		
		layout = self.layout
		row = layout.row(align=True)
		row = layout.row(align=True)
		
		# buttons
		row.operator("screen.region_quadview", text = "Toggle Quad View")
		row = layout.row(align=True)
		
		# simplify
		state = bpy.context.scene.render.use_simplify

		if (state) :
			current_icon = 'CHECKBOX_HLT'
		else:
			current_icon = 'CHECKBOX_DEHLT'
			
		row.operator("scene.simplify_toggle", icon = current_icon)
		row = layout.row(align=True)
		
		'''
		# fluid bake
		obj = bpy.context.active_object
		if "Fluidsim" in obj.modifiers :
		#	if fluid.type == 'DOMAIN':
		#	row.operator("fluid.bake", text="Bake",translate=False, icon='MOD_FLUIDSIM')
			row.operator("object.bake_fluid", text="Bake",translate=False, icon='MOD_FLUIDSIM')
		'''

'''
class BakeFluid(bpy.types.Operator):

	bl_idname = "object.bake_fluid"
	bl_label = "Bake Fluid"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		bpy.ops.fluid.bake()
		return {'FINISHED'}
'''		

class SimplifyToggle(bpy.types.Operator):

	'''Simplify Toggle'''
	bl_idname = "scene.simplify_toggle"
	bl_label = "Simplify"
	bl_options = {'REGISTER', 'UNDO'}

	
	def execute(self, context):

		bpy.context.scene.render.use_simplify = not bpy.context.scene.render.use_simplify

		return {'FINISHED'}
	
	
###########################################################
class SetInOutRange(bpy.types.Operator):

	'''Set In and Out Range'''
	bl_idname = "time.range_in_out"
	bl_label = "Set In and Out Range"
	bl_options = {'REGISTER', 'UNDO'}
	
	
	options = [
	("StartRange", "Start Range", "", "", 0),
    ("EndRange", "End Range", "", "", 1)
    ]

	range = EnumProperty( name = "Range", description = "", items = options )
	
	
	def execute(self, context):

		bpy.context.scene.use_preview_range = True

		if(self.range == 'StartRange'):
			bpy.context.scene.frame_preview_start = bpy.context.scene.frame_current

		else:
			bpy.context.scene.frame_preview_end = bpy.context.scene.frame_current


		return {'FINISHED'}	
			
				
################################################################
# register #

def register():
	bpy.utils.register_module(__name__)
	
def unregister():
	bpy.utils.unregister_module(__name__)
	
if __name__ == "__main__":
	register()