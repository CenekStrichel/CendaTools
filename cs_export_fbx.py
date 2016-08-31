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
	"name": "Export FBX",
	"author": "Cenek Strichel",
	"version": (1, 0, 0),
	"blender": (2, 77, 0),
	"location": "Tools > Export to FBX",
	"description": "Export selected objects to destination (FBX)",
	"category": "Cenda Tools"}
	

import bpy
from shutil import copyfile


class StringsGroup(bpy.types.PropertyGroup):
	
	bpy.types.Scene.Simplify = bpy.props.FloatProperty(
	name = "Simplify",
	default = 0.1,
	soft_min = 0.0,
	description = "How simplify baked animation\n0 is disabled")
	
	bpy.types.Scene.NLAExport = bpy.props.BoolProperty( 
	name = "Export NLA Strips", 
	default = True, 
	description = "Only clip from NLA will be exported")
	
	bpy.types.Scene.ExportFBX = bpy.props.StringProperty(
	name = "Export",
	default = "",
	subtype = "FILE_PATH",
	description = "Export path\nE:\\model.fbx")
	
	bpy.types.Scene.Backup = bpy.props.BoolProperty( 
	name = "Backup", 
	default = False, 
	description = "Optional\nEnable copy exported file to file")
	
	bpy.types.Scene.BackupFBX = bpy.props.StringProperty( 
	name = "Backup Path", 
	default = "", 
	subtype = "FILE_PATH", 
	description = "Optional\nCopy exported file to file")
	
	


class ExportToPlacePanel(bpy.types.Panel):
	
	bl_label = "Export to FBX"
	bl_idname = "EXPORT_PANEL"
	
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "Tools"
	bl_context = "objectmode"


	def draw(self, context):
		
		scn = context.scene
		layout = self.layout
		row = layout.row(align=True)

		# Settings
		box = layout.box()
		
		box.label("Settings")
		box.prop( scn, "Simplify" )
		box.prop( scn, "NLAExport" )	
		

		# Export
		box = layout.box()
		
		box.label("Export Paths")
		box.prop( scn, "ExportFBX", text = "" )

		# Backup
		box.prop( scn, "Backup" )

		if(bpy.context.scene.Backup):
			box.prop( scn, "BackupFBX", text = ""  )

		# Export button
		row = layout.row(align=True)
		row.scale_y = 2
		row.operator("cenda.export_to_place", text = "Export", icon="EXPORT" )


# rename button	
class ExportToPlace(bpy.types.Operator):
	
	
	"""Export selected FBX"""
	bl_idname = "cenda.export_to_place"
	bl_label = "Export to Place"


	def execute(self, context ):

		exportPath = context.scene.ExportFBX
		
		# check if something is selected
		if( len(context.selected_objects) == 0):
			self.report({'ERROR'}, ("No objects selected") )
			return{'FINISHED'}
		
		# check if path is setted
		if( exportPath == "" ):
			self.report({'ERROR'}, ("Export path is not setted") )
			return{'FINISHED'}

		# check fbx
		if( not exportPath.endswith (".fbx") and not backupPath.endswith (".FBX") ):
			context.scene.ExportFBX += ".fbx"
			exportPath += ".fbx"
			
		# convert relative path to absolute
		exportPath = bpy.path.abspath( exportPath ) 
		
		# export
		bpy.ops.export_scene.fbx(

		filepath = exportPath,
		check_existing = True,
		axis_forward = '-Z',
		axis_up = 'Y',
		version = 'BIN7400',

		use_selection = True,
		global_scale = 1.0,
		apply_unit_scale = False,
		bake_space_transform = False,
		object_types = {'MESH', 'OTHER', 'EMPTY', 'CAMERA', 'LAMP', 'ARMATURE'},
		use_mesh_modifiers = True,
		mesh_smooth_type = 'OFF',

		use_mesh_edges = False,
		use_tspace = False,
		use_custom_props = False,
		add_leaf_bones = False,
		primary_bone_axis = 'Y',
		secondary_bone_axis = 'X',
		use_armature_deform_only = True,
		armature_nodetype = 'NULL',

		bake_anim = True,
		bake_anim_use_all_bones = True,
		bake_anim_use_nla_strips = context.scene.NLAExport,
		bake_anim_use_all_actions = False,
		bake_anim_force_startend_keying = True,
		bake_anim_step = 1.0,
		bake_anim_simplify_factor = context.scene.Simplify,

		use_anim = True,
		use_anim_action_all = True,
		use_default_take = True,
		use_anim_optimize = True,

		anim_optimize_precision = 6.0,
		path_mode = 'AUTO',
		embed_textures = False,
		batch_mode = 'OFF',
		use_batch_own_dir = True
		)

		self.report({'INFO'}, ("Exported to " + exportPath) )
		
		# BACKUP #
		if( context.scene.Backup ):

			backupPath = context.scene.BackupFBX
			
			# make backup
			if( backupPath == "" ):
				self.report({'ERROR'}, ("FBX backup path is not setted") )
				return{'FINISHED'}
	
			# check fbx
			if( not backupPath.endswith (".fbx") and not backupPath.endswith (".FBX") ):
				context.scene.BackupFBX += ".fbx"
				backupPath += ".fbx"
				
			# convert relative path to absolute	
			backupPath = bpy.path.abspath( backupPath )
			
			# duplicate exported FBX	
			copyfile(exportPath, backupPath)

		return{'FINISHED'} 


################################################################
# register #

def register():
	bpy.utils.register_module(__name__)
	
def unregister():
	bpy.utils.unregister_module(__name__)
	
if __name__ == "__main__":
	register()