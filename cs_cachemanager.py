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
	"name": "Cache Manager",
	"category": "Cenda Tools",
	"author": "Cenek Strichel",
	"version": (1, 0, 0),
	"blender": (2, 79, 0),
	"description": "Manager for cache files of physics files",
	"location": "Properties physics panel",
	"wiki_url": "https://github.com/CenekStrichel/CendaTools/wiki",
	"tracker_url": "https://github.com/CenekStrichel/CendaTools/issues"
}


import bpy
import os
import subprocess

from bpy.props import IntProperty, BoolProperty, FloatProperty, StringProperty, EnumProperty


class CacheDeletePanel(bpy.types.Panel):
	
	"""Creates a Panel in the scene context of the properties editor"""
	bl_label = "Cache Manager"
	bl_idname = "CACHEMANAGER_PT_layout"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "physics"
	
	bpy.types.Object.CacheDeleteFile = StringProperty( 
	name = "Cache File", 
	default = "",
	description = "Cache file")
	
	def draw(self, context):
		
		layout = self.layout
		
		obj = context.object
		scn = context.scene
		domainFound = False
		
		for modifier in obj.modifiers:
			if modifier.type == 'SMOKE':
			#	if modifier.smoke_type == 'DOMAIN':
					
				domainFound = True
				
				# cache file name
				row = layout.row(align=True)
				row.prop( obj, "CacheDeleteFile" )

				# cache file warning
				if(len(context.object.CacheDeleteFile) > 0):
					
					filepath = bpy.data.filepath.split("\\")
					file = filepath[ len(filepath)-1 ].replace(".blend","")
					directory = bpy.data.filepath.replace(filepath[ len(filepath)-1 ], "")
					frame = bpy.context.scene.frame_current + 1 # +1 because zero is not cached
					fileCache = (directory + "blendcache_" + file + "\\" + context.object.CacheDeleteFile + "_" + str(frame).zfill(6) + "_00.bphys" )
					
					if(os.path.isfile( fileCache )):

						# cache delete button
						row = layout.row(align=True)
						row.operator("view3d.cache_delete_files", text = "Delete Cache", icon = "CANCEL")
						
				# open folder
				row = layout.row(align=True)	
				row.operator("view3d.cache_file_folder_open", text = "Open Cache Folder", icon = "FILE_FOLDER")	
					
		if(domainFound == False):
			row = layout.row(align=True)
			row.label("Select Smoke Object")

	
class OpenCacheFolder(bpy.types.Operator):

	"""Open folder with cache"""
	bl_label = "Open cache folder"
	bl_idname = "view3d.cache_file_folder_open"

	def execute(self, context):
		
		filepath = bpy.data.filepath.split("\\")
		file = filepath[ len(filepath)-1 ].replace(".blend","")
		directory = bpy.data.filepath.replace(filepath[ len(filepath)-1 ], "")
		finalDirectory = directory + "blendcache_" + file
		subprocess.Popen("explorer "+finalDirectory)

		return {'FINISHED'}
		
		
class CacheDelete(bpy.types.Operator):

	"""Creates a Panel in the scene context of the properties editor"""
	bl_label = "Delete cache files"
	bl_idname = "view3d.cache_delete_files"

	def execute(self, context):

		if(len(context.object.CacheDeleteFile) == 0):
			self.report({'ERROR'}, ("Set cache file first") )
			return{'FINISHED'}
		
		else:
			cacheName = context.object.CacheDeleteFile


		filepath = bpy.data.filepath.split("\\")
		file = filepath[ len(filepath)-1 ].replace(".blend","")
		directory = bpy.data.filepath.replace(filepath[ len(filepath)-1 ], "")


		if(bpy.context.scene.use_preview_range):
			startFrame = bpy.context.scene.frame_preview_start
			endFrame = bpy.context.scene.frame_preview_end
		else:
			startFrame = bpy.context.scene.frame_start
			endFrame = bpy.context.scene.frame_end


		for i in range( startFrame, endFrame+1 ):
			
			fileCache = (directory + "blendcache_" + file + "\\" + cacheName + "_" + str(i).zfill(6) + "_00.bphys" )
			
			try:
				os.remove( fileCache )

			except OSError:
				pass
			
		return {'FINISHED'}


############################################################################################
def register():
	bpy.utils.register_module(__name__)


def unregister():
	bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
	register()