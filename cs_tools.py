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
	"version": (1, 0, 2),
	"blender": (2, 79, 0),
	"location": "Many commands",
	"description": "Many tools",
	"category": "Cenda Tools",
	"wiki_url": "https://github.com/CenekStrichel/CendaTools/wiki",
	"tracker_url": "https://github.com/CenekStrichel/CendaTools/issues"
	}

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
				bpy.context.scene.frame_preview_start = bpy.context.scene.frame_current + 1
			
				# start range
				markerStatus = bpy.ops.screen.marker_jump(next = True)
				if(markerStatus == {'CANCELLED'} ):
					bpy.context.scene.frame_preview_end += 200
				else:	
					bpy.context.scene.frame_preview_end = bpy.context.scene.frame_current + 1
					
	
		# BACKWARD #
		else:

			bpy.ops.screen.marker_jump(next = False)
	
			bpy.context.scene.frame_preview_end = bpy.context.scene.frame_current
		
			# start range
			markerStatus = bpy.ops.screen.marker_jump(next = False)
			if(markerStatus == {'CANCELLED'} ):
				bpy.context.scene.frame_preview_start = 0
			else:	
				bpy.context.scene.frame_preview_start = bpy.context.scene.frame_current
	
			# if end, jump to first
			if( bpy.context.scene.frame_preview_start == 0 and bpy.context.scene.frame_preview_end == 0):
				markerStatus = bpy.ops.screen.marker_jump(next = True)
				bpy.context.scene.frame_preview_end = bpy.context.scene.frame_current
				self.report({'INFO'},"First Shot Reached")
				
		# change after setting shot
		bpy.context.scene.frame_current	= bpy.context.scene.frame_preview_start
		if(not last):
			bpy.context.scene.frame_preview_end -= 1 # I dont want show next marker shot
		
		# frame timeline
		for area in bpy.context.screen.areas:
			FrameForEditor( area, 'TIMELINE')

		return{'FINISHED'}
			

class ShowCameraView(bpy.types.Operator):

	bl_idname = "screen.show_camera_view"
	bl_label = "Show Camera View"

	def execute(self, context):
		
		space = bpy.context.space_data
		
		# Normal view
		if(space.region_3d.view_perspective == 'CAMERA'):
			space.show_only_render = False
			space.show_manipulator = True
			space.fx_settings.use_ssao  = False

		# CAMERA VIEW
		else:
			space.show_only_render = True
			space.show_manipulator = False
			space.fx_settings.use_ssao  = True
			
		bpy.ops.view3d.viewnumpad(type = "CAMERA")

		return {'FINISHED'}
	
	
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
	
	
class HideObjects(bpy.types.Operator):
	
	bl_idname = "object.hide_view_and_render"
	bl_label = "Hide View and Render"
	
#	extend = BoolProperty(name="Extend", default=False)

#	@classmethod
#	def poll(cls, context):
#		return context.area.type == 'GRAPH_EDITOR'

	def execute(self, context):

		bpy.ops.object.hide_view_set()
		bpy.ops.object.hide_render_set()

				
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


class WeightMaskSelect(bpy.types.Operator):
	
	bl_idname = "paint.weight_mask_select"
	bl_label = "Weight Mask Select"
	
	SelectTypeEnum = [
		("More", "More", "", "", 0),
	    ("Less", "Less", "", "", 100),
	    ]
	
	selectType = EnumProperty( name = "Select Type", description = "", items=SelectTypeEnum )
	
#	@classmethod
#	def poll(cls, context):
#		return context.area.type == 'GRAPH_EDITOR'

	def execute(self, context):
		
		'''
		if(context.weight_paint_object.data.use_paint_mask_vertex):
			self.report({'ERROR'}, "Only Face Mask is supported for now!")
			return {'FINISHED'}	
		
		if(context.object.data.use_paint_mask_vertex):
			self.report({'ERROR'}, "Only Face Mask is supported for now!")
			return {'FINISHED'}	
		'''
		
	#	bpy.context.object.data.use_paint_mask = True

		bpy.ops.object.editmode_toggle()
		
			
		if(self.selectType == 'More'):
			bpy.ops.mesh.select_more()
			
		elif(self.selectType == 'Less'):
			bpy.ops.mesh.select_less()
			
		bpy.ops.object.editmode_toggle()
		bpy.ops.paint.weight_paint_toggle()
		
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

# my isolate version - not working well, don`t use it
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
	
	
	
class JoinObjectsWithUV(bpy.types.Operator):
	
	bl_idname = "object.join_with_uv"
	bl_label = "Join with UV"
	bl_options = {'REGISTER', 'UNDO'}
	
	uvmerge = BoolProperty(name="UV Merge",default=True)
	
	def execute(self, context):
		
		if(self.uvmerge):
			# rename UV for merge
			newName = bpy.context.object.data.uv_textures[0].name
			
			# all objects UV rename
			for obj in bpy.context.selected_objects:
				obj.data.uv_textures[0].name = newName

		# join
		bpy.ops.object.join()	
						 
		return {'FINISHED'}
		

	

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
		
		#################################################
		# quad view
		row.operator("screen.region_quadview", text = "Quad View", icon = "GRID")
		
		# simplify			
		state = bpy.context.scene.render.use_simplify
		
		if (state) :
			current_icon = 'CHECKBOX_HLT'
		else:
			current_icon = 'CHECKBOX_DEHLT'
			
		row.operator("scene.simplify_toggle", icon = current_icon)
			
		#################################################	
		# culling	
		row = layout.row(align=True)	
		state = bpy.context.space_data.show_backface_culling

		if (state) :
			current_icon = 'CHECKBOX_HLT'
		else:
			current_icon = 'CHECKBOX_DEHLT'
		
		row.operator("scene.backface_toggle", icon = current_icon)

		# texture	
		if( context.scene.render.engine == "BLENDER_RENDER" and context.object.type == "MESH"):
			row.operator("scene.texture_toggle")
		
		'''
		#################################################
		# export
		row = layout.row(align=True)
		
		if(bpy.context.active_object.mode  == 'OBJECT'):
			row.enabled = True
		else:
			row.enabled = False
			
		# only first override is used
		textExport = context.scene.ExportPath.rsplit('\\', 1)[-1]
	#	icon = "EXPORT"
		
		for obj in bpy.context.selected_objects:
			if( obj.ExportOverride ):
				textExport = "[ " + context.object.ExportPathOverride.rsplit('\\', 1)[-1] + " ]"	
			#	icon = "PMARKER_ACT"
				break
			
		if(len(textExport) > 0):
			row.operator("cenda.export_to_place", icon = "EXPORT", text = textExport)
		'''
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
#	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		bpy.ops.fluid.bake()
		return {'FINISHED'}
'''		


class SimplifyToggle(bpy.types.Operator):

	'''Simplify Toggle'''
	bl_idname = "scene.simplify_toggle"
	bl_label = "Simplify"
#	bl_options = {'REGISTER', 'UNDO'}

	
	def execute(self, context):

		bpy.context.scene.render.use_simplify = not bpy.context.scene.render.use_simplify

		return {'FINISHED'}
	
	
class BackfaceToggle(bpy.types.Operator):

	'''Backface'''
	bl_idname = "scene.backface_toggle"
	bl_label = "Culling"
#	bl_options = {'REGISTER', 'UNDO'}

	
	def execute(self, context):

		bpy.context.space_data.show_backface_culling = not bpy.context.space_data.show_backface_culling

		return {'FINISHED'}
		
		
		
class TextureToggle(bpy.types.Operator):

	'''Texture Toggle'''
	bl_idname = "scene.texture_toggle"
	bl_label = "Texture"
#	bl_options = {'REGISTER', 'UNDO'}

	
	def execute(self, context):

		# hardcoded for now (for normal maps)
		context.object.active_material.use_textures[1] = not context.object.active_material.use_textures[1]

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
		
	
class ShowMaterial(bpy.types.Operator):

	'''Show Material'''
	bl_idname = "scene.show_material"
	bl_label = "Show Material"
	bl_options = {'REGISTER', 'UNDO'}


	def execute(self, context):
		
		obj = bpy.context.active_object

		#
		if(obj.type == "MESH"):
			
			for area in bpy.context.screen.areas: # iterate through areas in current screen
				if area.type == 'PROPERTIES':
					for space in area.spaces: # iterate through all founded panels
						if space.type == 'PROPERTIES':	
							space.context = 'MATERIAL'
						
		return {'FINISHED'}	
	
	
class ParentObject(bpy.types.Operator):

	'''Make Parent and Show'''
	bl_idname = "object.parent_and_show"
	bl_label = "Make Parent and Show"
	bl_options = {'REGISTER', 'UNDO'}


	def execute(self, context):
		
		# show all
		for obj in bpy.context.selected_objects:
			obj.hide = False
			
		bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
				
		return {'FINISHED'}
	
	
class ProportionalSwitcher(bpy.types.Operator):

	'''Proportional Switcher'''
	bl_idname = "scene.proportional_switcher"
	bl_label = "Proportional Switcher"
#	bl_options = {'REGISTER', 'UNDO'}

	proportionalType = [
#	("DISABLED", "DISABLED", "", "", 0),
    ("ENABLED", "Enable", "", "", 0),
	("PROJECTED", "Projected", "", "", 1),
    ("CONNECTED", "Connected", "", "", 2)
    ]

	type = EnumProperty( name = "Type", description = "", items = proportionalType )
	
	def execute(self, context):
		
		# same is calling toggle
		if( bpy.context.scene.tool_settings.proportional_edit != 'DISABLED' ):
			bpy.context.scene.tool_settings.proportional_edit = 'DISABLED'
			
		elif( bpy.context.scene.tool_settings.proportional_edit == 'DISABLED' ): 
			bpy.context.scene.tool_settings.proportional_edit = self.type
			
		else:
			bpy.context.scene.tool_settings.proportional_edit = 'DISABLED'
	
		# TODO - add also DOPE and GRAPH
		
		return {'FINISHED'}
	
	
#class SelectRecursiveAndShow(bpy.types.Operator):

#	'''Select Recursive and Show'''
'''
	bl_idname = "outliner.select_recursive_and_show"
	bl_label = "Select Recursive and Show"
	bl_options = {'REGISTER', 'UNDO'}


	def execute(self, context):
		
		bpy.ops.outliner.item_activate('INVOKE_DEFAULT')

		
		
	#	# show all
	#	for obj in bpy.context.selected_objects:
	#		obj.hide = False
			
	#	bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
				
		return {'FINISHED'}	
'''							
################################################################
# register #

def register():
	bpy.utils.register_module(__name__)
	
def unregister():
	bpy.utils.unregister_module(__name__)
	
if __name__ == "__main__":
	register()