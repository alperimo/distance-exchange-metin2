import uiScriptLocale
import gameInfo

ROOT = "d:/ymir work/ui/game/"
FACE_SLOT_FILE = "d:/ymir work/ui/game/windows/box_face.sub"

WIDTH = 272
HEIGHT = 435 + 37 + 20 + 9

window = {
	"name" : "ExchangeDialog",

	"x" : SCREEN_WIDTH - 176 - 269,
	"y" : SCREEN_HEIGHT - 37 - 565 + 36,

	"style" : ("movable", "float",),

	"width" : WIDTH,
	"height" : HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : WIDTH,
			"height" : HEIGHT,

			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 8,
 
					"width" : WIDTH - 15,
					"color" : "gray",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":WIDTH / 2 - 9, "y":3, "text":"Alýþveriþ", "text_horizontal_align":"center" },
					),
				},

				## Start UI

				{ "name" : "Target_Face_Slot", "type" : "image", "x" : 15, "y" : 36, "image" : FACE_SLOT_FILE, },
				{ "name" : "Target_Character_Image", "type" : "image", "x" : 18, "y" : 41, "image" : "icon/face/warrior_m.tga", },
				{ "name" : "Target_Name", "type" : "text", "x" : 68, "y" : 36, "text" : "Fatihbab34 " , "fontsize" : "LARGE", },
				{ "name" : "Target_Level", "type" : "text", "x" : 71, "y" : 49, "text" : "Lv. 99 " , "fontsize" : "LARGE", },
				{ "name" : "Target_Guild", "type" : "text", "x" : 108, "y" : 49, "text" : "TURKIYE " , "fontsize" : "LARGE", },
					
				{ "name" : "My_Face_Slot", "type" : "image", "x" : 15, "y" : 216 + 37, "image" : FACE_SLOT_FILE, },
				{ "name" : "My_Character_Image", "type" : "image", "x" : 18, "y" : 221 + 37, "image" : "icon/face/sura_m.tga", },
				{ "name" : "My_Name", "type" : "text", "x" : 68, "y" : 216 + 37, "text" : "Sen" , "fontsize" : "LARGE", },
				{ "name" : "My_Level", "type" : "text", "x" : 71, "y" : 229 + 37, "text" : "Lv. 78 " , "fontsize" : "LARGE", },
				{ "name" : "My_Guild", "type" : "text", "x" : 108, "y" : 229 + 37, "text" : "TEST " , "fontsize" : "LARGE", },
				
				## Owner Window Gadgets
		
				{
					"name" : "Owner",
					"type" : "window",

					"x" : 9,
					"y" : 235 + 37 + 28 + 10,

					"width" : 259,
					"height" : 128,

					"children" :
					(
						{
							"name" : "Owner_Slot",
							"type" : "grid_table",

							"x" : 0,
							"y" : 0,

							"start_index" : 0,
							"x_count" : 8,
							"y_count" : 4,
							"x_step" : 32,
							"y_step" : 32,
							"x_blank" : 0,
							"y_blank" : 0,


							"image" : "d:/ymir work/ui/public/slot_base.sub",
						},
						
					),
				},

				{
					"name" : "Owner_Accept_Button",
					"type" : "toggle_button",

					"x" : 0,
					"y" : 20+7+4,

					"text" : "Kabul et",

					"horizontal_align":"center",
					"vertical_align":"bottom",

					"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
				},

				{
					"name" : "My_Money",
					"type" : "button",

					"x" : 7,
					"y" : 42+7+4,

					"horizontal_align":"center",
					"vertical_align":"bottom",

					"default_image" : "d:/ymir work/ui/public/parameter_slot_04.sub",
					"over_image" : "d:/ymir work/ui/public/parameter_slot_04.sub",
					"down_image" : "d:/ymir work/ui/public/parameter_slot_04.sub",

					"children" :
					(
						{
							"name":"My_Money_Icon",
							"type":"image",

							"x":-18,
							"y":2,

							"image":"d:/ymir work/ui/game/windows/money_icon.sub",
						},
						{
							"name" : "My_Money_Value",
							"type" : "text",

							"x" : 3,
							"y" : 3,

							"text" : "150.000.000 Yang",

							"horizontal_align" : "left",
							"text_horizontal_align" : "left",
						},
					),
				},

				## Target Window Gadgets
				
				{
					"name" : "Target",
					"type" : "window",

					"x" : 9,
					"y" : 55 + 38,

					"width" : 259,
					"height" : 128,

					"children" :
					(
						{
							"name" : "Target_Slot",
							"type" : "grid_table",

							"x" : 0,
							"y" : 0,

							"start_index" : 0,
							"x_count" : 8,
							"y_count" : 4,
							"x_step" : 32,
							"y_step" : 32,
							"x_blank" : 0,
							"y_blank" : 0,

							"image" : "d:/ymir work/ui/public/slot_base.sub",
						},
						
					),
				},

				{
					"name" : "Target_Money",
					"type" : "image",

					"x" : 7,
					"y" : 192 + 37,
					
					"horizontal_align":"center",
					"image" : "d:/ymir work/ui/public/parameter_slot_04.sub",

					"children" :
					(
						{
							"name":"Target_Money_Icon",
							"type":"image",

							"x":-18,
							"y":2,

							"image":"d:/ymir work/ui/game/windows/money_icon.sub",
						},
						{
							"name" : "Target_Money_Value",
							"type" : "text",

							"x" : 3,
							"y" : 2,

							"text" : "125.000.000 Yang",

							"horizontal_align" : "left",
							"text_horizontal_align" : "left",
						},
					),
				},

				## Accepted Images
				{
					"name" : "My_Accepted",
					"type" : "ani_image",

					"x" : 9,
					"y" : 309,
					
					"images" : (
						gameInfo.CONFIG_YOL+"kabul.tga",
					),
				},

				{
					"name" : "Target_Accepted",
					"type" : "ani_image",

					"x" : 9,
					"y" : 92,
					
					"images" : (
						gameInfo.CONFIG_YOL+"kabul.tga",
					),
				},

				{
					"name" : "Successfully_Islem",
					"type" : "ani_image",

					"x" : 19,
					"y" : 150 - 28,
					
					"images" : (
						gameInfo.CONFIG_YOL+"succes.tga",
					),
				},

				## Accepted Text
				{ "name" : "Loading_Islem", "type" : "text", "x" : 75, "y" : 217, "text" : "%0 " , "fontsize" : "LARGE", },

				## Accepted Close
				{
					"name" : "Accepted_Close",
					"type" : "button",

					"x" : 0,
					"y" : 329,

					"text" : "Pencereyi Kapat",

					"horizontal_align":"center",

					"default_image" : "d:/ymir work/ui/public/xlarge_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/xlarge_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/xlarge_button_03.sub",
				},
			),
		},
	),
}