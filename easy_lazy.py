import bpy

bl_info = {
    "name": "Easy Lazy",
    "blender": (2, 80, 0),
    "category": "Object",
    "author": "Your Name",
    "location": "View3D > Sidebar > Easy Lazy",
    "description": "Batch rename and lazy parent objects with ease.",
    "wiki_url": "https://github.com/your-repo/easy_lazy",
    "tracker_url": "https://github.com/your-repo/easy_lazy/issues",
    "support": "COMMUNITY",
    "version": (1, 0),
}

class OBJECT_OT_multi_rename(bpy.types.Operator):
    """Multi Rename Selected Objects"""
    bl_idname = "object.multi_rename"
    bl_label = "Multi Rename Objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        base_name = context.scene.multi_rename_base_name
        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}
        
        for i, obj in enumerate(selected_objects, start=1):
            obj.name = f"{base_name}.{str(i).zfill(2)}"
        
        return {'FINISHED'}

class OBJECT_OT_create_empty_and_add_to_list(bpy.types.Operator):
    """Create an Empty and Add to List"""
    bl_idname = "object.create_empty_and_add_to_list"
    bl_label = "Create Empty and Add to List"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        empty_name = context.scene.empty_name
        empty = bpy.data.objects.new(empty_name, None)
        context.collection.objects.link(empty)
        
        # Add the empty object to the dropdown list
        context.scene.parent_object = empty
        
        return {'FINISHED'}

class OBJECT_OT_lazy_parent(bpy.types.Operator):
    """Lazy Parent Selected Objects to Chosen Object"""
    bl_idname = "object.lazy_parent"
    bl_label = "Lazy Parent"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        parent_object = context.scene.parent_object
        if not parent_object:
            self.report({'WARNING'}, "No parent object selected")
            return {'CANCELLED'}
        
        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}
        
        for obj in selected_objects:
            if obj != parent_object:
                obj.parent = parent_object
        
        return {'FINISHED'}

class OBJECT_PT_easy_lazy_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Easy Lazy"
    bl_idname = "OBJECT_PT_easy_lazy"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Easy Lazy'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.label(text="Multi Rename", icon='SORTALPHA')
        layout.prop(scene, "multi_rename_base_name")
        layout.operator(OBJECT_OT_multi_rename.bl_idname)
        
        layout.separator()
        layout.separator()
        
        layout.label(text="Lazy Parent", icon='CONSTRAINT')
        layout.prop_search(scene, "parent_object", scene, "objects", text="Parent Object")
        layout.operator(OBJECT_OT_lazy_parent.bl_idname)
        
        layout.operator(OBJECT_OT_create_empty_and_add_to_list.bl_idname, text="(+) Create Empty")
        layout.prop(scene, "empty_name")

def register():
    bpy.utils.register_class(OBJECT_OT_multi_rename)
    bpy.utils.register_class(OBJECT_OT_create_empty_and_add_to_list)
    bpy.utils.register_class(OBJECT_OT_lazy_parent)
    bpy.utils.register_class(OBJECT_PT_easy_lazy_panel)
    
    bpy.types.Scene.multi_rename_base_name = bpy.props.StringProperty(
        name="Base Name",
        description="Base name for the objects",
        default="Object"
    )
    bpy.types.Scene.parent_object = bpy.props.PointerProperty(
        name="Parent Object",
        type=bpy.types.Object,
        description="Object to parent selected objects to"
    )
    bpy.types.Scene.empty_name = bpy.props.StringProperty(
        name="Empty Name",
        description="Name of the empty object",
        default="Empty"
    )

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_multi_rename)
    bpy.utils.unregister_class(OBJECT_OT_create_empty_and_add_to_list)
    bpy.utils.unregister_class(OBJECT_OT_lazy_parent)
    bpy.utils.unregister_class(OBJECT_PT_easy_lazy_panel)
    
    del bpy.types.Scene.multi_rename_base_name
    del bpy.types.Scene.parent_object
    del bpy.types.Scene.empty_name

if __name__ == "__main__":
    register()
