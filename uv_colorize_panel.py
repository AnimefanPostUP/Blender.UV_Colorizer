import bpy
import os
import bmesh
import math
from random import uniform
from .uv_colorize_palette_picker import palette_picker
from .__init__ import bl_info
from enum import Enum
from bpy.types import Menu


import gpu
import bgl
import blf
import json
import subprocess
import mathutils
from mathutils import Matrix

#Using Following Addons: Bookmarks, Outline Map, Fold Plus


debugname="UV_COLORIZE" #Long Name in Logs
#region <Globalvars> <Operator>
debugshort="UVC" #Shortname in Log, in Logs of normal Functions
debugcounter=0 #Counts Columns
deeplog=True #Toggles if anything should be displayed
#endregion <Globalvars>   

#region <Logging> <Debug>

class LOGTYPE(Enum):
    #Types
    UI="UI"
    FUNCTION="FUNCTION"

    #Subtypes Startcall
    ONECALL = "ONECALL"
    START = "START"

    #Subtype Exitcall
    FINISH = "FINISH"
    SKIP = "SKIP"
    ERROREXIT = "<ERROREXIT>"

    #Subtype Comment
    INFO = "<I>"
    ACTION = "<A>"
    WARNING = "<!>"
    ERROR="<ERROR>"

    #Subtype Commend Smallfunction In/Out-Put
    IN="IN"
    OUT="OUT"

    NOTYPE = "NOTYPE"
  
def printLog( src="", type=LOGTYPE.FUNCTION, msg="", subtype= LOGTYPE.NOTYPE):

    outputmessage=""

    """ !METHOD!
    Sets the Text of the Errormessage, used by the Error Function
    
    Keyword arguments:
    :param str src:                     Source of Log
    :param LOGTYPE type:                TYPE OF LOG, Usually FUNCTION, or something alse
    :param str msg:                     Message to Print
    :param LOGTYPE subtype:             Subtype defines the Way how to Print depending on the (Main)Type
    """
    global debugcounter
        
    if type is LOGTYPE.FUNCTION :
        outputmessage=outputmessage+debugshort+"<F>"+" - "+src
        if subtype in {LOGTYPE.START, LOGTYPE.FINISH, LOGTYPE.SKIP, LOGTYPE.ERROREXIT, LOGTYPE.ONECALL}:
            debugcounter=0
            outputmessage=outputmessage+"_"+str(subtype.value)
            if msg != "":
                outputmessage=outputmessage+" : ( "+msg+" )  \n"
        if deeplog:
            if subtype in {LOGTYPE.INFO, LOGTYPE.ACTION, LOGTYPE.WARNING, LOGTYPE.ERROR, LOGTYPE.IN, LOGTYPE.OUT}:
                debugcounter += 1
                outputmessage=outputmessage+" ["+str(subtype.value)+"]"
                if msg != "":
                    outputmessage=str(debugcounter)+"> \t"+outputmessage+"\t"+msg

    if type is LOGTYPE.UI :
        outputmessage=outputmessage+debugshort+"<UI> debug: "+msg
        debugcounter=0

    print(outputmessage) 
    


#endregion <Logging>    

# ==================================================================================
# ||                               MainPanels                                     ||
# ==================================================================================
# || Description: Color Display Panel and the Palette Panel                       ||
# ==================================================================================

#create a new panel PANELclass

#Tools Section
'''

class uvc_extratoolpanel():
    """ %PANEL%
    Drawing the Colors and eventually Displayoption Buttons in Future
    """
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "UV Colorize"
    bl_options = {"DEFAULT_CLOSED"}
 
#Core Menu    
class extratool_PT_panel(uvc_extratoolpanel, bpy.types.Panel):
    """ %PANEL%
    Drawing the Colors and eventually Displayoption Buttons in Future
    """
    bl_idname = "UVC_PT_extratools"
    bl_label = "Extra Tools"
     
    def draw(self, ctx):
        layout = self.layout

#Pivotsetter
class UVC_PT_extratools_1(uvc_extratoolpanel, bpy.types.Panel):
    bl_label = "Pivot Setter"
    bl_parent_id = "UVC_PT_extratools"
    
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        settingsdata=bpy.context.scene.uv_palettes_settings_data

        box = layout.box() #NEW BOX
        box.label(text="Set Pivot")     
        row=box.row()   
        box.label(text="Top/Bottom are Z Axies")  
        row=box.row()   
        box.label(text="in Z/Z- mode its the Y Axies")  
        
        row.prop(settingsdata, "direction", expand=True) 
        row=box.row()    
        row.prop(settingsdata, "transformspace", expand=True) 
        row=box.row()    
        
        op=row.operator(UVC_Operator_setOrigin.bl_idname, text="", icon="RADIOBUT_ON")
        op.height="tl"
        op.direction=settingsdata.direction
        op.transformspace=settingsdata.transformspace
        op=row.operator(UVC_Operator_setOrigin.bl_idname, text="", icon="TRIA_UP")
        op.height="tm"
        op.direction=settingsdata.direction
        op.transformspace=settingsdata.transformspace
        op=row.operator(UVC_Operator_setOrigin.bl_idname, text="", icon="RADIOBUT_ON")
        op.height="tr"
        op.direction=settingsdata.direction
        op.transformspace=settingsdata.transformspace
        row=box.row()    
        
        op=row.operator(UVC_Operator_setOrigin.bl_idname, text="", icon="TRIA_LEFT")
        op.height="ml"
        op.direction=settingsdata.direction
        op.transformspace=settingsdata.transformspace
        op=row.operator(UVC_Operator_setOrigin.bl_idname, text="", icon="RADIOBUT_ON")
        op.height="mm"
        op.direction=settingsdata.direction
        op.transformspace=settingsdata.transformspace
        op=row.operator(UVC_Operator_setOrigin.bl_idname, text="", icon="TRIA_RIGHT")
        op.height="mr"
        op.direction=settingsdata.direction
        op.transformspace=settingsdata.transformspace
        row=box.row()    
        
        op=row.operator(UVC_Operator_setOrigin.bl_idname, text="", icon="RADIOBUT_ON")
        op.height="bl"
        op.direction=settingsdata.direction
        op.transformspace=settingsdata.transformspace
        op=row.operator(UVC_Operator_setOrigin.bl_idname, text="", icon="TRIA_DOWN")
        op.height="bm"
        op.direction=settingsdata.direction
        op.transformspace=settingsdata.transformspace
        op=row.operator(UVC_Operator_setOrigin.bl_idname, text="", icon="RADIOBUT_ON")
        op.height="br"
        op.direction=settingsdata.direction
        op.transformspace=settingsdata.transformspace
        row=box.row()    
        
        op=row.operator(UVC_Operator_setOrigin.bl_idname, text="Average")
        op.height="ct"
        op.direction=settingsdata.direction
        op.direction=settingsdata.direction
        row=box.row()    
  
#Rotationrool        
class UVC_PT_extratools_2(uvc_extratoolpanel, bpy.types.Panel):
    bl_label = "Rotationtool"
    bl_parent_id = "UVC_PT_extratools"
    
    
    def draw(self, context):
        layout = self.layout

        box = layout.box() #NEW BOX
        box.label(text="Rotationclip:")   
        row=box.row()   
        op=row.operator(UVC_Operator_clipRotation.bl_idname, text="Clip by 15°")
        row=box.row()   
        
        layout.row().separator()
        box.label(text="Quickrotate:")   
        row=box.row()   
        op=row.operator(UVC_Operator_rotate90DegL.bl_idname, text="Rotate L")
        row=box.row()   
        op=row.operator(UVC_Operator_rotate90DegR.bl_idname, text="Rotate R")
        row=box.row()   

#Autosmooth        
class UVC_PT_extratools_3(uvc_extratoolpanel, bpy.types.Panel):
    bl_label = "Autosmooth"
    bl_parent_id = "UVC_PT_extratools"
    
    
    def draw(self, context):
        layout = self.layout
        box = layout.box() #NEW BOX
        row=box.row()
        
        settingsdata = bpy.context.scene.uv_palettes_settings_data
        
        row.prop(settingsdata, "autosmooth", expand=True, text="Autosmooth")  
        row.prop(settingsdata, "cleanSplitNormals", expand=True, text="Set Clear")

        
        box.label(text="Split Normals by Degree:")   
        row=box.row()   
        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="15").angle=5
        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="20").angle=15
        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="25").angle=25
        row=box.row()  
        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="30").angle=30
        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="35").angle=35
        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="40").angle=40
        row=box.row()  
        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="45").angle=45
        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="50").angle=50
        op=row.operator(UVC_Operator_splitnormals.bl_idname, text="55").angle=55
        
        row = box.row()
        row.label(text="Active(!) Smoothing Angle:")  
        row.prop(settingsdata, "splitangle", text="" , slider=True)

'''

class uvc_panel():
    """ %PANEL%
    Drawing the Colors and eventually Displayoption Buttons in Future
    """
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "UV Colorize"
    bl_options = {"DEFAULT_CLOSED"}
 
#Core Menu    
class UVC_PT_data_panel(uvc_panel, bpy.types.Panel):
    """ %PANEL%
    Drawing the Colors and eventually Displayoption Buttons in Future
    """
    bl_idname = "UVC_PT_colors"
    bl_label = "UVC Menu"
     
    def draw(self, ctx):
        layout = self.layout


def get_current_Vertcount():
    """ !FUNCTION!
    Returns the Amount of Vertices in the Current Mesh
    
    :return: Amount of Vertices in the Current Mesh
    :rtype: int
    """
    functionname="GETCURRENTVERTCOUNT"
    mesh = bpy.context.object.data
    if mesh:
        return len(mesh.vertices)
    else:
        return 0

#Color         
class UVC_PT_color_panel(uvc_panel, bpy.types.Panel):
    """ %PANEL%
    Drawing the Colors and eventually Displayoption Buttons in Future
    """
    bl_label = "Color"
    bl_parent_id = "UVC_PT_colors"


    
    def draw(self, ctx):

        functionname="COLORPANELDRAW"

        layout = self.layout
        settingsdata=ctx.scene.uv_palettes_settings_data
        palette = return_CurrentPalette()
        
        spacing= settingsdata.gridspacing
        
        
        
        paletteStatus=availabilityCheck(palette)
        paletteNotNone=paletteStatus["Palette"]
        paletteLoaded=paletteStatus["Loaded"]
        paletteImageSet=paletteStatus["Image"] 
        paletteHasColors=paletteStatus["Colors"]
        paletteHasGroups=paletteStatus["Groups"]
        paletteDefaultMaterial=paletteStatus["DefaultMaterial"]
        paletteNotNone=paletteStatus["paletteNotNone"]
                      

        #WARNING yes this code is still messy...
        if  paletteNotNone and paletteHasColors and paletteLoaded:
            # Accessing integer properties
            tile_count_x = palette.p_tilecountx
            tile_count_y = palette.p_tilecounty   
                
            showSelection = settingsdata.showSelection         
            selectedColor=-1
            
            if (showSelection):
                
                print ("change detected")
                majority_segment = uv_Tilenumber_By_Active_Face_UV(ctx, palette)
                if(majority_segment):
                    selectedColor= math_getIndexByTile(majority_segment[0],majority_segment[1],tile_count_x)

  
                    
                
            row = layout.row()
            row.operator(UVC_Operator_Settings_accessSettingsView.bl_idname, text="", icon="SETTINGS").menuname="colorpanel"
        
            
            if(settingsdata.settingsmenu=="colorpanel" and settingsdata.showSettings):        
                box = layout.box()
                row = box.row()

                row.operator(UVC_Operator_Settings_return.bl_idname, text="Close", icon="X")   
                
                row.prop (settingsdata, "gridspacing", text="Spacing", slider=True)
                row = box.row()
                
                row.prop (settingsdata, "showSelection", text="Display Seletion", slider=True)
                row = box.row()
                
                row.prop(settingsdata, "panelGridType",  expand=True)

            # Draw the elements in different Shapes
            

            if settingsdata.panelGridType == "ordered":
                # upperlayout = box
                # layoutposition = upperlayout.row(align=True)        
                upperlayout = layout.grid_flow(row_major=True, columns=tile_count_x*2  if palette.p_editcolorgroups else tile_count_x, even_columns=True, even_rows=True)  
                upperlayout
                upperlayout.scale_x = spacing
                upperlayout.scale_y = spacing
                layoutposition = upperlayout     
            else:   
                upperlayout = layout.grid_flow(row_major = True, even_columns = True, even_rows = True)
                layoutposition = upperlayout
            
            trig=False
                    
            for yt in reversed(range(tile_count_y)):               
                for xt in range(tile_count_x):
                    
                    index=img_getTilesetPixelIndex(xt, yt, tile_count_x)
                    
                    if (showSelection):   
                        if( index == selectedColor):
                            layoutposition = upperlayout.box()
                            trig=True

                    if 0 <= index < len(palette.colors): 
                        item = palette.colors[index]        
                        
                        if gf_Col_isHidden(palette, index) or palette.p_editcolorgroups: #if Color is hidden (inverted) show dummy unless in Editmode
                            
                            interactionicon="HIDE_OFF"

                            if palette.colorgroups[palette.selectedcolorgroup].colorgroupdata[index].state: #Set Icon for Group Edit
                                interactionicon="LOCKED"
                            else:
                                interactionicon="UNLOCKED" 
                                                       
                                                                                    
                            layoutposition.prop(item, "active", icon_value=layout.icon(item.icon), icon_only=True, emboss=False, index=index, expand=False) #Standard Color Prop
                         
                            if(palette.p_editcolorgroups) and paletteHasGroups and paletteLoaded:
                                    layoutposition.prop(palette.colorgroups[palette.selectedcolorgroup].colorgroupdata[index], "state", index=index, text=f"",icon=interactionicon) #Group Edit Prop

                        else: #if Color is hidden        
                            layoutposition.label(text="", icon="SELECT_SET")  
                            
                              
                        if trig:
                            layoutposition = upperlayout     
                            trig=False
                            
                           

    
    
                #else:
                    #print(f"No Colors!")
                    #printLog(src=functionname,type=LOGTYPE.UI ,subtype=LOGTYPE.ERROR,msg="No Colors!")

#Palettes
class UVC_PT_colorize_panel(uvc_panel, bpy.types.Panel):

    """ %PANEL%
    usage: Panel to Display Elements for Managing the Palettes
    """
    bl_idname = "UVC_PT_palettepanel"
    bl_label = "Palettes"
    bl_parent_id = "UVC_PT_colors"


    def draw(self, ctx):
        layout = self.layout

        palette = return_CurrentPalette()
        settingsdata=ctx.scene.uv_palettes_settings_data
        
        paletteStatus=availabilityCheck(palette)
        paletteNotNone=paletteStatus["Palette"]
        paletteLoaded=paletteStatus["Loaded"]
        paletteImageSet=paletteStatus["Image"] 
        # paletteHasColors=paletteStatus["Colors"]
        # paletteHasGroups=paletteStatus["Groups"]
        # paletteDefaultMaterial=paletteStatus["DefaultMaterial"]
        paletteNotNone=paletteStatus["paletteNotNone"]

        displaySettings=False       

        if(settingsdata.settingsmenu=="panellist" and paletteNotNone and settingsdata.showSettings):
            displaySettings=True  

    #Frontpart of the Menu Looks different depending on if theres none,  1 , > 1,  Palettes
        
        box = layout.box()
        row = box.row()    
        
        
        if paletteNotNone:
            
            if(len(bpy.context.scene.uv_palettes)<2):
                
                if(palette.img):
                    row.popover(palette_picker.bl_idname, text='', translate=True, icon_value=layout.icon(palette.img))
                    row.label(text=""+palette.img.name)
                else:
                    row.popover(palette_picker.bl_idname, text='Select Image', translate=True, icon="ERROR")
                    row.label(text="...")
                        
            else:
                row.template_list("UVC_UL_colors", "", ctx.scene, "uv_palettes", ctx.scene, "uv_palettes_index")    
        else:
            row.operator(UVC_Operator_Palette_add.bl_idname, text="[Setup] Add Palette", icon="PLUS") 

        #row.label(text="")#Spacer
        
    

        #Buttons for Adding, Removing and Loading/Unloading
        
        
        row = layout.row()
            
        # if(not (settingsdata.showAddbutton_Panel and settingsdata.showDeletebutton_Panel and settingsdata.showAddbutton_Colorgroup and settingsdata.showDeletebutton_Colorgroup)):
        #     row.label(text="Some Options Hidden (Settings)")



 
        if(paletteNotNone and not displaySettings):
            row.operator(UVC_Operator_Settings_accessSettingsView.bl_idname, text="Editmode", icon="SETTINGS").menuname="panellist"   
        else:
            
      
            
            if(displaySettings):
                row.operator(UVC_Operator_Settings_return.bl_idname, text="Close", icon="X")
                row = layout.row()
                
            if(displaySettings):
                row.operator(UVC_Operator_Palette_add.bl_idname, text="Add Palette", icon="PLUS")   
                row = layout.row()      
                
        if(displaySettings and paletteNotNone):
            row.operator(UVC_Operator_Palette_remove.bl_idname, text="Remove Selected", icon="TRASH")
            row = layout.row()
            row.operator(UVC_Operator_Palette_update.bl_idname, text="Reload Palette", icon="FILE_REFRESH")

        #Settings for loading          
        
        if  paletteNotNone and paletteImageSet:#Check if Palette is Written            
            
            if not paletteLoaded:
                  
                row.operator(UVC_Operator_Palette_update.bl_idname, text="Load", icon="TEXTURE")
                row.prop(settingsdata, "convertColorspace", text="fix sRGB")
                row = layout.row(align=True)
                row.prop(palette, "pe_tilecountx", text="X TileCount ")
                row.prop(palette, "pe_tilecounty", text="Y TileCount ")
                #INSERT HERE UID 934820

                

            row=layout.separator()
            row=layout.separator()
             
        #Colorgroup Section below the Panel Management
         
        checkup=False
       
        if (palette):            
            if(paletteLoaded):    
                if(len(return_CurrentPalette().colorgroups)>0):
                        checkup=True
            # else:
            #     box = layout.box()
            #     row= box.row()
            #     if palette.img:
            #         row.label(text="Palette not Loaded!", icon="ERROR") 
            #     else:
            #         row.label(text="No Palette Image!", icon="ERROR")                    
        # else:       
        #     if(settingsdata.showPanels):
        #         box = layout.box()
        #         row=box.row()
        #         row.label(text="No Palette Created!", icon="ERROR")
        
        
        
        # Settingsmenu
        # if(displaySettings):
        #         box = layout.box()            
        #         box.label(text="Palette Settings:")
        #         row=box.row()
        #         row.prop(palette, "name", expand=True, icon="HIDE_OFF"if settingsdata.showDeletebutton_Panel else "HIDE_ON")
            
        
        

        
        if(not palette or displaySettings):
            box = layout.box()
            row=box.row()
            row.prop(settingsdata, "presetSubmenu", expand=True)


        if(settingsdata.presetSubmenu=="presetlist" and (displaySettings or not palette)):                 
            # #LoadPresets
            # if(len(settingsdata.settingspresets)<=0):
            #     refreshPresets(self, context)

                #Display Settings:
            
            box = layout.box()
            row=box.row()
            
            row.operator(UVC_Operator_Settings_openDirectoryDirectory.bl_idname, text="", icon="FILE_FOLDER")
            row.label(text="Palette Presets:")
            row=box.row()
            
            row=box.row()
            if len(settingsdata.settingspresets)>0:
                row.template_list("UVC_UL_presets", "", settingsdata, "settingspresets", settingsdata, "settingspresets_index")    
        
            row=box.row()
            if len(settingsdata.settingspresets)>0:
                row.operator(UVC_Operator_Settings_refreshPresets.bl_idname, text="Refresh", icon="FILE_REFRESH")
            else:
                row.operator(UVC_Operator_Settings_refreshPresets.bl_idname, text="Load", icon="FILE")
            if len(settingsdata.settingspresets)>0:
                row.operator(UVC_Operator_Settings_setPreset.bl_idname, text="Apply", icon="CHECKMARK")
                row=box.row()
                #row=box.row()
                #box.label(text=settingsdata.settingspresets[settingsdata.settingspresets_index].settingsFilename)
                
                if(settingsdata.showPresetLoadSettings):
                    row.prop(settingsdata, "showPresetLoadSettings", text="Loading Settings", icon="HIDE_OFF"if settingsdata.showPresetLoadSettings else "HIDE_ON")
                else:
                    row.prop(settingsdata, "showPresetLoadSettings", text="Show Settings", icon="HIDE_OFF"if settingsdata.showPresetLoadSettings else "HIDE_ON")


                if(settingsdata.showPresetLoadSettings):
                    row=box.row()
                    row.label(text="Loading Settings")

                    row=box.row()
                    row.label(text="Config Load Mode:")
                    row.prop(settingsdata,"importmode_Settigs", text="")

                    row=box.row()
                    row.label(text="Palette Load Mode:")
                    row.prop(settingsdata,"importmode_Palette", text="")

                    row=box.row()
                    if(settingsdata.importmode_Palette in ["groups_only","find","current"]):
                        row.label(text="May not be Applied in current Palette Load Mode)")

                    row.label(text="Groups Load Mode:")
                    row.prop(settingsdata,"importmode_Groups", text="")

                    row=box.row()
                    row.label(text="Image Import Mode:")
                    row.prop(settingsdata,"importmode_Image", text="")

                    row=box.row()
                    row.label(text="Image Load Mode:")
                    row.prop(settingsdata,"importmode_Image_setImage", text="")
            

        if(settingsdata.presetSubmenu=="import" and (displaySettings or not palette)): 

            box = layout.box()
            row=box.row()
            
            
            box.label(text="Import Preset:")
            row=box.row()
            row.operator(UVC_Operator_Settings_importPreset.bl_idname, text="Import", icon="CONSOLE")


            
            if(settingsdata.settingsPathPre != ""):
                row=box.row()
                row.label(text=settingsdata.settingsPathPre)

        if(settingsdata.presetSubmenu=="export" and (displaySettings or not palette)): 

            box = layout.box()
            row=box.row()
            row.operator(UVC_Operator_Settings_openDirectoryDirectory.bl_idname, text="", icon="FILE_FOLDER")
            row.label(text="Export (to addons Folder):")

            row=box.row()          
            row.label(text="Preset Name:")
            row=box.row()  
            row.prop(settingsdata,"settingsTitle", text="")
            
            row=box.row()
            row.label(text="Include in Export:")
            
            row=box.row()
            row.prop(settingsdata,"export_Settings", text="Config", toggle=True)
            row.prop(settingsdata,"export_Palette", text="Current Palette", toggle=True)
            row.prop(settingsdata,"export_Image", text="Image", toggle=True)
            row=box.row()
            row.label(text="imageExportMode")
            row=box.row()
            row.prop(settingsdata, "imageExportMode", text="")

            row=box.row()
            row.operator(UVC_Operator_Settings_savesettings.bl_idname, text="Save Current", icon="CURRENT_FILE")    

#Groups  
class UVC_PT_group_panel(uvc_panel, bpy.types.Panel):

    """ %PANEL%
    usage: Panel to Display Elements for Managing the Palettes
    """
    bl_idname = "UVC_PT_grouppanel"
    bl_label = "Groups"
    bl_parent_id = "UVC_PT_colors"
    

    def draw(self, ctx):
        layout = self.layout

        palette = return_CurrentPalette()
        settingsdata=ctx.scene.uv_palettes_settings_data
        
        paletteStatus=availabilityCheck(palette)
        #paletteNotNone=paletteStatus["Palette"]
        paletteLoaded=paletteStatus["Loaded"]
        # paletteImageSet=paletteStatus["Image"] 
        # paletteHasColors=paletteStatus["Colors"]
        # paletteHasGroups=paletteStatus["Groups"]
        # paletteDefaultMaterial=paletteStatus["DefaultMaterial"]
        # paletteNotNone=paletteStatus["paletteNotNone"]
        

    #Frontpart of the Menu Looks different depending on if theres none,  1 , > 1,  Palettes
        
        #Colorgroup Section below the Panel Management
         
        checkup=False
       
        if (palette):        
            if(paletteLoaded):    
                if(len(return_CurrentPalette().colorgroups)>0):
                        checkup=True


                # ====================MASKEDITOR====================
                box=layout.box()
                grid = box.column_flow(columns = 0, align=True) #create box for colorgroupeditor  
                row=grid.row()
                row.label(text="Group Menu:")

                if(len(return_CurrentPalette().colorgroups)>0):  
                    grid.scale_y = 1.2
                    grid.template_list("UVC_UL_colorgroups", "", palette, "colorgroups", return_CurrentPalette(), "selectedcolorgroup")
                    row=grid.row()
                #layout.label(text="Load to see more Options!",) 
                #grid.label(text="Colorgroups:")                    

                if(settingsdata.showColorgroupList_LayerOperation):
                    row=grid.row()
                    row.prop(palette, "colorgroupLayermode", expand=True)

                row=grid.row()
                
                if(palette.p_editcolorgroups):
                    row.operator(UVC_Operator_Palette_colorgroup_add.bl_idname, text="", icon="PLUS") 
                    
                if(len(return_CurrentPalette().colorgroups)>0):
                    checkup=True
                    currentcolorgroup=palette.colorgroups[palette.selectedcolorgroup]

                    if(palette.p_editcolorgroups):
                        
                        row.operator(UVC_Operator_Palette_colorgroup_config.bl_idname, text="Exit Edit", icon="X")
                        
                    else:
                        row.operator(UVC_Operator_Palette_colorgroup_config.bl_idname, text="Editmode", icon="SETTINGS")
                        
                    if(palette.p_editcolorgroups):
                        row.operator(UVC_Operator_Palette_colorgroup_remove.bl_idname, text="", icon="TRASH")
           
        
        if(checkup):    #More Options for Groups in Editmode
            currentcolorgroup=palette.colorgroups[palette.selectedcolorgroup]  
            if(palette.p_editcolorgroups):
                box=layout.box()
                row=box.row()

                row.prop(currentcolorgroup,"title")            

                #TITLE
                row=box.row() 
                row.prop(settingsdata, "advancedSettings", text="", icon="OPTIONS")
                row.prop(settingsdata, "showgroupsOtherSettings", text="Show Options", icon="COLLAPSEMENU")
                
                row=box.row()
                if(settingsdata.advancedSettings):
                    #Setting to Show AlwaysActive and Invert in UI
                    box = layout.box()     
                    box.label(text="Colorgroup Activation:", icon="FILTER")
                    row=box.row()
                    row.label(text="", icon="LOCKED")
                    row.prop(settingsdata, "showColorgroupList_alwaysActive", text="Always Active", icon="HIDE_OFF"if settingsdata.showColorgroupList_alwaysActive else "HIDE_ON")
                    row.separator
                    row.label(text="", icon="CLIPUV_DEHLT")
                    row.prop(settingsdata, "showColorgroupList_inverted", text="Invert", icon="HIDE_OFF"if settingsdata.showColorgroupList_inverted else "HIDE_ON")
                    

                    box = layout.box()     
                    box.label(text="Operationmode is either AND/OR:", icon="CON_SIZELIMIT")
                    row=box.row()
                    row.label(text="", icon="HIDE_OFF")
                    row.prop(settingsdata, "showColorgroupList_LayerOperation", text="Layer Operation", icon="HIDE_OFF"if settingsdata.showColorgroupList_LayerOperation else "HIDE_ON")

                    box = layout.box()     
                    box.label(text="UI Options:", icon="WINDOW")
                    row=box.row()
                    #row.label(text="", icon="HIDE_OFF")
                    #row.prop(settingsdata, "showColorgroupList_lock", text="Disable Color", icon="HIDE_OFF"if settingsdata.showColorgroupList_lock else "HIDE_ON")
                    #Option to Hide Color
                    row.label(text="", icon="HIDE_OFF")
                    row.prop(settingsdata, "showColorgroupList_hideColors", text="Show Colors", icon="HIDE_OFF"if settingsdata.showColorgroupList_hideColors else "HIDE_ON")
                    

                if(settingsdata.showgroupsOtherSettings):
                    #Setting to Show Add to Colorwheel and Quickselect in UI
                    box = layout.box()      
                    box.label(text="Add To other Menus:", icon="PRESET_NEW")
                    row=box.row()
                    row.label(text="", icon="TPAINT_HLT")
                    row.prop(settingsdata, "showColorgroupList_addToColorwheel", text="Colorwheel", icon="HIDE_OFF"if settingsdata.showColorgroupList_addToColorwheel else "HIDE_ON") 
                    
                    row.label(text="", icon="COLOR")
                    row.prop(settingsdata, "showColorgroupList_addToColorshift", text="ColorShift", icon="HIDE_OFF"if settingsdata.showColorgroupList_addToColorshift else "HIDE_ON")
                    #Not Implemented!
                    #row.label(text="", icon="MENU_PANEL")
                    #row.prop(settingsdata, "showColorgroupList_addToQuickselect", text="Quickselect", icon="HIDE_OFF"if settingsdata.showColorgroupList_addToQuickselect else "HIDE_ON")


                    # box = layout.box()     
                    # box.label(text="Groupselect Behavior Between Masks", icon="MOD_MASK")
                    # row=box.row()
                    # row.label(text="", icon="SELECT_EXTEND")
                    # row.prop(settingsdata, "showColorgroupList_applyOnTool_Selection", text="Selection", icon="HIDE_OFF"if settingsdata.showColorgroupList_applyOnTool_Selection else "HIDE_ON")
                    # row.label(text="", icon="SELECT_INTERSECT")
                    # row.prop(settingsdata, "showColorgroupList_applyOnTool_Deselection", text="Deselection", icon="HIDE_OFF"if settingsdata.showColorgroupList_applyOnTool_Deselection else "HIDE_ON")

                
                  
                    
                #grid.label(text="Colorgroup Options:") 
                #Settings where here before but where moves to the colorgroup display
            # else:
            #     grid.label(text="Colorgroups") 
            


           
#Panel (settings)          
class UVC_Panel_Settings():
    """Displays the Settings of the ADDON, currently used for Implementing new Features to sort them in Later"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "UV Colorize"
    bl_options = {"DEFAULT_CLOSED"}
  
#Core    
class UVC_PT_Panel_0(UVC_Panel_Settings, bpy.types.Panel):
    """Displays the Settings of the ADDON, currently used for Implementing new Features to sort them in Later"""
    bl_idname = "UVC_PT_panel_settings"
    bl_label = "Toolbox"
        
    def draw(self, context):
        layout = self.layout
        row=layout.row()
        
        settingsdata=context.scene.uv_palettes_settings_data
        palette=return_CurrentPalette()
        
        checkup=False
 
        #use availabilityCheck to set the variables instead of direct access
        paletteStatus=availabilityCheck(palette)
        paletteNotNone=paletteStatus["Palette"]
        paletteLoaded=paletteStatus["Loaded"]
        paletteImageSet=paletteStatus["Image"] 
        paletteHasColors=paletteStatus["Colors"]
        paletteHasGroups=paletteStatus["Groups"]
        paletteDefaultMaterial=paletteStatus["DefaultMaterial"]
        paletteNotNone=paletteStatus["paletteNotNone"]
        
        textwidth=1.2
        
        

        if True:
            # if(not settingsdata.showSettings):
            #     #region <TOPBar> <UI>
                
            #     #Selection for which Main Menu Section to Show
            #     box = layout.box()    
            #     row = row=box.row() 
            #     row.prop(settingsdata, "settingsDisplay", expand=True)
            #     #endregion <TOPBar> 
                                                      
            #  # ====================Settings====================
            #  #Settings Banner
            
            '''
            
            if(settingsdata.showSettings):

                 #Sections
                box = layout.box()     
                row=box.row()
                if(settingsdata.settingsmenu=="panellist"): 
                    row.operator(UVC_Operator_Settings_return.bl_idname, text="Exit", icon="BACK")
                else:                  
                    row.operator(UVC_Operator_Settings_return.bl_idname, text="Return to Tools", icon="BACK")                
               
                # <<<<<<<<DISPLAY>>>>>>>>>>
                  
                if(settingsdata.showSettings):  
                    box = layout.box()     
                    row=box.row()           
                    row.operator(UVC_Operator_Settings_return.bl_idname, text="Close", icon="BACK")   
                    
                #Display Settings for Show Add/Delete Buttons
            '''
                
            # if(settingsdata.settingsmenu=="panellist"): 
            #     #Hide Palette Delete
            #     box = layout.box()              
            #     box.label(text="In Palette Edit Mode:", icon="QUESTION")
            #     row = box.row()   
            #     row.label(text="Tool Settings Are Restricted")
            #     row = box.row()   
            #     row.label(text="Click Exit to Leave Edit Mode")
                                    
            #     #rDisplay Settings for Color Panel and Colorwheel
            

    
            # if(settingsdata.settingsmenu=="colorwheel"):      
            #     #Colorwheel Displaymode
            #     box = layout.box()            
            #     box.label(text="Colorwheel Display:",icon="GROUP_VCOL")
            #     row=box.row()
            #     row.prop(settingsdata, "colorwheelDisplayType", expand=True)


            #  # ====================DEBUG====================              
            # if(settingsdata.settingsDisplay == "debug" and not settingsdata.showSettings):
            #     box = layout.box()

            #     box.label(text="Debug Options")
            #     row=box.row()
            #     row.operator(UVC_Operator_Settings_toggleLog.bl_idname, text="Toggle Deep_Logging", icon="HIDE_OFF"if deeplog else "HIDE_ON")

            #     row=box.row()
            #     row.operator(UVC_Operator_Settings_toggleConsole.bl_idname, text="Toggle Console", icon="CONSOLE")

            #     row=box.row()
            #     row.operator(UVC_Operator_Settings_printPath.bl_idname, text="Write Paths to Console", icon="CONSOLE")
                
            # # ====================Info====================
            
            # if(settingsdata.settingsDisplay == "info" and not settingsdata.showSettings):

            #     box = layout.box()
            #     box.label(text="Info:")
            #     row=box.row()
                
            #     row.label(text="Addon: "+bl_info["name"])
            #     row=box.row()
            #     row.label(text="Author: "+bl_info["author"])
            #     row=box.row()
            #     row.label(text="Edited by: Christian Schnoor")
            #     row=box.row()
            #     row.label(text="BlenderVer."+str(bl_info["blender"]))
            #     row=box.row()
            #     row.label(text="AddonVer."+str(bl_info["version"]))

            #     row=box.row()
            #     row=box.row()
            #     row.label(text="Guides can be Found in the Addons Files")
            #     row=box.row()
            #     row.label(text="Use Debug Menu to get there")
 
#Menus       
class UVC_PT_Panel_1(UVC_Panel_Settings, bpy.types.Panel):
    """Displays the Settings of the ADDON, currently used for Implementing new Features to sort them in Later"""
    bl_label = "Menus"
    bl_parent_id = "UVC_PT_panel_settings"


    def draw(self, context):
        layout = self.layout
        box=layout.box()
        row=box.row()
        
        textwidth=1.3
        settingsdata=context.scene.uv_palettes_settings_data                
        #region <Toolmenu/Colorwheel> <Methods>  
        row.label(text="", icon="BLANK1")                        
        row.label(text="Tool Menus:")     
        row=box.row()   
                
        #row.label(text="", icon="BRUSHES_ALL")
        row.operator(UVC_Operator_Settings_accessSettingsView.bl_idname, text="", icon="SETTINGS").menuname="colorwheel"
        #row.label(text="", icon="BLANK1")
        col = row.column()
        col.scale_x = textwidth
        col.operator(UVC_Operator_Settings_openColorWheel.bl_idname, text="Colorwheel")   
        row.label(text=return_KeyBy_bl_id(UVC_Operator_Settings_openColorWheel.bl_idname))  

        row=box.row()
        #row.label(text="", icon="COLLAPSEMENU")
        row.label(text="", icon="BLANK1")
        #row.operator(UVC_Operator_Settings_accessSettingsView.bl_idname, text="", icon="SETTINGS").menuname="toolmenu"
        col = row.column()
        col.scale_x = textwidth
        col.operator(UVC_Operator_Settings_openToolMenu.bl_idname, text="Toolmenu")   
        row.label(text=return_KeyBy_bl_id(UVC_Operator_Settings_openToolMenu.bl_idname)) 
         
        if(settingsdata.showSettings and settingsdata.settingsmenu=="colorwheel"):
            box = layout.box()     
            row=box.row()           
            row.operator(UVC_Operator_Settings_return.bl_idname, text="Close", icon="X")   
                
            if(settingsdata.settingsmenu=="colorwheel"):      
                #Colorwheel Displaymode       
                box.label(text="Colorwheel Display:",icon="GROUP_VCOL")
                row=box.row()
                row.prop(settingsdata, "colorwheelDisplayType", expand=True)
        
        #endregion <return>    
                
#Select Tools       
class UVC_PT_Panel_2(UVC_Panel_Settings, bpy.types.Panel):
    """Displays the Settings of the ADDON, currently used for Implementing new Features to sort them in Later"""
    bl_label = "Select Tools"
    bl_parent_id = "UVC_PT_panel_settings"


    def draw(self, context):
        layout = self.layout
        box=layout.box()
        row=box.row()
        settingsdata=context.scene.uv_palettes_settings_data
        
        textwidth=1.3
        #region <Select by Color> <Methods>
                
        #row.operator(UVC_Operator_Settings_accessSettingsView.bl_idname, text="", icon="SETTINGS").menuname="selectcolor"
        row.label(text="", icon="BLANK1")
        row.label(text="By Active Color:")       
        row=box.row()
        
        row.prop(settingsdata, "setActiveColor_in_ToolMenu", expand=True, icon="PINNED"if settingsdata.setActiveColor_in_ToolMenu else "UNPINNED", icon_only=True)
        col = row.column()
        col.scale_x = textwidth
        col.operator(UVC_Operator_Settings_selectssimilar_operator.bl_idname, text="Select")
        row.label(text=return_KeyBy_bl_id(UVC_Operator_Settings_selectssimilar_operator.bl_idname));  

        row=box.row()

        row.prop(settingsdata, "deselectSimilar_in_ToolMenu", expand=True, icon="PINNED"if settingsdata.deselectSimilar_in_ToolMenu else "UNPINNED", icon_only=True)
        col = row.column()
        col.scale_x = textwidth
        col.operator(UVC_Operator_Settings_deselectssimilar.bl_idname, text="Deselect")
        row.label(text=return_KeyBy_bl_id(UVC_Operator_Settings_deselectssimilar.bl_idname));  
        row=box.row()
        
        #endregion <return>       

#Colorshift
class UVC_PT_Panel_3(UVC_Panel_Settings, bpy.types.Panel):
    """Displays the Settings of the ADDON, currently used for Implementing new Features to sort them in Later"""
    bl_label = "Colorshift"
    bl_category = "UV Colorize"
    bl_idname = "UVC_PT_panel_settings_3"
    bl_parent_id = "UVC_PT_panel_settings"
    bl_space_type = 'VIEW_3D'


    def draw(self, context):
        
        layout = self.layout
        box=layout.box()
        row=box.row()
        settingsdata=context.scene.uv_palettes_settings_data
        textwidth=1.3
        
        #row.operator(UVC_Operator_Settings_accessSettingsView.bl_idname, text="", icon="SETTINGS").menuname="colorshift"
        row.label(text="", icon="BLANK1")
        row.label(text="Color Shift:")        
        row=box.row()   
            
        row.prop(settingsdata, "colorshiftUp_in_ToolMenu", expand=True, icon="PINNED"if settingsdata.colorshiftUp_in_ToolMenu else "UNPINNED", icon_only=True)
        col = row.column()
        col.scale_x = textwidth
        col.operator(UVC_Operator_ColorshiftUp.bl_idname, text="Next Color")
        row.label(text=return_KeyBy_bl_id(UVC_Operator_ColorshiftUp.bl_idname));  
        
        row=box.row()
        row.prop(settingsdata, "colorshiftDown_in_ToolMenu", expand=True, icon="PINNED"if settingsdata.colorshiftDown_in_ToolMenu else "UNPINNED", icon_only=True)
        col = row.column()
        col.scale_x = textwidth
        col.operator(UVC_Operator_ColorshiftDown.bl_idname, text="Previous Color")
        row.label(text=return_KeyBy_bl_id(UVC_Operator_ColorshiftDown.bl_idname));  

#Set Default
class UVC_PT_Panel_4(UVC_Panel_Settings, bpy.types.Panel):
    """Displays the Settings of the ADDON, currently used for Implementing new Features to sort them in Later"""
    bl_label = "Set Default Mat/Tex"
    bl_parent_id = "UVC_PT_panel_settings"


    def draw(self, context):
        
        layout = self.layout
        box=layout.box()
        row=box.row()
        settingsdata=context.scene.uv_palettes_settings_data
        textwidth=1.3
        
        #row.operator(UVC_Operator_Settings_accessSettingsView.bl_idname, text="", icon="SETTINGS").menuname="colorshift"
        row.label(text="Set Material:")        
        row=box.row()   
        
        palette=return_CurrentPalette()
        if(palette):
        
            row=box.row()
            #row.operator(UVC_Operator_Settings_accessSettingsView.bl_idname, text="", icon="SETTINGS").menuname="setdefaulttexture"
            # row.label(text="", icon="REMOVE")
            # row.prop(settingsdata, "showSetTexture", expand=True, icon="PINNED"if settingsdata.showSetTexture else "UNPINNED", icon_only=True)
            # row.operator(UVC_Operator_Settings_addPaletteTexture.bl_idname, text="Add Palette Texture").byOperator=True
            # row.label(text=return_KeyBy_bl_id(UVC_Operator_Settings_addPaletteTexture.bl_idname));  

            row=box.row()
            row.operator(UVC_Operator_Settings_accessSettingsView.bl_idname, text="", icon="SETTINGS").menuname="setdefaultmaterial"
            row.prop(settingsdata, "setDefaultMaterial_in_ToolMenu", expand=True, icon="PINNED"if settingsdata.setDefaultMaterial_in_ToolMenu else "UNPINNED", icon_only=True)
            row.operator(UVC_Operator_Settings_addDefaultmaterial.bl_idname, text="Add Default Material").byOperator=True
            row.label(text=return_KeyBy_bl_id(UVC_Operator_Settings_addDefaultmaterial.bl_idname));  
            row=box.row()
            row.label(text="", icon="BLANK1")
            row.label(text="", icon="BLANK1")
            row.prop(palette, "defaultmaterial", text="")
            row.label(text="Default Mat");  

        else: #LL232
            row=box.row()
            row.label(text="No Palette added");  
            row=box.row()
            row.label(text="Some options are Hidden", icon="QUESTION"); 
            
        if(settingsdata.showSettings) and (settingsdata.settingsmenu=="setdefaultmaterial"):

                 #Sections
                box = layout.box()     
                row=box.row()           
                row.operator(UVC_Operator_Settings_return.bl_idname, text="Close", icon="X")
                
                if(settingsdata.settingsmenu=="setdefaultmaterial"):      
                    
                    #Material Mode, how when or how Materials are added when setting Colors or so
                    row=box.row()
                    box.label(text="How Materials are added on SetColor / Tool:", icon="NEWFOLDER")
                    
                    row=box.row()
                    row.prop(settingsdata, "defaultMaterialSetMode", expand=True)   

                    row=box.row()
                    row.label(text="Empty Slots Action:", icon="NODE")
                    row=box.row()
                    row.prop(settingsdata, "emptySlotAction", expand=True)
 
#Set Color Tools                                        
class UVC_PT_Panel_5(UVC_Panel_Settings, bpy.types.Panel):
    """Displays the Settings of the ADDON, currently used for Implementing new Features to sort them in Later"""
    bl_label = "Set Color Tools"
    bl_parent_id = "UVC_PT_panel_settings"


    def draw(self, context):
        layout = self.layout
        box=layout.box()
        row=box.row()
        settingsdata=context.scene.uv_palettes_settings_data
        
        textwidth=1.3
        #region <Select by Color> <Methods>

        row.operator(UVC_Operator_Settings_accessSettingsView.bl_idname, text="", icon="SETTINGS").menuname="selectcolor"
        row.label(text="By Active Color:")       
        row=box.row()
        
        #row.prop(settingsdata, "UVC_Operator_Settings_setColorBySelected", expand=True, icon="PINNED"if settingsdata.selectSimilar_in_ToolMenu else "UNPINNED", icon_only=True)
        row.label(text="", icon="BLANK1")
        col = row.column()
        col.scale_x = textwidth
        col.operator(UVC_Operator_Settings_setColorBySelected.bl_idname, text="Select")  
        row.label(text=return_KeyBy_bl_id(UVC_Operator_Settings_setColorBySelected.bl_idname));  

        # row=box.row()

        # #row.prop(settingsdata, "deselectSimilar_in_ToolMenu", expand=True, icon="PINNED"if settingsdata.deselectSimilar_in_ToolMenu else "UNPINNED", icon_only=True)
        # col = row.column()
        # col.scale_x = textwidth
        # col.operator(UVC_Operator_Settings_setColorBySelected.bl_idname, text="Deselect")
        # row.label(text=return_KeyBy_bl_id(UVC_Operator_Settings_setColorBySelected.bl_idname));  
        # row=box.row()
        
        #endregion <return>    



# ==================================================================================
# ||                                    Lists                                     ||
# ==================================================================================
# || Description: Lists of Colorgroups and Panels                                       ||
# ==================================================================================

class UVC_UL_presets(bpy.types.UIList): #Sets actual Colors to Icons if the Grid Elements
    """ %LIST%
    usage: Displays the List of Palette Elements, is called in the "Colorize Panel"
    """
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.label(text=item.settingsFilenameOnly) 

class UVC_UL_colors(bpy.types.UIList): #Sets actual Colors to Icons if the Grid Elements
    """ %LIST%
    usage: Displays the List of Palette Elements, is called in the "Colorize Panel"
    """
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        selectedpalette = return_CurrentPalette()
        palette=item


        paletteNotNone =False
        paletteLoaded =False
        paletteImageSet=False       
        paletteHasColors=False
        
        if  palette is not None:
            paletteNotNone=True
            if palette.img:
                paletteImageSet=True
                if palette.p_loaded:
                    paletteLoaded=True
                    if len(palette.colors) > 0:
                        paletteHasColors=True
                        

        if  selectedpalette == item: 
            if paletteImageSet: #set icon and text if image is present
                layout.popover(palette_picker.bl_idname, text='', translate=True, icon_value=layout.icon(item.img)) 
                layout.label(text=item.img.name) 
            else: #set icon and text if no image is present
                layout.popover(palette_picker.bl_idname, text='', translate=True, icon="ERROR")
                layout.label(text="<--Select Image")

        else: #If is not the selected image
            if paletteImageSet: #Set text
                layout.label(text=item.img.name, icon_value=layout.icon(item.img)) 
            else: #if no image set
                layout.label(text="No Texture")
 
            if paletteImageSet:   
                if not paletteLoaded:
                    row = layout.row()
                    layout.label(text="unloaded ")
                    
class UVC_UL_colorgroups(bpy.types.UIList): 
    """Displays a List containing the Colorgroups"""

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        
 
        palette=return_CurrentPalette()
        settingsdata=context.scene.uv_palettes_settings_data
        

        
        row=layout.row(align=True)

        #Icon if Group is (Disabled), (Selected), (Selected) and (Always Active) or (Not Selected and Always Active)
        
        
        if  item == palette.colorgroups[palette.selectedcolorgroup]: #If this the Selected Colorgroup
            row.label(text=item.title,icon= "PLUS"if item.alwaysActive else "RADIOBUT_ON")
                    
        else:     
            row.label(text=item.title, icon= "LAYER_ACTIVE"if item.alwaysActive else "LAYER_USED")

        
        #Always Active, Invert, Hide Color Buttons
             
        if(settingsdata.showColorgroupList_alwaysActive) : row.prop(item, "alwaysActive", icon="LOCKED"if item.alwaysActive else "UNLOCKED", icon_only=True) #Pinicon
        if(settingsdata.showColorgroupList_inverted) : row.prop(item, "inverted", icon="CLIPUV_DEHLT"if item.inverted else "CLIPUV_HLT", icon_only=True) #Colorgroupicon
        if(settingsdata.showColorgroupList_hideColors) : row.prop(item, "hideColors", icon="HIDE_OFF"if item.hideColors else "HIDE_ON", icon_only=True) #Eyeicon
        #if(settingsdata.showColorgroupList_lock) : row.prop(item, "lock", icon="HIDE_ON"if item.showColorgroupList_lock else "HIDE_OFF", icon_only=True) #Eyeicon
        

        
        #Add to Colorwheel or (doesnt Exist yet) Quickselection 
   
        #grid.label(text="Add Colorgroup to") 
        if(settingsdata.showColorgroupList_addToColorwheel) : row.prop(item, "addToColorwheel", icon="TPAINT_HLT"if item.addToColorwheel else "CHECKBOX_DEHLT", icon_only=True)
        if(settingsdata.showColorgroupList_addToColorshift) : row.prop(item, "addToColorshift", icon="RESTRICT_COLOR_ON"if item.addToColorshift else "RESTRICT_COLOR_OFF", icon_only=True)


        
        #Group Behavior Options for Select, Deselect and Colorshoft Tool
               
        # grid.label(text="Apply Colorgroup on Addon Tools:") 
        if(settingsdata.showColorgroupList_applyOnTool_Selection) : row.prop(item, "applyOnTool_Selection", icon="SELECT_EXTEND"if item.applyOnTool_Selection else "CHECKBOX_DEHLT", icon_only=True) #Selecticons
        if(settingsdata.showColorgroupList_applyOnTool_Deselection) : row.prop(item, "applyOnTool_Deselection", icon="SELECT_INTERSECT"if item.applyOnTool_Deselection else "CHECKBOX_DEHLT", icon_only=True)
  
preview_collections = {}

# ==================================================================================
# ||                                 Functions                                    ||
# ==================================================================================
# || Description: Internal Functions                                              ||
# ==================================================================================

#region <UI> <Methods>


def get_clockwise_mapping(num_elements):
    """Generate a clockwise mapping for the given number of elements."""
    if num_elements <= 0:
        return []
    
    # Define the fixed arrays
    fixed_mappings = {

        1: [0,1,2,3,4,5,6,7],
        2: [1,0,2,3,4,5,6,7],
        3: [2,0,1,3,4,5,6,7],
        4: [3,1,2,0,4,5,6,7],
        5: [3,1,2,0,4,5,6,7],
        6: [4,2,3,0,5,1,6,7],
        7: [5,2,3,0,6,1,4,7],
        8: [6,2,4,0,7,1,5,3]
    }
    
    # Return the mapping based on the number of elements
    return fixed_mappings.get(num_elements, [])

#endregion <UI>    

#region <Math> <Methods>

def linear_to_sRGB(linear_value):
    if linear_value <= 0.0031308:
        sRGB_value = 12.92 * linear_value
    else:
        sRGB_value = 1.055 * (linear_value ** (1/2.4)) - 0.055
    return sRGB_value

def math_UVPosition_By_Tile(xt, yt, tile_count_x, tile_count_y):
    
    """  !METHOD!
    Divides the UV into Tiles based on Tilecount and gets the Center Position of that Square

    Keyword arguments:
    :param int xt,yt:                       Squareposition
    :param: int tile_count_x,tile_count_y:  Amount of Squares per Axies
    :return: float uv_x, uv_y:              Postion on UV 0.0-1.0
    """

    
    uv_x = (xt / tile_count_x) + (0.5 / tile_count_x)
    uv_y = (yt / tile_count_y) + (0.5 / tile_count_y)
    
    #Add Debug Here?

    return uv_x, uv_y

def math_PixelIndex_By_TileNumber(xt, yt, width, height, tile_count_x, tile_count_y, uv_offset_x=0, uv_offset_y=0):
    """ !METHOD! 
    Uses the Sizes of the Texture, the Tilecount and Calculates the Index of the Pixel in the Array

    Keyword arguments:
    :param int xt,yt:                       Squareposition
    :param float width,height:              Size of Image
    :param: int tile_count_x,tile_count_y:  Amount of Squares per Axies
    :return: int index:                     index of Pixel inside a Array
    """
        
    mid_x = (xt * width // tile_count_x) + (width // tile_count_x // 2) + int(uv_offset_x)
    mid_y = (yt * height // tile_count_y) + (height // tile_count_y // 2) + int(uv_offset_y)
    index = (mid_y * width + mid_x) * 4

    functionname="CalculateMiddlePixel"

    printLog(src=functionname, msg="xt: " + str(xt) + " yt: " + str(yt) + " width: " + str(width) + " height: " + str(height) + " tile_count_x: " + str(tile_count_x) + " tile_count_y: " + str(tile_count_y) + " uv_offset_x: " + str(uv_offset_x) + " uv_offset_y: " + str(uv_offset_y), subtype=LOGTYPE.IN)
    printLog(src=functionname, msg="index: " + str(index), subtype=LOGTYPE.OUT)
     
    return index 
    
def math_getTileFromUVXY(tilecountx, tilecounty, x,y):    
    
    """ !METHOD!
    Calculates the Basetile from the Tilecount and the UV Coordinate

    Keyword arguments:
    xxx                       N/A #
    """


    segment_x = int(min(math.floor(x * tilecountx), tilecountx - 1))
    segment_y = int(min(math.floor(y * tilecounty), tilecounty - 1))
    #printLog(src="calculateSegment", subtype=LOGTYPE.INFO, msg="Segmentcoordinates"+str(segment_x)+"/"+str(segment_y)) 
    
    return segment_x,segment_y  
   
def math_getTileFromUV(tilecountx, tilecounty, uv):
    """ !METHOD!
    Calculates the Basetile from the Tilecount and the UV Coordinate

    Keyword arguments:
    xxx                       N/A #
    """



    segment_x = int(min(math.floor(uv.x * tilecountx), tilecountx - 1))
    segment_y = int(min(math.floor(uv.y * tilecounty), tilecounty - 1))
    #printLog(src="calculateSegment", subtype=LOGTYPE.INFO, msg="Segmentcoordinates"+str(segment_x)+"/"+str(segment_y)) 
    
    return segment_x,segment_y  

def img_readPixel_By_Index(img, index):
    """ !METHOD!
    Gets the Color of a Pixel inside a Pixel Array of an Image

    Keyword arguments:
    :param Image img:                       Image to get the Pixel From
    :return: int[4] index:                  4 Pixels representing RGBA
    """
    return img.pixels[index:index + 4]

def readImagePixel(image, x, y):
    """ !METHOD!
    Reads the Pixel Data of an Image

    Keyword arguments:
    :param Image img:                       Image to get the Pixel From
    :return: int[4] index:                  4 Pixels representing RGBA
    """
    
    width = image.size[0]
    height = image.size[1]
    
    index = img_getImagePixelIndex(x, y, width)
    pixels=image.pixels[index:index + 4]
    
    return pixels

def img_getImagePixelIndex(xt, yt, imagewidth):
    """ !METHOD!
    Gets the Color of a Pixel inside a Pixel Array of an Image

    Keyword arguments:
    :param Image img:                       Image to get the Pixel From
    :return: int[4] index:                  4 Pixels representing RGBA
    """
    
    return (yt * imagewidth + xt)*4

def img_getTilesetPixelIndex(xt, yt, tilesizex):
    """ !METHOD!
    Gets the Color of a Pixel inside a Pixel Array of an Image

    Keyword arguments:
    :param Image img:                       Image to get the Pixel From
    :return: int[4] index:                  4 Pixels representing RGBA
    """
    
    return yt * (tilesizex) + xt 

def math_getIndexByTile(xt, yt, tile_count_x):
    
    return yt * tile_count_x + xt

#endregion <Math>    

#region <Logic> <Methods>

def op_update_Palette(self, context):
    """ !METHOD!
    Updates the Current Selected Panel,
    Loads and Saves the Image
    Creates or Overwrites Previewimages based on the Pixel Colors and Packs them
    Eventually Delets Colorgroups etc.
    
    Keyword arguments:
    self, context                       N/A
    """
    settingsdata=context.scene.uv_palettes_settings_data
    #Loading Palette, Loading Values
    
    functionname="UpdatePalette"
    printLog(src=functionname, subtype=LOGTYPE.START)

    #Gets the Current Palette and clears it
    palette = return_CurrentPalette()
    palette.colors.clear()
    palette.p_editcolorgroups=False


    #Limit UV Offset to stay safe:
    #uv_offset_x = max(min(uv_offset_x, 0), scaling_x+(0.5/tile_count_x)) 
    #uv_offset_y = max(min(uv_offset_y, 0), scaling_y+(0.5/tile_count_y)) 

    img = palette.img #Check if it has an Image, if yes Skip
    if not img:
        printLog(src=functionname, subtype=LOGTYPE.ERROREXIT,msg="No Image")
        return
    
    #Unpack Previous Image if not used
    # if palette.oldimg:
    #     if not palette.oldimg is palette.img:
    #         bpy.ops.image.unpack({'image':  palette.oldimg})
    #         palette.oldimg=palette.img
    
    #Get coordinates and check for color count

    width = img.size[0]
    height = img.size[1] 

    #Load External Values
    scaling_x = palette.pe_scalex
    scaling_y = palette.pe_scaley
    uv_offset_x = palette.pe_offsetx
    uv_offset_y = palette.pe_offsety
    tile_count_x = palette.pe_tilecountx
    tile_count_y = palette.pe_tilecounty
    
    print("imagesize"+ str(width) +"/"+ str(height))
    
    #Check if Image and Tilecount dont fit together in terms of sizes

    if width < tile_count_x:
        Error("Resolution smaller than Tilecount X")
        printLog(src=functionname, subtype=LOGTYPE.ERROREXIT,msg="Resolution smaller than Tilecount X")
        return_CurrentPalette().img = None
        return
    if width < tile_count_y:
        Error("Resolution smaller than Tilecount Y")
        printLog(src=functionname, subtype=LOGTYPE.ERROREXIT,msg="Resolution smaller than Tilecount Y")
        return_CurrentPalette().img = None
        return
    
    #Check Bounds Tilecount
    if tile_count_x<=0:
        Error("Tilecount X cant be 0")
        printLog(src=functionname, subtype=LOGTYPE.ERROREXIT,msg="ilecount X cant be 0")
        return_CurrentPalette().img = None
        return
    if tile_count_y<=0:
        Error("Tilecount Ycant be 0")
        printLog(src=functionname, subtype=LOGTYPE.ERROREXIT,msg="Tilecount Y cant be 0")
        return_CurrentPalette().img = None
        return
   
    #Overwrite variabled of the Palette using the UI values
    palette.p_scale[0]=scaling_x
    palette.p_scale[1]=scaling_y
    palette.p_offset[0]=uv_offset_x
    palette.p_offset[1]=uv_offset_y
    palette.p_tilecountx=tile_count_x
    palette.p_tilecounty=tile_count_y

    #Rescale if required
    if scaling_x or scaling_y<1:
        width=int(width*scaling_x)
        height=int(height*scaling_y)
    
    #Create Colorgroup if not Exists:
    if(not palette.colorgroups):
        if(not len(palette.colorgroups) > 0):
            addColorgroup()

    #REMOVE REQUIRED MAYBE
    pcoll = preview_collections.get(img.name)   #get Previewimages
    save_dir = os.path.join(os.path.dirname(__file__), "preview_dir")

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    
    create_new = True
    
     #Check if preview Collection Images need to be recreated/added
    if pcoll:
        create_new = False #If exists dont create new collection [Bool is used later]
        printLog(src=functionname, subtype=LOGTYPE.INFO,msg="Preview Collection Detected")
    else:
        pcoll = bpy.utils.previews.new() #if doesnt exist create new preview collection
        printLog(src=functionname, subtype=LOGTYPE.ACTION,msg="Preview Collection Not found, will Recreate")
     
    print("Colorspace: "+img.colorspace_settings.name)
      
    imagepixels=img.pixels[:]


    #Iterate Image Pixels and Calculate
    
    iconsize=2
    for yt in range(tile_count_y):
        for xt in range(tile_count_x):
            # Calculate UV coordinates for the center of the tile
            uv_x, uv_y = math_UVPosition_By_Tile(xt, yt, tile_count_x, tile_count_y)
            print("uv: "+str(uv_x)+"/"+str(uv_y))

            index = math_PixelIndex_By_TileNumber(xt, yt, width, height, tile_count_x, tile_count_y, uv_offset_x, uv_offset_y)
            print(""+str(index))

            # Extract the color of the middle pixel from the texture
            #pixel_color = img_readPixel_By_Index(img, index)
            pixelindex=img_getTilesetPixelIndex(xt, yt, width)

            pixindex = int (img_getImagePixelIndex( int(uv_x*width), int(uv_y*height), width))
            pixel=imagepixels[pixindex:pixindex + 4]

            #pixel = readImagePixel(img, int(uv_x*width), int(uv_y*height))

            pixel_color=pixel

            #Convert Pixels
            pixels=[]
            for index in range(iconsize*iconsize):
 
                if(settingsdata.convertColorspace):
                    pixels.append(linear_to_sRGB(pixel[0]))
                    pixels.append(linear_to_sRGB(pixel[1]))
                    pixels.append(linear_to_sRGB(pixel[2]))
                    pixels.append(linear_to_sRGB(pixel[3]))
                else:
                    pixels.append(pixel[0])
                    pixels.append(pixel[1])
                    pixels.append(pixel[2])
                    pixels.append(pixel[3])    

            # for i in range(len(pixels)):
            #     pixels[i] = pixel

            print("2pixelscount: "+str(len(pixels)))
    
            #Create or Load Image 
    
            #Check if Image Exists and Delete if so
            if("."+img.name+"_UVColorIco_"+str(xt)+"/"+str(yt)+"-"+ str(pixelindex) in bpy.data.images): 
                
                image =bpy.data.images["."+img.name+"_UVColorIco_"+str(xt)+"/"+str(yt)+"-"+ str(pixelindex)]
                bpy.data.images.remove(image)
                printLog(src=functionname, subtype=LOGTYPE.ACTION,msg=": Image with Name:["+"."+img.name+"_UVColorIco_" + str(pixelindex)+"] will be Removed")

            image = bpy.data.images.new(name="."+img.name+"_UVColorIco_"+str(xt)+"/"+str(yt)+"-"+ str(pixelindex), width=iconsize, height=iconsize)
            printLog(src=functionname, subtype=LOGTYPE.ACTION,msg="Image with Name:["+"."+img.name+"_UVColorIco_" + str(pixelindex)+"] Created")
            print("pixelsofimage: "+str(len(image.pixels)))
            image.colorspace_settings.name = "Non-Color"
            image.pixels[:] = pixels
    
    
            #Save Image to Color Property and Save Image "icon"
    
            icon = pcoll.get(str(pixelindex)) # Set Icon by the Peview(i as index as string)
            if create_new: #if the list is not existing yet and needs to be recreated
                printLog(src=functionname, subtype=LOGTYPE.ACTION,msg=": icon ["+ str(pixelindex)+"] added to pcoll")
                icon = pcoll.new(str(pixelindex)) #create new Icon in pcoll and save it
                icon.icon_size = [iconsize,iconsize] #save size of the image (Icon is 8by8)
                icon.is_icon_custom = True
                icon.icon_pixels_float = pixels #Used as an icon

            color_item = palette.colors.add()
            color_item.uv = [uv_x, uv_y]
            color_item.name = str(pixelindex)
            color_item.color = pixel_color
            color_item.icon = image
            
       
            #Create File in Addon Directoy (arent deleted yet in any way)       
    
            #Imagesaving
            printLog(src=functionname, subtype=LOGTYPE.ACTION,msg="Image Created: "+"."+img.name+"_UVColorIco_" + str(pixelindex))
            image_name = "{}_{}.png".format(img.name, str(pixelindex))
            file_path = os.path.join(save_dir, image_name)
            image.save_render(file_path)
            image.pack()
            printLog(src=functionname, subtype=LOGTYPE.ACTION,msg="icon ["+image.name+"] was packed")
            
    
            #Write, Pack and Mark loaded
    
    preview_collections[img.name] = pcoll
    img.pack()
    palette.p_loaded=True
    printLog(src=functionname, subtype=LOGTYPE.FINISH)
    
def uv_Tilenumber_By_Active_Face_UV(self,context):
    """
    Find the most populated segment in the UV space of the selected parts of the mesh.

    Keyword arguments:
    context (bpy.context): Blender context
    :return: (tuple) majority_segment: X and Y coordinates of the majority segment, None: if no mesh with UV data is selected
    """
    
    #Load Object etc 
    
    functionname = "findMajoritySegment"
    printLog(src=functionname, subtype=LOGTYPE.START)  # Assuming printLog is defined elsewhere

    uvcoords=[]

        # Check if Blender is in edit mode
    if bpy.context.object is not None and bpy.context.object.mode == "EDIT":

        # Get selected objects in edit mode
        
        for obj in bpy.context.selected_objects:
            me = obj.data
            bm = bmesh.from_edit_mesh(me)

            # Get the active UV layer
            uv_lay = bm.loops.layers.uv.active

            # Initialize a list to store selected faces
            selected_faces = []

            # Iterate through faces to find selected ones
            face=None
            
            
            #Iterate Current Faces to find the Active Selection by using the bmesh history
            
            for face in bm.faces:
                for element in reversed(bm.select_history):
                    if isinstance(element, bmesh.types.BMFace):
                        face = element
                        break

                if face is None: 
                    return (None)
                if face.select :
                    selected_faces.append(face)
                    
                
           
            #Check if any faces are selected
            if len(selected_faces) == 0:
                continue
               
            #Iterate through selected faces and update UV coordinates
            for face in selected_faces:
                for loop in face.loops:
                    uvcoords.append(loop[uv_lay].uv )
                    
            # End Region

    
    printLog(src=functionname, subtype=LOGTYPE.INFO, msg="UV Coordinates Loaded (Count): "+str(len(uvcoords))) 
    
    #Exits if Palette doesnt Exist
    # Get the tile count from the palette
    palette = return_CurrentPalette()  # Assuming getCurrentPalette is defined elsewhere
    if palette is None:
        printLog(src=functionname, subtype=LOGTYPE.ERROR, msg="No Palette")  # Assuming printLog is defined elsewhere
        return None
    
    num_segments_x = palette.p_tilecountx
    num_segments_y = palette.p_tilecounty
    
    
    # Initialize a dictionary to count loops in each segment
    segment_counts = {(x, y): 0 for x in range(num_segments_x) for y in range(num_segments_y)}
    
    majority_segment=None
    # Iterate through UV coordinates and count loops in each segment
    for uv in uvcoords:

        # Calculate the segment indices for the UV coordinate
        segmentCoordinates = math_getTileFromUV(num_segments_x, num_segments_y, uv)
        
        #printLog(src=functionname, subtype=LOGTYPE.IN, msg="UV"+str(uv.x)+"/"+str(uv.y)) 
        # Increment the count for the corresponding segment
        if 0 <= segmentCoordinates[0] < num_segments_x and 0 <= segmentCoordinates[1] < num_segments_y:
            segment_counts[(segmentCoordinates[0], segmentCoordinates[1])] += 1
            
            #find and Set the Tile Segment with the most Verts in it
            majority_segment = max(segment_counts, key=segment_counts.get)
    
    printLog(src=functionname, subtype=LOGTYPE.FINISH)  # Assuming printLog is defined elsewhere
    return majority_segment

def mesh_Filter_Selection_By_Tilenumber(self, context, majority_segment, deselectmode):
    """ !METHOD!
    Select Verts that are on a Similar UV Position

    Keyword arguments:
    self, context                       N/A #
    """
    


    functionname="similarSegmentTool"
    #printLog(src=functionname, subtype=LOGTYPE.ONECALL)

    # Get the tile count from the palette
    palette = return_CurrentPalette()
    if palette is None:
        printLog(src=functionname, subtype=LOGTYPE.ERROREXIT,msg="No Palette")
        return None
    
    num_segments_x = palette.p_tilecountx
    num_segments_y = palette.p_tilecounty
    
    if majority_segment:
        # Get the mesh data of the active object
        mesh_data = bpy.context.active_object.data

        # Get the number of vertices in the mesh
        num_vertices = len(mesh_data.vertices)

        # Convert segment coordinates to UV space
        newUVPos = math_UVPosition_By_Tile(majority_segment[0], majority_segment[1], num_segments_x, num_segments_y)
        

                # Check if Blender is in edit mode
        if bpy.context.object.mode == "EDIT":

            # Get selected objects in edit mode
            for obj in bpy.context.selected_objects:
                me = obj.data
                bm = bmesh.from_edit_mesh(me)
                uv_lay = bm.loops.layers.uv.active #get active uv layer
                bm.select_flush(True)
                for face in bm.faces: #Iterate Faces and Select
                    for loop in face.loops:
                        segcoords=math_getTileFromUV(num_segments_x, num_segments_y, loop[uv_lay].uv)
                        #printLog(src=functionname, subtype=LOGTYPE.INFO, msg="segcoords: "+str(segcoords[0])+"/"+str(segcoords[1])) 

                        if (segcoords[0] == majority_segment[0] and segcoords[1] == majority_segment[1] and not deselectmode):#Compare if Position is on Tile Segment
                            face.select=True
                        if (segcoords[0] == majority_segment[0] and segcoords[1] == majority_segment[1] and deselectmode):
                            face.select=False

                            #loop[uv_lay].uv = newUVPos would override the uv of other Elements 
  

                
                #Update the mesh data         
                bmesh.update_edit_mesh(obj.data)

def availabilityCheck(palette):

        paletteNotNone =False
        paletteLoaded =False
        paletteImageSet=False       
        paletteHasColors=False
        paletteHasGroups=False
        paletteDefaultMaterial=False
        if palette is not None:
            paletteNotNone=True
            if palette.img:
                paletteImageSet=True
                if palette.defaultmaterial:
                    paletteDefaultMaterial=True
                if palette.p_loaded:
                    paletteLoaded=True
                    if len(palette.colors) > 0:
                        paletteHasColors=True
                        if(palette.colorgroups):
                            if(len(palette.colorgroups)>0):
                                paletteHasGroups=True

        palettestatus={
            "Palette":paletteNotNone,
            "Image":paletteImageSet,
            "Loaded":paletteLoaded,
            "Colors":paletteHasColors,

            "Groups":paletteHasGroups,
            "DefaultMaterial":paletteDefaultMaterial,
            "paletteNotNone":paletteNotNone,
            "paletteNotNone":paletteNotNone
        }
        return palettestatus

#endregion <Logic>   

def smoothObjects (self, context):
    #Shade Smooth all selected Objects
    wasInObjectmode=False
    
    if bpy.context.mode != 'EDIT_MESH':
        wasInObjectmode=True
        bpy.ops.object.mode_set(mode='EDIT')
    
    selected_Objects=bpy.context.selected_objects
    for obj in selected_Objects:
        if not obj.type == 'MESH':
                continue
                
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        for f in bm.faces:
            f.smooth = True
            
    if wasInObjectmode:
        bpy.ops.object.mode_set(mode='OBJECT')        
    bpy.context.view_layer.update()
    
def splitNormals(self, context):
    settingsdata = bpy.context.scene.uv_palettes_settings_data

    autosmooth= settingsdata.autosmooth
    clear= settingsdata.cleanSplitNormals
    activeMode=False
    
    #check if self has angle attribute
    if not hasattr(self, "angle"):
        angle = settingsdata.splitangle
        activeMode = True
    else:
        angle=self.angle
        
    
        
    edgecount=0      
    selected_Objects=bpy.context.selected_objects         
    if activeMode:
        #count selected edges using bmesh
        for obj in selected_Objects:
            if not obj.type == 'MESH':
                continue
                
            #get selected edges
            me = obj.data
            bm = bmesh.from_edit_mesh(me)
            for edge in bm.edges:
                if edge.select:
                    edgecount+=1    

    #Deselect objects that arent meshes
    for obj in selected_Objects:
        if not obj.type == 'MESH':
            obj.select_set(False)
           

      #go to edit mode if not already 
    if bpy.context.mode != 'EDIT_MESH':
        wasInObjectmode=True
        bpy.ops.object.mode_set(mode='EDIT')
    
    bpy.context.tool_settings.mesh_select_mode = (False, True, False)    
        
        
    
    if(autosmooth):
        smoothObjects(self, context)
        
    if clear: # Clear if needed
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.mark_sharp(clear=True)
        
        bpy.ops.mesh.customdata_custom_splitnormals_clear()    
           
    wasInObjectmode=False
    
    
    

        
    #Deselect all Edges first 
    bpy.ops.mesh.select_all(action='DESELECT')
    
    #Select all edges with a sharp edge angle
    bpy.ops.mesh.edges_select_sharp(sharpness=math.radians(angle))
    
    secondedgecount=0
    
    if activeMode:
        for obj in selected_Objects:
            if not obj.type == 'MESH':
                continue
                
            me = obj.data
            bm = bmesh.from_edit_mesh(me)
            for edge in bm.edges:
                if edge.select:
                    secondedgecount+=1
            
    if activeMode:
        if edgecount>secondedgecount or edgecount<secondedgecount:
            bpy.ops.ed.undo_push(message = "Push Undo (Split Normals Operator): "+str(abs(edgecount-secondedgecount)) + " Edges Changed")
            #print(str(abs(edgecount-secondedgecount)))
    
    #Split Normals of the selected edges
    bpy.ops.mesh.split_normals()
    # if not activeMode:
    #     bpy.ops.view3d.update_edit_mesh()
            
    # if not wasInObjectmode:
    #     bpy.ops.object.mode_set(mode='OBJECT')
    # else:
    #     bpy.ops.object.mode_set(mode='EDIT')
        
#region <Operators> <Methods>

def op_Select_By_Equal_Tile(self, context):
    """ !METHOD!
    Select Verts that are on a Similar UV Position

    Keyword arguments:
    self, context                       N/A #
    """
    functionname="selectSimilarSegment"
    


    #Exit if no Palette 
    
    palette = return_CurrentPalette()
    if palette is None:
        printLog(src=functionname, subtype=LOGTYPE.ERROREXIT,msg="No Palette")
        return None
 
    num_segments_x = palette.p_tilecountx
    num_segments_y = palette.p_tilecounty

    majority_segment = uv_Tilenumber_By_Active_Face_UV(self, context)
    if majority_segment:
        mesh_Filter_Selection_By_Tilenumber(self, context,majority_segment, False)
        
        printLog(src=functionname, subtype=LOGTYPE.INFO,msg="Segment Detected:"+str(majority_segment[0])+" / "+str(majority_segment[1]))
    else:
        printLog(src=functionname, subtype=LOGTYPE.ERROR,msg="No Segments Detected")

def op_Deselect_By_Equal_Tile(self, context):
    """ !METHOD!
    Select Verts that are on a Similar UV Position

    Keyword arguments:
    self, context                       N/A #
    """
    
    functionname="selectSimilarSegment"

        # Get the tile count from the palette
    palette = return_CurrentPalette()
    if palette is None:
        printLog(src=functionname, subtype=LOGTYPE.ERROREXIT,msg="No Palette")
        return None
    
    num_segments_x = palette.p_tilecountx
    num_segments_y = palette.p_tilecounty
    
    
    majority_segment = uv_Tilenumber_By_Active_Face_UV(self, context)
    if majority_segment:
        mesh_Filter_Selection_By_Tilenumber(self, context,majority_segment, True)
        printLog(src=functionname, subtype=LOGTYPE.INFO,msg="Segment Detected:"+str(majority_segment[0])+" / "+str(majority_segment[1]))
    else:
        printLog(src=functionname, subtype=LOGTYPE.ERROR,msg="No Segments Detected")
    
    printLog(src=functionname, subtype=LOGTYPE.ONECALL)

def op_setup_Color_On_Faces(self, context):
    """ !METHOD!
    Sets the Color of the Selected Faces, is used by Operators Usually

    Keyword arguments:
    self, context                       N/A #
    Warning: Dont Log Operators!
    """
    # Check if the function is used via a Color Display Panel Button "active"
    

    palette = return_CurrentPalette()
    
    
    targetuv=None
    if hasattr(self, "active"):
        if(palette.p_editcolorgroups):
            return None
        
        if self.active:
            
            targetuv=self.uv
            # Get the current palette
            

            # Iterate through colors in the palette
            for i, c in enumerate(palette.colors):
                if c == self:
                    palette.index = i
                else:
                    c.active = False
    else:
        targetuv=(self.uvcoords[0],self.uvcoords[1])
        
     

    
    if(targetuv is None):
        return None
    # Check if Blender is in edit mode
    if bpy.context.object.mode == "EDIT":

        # Get selected objects in edit mode    
        for obj in bpy.context.selected_objects:
            if not obj.type == 'MESH':
                continue
                
            me = obj.data
            bm = bmesh.from_edit_mesh(me)

            # Get the active UV layer
            uv_lay = bm.loops.layers.uv.active

            # Initialize a list to store selected faces
            selected_faces = []

            # Iterate through faces to find selected ones
            for face in bm.faces:
                if face.select:
                    selected_faces.append(face)

            # Check if any faces are selected
            if len(selected_faces) == 0:
                continue
             
            
            op_add_default_Material(context, self, selected_faces, obj)#Materialadding by Settings

            # Iterate through selected faces and update UV coordinates
            for face in selected_faces:
                for loop in face.loops:
                    loop[uv_lay].uv = targetuv

            # Update the mesh data
            #bm.select_flush(True)
            bmesh.update_edit_mesh(obj.data)
            
#endregion <Operators>    
            
#region <Colorgroup_Logic> <Methods>
             
def colorgroup_is_Pixel_Filtered(palette, colorindex, parameter): 
    '''
    returns if the Pixel is colorgrouped by Filter
    '''
    
    enabledColorgroups=getEnabledColorgroups(palette)
    status= False 
    if palette:
        if(palette.colorgroupLayermode=="and"):
            status= True
            

        if (enabledColorgroups):
            if (len(enabledColorgroups)>0):
                for colorgroup in enabledColorgroups:
                    if (isColorActive_InvertFilter(colorgroup, colorindex) and getattr(colorgroup, parameter)):
                        if(palette.colorgroupLayermode=="or"):
                            status= True 
                            break
                                        
                        if(palette.colorgroupLayermode=="and" and status):
                            status= True
                    else: 
                        status= False                          
            else:
                return status
    return status

def colorgroup_is_Active(palette, colorgroup): 
    
    state=False
    
    if not(palette.selectedcolorgroup+1 > len(palette.colorgroups)):
        state= True if (colorgroup.alwaysActive or colorgroup == palette.colorgroups[palette.selectedcolorgroup]) else False
    # if(False):
    #     return True if (colorgroup.alwaysActive or colorgroup == palette.colorgroups[palette.selectedcolorgroup]) else False
    
    return state

def getEnabledColorgroups(palette):
       
    enabledColorgroups=None  
    palette=return_CurrentPalette()

    enabledColorgroups=[]
    if(palette):
        for colorgroup in palette.colorgroups:
            if(colorgroup_is_Active(palette, colorgroup)):
                enabledColorgroups.append(colorgroup)
        if not len(enabledColorgroups)>0:
            enabledColorgroups=None
    return enabledColorgroups

def isColorgroupEnabled(palette, colorgroup):
    
    enabledColorgroups=None
    
    palette=return_CurrentPalette()
    if(palette):
        if(colorgroup.alwaysActive or colorgroup == palette.colorgroups[palette.selectedcolorgroup]):
            return True
         
    return False

def isColorActive_InvertFilter(colorgroup, colorindex):
    return colorgroup.colorgroupdata[colorindex].state if (not colorgroup.inverted) else not colorgroup.colorgroupdata[colorindex].state


#endregion <Colorgroup_Logic>   

#region <Colorgroup_All> <Methods>
def gf_Col_isLocked(palette, colorindex):
    return colorgroup_is_Pixel_Filtered(palette, colorindex, "lock")

def gf_Col_isHidden(palette, colorindex):
    return colorgroup_is_Pixel_Filtered(palette, colorindex, "hideColors")

#DEPRECATED?, Colorwheel uses Single Checks to Display individual Colorgroups
def gf_Col_inWheel(palette, colorindex):
    return colorgroup_is_Pixel_Filtered(palette, colorindex, "addToColorwheel")

def gf_Col_inQuick(palette, colorindex):
    return colorgroup_is_Pixel_Filtered(palette, colorindex, "addToColorshift")

def gf_Col_inToolSel(palette, colorindex):
    return colorgroup_is_Pixel_Filtered(palette, colorindex, "applyOnTool_Selection")

def gf_Col_inToolDes(palette, colorindex):
    return colorgroup_is_Pixel_Filtered(palette, colorindex, "applyOnTool_Deselection")

def gf_Col_ColShift(palette, colorindex):
    return colorgroup_is_Pixel_Filtered(palette, colorindex, "applyOnTool_ColorShift")

#endregion <Colorgroup_All>    

#region <Colorgroup_Single> <Methods>
#Independent Checks

def gf_Col_Single_Group_Filter(palette, colorindex, parameter, colorgroup):
    enabledColorgroups=getEnabledColorgroups(palette)
    status=False

    if (enabledColorgroups):
        if (colorgroup_is_Active(palette, colorgroup)):
            if (isColorActive_InvertFilter(colorgroup, colorindex) and getattr(colorgroup, parameter)):
                status= True
    return status

def gf_Col_Sgl_isLocked(palette, colorindex,colorgroup):
    return gf_Col_Single_Group_Filter(palette, colorindex, "lock",colorgroup)

def gf_Col_Sgl_isHidden(palette, colorindex,colorgroup):
    return gf_Col_Single_Group_Filter(palette, colorindex, "hideColors",colorgroup)

def gf_Col_Sgl_inWheel(palette, colorindex,colorgroup):
    return gf_Col_Single_Group_Filter(palette, colorindex, "addToColorwheel",colorgroup)

def gf_Col_Sgl_inQuick(palette, colorindex,colorgroup):
    return gf_Col_Single_Group_Filter(palette, colorindex, "addToColorshift",colorgroup)

def gf_Col_Sgl_inSel(palette, colorindex,colorgroup):
    return gf_Col_Single_Group_Filter(palette, colorindex, "applyOnTool_Selection",colorgroup)

def gf_Col_Sgl_inDes(palette, colorindex,colorgroup):
    return gf_Col_Single_Group_Filter(palette, colorindex, "applyOnTool_Deselection",colorgroup)

def gf_Col_Sgl_ColShift(palette, colorindex,colorgroup):
    return gf_Col_Single_Group_Filter(palette, colorindex, "applyOnTool_ColorShift",colorgroup)

#endregion <Colorgroup_Single>    

def toggleDrawingDepr(self, context):
    """ !METHOD!
    ???
    
    Keyword arguments:
    -
    """

    if self.uv_palettes_drawing:
        bpy.ops.object.modal_operator('INVOKE_DEFAULT')

#region <return> <Methods>

def return_CurrentPalette(): #Gives back the selected Palette using "bpy.context.scene.uv_palettes_index" or else None
    """ !METHOD!
    returns the Current Selected palette of theres palette
    
    Keyword arguments:
    :return: context ---:              Current Selected Palette, None if there no Palettes
    """

    if len(bpy.context.scene.uv_palettes) > bpy.context.scene.uv_palettes_index:
        return bpy.context.scene.uv_palettes[bpy.context.scene.uv_palettes_index]
    else:
        return None
  
def return_SettingsData():
    """ !METHOD!
    returns Settings Propertygroup Context
    
    Keyword arguments:
    :return: context ---:              Settings
    """
    return bpy.context.scene.uv_palettes_settings_data

def return_KeyBy_bl_id(idname):
        #     row.label(text=""+km.type)
    # Get the keymap for the 3D Viewport
    keymap = bpy.context.window_manager.keyconfigs.user.keymaps['Window']

    # Get the Blender User key configuration
    user_keyconfig = bpy.context.window_manager.keyconfigs.user

    # Check if the Blender User key configuration exists
    if user_keyconfig:
        # Get the "Window" keymap from the Blender User key configuration
        window_keymap = user_keyconfig.keymaps.get('Window')

        # Check if the "Window" keymap exists
        if window_keymap:
            # Iterate over keymap items in the "Window" keymap
            for item in window_keymap.keymap_items:
                # Check if the operator ID matches the target operator
                if item.idname == idname:
                    # Print the key binding for the operator
                    modifiers = [mod for mod in ['ctrl', 'alt', 'shift', 'oskey'] if getattr(item, mod)]
                    key_with_modifiers = '+'.join(modifiers + [item.type])
                    return str(key_with_modifiers)
                    break
            else:
                return "No Bind."
        else:
            return "No wm Keymap."
    else:
        return "No User kCfg."

#endregion <return>    

def open_file_explorer(path):
    if os.path.isdir(path):
        subprocess.Popen(f'explorer "{path}"')
    else:
        directory = os.path.dirname(path)
        subprocess.Popen(f'explorer "{directory}"')


# ==================================================================================
# ||                        Property Groups + Panels                              ||
# ==================================================================================
# || Description: Properties used in this Addon                                   ||
# ==================================================================================

class UVC_Group_boolcolorgroup(bpy.types.PropertyGroup):
    """tores Propertys For a Colorgroup Color Tile"""

    state: bpy.props.BoolProperty(name="state",default= True)

class UVC_Data_Palette_Colorgroup(bpy.types.PropertyGroup):
    """Stores Propertys for Colorgroups"""
    
    #GroupData for when Group is Filtering and how
    
    title: bpy.props.StringProperty (name="Name", default= "unnamed")       #type: ignore        #Name of the Colorgroup Displayed in the UI

    alwaysActive: bpy.props.BoolProperty(name="Colorgroup Always Active",default= True, \
    description="Advanced Option to Control which Groups should be enabled, \n usually all are enabled, using this Tool you can control what colors to show or to select")#Enables the Colorgroup even if not Selected not Reccomended
                                                                                        #Colorgroups should only be Active when Selected, else they should not do Anything at all,
    inverted: bpy.props.BoolProperty(name="Invert Colorgroup",default= False, description="Inverts the Colorgroup Selected Colors")          #Inverts the Fields of the Colorgroup

    
    #GroupData for Locking and Hiding Colors
    
    lock: bpy.props.BoolProperty(name="Disable Color",default= False, description="Disable in Color Panel")    #Disables the Color in the UI (May be Visible by an Lock Icon)
    hideColors: bpy.props.BoolProperty(name="Show Colors",default= True, description="Shows Selection in the Color Panel")                #Hides colors in UI completly
    
    #Where to Add Group
    
    addToColorwheel: bpy.props.BoolProperty(name="addToColorwheel",default= False, description="Display the Selected Colors \n inside the Colorwheel")      #Adds the Color to the UI 
    addToColorshift: bpy.props.BoolProperty(name="addToColorshift",default= False, description="Use the Selected Colors \n inside the Colorshift")     #Adds the Color to the QuickUI
    
    #Selectiontool Behavior
    
    applyOnTool_Selection: bpy.props.BoolProperty(name="applyOnTool_Selection",default= False, description="Will Disable Colors from getting selected \n from the Select Colorgroupcolors Tool")       #Disables the Selection via Tools
    applyOnTool_Deselection: bpy.props.BoolProperty(name="applyOnTool_Deselection",default= False, description="Will Disable Colors from getting deselected \n from the Deselect Colorgroupcolors Tool")       #Disables the Selection via Tools
       
    #General Group Data 
    
    colorgroupdata: bpy.props.CollectionProperty(name="Colorgroup Data", type=UVC_Group_boolcolorgroup)
    rename: bpy.props.BoolProperty(name="Configurate Colorgroup",default= True)
    
    #DELETE
    def get_array(self):
        return (True, self["somebool"])

    #DELETE
    def set_array(self, values):
        self["somebool"] = values[0] and values[1]  

#Propertygroup (color)
class UVC_Data_Palette_Color(bpy.types.PropertyGroup):
    """Stores Propertys for each Colors of a Panel"""

    active: bpy.props.BoolProperty(name="Select", update=op_setup_Color_On_Faces)
    color: bpy.props.FloatVectorProperty(name="Color", min=0, max=1, subtype="COLOR", size=4, default=(1,1,1,1))
    uv: bpy.props.FloatVectorProperty(name="UV Offset", size=2)
    icon: bpy.props.PointerProperty(name="Source", type=bpy.types.Image)
    colortype: bpy.props.IntProperty(name="Color Type",default=0)
      
#Propertygroup (palette)   
class UVC_Data_Palette(bpy.types.PropertyGroup):
    """Stores Propertys for each Palettes"""
    #Palette Data
    
    colors: bpy.props.CollectionProperty(name="Colors", type=UVC_Data_Palette_Color)
    img: bpy.props.PointerProperty(name="Source", type=bpy.types.Image)
    oldimg: bpy.props.PointerProperty(name="Buffer", type=bpy.types.Image)
    preview: None
    index: bpy.props.IntProperty(name="index")
    defaultmaterial: bpy.props.PointerProperty(name="Material", type=bpy.types.Material) 
    
    #Colorgroups
    
    colorgroups: bpy.props.CollectionProperty(name="Colorgroups", type=UVC_Data_Palette_Colorgroup)

    selectedcolorgroup: bpy.props.IntProperty(name="UV Colorgroups index")
    
    colorgroupLayermode: bpy.props.EnumProperty(
        items=[
            ('and', 'AND', 'AND filters a Color if all Active Colorgroups filter the Color ',"SELECT_INTERSECT",1),
            ('or', 'OR', 'OR filters a Color if any Active Colorgroup filters the Color', "SELECT_EXTEND",2)
        ],
        name="Colorgroup Layermode",
        description="Determines how the Colorgroup is applied",
        default='or',
    )
    
    ##Internal Palette Variables
    
    p_scale: bpy.props.FloatVectorProperty(name="Scaling", size=2)
    p_offset: bpy.props.FloatVectorProperty(name="UV Offset", size=2)
    p_tilecountx: bpy.props.IntProperty(name="Tilecount X",default=8, description="Amount of Tiles on X Axies")
    p_tilecounty: bpy.props.IntProperty(name="Tilecount X",default=8, description="Amount of Tiles on X Axies")
    p_loaded: bpy.props.BoolProperty(name="loaded",default= False)
    p_editcolorgroups: bpy.props.BoolProperty(name="is Drawing Colorgroup",default= False)
    
    #UI Variables
    
    pe_scalex: bpy.props.FloatProperty(name="PE_Scaling X", min=0, max=1, default=1.0)
    pe_scaley: bpy.props.FloatProperty(name="PE_Scaling Y", min=0, max=1, default=1.0)
    pe_offsetx: bpy.props.FloatProperty(name="PE_UV Offset X", min=0, max=1, default=0.0)
    pe_offsety: bpy.props.FloatProperty(name="PE_UV Offset Y", min=0, max=1, default=0.0)
    pe_tilecountx: bpy.props.IntProperty(name="PE_Tilecount X", min=0, max=64,default=8)
    pe_tilecounty: bpy.props.IntProperty(name="PE_Tilecount Y", min=0, max=64,default=8)
    
    
    
class UVC_MT_Colorwheel(Menu):
    # bl_label is displayed at the center of the pie menu
    bl_label = 'UVC_MT_Colorwheel'
    bl_idname = 'UVC_MT_Colorwheel'


    def draw(self, context): #Draw Pie Menu
        layout = self.layout
        count=0
        total=0
        pie = layout.menu_pie()
        palette=return_CurrentPalette() #Get colorgrouped Colors
        if(palette):
            colorgroupcount=len(palette.colorgroups)
            settingsdata=context.scene.uv_palettes_settings_data
            #box = pie.split().box().column()
            if(settingsdata.colorwheelDisplayType == "horizontal"):
                
                for colorgroupindex in range(colorgroupcount):
                    count=0
                    for colindex in range(len(palette.colors)):
                        if(gf_Col_Sgl_inWheel(palette, colindex ,palette.colorgroups[colorgroupindex])):      
                            if(count==0):
                                
                                box=pie.split().box()
                                grid=box.row()

                                row_label=grid.row()
                                row_label.label(text=""+palette.colorgroups[colorgroupindex].title)
                                
                                total=total+1   
                                row= grid.row()

                            if(count%3 == 0 and count!=0):
                                row= grid.row()
                                
                                
                            row.operator( UVC_Operator_Palette_setColor.bl_idname, icon_value = layout.icon(palette.colors[colindex].icon)).uvcoords=palette.colors[colindex].uv
                            count=count+1
                    if(total>6):
                        break

            if(settingsdata.colorwheelDisplayType == "vertcial"):

              
                colorgroupcount=len(palette.colorgroups)
                settingsdata=context.scene.uv_palettes_settings_data
                #box = pie.split().box().column()
                    
                for colorgroupindex in range(colorgroupcount):
                    count=0
                    for colindex in range(len(palette.colors)):
                        if(gf_Col_Sgl_inWheel(palette, colindex ,palette.colorgroups[colorgroupindex])):      
                            if(count==0):
                                row = pie.split().box()
                                total=total+1   
                                column = row.column()    
                            column.operator( UVC_Operator_Palette_setColor.bl_idname, icon_value = layout.icon(palette.colors[colindex].icon)).uvcoords=palette.colors[colindex].uv
                            column = row.column()  
                            count=count+1
                    if(total>6):
                        break

            
                                #box = pie.split().box().column()
                                #box.operator(UVC_Operator_Palette_setColor.bl_idname, icon_value = layout.icon(palette.colors[availableColors[colindex]].icon), text=""+str(availableColors[colindex])).uvcoords=palette.colors[availableColors[colindex]].uv


            if(settingsdata.colorwheelDisplayType == "grouped"):
                                #box = pie.split().box().column()
                colorgroupcount=len(palette.colorgroups)
                for colorgroupindex in range(colorgroupcount):
                    count=0
                    for colindex in range(len(palette.colors)):
                        if(gf_Col_Sgl_inWheel(palette, colindex ,palette.colorgroups[colorgroupindex])):      
                            if(count==0):
                                
                                box=pie.split().box()
                                row_label=box.row()
                                row_label.label(text=""+palette.colorgroups[colorgroupindex].title)
                                
                                row= box.row()
                                total=total+1   
                                

                            if(count%3 == 0 and count!=0):
                                row= box.row()
                                
                                
                            row.operator( UVC_Operator_Palette_setColor.bl_idname, icon_value = layout.icon(palette.colors[colindex].icon)).uvcoords=palette.colors[colindex].uv
                            count=count+1
                    if(total>6):
                        break

            if(settingsdata.colorwheelDisplayType == "singlefield"):


         
                availableColors=[]
                for colindex in range(len(palette.colors)):
                    if(gf_Col_inWheel(palette, colindex)):
                        if(len(availableColors)<8):
                            availableColors.append(colindex)
                        else:
                            break
                # for colindex in availableColors:
                #     pie.operator(UVC_Operator_Palette_setColor.bl_idname, icon_value = layout.icon(palette.colors[colindex].icon)).uvcoords=palette.colors[colindex].u
                        
                box = pie.split().box().column()
                clockwise_mapping=get_clockwise_mapping(num_elements=len(availableColors))


                #8 Field Total
                if(len(availableColors)>0): #Create Pie Menuoptions
                    
                    for numindex in range(8):  
                        if(clockwise_mapping[numindex]>=len(availableColors)):
                            pie.operator(EmptyOperator.bl_idname, icon="UNPINNED", text=""+str(clockwise_mapping[numindex]))
                        else:
                            pie.operator(UVC_Operator_Palette_setColor.bl_idname, icon_value = layout.icon(palette.colors[availableColors[clockwise_mapping[numindex]]].icon), text=""+str(clockwise_mapping[numindex])).uvcoords=palette.colors[availableColors[clockwise_mapping[numindex]]].uv
              
              
              
            '''
                    #box = pie.split().box().column()
                
            # for colindex in availableColors:
            #     pie.operator(UVC_Operator_Palette_setColor.bl_idname, icon_value = layout.icon(palette.colors[colindex].icon)).uvcoords=palette.colors[colindex].u

            '''


          


            
    #Center Pivot, Top Bottom, X/X- Y/Y- Direction Add Checkboxes for Direction,or Center and Height
    #5 Options are Center and each Direction, while the Others are Top, Mid or Bottom, and the Last ist Left or Right Corner, based on Max Size,
    #Alternatively, average or median
    
#region <LoadingMethods> <Operator>

def actiontextWasSet(self, ctx):
    bpy.context.scene.uv_popup_buffer.actiontextWasSet=True

def actionReturn(self, ctx):
    bpy.context.scene.uv_popup_buffer.actiontextWasSet=False
    bpy.context.scene.uv_popup_buffer.actiontext=""

def load_settings_from_file(filepath):
    with open(filepath, 'r') as f:
        property_dict = json.load(f)
    return property_dict

def load_settings_data(property_dict, settingsdata, context):

    #getSettingsdataDict

    settings=None

    if("settings" in property_dict):
        if(property_dict["settings"]):
            settings=property_dict["settings"]

    if(settings):
        for key, value in settings.items():
            if hasattr(settingsdata, key):
                setattr(settingsdata, key, value)

def load_palette_data(property_dict, context, settingsdata, isNewPalette, targetpalette):

    #getSettingsdataDict

    palettedata_dict=None

    print("Try Loading Palette")
    if("palette" in property_dict):
        palettedata_dict=property_dict["palette"].copy()

    if( isinstance(palettedata_dict, dict)):
        print("Found Palettedata")
        for palettekey, palettevalue in palettedata_dict.items(): #Iterates each Palette



            if(isinstance(palettevalue, dict)): #If Dictionary check for registered ones below here:

                if(palettekey=="colorgroups" and settingsdata.importmode_Groups!="off"): #Check for Groups     

                    #Enum Option Logic for Groups
                    if(not isNewPalette):
                        if settingsdata.importmode_Groups=="clean": # Clear Groups of the Panel to the beginning
                            targetpalette.colorgroups.clear()


                    for groupskey, groupsvalue in palettedata_dict["colorgroups"].items(): #Iterates each Colorgroup Data inside each Colorgroup
                        
                        #Enum Option Log for Group
                        if isNewPalette:
                            if settingsdata.importmode_Groups=="auto" : #Only adds Colorgroup if it doesnt exist yet                                                         
                                    if(element.title == palettedata_dict["colorgroups"]["title"]):
                                        for element in targetpalette.colorgroups:
                                            if(element.title == palettedata_dict["colorgroups"]["title"]):
                                                break #exit if it already exists
             
                                    
                        if settingsdata.importmode_Groups=="add" or (not isNewPalette and settingsdata.importmode_Groups in ["auto", "modify"]): #add / add if file is not new but auto or modify is selected
                            targetgroup=targetpalette.colorgroups.add()      

                        if isNewPalette:
                            if settingsdata.importmode_Groups=="modify": #Only Modify existing Groups, dont add new
                                for element in targetpalette.colorgroups:
                                    if(element.title == palettedata_dict["colorgroups"]["title"]):
                                        targetgroup=element
                                        targetgroup.colorgroupdata.clear()
                                    else:
                                        break #exit if it doesnt exist
                        
                        print("try init groups property:"+groupskey+" /  probably dict")

                        for groupkey, groupvalue in groupsvalue.items(): #Init Group Entry#   

                            if(isinstance(groupvalue, dict)): #Init Group Datapoints
                                    if(groupkey == "colorgroupdata"):   
                                        for colorgroupdataindex, colorgroupdatapointvalue in groupvalue.items():
                                            print("creating group datapoint:"+str(colorgroupdataindex)+" / "+str(colorgroupdatapointvalue))
                                            newgroupdata=targetgroup.colorgroupdata.add()
                                            newgroupdata.state=colorgroupdatapointvalue

                            else: #if not a Group
                                print("try init group property:"+groupkey+" / "+ str(groupskey))
                                if hasattr(targetgroup, groupkey):
                                    setattr(targetgroup, groupkey, groupvalue)
                            
            else: #Set Data of Palette
                print("try init palette property:"+palettekey+" / "+ str(palettevalue))
                if hasattr(targetpalette, palettekey):
                    setattr(targetpalette, palettekey, palettevalue)
        return targetpalette

def load_image_data(property_dict, context, settingsdata, palette=None):

    #getSettingsdataDict

    imagedata_dict=None

    print("Try Loading Image")
    if("image" in property_dict):
        if all(key in property_dict["image"] for key in ("width", "height", "name", "imagedata")):  
            imagedata_dict=property_dict["image"].copy()

 
    if( isinstance(imagedata_dict, dict)):

        width=imagedata_dict["width"]
        height=imagedata_dict["height"]
        name=imagedata_dict["name"]

        for index in range(width*height): # Check if all Data is stored
            print(index)
            if(not str(index) in imagedata_dict["imagedata"]):
                print("RIP"+index)
                return None
    
        pixeldataarray=[]

        print("Found Imagedata")
        for pixelindex, pixeldata in imagedata_dict["imagedata"].items():       
            print(str(pixelindex))
            if(isinstance(pixeldata, dict)): #Init Propertygroups of Palette
                pixeldataarray.append(pixeldata["R"])
                pixeldataarray.append(pixeldata["G"])
                pixeldataarray.append(pixeldata["B"])
                pixeldataarray.append(pixeldata["A"])


        useAdd=False

        if settingsdata.importmode_Image =="overwrite":
            if(name in bpy.data.images):      
                if(bpy.data.images[name].size[0] == width and bpy.data.images[name].size[1] == height):
                    newimage =bpy.data.images[name]
                    newimage.pixels[:] = pixeldataarray #Write Pixeldata inside
                else:
                    useAdd=True
            else:            
                useAdd=True

        if settingsdata.importmode_Image =="add" or useAdd:
            for i in range(999): #recreate name if image already exists
                if (name in bpy.data.images):
                    name + "_"+str(i).zfill(3)
                else: 
                    break
            newimage = bpy.data.images.new(name=name , width=width, height=height)
            newimage.pixels[:] = pixeldataarray #Write Pixeldata inside

        if(newimage):
            newimage.pixels[:] = pixeldataarray #Write Pixeldata inside
        else:
            return None
        
        return newimage

def loadSettings(self, ctx):
    printLog(subtype=LOGTYPE.START)
    palette=return_CurrentPalette()
    check=availabilityCheck(palette)

    settingsdata=ctx.scene.uv_palettes_settings_data
    file_path = settingsdata.settingsPath
    printLog(subtype=LOGTYPE.ONECALL, msg="Path: "+file_path)
    #Load File
    if not os.path.exists(file_path):
        printLog(subtype=LOGTYPE.ERROR, msg="Path not Valid")
        return None
    
    

    property_dict = load_settings_from_file(file_path)

    if(not isinstance(property_dict, dict)):
        printLog(subtype=LOGTYPE.ERROR, msg="Couldnt Extracts Data")
        return None

    #Init Checks
    runLoad_Settings=False
    runLoad_Palette=False
    runLoad_Image=False
    targetimage=None
    isNewPalette=False
    targetpalette=None
    #Settings Enum Selection
    if settingsdata.importmode_Settigs=="load": 
        runLoad_Settings=True

    #Palette Enum Selection
    if settingsdata.importmode_Palette=="new": 
        print("NEW")
        targetpalette = ctx.scene.uv_palettes.add()
        ctx.scene.uv_palettes_index = len(ctx.scene.uv_palettes)-1 #select the newly created Palette
        isNewPalette=True
        runLoad_Palette=True
    
    if settingsdata.importmode_Palette in ["groups_only", "complete", "current"] and check["Palette"]: #write into current one, masking happens inside the function for now
        targetpalette=return_CurrentPalette()#select current 
        runLoad_Palette=True
 
    if settingsdata.importmode_Palette in ["clean"]: #deletes all panels and adds one new
        ctx.scene.uv_palettes.clear()
        targetpalette=ctx.scene.uv_palettes.add()
        isNewPalette=True
        runLoad_Palette=True

    #Group Enum Selection is inside the load Palettes for now
    #if(settingsdata.importmode_Groups in ["groups_only","find","current"])

    #the Real Image Enum Selection in load Image
    
    #if(targetpalette):

    if(settingsdata.importmode_Image in ["add", "overwrite"]):
        runLoad_Image=True

    #Load data
    if(runLoad_Settings):
        load_settings_data(property_dict, settingsdata ,ctx)

    if(runLoad_Palette):
        load_palette_data(property_dict, ctx, settingsdata , isNewPalette, targetpalette) #Loads Palette into Project
    
    if(runLoad_Image):
        targetimage=load_image_data(property_dict, ctx, settingsdata, palette) #Loads image as File into Project

    if(settingsdata.importmode_Palette in ["group only","new","complete","find","current"]):
        if(settingsdata.importmode_Image_setImage  == "auto"): #Set Image if is possible
            if(targetpalette):
                if(targetimage):
                    if(not targetpalette.img):
                        targetpalette.img=targetimage

        if(settingsdata.importmode_Image_setImage  == "set"): #Set Image if is possible
            targetpalette.img=targetimage
            if(targetpalette.p_loaded): #Unload if it was loaded, because it need to reload the Color Previews
                targetpalette.p_loaded=False



    if not os.path.exists(file_path): #Save Preset Locally

        #Generate Path for Local Save
        filename= os.path.basename(file_path)
        current_directory = os.path.dirname(__file__)
        settings_presets_directory = os.path.join(current_directory, "settings_presets")
        settings_file_directory = os.path.join(settings_presets_directory, filename+".json")
        
        #save_property_group(settings_file_directory, settingsdata)
        with open(settings_file_directory, 'w') as f:
            json.dump(property_dict, f)
        printLog(subtype=LOGTYPE.FINISH)

    return None

#endregion <LoadingMethods>    

class UVC_PopupBuffer(bpy.types.PropertyGroup):
    """Stores Properties for Popup Action"""
    confirmed: bpy.props.BoolProperty(name="Confirmed", description ="when action is Confirmed",default=False, update=actionReturn)
    actiontext: bpy.props.StringProperty(name="Action Text", description ="Text of Action",default="", update=actiontextWasSet)
    actiontextWasSet: bpy.props.BoolProperty(name="Actiontext was Set", description ="when action text was set on Action",default=False)

class UVC_Group_settingspresets(bpy.types.PropertyGroup):
    """Stores Settings"""
    settingsFilename: bpy.props.StringProperty(name="Current Path of Settings if exist", description ="toLoadTh",default="Load settings when using Reload or Load Button")
    settingsFilenameOnly : bpy.props.StringProperty(name="Filename", description ="Presets File Name",default="unnamed_preset", )

#Propertygroup (settings)

class UVC_Data_Settings(bpy.types.PropertyGroup):
    """Stores Settings"""
    settingsTitle: bpy.props.StringProperty(name="Settings Name", description ="UI and FIlename of the Preset",default="userpreset")
    settingsPath: bpy.props.StringProperty(name="Current Path of Settings if exist", description ="toLoadTh",default="Load settings when using Reload or Load Button", update=loadSettings)
    settingsPathPre: bpy.props.StringProperty(name="Settings Path", description ="Loadingpath of the Settingsfile, will Update Settings when Changed",default="")
 
    settingspresets: bpy.props.CollectionProperty(name="Settings Presets", type=UVC_Group_settingspresets)
    settingspresets_index: bpy.props.IntProperty(name="settingspresets index")

    settingsDisplay: bpy.props.EnumProperty(
        
        items=[
            ('debug', '', 'Shows Debug Settings','CONSOLE', 0),
            ('info', '', 'Shows Extra Settings','SEQ_STRIP_META', 1),
            ('collapse', '', 'Collapses all the Menus','FULLSCREEN_EXIT', 2),
        ],
        name="menu",
        description="Which Settings Menu to Display",
        default='collapse',
    )

    showSettings: bpy.props.BoolProperty(name="Show Settings", description ="Show Settings",default= False)

    colorwheelDisplayType: bpy.props.EnumProperty(
        items=[
            ('horizontal', 'H', 'Hozizontal From Left to Right', 'ARROW_LEFTRIGHT', 1),
            ('vertcial', 'V', 'Vertical Top to Bottom', 'EMPTY_SINGLE_ARROW', 2),
            ('grouped', 'G', 'Grouped, Aligned Together', 'LIGHTPROBE_GRID', 3),
            ('singlefield', 'S', 'Single One per Pie Section(8Max!)', 'IMGDISPLAY', 4),
        ],
        name=" ",
        description="Which way the Colorwheel should Display Color",
        default='grouped'
    )

    panelGridType: bpy.props.EnumProperty(
        items=[
            ('ordered', 'Order', 'Order like Texture', 'LINENUMBERS_ON', 1),
            ('fill', 'Free', 'Fills up the Space', 'EMPTY_SINGLE_ARROW', 2),
        ],
        name=" ",
        description="Which way the Panel should Display Color",
        default='ordered'
    )

    defaultMaterialSetMode: bpy.props.EnumProperty(
        items=[
            ('disabled', 'Disabled', '', 'X', 1),
            ('auto', 'Auto', 'Adds Material if Object has No Materials asssigned', 'FILE_NEW', 2),
            ('add', 'Add', 'Adds default Material if its not added yet', 'FILE_TICK', 3),
            ('set', 'Set', 'Forces to make the default Material the Only Material', 'DECORATE_ANIMATE', 4),
        ],
        name="Mode",
        description="When to Activate",
        default='auto'
    )

    subtools: bpy.props.EnumProperty(
        items=[
            ('menus', 'Menus', 'Menus', '', 1),#BRUSHES_ALL
            ('select', 'Select', 'Select Tools', '', 2),    #GROUP_VERTEX
            ('general', 'General', 'General Tools', '', 3),#SHORTDISPLAY
            ('collapse', '', 'Collapses all the Menus','FULLSCREEN_EXIT',4),
        ],
        name="Tool Section",
        description="When to Activate",
        default='collapse'
    )
    
    settingsmenu: bpy.props.EnumProperty(
        items=[
            ('colorwheel', 'xx', 'xx', '', 1),#BRUSHES_ALL
            ('toolmenu', 'xx', 'xx', '', 2),    #GROUP_VERTEX
            ('activecolor', 'xx', 'xx', '', 3),#SHORTDISPLAY
            ('colorshift', '', 'xx','',4),
            ('colorpanel', '', 'xx','',5),
            ('groups', '', 'xx','',6),
            ('groupsdisplay', '', 'xx','',7),
            ('rotationtool', '', 'xx','',8),
            ('setdefaultmaterial', '', 'xx','',9),
            ('setdefaulttexture', '', 'xx','',10),
            ('panellist', '', 'xx','',11),
            ('grouplist', '', 'xx','',12),
            ('selectcolor', '', 'xx','',13),
            ('pivottool', '', 'xx','',14),
            ('none', '', 'xx','',15),

            
        ],
        name="Tool Section",
        description="When to Activate",
        default='none'
    )
    
    #How Colors are Displayed
      
    displayGrid: bpy.props.BoolProperty(description ="Allow Grid Selection",default= True)
    autoGrid: bpy.props.BoolProperty(description ="Disable Grid when Colorgroup Filter Colors",default= True)
    
    #When Groups are Enabled
    
    showColorgroupList_alwaysActive: bpy.props.BoolProperty(name="Show 'Always Active'", description ="This will Show/Hide the Option in each Colorgroup Element in the List (default Off)",default= False,)
    showColorgroupList_inverted: bpy.props.BoolProperty(name="Show 'Invert'", description ="This will Show/Hide the Option in each Colorgroup Element in the List (default Off)",default= False)
    
    #Locking or Hiding Colors
    
    #showColorgroupList_lock: bpy.props.BoolProperty(name="[MASK] Show <Disable Color> in Menu",default= False)
    showColorgroupList_hideColors: bpy.props.BoolProperty(name="Show 'Hide Colors'", description ="This will Show/Hide the Option in each Colorgroup Element in the List (default Off)",default= False)

    #Adding to Colorwheel or Quickselect
    
    showColorgroupList_addToColorwheel: bpy.props.BoolProperty(name="Show 'Add to Colorhweel'", description ="This will Show/Hide the Option in each Colorgroup Element in the List (default On)",default= True)
    showColorgroupList_addToColorshift: bpy.props.BoolProperty(name="Show 'Add to Colorshift'", description ="This will Show/Hide the Option in each Colorgroup Element in the List (default Off)",default= True)
    
    #Behavior for Selectiontools 
    
    showColorgroupList_applyOnTool_Selection: bpy.props.BoolProperty(name="Show 'Apply on Tool Selection'", description ="This will Show/Hide the Option in each Colorgroup Element in the List (default Off)",default= False)
    showColorgroupList_applyOnTool_Deselection: bpy.props.BoolProperty(name="Show 'Apply on Tool Deselection'", description ="This will Show/Hide the Option in each Colorgroup Element in the List (default Off)",default= False)
    showColorgroupList_applyOnTool_ColorShift: bpy.props.BoolProperty(name="Show 'Apply on Tool Colorshift'", description ="This will Show/Hide the Option in each Colorgroup Element in the List (default Off)",default= False)
    
    
    showColorgroupList_LayerOperation: bpy.props.BoolProperty(name="XXX", description ="This will Show/Hide the Option in each Colorgroup Element in the List",default= False)

    #Show/Hide Panel or Group Buttons/Panels
    
    showPanels: bpy.props.BoolProperty(name="Show/Hide Panels", description ="Hide Panel List in UI",default= True)
    showGroups: bpy.props.BoolProperty(name="Show/Hide Groups", description ="Hide Group List in UI",default= False)
    
    showDeletebutton_Colorgroup: bpy.props.BoolProperty(name="Show Colorgroup Delete Button", description ="Will Show/Hide the Button in the Palettes Menu",default= True)
    showAddbutton_Colorgroup: bpy.props.BoolProperty(name="Show Colorgroup Add Button", description ="Will Show/Hide the Button in the Palettes Menu",default= True)
    
    #What to Display in the Tool Menu 
    
    selectSimilar_in_ToolMenu: bpy.props.BoolProperty(name="Show Select Color", description ="Will Show/Hide the Button in the 'ToolMenu' (popup)Menu",default= True)
    deselectSimilar_in_ToolMenu: bpy.props.BoolProperty(name="Show Deselect Color", description ="Will Show/Hide the Button in the 'ToolMenu' (popup)Menu",default= True)
    
    colorshiftUp_in_ToolMenu: bpy.props.BoolProperty(name="Display in Toolmenu",default= True)
    colorshiftDown_in_ToolMenu: bpy.props.BoolProperty(name="Display in Toolmenu",default= True)
    
    setDefaultMaterial_in_ToolMenu: bpy.props.BoolProperty(name="Show Set Default Material", description="Will Show/Hide the Button in the 'ToolMenu' (popup)Menu",default= False)
    setActiveColor_in_ToolMenu: bpy.props.BoolProperty(name="Display in Toolmenu",default= True)
    # SelectSimilar_in_ToolMenu: bpy.props.BoolProperty(name="Display in Toolmenu",default= True)
    # SelectSimilar_in_ToolMenu: bpy.props.BoolProperty(name="Display in Toolmenu",default= True)
    # SelectSimilar_in_ToolMenu: bpy.props.BoolProperty(name="Display in Toolmenu",default= True)

    #Settings for Material Add Behavior
    emptySlotAction: bpy.props.EnumProperty(
        items=[
            ('keep', 'Keep', 'Handle Empty Slots like all Material slots', '', 1),#BRUSHES_ALL
            ('ignore', 'Ignore', 'Ignore the Slots in Tool Execution, the Auto mode will threat them as they arent there', '', 2),    #GROUP_VERTEX
            ('remove', 'Remove', 'Remove them Automatically', '', 3),#SHORTDISPLAY
        ],
        name="Empty Slot Action",
        description="Action to Execute when a Color is Set",
        default='ignore'
    )

    showSetTexture: bpy.props.BoolProperty(name="Show Set Texture Color", description ="Will Show/Hide the Button in the 'ToolMenu' (popup)Menu",default= False)
    convertColorspace: bpy.props.BoolProperty(name="Convert to sRGB", description ="Will Convert from Linear to sRGB colorspace when creating the PreviewImages",default= False)
    
    #What to Display in the Tool Menu 
    


    showgroupsOtherSettings: bpy.props.BoolProperty(name="Show More Settings", description="Show Settings",default= False)
    advancedSettings: bpy.props.BoolProperty(name="Show Advanced Settings", description="Only Change them if you know what you do!",default= False)

    export_Settings: bpy.props.BoolProperty(name="Export Settings'", description ="",default= False)
    export_Palette: bpy.props.BoolProperty(name="Export Current Palette", description ="",default= False)
    export_Image: bpy.props.BoolProperty(name="Export Image", description ="",default= False)

    importmode_Settigs: bpy.props.EnumProperty(
        items=[
            ('off', 'Off', 'Dont Load Settings', '', 1),
            ('load', 'Load', 'Load Settings', '', 2),
           
        ],
        name="Settings Load Mode ",
        description="How to Load Palette",
        default='load'
    )


    importmode_Palette: bpy.props.EnumProperty(
        items=[
            ('off', 'Off', 'Dont Load Palettes', '', 1),
            ('groups_only', 'Groups to Active', 'Loads just the Groups into the current Palette', '', 2),
            ('new', 'New', 'Always Creates a New Palette (adds _import to name)', '', 3),
            ('complete', 'Complete', 'Create new Palette if none exist with the same Name', '', 4),
            ('find', 'Overwrite', 'Find Palette with Name and Overwrite', '', 5), 
            ('current', 'Current', 'Overwrite current Selected', '', 6),    
            ('clean', 'Clean', 'Make the Load the Only Palette (Deletes other Palettes!)', '', 7),
        ],
        name="Palette Load Mode ",
        description="How to Load Palette",
        default='new'
    )

    importmode_Groups: bpy.props.EnumProperty( #On Existing Data if using the importmode_palette==[groups_only,find,current]
        items=[
            ('off', 'Off', 'Dont add Groups', '', 1), 
            ('auto', 'Auto', 'creates Groups if they dont exist yet \n  (will default to "New" Mode if Palette is new)', '', 2),
            ('add', 'New', 'Creates new Groups', '', 3),
            ('modify', 'Modify', 'Dont add, only Modify if Group Exists  \n (will default to "New" Mode if Palette is new)', '', 4), 
            ('clean', 'Clean', 'Makes the Groups the only Groups', '', 5),
        ],
        
        name="Groups Load Mode ",
        description="How to Load Groups into a Palette",
        default='add'
    ) 
    importmode_Image: bpy.props.EnumProperty(
        items=[
            ('off', 'Off', 'Do not Import the Image', '', 1),
            ('add', 'New', 'Creates a New Blender Image Instance', '', 2),
            ('overwrite', 'Find', 'Overwrites the Pixels of the Existing Image if it matches the size or uses Add Mode', '', 3),  
        ],
        
        name="Image Load Mode ",
        description="How to Load the Image",
        default='add'
    )

    importmode_Image_setImage: bpy.props.EnumProperty(
        items=[
            ('off', 'Off', 'Do not Import the Image', '', 1),
            ('auto', 'Auto', 'Adds the image if none is Set yet', '', 2),
            ('Set', 'Set', 'Sets the image to the Palette', '', 3),  
        ],
        
        name="Set image to Palette",
        description="Set the Image to a Palette when loaded",
        default='auto'
    )
    
    imageExportMode: bpy.props.EnumProperty(
        items=[
            ('standard', 'Standard', 'Exports Image in original Size, ca cause Lag!', '', 1),
            ('tilesize', 'Tilesize', 'Store image in Optimized Size based on Tilecounts on current Palette', '', 2),
        ],
        
        name="Image Compress Type",
        description="How the Image is Stored to the Presetfile",
        default='tilesize'
    )

    presetSubmenu: bpy.props.EnumProperty(
        items=[
            ('presetlist', 'Preset', 'Show Preset Load Menu', '', 1),
            #('import', 'Import', 'Show Import Menu', '', 2),
            ('export', 'Export', 'Show Export Menu', '', 2),
            #('info', '', 'Informations', 'DESKTOP', 3),
            ('collapse', '', 'Collapse/Hide All Preset menus', 'FULLSCREEN_EXIT', 3),
        ],
        
        name="Select Which menu to Show",
        description="The Preset Menu allows you to Export and Import Presets and then Load them Globally from all your Projects",
        default='collapse'
    )
    
    direction: bpy.props.EnumProperty(
        items=[
            ('x', 'X', 'X', '', 1),
            ('xn', 'X-', 'X-', '', 2),    
            ('y', 'Y', 'Y', '', 3),
            ('yn', 'Y-', 'Y-', '', 4),    
            ('z', 'Z', 'Z', '', 5),
            ('zn', 'Z-', 'Z-', '', 6),    
        ],
        name="Which Direction",
        description="Which Direction to set the Pivot",
        default='zn'
    )
    
    transformspace: bpy.props.EnumProperty(
        items=[
            ('objectspace', 'Object', 'Direction by Objectspace', '', 1),
            ('worldspace', 'World', 'Direction by Worldspace', '', 2),    
            ('auto', 'Auto', 'Will Clip the Objectrotation by the most fitting Worldspace direction', '', 3),
        ],
        name="Which Direction",
        description="Which Direction to set the Pivot",
        default='objectspace'
    )
    showPresetLoadSettings : bpy.props.BoolProperty(name="Show Settings for Loading", description ="Options to Control what to Import from the Preset",default= False)
    cleanSplitNormals : bpy.props.BoolProperty(name="Clear Split Normals", description ="Clears Split Normals before resharpening",default= False)
    autosmooth : bpy.props.BoolProperty(name="Autosmooth", description ="Sets the Objects to Smooth Automatically",default= False)
    
    #Float Property called splitangle
    splitangle : bpy.props.FloatProperty(name="Split Angle", description ="Angle to Split Normals",default= 30, min=0, max=180, update = splitNormals)
    gridspacing : bpy.props.FloatProperty(name="Split Angle", description ="Angle to Split Normals",default= 1.0, min=0.0, max=2,)
    showSelection : bpy.props.BoolProperty(name="Show Selection", description ="Show Selection",default= False)

# ==================================================================================
# ||                                Palette Operator                               ||
# ==================================================================================
# || Description: Function to Manage Palette Tools                                 ||
# ==================================================================================


#create regions for UI design optimization functions:
#region <UIReturns> <Menus>    

#endregion <UIReturns> 

#region <SettingsMenuAccess> <Menus>    

#Method that uses a dict to return 2 
    
class UVC_Operator_Settings_accessSettingsView(bpy.types.Operator):
    bl_idname = "wm.uvc_settings_access"
    bl_label = "Open Settings"
    
    #String property to store the name of a element
    menuname: bpy.props.StringProperty(name="Name", default="")
    def execute(self, context):
        
        #set the active element to the name
        bpy.context.scene.uv_palettes_settings_data.settingsmenu=self.menuname
        bpy.context.scene.uv_palettes_settings_data.showSettings=True
    
        return {'FINISHED'}
    
class UVC_Operator_Settings_return(bpy.types.Operator):
    bl_idname = "wm.uvc_settings_return"
    bl_label = "Return to Previous Menu"
    
    def execute(self, context):
        
        bpy.context.scene.uv_palettes_settings_data.showSettings=False
        return {'FINISHED'}
    
#endregion <SettingsMenuAccess> 
                
#region <Openable_Menus> <Menus>            
            
       
#Colorwheel:        
class UVC_MT_Settings_Toolmenu(bpy.types.Menu):
    bl_label = "Tool Menu"
    bl_idname = "UVC_MT_Toolmenu"

    def draw(self, context):
        layout = self.layout
        
        # use an operator enum property to populate a sub-menu
        settingsdata=return_SettingsData()

        if(settingsdata.selectSimilar_in_ToolMenu):
            layout.operator(UVC_Operator_Settings_selectssimilar_operator.bl_idname, text="Select Color")
        if(settingsdata.deselectSimilar_in_ToolMenu):
            layout.operator(UVC_Operator_Settings_deselectssimilar.bl_idname, text="Deselect Color")
        
        if(settingsdata.setActiveColor_in_ToolMenu):
            layout.operator(UVC_Operator_Settings_setColorBySelected.bl_idname, text="Color by Selected")

        if(settingsdata.setDefaultMaterial_in_ToolMenu):
            layout.operator(UVC_Operator_Settings_addDefaultmaterial.bl_idname, text="adds default Material")
        # if(settingsdata.showSetTexture):
        #     layout.operator(UVC_Operator_Settings_addPaletteTexture.bl_idname, text="set Palette Texture")
        
        if(settingsdata.colorshiftUp_in_ToolMenu):
            layout.operator(UVC_Operator_ColorshiftUp.bl_idname, text="Quick Next")
        if(settingsdata.colorshiftDown_in_ToolMenu):
            layout.operator(UVC_Operator_ColorshiftDown.bl_idname, text="Quick Previous")
        # if(settingsdata.YYY):
        #     layout.operator(XXXX.bl_idname, text="XXXX")

class UVC_Operator_Settings_openToolMenu(bpy.types.Operator):
    """Opens Menu with Tools"""

    bl_idname = "wm.uv_colorizer_opentoolmenu"
    bl_label = "Open ToolMenu"

    def execute(self, ctx): #Bacially REmoves the Palette from the Palette, then removes the Palette and then selects the next possible Palette
        bpy.ops.wm.call_menu(name="UVC_MT_Toolmenu")
        return {'FINISHED'}  

class UVC_Operator_Settings_openColorWheel(bpy.types.Operator):
    """Selects faces with the same color as the ACTIVE face"""
    

    bl_idname = "wm.uv_colorizer_opencolorwheel"
    bl_label = "Open Colorwheel"

    def execute(self, ctx): #Bacially REmoves the Palette from the Palette, then removes the Palette and then selects the next possible Palette
        bpy.ops.wm.call_menu_pie(name="UVC_MT_Colorwheel")
        return {'FINISHED'}  
    
class UVC_Operator_Palette_setColor(bpy.types.Operator):
    """Selects faces with the same color as the ACTIVE face"""
    

    bl_idname = "uv_colorizer.setuv"
    bl_label = ""
    uvcoords: bpy.props.FloatVectorProperty("Col_Index", size=2, default=(0.0,0.0))

    def execute(self, ctx): #Bacially REmoves the Palette from the Palette, then removes the Palette and then selects the next possible Palette
        
        printLog(src="SetColorOperator", subtype=LOGTYPE.ONECALL, msg="Try Setting Color: "+str(self.uvcoords[0])+"/"+str(self.uvcoords[1]))
        bpy.ops.ed.undo_push(message = " Attempt Setting Color")
        op_setup_Color_On_Faces(self, ctx)
        
        return {'FINISHED'}  

#endregion <Openable_Menus>    

#region <SelectTools> <SelectTools Tools>
    
class UVC_Operator_Settings_selectssimilar_operator(bpy.types.Operator):
    """Selects faces with the same color as the ACTIVE face"""
    

    bl_idname = "wm.uvc_select_similar"
    bl_label = "Select Similar Color"

    def execute(self, ctx): #Bacially REmoves the Palette from the Palette, then removes the Palette and then selects the next possible Palette
        
        bpy.ops.ed.undo_push(message = "Attempt Selecting Similar Color")
        op_Select_By_Equal_Tile(self=self, context=ctx)
        bpy.ops.ed.undo_push(message = "Done Selecting Similar Color")
        

        return {'FINISHED'}  
    
class UVC_Operator_Settings_deselectssimilar(bpy.types.Operator):
    """Deselects faces with the same color as the ACTIVE face"""

    bl_idname = "wm.uvc_deselect_similar"
    bl_label = "Deselect Similar Color"

    def execute(self, ctx): #Bacially Removes the Palette from the Palette, then removes the Palette and then selects the next possible Palette
        printLog(src="SetDefaultMaterialOperator", subtype=LOGTYPE.ONECALL, msg="Attempt Adding Material")
        bpy.ops.ed.undo_push(message = "Attempt Deselecting Similar Color")
        
        op_Deselect_By_Equal_Tile(self=self, context=ctx)
        bpy.ops.ed.undo_push(message = "Done Deselecting Similar Color")
        
        return {'FINISHED'}  
    

#endregion <SelectTools>    

#region <SetColorBySelected> <SelectTools Tools>
    
    
def op_Set_Color_By_Selected(self, context):
    majority_segment = uv_Tilenumber_By_Active_Face_UV(self, context)
    
    palette = return_CurrentPalette()
    if palette is None:
        return None
    
    num_segments_x = palette.p_tilecountx
    num_segments_y = palette.p_tilecounty
    
    newUVPos = math_UVPosition_By_Tile(majority_segment[0], majority_segment[1], num_segments_x, num_segments_y)
    self.uvcoords=newUVPos
    op_setup_Color_On_Faces(self, context)
        
    
    
class UVC_Operator_Settings_setColorBySelected(bpy.types.Operator):
    """Selects faces with the same color as the ACTIVE face"""
    

    bl_idname = "wm.uvc_set_by_selected"
    bl_label = "Set the Color of Selected Faces by the Active Selection"
    uvcoords: bpy.props.FloatVectorProperty("Col_Index", size=2, default=(0.0,0.0))
    def execute(self, ctx): #Bacially REmoves the Palette from the Palette, then removes the Palette and then selects the next possible Palette
        
        bpy.ops.ed.undo_push(message = "Attempt Setting Similar Color")
        op_Set_Color_By_Selected(self=self, context=ctx)
        return {'FINISHED'}  
    


#endregion <SetColorBySelected> 

#region <SetMaterial> <Set Material Tool>

class UVC_Operator_Settings_addDefaultmaterial(bpy.types.Operator):
    """Deselects faces with the same color as the ACTIVE face"""

    bl_idname = "wm.uv_colorize_adddefaultmaterial"
    bl_label = "Add Default Material"
    byOperator: bpy.props.BoolProperty(name="IsCalledByOperator",default= False)

    def execute(self, ctx): #Bacially Removes the Palette from the Palette, then removes the Palette and then selects the next possible Palette
        self
        bpy.ops.ed.undo_push(message = "Attempt Adding Material")
        op_add_default_Material(self=self, context=ctx)  
        return {'FINISHED'}  

def op_add_default_Material(self, context, faces=None, obj=None):
    
    settingsdata=bpy.context.scene.uv_palettes_settings_data
    byOperator=False
    hasFaces=False
    inEditmode=bpy.context.object.mode == "EDIT"
    materialModeDisabled=settingsdata.defaultMaterialSetMode=="disabled"

    #Checks
    if(faces):
        if(not len(faces)<=0):
            hasFaces=True

    if(hasattr(self, "byOperator")):
        byOperator=True
  
    if not byOperator and materialModeDisabled: 
        return None #Skip if Disabled and not by Operator
    
    
    
    defaultMat = return_CurrentPalette().defaultmaterial #return if no Material to set
    if(defaultMat is None):
        return None #No Default
     
    objList=[] 
        
    if(obj and (not byOperator)):
        objList.append(obj)     
    else:
        objList=bpy.context.selected_objects
        hasFaces=False
        
        
    for obj in objList:   
    
        #Per Object
        hasDefaultMaterial=False
        hasNoMaterials=False
        mat_index = -1
        setFaces=False
        emptySlotsWhereFound=False
        hasOtherMaterials=False
        
        #Pre Cleanup
        
        # if(settingsdata.noneAsNoMaterial):
            
        #     bounds=len(obj.material_slots)
        #     for i, slot in enumerate((obj.material_slots)):
        #         if(i>=bounds-1):
        #             break
        #         if not slot.material:
        #             emptySlotsWhereFound=True
        #             if(settingsdata.autoRemoveNone):          
        #                 obj.data.materials.pop(index=i)
        #                 bounds=bounds-1
        #                 if(inEditmode):
        #                     bmesh.update_edit_mesh(obj.data)
        #         else:
        #             if slot.material != defaultMat:
        #                 hasOtherMaterials=True
        #Check
        if(len(obj.material_slots)<=0):
            hasNoMaterials=True    
                        
        if(not hasNoMaterials):
            for materialindex in reversed(range(len(obj.data.materials))):
                if not obj.material_slots[materialindex].material:
                    
                    if(settingsdata.emptySlotAction=="remove"):
                        obj.data.materials.pop(index=materialindex)
                    else:
                        if(settingsdata.emptySlotAction=="ignore"):
                            emptySlotsWhereFound=True
                else:
                    if obj.material_slots[materialindex].material == defaultMat:
                        hasOtherMaterials=True
                        


        hasOnlyOneMaterial=False

        #TO DO add function to detect "none" materials as no Materials
        if(not hasNoMaterials):
            if(len(obj.data.materials) <=1):
                hasOnlyOneMaterial=True
            
        #Find out if Object has the default Material already
        for i, slot in enumerate(obj.material_slots):
            if slot.material == defaultMat:
                mat_index = i
                
            
        #Check
        if(mat_index != -1):
            hasDefaultMaterial=True
            
        if(settingsdata.defaultMaterialSetMode=="auto"): #AUTO only add Material if none exists
            if((hasNoMaterials or emptySlotsWhereFound) and not hasDefaultMaterial): #add Material if not exist
                obj.data.materials.append(defaultMat)
                mat_index = len(obj.material_slots)


            if  (hasOtherMaterials or (emptySlotsWhereFound)): #Modify Faces if there was None Assignments
                if hasFaces:#Check
                    setFaces=True
            else:
                continue
    
        
        if(settingsdata.defaultMaterialSetMode=="add"): #ADD always add Material on Top
            if(not hasDefaultMaterial): #add Material if not exist
                obj.data.materials.append(defaultMat)
                mat_index = len(obj.material_slots)
            
            #Assign Material to Faces if any
            if hasFaces:#Check
                    setFaces=True
        
        
        if(settingsdata.defaultMaterialSetMode=="set"): #SET forces the default to be the only one
            if not (hasDefaultMaterial and hasOnlyOneMaterial): #Remove other Materials
                for materialindex in reversed(range(len( obj.data.materials))):
                    obj.data.materials.pop(index=materialindex)
                obj.data.materials.append(defaultMat) 
                mat_index = 0 

                if hasFaces:#Check
                    setFaces=True
                    

        
        if setFaces: #Set Face Material index if toggled from previous Checks
            for face in faces:
                face.material_index = mat_index      
        if(inEditmode):
            bmesh.update_edit_mesh(obj.data)
            
    return None #Done

class UVC_Operator_Settings_addPaletteTexture(bpy.types.Operator):
    """Adds Texture of the Palette to the Basecolor of the Material from the Selected Objects"""
    
    bl_idname = "wm.uv_colorize_addpalettetexture"
    bl_label = "Add Palette Color"
    byOperator: bpy.props.BoolProperty(name="IsCalledByOperator",default= False)

    def execute(self, ctx): #Bacially Removes the Palette from the Palette, then removes the Palette and then selects the next possible Palette
        bpy.ops.ed.undo_push(message = "Attempt Adding Texture")
        op_add_Texture_to_Material(self=self, context=ctx)
        return {'FINISHED'}  

def op_add_Texture_to_Material(self, context):
        
    palette=return_CurrentPalette()
    if(palette):
        print ("Start")    
            
        img = palette.img
        if(img is None):
            print ("None")    
            return None
        
        for obj in bpy.context.selected_objects:
            print ("obj")    
            if(len(obj.material_slots)<=0):
                print ("noslot")    
                continue
            
            
            material = obj.material_slots[obj.active_material_index].material

            material.use_nodes = True
            nodes = material.node_tree.nodes

            # Find or create the main shader node (Principled BSDF)
            node_base = None
            hasShaderNode=False
            if(nodes):
                for node in nodes:
                    if "Base Color" in node.inputs:
                        
                        hasShaderNode=True
                if(hasShaderNode):
                  
                    links = material.node_tree.links
                    for node in nodes:          
                        if "Base Color" in node.inputs:
                            input_name = "Base Color"
                            is_linked=True
                            #is_linked = any(link.from_socket.name == input_name and link.from_socket.type == 'RGBA' for link in node.inputs[input_name].links)
                            if (not is_linked):
                                node_tex = nodes.new('ShaderNodeTexImage')
                                node_tex.image=img
                                node_tex.name = "Palette_Texture"
                                node_tex.interpolation = "Closest"
                                node_tex.location = (node.location[0]-130,node.location[1])
                                link = links.new(node_tex.outputs["Color"], node.inputs["Base Color"])
       
            return {'FINISHED'}

    return None

#endregion <SetMaterial>    

#region <SelectTools_ByGroup> <Not Implemented>

class UVC_Operator_SelectByActiveGroups(bpy.types.Operator):
    """Toggles Logging On and Off, open Console under the Window Option"""

    bl_idname = "wm.uvc_tools_selectbyactivegroups"
    bl_label = "Select by Active Groups"

    def execute(self, ctx): #Bacially REmoves the Palette from the Palette, then removes the Palette and then selects the next possible Palette

        
        return {'FINISHED'}

class UVC_Operator_DeselectByActiveGroups(bpy.types.Operator):
    """Toggles Logging On and Off, open Console under the Window Option"""

    bl_idname = "wm.uvc_tools_deselectbyactivegroups"
    bl_label = "Deselect by Active Groups"

    def execute(self, ctx): #Bacially REmoves the Palette from the Palette, then removes the Palette and then selects the next possible Palette

        return {'FINISHED'}
  
#endregion <SelectTools_ByGroup>     
    
#region <Quickselect> <Quickselect Tools>    
    
class UVC_Operator_ColorshiftUp(bpy.types.Operator):
    """Toggles Logging On and Off, open Console under the Window Option"""

    bl_idname = "wm.uvc_tools_colorshiftup"
    bl_label = "Colorshift Next Color"
    directionUp: bpy.props.BoolProperty(name="IsCalledByOperator",default= True)
    def execute(self, ctx): #Bacially REmoves the Palette from the Palette, then removes the Palette and then selects the next possible Palette
        bpy.ops.ed.undo_push(message = "Attempt Colorshift Up")
        quickselect_updown(self=self, context=ctx)   
        return {'FINISHED'}

class UVC_Operator_ColorshiftDown(bpy.types.Operator):
    """Toggles Logging On and Off, open Console under the Window Option"""

    bl_idname = "wm.uvc_tools_colorshiftdown"
    bl_label = "Colorshift Previous Color"
    directionUp: bpy.props.BoolProperty(name="IsCalledByOperator",default= False)
    def execute(self, ctx): #Bacially REmoves the Palette from the Palette, then removes the Palette and then selects the next possible Palette
        bpy.ops.ed.undo_push(message = "Attempt Colorshift Down")
        quickselect_updown(self=self, context=ctx)
        return {'FINISHED'}
    
def op_quickselect():
    
    return None

def quickselect_updown(self, context):
    
    """ !METHOD!
    Sets the Color of the Selected Faces, is used by Operators Usually

    Keyword arguments:
    self, context                       N/A #
    Warning: Dont Log Operators!
    """
    
    directionIsUp=False
    if(self.directionUp):
        directionIsUp=True
        
    palette = return_CurrentPalette()
    if palette is None:
        return None
    
    num_segments_x = palette.p_tilecountx
    num_segments_y = palette.p_tilecounty

    # Check if the function is used via a Color Display Panel Button "active"

    # Check if Blender is in edit mode
    if bpy.context.object.mode == "EDIT":

        # Get selected objects in edit mode    
        for obj in bpy.context.selected_objects:
            if not obj.type == 'MESH':
                continue
         
            me = obj.data
            bm = bmesh.from_edit_mesh(me)

            # Get the active UV layer
            uv_lay = bm.loops.layers.uv.active

            # Initialize a list to store selected faces
            selected_faces = []

            # Iterate through faces to find selected ones
            for face in bm.faces:
                if face.select:
                    selected_faces.append(face)

            # Check if any faces are selected
            if len(selected_faces) == 0:
                continue
            
            
            op_add_default_Material(context, self, selected_faces, obj)#Materialadding by Settings

            filter = [[False for _ in range(num_segments_x)] for _ in range(num_segments_y)]
            
            for colindex in range(len(palette.colors)):
                filterposition=math_getTileFromUVXY(num_segments_x, num_segments_y,  palette.colors[colindex].uv[0],palette.colors[colindex].uv[1])
                if(filterposition[0]>-1,filterposition[1]>-1):
                    if(filterposition[0]<num_segments_x,filterposition[1]<num_segments_y):
                        filter[int(filterposition[0])][int(filterposition[1])]= gf_Col_inQuick(palette, colindex)
            indexcount=num_segments_x*num_segments_y    


            # Iterate through selected faces and update UV coordinates
            for face in selected_faces:
                for loop in face.loops:
                    #Implemented Change can be found here
                    
                    #get Color
                    position = math_getTileFromUV(num_segments_x, num_segments_y,  loop[uv_lay].uv)
                    
                    if(not position):
                        continue
                    #print("TileY : "+str(position[0]))
                    #print("TileX : "+str(position[1]))
                    
                    #Get Color and Request if Pixel is in Quickselect
                    pixelindex = img_getTilesetPixelIndex(position[0], position[1], num_segments_x)
                    
                    #print("Pixelindex by Position: "+str(pixelindex))
                    
                    #Continue if not
                    xC=int(pixelindex%num_segments_x)
                    yC=int(pixelindex//num_segments_x)
                    print("yC: "+str(yC)+" xC: "+str(xC)+" boolC: "+str(filter[xC][yC]))
                    if(not filter[xC][yC]):
                        #print("Skipped: "+str(pixelindex))
                        continue
                    #print(str(pixelindex))
                    
                    #find next Color in Quickselect
                    firstDone=False
                    
                    if(directionIsUp):
                        for i in range(indexcount):
                            iX=(i+pixelindex+1)%indexcount
                            x=int(iX%num_segments_x)
                            y=int(iX//num_segments_x)
                            print("y: "+str(y)+" x: "+str(x)+" bool: "+str(filter[x][y]))
                            if filter[x][y]:
                                
                                loop[uv_lay].uv = math_UVPosition_By_Tile(x, y, num_segments_x, num_segments_y)
                                break
        
                            
                    else:
                        for i in reversed(range(indexcount)):
                            iX=(i+pixelindex)%indexcount
                            x=int(iX%num_segments_x)
                            y=int(iX//num_segments_x)
                            print("y: "+str(y)+" x: "+str(x)+" bool: "+str(filter[x][y]))
                            if filter[x][y]:
                                
                                loop[uv_lay].uv = math_UVPosition_By_Tile(x, y, num_segments_x, num_segments_y)
                                break
                   
                            
                    # position = math_getTileFromUVXY(num_segments_x, num_segments_y,  palette.colors[pixelindex].uv[0], palette.colors[pixelindex].uv[1])
                    # if(not position):
                    #     continue
                    
                    # targetuv=math_UVPosition_By_Tile(position[0], position[1], num_segments_x, num_segments_y)
                    # print("Tile2Y : "+str(position[0]))
                    # print("Tile2X : "+str(position[1]))   
                    
                    # print("Setting Color by Index: "+str(pixelindex))
                    # loop[uv_lay].uv = targetuv
                    #End Change
                    #loop[uv_lay].uv = targetuv

            # Update the mesh data
            #bm.select_flush(True)
            bmesh.update_edit_mesh(obj.data)
            

            

    
    
    return None

#endregion <Quickselect>    

#region <Groups_AddRemoveEdit> <Managing Groups>

class UVC_Operator_Palette_colorgroup_add(bpy.types.Operator):
    """Adds a Colorgroup"""

    bl_idname = "uv_colorize.add_colorgroup"
    bl_label = "Add UV Colorgroup"
    def execute(self, ctx): #Bacially REmoves the Palette from the Palette, then removes the Palette and then selects the next possible Palette
        bpy.ops.ed.undo_push(message = "Attempt Adding Colorgroup")
        addColorgroup()
        
        return {'FINISHED'}

def addColorgroup():
        functionname="AddColorgroup"
        printLog(src=functionname, subtype=LOGTYPE.ONECALL)
        palette=return_CurrentPalette()
        colorgrouplist= palette.colorgroups    
        newcolorgroup = colorgrouplist.add()
        palette.selectedcolorgroup = max(min(palette.selectedcolorgroup, len(palette.colorgroups)-1), 0)
        #setup colorgroupdata
        for i in range( palette.p_tilecountx * palette.p_tilecounty):
            newcolorgroup.colorgroupdata.add()
        printLog(src=functionname, subtype=LOGTYPE.INFO,msg="Colorgroup Data Created")

class UVC_Operator_Palette_colorgroup_config(bpy.types.Operator):
    """Enters or Exits Editmode of Current Colorgroup"""

    bl_idname = "uv_colorize.config_colorgroup"
    bl_label = "Configurate UV Colorgroup"

    def execute(self, ctx): 
        
        if(return_CurrentPalette().p_editcolorgroups):
            if(bpy.context.scene.uv_palettes_settings_data.settingsmenu=="grouplist" and bpy.context.scene.uv_palettes_settings_data.showSettings):
                bpy.context.scene.uv_palettes_settings_data.settingsmenu="none"
                bpy.context.scene.uv_palettes_settings_data.showSettings=False
            
        else:
            bpy.context.scene.uv_palettes_settings_data.settingsmenu="grouplist"
            bpy.context.scene.uv_palettes_settings_data.showSettings=True
  
                
        return_CurrentPalette().p_editcolorgroups=not return_CurrentPalette().p_editcolorgroups
        printLog(src="ConfigColorgroupToggle", subtype=LOGTYPE.ONECALL)
        return {'FINISHED'}

class UVC_Operator_Palette_colorgroup_remove(bpy.types.Operator):
    """Removes Colorgroup"""

    bl_idname = "uv_colorize.remove_colorgroup"
    bl_label = "Remove UV Colorgroup"

    def execute(self, ctx): #Bacially REmoves the Palette from the Palette, then removes the Palette and then selects the next possible Palette
        functionname="RemoveColorgroup"
        printLog(src=functionname, subtype=LOGTYPE.ONECALL)

        palette=return_CurrentPalette()
        colorgrouplist= palette.colorgroups
        selcolorgroup=palette.selectedcolorgroup
        if len(colorgrouplist) > 0: 
            bpy.ops.ed.undo_push(message = "Attempt Deleting Colorgroup")
            colorgrouplist.remove(selcolorgroup)
            
            palette.selectedcolorgroup = max(min(selcolorgroup, len(colorgrouplist)-1), 0)
            
        else:
            printLog(src=functionname, subtype=LOGTYPE.ERROR,msg="No Colorgroup")    

        return {'FINISHED'}

#endregion <Groups_AddRemoveEdit>    

#region <Debugmenu> <Debugging Options>

class UVC_Operator_Settings_toggleLog(bpy.types.Operator):
    """Toggles Logging On and Off, open Console under the Window Option"""

    bl_idname = "wm.uvc_settings_toggledeeplog"
    bl_label = "Toggle Deep Log"

    def execute(self, ctx): #Bacially REmoves the Palette from the Palette, then removes the Palette and then selects the next possible Palette
        functionname="ToggleLogging"
        global deeplog

        if deeplog:
            printLog(src=functionname, subtype=LOGTYPE.INFO, msg="Logging is now: Disabled" )
        
        deeplog=not deeplog

        if deeplog:
            printLog(src=functionname, subtype=LOGTYPE.INFO, msg="Logging is now: Enabled" )
        
        return {'FINISHED'}

class UVC_Operator_Settings_toggleConsole(bpy.types.Operator):
    bl_idname = "wm.uvc_toggle_console"
    bl_label = "Toggle System Console"
    
    def execute(self, context):
        bpy.ops.wm.console_toggle()
        return {'FINISHED'}

class UVC_Operator_Settings_printPath(bpy.types.Operator):
    bl_idname = "wm.uvc_settings_print_paths"
    bl_label = "Print Addons Path"

    def execute(self, context):
        addons_path = bpy.utils.user_resource("SCRIPTS")
        print("Blender Addons Path:", addons_path)

        addons_path = bpy.utils.user_resource("CONFIG")
        print("Blender Config Path:", addons_path)

        addons_path = bpy.utils.user_resource("AUTOSAVE")
        print("Blender Autosave Path:", addons_path)

        addons_path = bpy.utils.user_resource("DATAFILES")
        print("Blender Datafiles Path:", addons_path)

        addon_folder = os.path.dirname(__file__)
        print("This Addons Path:", addon_folder)


        return {'FINISHED'}

#endregion <Debugmenu>    

#region <SettingPresets_Import> <Importing Presets>

def copyData(self, context):
    settingsdata=bpy.context.scene.uv_palettes_settings_data
    property_dict=None
    newfilepath=self.settings_path
    if os.path.isdir(newfilepath):
        
        with open(newfilepath, 'r') as f:
            property_dict = json.load(f)


        filename= os.path.basename(newfilepath)
        current_directory = os.path.dirname(__file__)
        settings_presets_directory = os.path.join(current_directory, "settings_presets")
        settings_file_directory = os.path.join(settings_presets_directory, filename+".json")
        
        if(not property_dict is None ):
            with open(settings_file_directory, 'w') as f:
                json.dump(property_dict, f)
            refreshPresets(self=self, context=context)    
            settingsdata.presetSubmenu="presetlist"
        
            
    return None    

#endregion <SettingPresets_Import>    

#region <SettingPresets_Saving> <Saving Presets>
class UVC_Operator_Settings_openDirectoryDirectory(bpy.types.Operator):
    bl_idname = "wm.uvc_settings_openpresetdirectory"
    bl_label = "Open Preset Folder"
    
    def execute(self, context):
        current_directory = os.path.dirname(__file__)
        settings_presets_directory = os.path.join(current_directory, "settings_presets")
        open_file_explorer(settings_presets_directory)
        return {'FINISHED'}
    
class UVC_Operator_Settings_importPreset(bpy.types.Operator):
    bl_idname = "wm.uvc_settings_importpresetfile"
    bl_label = "Import Settings Preset into Addons Folder"
    settings_path: bpy.props.StringProperty(name="Settings Path", default="")

    def execute(self, context):
        current_directory = os.path.dirname(__file__)
        settings_presets_directory = os.path.join(current_directory, "settings_presets")
        self.settings_path=settings_presets_directory
        return {'FINISHED'}
    
    def invoke(self, context, event):
        default_directory = os.path.dirname(self.settings_path)
        context.window_manager.fileselect_add(self)
        copyData(self=self, context=context)
        return {'RUNNING_MODAL'}
    
    def draw(self, context):
        pass

class UVC_Operator_Settings_savesettings(bpy.types.Operator):
    bl_idname = "wm.uvc_settings_save"
    bl_label = "Save Settings Preset"
    
    def execute(self, context):
        savesettings()
        refreshPresets(self=self, context=context)
        return {'FINISHED'}
    
def savesettings():# Get the directory of the currently executed file
    #get Settings
    settingsdata=bpy.context.scene.uv_palettes_settings_data
    # Construct the path to the "settings_presets" folder
    if settingsdata.settingsTitle=="default":
        printLog(subtype=LOGTYPE.ERROR, msg="Cant Overwrite Default!, Change Settings in the Files Directly instead or Overwrite Manually!")
        return None

    current_directory = os.path.dirname(__file__)
    settings_presets_directory = os.path.join(current_directory, "settings_presets")
    settings_file_directory = os.path.join(settings_presets_directory, settingsdata.settingsTitle+".json")

    #SaveSettings to File
    save_property_group(settings_file_directory, settingsdata)
    return None

# Function to save property group to JSON file
def save_property_group(filepath, property_group):
    #prop_dict = property_group_to_dict(property_group)
    settingsdata=bpy.context.scene.uv_palettes_settings_data
    palette=return_CurrentPalette()
    check = availabilityCheck(palette)

    exportSettings=settingsdata.export_Settings
    exportPalette=settingsdata.export_Palette
    exportImage=settingsdata.export_Image

    if(not check["Palette"]):
        exportPalette=False

    if(not check["Image"]):
        exportImage=False
    

    if(exportSettings):
        settings_dict = {
            #Displaytypes
            "settingsDisplay": settingsdata.settingsDisplay,
            "colorwheelDisplayType": settingsdata.colorwheelDisplayType,
            "panelGridType": settingsdata.panelGridType,

            #"displayGrid": settingsdata.displayGrid, deprecated
            #"autoGrid": settingsdata.autoGrid, deprecated

            #Show
            "showColorgroupList_alwaysActive": settingsdata.showColorgroupList_alwaysActive,
            "showColorgroupList_inverted": settingsdata.showColorgroupList_inverted,
            "showColorgroupList_hideColors": settingsdata.showColorgroupList_hideColors,

            #Add
            "showColorgroupList_addToColorwheel": settingsdata.showColorgroupList_addToColorwheel,
            "showColorgroupList_addToColorshift": settingsdata.showColorgroupList_addToColorshift,

            #Tooldisplay
            "showColorgroupList_applyOnTool_Selection": settingsdata.showColorgroupList_applyOnTool_Selection,
            "showColorgroupList_applyOnTool_Deselection": settingsdata.showColorgroupList_applyOnTool_Deselection,
            
            #Show Layer Operation
            "showColorgroupList_LayerOperation": settingsdata.showColorgroupList_LayerOperation,
            
            #Show Hide Panels Groups and Buttons
            "showPanels": settingsdata.showPanels,
            "showGroups": settingsdata.showGroups,
            
            #In Tool Menu
            "selectSimilar_in_ToolMenu": settingsdata.selectSimilar_in_ToolMenu,
            "deselectSimilar_in_ToolMenu": settingsdata.deselectSimilar_in_ToolMenu,
            "setDefaultMaterial_in_ToolMenu": settingsdata.setDefaultMaterial_in_ToolMenu,
            "defaultMaterialSetMode": settingsdata.defaultMaterialSetMode,
            "emptySlotAction": settingsdata.emptySlotAction,
            
            "showSetTexture": settingsdata.showSetTexture,
            "advancedSettings": settingsdata.advancedSettings,
            "convertColorspace": settingsdata.convertColorspace

    }

    if(exportPalette):
        palette_dict = { #Palette Without Group
            #needs to be set in Import: #
            #will be added in next parts : #+
            #will be added but is special: #++

            #"colors" : palette.xxx,
            #+"img" : palette.xxx,
            #"oldimg" : palette.xxx,
            #"preview" : palette.xxx,
            #"index" : palette.index, 
            #"defaultmaterial" : palette.xxx,

            #++"colorgroups" : palette.xxx,

            "selectedcolorgroup" : 0,
            "colorgroupLayermode" : palette.colorgroupLayermode,
            
            "p_loaded" : False,
            "p_editcolorgroups" : False,

            "pe_scalex" : palette.p_scale[0],
            "pe_scaley" : palette.p_scale[1],
            "pe_offsetx" : palette.pe_offsetx,
            "pe_offsety" : palette.pe_offsety,
            "pe_tilecountx" : palette.pe_tilecountx,
            "pe_tilecounty" : palette.pe_tilecounty

            #colorwillbe reloaded

            
        }

        groups_dict = {
    
        }

        for i in range(len(palette.colorgroups)): #Load Single Groups
            colorgroup=palette.colorgroups[i]
            group_dict = {
                "title" : colorgroup.title,
                "alwaysActive": colorgroup.alwaysActive,
                "inverted" : colorgroup.inverted,
                "lock" : colorgroup.lock,
                "hideColors" : colorgroup.hideColors,
                "addToColorwheel" : colorgroup.addToColorwheel,
                "addToColorshift" : colorgroup.addToColorshift,
                "applyOnTool_Selection" : colorgroup.applyOnTool_Selection,
                "applyOnTool_Deselection" : colorgroup.applyOnTool_Deselection,
                "colorgroupdata" : {
                
                }
            }
            
            colorgroupdatapoints={} #Load Single Datapoints in Group
            for colorgroupindex in range(len(colorgroup.colorgroupdata)):
                colorgroupdatapoints.update({str(colorgroupindex) : colorgroup.colorgroupdata[colorgroupindex].state})
            
            if len(colorgroupdatapoints) != 0:
                group_dict["colorgroupdata"]=colorgroupdatapoints #Add Datapoints to Group

            groups_dict.update({i : group_dict}) # Add Group to Groups
        
        if len(groups_dict) != 0:
            palette_dict.update({"colorgroups":groups_dict}) #Add Groups to Palette

        #merge palette with settings

    if(exportImage):


        img = palette.img
        x=img.size[0]
        y=img.size[1]
        width=x
        height=y
        if(settingsdata.imageExportMode=="tilesize"): #Take the Size depending if the Palette is loaded
            if(palette.p_loaded):
                x=palette.p_tilecountx
                y=palette.p_tilecounty
            else:
                x=palette.pe_tilecountx
                y=palette.pe_tilecounty

        image_dict = {
            "width": x,
            "height": y,
            "name": img.name,
        }

        data = {}
        entrynumber=0
        if(settingsdata.imageExportMode=="tilesize"):
            for yt in range(x):
                for xt in range(y):
                    # index = math_PixelIndex_By_TileNumber(xt, yt, x, y, y, x, 0, 0)
                    uv_x, uv_y = math_UVPosition_By_Tile(xt, yt, x, y)
                    pixindex = int (img_getImagePixelIndex( int(uv_x*width), int(uv_y*height), width))
                    rgbaPre=img.pixels[pixindex:pixindex + 4]
                    print("Len of image"+str(len(img.pixels)))
  
                    rgba=[]
                    # if(settingsdata.convertColorspace):
                    #     rgba.append(linear_to_sRGB(rgbaPre[0]))
                    #     rgba.append(linear_to_sRGB(rgbaPre[1]))
                    #     rgba.append(linear_to_sRGB(rgbaPre[2]))
                    #     rgba.append(linear_to_sRGB(rgbaPre[3]))
                    # else:
                    rgba.append(rgbaPre[0])
                    rgba.append(rgbaPre[1])
                    rgba.append(rgbaPre[2])
                    rgba.append(rgbaPre[3])

                    #Write it to pixeldict
                    #rgba = img.pixels[pixindex:pixindex + 4]
                    pixel_dict = {"R": rgba[0], "G": rgba[1], "B": rgba[2], "A": rgba[3]}
                    data.update({entrynumber:pixel_dict})
                    entrynumber=entrynumber+1


        if(settingsdata.imageExportMode=="standard"):
            for index in range(y*x):
                rgba = img.pixels[index:index + 4]  # Get RGBA values for the current pixel
                pixel_dict = {"R": rgba[0], "G": rgba[1], "B": rgba[2], "A": rgba[3]}  # Create a dictionary for the pixel
                data.update({index:pixel_dict})

        if(len (data)>0):
            image_dict.update({"imagedata" : data})
          
    property_dict={}

    if (exportSettings):
        if len(settings_dict) > 0:
            property_dict.update({"settings" : settings_dict})

    if (exportPalette):
        if len(palette_dict) > 0:
            property_dict.update({"palette" : palette_dict})

    if (exportImage):
        if len(image_dict) > 0:
            property_dict.update({"image" : image_dict})

    with open(filepath, 'w') as f:
        json.dump(property_dict, f, indent=4, separators=(',', ': '))

# Function to convert property group to dictionary
def property_group_to_dict(property_group):
    prop_dict = {}
    for prop_name, prop_value in property_group.bl_rna.properties.items():
        if hasattr(prop_value, "type"):  # Check if property has a type
            if prop_value.type == "POINTER":  # Check if property is a pointer to another property group
                nested_property_group = getattr(property_group, prop_name)
                prop_dict[prop_name] = property_group_to_dict(nested_property_group)
            else:
                prop_dict[prop_name] = getattr(property_group, prop_name)
    return prop_dict

#endregion <SettingPresets_Saving>  

#region <SettingPresets_Loading> <Loading Presets>

class UVC_Operator_Popup_cancel(bpy.types.Operator):
    bl_idname = "wm.uvc_settings_loadpreset_cancel"
    bl_label = "Confirm"

    def execute(self, context):
        print("UVC_Canceled_Popup")
        return {'FINISHED'}

class UVC_Operator_Settings_defaultsettings_confirm(bpy.types.Operator):
    bl_idname = "wm.uvc_settings_loadpreset_confirm"
    bl_label = "Load Default Confirm"
    def execute(self, context):
        settingsdata=bpy.context.scene.uv_palettes_settings_data
        settingsdata.presetSubmenu="collapse" #Close Menu to make user Focus the Loading Button better
    
        filename=settingsdata.settingspresets[settingsdata.settingspresets_index].settingsFilename
        current_directory = os.path.dirname(__file__)
        settings_presets_directory = os.path.join(current_directory, "settings_presets")
        settings_file_directory = os.path.join(settings_presets_directory, filename)

        settingsdata.settingsPath=settings_file_directory
        return {'FINISHED'}
       
def drawsetpresetconfirm(self, context):
    layout = self.layout

    # Draw a confirmation message
    row = layout.row()
    row.label(text=f"Do you want to load the Preset?")
    row = layout.row()
    row.operator(UVC_Operator_Settings_defaultsettings_confirm.bl_idname, text="Load")
    row.operator(UVC_Operator_Popup_cancel.bl_idname, text="Cancel")

    return {'FINISHED'} 
            
class UVC_Operator_Settings_setPreset(bpy.types.Operator):
    """Apple the Selected Preset"""
    bl_idname = "wm.uvc_settings_setpreset"
    bl_label = "set the selected preset"   

    def execute(self, context):

        wm = context.window_manager
        wm.popup_menu(drawsetpresetconfirm, title="Confirm", icon='INFO')

        
        
        return {'FINISHED'} 

class UVC_Operator_Settings_refreshPresets(bpy.types.Operator):
    """Dectects New or yet not Registered Presets in the Filefolder"""

    bl_idname = "wm.uvc_settings_refresh"
    bl_label = "Refresh Presets"

    def execute(self, ctx): #Bacially REmoves the Palette from the Palette, then removes the Palette and then selects the next possible Palette
        refreshPresets(self=self, context=ctx)
        return {'FINISHED'}
    
def refreshPresets(self, context):
    settingsdata=bpy.context.scene.uv_palettes_settings_data

     # Get the directory of the currently executed file
    current_directory = os.path.dirname(__file__)

    # Construct the path to the "settings_presets" folder
    settings_presets_directory = os.path.join(current_directory, "settings_presets")

    # Clear the existing presets
    settingsdata.settingspresets_index=0
    settingsdata.settingspresets.clear()
    

    # Iterate through all files in the directory
    for filename in os.listdir(settings_presets_directory):
        print(""+str(filename))
        #if filename.endswith(".json"):
        # Append the file path to the presets list
        newentry=settingsdata.settingspresets.add()
        newentry.settingsFilenameOnly = str(filename)
        newentry.settingsFilename=os.path.join(settings_presets_directory, str(filename))
        if(len(settingsdata.settingspresets)>0):
            settingsdata.settingspresets_index= len(settingsdata.settingspresets)-1
        else:
            settingsdata.settingspresets_index= 0
    return None
    
#endregion <SettingPresets_Loading>      
    
#region <SetOrigin> <Tools for Origin Management : Disabled on Default>

class UVC_Operator_setOrigin(bpy.types.Operator):

    """ OPERATOR
    Adds a Panel
    """


    bl_idname = "uvc.setorigin"
    bl_label = "sets the Origin of all Selected Objects"
    
    
    
    height: bpy.props.EnumProperty(
        items=[
            ('tl', 'Top Left', 'ltl', '', 1),
            ('tm', 'Top Mid', 'tm', '', 2),    
            ('tr', 'Top Right', 'tr', '', 3),
            ('ml', 'Mid Left', 'ml', '', 4),
            ('mm', 'Mid ', '', 'mm', 5),    
            ('mr', 'Mid Right', 'mr', '', 6),
            ('bl', 'Bottom Left', 'bl', '', 7),
            ('bm', 'Bottom Mid', 'bm', '', 8),    
            ('br', 'Bottom Right', 'br', '', 9),
            ('ct', 'Center', 'cr', '', 10),
        ],
        name="Pivot Placement",
        description="If the Pivot should be placed on a Edge, Corner or Face",
        default='mm'
    )
    

    direction: bpy.props.EnumProperty(
        items=[
            ('x', 'X', 'X', '', 1),
            ('xn', 'X-', 'X-', '', 2),    
            ('y', 'Y', 'Y', '', 3),
            ('yn', 'Y-', 'Y-', '', 4),    
            ('z', 'Z', 'Z', '', 5),
            ('zn', 'Z-', 'Z-', '', 6),    
        ],
        name="Which Direction",
        description="Which Direction to set the Pivot",
        default='zn'
    )
    
    transformspace: bpy.props.EnumProperty(
        items=[
            ('objectspace', 'Object', 'Direction by Objectspace', '', 1),
            ('worldspace', 'World', 'Direction by Worldspace', '', 2),    
            ('auto', 'Auto', 'Will Clip the Objectrotation by the most fitting Worldspace direction', '', 3),
        ],
        name="Which Direction",
        description="Which Direction to set the Pivot",
        default='objectspace'
    )
    
    def execute(self, ctx):
        bpy.ops.ed.undo_push(message = "Attempt Setting Origin of Selection")
        setPivot(self=self, context=ctx)
        
        return {'FINISHED'}
      
def find_most_facing_axis(vector):
    normalized_vector = vector.normalized()
    max_component = max(abs(comp) for comp in normalized_vector)
    
    if normalized_vector.x == max_component:
        return mathutils.Vector((1.0, 0.0, 0.0))
    elif normalized_vector.x == -max_component:
        return mathutils.Vector((-1.0, 0.0, 0.0))
    elif normalized_vector.y == max_component:
        return mathutils.Vector((0.0, 1.0, 0.0))
    elif normalized_vector.y == -max_component:
        return mathutils.Vector((0.0, -1.0, 0.0))
    elif normalized_vector.z == max_component:
        return mathutils.Vector((0.0, 0.0, 1.0))
    else:
        return mathutils.Vector((0.0, 0.0, -1.0))

def setPivot(self, context):

    
    height=self.height
    direction=self.direction
    transformspace=self.transformspace
    
    if(not height):
        height="mm"
    
    if(not direction):
        height="zn"
    
    if(not transformspace):
        height="objectspace"
    
    Xpos=False
    Xneg=False
  
    Ypos=False
    Yneg=False
    
    Zpos=False
    Zneg=False
    
    tl=False
    tm=False 
    tr=False
    
    ml=False  
    mm=False
    mr=False
    
    bl=False  
    bm=False
    br=False

    objectspace=False
    worldspace=False
    auto=False
    
    
    if( transformspace=="objectspace" ):
        objectspace=True
            
    if( transformspace=="worldspace" ):
        worldspace=True
        
    if( transformspace=="auto" ):
        auto=True  
        
                     
    if( direction=="x" ):
        print("Direction : X")
        Xpos=True
    if( direction=="xn" ):
        print("Direction : -X")
        Xneg=True
        
    if( direction=="y" ):
        print("Direction : Y")
        Ypos=True
    if( direction=="yn" ):
        print("Direction : -Y")
        Yneg=True
                    
    if( direction=="z" ):
        print("Direction : Z")
        Zpos=True
    if( direction=="zn" ):
        print("Direction : -Z")
        Zneg=True
        
             
    if( height=="tl" ):
        print("Top Left")
        tl=True
    if( height=="tm" ):
        print("Top Mid")
        tm=True  
    if( height=="tr" ):
        print("Top Right")
        tr=True
    if( height=="ml" ):
        print("Mid Left")
        ml=True             
    if( height=="mm" ):
        print("Mid Mid")
        mm=True
    if( height=="mr" ):
        print("Mid Right")
        mr=True  
    if( height=="bl" ):
        print("Bottom Left")
        bl=True               
    if( height=="bm" ):
        print("Bottom Mid")
        bm=True
    if( height=="br" ):
        print("Bottom Right")
        br=True
    
    if not (worldspace or objectspace or auto):
        objectspace=True
        
    if not (tl or tm or tr or ml or mm or mr or bl or bm or br):
        mm=True
        
    if not(Xpos or Xneg or Ypos or Yneg or Zpos or Zneg):
        Zneg=True
           

    automatrixinit=mathutils.Euler((0, 0, 0), 'XYZ')
    
    selected_Objects=bpy.context.selected_objects
    wasInObjectmode=True
    
    #go to edit mode if not already 
    if bpy.context.mode != 'OBJECT':
        wasInObjectmode=False
        bpy.ops.object.mode_set(mode='OBJECT')
    
    setSelectionforAllObjects(selected_Objects, False)    

    if( height!="ct" ):
        #Correct Alignments before Setting Origins again
        for obj in selected_Objects:
            obj.select_set(True) 
        # Check if the object is a mesh
            if obj and obj.type == 'MESH':
                # Get the mesh data
                mesh = obj.data
                
                # Iterate over vertices and calculate the sum
                vert_sum = mathutils.Vector((0.0, 0.0, 0.0))
                for vert in mesh.vertices:
                    vert_sum += vert.co
                
                # Calculate the average
                avg_position_local  = vert_sum / len(mesh.vertices)
                
                # Set the pivot point to the average position
                bpy.context.scene.cursor.location = obj.matrix_world @ avg_position_local
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            obj.select_set(False) 
        bpy.context.view_layer.update()   
    
    
    for obj in selected_Objects:
        obj.select_set(True) 
    # Check if the object is a mesh

        if obj and obj.type == 'MESH':
            # Get the mesh data
            mesh = obj.data
            First=True                
            axies_x_Min=0
            axies_x_Max=0
            axies_y_Min=0
            axies_y_Max=0
            axies_z_Min=0
            axies_z_Max=0
            
            

                    
            if(auto and height!="ct"):
                pivot = obj.matrix_world @  mathutils.Vector((0.0, 0.0, 0.0)) #get Pivot
                
                Xpos=False
                Xneg=False
                Ypos=False
                Yneg=False
                Zpos=False
                Zneg=False
                
                if( direction=="x" ):
                    directionvector = mathutils.Vector((1.0, 0.0, 0.0) ) #Create Upwarts Vector
                    pivotRotationOnly= (obj.matrix_world.inverted() @(directionvector+ pivot    ))   
                    most_facing_axis = find_most_facing_axis(pivotRotationOnly) #Return Vector with closed axies  
           
                if( direction=="xn" ):
                    directionvector = mathutils.Vector((-1.0, 0.0, 0.0) ) #Create Upwarts Vector
                    pivotRotationOnly= (obj.matrix_world.inverted() @(directionvector+ pivot    ))     
                    most_facing_axis = find_most_facing_axis(pivotRotationOnly) #Return Vector with closed axies  
          
                if( direction=="y" ):
                    directionvector = mathutils.Vector((0.0, 1.0, 0.0) ) #Create Upwarts Vector
                    pivotRotationOnly= (obj.matrix_world.inverted() @(directionvector+ pivot    ))        
                    most_facing_axis = find_most_facing_axis(pivotRotationOnly) #Return Vector with closed axies  
         
                if( direction=="yn" ):
                    directionvector = mathutils.Vector((0.0, -1.0, 0.0) ) #Create Upwarts Vector
                    pivotRotationOnly= (obj.matrix_world.inverted() @(directionvector+ pivot    ))        
                    most_facing_axis = find_most_facing_axis(pivotRotationOnly) #Return Vector with closed axies  
         
                if( direction=="z" ):
                    directionvector = mathutils.Vector((0.0, 0.0, 1.0) ) #Create Upwarts Vector
                    pivotRotationOnly= (obj.matrix_world.inverted() @(directionvector+ pivot    ))        
                    most_facing_axis = find_most_facing_axis(pivotRotationOnly) #Return Vector with closed axies  
      
                if( direction=="zn" ):                    
                    directionvector = mathutils.Vector((0.0, 0.0, -1.0) ) #Create Upwarts Vector
                    pivotRotationOnly= (obj.matrix_world.inverted() @(directionvector+ pivot    ))       
                    most_facing_axis = find_most_facing_axis(pivotRotationOnly) #Return Vector with closed axies  
       
                    
                if(most_facing_axis.x > 0.5):
                    print("remap to x")
                    Xpos=True
                if(most_facing_axis.x < -0.5):
                    print("remap to -x")
                    Xneg=True
                if(most_facing_axis.y > 0.5):
                    print("remap to y")
                    Ypos=True
                if(most_facing_axis.y < -0.5):
                    print("remap to -y")
                    Yneg=True   
                if(most_facing_axis.z > 0.5):
                    print("remap to z")
                    Zpos=True
                if(most_facing_axis.z < -0.5):
                    print("remap to -z")
                    Zneg=True
                
      
                   
                print("target: "+str(most_facing_axis))
                       

            # Iterate over vertices and calculate the sum
            vert_sum = mathutils.Vector((0.0, 0.0, 0.0))
            for vert in mesh.vertices:
                
                if objectspace:
                    co = vert.co
                
                if worldspace:
                    co = obj.matrix_world @ vert.co
                    
                if auto:                    
                    co = vert.co
                

                if(First):
                    First=False
                    axies_x_Min=co.x
                    axies_x_Max=co.x
                    axies_y_Min=co.y
                    axies_y_Max=co.y
                    axies_z_Min=co.z
                    axies_z_Max=co.z
                    vert_sum += co
                else:
                    #override if lower or higher      
                    if co.x < axies_x_Min:
                        axies_x_Min = co.x
                    if co.x > axies_x_Max:
                        axies_x_Max = co.x
                        
                    if co.y < axies_y_Min:
                        axies_y_Min = co.y
                    if co.y > axies_y_Max:
                        axies_y_Max = co.y
                        
                    if co.z < axies_z_Min:
                        axies_z_Min = co.z
                    if co.z > axies_z_Max:
                        axies_z_Max = co.z
                        
                    vert_sum += co
                                
                                            
            # Calculate the average
            if( height=="ct" ):
                position_local  = vert_sum / len(mesh.vertices)
            
                if objectspace:
                    # Set the pivot point to the average position
                    bpy.context.scene.cursor.location = obj.matrix_world @ position_local
                    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                if worldspace:
                    bpy.context.scene.cursor.location = position_local
                    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                if auto:
                    bpy.context.scene.cursor.location = position_local
                    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            
            else:
                position_local = mathutils.Vector((0.0, 0.0, 0.0))
                
                # Erase Axies to set the Direction
                if( Xpos ):
                    position_local.x=axies_x_Max
                if( Xneg ):
                    position_local.x=axies_x_Min
                    
                if( Ypos ):
                    position_local.y=axies_y_Max
                if( Yneg ):
                    position_local.y=axies_y_Min
                                
                if( Zpos ):
                    position_local.z=axies_z_Max
                if( Zneg ):
                    position_local.z=axies_z_Min
                    
                #Write Axies that are used to calculate    
                
                if(Xpos or Xneg or Ypos or Yneg):
                     #Set Height
                    if(tl or tm or tr):
                       position_local.z=axies_z_Max 
                       
                    if(ml or mm or mr):
                        position_local.z=(axies_z_Min+ axies_z_Max)/2
                        
                    if(bl or bm or br):
                        position_local.z=axies_z_Min
                    
                if(Xpos or Xneg ):
                                                          
                    #Set Axies
                    if(tl or ml or tl):
                       position_local.y=axies_y_Max 
                       
                    if(tm or mm or bm):
                        position_local.y=(axies_y_Min+ axies_y_Max)/2
                        
                    if(tr or mr or br):
                        position_local.y=axies_y_Min
                        
                if(Ypos or Yneg):                  
                        
                    #Set Axies
                    if(tl or ml or tl):
                       position_local.x=axies_x_Max 
                       
                    if(tm or mm or bm):
                        position_local.x=(axies_x_Min+ axies_x_Max)/2
                        
                    if(tr or mr or br):
                        position_local.x=axies_x_Min
                        
                        
                    
                if(Zpos or Zneg):
                    
                    if(tl or tm or tr):
                       position_local.y=axies_y_Max 
                       
                    if(ml or mm or mr):
                        position_local.y=(axies_y_Min+ axies_y_Max)/2
                        
                    if(bl or bm or br):
                        position_local.y=axies_y_Min
                        
                    #Set Axies
                    if(tl or ml or bl):
                       position_local.x=axies_x_Max 
                       
                    if(tm or mm or bm):
                        position_local.x=(axies_x_Min+ axies_x_Max)/2
                        
                    if(tr or mr or br):
                        position_local.x=axies_x_Min
                        
                        
                print(str(position_local))       
                 
                if(auto):
                    bpy.context.scene.cursor.location = obj.matrix_world @ position_local
                    #bpy.context.scene.cursor.location = automatrixfixer.inverted() @ position_local #Remove the Correctionangle from Curser to align it with the Actual Object
                    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                if objectspace:
                    # Set the pivot point to the average position
                    bpy.context.scene.cursor.location = obj.matrix_world @ position_local
                    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                if worldspace:
                    bpy.context.scene.cursor.location = position_local
                    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                    
                
        obj.select_set(False)         
        
    setSelectionforAllObjects(selected_Objects, True)        
    
    if wasInObjectmode  :
        bpy.ops.object.mode_set(mode='OBJECT')
    else :
        bpy.ops.object.mode_set(mode='EDIT')
 
    return None

def setSelectionforAllObjects(selected_Objects, state):
    for obj in selected_Objects:
        obj.select_set(state) 
    bpy.context.view_layer.update()              
    

#endregion <SettingPresets_Loading>      

class UVC_Operator_splitnormals(bpy.types.Operator):    
    """ OPERATOR Adds a Panel"""


    bl_idname = "wm.uvc_splitnormals"
    bl_label = "Splits the Normals of all selected Objects"
    #create integer
    angle : bpy.props.IntProperty(name="Angle", default=30, min=-360, max=360)

    def execute(self, ctx):
        bpy.ops.ed.undo_push(message = "Attempt Smoothing")
        splitNormals(self=self, context=ctx)
        return {'FINISHED'}

    

#region <Rotationtool> <Tools for Rotation : Disabled on Default>

class UVC_Operator_rotate90DegL(bpy.types.Operator):    
    """ OPERATOR Adds a Panel"""


    bl_idname = "wm.uvc_rotate90degl"
    bl_label = "Rotates 90 degrees"
    

    
    
    def execute(self, ctx):
        bpy.ops.ed.undo_push(message = "Attempt Rotating")
        rotate90DegL(self=self, context=ctx)
        
        return {'FINISHED'}
  
def rotate90DegL(self, context):
    
    selected_Objects=bpy.context.selected_objects  
    setSelectionforAllObjects(selected_Objects, False)    

    for obj in selected_Objects:
        obj.select_set(True) 
        
        # Check if the object is a mesh
        if obj and obj.type == 'MESH':

            current_rotation = obj.rotation_euler
            new_rotation_z = current_rotation.z + math.radians(90)
            obj.rotation_euler = (current_rotation.x, current_rotation.y, new_rotation_z)

            mesh = obj.data           
            obj.select_set(False) 
    bpy.context.view_layer.update()   

    
    for obj in selected_Objects:
        obj.select_set(True) 
        
def rotate90DegR(self, context):
    
    selected_Objects=bpy.context.selected_objects     
    setSelectionforAllObjects(selected_Objects, False)    

    for obj in selected_Objects:
        obj.select_set(True) 
        
        # Check if the object is a mesh
        if obj and obj.type == 'MESH':

            current_rotation = obj.rotation_euler
            new_rotation_z = current_rotation.z + math.radians(-90)
            obj.rotation_euler = (current_rotation.x, current_rotation.y, new_rotation_z)
                    
            mesh = obj.data           
            obj.select_set(False) 
    bpy.context.view_layer.update()   

    
    for obj in selected_Objects:
        obj.select_set(True) 
                         
class UVC_Operator_rotate90DegR(bpy.types.Operator):    
    """ OPERATOR Adds a Panel"""


    bl_idname = "wm.uvc_rotate90degr"
    bl_label = "Rotates 90 degrees"
    

    
    
    def execute(self, ctx):
        bpy.ops.ed.undo_push(message = "Attempt Rotating")
        rotate90DegR(self=self, context=ctx)
        return {'FINISHED'}

class UVC_Operator_clipRotation(bpy.types.Operator):    
    """ OPERATOR Adds a Panel"""


    bl_idname = "wm.uvc_cliprotation"
    bl_label = "Clips the Rotation to 15 Degrees into the shortest direction"
    

    
    
    def execute(self, ctx):
        bpy.ops.ed.undo_push(message = "Attempt Clipping Rotation")
        clipRotation(self=self, context=ctx)
        
        return {'FINISHED'}
    
def clipRotation(self, context):  
    selected_Objects=bpy.context.selected_objects
       
    for obj in selected_Objects:
        obj.select_set(False)
    bpy.context.view_layer.update()   

    for obj in selected_Objects:
        obj.select_set(True) 
        
    # Check if the object is a mesh
        if obj and obj.type == 'MESH':
              
            
            # Get the current rotation in radians
            current_rotation = obj.rotation_euler

            # Convert rotation to degrees
            current_rotation_degrees = [math.degrees(r) for r in current_rotation]

            # Calculate the next rotation in degrees
            next_rotation_degrees_positive = [round(angle / 15) * 15 for angle in current_rotation_degrees]
            next_rotation_degrees_negative = [(round(angle / 15) - 1) * 15 for angle in current_rotation_degrees]

            # Convert degrees back to radians
            next_rotation_radians_positive = [math.radians(angle) for angle in next_rotation_degrees_positive]
            next_rotation_radians_negative = [math.radians(angle) for angle in next_rotation_degrees_negative]

            # Calculate the difference between positive and negative rotations
            diff_positive = sum(abs(angle - current_angle) for angle, current_angle in zip(next_rotation_degrees_positive, current_rotation_degrees))
            diff_negative = sum(abs(angle - current_angle) for angle, current_angle in zip(next_rotation_degrees_negative, current_rotation_degrees))

            # Set the rotation based on the shortest path
            if diff_positive < diff_negative:
                obj.rotation_euler = next_rotation_radians_positive
            else:
                obj.rotation_euler = next_rotation_radians_negative       
            
            mesh = obj.data           
            obj.select_set(False) 
    bpy.context.view_layer.update()   

    
    for obj in selected_Objects:
        obj.select_set(True) 
    

#endregion <Palette_AddRemoveEdit>    


class UVC_Operator_rerouteSnapping(bpy.types.Operator):    
    """ OPERATOR Adds a Panel"""


    bl_idname = "wm.uvc_splitnormals"
    bl_label = "Splits the Normals of all selected Objects"
    #create integer
    angle : bpy.props.IntProperty(name="Angle", default=30, min=-360, max=360)

    def execute(self, ctx):
        bpy.ops.ed.undo_push(message = "Attempt Smoothing")
        splitNormals(self=self, context=ctx)
        return {'FINISHED'}


#region <Palette_AddRemoveEdit> <Managing Palettes>

class UVC_Operator_Palette_add(bpy.types.Operator):

    """ OPERATOR
    Adds a Panel
    """


    bl_idname = "uvc.add_palette"
    bl_label = "Add UV Palette"
    

    def execute(self, ctx):
        functionname="AddPalette"
        printLog(src=functionname, type=LOGTYPE.FUNCTION, subtype=LOGTYPE.START)


        palette = ctx.scene.uv_palettes.add() #createsnew Palette Item
        current = return_CurrentPalette() #Gets Palette
        
        if current: #and current.texture: #DONT KNOW WHAT DOES DO LOL
            bpy.ops.ed.undo_push(message = "Attempt Adding Palette")
            palette.img = current.img #changes image aswell
            ctx.scene.uv_palettes_index = len(ctx.scene.uv_palettes)-1 #select the newly created Palette
            #updatePalette(self, ctx) #Updates the Palette normally
            printLog(src=functionname, type=LOGTYPE.FUNCTION, subtype=LOGTYPE.FINISH)

            return {'FINISHED'}
        
        printLog(src=functionname, type=LOGTYPE.FUNCTION, subtype=LOGTYPE.FINISH)
        return {'FINISHED'}
    
class UVC_Operator_Palette_remove(bpy.types.Operator):
    bl_idname = "uvc.remove_palette"
    bl_label = "Remove UV Palette"

    def execute(self, ctx): #Bacially REmoves the Palette from the Palette, then removes the Palette and then selects the next possible Palette
        functionname="RemovePalette"
        printLog(src=functionname, type=LOGTYPE.FUNCTION, subtype=LOGTYPE.ONECALL)
        
        if len(ctx.scene.uv_palettes) > 0: 
            current=ctx.scene.uv_palettes[ctx.scene.uv_palettes_index]
           # if current.p_loaded:
                #bpy.ops.image.unpack(current.img)   
            printLog(src=functionname, msg="Deleting Palette with Index:" + str(ctx.scene.uv_palettes_index), type=LOGTYPE.ACTION)
            bpy.ops.ed.undo_push(message = "Attempt Deleting Palette")
            ctx.scene.uv_palettes.remove(ctx.scene.uv_palettes_index)
            ctx.scene.uv_palettes_index = max(min(ctx.scene.uv_palettes_index, len(ctx.scene.uv_palettes)-1), 0)
        else:
            printLog(src=functionname, msg="No Palettes to delete", type=LOGTYPE.INFO)
        
        
        return {'FINISHED'}

class UVC_Operator_Palette_update(bpy.types.Operator):



    """ OPERATOR
    Loads/Unloads Panel
    """

    bl_idname = "uvc.update_palette"
    bl_label = "Update Palette"    
    def execute(self, ctx):

        functionname="UpdatePalette"
        printLog(src="UPDATEPALETTE", type=LOGTYPE.FUNCTION, msg="",  subtype= LOGTYPE.ONECALL)

        current = return_CurrentPalette() #Gets Palette
        if  current.p_loaded:
            current.p_loaded=False 
            current.colors.clear()

            if (current.pe_scalex != current.p_scale[0] or
                current.pe_scaley != current.p_scale[1] or
                current.pe_offsetx != current.p_offset[0] or
                current.pe_offsety != current.p_offset[1] or
                current.pe_tilecountx != current.p_tilecountx or
                current.pe_tilecounty != current.p_tilecounty):
                 
                    #clear colorgroups if the tilecount is greater
                    if current.pe_tilecountx < current.p_tilecountx or current.pe_tilecounty < current.p_tilecounty:
                        printLog(src="UPDATEPALETTE", type=LOGTYPE.FUNCTION, msg="Cleared Colorgroup of Palette",  subtype= LOGTYPE.ACTION)
                        current.colorgroups.clear()
                    current.p_editcolorgroups=False
                    #UI Variables
                    current.pe_scalex= current.p_scale[0]
                    current.pe_scaley= current.p_scale[1]
                    current.pe_offsetx= current.p_offset[0]
                    current.pe_offsety= current.p_offset[1]
                    current.pe_tilecountx= current.p_tilecountx
                    current.pe_tilecounty= current.p_tilecounty
                    printLog(src="UPDATEPALETTE", type=LOGTYPE.FUNCTION, msg="Overwritten Palette Transform Data",  subtype= LOGTYPE.ACTION)

           
        else:
            if current:   
                op_update_Palette(self, ctx) #Updates the Palette

        return {'FINISHED'}
    
#endregion <Palette_AddRemoveEdit>    

class EmptyOperator(bpy.types.Operator):
    bl_idname = "my.empty_operator"
    bl_label = "Empty Operator"

    def execute(self, context):
        return {'FINISHED'}


# ==================================================================================
# ||                             Registration                                      ||
# ==================================================================================
# || Description:                                                                  ||
# ==================================================================================

#region <Utility> <Methods>

def register():
    """ !METHOD!
    Registrates Elements, may be used Different than usual due to the auto_load.py

    Keyword arguments:
    -
    """
    functionname="Register"
    printLog(src=functionname, subtype=LOGTYPE.ONECALL)

    #Panel2 Settings
    setattr(bpy.types.Scene, "uv_palettes_settings_data", bpy.props.PointerProperty(name="UV Palettes settings data", type=UVC_Data_Settings))

    #Panel1 Programm
    setattr(bpy.types.Scene, "uv_palettes", bpy.props.CollectionProperty(name="UV Palettes", type=UVC_Data_Palette)) #searches the Object "uv_palettes" and sets it to the prop 
    setattr(bpy.types.Scene, "uv_palettes_index", bpy.props.IntProperty(name="UV Palettes index"))
    setattr(bpy.types.Scene, "uv_colorgroup_index", bpy.props.IntProperty(name="UV Colorgroup index"))
    setattr(bpy.types.Scene, "uv_palettes_drawing", bpy.props.BoolProperty(name="UV Palettes drawing", update= toggleDrawingDepr))
    setattr(bpy.types.Scene, "uv_popup_buffer", bpy.props.PointerProperty(name="UVC Buffer", type=UVC_PopupBuffer))
    

    
    #setattr(bpy.types.Scene, "UVC_Menu_Colorwheel", Menu(name="UV Palettes drawing", update= toggleDrawing))
    
    #find_collections_with_previews() not working properly!

#UTILS
ErrorMsg = None
def Error(reason):
    """ !METHOD!
    Displays a Error Popup with the text inside the Parameters
    
    Keyword arguments:
    :param str reason:               String with the Text to Display inside the Error Popup
    """

    global ErrorMsg
    ErrorMsg = reason
    bpy.context.window_manager.popup_menu(ErrorPanel, title="Error", icon='ERROR')

def ErrorPanel(self, context):
    """ !METHOD!
    Sets the Text of the Errormessage, used by the Error Function
    
    Keyword arguments:
    self, context                       N/A #
    """
    self.layout.label(text = ErrorMsg)

#endregion <Utility>   

#region <Presets> <Methods>


#region <Logging> <Debug>
#endregion <Logging>    

#region <Lists> <UserInterface>
#endregion <Lists>    

#region <Menus> <UserInterface>
#endregion <Menus>    

#region <Panels> <UserInterface>
#endregion <Panels>    

#region <Logging> <UserInterface>
#endregion <Logging>    



#region <Settings> <DataPropertygroups>
#endregion <Settings>    

#region <Palette> <DataPropertygroups>
#endregion <Palette>    

#region <Colorgroups> <DataPropertygroups>
#endregion <Colorgroups>    



#region <Settings> <Methods>
#endregion <Settings>    

#region <Palette> <Methods>
#endregion <Palette>    

#region <Colorgroups> <Methods>
#endregion <Colorgroups>    



#region <Math> <Methods>
#endregion <Math>    

#region <Logic> <Methods>
#endregion <Logic>    

#region <Checks> <Methods>
#endregion <Checks>    

#region <Colorgroup_Logic> <Methods>
#endregion <Colorgroup_Logic>   

#region <Colorgroup_All> <Methods>
#endregion <Colorgroup_All>    

#region <Colorgroup_Single> <Methods>
#endregion <Colorgroup_Single>    


#region <return> <Methods>
#endregion <return>    

#region <Operators> <Methods>
#endregion <Operators>    



#region <Palette_AddRemoveEdit> <Palette>
#endregion <Palette_AddRemoveEdit>    

#region <Groups_AddRemoveEdit> <Groups>
#endregion <Groups_AddRemoveEdit>    

#region <Palette_AddRemoveEdit> <Methods>
#endregion <Palette_AddRemoveEdit>    



#region <Quickselect> <Operator>
#endregion <Quickselect>    


#region <SelectTools> <Methods>
#endregion <SelectTools>    

#region <SelectTools_ByGroup> <Methods>
#endregion <SelectTools_ByGroup>    

#region <SetMaterial> <Methods>
#endregion <SetMaterial>    

#region <Openable_Menus> <Methods>
#endregion <Openable_Menus>    

#region <Presets> <Methods>
#endregion <Presets>    

#region <SettingPresets_Saving> <Operator>
#endregion <SettingPresets_Saving>    

#region <SettingPresets_Loading> <Operator>
#endregion <SettingPresets_Loading>    

#region <SettingPresets_Import> <Operator>
#endregion <SettingPresets_Import>    


#region <LoadingMethods> <Operator>
#endregion <LoadingMethods>    


#region <Globalvars> <Operator>
#endregion <Globalvars>    

#region <Debugmenu> <Operator>
#endregion <Debugmenu>    


#region <Utility> <Methods>
#endregion <Utility>    

'''
Tags:

<Colorpanel> 
<Panel> 
<Settings> 

<Userinterface>
<Method>
'''

#endregion <Presets>    