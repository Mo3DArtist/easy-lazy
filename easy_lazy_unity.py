bl_info = {
    "name": "Easy Lazy Unity",
    "blender": (2, 80, 0),
    "category": "Object",
    "author": "Mohamed Fathi",
    "description": "Batch rename and lazy parent objects with ease.",
    "location": "View3D > Sidebar > Easy Lazy Unity",
    "warning": "",
    "doc_url": "https://github.com/Mo3DArtist/easy-lazy",
    "tracker_url": "https://github.com/Mo3DArtist/easy-lazy/issues",
    "support": "COMMUNITY",
    "version": (1, 2),
}

import bpy

class EasyLazyUnityPanel(bpy.types.Panel):
    bl_label = "Easy Lazy Unity"
    bl_idname = "OBJECT_PT_easy_lazy_unity"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Easy Lazy Unity'
    
    def draw(self, context):
        layout = self.layout
        
        # Multi Rename Section
        layout.label(text="Multi Rename")
        layout.prop(context.scene, "new_name", icon='MESH_CUBE')
        layout.operator("object.easy_lazy_multi_rename", text="Rename Selected", icon='OUTLINER_DATA_MESH')
        
        layout.separator()
        
        # Lazy Parent Section
        layout.label(text="Lazy Parent")
        layout.prop_search(context.scene, "parent_object", context.scene, "objects", icon='GROUP')
        layout.operator("object.easy_lazy_parent", text="Set Parent", icon='CONSTRAINT')
        layout.operator("object.easy_lazy_add_empty", text="Add Empty as Parent", icon='OUTLINER_OB_EMPTY')
        
        layout.separator()
        
        # Apply Transforms Section
        layout.label(text="Apply Transforms")
        layout.operator("object.easy_lazy_apply_transforms", text="Apply Transforms", icon='OBJECT_ORIGIN')
        layout.operator("object.easy_lazy_apply_transforms_origin", text="Apply Transforms & Set Origin", icon='PIVOT_BOUNDBOX')
        layout.operator("object.easy_lazy_recenter_objects", text="Recenter Objects", icon='PIVOT_CURSOR')

class EasyLazyMultiRename(bpy.types.Operator):
    bl_idname = "object.easy_lazy_multi_rename"
    bl_label = "Rename Selected Objects"

    def execute(self, context):
        new_name = context.scene.new_name
        selected_objects = context.selected_objects
        for idx, obj in enumerate(selected_objects):
            obj.name = f"{new_name}.{str(idx).zfill(2)}"
        return {'FINISHED'}

class EasyLazyParent(bpy.types.Operator):
    bl_idname = "object.easy_lazy_parent"
    bl_label = "Set Parent"

    def execute(self, context):
        parent_object = context.scene.parent_object
        selected_objects = context.selected_objects
        for obj in selected_objects:
            if obj.name != parent_object.name:
                obj.parent = parent_object
        return {'FINISHED'}

class EasyLazyAddEmpty(bpy.types.Operator):
    bl_idname = "object.easy_lazy_add_empty"
    bl_label = "Add Empty as Parent"

    def execute(self, context):
        empty = bpy.data.objects.new("Empty", None)
        bpy.context.collection.objects.link(empty)
        for obj in context.selected_objects:
            obj.parent = empty
        return {'FINISHED'}

class EasyLazyApplyTransforms(bpy.types.Operator):
    bl_idname = "object.easy_lazy_apply_transforms"
    bl_label = "Apply Transforms"

    def execute(self, context):
        for obj in context.selected_objects:
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        return {'FINISHED'}

class EasyLazyApplyTransformsOrigin(bpy.types.Operator):
    bl_idname = "object.easy_lazy_apply_transforms_origin"
    bl_label = "Apply Transforms & Set Origin"

    def execute(self, context):
        for obj in context.selected_objects:
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
        return {'FINISHED'}

class EasyLazyRecenterObjects(bpy.types.Operator):
    bl_idname = "object.easy_lazy_recenter_objects"
    bl_label = "Recenter Objects"

    def execute(self, context):
        selected_objects = context.selected_objects
        if not selected_objects:
            return {'CANCELLED'}
        
        # Reset the location of the 3D cursor to the origin
        bpy.context.scene.cursor.location = (0.0, 0.0, 0.0)
        cursor_location = bpy.context.scene.cursor.location

        for obj in selected_objects:
            obj.location = cursor_location
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(EasyLazyUnityPanel)
    bpy.utils.register_class(EasyLazyMultiRename)
    bpy.utils.register_class(EasyLazyParent)
    bpy.utils.register_class(EasyLazyAddEmpty)
    bpy.utils.register_class(EasyLazyApplyTransforms)
    bpy.utils.register_class(EasyLazyApplyTransformsOrigin)
    bpy.utils.register_class(EasyLazyRecenterObjects)
    bpy.types.Scene.new_name = bpy.props.StringProperty(name="New Name", default="Object")
    bpy.types.Scene.parent_object = bpy.props.PointerProperty(type=bpy.types.Object)

def unregister():
    bpy.utils.unregister_class(EasyLazyUnityPanel)
    bpy.utils.unregister_class(EasyLazyMultiRename)
    bpy.utils.unregister_class(EasyLazyParent)
    bpy.utils.unregister_class(EasyLazyAddEmpty)
    bpy.utils.unregister_class(EasyLazyApplyTransforms)
    bpy.utils.unregister_class(EasyLazyApplyTransformsOrigin)
    bpy.utils.unregister_class(EasyLazyRecenterObjects)
    del bpy.types.Scene.new_name
    del bpy.types.Scene.parent_object

if __name__ == "__main__":
    register()