import flet as ft 
import sqlite3


now_mode = 0
now_wort = 0

bright = 0
speed = 0
color = 0

# db = sqlite3.connect('base_for_modes.db')
# cur = db.cursor()

# cur.execute("""CREATE TABLE IF NOT EXISTS
# 			modes(
# 				id INTEGER PRIMARY KEY,
# 				bright INTEGER,
# 				speed INTEGER,
# 				color INTEGER
# 			)
# 		""")


# for i in range (1, 9):
# 	cur.execute("INSERT INTO modes VALUES(?, ?, ?, ?)", (i, 0, 0, 0))
# 	db.commit()

# db.close()


def main(page: ft.Page):

	global bright, speed, color

	page.title = "Лампа"
	page.theme_mode = 'dark'
	page.vertical_alignment = ft.MainAxisAlignment.CENTER
	page.window_width = 360 
	page.window_height = 640
	page.window_resizable = False


	def data_base_add(mode, property, value):
		global cur, db, now_mode, bright, speed, color	
		
		db = sqlite3.connect('base_for_modes.db')
		cur = db.cursor()	

		if property == 1:
			bright = value
			cur.execute("UPDATE modes SET bright = ? WHERE id = ?", (bright, mode))
		if property == 2:
			speed = value
			cur.execute("UPDATE modes SET speed = ? WHERE id = ?", (speed, mode))
		if property == 3:
			color = value
			cur.execute("UPDATE modes SET color = ? WHERE id = ?", (color, mode))

		
		db.commit()
		db.close()


	


	def bright_slider_output(e):#brightness_6
		print("1 == ", e.control.value, "mode - ", now_mode)
		data_base_add(now_mode, 1, e.control.value)

	def speed_slider_output(e):#speed
		print("2 == ", e.control.value, "mode - ", now_mode)
		data_base_add(now_mode, 2, e.control.value)
		
	def color_slider_output(e):#brush_rounded
		print("3 == ", e.control.value, "mode - ", now_mode)
		data_base_add(now_mode, 3, e.control.value)

	def toggle_icon_button(e):
		e.control.selected = not e.control.selected
		e.control.update()




	buttons = []
	buttons_text = {
		0:["None"],
		1:["Fire", ft.icons.LOCAL_FIRE_DEPARTMENT_ROUNDED, "red"],
		2:["Lava", ft.icons.VOLCANO_ROUNDED, "orange"],
		3:["Snow", ft.icons.CLOUDY_SNOWING, "white"],
		4:["Firework", ft.icons.CELEBRATION_ROUNDED, "pink"],
		5:["Ocean", ft.icons.WAVES, "#0096ff"],
		6:["Rainbow", ft.icons.LOOKS_ROUNDED, "#f0c222"],
		7:["Color", ft.icons.FORMAT_COLOR_FILL_ROUNDED, "#1ab737"],
		8:["Gradient", ft.icons.INVERT_COLORS_ON, "#5c15d2"]
	}

	sliders = []
	slider_properties = {
		1:[bright, "255", bright_slider_output],
		2:[speed, "100", speed_slider_output],
		3:[color, "360", color_slider_output]
	}
	

	def output(e: ft.ControlEvent):	
		global now_mode, bright, speed, color	
		now_mode = e.control.data 
		print(now_mode, "Кнопка нажата!") 

		db = sqlite3.connect('base_for_modes.db')
		cur = db.cursor()

		cur.execute('SELECT *, id FROM modes WHERE id = ?', (now_mode,))
		data_mode = cur.fetchone()

		i = 1
		for res in data_mode:
			if i == 2:
				bright = res
				slider_properties[1][0] = bright
				print(bright)
			if i == 3:
				speed = res
				slider_properties[2][0] = speed
				print(speed)
			if i == 4:
				color = res
				slider_properties[3][0] = color
				print(color)
			i += 1

		for i in range(0, 3):
			sliders[i].content = ft.Slider(
				on_change=slider_properties.get(i+1)[2],
				value = slider_properties.get(i+1)[0],
				min = 0,
				max = slider_properties.get(i+1)[1],
				divisions = 100,
				width = 265
			)
			page.update()
			print(slider_properties.get(i+1)[0], "ssssssssssssssss")

		label_mode.value = f"Mode: {buttons_text.get(now_mode)[0]}"
		page.update()

		cur.execute('SELECT * FROM modes')
		print("\n", cur.fetchall(), "\n")
		db.close()
	


	for i in range (1, 9):
		btn = ft.ElevatedButton(
			data = i,
			on_click=output,
			width = 150,
			height = 50,
			content = ft.Container(
				content=ft.Row([
					ft.Text(value=buttons_text.get(i)[0], size=20, color="white"),
					ft.Icon(name=buttons_text.get(i)[1], color=buttons_text.get(i)[2])
				], alignment=ft.MainAxisAlignment.CENTER)
			)
		)
		buttons.append(btn)


	for i in range (1, 4):
		sld = ft.Container(
		theme = ft.Theme(slider_theme=ft.SliderTheme(active_track_color = "red", )),
		content =ft.Slider(
			on_change=slider_properties.get(i)[2],
			value = slider_properties.get(i)[0],
			min = 0,
			max = slider_properties.get(i)[1],
			divisions = 100,
			width = 265
			)
		)
		sliders.append(sld)


	label_mode = ft.Text(value=f"Mode: {buttons_text.get(now_mode)[0]}", size=20, color="#333538")



	page.add(
		ft.Row([
			label_mode
		], alignment=ft.MainAxisAlignment.CENTER),

		ft.Row([
			ft.IconButton(
				icon_size = 40,
            	icon=ft.icons.POWER_SETTINGS_NEW_ROUNDED,
            	selected_icon=ft.icons.SETTINGS_POWER,
            	on_click=toggle_icon_button,
            	selected=False,
            	style=ft.ButtonStyle(color={"selected": ft.colors.GREEN, "": ft.colors.RED}),
        )
		 ], alignment=ft.MainAxisAlignment.CENTER),
		ft.Container(height = 10),

		ft.Row([
			buttons[0], buttons[1]
		], alignment=ft.MainAxisAlignment.CENTER),

		ft.Row([
			buttons[2], buttons[3]
		], alignment=ft.MainAxisAlignment.CENTER),

		ft.Row([
			buttons[4], buttons[5]
		], alignment=ft.MainAxisAlignment.CENTER),

		ft.Row([
			buttons[6], buttons[7]
		], alignment=ft.MainAxisAlignment.CENTER),

		ft.Container(height = 15),

		ft.Row([
			sliders[0], ft.Icon(name=ft.icons.SUNNY, color="white")
		], alignment=ft.MainAxisAlignment.CENTER),
		ft.Row([
			sliders[1], ft.Icon(name=ft.icons.SPEED, color="white")
		], alignment=ft.MainAxisAlignment.CENTER),	
		ft.Row([
			sliders[2], ft.Icon(name=ft.icons.COLOR_LENS_ROUNDED, color="white")
		], alignment=ft.MainAxisAlignment.CENTER),		

	)


ft.app(target=main, view = None, port = 8000)	