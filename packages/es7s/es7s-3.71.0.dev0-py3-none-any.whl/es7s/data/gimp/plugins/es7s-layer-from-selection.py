#!/usr/bin/env python

# GIMP plugin for "New Layer from Selection" routine
# (c) delameter 2023
#
#   History:
#
#   v0.0: 2023-06-06: Prototype
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
import os
import sys
from gimpfu import *

def layerFromSelection(image):
    if pdb.gimp_selection_is_empty(image) == 1:
        pdb.gimp_message("Selection on active layer is empty.")
        return
    
    drawable = pdb.gimp_image_get_active_layer(image)
    pdb.gimp_edit_cut(drawable)

    flayer = pdb.gimp_edit_paste(drawable, True)
    pdb.gimp_floating_sel_to_layer(flayer)

    pdb.gimp_selection_none(image)
    pdb.gimp_image_set_active_layer(image, drawable)


register(
    'es7s-layer-new-from-selection',
    'Layer from Selection: %s' % os.path.abspath(sys.argv[0]),
    'Create new layer from Selection',
    'delameter',
    'delameter',
    '2023',
    'Layer from Selection',
    "*",
    [
        #(PF_INT32,   "runmode",        "Run mode", None),
        (PF_IMAGE,    "image",       "Input image", None),
        #(PF_DRAWABLE, "drawable", "Input drawable", None),
        #(PF_LAYER, "drawable", "DRAWING:", None),
    ],
    [],
    layerFromSelection,
    menu='<Image>/Layer',
)

main()       
