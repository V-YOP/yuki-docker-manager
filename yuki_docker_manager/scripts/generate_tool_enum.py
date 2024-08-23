import re
from typing import Dict, List, Optional, TypedDict
from krita import *
import os.path as path
DIR = r'd:\DESKTOP\CODES\yuki_docker_manager\yuki_docker_manager'
from yuki_docker_manager.helper.Toolbox import Toolbox

import json

class Field(TypedDict):
    en: str
    zh: str
    c: Optional[str]

with open(path.join(DIR, 'doc', 'krita.po.json'), 'rt') as f:
    fields : List[Field] = json.loads(f.read())

    en_to_po: Dict[str, Field] = {}
    for field in fields:
        en_to_po[field['en']] = field
        
def camel_to_snake(name: str) -> str:
    # 使用正则表达式找到大驼峰命名法中的每个单词的开始位置
    # 并在这些位置插入下划线
    # 然后将结果转换为全大写
    return re.sub(r'(?<!^)(?<!_)(?<!\d)([A-Z])', r'_\1', name).upper()


LISTOFTOOLS = [
    { "toolName": "", "toolIcon": "", "toolString": "" },
    { "toolName": "InteractionTool", "toolIcon": "select", "toolString": "Select Shapes Tool" },
    { "toolName": "SvgTextToo", "toolIcon": "draw-text", "toolString": "Text Tool" },
    { "toolName": "PathTool", "toolIcon": "shape_handling", "toolString": "Edit Shapes Tool" },
    { "toolName": "KarbonCalligraphyTool", "toolIcon": "calligraphy", "toolString": "Calligraphy" },
    { "toolName": "KritaShape/KisToolBrush", "toolIcon": "krita_tool_freehand", "toolString": "Freehand Brush Tool" },
    { "toolName": "KritaShape/KisToolLine", "toolIcon": "krita_tool_line", "toolString": "Line Tool" },
    { "toolName": "KritaShape/KisToolRectangle", "toolIcon": "krita_tool_rectangle", "toolString": "Rectangle Tool" },
    { "toolName": "KritaShape/KisToolEllipse", "toolIcon": "krita_tool_ellipse", "toolString": "Ellipse Tool" },
    { "toolName": "KisToolPolygon", "toolIcon": "krita_tool_polygon", "toolString": "Polygon Tool" },
    { "toolName": "KisToolPolyline", "toolIcon": "polyline", "toolString": "Polyline Tool" },
    { "toolName": "KisToolPath", "toolIcon": "krita_draw_path", "toolString": "Bezier Curve Tool" },
    { "toolName": "KisToolPencil", "toolIcon": "krita_tool_freehandvector", "toolString": "Freehand Path Tool" },
    { "toolName": "KritaShape/KisToolDyna", "toolIcon": "krita_tool_dyna", "toolString": "Dynamic Brush Tool" },
    { "toolName": "KritaShape/KisToolMultiBrush", "toolIcon": "krita_tool_multihand", "toolString": "Multibrush Tool" },
    { "toolName": "KisToolTransform", "toolIcon": "krita_tool_transform", "toolString": "Transform Tool" },
    { "toolName": "KritaTransform/KisToolMove", "toolIcon": "krita_tool_move", "toolString": "Move Tool" },
    { "toolName": "KisToolCrop", "toolIcon": "tool_crop", "toolString": "Crop Tool" },
    { "toolName": "KritaFill/KisToolGradient", "toolIcon": "krita_tool_gradient", "toolString": "Gradient Tool" },
    { "toolName": "KritaSelected/KisToolColorSampler", "toolIcon": "krita_tool_color_sampler", "toolString": "Color Sampler" },
    { "toolName": "KritaShape/KisToolLazyBrush", "toolIcon": "krita_tool_lazybrush", "toolString": "Colorize Mask Tool" },
    { "toolName": "KritaShape/KisToolSmartPatch", "toolIcon": "krita_tool_smart_patch", "toolString": "Smart Patch Tool" },
    { "toolName": "KritaFill/KisToolFill", "toolIcon": "krita_tool_color_fill", "toolString": "Fill Tool" },
    { "toolName": "KisToolEncloseAndFill", "toolIcon": "krita_tool_enclose_and_fill", "toolString": "Enclose and Fill Tool" },
    { "toolName": "KisAssistantTool", "toolIcon": "krita_tool_assistant", "toolString": "Assistant Tool" },
    { "toolName": "KritaShape/KisToolMeasure", "toolIcon": "krita_tool_measure", "toolString": "Measurement Tool" },
    { "toolName": "ToolReferenceImages", "toolIcon": "krita_tool_reference_images", "toolString": "Reference Images Tool" },
    { "toolName": "KisToolSelectRectangular", "toolIcon": "tool_rect_selection", "toolString": "Rectangular Selection Tool" },
    { "toolName": "KisToolSelectElliptical", "toolIcon": "tool_elliptical_selection", "toolString": "Elliptical Selection Tool" },
    { "toolName": "KisToolSelectPolygonal", "toolIcon": "tool_polygonal_selection", "toolString": "Polygonal Selection Tool" },
    { "toolName": "KisToolSelectOutline", "toolIcon": "tool_outline_selection", "toolString": "Freehand Selection Tool" },
    { "toolName": "KisToolSelectContiguous", "toolIcon": "tool_contiguous_selection", "toolString": "Contiguous Selection Tool" },
    { "toolName": "KisToolSelectSimilar", "toolIcon": "tool_similar_selection", "toolString": "Similar Color Selection Tool" },
    { "toolName": "KisToolSelectPath", "toolIcon": "tool_path_selection", "toolString": "Bezier Curve Selection Tool" },
    { "toolName": "KisToolSelectMagnetic", "toolIcon": "tool_magnetic_selection", "toolString": "Magnetic Selection Tool" },
    { "toolName": "ZoomTool", "toolIcon": "tool_zoom", "toolString": "Zoom Tool" },
    { "toolName": "PanTool", "toolIcon": "tool_pan", "toolString": "Pan Tool" }
    ]


print('class ToolEnum(Enum):')

for tool in Toolbox.__get_tool_buttons(Krita.instance().activeWindow()):
    left_brace_idx = tool.toolTip().find('(')
    if left_brace_idx != -1:
        tooltip = tool.toolTip()[:left_brace_idx].strip()
    else:
        tooltip = tool.toolTip()
    
    tool_name = tool.objectName()
    en_desc = tooltip
    zh_desc = en_to_po[tooltip]['zh']
    icon_name = next(( i['toolIcon'] for i in LISTOFTOOLS if i['toolName'] == tool_name ), None)
    enum_name = camel_to_snake(tool_name.replace('/', ''))
    print(f"    {enum_name} = ('{tool_name}', '{icon_name}', '{en_desc}', '{zh_desc}')")
