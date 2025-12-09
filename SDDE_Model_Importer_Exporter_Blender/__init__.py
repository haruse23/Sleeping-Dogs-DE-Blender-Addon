bl_info = {
    "name": "SDDE Importer and Exporter",
    "author": "haru233",
    "version": (1, 0),
    "blender": (4, 5, 0),
    "location": "File > Import, File > Export",
    "description": "Import and Export SDDE Game Models",
    "category": "Import-Export",
}


import bpy
from .BlenderSDDE import ImportSDDEModel, ExportSDDEModel


class SDDE_CollectionItem(bpy.types.PropertyGroup):
    collection: bpy.props.PointerProperty(type=bpy.types.Collection)
    selected: bpy.props.BoolProperty(default=False)


class SDDE_UL_CollectionList(bpy.types.UIList):
    bl_idname = "SDDE_UL_CollectionList"

    def draw_item(self, context, layout, data, item, icon, active_data, active_prop, index):
        row = layout.row()
        row.prop(item, "selected", text=item.collection.name)


class IMPORT_OT_sdde(bpy.types.Operator):
    bl_idname = "import_scene.sdde"
    bl_label = "Import SDDE"
    bl_options = {'PRESET'}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        from .BlenderSDDE import ImportSDDEModel
        ImportSDDEModel(self.filepath)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class EXPORT_OT_sdde(bpy.types.Operator):
    bl_idname = "export_scene.sdde"
    bl_label = "Export SDDE"
    bl_options = {'PRESET'}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def draw(self, context):
        layout = self.layout
        layout.label(text="Select Collections to Export:")
        layout.template_list(
            "SDDE_UL_CollectionList", "",
            context.scene, "sdde_export_collections",
            context.scene, "sdde_export_collection_index",
        )

    def invoke(self, context, event):
        populate_collection_list()  # refresh the list
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


    def execute(self, context):
        selected_cols = [
            item.collection for item in context.scene.sdde_export_collections
            if item.selected
        ]

        if not selected_cols:
            self.report({'ERROR'}, "No collections selected for export")
            return {'CANCELLED'}
            
        for col in selected_cols:
            ExportSDDEModel(self.filepath)
            print("Exporting collection:", col.name)
        # ------------------------------------------

        return {'FINISHED'}


def menu_func_import(self, context):
    self.layout.operator(IMPORT_OT_sdde.bl_idname, text="SDDE (.perm.bin)")


def menu_func_export(self, context):
    self.layout.operator(EXPORT_OT_sdde.bl_idname, text="SDDE (.perm.bin)")


def populate_collection_list():
    """Fill the export list with all collections."""
    scn = bpy.context.scene
    scn.sdde_export_collections.clear()

    for col in bpy.data.collections:
        item = scn.sdde_export_collections.add()
        item.collection = col
        item.selected = False


def register():
    bpy.utils.register_class(IMPORT_OT_sdde)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

    bpy.utils.register_class(SDDE_CollectionItem)
    bpy.utils.register_class(SDDE_UL_CollectionList)
    bpy.utils.register_class(EXPORT_OT_sdde)
    bpy.types.Scene.sdde_export_collections = bpy.props.CollectionProperty(type=SDDE_CollectionItem)
    bpy.types.Scene.sdde_export_collection_index = bpy.props.IntProperty(default=0)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_class(IMPORT_OT_sdde)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

    bpy.utils.unregister_class(SDDE_CollectionItem)
    bpy.utils.unregister_class(SDDE_UL_CollectionList)
    bpy.utils.unregister_class(EXPORT_OT_sdde)
    del bpy.types.Scene.sdde_export_collections
    del bpy.types.Scene.sdde_export_collection_index
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()
