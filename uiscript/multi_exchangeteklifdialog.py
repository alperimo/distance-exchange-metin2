import uiScriptLocale

window = {
	"name" : "InputDialog",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width" : 200,
	"height" : 110,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : 200,
			"height" : 110,

			"title" : "",

			"children" :
			(

				## Input Slot
				{
					"name" : "InputSlot",
					"type" : "slotbar",

					"x" : 0,
					"y" : 34,
					"width" : 90+25,
					"height" : 18,
					"horizontal_align" : "center",

					"children" :
					(
						{
							"name" : "InputValue",
							"type" : "editline",

							"x" : 3,
							"y" : 3,

							"width" : 90+25,
							"height" : 18,

							"input_limit" : 18,
						},
					),
				},

				## Input Slot
				{
					"name" : "RakipValue",
					"type" : "text",

					"x" : 0,
					"y" : 59,
					"text" : "Oyuncu adýný girin",
					"text_horizontal_align" : "center",
					"horizontal_align" : "center",
				},

				## Button
				{
					"name" : "AcceptButton",
					"type" : "button",

					"x" : - 61 - 5 + 30,
					"y" : 78,
					"horizontal_align" : "center",

					"text" : "Gönder",
					"tooltip_text" : "Ona ticaret isteði yolla.",

					"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
				},
				{
					"name" : "CancelButton",
					"type" : "button",

					"x" : 5 + 30,
					"y" : 78,
					"horizontal_align" : "center",

					"text" : uiScriptLocale.CANCEL,

					"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
				},
			),
		},
	),
}