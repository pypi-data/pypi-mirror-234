# -*- coding: utf-8 -*-
import time  #내장모듈

import basic_data  # xython 모듈

import pyperclip3
import pyautogui

class pyclick:
	"""
	여러가지 사무용에 사용할 만한 메소드들을 만들어 놓은것이며,
	좀더 특이한 것은 youtil2로 만들어서 사용할 예정입니다 
	"""

	def __init__(self):
		self.base_data = basic_data.basic_data()
		self.var = self.base_data.vars
		self.var_common={}

	def check_action_key(self, input_value):
		input_value = str(input_value).lower()
		if input_value in self.var["action_key_list"]:
			result = input_value
		else:
			result = ""
		return result

	def click_mouse_general(self, click_type="click", click_times=1, interval_time=0.25):
		# 마우스 클릭에 대한 일반적인것
		# 입력형태 : pyautogui.click(button=’right', clicks=3, interval =0.25)
		pyautogui.click(button=click_type, clicks=click_times, interval=interval_time)

	def click_mouse_left(self, click_times = 1):
		pyautogui.click(button="left", clicks= click_times)

	def click_mouse_left_down(self):
		pyautogui.mouseDown(button='left')

	def click_mouse_left_up(self):
		pyautogui.mouseUp(button='left')

	def click_mouse_right(self, click_times = 1):
		pyautogui.click(button="right", clicks=click_times)

	def click_mouse_right_down(self):
		pyautogui.mouseDown(button='right')

	def click_mouse_right_up(self):
		pyautogui.mouseUp(button='right')

	def copy(self):
		pyautogui.hotkey('ctrl', "c")

	def data_keyboard(self):
		result =self.var["keyboard_action_list_all"]
		return result

	def dclick_mouse_left(self, interval_time=0.25):
		pyautogui.click(button="left", clicks=2, interval=interval_time)

	def dclick_mouse_right(self, interval_time=0.25):
		pyautogui.click(button="right", clicks=2, interval=interval_time)

	def drag_mouse_pxy1_to_pxy2(self, pxy1, pxy2, drag_speed=0.5):
		pyautogui.moveTo(pxy1[0], pxy1[1])
		pyautogui.dragTo(pxy2[0], pxy2[1], drag_speed)

	def drag_mouse_to_pwh(self, phw, drag_speed=0.5):
		# 현재 마우스위치에서 상대적인 위치인 pxy로 이동
		# 상대적인 위치의 의미로 width 와 height 의 개념으로 pwh 를 사용 duration 은 드레그가 너무 빠를때 이동하는 시간을 설정하는 것이다
		pyautogui.drag(phw[0], phw[1], drag_speed)

	def drag_mouse_to_pxy(self, pxy, drag_speed=0.5):
		# 현재 마우스위치에서 절대위치인 머이로 이동	duration 은 드레그가 너무 빠를때 이동하는 시간을 설정하는 것이다
		pyautogui.dragTo(pxy[0], pxy[1], drag_speed)

	def get_pxy_for_selected_image(self, input_file_name):
		#화면에서 저장된 이미지랑 같은 위치를 찾아서 돌려주는 것
		button5location = pyautogui.locateOnScreen(input_file_name)
		center = pyautogui.center(button5location)
		return center

	def key_down_with_one_key(self, one_key):
		pyautogui.keyDown(one_key)

	def key_up_with_one_key(self, one_key):
		pyautogui.keyUp(one_key)

	def move_cursor(self, direction, press_times = 1):
		#마우스커서를 기준으로 이동하는것
		for no in range(press_times):
			pyautogui.press(direction)

	def move_mouse_as_pwh(self, pwh):
		"""
		현재의 위치에서 이동시키는것
		마우스의 위치를 이동시킨다
		"""
		pyautogui.move(pwh[0], pwh[1])

	def move_mouse_as_pxy(self, pxy):
		"""
		마우스의 위치를 이동시킨다
		"""
		pyautogui.moveTo(pxy[0], pxy[1])


	def paste(self):
		pyautogui.hotkey('ctrl', "v")

	def paste_for_clibboard_data(self):
		# 클립보드에 저장된 텍스트를 붙여넣습니다.
		pyperclip3.paste()

	def press_one_key(self, input_key="enter"):
		#기본적인 키를 누르는 것을 설정하는 것이며
		#기본값은 enter이다
		#press의 의미는 down + up이다
		pyautogui.press(input_key)

	def read_monitor_size(self):
		"""모니터의 해상도를 읽어오는 것"""
		result = pyautogui.size()
		return result

	def read_mouse_position(self):
		position = pyautogui.position()
		return [position.x, position.y]

	def save(self):
		pyautogui.hotkey('ctrl', "s")

	def screen_capture_with_save_file(self, file_name="D:Wtemp_101.jpg"):
		# 스크린 캡쳐를 해서, 화면을 저장하는 것
		pyautogui.screenshot(file_name)
		return file_name

	def move_screen_by_scroll(self, input_no):
		""" 현재 위치에서 상하로 스크롤하는 기능 #위로 올리는것은 +숫자，내리는것은 -숫자로 사용 """
		pyautogui.scroll(input_no)

	def screen_capture_with_size(self):
		im3 = pyautogui.screenshot('my_region.png', region=(0, 0, 300, 300))

	def select_from_curent_cursor(self, direction, press_times):
		#현재위치에서 왼쪽이나 오른쪽으로 몇개를 선택하는 것
		pyautogui.keyDown("shift")
		for one in range(press_times):
			self.key_down_with_one_key(direction)
		pyautogui.keyUp("shift")

	def message_box_for_input_by_password_style(self, input_text, input_title="", input_default_text =""):
		a = pyautogui.password(text=input_text, title=input_title, default=input_default_text, mask='*')
		print(a)


	def message_box_for_show(self, input_text, input_title="", input_default_text =""):
		a = pyautogui.prompt(text=input_text, title=input_title, default=input_default_text)
		print(a)

	def message_box_for_write(self, input_text, input_title=""):
		pyautogui.alert(text=input_text, title=input_title, button='OK')

	def message_box_for_write_with_input_list(self, button_list):
		# 메세지박스의 버튼을 만드는 것
		press_button_name = pyautogui.confirm('Enter option', buttons=['A', 'B', 'C'])
		return press_button_name
	def type_1000times_delete_key(self):
		# 현재위치에서 자료를 지우는것
		# 최대 한줄의 자료를 다 지워서 x 의 위치가 변거나 textbox 안의 자료가 다지워져 위치이동이 없으면 종료
		for no in range(0, 1000):
			position = pyautogui.position()
			pxy_old = [position.x, position.y]
			pyautogui.press('delete')
			position = pyautogui.position()
			pxy_new = [position.x, position.y]
			if pxy_old == pxy_new or pxy_old[1] != pxy_new[1]:
				break

	def type_N_times_backspace(self, number = 10):
		# 현재위치에서 자료를 지우는것
		# 죄대 한줄의 자료를 다 지워서 x 의 위지가 변거나 textbox 안의 자료가 다지워져 위지이동이 없으면 종료
		for no in range(0, number):
			pyautogui.press('backspace')
			time.sleep(0.2)

	def type_action_key(self, action, times=1, input_interval=0.1):
		pyautogui.press(action, presses=times, interval=input_interval)

	def type_backspace_until_finish(self):
		# 자료를 다 삭제할때까지 지우는것
		#최대 1000번까지 한다
		for no in range(0, 1000):
			position = pyautogui.position()
			pxy_old = [position.x, position.y]
			pyautogui.press('backspace')
			position = pyautogui.position()
			pxy_new = [position.x, position.y]
			if pxy_old == pxy_new or pxy_old[1] != pxy_new[1]:
				break
			time.sleep(0.2)

	def type_ctrl_n_one_letter(self, input_text):
		#ctrl + 키를 위한것
		pyautogui.hotkey('ctrl', input_text)

	def type_hotkey_n_key(self, input_hotkey, input_key):
		# pyautogui.hotkey(’ctrl’, *c') ==> ctrl-c to copy
		pyautogui.hotkey(input_hotkey, input_key)

	def type_text_for_hangul(self, input_text):
		# 영문은 어떻게 하면 입력이 잘되는데, 한글이나 유니코드는 잘되지 않아 찾아보니 아래의 형태로 사용하시면 가능합니다
		# pyautogui 가 unicode 는 입력이 안됩니다
		pyperclip3.copy(input_text)
		pyautogui.hotkey('ctrl', "v")

	def type_text_one_by_one(self, input_text):
		# 영문은 어떻게 하면 입력이 잘되는데, 한글이나 유니코드는 잘되지 않아 찾아보니 아래의 형태로 사용하시면 가능합니다
		# 어떤경우는 여러개는 않되어서 한개씩 들어가는 형태로 한다
		for one_letter in input_text:
			pyperclip3.copy(one_letter)
			pyautogui.hotkey("ctrl", "v")

	def type_text_with_interval(self, input_text, input_interval=0.1):
		# 그저 글자를 타이핑 치는 것이다
		# pyautogui.pressfenter', presses=3z interval=3) # enter 키를 3 초에 한번씩 세번 입력합니다.
		pyautogui.typewrite(input_text, interval=input_interval)

	def type_ctrl_plus_letter(self, input_text):
		pyautogui.hotkey('ctrl', input_text)

	def type_normal_key(self, input_text="enter"):
		pyautogui.press(input_text)

	def mouse_drag(self, pxy):
		pyautogui.dragTo(pxy[0], pxy[1])

	def get_text_from_clipboard(self):
		"""
		클립보드에 입력된 내용을 복사를 하는 것이다
		"""
		result = pyperclip3.paste()
		return result

	def show_message(self):
		pyautogui.alert(text='내용입니다', title='제목입니다', button='OK')

	def paste_clibboard_data(self):
		# 클립보드에 저장된 텍스트를 붙여넣습니다.
		pyperclip.paste()

	def type_backspace_until_empty(self):
		# 자료를 다 삭제할때까지 지우는것
		#최대 1000번까지 한다
		for no in range(0, 1000):
			position = pyautogui.position()
			pxy_old = [position.x, position.y]
			pyautogui.press('backspace')
			position = pyautogui.position()
			pxy_new = [position.x, position.y]
			if pxy_old == pxy_new or pxy_old[1] != pxy_new[1]:
				break
			time.sleep(0.2)

	def type_action_key_with_keyboard(self, action, times=1, input_interval=0.1):
		pyautogui.press(action, presses=times, interval=input_interval)

	def type_each_letter_by_interval_with_keyboard(self, input_text, input_interval=0.1):
		# 그저 글자를 타이핑 치는 것이다
		# pyautogui.pressfenter', presses=3z interval=3) # enter 키를 3 초에 한번씩 세번 입력합니다.
		pyautogui.typewrite(input_text, interval=input_interval)

	def type_hotkey(self, input_keys):
		# pyautogui.hotkey(’ctrl’, *c')
		# ctrl-c to copy
		pyautogui.hotkey(input_keys[0], input_keys[1])

	def type_text(self, input_text="enter"):
		#기본적인 키를 누르는 것을 설정하는 것이며
		#기본값은 enter이다
		pyautogui.press(input_text)

	def type_text_one_by_one_with_keyboard(self, input_text):
		# 영문은 어떻게 하면 입력이 잘되는데, 한글이나 유니코드는 잘되지 않아 찾아보니 아래의 형태로 사용하시면 가능합니다
		# 어떤경우는 여러개는 않되어서 한개씩 들어가는 형태로 한다
		for onejetter in input_text:
			pyperclip.copy(onejetter)
			pyautogui.hotkey("ctrl", "v")

	def type_text_with_keyboard(self, input_text):
		# 영문은 어떻게 하면 입력이 잘되는데, 한글이나 유니코드는 잘되지 않아 찾아보니 아래의 형태로 사용하시면 가능합니다
		# pyautogui 가 unicode 는 입력이 안됩니다
		pyperclip.copy(input_text)
		pyautogui.hotkey('ctrl', "v")


	def zzz_sample_with_win32com(self):
		result = """
		win32api.SetCursorPos((x, y))
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

		(left, top, right, bottom) 영역으로 마우스 커서 제한하기
		win32api.ClipCursor((200, 200, 700, 700))

		마우스 커서 제한 해제하기
		win32api.ClipCursor((0, 0, 0, 0))
		win32api.ClipCursor()
		"""