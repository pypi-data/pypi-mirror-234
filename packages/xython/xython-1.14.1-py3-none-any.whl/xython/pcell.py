# -*- coding: utf-8 -*-
import re
import math
import string
import random
import os
from itertools import combinations_with_replacement

import scolor  # xython 모듈
import basic_data  # xython 모듈
import youtil  # xython 모듈
import win32gui  # pywin32의 모듈
import win32api  # pywin32의 모듈
import win32com.client  # pywin32의 모듈
from pywintypes import TimeType


class pcell:
	"""
	엑셀을 컨트롤 할수있는 모듈
	"""

	def __init__(self, filename=""):
		# 공통으로 사용할 변수들을 설정하는 것
		self.color = scolor.scolor()
		self.util = youtil.youtil()
		self.base_data = basic_data.basic_data()
		self.var_common = self.base_data.vars  # package안에서 공통적으로 사용되는 변수들
		self.var_pcell = {}  # 이 클래스안에서만 사용되는 local 변수들
		# 만약 화일의 경로가 있으면 그 화일을 열도록 한다
		self.xlapp = win32com.client.dynamic.Dispatch('Excel.Application')
		self.xlapp.Visible = 1

		self.var_pcell["use_same_sheet"] = False

		if filename != None:
			self.filename = str(filename).lower()
			if filename != "" and not "." in self.filename[-5:]:
				self.filename = self.filename + ".xlsx"

		if self.filename == 'activeworkbook' or not self.filename:
			# activeworkbook으로 된경우는 현재 활성화된 workbook을 그대로 사용한다
			self.xlbook = self.xlapp.ActiveWorkbook
			if self.xlbook == None:
				# 만약 activework북을 부르면서도 화일이 존재하지 않으면 새로운 workbook을 만드는 것
				try:
					self.xlapp.WindowState = -4137
					self.xlbook = self.xlapp.WorkBooks.Add()
				except:
					win32gui.MessageBox(0, "There is no Activeworkbook", "www.xython.co.kr", 0)
		elif filename.lower() == 'new':
			# 빈것으로 된경우는 새로운 workbook을 하나 열도록 한다
			self.xlapp.WindowState = -4137
			self.xlbook = self.xlapp.WorkBooks.Add()
		elif not (self.filename == 'activeworkbook') and self.filename:
			# 만약 화일 이름이 따로 주어 지면 그 화일을 연다
			if self.xlapp.WorkBooks.Count:
				for index in range(self.xlapp.WorkBooks.Count):
					opened_file_name = self.xlapp.WorkBooks[index].Path + "\\" + self.xlapp.WorkBooks[index].Name

					if "\\" in self.filename or "/" in self.filename:
						if opened_file_name == self.filename:
							self.xlbook = self.xlapp.WorkBooks[index]
					else:
						if self.xlapp.WorkBooks[index].Name == self.filename:
							self.xlbook = self.xlapp.WorkBooks[index]
			else:
				try:
					# self.xlapp.WindowState = -4137
					self.xlbook = self.xlapp.Workbooks.Open(self.filename)
				except:
					win32gui.MessageBox(0, "Please check file path", "www.xython.co.kr", 0)

	def activate_cell(self, sheet_name="", xyxy=[1, 1, 7, 7], xy=[3, 3]):
		"""
		셀 객체를 돌려준다

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param xy: [가로번호, 세로번호]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		self.select_range("", xyxy)
		sheet_object.Range("b2").Activate

	def add_button_with_macro(self, sheet_name="", xyxy="", macro_code="", title=""):
		"""
		매크로랑 연결된 버튼을 만드는것
		버튼을 만들어서 그 버튼에 매크로를 연결하는 것이다
		매크로와 같은것을 특정한 버튼에 연결하여 만드는것을 보여주기위한 것이다
		Add(왼쪽의 Pixel, 위쪽 Pixce, 넓이, 높이)
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호 range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param macro_code: macro code, 매크로 코드
		:param title: caption for button, 버튼위에 나타나는 글씨
		:return: X / 없음
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		new_btn = sheet_object.Buttons()
		sheet_object.Cells(x1, y1).Select()
		left_px, top_px, width_px, height_px = self.read_coord_in_cell("", [x1, y1])
		new_btn.Add(left_px, top_px, width_px, height_px)
		new_btn.OnAction = macro_code
		new_btn.Text = title

	def add_picture_in_sheet(self, sheet_name, file_path, xywh, link=0, image_in_file=1):
		"""
		insert picture in sheet / 시트에 사진을 넣는것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param file_path:
		:param xywh: [x, y, width, height]
		:param link:
		:param image_in_file:
		:return:
		"""
		self.insert_picture_in_sheet(sheet_name, file_path, xywh, link, image_in_file)

	def add_picture_in_sheet_by_pixel(self, sheet_name, file_path, pxpywh, link=0, image_in_file=1):
		"""
		그림을 픽셀크기로 시트에 넣는 것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param file_path: file_path
		:param pxpywh:
		:param link:
		:param image_in_file:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Shapes.AddPicture(file_path, link, image_in_file, pxpywh[0], pxpywh[1], pxpywh[2], pxpywh[3])

	def add_shape_by_xywh(self, sheet_name, shape_no=35, xywh=""):
		"""
		그림을 픽셀크기로 시트에 넣는 것
		shape_no : 엑셀에서 정의한 도형의 번호
		xywh : 왼쪽윗부분의 위치에서 너비와 높이
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param shape_no: shape_no
		:param xywh: [x, y, width, height]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Shapes.Addshape(shape_no, xywh[0], xywh[1], xywh[2], xywh[3])

	def add_sheet_new(self):
		"""
		새로운 시트를 추가
		메뉴에서 제외
		** 엣날자료를 위해서 보관하는 목족, 다른 함수를 사용하세요

		:return:
		"""
		self.new_sheet()

	def add_sheet_new_with_name(self, input_name=""):
		"""
		새로운 시트를 이름을 넣어서 추가
		메뉴에서 제외
		** 엣날자료를 위해서 보관하는 목족, 다른 함수를 사용하세요

		:param input_name:
		:return:
		"""
		self.new_sheet(input_name)

	def add_text_by_step(self, sheet_name="", xyxy="", input_text="입력필요", step=1):
		"""
		몇번째마다 글을 추가하는것
		메뉴에서 제외
		** 엣날자료를 위해서 보관하는 목족, 다른 함수를 사용하세요

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호 range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_text: 입력되는 text형식의 자료
		:param step: n번째마다 반복되는것
		:return:
		"""
		self.add_text_in_range_by_step(sheet_name, xyxy, input_text, step)

	def add_text_in_range_at_left(self, sheet_name="", xyxy="", input_text="입력필요"):
		"""
		선택한 영역의 왼쪽에 입력한 글자를 추가

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호 range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_text: 입력되는 text형식의 자료
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				cell_value = sheet_object.Cells(x, y).Value
				if cell_value == None:
					cell_value = ""
				sheet_object.Cells(x, y).Value = str(input_text) + cell_value

	def add_text_in_range_at_right(self, sheet_name="", xyxy="", input_text="입력필요"):
		"""
		선택한 영역의 오른쪽에 입력한 글자를 추가

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호 range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_text: 입력되는 text형식의 자료
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				cell_value = sheet_object.Cells(x, y).Value
				if cell_value == None:
					cell_value = ""
				sheet_object.Cells(x, y).Value = cell_value + str(input_text)

	def add_text_in_range_by_step(self, sheet_name="", xyxy="", input_text="", step=""):
		"""
		선택한 영역의 시작점부터 n번째 셀마다 값을 넣기

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호 range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_text: 입력되는 text형식의 자료
		:param step: n번째마다 반복되는것
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		basic_list = []
		for one_data in input_text.split(","):
			basic_list.append(one_data.strip())
		num = 1
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				if divmod(num, int(step))[1] == 0:
					sheet_object.Cells(x, y).Value = str(input_text)
				num = num + 1

	def add_text_in_range_by_xystep(self, sheet_name="", xyxy="", input_text="", xystep=[1, 1]):
		"""
		선택한 영역의 시작점부터 x,y 번째 셀마다 값을 넣기

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호 range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_text: 입력되는 text형식의 자료
		:param xystep:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			if divmod(x, xystep[0])[1] == 0:
				for y in range(y1, y2 + 1):
					if divmod(x, xystep[1])[1] == 0:
						cell_value = sheet_object.Cells(x, y).Value
						if cell_value == None:
							cell_value = ""
						sheet_object.Cells(x, y).Value = cell_value + str(input_text)

	def change_active_workbook(self, input_file_name):
		"""
		열려진 워드 화일중 이름으로 선택하는것
		메뉴에서 제외

		:param input_file_name: file_name
		:return:
		"""
		self.xlapp.Visible = True
		win32gui.SetForegroundWindow(self.xlapp.hwnd)
		self.xlapp.WorkBooks(input_file_name).Activate()
		self.xlapp.WindowState = win32com.client.constants.xlMaximized

	def change_char_to_num(self, input_text="입력필요"):
		"""
		주소를 바꿔주는 것이다
		문자가 오던 숫자가 오던 숫자로 변경하는 것이다
		 b를 2로 바꾸어 주는것
		메뉴에서 제외

		:param input_text: 입력되는 text형식의 자료
		:return:
		"""
		aaa = re.compile("^[a-zA-Z]+$")  # 처음부터 끝가지 알파벳일때
		result_str = aaa.findall(str(input_text))

		bbb = re.compile("^[0-9]+$")  # 처음부터 끝가지 숫자일때
		result_num = bbb.findall(str(input_text))

		if result_str != []:
			no = 0
			result = 0
			for one in input_text.lower()[::-1]:
				num = string.ascii_lowercase.index(one) + 1
				result = result + 26 ** no * num
				no = no + 1
		elif result_num != []:
			result = int(input_text)
		else:
			result = "error"
		return result

	def change_data_position_for_list2d_by_2_index(self, input_list2d, input_no_list):
		"""
		2차원 리스트의 자료에서 각 라인별 2개의 위치를 바꾼는것
		change_position_for_list2d_by_2_index([[1,2,3], [4,5,6]], [0,2])
		[[1,2,3], [4,5,6]] ==> [[3,2,1], [6,5,4]]
		메뉴에서 제외

		:param input_list2d: list type 2dimension, 2차원의 리스트형
		:param input_no_list:
		:return:
		"""
		for before, after in input_no_list:
			for no in range(len(input_list2d)):
				value1 = input_list2d[no][before]
				value2 = input_list2d[no][after]
				input_list2d[no][before] = value2
				input_list2d[no][after] = value1
		return input_list2d

	def change_first_char_only_in_range(self, sheet_name="", xyxy="", input_2d_list=[]):
		"""
		메뉴에서 제외
		가끔 맨앞글자만 바꾸고 싶을때
		엑셀값중, 맨앞의 글자만 변경하는 것
		사용법 : change_first_char("", [1,1,100,1], [["'", ""], ["*", ""], [" ", ""],])

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_2d_list: list type 2dimension, 2차원의 리스트형
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		to_be_changed = []
		for one in input_2d_list:
			to_be_changed.append(one[0])

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				cell_value = sheet_object.Cells(x, y).Value
				one_char = str(cell_value[0])
				if cell_value[0] in to_be_changed:
					for list_1d in input_2d_list:
						one_char = one_char.replace(list_1d[0], list_1d[1])
				sheet_object.Cells(x, y).Value = one_char + cell_value[1:]

	def change_input_color_to_rgb(self, input_color):
		"""
		입력된 색깔을 rgb로 바꾸는 것
		메뉴에서 제외

		:param input_color: 색이름
		:return:
		"""
		input_type = type(input_color)
		if input_type == type(123):
			result = self.color.change_rgbint_to_rgb(input_color)
		elif input_type == type("abc"):
			result = self.color.change_scolor_to_rgb(input_color)
		elif input_type == type([]):
			result = input_color
		return result

	def change_input_data_to_list2d(self, input_data):
		"""
		:param input_data: 입력자료
		:return:

		입력된 자료형에 따라서 2차원으로 만들어 주는것
		1차원의 리스트는 [1,2,3,4]의 형태이며
		이것은 같은 가로에 세로의 글자가 다른것이다
		메뉴에서 제외
		"""
		if type(input_data) == type([]) or type(input_data) == type(()):
			if type(input_data[0]) == type([]) or type(input_data[0]) == type(()):
				result = input_data
			else:
				result = [input_data]
		elif type(input_data) == type("123") or type(input_data) == type(123):
			result = [[input_data]]
		return result

	def change_input_data_to_yline_style(self, input_data):
		"""		
		1차원리스트를 2차원으로 만들면, 세로입력을 가로입력으로 바꾸는 것이다
		메뉴에서 제외

		:param input_data: 입력자료
		:return:
		"""
		result = self.change_list1d_to_list2d(input_data)
		return result

	def change_last_char_only_in_range(self, sheet_name="", xyxy="", input_2d_list=[]):
		"""		
		엑셀값중, 맨앞의 글자만 변경하는 것
		사용법 : change_first_char("", [1,1,100,1], [["'", ""], ["*", ""], [" ", ""],])

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_2d_list: list type 2dimension, 2차원의 리스트형
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		to_be_changed = []
		for one in input_2d_list:
			to_be_changed.append(one[0])

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				cell_value = sheet_object.Cells(x, y).Value
				one_char = str(cell_value[-1])
				if cell_value[-1] in to_be_changed:
					for list_1d in input_2d_list:
						one_char = one_char.replace(list_1d[0], list_1d[1])
				sheet_object.Cells(x, y).Value = cell_value[:-1] + one_char

	def change_list1d_to_list2d(self, input_list1d):
		"""		
		1차원의 리스트를  2차원으로 만드는 것
		입력 : [1,2,3,4]
		출력 : [[1], [2], [3], [4],]
		메뉴에서 제외

		:param input_list1d: list type, 1차원 리스트형
		:return:
		"""
		result = []
		if len(input_list1d) > 0:
			if type(input_list1d[0]) != type([]):
				for one in input_list1d:
					result.append([one, ])
		return result

	def change_list1d_to_list2d_with_yline_style(self, input_list1d):
		"""
		1차원의 리스트를  2차원으로 만드는 것
		입력 : [1,2,3,4]
		출력 : [[1], [2], [3], [4],]
		메뉴에서 제외

		:param input_list1d: list type, 1차원 리스트형
		:return:
		"""
		result = self.change_list1d_to_list2d(input_list1d)
		return result

	def change_list2d_as_samelen(self, input_list2d="입력필요"):
		"""
		2차원 리스트의 최대 길이로 같게 만드는 것
		가끔 자료의 갯수가 달라서 생기는 문제가 발생할 가능성이 있는것을 맞추는것
		추가할때는 ""를 맞는갯수를 채워넣는다
		메뉴에서 제외

		:param input_list2d: list type 2dimension, 2차원의 리스트형
		:return:
		"""
		input_text = None
		max_num = max(map(lambda x: len(x), input_list2d))
		result = []
		for one in input_list2d:
			one_len = len(one)
			if max_num == one_len:
				result.append(one)
			else:
				one.extend([input_text] * (max_num - one_len))
				result.append(one)
		return result

	def change_list_size(self, xy_list, resize=[1, 1]):
		"""
		리스트의 크기를 다시 설정하는 것
		메뉴에서 제외

		:param xy_list:
		:param resize:
		:return:
		"""
		result = []
		# 자료의 x갯수를 요청한것과 비교
		if len(xy_list) < resize[0] or resize[0] == 0:
			pass
		else:
			xy_list = xy_list[:resize[0]]
		# 자료의 y갯수를 요청한것과 비교
		for x_list in xy_list:
			if len(x_list) < resize[1] or resize[1] == 0:
				pass
			else:
				x_list = xy_list[:resize[0]]
			result.append(x_list)
		return result

	def change_num_to_char(self, input_data="입력필요"):
		"""
		입력값 : 27 => 출력값 : aa
		숫자를 문자로 바꿔주는 것
		메뉴에서 제외

		:param input_data: 입력자료
		:return:
		"""
		re_com = re.compile(r"([0-9]+)")
		result_num = re_com.match(str(input_data))

		if result_num:
			base_number = int(input_data)
			result_01 = ''
			result = []
			while base_number > 0:
				div = base_number // 26
				mod = base_number % 26
				if mod == 0:
					mod = 26
					div = div - 1
				base_number = div
				result.append(mod)
			for one_data in result:
				result_01 = string.ascii_lowercase[one_data - 1] + result_01
			final_result = result_01
		else:
			final_result = input_data
		return final_result

	def change_position_for_list2d_by_2_index(self, input_list2d, input_no_list):
		"""
		2차원 리스트의 자료에서 각 라인별 2개의 위치를 바꾼는것
		change_position_for_list2d_by_2_index([[1,2,3], [4,5,6]], [0,2])
		[[1,2,3], [4,5,6]] ==> [[3,2,1], [6,5,4]]

		:param input_list2d: list type 2dimension, 2차원의 리스트형
		:param input_no_list:
		:return:
		"""
		for before, after in input_no_list:
			for no in range(len(input_list2d)):
				value1 = input_list2d[no][before]
				value2 = input_list2d[no][after]
				input_list2d[no][before] = value2
				input_list2d[no][after] = value1
		return input_list2d

	def change_rgb_to_rgbint(self, input_rgb):
		"""
		rgb인 값을 color에서 인식이 가능한 정수값으로 변경
		메뉴에서 제외

		:param input_rgb: rgb형식의 입력값
		:return:
		"""
		result = (int(input_rgb[2])) * (256 ** 2) + (int(input_rgb[1])) * 256 + int(input_rgb[0])
		return result

	def change_rgbint_to_colorname(self, rgbint):
		"""
		rgb의 정수값을 color이름으로 변경
		메뉴에서 제외

		:param rgbint: change rgb value to int, rgb를 정수로 변환한 값
		:return:
		"""
		try:
			rgblist = self.change_rgbint_to_rgb(rgbint)
			color_index = self.data_dic_colorindex_to_rgblist(rgblist)
			colorname = self.data_dic_colorname_to_colorindex(color_index)
		except:
			colorname = None
		return colorname

	def change_rgbint_to_rgb(self, input_int):
		"""
		rgb의 int값을 rgb 리슽형으로 바꾸는 것이다
		메뉴에서 제외

		:param input_int:
		:return:
		"""
		mok0, namuji0 = divmod(input_int, 256 * 256)
		mok1, namuji1 = divmod(namuji0, 256)
		result = [namuji1, mok1, mok0]
		return result

	def change_shape_degree(self, sheet_name, shape_obj, degree):
		"""
		메뉴에서 제외
		도형을 회전시키는 것
		shape _ obi :이동시킬 도형 이름

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param shape_obj: shape_obj
		:param degree: degree
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		oShape = sheet_object.Shapes(shape_obj)
		oShape.IncrementRotation(degree)

	def change_sheet_name(self, old_name="입력필요", new_name="입력필요"):
		"""
		시트이름을 변경하는 것
		메뉴에서 제외

		:param old_name:
		:param new_name:
		:return:
		"""
		all_sheet_names = self.read_sheet_name_all()
		if not new_name in all_sheet_names:
			self.xlbook.Worksheets(old_name).Name = new_name

	def change_string_address(self, input_text="입력필요"):
		"""
		입력형태 : "", "$1:$8", "1", "a","a1", "a1b1", "2:3", "b:b"
		입력된 주소값을 [x1, y1, x2, y2]의 형태로 만들어 주는 것이다
		메뉴에서 제외

		:param input_text: 입력되는 text형식의 자료
		:return:
		"""
		aaa = re.compile("[a-zA-Z]+|\d+")
		address_list = aaa.findall(str(input_text))
		temp = []
		result = []

		for one in address_list:
			temp.append(self.check_one_address(one))

		if len(temp) == 1 and temp[0][1] == "string":
			# "a"일때
			result = [0, temp[0][0], 0, temp[0][0]]
		elif len(temp) == 1 and temp[0][1] == "num":
			# 1일때
			result = [temp[0][0], 0, temp[0][0], 0]
		elif len(temp) == 2 and temp[0][1] == temp[1][1] and temp[0][1] == "string":
			# "a:b"일때
			result = [0, temp[0][0], 0, temp[1][0]]
		elif len(temp) == 2 and temp[0][1] == temp[1][1] and temp[0][1] == "num":
			# "2:3"일때
			result = [temp[0][0], 0, temp[1][0], 0]
		elif len(temp) == 2 and temp[0][1] != temp[1][1] and temp[0][1] == "num":
			# "2a"일때
			result = [temp[0][0], temp[1][0], temp[0][0], temp[1][0]]
		elif len(temp) == 2 and temp[0][1] != temp[1][1] and temp[0][1] == "string":
			# "a2"일때
			result = [temp[1][0], temp[0][0], temp[1][0], temp[0][0]]
		elif len(temp) == 4 and temp[0][1] != temp[1][1] and temp[0][1] == "num":
			# "a2b3"일때
			result = [temp[0][0], temp[1][0], temp[2][0], temp[3][0]]
		elif len(temp) == 4 and temp[0][1] != temp[1][1] and temp[0][1] == "string":
			# "2a3c"일때
			result = [temp[1][0], temp[0][0], temp[3][0], temp[2][0]]
		return result

	def change_string_address_to_xyxy(self, input_text="입력필요"):
		"""
		메뉴에서 제외

		:param input_text: 입력되는 text형식의 자료
		:return:
		"""
		result = self.change_string_address(input_text)
		return result

	def change_string_to_address(self, input_text="입력필요"):
		"""
		메뉴에서 제외

		:param input_text: 입력되는 text형식의 자료
		:return:
		"""
		result = self.change_string_address(input_text)
		return result

	def change_value_as_swapcase(self, sheet_name="", xyxy=""):
		"""
		영역안의 값을 대/소문자를 바꾸는 것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		for y in range(y1, y2 + 1):
			for x in range(x1, x2 + 1):
				temp_data = self.read_cell_value(sheet_name, [x, y])
				self.write_cell_value(sheet_name, [x, y], str(temp_data).swapcase())

	def change_value_to_capital_in_range(self, sheet_name, xyxy):
		"""
		change_text_as_capital(sheet_name, xyxy)
		선택한 영역의 값들을 첫글자만 대문자로 변경
		입력값 : 입력값없이 사용가능

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = str(sheet_object.Cells(x, y).Value)
				if value == None:
					pass
				else:
					sheet_object.Cells(x, y).Value = value.capitalize()

	def change_value_to_lower_in_range(self, sheet_name="", xyxy=""):
		"""
		선택영역안의 모든글자를 소문자로 만들어 주는것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = str(sheet_object.Cells(x, y).Value)
				if value == None:
					pass
				else:
					sheet_object.Cells(x, y).Value = value.lower()

	def change_value_to_ltrim_in_range(self, sheet_name="", xyxy=""):
		"""
		왼쪽끝의 공백을 삭제하는 것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:

		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				cell_value = str(sheet_object.Cells(x, y).Value)
				if cell_value == None:
					pass
				else:
					changed_data = str(cell_value).lstrip()
					if cell_value != changed_data:
						sheet_object.Cells(x, y).Value = changed_data
						self.paint_cell_by_scolor(sheet_name, [x, y], "yel+")

	def change_value_to_rtrim_in_range(self, sheet_name="", xyxy="", scolor_name="yel+"):
		"""
		선택한 영역의 셀 값들의 오른쪽 공백을 없앤것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param scolor_name: scolor value
		:return:

		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				cell_value = str(sheet_object.Cells(x, y).Value)
				if cell_value == None:
					pass
				else:
					changed_data = str(cell_value).rstrip()
					if cell_value != changed_data:
						sheet_object.Cells(x, y).Value = changed_data
						self.paint_cell_by_scolor(sheet_name, [x, y], scolor_name)

	def change_value_to_strikethrough_in_range(self, sheet_name="", xyxy=""):
		"""
		선택한 영역의 셀 값들을 취소선으로 만드는것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.Font.Strikethrough = True

	def change_value_to_swapcase_in_range(self, sheet_name="", xyxy=""):
		"""
		선택한 영역의 값들을 대소문자를 변경

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = str(sheet_object.Cells(x, y).Value)
				if value == None:
					pass
				else:
					sheet_object.Cells(x, y).Value = value.swapcase()

	def change_value_to_trim_in_range(self, sheet_name="", xyxy="", scolor_name="yel"):
		"""
		왼쪽끝의 공백을 삭제하는 것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param scolor_name: scolor value
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				cell_value = sheet_object.Cells(x, y).Value
				changed_data = self.excel_fun_trim(cell_value)
				if cell_value == changed_data or cell_value == None:
					pass
				else:
					sheet_object.Cells(x, y).Value = changed_data
					self.paint_cell_by_scolor(sheet_name, [x, y], scolor_name)

	def change_value_to_underline_in_range(self, sheet_name="", xyxy=""):
		"""
		선택한 영역의 셀 값들에 밑줄을 넣는 것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.Font.Underline = True

	def change_value_to_upper_in_range(self, sheet_name="", xyxy=""):
		"""
		선택한 영역의 값들을 대문자로 변경
		입력값 : 입력값없이 사용가능

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = str(sheet_object.Cells(x, y).Value)
				if value == None:
					pass
				else:
					sheet_object.Cells(x, y).Value = value.upper()

	def change_xy_to_a1(self, xy=[3, 4]):
		"""
		xy의 형태로 넘어온 셀값을 A1형식으로 바꾸는 것
		메뉴에서 제외

		:param xy: [2,3]의 형식
		:return:
		"""
		x_char = self.change_num_to_char(xy[0])
		result = str(x_char[0]) + str(xy[1])
		return result

	def change_xylist_to_addresschar(self, xy_list=[[1, 1], [2, 3], [2, 4]]):
		"""
		메뉴에서 제외

		:param xy_list: [[1, 1], [2, 3], [2, 4]]
		:return:
		"""
		result = ""
		for one_data in xy_list:
			y_char = self.change_num_to_char(one_data[1])
			result = result + str(y_char[0]) + str(one_data[0]) + ', '
		return result[:-2]

	def change_xyxy_to_pxyxy(self, xyxy):
		"""
		셀의 번호를 주면, 셀의 왼쪽과 오른쪽아래의 픽셀 주소를 돌려준다
		픽샐의 값으로 돌려주는것
		메뉴에서 제외

		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		px1, py1, px1_w, py1_h = self.read_coord_in_cell("", [x1, y1])
		px2, py2, px2_w, py2_h = self.read_coord_in_cell("", [x2, y2])

		result = [px1, py1, px2 + px2_w - px1, py2 + py2_h - py1]
		return result

	def change_xyxy_to_r1c1(self, xyxy=""):
		"""
		입력값 :	[1,2,3,4]
		출력값 : "b1:d3"
		메뉴에서 제외

		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		str_1 = self.change_num_to_char(y1)
		str_2 = self.change_num_to_char(y2)
		result = str_1 + str(x1) + ":" + str_2 + str(x2)
		return result

	def change_xyxy_to_r1r1(self, xyxy=""):
		"""
		입력값 :	[1,2,3,4]
		출력값 : "b1:b1"
		메뉴에서 제외

		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		str_1 = self.change_num_to_char(y1)
		result = str_1 + str(x1) + ":" + str_1 + str(x1)
		return result

	def check_address_value(self, input_data=""):
		"""
		입력형태 :, "", [1,2], [1,2,3,4], "$1:$8", "1", "a","a1", "a1b1", "2:3", "b:b"
		입력된 주소값을 [x1, y1, x2, y2]의 형태로 만들어 주는 것이다
		입력된 자료의 형태에 따라서 구분을 한다
		메뉴에서 제외

		:param input_data: 입력자료
		:return:
		"""
		if type(input_data) == type([]):  # 리스트형태 일때
			if len(input_data) == 2:
				result = input_data + input_data
			elif len(input_data) == 4:
				result = input_data
		elif input_data == "" or input_data == None:  # 아무것도 입력하지 않을때
			result = self.read_address_in_selection()
		elif type(input_data) == type("string"):  # 문자열일때
			result = self.change_string_address(input_data)
		else:
			result = self.read_address_in_selection()
		try:
			changed_result = [min(result[0], result[2]), min(result[1], result[3]), max(result[0], result[2]),
			                  max(result[1], result[3])]
		except:
			changed_result = result

		return changed_result

	def check_address_with_datas(self, xyxy="", input_datas="입력필요"):
		"""
		입력주소와 자료를 받아서 최소로할것인지 최대로 할것인지를 골라서 나타낼려고 한다
		[$A$1], [$A$1:$B$2], [$1:$7], [$A:$B] ["A1"],[2,1,3,2], [1,2]이 경우가 가능
		Output Style :  [["$A$2:$B$3"],["A1","B2],[2,1,3,2]]무조건 3개의 형태로 나오도록 만든다
		메뉴에서 제외

		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_datas:  입력자료
		:return:
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		result = {}
		x_len = len(input_datas)
		y_len = len(input_datas[0])

		y_len_rng = y2 - y1 + 1
		x_len_rng = x2 - x1 + 1

		max_num = max(map(lambda y: len(y), input_datas))
		min_num = min(map(lambda y: len(y), input_datas))

		max_y = max(y_len, y_len_rng)
		max_x = max(max_num, x_len_rng)
		min_y = max(y_len, y_len_rng)
		min_x = max(x_len, x_len_rng)

		# 입력할것중 가장 적은것을 기준으로 적용
		result["xyxy_min"] = [x1, y1, x1 + min_y, y1 + min_num]
		# 입력할것중 가장 큰것을 기준으로 적용
		result["xyxy_max"] = [x1, y1, x1 + max_y, y1 + max_y]
		# 일반적인기준으로 적용하는것
		result["xyxy_basic"] = [x1, y1, x1 + x_len, y1 + max_num]
		return result

	def check_cell_type(self, input_data="입력필요"):
		"""
		check_cell_type( input_data="입력필요")
		주소형태의 문자열이 어떤 형태인지 알아 내는 것
		입력값 : 주소형태의 문자열
		출려값 : "a1", "aa", "11"
		메뉴에서 제외

		:param input_data: 입력자료
		:return:
		"""
		result = ""
		if input_data[0][0] in string.ascii_lowercase and input_data[1][0] in string.digits:
			result = "a1"
		if input_data[0][0] in string.ascii_lowercase and input_data[1][0] in string.ascii_lowercase:
			result = "aa"
		if input_data[0][0] in string.digits and input_data[1][0] in string.digits:
			result = "11"
		return result

	def check_colorname_by_rgbint(self, rgbint):
		"""
		예전 코드를 위해 남겨 놓는것
		메뉴에서 제외

		:param rgbint: change rgb value to int, rgb를 정수로 변환한 값
		:return:
		"""
		result = self.change_rgbint_to_colorname(rgbint)
		return result

	def check_data_type(self, input_data="입력필요"):
		"""
		영역으로 입력된 자료의 형태를 확인해서 돌려주는 것
		입력값으로 들어온것이 리스트형태인지, 영역의 형태인지, 값의 형태인지를 알아보는것이다
		Input Style :	1개의 입력값
		Output Style : "list", "range", "value", "error"
		메뉴에서 제외

		:param input_data: 입력자료
		:return:
		"""
		if type(input_data) == type([]):
			result = "list"
		elif len(str(input_data).split(":")) > 1:
			result = "range"
		elif type(input_data) == type("aaa"):
			result = "value"
		else:
			result = "error"
		return result

	def check_datatype_for_input_data(self, input_data):
		"""
		입력된 자료형을 확인하는것
		메뉴에서 제외

		:param input_data: 입력자료
		:return:
		"""
		if type(input_data) == type([]):
			if type(input_data[0]) == type([]):
				# 2차원의 자료이므로 입력값 그대로를 돌려준다
				result = "list2d_list"
			elif type(input_data[0]) == type(()):
				result = "list_tuple"
			else:
				result = "list1d"
		elif type(input_data) == type(()):
			if type(input_data[0]) == type([]):
				# 2차원의 자료이므로 입력값 그대로를 돌려준다
				result = "tuple_list"
			elif type(input_data[0]) == type(()):
				result = "tuple_tuple"
			else:
				result = "tuple1d"
		elif type(input_data) == type(123):
			result = "int"
		elif type(input_data) == type("123"):
			result = "string"
		return result

	def check_differ_at_2_area(self, input_sa1, input_sa2):
		"""
		2개의 같은 크기의 영역의 2개 자료를 비교하여
		첫번째 같은입력된 자료형을 확인하는것
		메뉴에서 제외

		:param input_sa1:
		:param input_sa2:
		:return:
		"""
		datal = self.read_value_in_range(input_sa1[0], input_sa1[1])
		data2 = self.read_value_in_range(input_sa2[0], input_sa2[1])
		start_x = input_sa2[1][0]
		start_y = input_sa2[1][1]
		for x in range(len(datal)):
			for y in range(len(datal[0])):
				if datal[x][y] == data2[x][y]:
					pass
				else:
					self.paint_cell_by_excel_colorno(input_sa2[0], [x + start_x, y + start_y], 3)

	def check_differ_at_same_area(self, input_sa1, input_sa2):
		"""
		동일한 사이즈의 다른 영역에서 다른 것만 색칠하기
		메뉴에서 제외

		:param input_sa1:
		:param input_sa2:
		:return:
		"""
		datal = self.read_value_in_range(input_sa1[0], input_sa1[1])
		data2 = self.read_value_in_range(input_sa2[0], input_sa2[1])
		start_x = input_sa2[1][0]
		start_y = input_sa2[1][1]
		for x in range(len(datal)):
			for y in range(len(datal[0])):
				if datal[x][y] == data2[x][y]:
					pass
				else:
					self.paint_cell_by_excel_colorno(input_sa2[0], [x + start_x, y + start_y], 3)

	def check_file_in_folder(self, path, file_name):
		"""
		메뉴에서 제외

		:param path: path
		:param file_name: file_name
		:return:
		"""
		result = ""
		if path == "":
			path = "C:/Users/Administrator/Documents"
		file_name_all = self.util.read_folder_filename_all(path)
		if file_name in file_name_all:
			result = file_name
		return result

	def check_filepath(self, file_name):
		"""
		경로를 구분하는 \\과 /의 혼돈 삽입으로 다시 확인하고자 한다 가능하면 /를 사용하기를 권장 한다

		:param file_name: file_name
		:return:
		"""
		file_name = file_name.replace("\\\\", "/")
		file_name = file_name.replace("\\", "/")
		return file_name

	def check_input_color_rgb(self, input_color):
		"""
		입력값 : 색깔이름
		출력값 : rgb값
		메뉴에서 제외

		:param input_color: 색이름
		:return:
		"""
		result = self.change_input_color_to_rgb(input_color)
		return result

	def check_input_data(self, input_data):
		"""
		입력값을 확인하는 것
		메뉴에서 제외

		:param input_data: 입력자료
		:return:
		"""
		result = self.check_datatype_for_input_data(input_data)
		return result

	def check_intersect_address(self, xyxy="", input_datas="입력필요"):
		"""
		이름을 좀더 사용하기 쉽도록 만든것
		메뉴에서 제외

		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_datas:
		:return:
		"""
		result = self.check_address_with_datas(xyxy, input_datas)
		return result

	def check_list_address(self, input_list="입력필요"):
		"""
		주소값을 4자리 리스트로 만들기 위하여 사용하는것
		메뉴에서 제외

		:param input_list: list type
		:return:
		"""
		result = []
		if len(input_list) == 1:
			xy = str(input_list[0]).lower()
			# 값이 1개인경우 : ['1'], ['a']
			if xy[0] in string.digits:
				result = [xy, 0, xy, 0]
			elif xy[0].lower() in string.ascii_lowercase:
				result = [0, xy, 0, xy]
		elif len(input_list) == 2:
			# 값이 2개인경우 : ['a', '1'], ['2', '3'], ['a', 'd']
			y1 = str(input_list[0]).lower()
			x1 = str(input_list[1]).lower()
			if y1[0] in string.digits:
				if x1[0] in string.digits:
					result = [y1, 0, x1, 0]
				elif x1[0] in string.ascii_lowercase:
					result = [y1, y1, y1, y1]
			elif y1[0] in string.ascii_lowercase:
				if x1[0] in string.digits:
					result = [x1, y1, y1, y1]
				elif x1[0] in string.ascii_lowercase:
					result = [0, y1, 0, x1]
		elif len(input_list) == 4:
			y1 = str(input_list[0]).lower()
			x1 = str(input_list[1]).lower()
			y2 = str(input_list[2]).lower()
			x2 = str(input_list[3]).lower()
			# 값이 4개인경우 : ['aa', '1', 'c', '44'], ['1', 'aa', '44', 'c']
			if y1[0] in string.digits and x2[0] in string.digits:
				if x1[0] in string.ascii_lowercase and x2[0] in string.ascii_lowercase:
					result = [x1, y1, x2, y2]
				elif x1[0] in string.digits and x2[0] in string.digits:
					result = [x1, y1, x2, y2]
			elif y1[0] in string.ascii_lowercase and x2[0] in string.ascii_lowercase:
				if x1[0] in string.digits and x2[0] in string.digits:
					result = [x1, y1, x2, x2]
		final_result = []
		for one in result:
			one_value = str(one)[0]
			if one_value in string.ascii_lowercase:
				aaa = self.change_char_to_num(one)
			else:
				aaa = str(one)
			final_result.append(aaa)
		return final_result

	def check_merge_in_range(self, sheet_name="", xyxy=""):
		"""
		영역안의 병합된 자료를 알려주는것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		result = self.get_address_for_merge_in_range(sheet_name, xyxy)
		return result

	def check_numberformat(self, sheet_name, xyxy):
		"""
		셀의 여러 값들을 가지고 셀값의 형태를 분석하는 것이다
		단, 속도가 좀 느려진다

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		result = []

		for x in range(x1, x2 + 1):
			temp = []
			for y in range(y1, y2 + 1):
				one_dic = {}
				one_cell = sheet_object.Cells(x, y)
				one_dic["y"] = x
				one_dic["x"] = y
				one_dic["value"] = one_cell.Value
				one_dic["value2"] = one_cell.Value2
				one_dic["text"] = one_cell.Text
				one_dic["formular"] = one_cell.Formula
				one_dic["formularr1c1"] = one_cell.FormulaR1C1
				one_dic["numberformat"] = one_cell.NumberFormat
				one_dic["type"] = type(one_cell.Value)

				if type(one_cell.Value) is TimeType:
					# pywintypes.datetime가 맞는지를 확인하는 코드이다
					print('날짜에요!', one_cell.Value, str(type(one_cell.Value)))

				tem_1 = ""
				if (
						"h" in one_cell.NumberFormat or "m" in one_cell.NumberFormat or "s" in one_cell.NumberFormat) and ":" in one_cell.NumberFormat:
					tem_1 = "time"

				if "y" in one_cell.NumberFormat or "mmm" in one_cell.NumberFormat or "d" in one_cell.NumberFormat:
					tem_1 = "date" + tem_1

				if type(one_cell.Value) == type(123.45) and one_cell.Value > 1 and tem_1 == "time":
					tem_1 = "datetime"

				one_dic["style"] = tem_1
				temp.append(one_dic)
			result.append(temp)
		return result


	def check_one_address(self, input_text=""):
		"""
		입력된 1개의 주소를 문자인지, 숫자인지
		숫자로 변경하는 것이다
		메뉴에서 제외

		:param input_text: 입력되는 text형식의 자료
		:return:
		"""
		re_com_1 = re.compile("^[a-zA-Z]+$")  # 처음부터 끝가지 알파벳일때
		result_str = re_com_1.findall(str(input_text))

		re_com_2 = re.compile("^[0-9]+$")  # 처음부터 끝가지 숫자일때
		result_num = re_com_2.findall(str(input_text))

		if result_num == [] and result_str != []:
			address_type = "string"
			no = 0
			address_int = 0
			for one in input_text.lower()[::-1]:
				num = string.ascii_lowercase.index(one) + 1
				address_int = address_int + 26 ** no * num
				no = no + 1
		elif result_str == [] and result_num != []:
			address_type = "num"
			address_int = int(input_text)
		else:
			address_int = "error"
			address_type = "error"
		return [address_int, address_type, input_text]

	def check_same_data(self, input_list, check_line=10):
		"""
		엑셀의 선택한 자료에서 여러줄을 기준으로 같은 자료만 갖고오기
		메뉴에서 제외

		:param input_list: list type
		:param check_line:
		:return:
		"""
		result = []
		base_value = ""
		xy = self.read_address_in_activecell()
		for no in input_list:
			base_value = base_value + str(self.read_cell_value("", [xy[0], no]))

		# 혹시 1보다 작은 숫자가 나올 수있으므로, 최소시작점을 1로하기위해
		start_x = max(int(xy[0]) - check_line, 1)

		# 위로10개 아래로 10개의 자료를 확인한다
		for no in range(start_x, start_x + 20):
			cell_value = ""
			for one in input_list:
				cell_value = cell_value + str(self.read_cell_value("", [no, one]))
			if base_value == cell_value:
				# 보통 50개이상의 줄을 사용하지 않으므로 50개를 갖고온다
				temp = self.read_value_in_range("", [no, 1, no, 50])
				result.append(temp[0])
		return result

	def check_sheet_name(self, sheet_name=""):
		"""
		시트이름으로 객체를 만들어서 돌려주는 것이다
		이름이 없으면 현재 활성화된 시트를 객체로 만들어 사용한다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		if self.var_pcell["use_same_sheet"]:
			sheet_object = self.var_pcell["sheet_object"]
		elif sheet_name == "" or sheet_name == None or str(sheet_name).lower() == "activesheet":
			sheet_object = self.xlbook.ActiveSheet
		else:
			sheet_object = self.xlbook.Worksheets(str(sheet_name))
		return sheet_object

	def check_sheet_password(self, isnum="yes", istext_small="yes", istext_big="yes", isspecial="no", len_num=10):
		"""
		시트의 암호를 찾아주는것

		:param isnum:
		:param istext_small:
		:param istext_big:
		:param isspecial:
		:param len_num:
		:return:
		"""
		check_char = []
		if isnum == "yes":
			check_char.extend(list(string.digits))
		if istext_small == "yes":
			check_char.extend(list(string.ascii_lowercase))
		if istext_big == "yes":
			check_char.extend(list(string.ascii_uppercase))
		if isspecial == "yes":
			for one in "!@#$%^*M-":
				check_char.extend(one)
		zz = combinations_with_replacement(check_char, len_num)
		for aa in zz:
			try:
				pswd = "".join(aa)
				self.unlock_sheet("", pswd)
				# print("발견", pswd)
				break
			except:
				pass

	def check_string_address(self, input_text="입력필요"):
		"""
		Input Style :	"$1:$8", "1", "a","a1", "a1b1", "2:3", "b:b"
		Output Style :숫자와 문자로 된부분을 구분하는 것
		string형태의 address를 문자와 숫자로 나누는것
		메뉴에서 제외

		:param input_text: 입력되는 text형식의 자료
		:return:
		"""
		aaa = re.compile("[a-zA-Z]+|\d+")
		result = aaa.findall(str(input_text))
		return result

	def check_x_address(self, input_data="입력필요"):
		"""
		메뉴에서 제외

		:param input_data: 입력자료
		:return:
		"""
		temp = self.check_xx_address(input_data)
		result = temp[0]
		return result

	def check_xx_address(self, xyxy="입력필요"):
		"""
		입력 주소중 xx가 맞는 형식인지를 확인하는것
		결과= [2, 2]의 형태로 만들어 주는것
		메뉴에서 제외

		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		if type(xyxy) == type([]):
			if len(xyxy) == 1:
				result = [xyxy[0], xyxy[0]]
			elif len(xyxy) == 2:
				result = xyxy
		else:
			x = self.change_char_to_num(xyxy)
			result = [x, x]
		return result

	def check_xy_address(self, xyxy=""):
		"""
		x나 y의 하나를 확인할때 입력을 잘못하는 경우를 방지하기위해 사용
		Input Style :	3, [3], [2,3], D, [A,D], [D]
		Output Style : [3,3], [2,3], [4,4], [1,4]
		메뉴에서 제외

		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		result = [x1, y1]
		return result

	def check_y_address(self, input_data="입력필요"):
		"""
		결과 = ["b", "b"]의 형태로 만들어 주는것
		메뉴에서 제외

		:param input_data: 입력자료
		:return:
		"""
		temp = self.check_yy_address(input_data)
		result = temp[0]
		return result

	def check_yy_address(self, input_data="입력필요"):
		"""
		결과 = ["b", "b"]의 형태로 만들어 주는것
		메뉴에서 제외

		:param input_data: 입력자료
		:return:
		"""
		if input_data == "" or input_data == None:
			temp = self.read_address_in_selection()
			result = [temp[1], temp[3]]
		elif type(input_data) == type("string") or type(input_data) == type(123):
			temp = self.change_num_to_char(input_data)
			result = [temp, temp]
		elif type(input_data) == type([]):
			if len(input_data) == 2:
				result = input_data  # 이부분이 check_address_value와 틀린것이다
			elif len(input_data) == 4:
				temp = input_data
				result = [temp[1], temp[3]]
		else:
			temp = self.read_address_in_selection()
			result = [temp[1], temp[3]]

		new_y1 = self.change_num_to_char(result[0])
		new_y2 = self.change_num_to_char(result[1])

		return [new_y1, new_y2]

	def close(self):
		"""
		열려진 화일을 닫는것
		메뉴에서 제외

		:return:
		"""
		self.xlbook.Close(SaveChanges=0)

	# del self.xlapp

	def close_activeworkbook(self):
		"""
		열려진 화일을 닫는것
		메뉴에서 제외

		:return:
		"""
		self.xlbook.Close(SaveChanges=0)

	def close_excel(self):
		"""
		엑셀 프로그램을 끄는것

		:return:
		"""
		self.quit_excel

	def copy_range(self, sheet_name="", xyxy=""):
		"""

		영역의 복사까지만 하는 기능이다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		self.check_address_value(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2)).Copy()

	def copy_sheet(self, old_sheet_name="", new_sheet_name=""):
		"""
		:param old_sheet_name:
		:param new_sheet_name:
		:return:
		"""
		self.copy_sheet_at_same_workbook(old_sheet_name, new_sheet_name)

	def copy_sheet_at_new_workbook(self, old_sheet_name="", new_sheet_name=""):
		"""
		:param old_sheet_name:
		:param new_sheet_name:
		:return:
		"""
		sheet_object = self.check_sheet_name(old_sheet_name)
		sheet_object.Select()
		sheet_object.Copy()

	def copy_sheet_at_same_workbook(self, old_sheet_name="", new_sheet_name=""):
		"""
		:param old_sheet_name:
		:param new_sheet_name:
		:return:
		"""
		sheet_object = self.check_sheet_name(old_sheet_name)
		sheet_object.Copy(Before=sheet_object)
		if not new_sheet_name == "":
			old_name = self.read_activesheet_name()
			self.change_sheet_name(old_name, new_sheet_name)

	def copy_value_in_cell(self, sheet_name_1="", xyxy_1="", sheet_name_2="", xyxy_2=""):
		"""

		값을 일정한 영역에서 갖고온다
		만약 영역을 두개만 주면 처음과 끝의 영역을 받은것으로 간주해서 알아서 처리하도록 변경하였다
		메뉴에서 제외

		:param sheet_name_1:
		:param xyxy_1:
		:param sheet_name_2:
		:param xyxy_2:
		:return:
		"""
		sheet_object_1 = self.check_sheet_name(sheet_name_1)

		x11, y11, x21, y21 = self.check_address_value(xyxy_1)

		cell_value = sheet_object_1.Cells(x11, y11).Value
		cell_value = self.write_value_in_cell(sheet_name_2, xyxy_2, cell_value)

	def copy_xxline(self, sheet_name="", xyxy=""):
		"""

		가로영역을 복사
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, x2 = self.check_xx_address(xyxy)
		sheet_object.Rows(str(x1) + ":" + str(x2)).Copy()

	def copy_yyline(self, sheet_name="", xyxy=""):
		"""

		세로영역을 복사
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		y1, y2 = self.check_yy_address(xyxy)
		sheet_object.Columns(str(y1) + ":" + str(y2)).Copy()

	def count_range_samevalue(self, sheet_name="", xyxy=""):
		"""
		보관용
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		self.count_samevalue_in_range(sheet_name, xyxy)

	def count_samevalue_in_range(self, sheet_name="", xyxy=""):
		"""
		 입력값 : 입력값없이 사용가능
		 선택한 영역의 반복되는 갯수를 구한다
		 1. 선택한 영역에서 값을 읽어온다
		 2. 사전으로 읽어온 값을 넣는다
		 3. 열을 2개를 추가해서 하나는 값을 다른하나는 반복된 숫자를 넣는다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		all_data = self.read_value_in_range("", [x1, y1, x2, y2])
		py_dic = {}
		# 읽어온 값을 하나씩 대입한다
		for line_data in all_data:
			for one_data in line_data:
				# 키가와 값을 확인
				if one_data in py_dic:
					py_dic[one_data] = py_dic[one_data] + 1
				else:
					py_dic[one_data] = 1
		self.insert_yyline_in_range(sheet_name, 1)
		self.insert_yyline_in_range(sheet_name, 1)
		dic_list = list(py_dic.keys())
		for no in range(len(dic_list)):
			sheet_object.Cells(no + 1, 1).Value = dic_list[no]
			sheet_object.Cells(no + 1, 2).Value = py_dic[dic_list[no]]

	def count_shape_in_sheet(self, sheet_name):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		result = sheet_object.Shapes.Count
		return result

	def count_sheet_nos(self):
		"""
		시트의 갯수를 돌려준다
		메뉴에서 제외

		:return:
		"""
		return self.xlbook.Worksheets.Count

	def count_worksheet_all(self):
		"""
		출력값 : 시트의 갯수
		메뉴에서 제외

		:return:
		"""
		result = self.read_worksheet_numbers()
		return result

	def data_all(self):
		"""
		라인 두께에 대한 자료를 돌려준디
		메뉴에서 제외

		:return:
		"""
		result = self.var_common

		return result

	def data_dic_colorindex_to_colorname(self, input_colorindex):
		"""
		색이름으로 엑셀 색번호를 돌려주는것
		메뉴에서 제외

		:param input_colorindex:
		:return:
		"""
		dic_colorname_colorindex = self.var_common["excel_colorindex_vs_color_name"]

		result = dic_colorname_colorindex[int(input_colorindex)]
		return result

	def data_dic_colorindex_to_rgbint(self, input_rgbint):
		"""
		rgb int값으로 엑셀의 색번호를 돌려주는것
		메뉴에서 제외

		:param input_rgbint: rgb의 정수값
		:return:
		"""
		dic_colorindex_rgbint = self.var_common["excel_colorindex_vs_rgbint"]
		result = dic_colorindex_rgbint[int(input_rgbint)]
		return result

	def data_dic_colorindex_to_rgblist(self, rgblist):
		"""
		rgb값으로 엑셀의 색번호를 돌려주는것
		메뉴에서 제외

		:param rgblist: [r, g, b]형식
		:return:
		"""
		basic = self.var_common["dic_rgb값_vs_엑셀_색번호"]
		result = basic[rgblist]
		return result

	def data_dic_colorname_to_colorindex(self, input_colorindex):
		"""
		색번호로 색이름을 돌려주는것
		메뉴에서 제외

		:param input_colorindex: 엑셀의 56가지 번호의 색번호
		:return:
		"""
		dic_colorname_colorindex = self.var_common["dic_색이름_vs_엑셀_색번호"]

		result = dic_colorname_colorindex[int(input_colorindex)]
		return result

	def data_dic_line_position(self, input_data=""):
		"""
		라인 위치에 대한 자료를 돌려준디
		메뉴에서 제외

		:param input_data: 입력자료
		:return:
		"""
		line_position = self.var_common["dic_선위치_vs_index번호"]

		if input_data in line_position.keys():
			result = line_position[input_data]
		else:
			result = [9]
		return result

	def data_dic_line_style(self, input_data=""):
		"""
		라인 스타일에 대한 자료를 돌려준디
		메뉴에서 제외

		:param input_data: 입력자료
		:return:
		"""
		line_style_dic = self.var_common["dic_선형태_vs_번호"]

		if input_data in line_style_dic.keys():
			result = line_style_dic[input_data]
		else:
			result = 1
		return result

	def data_dic_line_thickness(self, input_data=""):
		"""
		라인 두께에 대한 자료를 돌려준디
		메뉴에서 제외

		:param input_data: 입력자료
		:return:
		"""
		line_thickness_dic = self.var_common["dic_선굵기_vs_번호"]

		if input_data in line_thickness_dic.keys():
			result = line_thickness_dic[input_data]
		else:
			result = 2
		return result

	def data_dic_rgblist_to_colorindex(self, input_colorindex):
		"""
		엑셀의 색번호로 rgb값을 돌려주는것
		메뉴에서 제외

		:param input_colorindex:
		:return:
		"""
		dic_colorindex_rgblist = self.var_common["dic_rgb값_vs_엑셀_색번호"]

		result = dic_colorindex_rgblist[int(input_colorindex)]
		return result

	def data_shift_xline_to_2d(self, input_range, repeat_no, start_xy):
		"""
		한줄의 자료를 여러줄로 바꾸어서 출력하는 것
		메뉴에서 제외

		:param input_range: 영역자료 [1,1,5,5]
		:param repeat_no:
		:param start_xy:
		:return:
		"""
		all_data_set = self.read_value_in_range("", input_range)
		for no in range(len(all_data_set[0])):
			mok, namuji = divmod(no, repeat_no)
			new_x = mok + start_xy[0]
			new_y = namuji + start_xy[1]
			self.write_value_in_cell("", [new_x, new_y], all_data_set[0][no])

	def data_shift_yline_to_2d(self, input_range, repeat_no, start_xy):
		"""
		한줄의 자료를 여러줄로 바꾸어서 출력하는 것
		메뉴에서 제외

		:param input_range: 영역자료 [1,1,5,5]
		:param repeat_no:
		:param start_xy:
		:return:
		"""
		all_data_set = self.read_value_in_range("", input_range)
		for no in range(len(all_data_set)):
			mok, namuji = divmod(no, repeat_no)
			new_x = mok + start_xy[0]
			new_y = namuji + start_xy[1]
			self.write_value_in_cell("", [new_x, new_y], all_data_set[no][0])

	def delete_all_draw_line_in_range(self, sheet_name="", xyxy=""):
		"""
		시트의 모든 라인을 지우는 것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		self.delete_all_line_in_range(sheet_name, xyxy)

	def delete_all_drawing_in_sheet(self, sheet_name=""):
		"""
		시트안의 모든 객체를 삭제하는 것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		drawings_nos = sheet_object.Shapes.Count
		print(drawings_nos)
		if drawings_nos > 0:
			for num in range(drawings_nos, 0, -1):
				# Range를 앞에서부터하니 삭제하자마자 번호가 다시 매겨져서, 뒤에서부터 삭제하니 잘된다
				sheet_object.Shapes(num).Delete()
		return drawings_nos

	def delete_all_line_in_range(self, sheet_name="", xyxy=""):
		"""
		영역의 모든선을 지운다

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		for each in [5, 6, 7, 8, 9, 10, 11, 12]:
			my_range.Borders(each).LineStyle = -4142

	def delete_all_rangename(self):
		"""
		영역이름을 다 삭제한다

		:return:
		"""
		self.delete_rangename_all()

	def delete_all_samevalue_in_range(self, sheet_name="", xyxy=""):
		"""
		영역안에서 같은것이 있으면 모두 지우고, 고유한것만 남기는것
		2개가 같으면 2개모두 지우는 것이다

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		temp_dic = {}
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		all_datas = self.read_value_in_range(sheet_name, xyxy)

		# 모든 자료의 반복 갯수와 셀주소를 저장한다
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_object.Cells(x, y).Value
				if value == None or value == "":
					pass
				else:
					if value in temp_dic.keys():
						temp_dic[value] = temp_dic[value]["num"] + 1
						temp_dic[value]["xy"].append([x, y])
					else:
						temp_dic[value] = {"num": 1, "xy": [[x, y]]}

		# 1개이상 반복된것을 모두 지우도록 한다
		for one in temp_dic.keys():
			if temp_dic[one]["num"] > 1:
				for xy_address in temp_dic[one]["xy"]:
					sheet_object.Cells(xy_address[0], xy_address[1]).Value = ""

	def delete_all_shape_in_sheet(self, sheet_name=""):
		"""
		시트의 모든 객체를 지우는 것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		self.delete_all_drawing_in_sheet(sheet_name)

	def delete_all_value_in_sheet(self, sheet_name=""):
		"""
		시트안의 모든 값만을 삭제
		시트를 그대로 둬야하는 경우에 사용
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Cells.ClearContents()

	def delete_color(self, sheet_name, xyxy):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		self.delete_color_in_range(sheet_name, xyxy)

	def delete_color_in_range(self, sheet_name="", xyxy=""):
		"""
		영역의 색을 지우는 것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.Interior.Pattern = -4142
		my_range.Interior.TintAndShade = 0
		my_range.Interior.PatternTintAndShade = 0

	def delete_continious_samevalue_in_range(self, sheet_name="", xyxy=""):
		"""
		대상 : 선택한 영역
		밑으로 같은 값들이 있으면 지우는것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		for y in range(y1, y2 + 1):
			for x in range(x2, x1 + 1, -1):
				base_value = sheet_object.Cells(x, y).Value
				up_value = str(sheet_object.Cells(x - 1, y).Value)
				if base_value == up_value:
					# self.write_value_in_cell(sheet_name, [x, y], "")
					sheet_object.Cells(x, y).Value = ""

	def delete_empty_xline_in_range(self, sheet_name, xyxy):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x2, x1, -1):
			changed_address = str(x) + ":" + str(x)
			num = self.xlapp.WorksheetFunction.CountA(sheet_object.Range(changed_address))
			if num == 0:
				sheet_object.Rows(changed_address).Delete()

	def delete_empty_yline_in_range(self, sheet_name, xyxy):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for y in range(y2, y1, -1):
			cha_y = self.change_num_to_char(y)
			changed_address = str(cha_y) + ":" + str(cha_y)
			num = self.xlapp.WorksheetFunction.CountA(sheet_object.Range(changed_address))
			if num == 0:
				sheet_object.Columns(changed_address).Delete()

	def delete_line_in_list2d_by_index(self, input_list2d, no_list):
		"""
		입력형태 : 2차원리스트, [2,5,7]
		메뉴에서 제외

		:param input_list2d: list type 2dimension, 2차원의 리스트형
		:param no_list:
		:return:
		"""
		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_list2d)):
				del input_list2d[x][one]
		return input_list2d

	def delete_linecolor(self, sheet_name, xyxy):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		self.delete_linecolor_in_range(sheet_name, xyxy)

	def delete_linecolor_in_range(self, sheet_name="", xyxy=""):
		"""
		영역안의 라인의 색을 지우는 것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.Interior.Pattern = 0
		my_range.Interior.PatternTintAndShade = 0

	def delete_link(self, sheet_name, xyxy):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		self.delete_link_in_range(sheet_name, xyxy)

	def delete_link_in_range(self, sheet_name="", xyxy=""):
		"""
		영역안의 링크를 삭제하는 것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.Hyperlinks.Delete()

	def delete_memo(self, sheet_name, xyxy):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		self.delete_memo_in_range(sheet_name, xyxy)

	def delete_memo_in_range(self, sheet_name="", xyxy=""):
		"""
		영역안의 메모를 삭제하는 것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.ClearComments()

	def delete_panthom_rangname(self):
		"""
		이름영역중에서 연결이 끊긴것을 삭제하는 것

		:return:
		"""
		cnt = self.xlapp.Names.Count
		for num in range(1, cnt + 1):
			aaa = self.xlapp.Names(num).Name
			if aaa.find("!") < 0:
				self.xlapp.Names(aaa).Delete()

	def delete_patial_value_in_range_as_0toN(self, sheet_name="", xyxy="", num="입력필요"):
		"""
		선택영역의 값중에서 일부분만 지우는것
		앞에서부터 N개까지의 글자를 삭제하는것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param num:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):

				cell_value = sheet_object.Cells(x, y).Value
				if cell_value != "" or cell_value != None or cell_value != None:
					sheet_object.Cells(x, y).Value = cell_value[int(num):]

	def delete_rangename(self, range_name):
		"""
		:param range_name: 영역이름
		:return:
		"""
		"""
		엣날 자료를 위한것으로, 더이상 사용하지 마세요
		메뉴에서 제외
		"""
		self.xlbook.Names(range_name).Delete()

	def delete_rangename_all(self):
		"""
		모든 rangename을 삭제하는 것

		:return:
		"""
		aaa = self.xlapp.Names
		for one in aaa:
			ddd = str(one.Name)
			if ddd.find("!") < 0:
				print(ddd)
				self.xlbook.Names(ddd).Delete()

	def delete_rangename_by_name(self, range_name):
		"""
		입력한 이름을 삭제한다
		name은 workbook으로 되지만 동일하게 하기위하여 sheet_name을 넣은 것이다
		메뉴에서 제외

		:param range_name: 영역이름
		:return:
		"""
		result = self.xlbook.Names(range_name).Delete()
		return result

	def delete_rangname_for_panthom(self):
		"""
		메뉴에서 제외

		:return:
		"""
		aaa = self.xlbook.Names
		cnt = self.xlbook.Names.Count
		for num in range(1, cnt + 1):
			aaa = self.xlbook.Names(num).Name
			if aaa.find("!") < 0:
				self.xlbook.Names(aaa).Delete()

	def delete_rangname_panthom(self):
		"""
		엣날 자료를 위한것으로, 더이상 사용하지 마세요

		:return:
		"""
		self.delete_rangname_for_panthom()

	def delete_samevalue_in_range(self, sheet_name="", xyxy=""):
		"""
		영역안의 같은 값을 지우는 것이다

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		set_a = set([])
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = str(sheet_object.Cells(x, y).Value)
				if value == "" or value == None:
					pass
				else:
					len_old = len(set_a)
					set_a.add(value)
					len_new = len(set_a)
					if len_old == len_new:
						sheet_object.Cells(x, y).Value = ""

	def delete_samevalue_in_range_by_many_column_are_same(self, sheet_name="", xyxy=""):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		self.delete_xxline_value_in_range_by_same_line(sheet_name, xyxy)

	def delete_shape_all_in_sheet(self, sheet_name):
		"""
		모든객체를 삭제

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		shape_no = sheet_object.Shapes.Count
		if shape_no > 0:
			for aa in range(shape_no, 0, -1):
				sheet_object.Shapes(aa).Delete()

	def delete_shape_by_name(self, sheet_name="", shape_name="입력필요"):
		"""
		객체의 이름으로 제거하는것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param shape_name:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Shapes(shape_name).Delete()

	def delete_shape_in_sheet(self, sheet_name, shape_name):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param shape_name:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Shapes(shape_name).Delete()

	def delete_sheet(self, sheet_name=""):
		"""
		엣날 자료를 위한것으로, 더이상 사용하지 마세요
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		self.delete_sheet_by_name(sheet_name)

	def delete_sheet_by_name(self, sheet_name=""):
		"""
		시트하나 삭제하기
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		try:
			sheet_object = self.check_sheet_name(sheet_name)
			self.xlapp.DisplayAlerts = False
			sheet_object.Delete()
			self.xlapp.DisplayAlerts = True
		except:
			pass

	def delete_sheet_name(self, sheet_name):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		self.delete_sheet_by_name(sheet_name)

	def delete_value_in_cell(self, sheet_name="", xyxy=""):
		"""
		셀안의 값을 삭제하는것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		sheet_object.Cells(x1, y1).ClearContents()

	def delete_value_in_range(self, sheet_name="", xyxy=""):
		"""
		영역안의 값을 삭제하는것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.ClearContents()

	def delete_value_in_range_between_a_and_b(self, sheet_name="", xyxy="", input_list=["(", ")"]):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_list: list type
		:return:
		"""
		self.delete_value_in_range_between_specific_letter(sheet_name, xyxy, input_list)

	def delete_value_in_range_between_specific_letter(self, sheet_name="", xyxy="", input_list=["(", ")"]):
		"""
		(sheet_name="", yxyx="", input_list=["(",")"])
		입력형식 : ["(",")"]
		입력자료의 두사이의 자료를 포함하여 삭제하는것
		예: abc(def)gh ==>abcgh

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_list: list type
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		input_list[0] = str(input_list[0]).strip()
		input_list[1] = str(input_list[1]).strip()

		special_char = ".^$*+?{}[]\|()"
		# 특수문자는 역슬래시를 붙이도록
		if input_list[0] in special_char: input_list[0] = "\\" + input_list[0]
		if input_list[1] in special_char: input_list[1] = "\\" + input_list[1]
		re_basic = str(input_list[0]) + ".*" + str(input_list[1])

		# 찾은값을 넣을 y열을 추가한다
		new_x = int(x2) + 1
		self.insert_yline(sheet_name, new_x)
		for y in range(y1, y2 + 1):
			temp = ""
			for x in range(x1, x2 + 1):
				cell_value = sheet_object.Cells(x, y).Value
				# print("셀 값", cell_value, re_basic)
				result_list = re.findall(re_basic, str(cell_value))

				if result_list == None or result_list == []:
					pass
				else:
					temp = temp + str(result_list)
					self.paint_cell_by_scolor("", [x, y], "yel++")
			sheet_object.Cells(y, new_x).Value = temp

	def delete_value_in_range_by_continious_samevalue(self, sheet_name="", xyxy=""):
		"""
		영역안에서 연속된 같은 값을 삭제 한다

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		# print(x1, y1, x2, y2)
		for y in range(y1, y2 + 1):
			for x in range(x2, x1 - 1, -1):
				up_value = sheet_object.Cells(x - 1, y).Value
				down_value = sheet_object.Cells(x, y).Value
				if down_value == up_value:
					sheet_object.Cells(x, y).Value = ""

	def delete_value_in_range_by_no(self, sheet_name="", xyxy="", input_no=""):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_no:
		:return:
		"""
		self.delete_patial_value_in_range_as_0toN(sheet_name, xyxy, input_no)

	def delete_value_in_range_by_step(self, sheet_name="", xyxy="", step_no=""):
		"""
		삭제 : 선택자료중 n번째 가로열의 자료를 값만 삭제하는것
		일하다보면 3번째 줄만 삭제하고싶은경우가 있다, 이럴때 사용하는 것이다

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param step_no:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			if divmod(x - x1 + 1, step_no)[1] == 0:
				sheet_object.Range(sheet_object.Cells(x, y1), sheet_object.Cells(x, y2)).ClearContents()

	def delete_value_in_usedrange(self, sheet_name=""):
		"""
		자주사용하는 것 같아서 만들어 봄
		usedrange의 값을 지우는것을 만들어 보았다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		aaa = self.read_address_usedrange(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(aaa)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.ClearContents()

	def delete_vba_module(self, module_name_list):
		"""
		입력형태 : 리스트형, 메크로 모듈이름
		역활 : 열려있는 화일안에서 입력리스트의 메크로를 삭제를 하는 것
		메뉴에서 제외

		:param module_name_list:
		:return:
		"""
		for module_name in module_name_list:
			xlmodule = self.xlbook.VBProject.VBComponents(module_name)
			self.xlbook.VBProject.VBComponents.Remove(xlmodule)

	def delete_xline(self, sheet_name="", xx=""):
		"""
		선택한영역에서 x줄의 값이 없으면 x줄을 삭제한다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xx:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		new_xx = self.check_xx_address(xx)
		sheet_object.Rows(str(new_xx[0]) + ':' + str(new_xx[1])).Delete()

	def delete_xline_in_range_as_empty(self, sheet_name="", xyxy=""):
		"""
		선택한영역에서 x줄의 값이 없으면 x줄을 삭제한다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x2, x1, -1):
			changed_address = str(x) + ":" + str(x)
			num = self.xlapp.WorksheetFunction.CountA(sheet_object.Range(changed_address))
			if num == 0:
				sheet_object.Rows(changed_address).Delete()

	def delete_xline_in_range_by_samevalue(self, sheet_name="", xyxy=""):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		self.delete_samevalue_in_range_by_many_column_are_same(sheet_name, xyxy)

	def delete_xline_in_range_by_step(self, sheet_name="", xyxy="", step_no="입력필요"):
		"""
		영역안의 자료에서 선택한 가로행을 삭제한다
		값만 삭제하는것이 아니다
		위에서부터 삭제가 되게 만든것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param step_no:
		:return:
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		del_no = 0  # 삭제된 줄수
		total_no = 1  # 천체 라인수
		for x in range(x1, x2 + 1):
			if x2 == total_no:
				break
			if divmod(total_no, step_no)[1] == 0:
				current_x = total_no - del_no
				self.delete_xline(sheet_name, [current_x, current_x])
				del_no = del_no + 1
			total_no = total_no + 1

	def delete_xline_value_in_range_by_step(self, sheet_name="", xyxy="", step_no="입력필요"):
		"""
		삭제 : 2 ==> 기존의 2번째 마다 삭제 (1,2,3,4,5,6,7 => 1,3,5,7)
		삭제 : 선택자료중 n번째 세로줄의 자료를 값만 삭제하는것
		일하다보면 3번째 줄만 삭제하고싶은경우가 있다, 이럴때 사용하는 것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param step_no:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			if divmod(x - x1 + 1, step_no)[1] == 0:
				sheet_object.Range(sheet_object.Cells(x, y1), sheet_object.Cells(x, y2)).ClearContents()

	def delete_xxline_in_sheet(self, sheet_name, xx):
		"""
		가로 한줄삭제하기
		입력형태는 2, [2,3]의 두가지가 가능하다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xx: 가로줄의 시작과 끝 => [3,5]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		new_xx = self.check_xx_address(xx)
		sheet_object.Rows(str(new_xx[0]) + ':' + str(new_xx[1])).Delete(-4121)

	def delete_xxline_value_in_range_by_same_line(self, sheet_name="", xyxy=""):
		"""
		한줄씩 비교를 해서
		줄의 모든 값이 똑같으면 처음것을 제외하고 다음 자료부터 값만 삭제하는 것이다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		all_values = self.read_value_in_range(sheet_name, xyxy)

		same_nos = self.get_nos_in_input_list2d_by_same_xline(all_values)
		for no in same_nos:
			sheet_object.Range(sheet_object.Cells(no + x1, y1),
			                   sheet_object.Cells(no + x1, y2)).ClearContents()

	def delete_yline(self, sheet_name="", yy=""):
		"""
		선택한영역에서 x줄의 값이 없으면 x줄을 삭제한다
		여러줄의 라인이 들어오더라도, 한줄만 삭제하는 것이다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param yy: 세로줄의 사작과 끝 => [3,7]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		y1, y2 = self.check_yy_address(yy)
		sheet_object.Columns(y1 + ':' + y1).Delete()

	def delete_yline_in_range_by_step(self, sheet_name="", xyxy="", step_no="입력필요"):
		"""
		선택한 영역안의 세로줄중에서 선택한 몇번째마다 y라인을 삭제하는것
		(선택한 영역안에서 3번째 마다의 y라인을 삭제하는것)

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param step_no:
		:return:
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		del_no = 0  # 삭제된 줄수
		total_no = 1  # 천체 라인수
		for y in range(y1, y2 + 1):
			if y2 == total_no:
				break
			if divmod(total_no, step_no)[1] == 0:
				current_y = total_no - del_no
				self.delete_yline(sheet_name, current_y)
				del_no = del_no + 1
			total_no = total_no + 1

	def delete_yline_value_in_range_by_step(self, sheet_name="", xyxy="", step_no="입력필요"):
		"""
		선택한 영역안의 세로줄중에서 선택한 몇번째마다 y라인의 값을 삭제하는것
		(선택한 영역안에서 3번째 마다의 y라인의 값을 삭제하는것)

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param step_no:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for y in range(y1, y2 + 1):
			if divmod(y - y1 + 1, step_no)[1] == 0:
				sheet_object.Range(sheet_object.Cells(x1, y), sheet_object.Cells(x2, y)).ClearContents()

	def delete_yyline(self, sheet_name="", yy=""):
		"""
		선택한영역에서 여러개의 y줄을 삭제한다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param yy: 세로줄의 사작과 끝 => [3,7]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		y1, y2 = self.check_yy_address(yy)
		sheet_object.Columns(y1 + ':' + y2).Delete()

	def delete_yyline_as_empty(self, sheet_name, yy_list):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param yy_list: 세로줄의 사작과 끝 => [3,7]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		for y in range(yy_list[0], yy_list[1] + 1):
			changed_address = str(y) + ":" + str(y)
			num = self.xlbook.WorksheetFunction.CountA(sheet_object.Range(changed_address))
			if num == 0:
				sheet_object.Rows(changed_address).Delete()

	def delete_yyline_in_range(self, range_obj, yy_list):
		"""
		range객체의 y열들을 삭제하는것
		메뉴에서 제외

		:param range_obj: range객체
		:param yy_list: 세로줄의 사작과 끝 => [3,7]
		:return:
		"""
		for num in yy_list:
			range_obj.Columns(int(num)).Delete()
		return range_obj

	def delete_yyline_in_sheet(self, sheet_name="", yy=""):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param yy: 세로줄의 사작과 끝 => [3,7]
		:return:
		"""
		self.delete_yyline(sheet_name, yy)

	def draw_bottomline(self, sheet_name="", xyxy="", line_style="basic", thickness="basic", color="blu"):
		"""
		엣날 자료를 위한것으로, 더이상 사용하지 마세요
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param line_style: 선의 스타일
		:param thickness: 두께
		:param color: 색깔
		:return:
		"""
		self.draw_line_one_in_range(sheet_name, xyxy, line_style, thickness, color, 9)

	def draw_bottomline_in_range(self, sheet_name, xyxy, line_style, thickness, scolor):
		"""
		선택영역에서 선을 긋는것, 맨마지막 라인에 선긋기
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param line_style: 선의 스타일
		:param thickness: 두께
		:param color: scolor 형식의 색이름, 빨강++
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		rgb_list = self.color.change_scolor_to_rgb(scolor)
		my_range.Borders(9).Color = self.color.change_rgb_to_rgbint(rgb_list)
		my_range.Borders(9).Weight = thickness
		my_range.Borders(9).LineStyle = line_style

	def draw_detail_line_in_range(self, **input):
		"""
		선택영역에서 선을 긋는것
		선긋기를 좀더 상세하게 사용할수 있도록 만든것
		밐의 base_data의 값들을 이용해서 입력하면 된다
		메뉴에서 제외

		:param input:
		:return:
		"""
		enum_line = self.var_common["dic_선모양_vs_index번호"]
		base_data = self.var_common["base_cell_data"]
		# 기본자료에 입력받은값을 update하는것이다
		sheet_object = self.check_sheet_name("")
		base_data.update(input)
		sheet = self.check_sheet_name(base_data["sheet_name"])
		set_line = sheet_object.Shapes.AddLine(base_data["xyxy"][0], base_data["xyxy"][1], base_data["xyxy"][2],
		                                       base_data["xyxy"][3])
		set_line.Select()
		set_line.Line.ForeColor.RGB = base_data["color"]
		set_line.Line.DashStyle = enum_line[base_data["line_style"]]
		set_line.Line.Weight = base_data["thickness"]
		set_line.Line.Transparency = base_data["transparency"]
		# 엑셀에서는 Straight Connector 63의 형태로 이름이 자동적으로 붙여진다
		set_line.Line.BeginArrowheadStyle = enum_line[base_data["head_style"]]
		set_line.Line.BeginArrowheadLength = enum_line[base_data["head_length"]]
		set_line.Line.BeginArrowheadWidth = enum_line[base_data["head_width"]]
		set_line.Line.EndArrowheadStyle = enum_line[base_data["tail_style"]]  # 화살표의 머리의 모양
		set_line.Line.EndArrowheadLength = enum_line[base_data["tail_length"]]  # 화살표의 길이
		set_line.Line.EndArrowheadWidth = enum_line[base_data["tail_width"]]  # 화살표의 넓이
		result = set_line.Name
		return result

	def draw_inner_xline(self, sheet_name, xyxy, line_style, thickness, scolor):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param line_style: 선의 스타일
		:param thickness: 두께
		:param color: scolor 형식의 색이름, 빨강++
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		rgb_list = self.color.change_scolor_to_rgb(scolor)
		my_range.Borders(12).Color = self.color.change_rgb_to_rgbint(rgb_list)
		my_range.Borders(12).Weight = thickness
		my_range.Borders(12).LineStyle = line_style

	def draw_inner_yline(self, sheet_name, xyxy, line_style, thickness, scolor):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param line_style: 선의 스타일
		:param thickness: 두께
		:param color: scolor 형식의 색이름, 빨강++
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		rgb_list = self.color.change_scolor_to_rgb(scolor)
		my_range.Borders(11).Color = self.color.change_rgb_to_rgbint(rgb_list)
		my_range.Borders(11).Weight = thickness
		my_range.Borders(11).LineStyle = line_style

	def draw_innerx_line_in_range(self, sheet_name="", xyxy="", line_style="basic", thickness="basic", color="blu"):
		"""
		선택영역에서 선을 긋는것, 안쪽에 x라인 선긋기
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param line_style: 선의 스타일
		:param thickness: 두께
		:param color: 색깔
		:return:
		"""
		self.draw_line_one_in_range(sheet_name, xyxy, line_style, thickness, color, 12)

	def draw_inneryline_in_range(self, sheet_name="", xyxy="", line_style="basic", thickness="basic", color="blu"):
		"""
		선택영역에서 선을 긋는것, 안쪽에 y라인 선긋기
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param line_style: 선의 스타일
		:param thickness: 두께
		:param color: 색깔
		:return:
		"""
		self.draw_line_one_in_range(sheet_name, xyxy, line_style, thickness, color, 11)

	def draw_left_line(self, sheet_name="", xyxy="", line_style="basic", thickness="basic", color="blu"):
		"""
		엣날 자료를 위한것으로, 더이상 사용하지 마세요
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param line_style: 선의 스타일
		:param thickness: 두께
		:param color: 색깔
		:return:
		"""
		self.draw_line_one_in_range(sheet_name, xyxy, line_style, thickness, color, 7)

	def draw_left_line_in_range(self, sheet_name, xyxy, line_style, thickness, scolor):
		"""
		선택영역에서 선을 긋는것, 왼쪽에 선긋기
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param line_style: 선의 스타일
		:param thickness: 두께
		:param color: scolor 형식의 색이름, 빨강++
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		rgb_list = self.color.change_scolor_to_rgb(scolor)
		my_range.Borders(7).Color = self.color.change_rgb_to_rgbint(rgb_list)
		my_range.Borders(7).Weight = thickness
		my_range.Borders(7).LineStyle = line_style

	def draw_line(self, sheet_name, xyxy, input_list):
		"""
	    draw_range_line(sheet_name="", xyxy="", input_list)
	    [선의위치, 라인스타일, 굵기, 색깔]
	    입력예 : [7,1,2,1], ["left","-","t0","bla"]
	    선의위치 (5-대각선 오른쪽, 6-왼쪽대각선, 7:왼쪽, 8;위쪽, 9:아래쪽,
			10:오른쪽, 11:안쪽세로, 12:안쪽가로)
	    라인스타일 (1-실선, 2-점선, 3-가는점선, 6-굵은실선,
	    굵기 (0-이중, 1-얇게, 2-굵게)
	    색깔 (0-검정, 1-검정, 3-빨강),
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_list: list type
		:return:
	    """
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		line_type = self.var_common["dic_선위치_vs_번호"]
		line_style_dic = self.var_common["dic_선형태_vs_번호"]
		weight_dic = self.var_common["dic_선굵기_vs_번호"]

		rgb_list = self.color.change_scolor_to_rgb(input_list[3])
		my_range.Borders(line_type[input_list[0]]).Color = self.color.change_rgb_to_rgbint(rgb_list)
		my_range.Borders(line_type[input_list[0]]).Weight = weight_dic[input_list[2]]
		my_range.Borders(line_type[input_list[0]]).LineStyle = line_style_dic[input_list[1]]

	def draw_line_in_pxyxy_range(self, sheet_name, line_xyxy, rgb_list):
		"""
		선택영역에서 선을 긋는것
		pixel을 기준으로 선긋기
		선을 그을때는 위치와 넓이 높이로 긋는데, change_xyxy_to_pxyxy을 사용하면 셀위치를 그렇게 바꾸게 만든다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param line_xyxy:
		:param rgb_list:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(line_xyxy)
		pxyxy = self.change_xyxy_to_pxyxy([x1, y1, x2, y2])

		sheet_object.Shapes.AddLine(pxyxy[0], pxyxy[1], pxyxy[2], pxyxy[3]).Select()
		self.xlapp.Selection.ShapeRange.Line.ForeColor.RGB = self.color.change_rgb_to_rgbint(rgb_list)
		self.xlapp.Selection.ShapeRange.Line.Weight = 5

	def draw_line_in_range(self, sheet_name="", xyxy="", position="", scolor="", line_style="", thickness=""):
		"""
		입력예 : [선의위치, 색깔, 라인스타일, 굵기] ==> [7,1,2,1], "", "",""
		""으로 된것이 기본으로 설정하는 것이다
		"l": left, "t": top, "b": bottom, "r": right, "h": horizental, "v": vertical, "a": all,"o": outside,"/": "/","\\": "\",
		""으로 된것이 기본으로 설정하는 것이다
		color = rgb 값
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param position: 위치
		:param color: scolor 형식의 색이름, 빨강++
		:param line_style: 선의 스타일
		:param thickness: 두께
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		line_position = self.var_common["dic_선위치_vs_번호"]
		line_thickness_dic = self.var_common["dic_선굵기_vs_번호"]
		line_style_dic = self.var_common["dic_선형태_vs_번호"]

		rgb_list = self.color.change_scolor_to_rgb(scolor)
		colorint = self.color.change_rgb_to_rgbint(rgb_list)
		aa = []
		if type(position) == type([]):
			for one in position:
				aa.extend(line_position[one])
		else:
			aa.extend(line_position[position])

		for po_no in aa:
			my_range.Borders(po_no).Color = colorint
			my_range.Borders(po_no).Weight = line_thickness_dic[str(thickness)]
			my_range.Borders(po_no).LineStyle = line_style_dic[line_style]

	def draw_line_in_range_as_basic(self, sheet_name="", xyxy="", position="all", scolor="black", line_style="basic",
	                                thickness="thin"):
		"""
		입력예 : [선의위치, 색깔, 라인스타일, 굵기] ==> [7,1,2,1], "", "",""
		""으로 된것이 기본으로 설정하는 것이다
		"l": left, "t": top, "b": bottom, "r": right, "h": horizental, "v": vertical, "a": all,"o": outside,"/": "/","\\": "\",
		""으로 된것이 기본으로 설정하는 것이다
		color = rgb 값
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param position: 위치
		:param color: scolor 형식의 색이름, 빨강++
		:param line_style: 선의 스타일
		:param thickness: 두께
		:return:
		"""
		line_position = self.var_common["dic_선위치_vs_index번호"]
		line_thickness_dic = self.var_common["dic_선굵기_vs_번호"]
		line_style_dic = self.var_common["dic_선형태_vs_번호"]

		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		rgb_list = self.color.change_scolor_to_rgb(scolor)
		colorint = self.color.change_rgb_to_rgbint(rgb_list)
		aa = []
		if type(position) == type([]):
			for one in position:
				aa.extend(line_position[one])
		else:
			aa.extend(line_position[position])

		for po_no in aa:
			my_range.Borders(po_no).Color = colorint
			my_range.Borders(po_no).Weight = line_thickness_dic[str(thickness)]
			my_range.Borders(po_no).LineStyle = line_style_dic[line_style]

	def draw_line_one_in_range(self, sheet_name="", xyxy="", line_style="basic", thickness="basic", color="blu",
	                           line_position=""):
		"""
		선택영역에서 선을 긋는것
		라인의 위치에 따라서 선을 긋는것이다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param line_style: 선의 스타일
		:param thickness: 두께
		:param color: 색깔
		:param line_position:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		rgb_list = self.color.change_scolor_to_rgb(color)
		my_range.Borders(line_position).Color = self.color.change_rgb_to_rgbint(rgb_list)
		my_range.Borders(line_position).Weight = self.data_dic_line_thickness(thickness)
		my_range.Borders(line_position).LineStyle = self.data_dic_line_style(line_style)

	def draw_right_line(self, sheet_name, xyxy, line_style, thickness, scolor):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param line_style: 선의 스타일
		:param thickness: 두께
		:param color: scolor 형식의 색이름, 빨강++
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		rgb_list = self.color.change_scolor_to_rgb(scolor)
		my_range.Borders(10).Color = self.color.change_rgb_to_rgbint(rgb_list)
		my_range.Borders(10).Weight = thickness
		my_range.Borders(10).LineStyle = line_style

	def draw_top_line(self, sheet_name, xyxy, line_style, thickness, scolor):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param line_style: 선의 스타일
		:param thickness: 두께
		:param color: scolor 형식의 색이름, 빨강++
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		rgb_list = self.color.change_scolor_to_rgb(scolor)
		my_range.Borders(8).Color = self.color.change_rgb_to_rgbint(rgb_list)
		my_range.Borders(8).Weight = thickness
		my_range.Borders(8).LineStyle = line_style

	def draw_triangle(self, xyxy, per=100, reverse=1, size=100):
		"""
		직각삼각형
		정삼각형에서 오른쪽이나 왼쪽으로 얼마나 더 간것인지
		100이나 -100이면 직삼각형이다
		사각형은 왼쪽위에서 오른쪽 아래로 만들어 진다
		메뉴에서 제외

		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param per:
		:param reverse:
		:param size:
		:return:
		"""
		x1, y1, x2, y2 = xyxy
		width = x2 - x1
		height = y2 - y1
		lt = [x1, y1]  # left top
		lb = [x2, y1]  # left bottom
		rt = [x1, y2]  # right top
		rb = [x2, y2]  # right bottom
		tm = [x1, int(y1 + width / 2)]  # 윗쪽의 중간
		lm = [int(x1 + height / 2), y1]  # 윗쪽의 중간
		rm = [int(x1 + height / 2), y1]  # 윗쪽의 중간
		bm = [x2, int(y1 + width / 2)]  # 윗쪽의 중간
		center = [int(x1 + width / 2), int(y1 + height / 2)]

		result = [lb, rb, rt]
		return result

	def draw_user_style_02(self, sheet_name="", xyxy=""):
		"""
		선택영역에서 선을 긋는것
		사용자가 만든 스타일의 선긋기
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		range_head = [x1, y1, x1, y2]
		range_body = [x1 + 1, y1, x2 - 1, y2]
		range_tail = [x2, y1, x2, y2]
		range_outside = [x1, y1, x2, y2]

		line_list_head = [["o", "bla", "", "5"], ["h", "bla", "", "5"], ]
		line_list_body = [["v", "bla", "", "4"], ["h", "bla", "", "5"], ]
		line_list_tail = [["o", "bla", "", "5"], ["h", "bla", "", "5"], ]
		line_list_outside = [["o", "bla", "", "6"], ]

		for one in line_list_head:
			self.draw_line_in_range(sheet_name, range_head, one[0], one[1], one[2], one[3])
		for one in line_list_body:
			self.draw_line_in_range(sheet_name, range_body, one[0], one[1], one[2], one[3])
		for one in line_list_tail:
			self.draw_line_in_range(sheet_name, range_tail, one[0], one[1], one[2], one[3])
		for one in line_list_outside:
			self.draw_line_in_range(sheet_name, range_outside, one[0], one[1], one[2], one[3])

	def excel_fun_ltrim(self, input_data):
		"""
		메뉴에서 제외

		:param input_data: 입력자료
		:return:
		"""
		aaa = self.xlapp.WorksheetFunction.LTrim(input_data)
		return aaa

	def excel_fun_rtrim(self, input_data):
		"""
		엑셀의 함수를 사용해서 값을 바꾸는 것이다
		메뉴에서 제외

		:param input_data: 입력자료
		:return:
		"""
		aaa = self.xlapp.WorksheetFunction.RTrim(input_data)
		return aaa

	def excel_fun_trim(self, input_data="입력필요"):
		"""
		엑셀의 함수를 사용해서 값을 바꾸는 것이다
		메뉴에서 제외

		:param input_data: 입력자료
		:return:
		"""
		aaa = self.xlapp.WorksheetFunction.Trim(input_data)
		return aaa

	def find_word_in_range(self, sheet_name="", xyxy="", input_text=""):
		"""
		영역안의 글자를 찾는다

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_text: 입력되는 text형식의 자료
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		first_range = my_range.Find(input_text)
		temp_range = first_range
		if first_range != None:
			while 1:
				temp_range = my_range.FindNext(temp_range)
				if temp_range == None or temp_range == first_range.Address:
					break
				else:
					temp_range = temp_range

	def get_4_edge_xy_for_xyxy(self, xyxy=[1, 2, 3, 4]):
		"""
		영역을 주면, 4 개의 꼭지점을 돌려주는것
		기준은 왼쪽위부터 시계방향으로 돌아간다
		메뉴에서 제외

		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		x1, y1, x2, y2 = xyxy
		result = [[x1, y1], [x1, y2], [x2, y2], [x2, y1]]
		return result

	def get_activesheet_object(self):
		"""
		메뉴에서 제외

		:return:
		"""
		sheet_name = self.xlapp.ActiveSheet.Name
		sheet_object = self.check_sheet_name(sheet_name)
		return sheet_object

	def get_address_for_merge_in_range(self, sheet_name="", xyxy=""):
		"""
		영역안의 병합된 자료를 알려주는것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		result = []

		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.read_address_for_usedrange(sheet_name)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				my_range = sheet_object.Cells(x, y)
				# print(x,y,my_range.MergeCells)
				if my_range.MergeCells:
					my_range.Select()
					ddd = self.read_address_for_selection()
					if not ddd in result:
						result.append(ddd)
		return result

	def get_cell_object(self, sheet_name="", xy=[7, 7]):
		"""
		셀 객체를 돌려준다

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xy: [가로번호, 세로번호]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		cell_object = sheet_object.Cells(xy[0], xy[1])
		return cell_object

	def get_diagonal_xy(self, xyxy=[5, 9, 12, 21]):
		"""
		좌표와 대각선의 방향을 입력받으면, 대각선에 해당하는 셀을 돌려주는것
		좌표를 낮은것 부터 정렬하기이한것 [3, 4, 1, 2] => [1, 2, 3, 4]
		메뉴에서 제외

		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		result = []
		if xyxy[0] > xyxy[2]:
			x1, y1, x2, y2 = xyxy[2], xyxy[3], xyxy[0], xyxy[1]
		else:
			x1, y1, x2, y2 = xyxy

		x_height = abs(x2 - x1) + 1
		y_width = abs(y2 - y1) + 1
		step = x_height / y_width
		temp = 0

		if x1 <= x2 and y1 <= y2:
			# \형태의 대각선
			for y in range(1, y_width + 1):
				x = y * step
				if int(x) >= 1:
					final_x = int(x) + x1 - 1
					final_y = int(y) + y1 - 1
					if temp != final_x:
						result.append([final_x, final_y])
						temp = final_x
		else:
			for y in range(y_width, 0, -1):
				x = x_height - y * step

				final_x = int(x) + x1
				final_y = int(y) + y1 - y_width
				temp_no = int(x)

				if temp != final_x:
					temp = final_x
					result.append([final_x, final_y])
		return result

	def get_intersect_address_with_range1_and_range2(self, rng1="입력필요", rng2="입력필요"):
		"""
		두개의 영역에서 교차하는 구간을 돌려준다
		만약 교차하는게 없으면 ""을 돌려준다
		메뉴에서 제외

		:param rng1: [1,1,5,5]형식 1번째
		:param rng2: [1,1,5,5]형식 2번째
		:return:
		"""
		range_1 = self.check_address_value(rng1)
		range_2 = self.check_address_value(rng2)
		x11, y11, x12, y12 = range_1
		x21, y21, x22, y22 = range_2
		if x11 == 0:
			x11 = 1
			x12 = 1048576
		if x21 == 0:
			x21 = 1
			x22 = 1048576
		if y11 == 0:
			y11 = 1
			y12 = 16384
		if y21 == 0:
			y21 = 1
			y22 = 16384
		new_range_x = [x11, x21, x12, x22]
		new_range_y = [y11, y21, y12, y22]
		new_range_x.sort()
		new_range_y.sort()
		if x11 <= new_range_x[1] and x12 >= new_range_x[2] and y11 <= new_range_y[1] and y12 >= new_range_y[1]:
			result = [new_range_x[1], new_range_y[1], new_range_x[2], new_range_y[2]]
		else:
			result = "교차점없음"
		return result

	def get_intersect_address_with_range_and_input_address(self, xyxy="", input_datas="입력필요"):
		"""
		이름을 좀더 사용하기 쉽도록 만든것
		메뉴에서 제외

		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_datas:
		:return:
		"""
		result = self.check_address_with_datas(xyxy, input_datas)
		return result

	def get_nos_in_input_list2d_by_same_xline(self, input_2dlist=""):
		"""
		2dlist의 자료의 형태로 된것중에서
		위에서 부터 같은것을 삭제 한다
		0,3,5의 3개가 같은것이라면 제일 앞의 1개는 제외하고 [3,5]를 돌려준다
		메뉴에서 제외

		:param input_2dlist: 2차원자료의 리스트
		:return:
		"""
		all_datas = input_2dlist
		total_len = len(all_datas)
		same_nos = []
		for no in range(total_len):
			if no in same_nos:
				pass
			else:
				one_list = all_datas[no]
				# print(one_list)
				for num in range(no + 1, total_len):
					if num in same_nos:
						pass
					else:
						if one_list == all_datas[num]:
							same_nos.append(num)
		return same_nos

	def get_same_value_value_in_range(self, sheet_name="", xyxy=""):
		"""
		선택한 자료중에서 고유한 자료만을 골라내는 것이다
		1. 관련 자료를 읽어온다
		2. 자료중에서 고유한것을 찾아낸다
		3. 선택영역에 다시 쓴다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		temp_datas = self.read_value_in_range("", xyxy)
		temp_result = []
		for one_list_data in temp_datas:
			for one_data in one_list_data:
				if one_data in temp_result or type(one_data) == type(None):
					pass
				else:
					temp_result.append(one_data)
		self.delete_value_in_range("", xyxy)
		for num in range(len(temp_result)):
			mox, namuji = divmod(num, x2 - x1 + 1)
			sheet_object.Cells(x1 + namuji, y1 + mox).Value = temp_result[num]

	def get_sheet_object(self, sheet_name=""):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		if str(sheet_name).lower() == "activesheet" or sheet_name == "":
			sheet = self.xlapp.ActiveSheet
		elif sheet_name in self.read_activesheet_name():
			sheet_object = self.check_sheet_name(sheet_name)
		else:
			self.insert_sheet()
			old_sheet_name = self.read_activesheet_name()
			self.change_sheet_name(old_sheet_name, sheet_name)
			sheet_object = self.check_sheet_name(sheet_name)
		return sheet_object

	def get_unique_value_in_range(self, sheet_name="", xyxy=""):
		"""
		선택한 자료중에서 고유한 자료만을 골라내는 것이다
		1. 관련 자료를 읽어온다
		2. 자료중에서 고유한것을 찾아낸다
		3. 선택영역에 다시 쓴다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		temp_datas = self.read_value_in_range("", xyxy)
		temp_result = []
		for one_list_data in temp_datas:
			for one_data in one_list_data:
				if one_data in temp_result or type(one_data) == type(None):
					pass
				else:
					temp_result.append(one_data)
		self.delete_value_in_range("", xyxy)
		for num in range(len(temp_result)):
			mox, namuji = divmod(num, x2 - x1 + 1)
			sheet_object.Cells(x1 + namuji, y1 + mox).Value = temp_result[num]

	def get_vba_module_name_all(self):
		"""
		현재 열려진 엑셀 화일안의 매크로모듈 이름을 찾아서 돌려주는 것
		아래에 1,2,3을 쓴것은 모듈의 종류를 여러가지인데, 해당하는 모듈의 종류이며.
		이것을 하지 않으면 다른 종류의 것들도 돌려주기 때문이다

		 xlapp.Close(SaveChanges=False)
		 xlapp.Quit()
		 del.xlapp
		메뉴에서 제외

		:return:
		"""
		result = []
		for i in self.xlbook.VBProject.VBComponents:
			if i.type in [1, 2, 3]:
				result.append(i.Name)
		return result

	def get_xxline_object(self, sheet_name, xx):
		"""
		xx영역을 객체로 돌려주는것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xx: 가로줄의 시작과 끝 => [3,5]
		:return:
		"""
		new_x = self.check_xx_address(xx)
		sheet_object = self.check_sheet_name(sheet_name)
		result = sheet_object.Rows(str(new_x[0]) + ':' + str(new_x[1]))
		return result

	def get_xy_list_for_circle(self, r, precious=10, xy=[0, 0]):
		"""
		엑셀을 기준으로, 반지름이 글자를 원으로 계속 이동시키는 것
		메뉴에서 제외

		:param r: 반지금
		:param precious: 얼마나 정밀하게 할것인지, 1도를 몇번으로 나누어서 계산할것인지
		:param xy: [가로번호, 세로번호]
		:return:
		"""
		result = []
		temp = []
		for do_1 in range(1, 5):
			for do_step in range(90 * precious + 1):
				degree = (do_1 * do_step) / precious
				# r을 더하는 이유는 마이너스는 않되므로 x, y측을 이동시키는것
				x = math.cos(degree) * r
				y = math.sin(degree) * r
				new_xy = [int(round(x)), int(round(y))]

				if not new_xy in temp:
					temp.append(new_xy)
		area_1 = []
		area_2 = []
		area_3 = []
		area_4 = []

		for x, y in temp:
			new_x = x + r + 1 + xy[0]
			new_y = y + r + 1 + xy[1]

			if x >= 0 and y >= 0:
				area_1.append([new_x, new_y])
			elif x >= 0 and y < 0:
				area_2.append([new_x, new_y])
			elif x < 0 and y < 0:
				area_3.append([new_x, new_y])
			elif x < 0 and y >= 0:
				area_4.append([new_x, new_y])
		area_1.sort()
		area_1.reverse()
		area_2.sort()
		area_3.sort()
		area_4.sort()
		area_4.reverse()

		result.extend(area_2)
		result.extend(area_1)
		result.extend(area_4)
		result.extend(area_3)
		return result

	def get_yyline_object(self, sheet_name, yy):
		"""
		yy영역을 객체로 돌려주는것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param yy: 세로줄의 사작과 끝 => [3,7]
		:return:
		"""
		new_y = self.check_yy_address(yy)
		sheet_object = self.check_sheet_name(sheet_name)
		result = sheet_object.Columns(str(new_y[0]) + ':' + str(new_y[1]))
		return result

	def history(self):
		"""
		revision에대한 간략한 설명을 넣을 것입니다
		메뉴에서 제외

		:return:
		"""
		result = """
			2023-03-02 : 전반적으로 이름을 수정함
			2023-05-09 : 이름과 부족한 것을 추가함
			"""
		return result

	def insert_excel_function_in_cell(self, sheet_name, xy, input_fucntion, input_xyxy):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xy: [가로번호, 세로번호]
		:param input_fucntion:
		:param input_xyxy:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		range = self.change_xyxy_to_r1c1(input_xyxy)
		x1, y1, x2, y2 = self.check_address_value(xy)
		result = "=" + input_fucntion + "(" + range + ")"
		sheet_object.Cells(x1, y1).Value = result

	def insert_image_in_sheet(self, sheet_name, file_path, xywh, link=0, image_in_file=1):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param file_path:
		:param xywh: [x, y, width, height]
		:param link:
		:param image_in_file:
		:return:
		"""
		self.insert_picture_in_sheet(sheet_name, file_path, xywh, link, image_in_file)

	def insert_image_in_xyxy(self, sheet_name, xyxy, file_path):
		"""
		image화일을 넣는것
		선택한 영역안에 자동으로 올수있도록 만들어 보자
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param file_path:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		xywh = self.change_xyxy_to_pxyxy(xyxy)
		sheet_object.Shapes.AddPicture(file_path, 0, 1, xywh[0], xywh[1], xywh[2], xywh[3])

	def insert_line_in_sheet(self, sheet_name, xx):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xx: 가로줄의 시작과 끝 => [3,5]
		:return:
		"""
		self.insert_xxline(sheet_name, xx)

	def insert_list2d_blank_by_index(self, input_list2d, no_list):
		"""
		입력형태 : 2차원리스트, [2,5,7]
		메뉴에서 제외

		:param input_list2d: list type 2dimension, 2차원의 리스트형
		:param no_list:
		:return:
		"""
		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_list2d)):
				input_list2d[x].insert(int(one), "")
		return input_list2d

	def insert_picture_in_sheet(self, sheet_name, file_path, xywh, link=0, image_in_file=1):
		"""
		image화일을 넣는것
		선택한 영역안에 자동으로 올수있도록 만들어 보자
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param file_path:
		:param xywh: [x, y, width, height]
		:param link:
		:param image_in_file:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		rng = sheet_object.Cells(xywh[0], xywh[1])
		# sh.Shapes.AddPicture("화일이름", "링크가있나", "문서에저장", "x좌표", "y좌표", "넓이","높이")
		sheet_object.Shapes.AddPicture(file_path, link, image_in_file, rng.Left, rng.Top, xywh[2], xywh[3])

	def insert_sheet(self, sheet_name=""):
		"""
		시트하나 추가하기
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		self.xlbook.Worksheets.Add()
		if sheet_name:
			old_name = self.xlapp.ActiveSheet.Name
			self.xlbook.Worksheets(old_name).Name = sheet_name

	def insert_sheet_new(self, sheet_name=""):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		self.insert_sheet(sheet_name)

	def insert_sheet_with_name(self, sheet_name="입력필요"):
		"""
		시트이름과 함께 시트하나 추가하기
		함수의 공통적인 이름을 위해서 만든것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		self.insert_sheet(sheet_name)

	def insert_xline(self, sheet_name, x):
		"""
		가로열을 한줄삽입하기
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param x:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		num_r1 = self.change_char_to_num(x)
		sheet_object.Rows(str(num_r1) + ':' + str(num_r1)).Insert(-4121)

	def insert_xline_in_range_by_step(self, sheet_name="", xyxy="", step_no="입력필요"):
		"""
		n번째마다 열을 추가하는것
		새로운 가로열을 선택한 영역에 1개씩 추가하는것
		n번째마다는 n+1번째가 추가되는 것
		메뉴에서 제외

		2023-09-27 : 뒤에서부터 실행하는 부분으로 변경함

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param step_no:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		for x in range(x2, x1, -1):
			mok, namuji = divmod(x, int(step_no))
			if namuji == step_no - 1:
				# print("===>", x + x1)
				x_no = self.change_char_to_num(x + x1)
				# print("===>", x_no)
				sheet_object.Range(str(x_no) + ':' + str(x_no)).Insert(-4121)

	def insert_xline_with_sum_value_for_each_yline(self, input_list2d, xy):
		"""
		선택한 영역의 세로자료들을 다 더해서 제일위의 셀에 다시 넣는것
		메뉴에서 제외

		:param input_list2d: list type 2dimension, 2차원의 리스트형
		:param xy: [가로번호, 세로번호]
		:return:
		"""
		x_len = len(input_list2d)
		y_len = len(input_list2d[0])
		for y in range(y_len):
			temp = ""
			for x in range(x_len):
				self.write_value_in_cell("", [x + xy[0], y + xy[1]], "")
				if input_list2d[x][y]:
					# print(input_list2d[x][y])
					temp = temp + " " + input_list2d[x][y]
			# print(temp)
			self.write_value_in_cell("", [xy[0], y + xy[1]], str(temp).strip())

	def insert_xxline(self, sheet_name, xx_list):
		"""
		가로열을 한줄삽입하기
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xx_list:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1 = self.change_char_to_num(xx_list[0])
		x2 = self.change_char_to_num(xx_list[1])
		min_x1 = min(x1, x2)
		max_x2 = max(x1, x2)
		for num in range(max_x2 + 1, min_x1, -1):
			sheet_object.Range(str(num) + ':' + str(num)).Insert(-4121)

	def insert_xxline_in_range(self, sheet_name="", xx_list="입력필요"):
		"""
		가로열을 한줄삽입하기
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xx_list:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		if type(xx_list) == type([]) and len(xx_list) == 1:
			x2 = x1 = self.change_char_to_num(xx_list[0])
		elif type(xx_list) == type([]) and len(xx_list) == 2:
			x1 = self.change_char_to_num(xx_list[0])
			x2 = self.change_char_to_num(xx_list[1])
		else:
			x2 = x1 = self.change_char_to_num(xx_list)
		sheet_object.Rows(str(x1) + ':' + str(x2)).Insert()

	def insert_yline(self, sheet_name, y):
		"""
		세로행을 한줄삽입하기
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param y:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		num_r1 = self.change_num_to_char(y)
		sheet_object.Columns(str(num_r1) + ':' + str(num_r1)).Insert(-4121)

	def insert_yline_in_range_by_step(self, sheet_name="", xyxy="", step_no="입력필요"):
		"""
		 n번째마다 열을 추가하는것
		 새로운 가로열을 선택한 영역에 1개씩 추가하는것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param step_no:
		:return:
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		# 일정부분으로 추가되는것을 앞에서부터 적용
		step_no = int(step_no)
		add_y = 0
		for no in range(0, y2 - y1 + 1):
			y = add_y + no
			if divmod(y, step_no)[1] == step_no - 1:
				self.insert_yyline(sheet_name, y + y1)
				add_y = add_y + 1

	def insert_yyline(self, sheet_name, yy_list):
		"""
		세로행을 한줄삽입하기
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param yy_list: 세로줄의 사작과 끝 => [3,7]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		if type(yy_list) == type([]) and len(yy_list) == 1:
			x2 = x1 = self.change_num_to_char(yy_list[0])
		elif type(yy_list) == type([]) and len(yy_list) == 2:
			x1 = self.change_num_to_char(yy_list[0])
			x2 = self.change_num_to_char(yy_list[1])
		else:
			x2 = x1 = self.change_num_to_char(yy_list)
		sheet_object.Columns(str(x1) + ':' + str(x2)).Insert()

	def insert_yyline_in_range(self, sheet_name="", yy="입력필요"):
		"""
		가로열을 한줄삽입하기
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param yy: 세로줄의 사작과 끝 => [3,7]
		:return:
		"""
		self.insert_yyline(sheet_name, yy)

	def is_empty_xline(self, sheet_name, no):
		"""
		열전체가 빈 것인지 확인해서 돌려준다
		현재의 기능은 한줄만 가능하도록 하였다
		다음엔 영역이 가능하도록 하여야 겠다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param no:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		result = self.xlapp.WorksheetFunction.CountA(sheet_object.Rows(no).EntireRow)
		return result

	def is_empty_yline(self, sheet_name, no):
		"""
		열전체가 빈 것인지 확인해서 돌려준다
		현재의 기능은 한줄만 가능하도록 하였다
		다음엔 영역이 가능하도록 하여야 겠다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param no:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		result = self.xlapp.WorksheetFunction.CountA(sheet_object.Columns(no).EntireColumn)
		return result

	def make_password(self, isnum="yes", istext_small="yes", istext_big="yes", isspecial="no", len_num=10):
		"""
		엑셀시트의 암호를 풀기위해 암호를 계속 만들어서 확인하는 것
		메뉴에서 제외

		:param isnum:
		:param istext_small:
		:param istext_big:
		:param isspecial:
		:param len_num:
		:return:
		"""
		check_char = []
		if isnum == "yes":
			check_char.extend(list(string.digits))
		if istext_small == "yes":
			check_char.extend(list(string.ascii_lowercase))
		if istext_big == "yes":
			check_char.extend(list(string.ascii_uppercase))
		if isspecial == "yes":
			for one in "!@#$%^*_-":
				check_char.extend(one)

		zz = combinations_with_replacement(check_char, len_num)
		for aa in zz:
			try:
				pswd = "".join(aa)
				# print(pswd)
				self.set_sheet_lock_off("", pswd)
				break
			# print("발견", pswd)
			except:
				pass

	def make_serial_no(self, sheet_name, xyxy, last_len_char=3):
		"""
		바로위의 값과 비교해서, 알아서 연속된 번호를 만들어주는 기능
		맨마지막의 값을 읽어와서 그것에 1을 더한값을 돌려주는 것이다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param last_len_char:
		:return:
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		upper_value = self.read_value_in_cell(sheet_name, [x1, y1])
		new_no = format(int(upper_value[:-1 * last_len_char]) + 1, )

		result = upper_value[last_len_char:] + str(int(upper_value[:-1 * last_len_char]) + 1)
		return result

	def make_vba_module(self, vba_code, macro_name):
		"""
		텍스트로 만든 매크로 코드를 실행하는 코드이다

		:param vba_code:
		:param macro_name:
		:return:
		"""
		new_vba_code = "Sub " + macro_name + "()" + vba_code + "End Sub"
		mod = self.xlbook.VBProject.VBComponents.Add(1)
		mod.CodeModule.AddFromString(new_vba_code)

	def make_xy_list_for_box_style(self, xyxy):
		"""
		좌표를 주면, 맨끝만 나터내는 좌표를 얻는다
		메뉴에서 제외

		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		temp_1 = []
		for x in [xyxy[0], xyxy[2]]:
			temp = []
			for y in range(xyxy[1], xyxy[3] + 1):
				temp.append([x, y])
			temp_1.append(temp)

		temp_2 = []
		for y in [xyxy[1], xyxy[3]]:
			temp = []
			for x in range(xyxy[0], xyxy[2] + 1):
				temp.append([x, y])
			temp_2.append(temp)

		result = [temp_1[0], temp_2[1], temp_1[1], temp_2[0]]
		return result

	def make_y_value(self, input_data):
		"""
		1차원리스트를 2차원으로 만들면, 세로입력을 가로입력으로 바꾸는 것이다
		메뉴에서 제외

		:param input_data: 입력자료
		:return:
		"""
		result = self.change_list1d_to_list2d(input_data)
		return result

	def merge_top_2_ylines_in_range(self, sheet_name="", xyxy=""):  # 셀들을 합하는 것이다
		"""
		선택 영역중 바로 위의것과 아랫것만 병합하는것
		제일위의 2줄만 가로씩 병합하는 것이다
		세로줄 갯수만큰 병합하는것
		위와 아래에 값이 있으면 알람이 뜰것이다

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		if x1 == x2:
			pass
		else:
			for x in range(x1, x2 + 1):
				sheet_object.Range(sheet_object.Cells(x, y1), sheet_object.Cells(x, y1 + 1)).Merge(0)

	def manual(self):
		"""
		간략한 이 모듈에 대한 설명입니다

		:return:
		"""
		result = """
			"""
		return result

	def merge_top_2_xlines_in_range(self, sheet_name="", xyxy=""):  # 셀들을 합하는 것이다
		"""
		선택 영역중 바로 위의것과 아랫것만 병합하는것
		제일위의 2줄만 세로씩 병합하는 것이다
		가로줄 갯수만큰 병합하는것
		위와 아래에 값이 있으면 알람이 뜰것이다

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		if y1 == y2:
			pass
		else:
			for y in range(y1, y2 + 1):
				sheet_object.Range(sheet_object.Cells(x1, y), sheet_object.Cells(x1 + 1, y)).Merge(0)

	def merge_left_2_ylines_in_range(self, sheet_name="", xyxy=""):  # 셀들을 합하는 것이다
		"""
		선택 영역중 바로 위의것과 아랫것만 병합하는것
		왼쪽의 2줄을 병합하는 것이다

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		if x1 == x2:
			pass
		else:
			for x in range(x1, x2 + 1):
				sheet_object.Range(sheet_object.Cells(x, y1), sheet_object.Cells(x, y1 + 1)).Merge(0)

	def move_activecell_by_xy_offset(self, sheet_name, xy):
		"""
		activecell을 offset으로 이동시키는것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xy: [가로번호, 세로번호]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xy)
		xyxy2 = self.read_address_in_activecell()
		sheet_object.Cells(xyxy2[0] + x1, xyxy2[1] + y1).Select()

	def move_activecell_in_range_to_bottom(self, sheet_name="", xyxy=""):
		"""
		선택한 위치에서 제일왼쪽, 제일아래로 이동
		xlDown: - 4121,xlToLeft : - 4159, xlToRight: - 4161, xlUp : - 4162
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Cells(x1, y1)
		my_range.End(-4121).Select()

	def move_activecell_in_range_to_leftend(self, sheet_name="", xyxy=""):
		"""
		입력값 : 입력값없이 사용가능
		선택한 위치에서 끝부분으로 이동하는것
		xlDown : - 4121, xlToLeft : - 4159, xlToRight : - 4161, xlUp : - 4162
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Cells(x1, y1)
		my_range.End(-4159).Select()

	def move_activecell_in_range_to_rightend(self, sheet_name="", xyxy=""):
		"""
		선택한 위치에서 끝부분으로 이동하는것
		xlDown: - 4121,xlToLeft : - 4159, xlToRight: - 4161, xlUp : - 4162
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Cells(x1, y1)
		my_range.End(-4161).Select()

	def move_activecell_in_range_to_top(self, sheet_name="", xyxy=""):
		"""
		선택한 위치에서 끝부분으로 이동하는것
		xlDown: - 4121,xlToLeft : - 4159, xlToRight: - 4161, xlUp : - 4162
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Cells(x1, y1)
		my_range.End(-4162).Select()

	def move_arrange_two_sheet_y_02(self):
		"""
		두개의 시트에서 하나를 기준으로 다른 하나의 시트 내용을 정렬하는것
		첫번째 시트의 제일 윗줄을 기준으로 두번째 시트를 정렬 하는것
		메뉴에서 제외

		:return:
		"""
		input_list = []

		# 기준시트와 옮길시트의 이름을 갖고온다
		input_data = self.read_messagebox_for_input("Please input specific char : ex) sheet_a, sheet_b")
		sheet_names = input_data.split(",")

		# sheet_names=["aaa", "bbb"]

		# 사용한 범위를 갖고온다
		range_1 = self.read_address_for_usedrange(sheet_names[0])
		range_2 = self.read_address_for_usedrange(sheet_names[1])

		no_title2 = range_2[2]

		# 기준 시트의 제목을 읽어와서 저장한다
		title_1 = self.read_range_value(sheet_names[0], [1, range_1[1], 1, range_1[3]])
		title_1_list = []
		for no in range(1, len(title_1[0]) + 1):
			title_1_list.append([no, title_1[0][no - 1]])

		# 하나씩 옮길시트의 값을 읽어와서 비교한후 맞게 정렬한다
		for y1 in range(len(title_1_list)):
			found = 0
			basic_title = title_1_list[y1][1]
			print("기준자료 ==>", basic_title)
			# 기준자료의 제목이 비어있으면 새로이 한칸을 추가한다
			if basic_title == None or basic_title == "":
				self.insert_yline(sheet_names[1], y1 + 1)
				no_title2 = no_title2 + 1
			else:
				# 만약 기준시트의 제목보다 더 넘어가면 그냥 넘긴다
				if y1 > no_title2:
					pass
				else:
					for y2 in range(y1, no_title2 + 1):
						move_title = self.excel.read_cell_value(sheet_names[1], [1, y2 + 1])
						if found == 0 and move_title == basic_title:
							print("발견자료 ==>", move_title)
							found = 1
							if y1 == y2:
								pass
							else:
								self.move_yline(sheet_names[1], sheet_names[1], y2 + 1, y1 + 1)

					if found == 0:
						# 빈칸을 하나 넣는다
						self.insert_yline(sheet_names[1], y1 + 1)

	def move_bottom_in_range(self, sheet_name="", xyxy=""):
		"""
		선택한 위치에서 제일왼쪽, 제일아래로 이동
		xlDown: - 4121,xlToLeft : - 4159, xlToRight: - 4161, xlUp : - 4162
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		sheet_object.Cells(x1, y2).Select()

	def move_cell(self, sheet_name_1, xy_from, sheet_name_2, xy_to):
		"""
		1 개의 셀만 이동시키는 것
		메뉴에서 제외
		2023-09-27 : 다른 시트로도 옮길수있도록 변경

		:param sheet_name_1:
		:param xy_from:
		:param sheet_name_2:
		:param xy_to:
		:return:
		"""
		sheet_object_1 = self.check_sheet_name(sheet_name_1)
		sheet_object_2 = self.check_sheet_name(sheet_name_2)
		x1, y1, x2, y2 = self.check_address_value(xy_from)
		sheet_object_1.Cells(x1, y1).Cut()
		x1, y1, x2, y2 = self.check_address_value(xy_to)
		my_range = sheet_object_2.Cells(x1, y1)
		sheet_object_2.Paste(my_range)

	def move_cell_to_another_sheet(self, sheet_list="입력필요", xy_list="입력필요"):
		"""
		다른시트로 값1개 옮기기
		입력형태 : [시트이름1, 시트이름2], [[2,3]. [4,5]]
		메뉴에서 제외

		:param sheet_list:
		:param xy_list:
		:return:
		"""
		sheet_object_1 = self.check_sheet_name(sheet_list[0])
		x1, y1 = xy_list[0]
		sheet_object_1.Cells(x1, y1).Cut()

		sheet_object_2 = self.check_sheet_name(sheet_list[1])
		x2, y2 = xy_list[1]
		sheet_object_2.Cells(x2, y2).Insert()

	def move_degree_distance(self, degree="입력필요", distance="입력필요"):
		"""
		move_degree_distance( degree="입력필요", distance="입력필요")
		현재 위치 x,y에서 30도로 20만큼 떨어진 거리의 위치를 돌려주는 것
		메뉴에서 제외

		:param degree:
		:param distance:
		:return:
		"""
		degree = degree * 3.141592 / 180
		y = distance * math.cos(degree)
		x = distance * math.sin(degree)
		return [x, y]

	def move_list2d_by_index(self, input_list2d, input_no_list):
		"""
		입력형태 : 2차원리스트, [[옮길것, 옮기고싶은자리].....]
		메뉴에서 제외

		:param input_list2d: list type 2dimension, 2차원의 리스트형
		:param input_no_list:
		:return:
		"""
		ori_no_dic = {}
		for one in range(len(input_list2d[0])):
			ori_no_dic[one] = one
		for before, after in input_no_list:
			new_before = ori_no_dic[before]
			new_after = ori_no_dic[after]

			for no in range(len(input_list2d)):
				if new_before < new_after:
					new_after = after - 1
				value = input_list2d[no][new_before]
				del input_list2d[no][new_before]
				input_list2d[no].insert(int(new_after), value)
		return input_list2d

	def move_list2d_by_index_old(self, input_list2d, input_no_list):
		"""
		입력형태 : 2차원리스트, [[옮길것, 옮기고싶은자리].....]
		메뉴에서 제외

		:param input_list2d: list type 2dimension, 2차원의 리스트형
		:param input_no_list:
		:return:
		"""
		input_no_list.sort()
		input_no_list.reverse()
		for before, after in input_no_list:
			for no in range(len(input_list2d)):
				if before < after:
					after = after - 1
				value = input_list2d[no][before]
				del input_list2d[no][before]
				input_list2d[no].insert(int(after), value)
		return input_list2d

	def move_range(self, sheet_name_old, xyxy_from, sheet_name_new, xyxy_to):
		"""
		모든값을 그대로 이동시키는 것
		메뉴에서 제외

		:param sheet_name_old:
		:param xyxy_from:
		:param sheet_name_new:
		:param xyxy_to:
		:return:
		"""
		sheet_object_old = self.check_sheet_name(sheet_name_old)
		sheet_object_new = self.check_sheet_name(sheet_name_new)
		x1, y1, x2, y2 = self.check_address_value(xyxy_from)
		my_range1 = sheet_object_old.Range(sheet_object_old.Cells(x1, y1), sheet_object_old.Cells(x2, y2))
		my_range1.Cut()
		x1, y1, x2, y2 = self.check_address_value(xyxy_to)
		my_range2 = sheet_object_new.Range(sheet_object_new.Cells(x1, y1), sheet_object_new.Cells(x2, y2))
		sheet_object_new.Paste(my_range2)

	def move_shape(self, sheet_name, shape_obj, top, left):
		"""
		메뉴에서 제외
		shape_obj : 이동시림 도형 이름

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param shape_obj:
		:param top:
		:param left:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		oShape = sheet_object.Shapes(shape_obj)
		oShape.Top = oShape.Top + top
		oShape.Left = oShape.left + left

	def move_to_bottom_in_range(self, sheet_name, xyxy):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.End(- 4121).Select()

	def move_to_leftend_in_range(self, sheet_name, xyxy):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.End(- 4159).Select()

	def move_to_rightend_in_range(self, sheet_name, xyxy):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.End(- 4161).Select()

	def move_to_top_in_range(self, sheet_name, xyxy):
		"""
		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:

		메뉴에서 제외
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.End(- 4162).Select()

	def move_value_in_range_to_left_except_emptycell(self, sheet_name="", xyxy=""):
		"""
		x열을 기준으로 값이 없는것은 왼쪽으로 옮기기
		전체영역의 값을 읽어오고, 하나씩 다시 쓴다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		value_2d = self.read_value_in_range(sheet_name, xyxy)
		self.delete_value_in_range(sheet_name, xyxy)
		for x in range(0, x2 - x1 + 1):
			new_y = 0
			for y in range(0, y2 - y1 + 1):
				value = value_2d[x][y]
				if value == "" or value == None:
					pass
				else:
					sheet_object.Cells(x + x1, new_y + y1).Value = value
					new_y = new_y + 1

	def move_values_between_specific_words_01(self, sheet_name, xyxy):
		"""
		괄호안의 모든 글자를 괄호를 포함하여 삭제하는것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		input = self.read_messagebox_for_input("Please input specific char : ex) a, b")
		input_new = input.split(",")
		# re_basic = "\\"+str(input_new[0]) + "[\^" + str(input_new[0]) +"]*\\" + str(input_new[1])

		input_new[0] = str(input_new[0]).strip()
		input_new[1] = str(input_new[1]).strip()

		special_char = ".^$*+?{}[]\|()"
		# 특수문자는 역슬래시를 붙이도록
		if input_new[0] in special_char: input_new[0] = "\\" + input_new[0]
		if input_new[1] in special_char: input_new[1] = "\\" + input_new[1]

		re_basic = str(input_new[0]) + ".*" + str(input_new[1])

		self.insert_yyline(sheet_name, y1 + 1)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				cell_value = str(self.read_cell_value(sheet_name, [x, y]))
				result_list = re.findall(re_basic, cell_value)
				#     print("새로운값 ==>", new_value)
				if result_list == None or result_list == []:
					pass
				else:
					print("result_list ==>", result_list)
					self.write_cell_value(sheet_name, [x, y + 1], result_list[0])

	def move_without_emptyline_01(self):
		"""
		메뉴에서 제외

		:return:
		"""
		self.excel = pcell.pcell('activeworkbook')

		# 선택한 영역에서 각 세로행의 자료가 입삭제할것들을 입력받은 빈칸이상이 있으면 당겨오는 것이다
		# 이것은 여러곳에서 갖고온 자료들중 삭제한후에 값들을 당겨서 하기에 손이 많이 가는것을 코드로 만든 것이다

		[x1, y1, x2, y2] = self.excel.read_select_address()
		# 0칸일때 빈 공간이 없는것이다
		step_line = int(self.read_messagebox_for_input("0 : 빈칸이 없는것입니다")) + 1

		for y in range(y1, y2 + 1):
			temp_data = []
			flag = 0
			for x in range(x1, x2 + 1):
				temp_value = self.excel.read_cell_value("", [x, y])
				print(x, "번째 ====>", temp_value)
				if temp_value == "" or temp_value == None:
					flag = flag + 1
				else:
					flag = 0
				if flag >= step_line:
					pass
				else:
					temp_data.append([temp_value])
					self.write_cell_value("", [x, y], "")
			print(temp_data)
			self.write_value_in_range_as_speedy("", [1, y], temp_data)

	def move_xline_value_to_multi_lines(self, input_xyxy, repeat_no, start_xy):
		"""
		x라인의 가로 한줄의 자료를 여반복갯수에 따라서 시작점에서부터 아래로 복사하는것
		입력자료 :  1줄의 영역, 반복하는 갯수, 자료가 옮겨갈 시작주소
		메뉴에서 제외

		:param input_xyxy:
		:param repeat_no:
		:param start_xy:
		:return:
		"""
		all_data_set = self.read_value_in_range("", input_xyxy)
		for no in range(len(all_data_set[0])):
			mok, namuji = divmod(no, repeat_no)
			new_x = mok + start_xy[0]
			new_y = namuji + start_xy[1]
			self.write_value_in_cell("", [new_x, new_y], all_data_set[0][no])

	def move_xxline_to_another_sheet(self, sheet_list="입력필요", xx_list="입력필요"):
		"""
		다른 시트로 이동시키기 위해서는 다른 시트를 활성화 시켜야 한다
		메뉴에서 제외

		:param sheet_list:
		:param xx_list:
		:return:
		"""
		sheet_object_1 = self.check_sheet_name(sheet_list[0])
		x1, x2 = self.check_xx_address(xx_list[0])
		sheet_object_1.Rows(str(x1) + ':' + str(x2)).Cut()

		sheet_object_2 = self.check_sheet_name(sheet_list[1])
		self.select_sheet(sheet_list[1])
		x21, x22 = self.check_xx_address(xx_list[1])
		sheet_object_2.Rows(str(x21) + ':' + str(x22)).Insert()

	def move_xy_to_top_end_of_selection(self, sheet_name="", xy=""):
		"""
		영역의 제일 위로 이동
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xy: [가로번호, 세로번호]
		:return:
		"""
		xldown = -4121
		xltoleft = -4159
		xltoright = -4161
		xlup = -4162

		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xy)
		my_range = sheet_object.Cells(x1, y1)
		for num in [xldown, xltoleft, xltoright, xlup]:
			my_range.End(num).Select()
			aa = self.read_address_in_activecell()
			print(aa)

	def move_yline_value_to_multi_lines(self, input_xyxy, repeat_no, start_xy):
		"""
		y라인의 가로 한줄의 자료를 여반복갯수에 따라서 시작점에서부터 아래로 복사하는것
		입력자료 :  1줄의 영역, 반복하는 갯수, 자료가 옮겨갈 시작주소
		메뉴에서 제외

		:param input_xyxy:
		:param repeat_no:
		:param start_xy:
		:return:
		"""
		all_data_set = self.read_value_in_range("", input_xyxy)
		for no in range(len(all_data_set)):
			mok, namuji = divmod(no, repeat_no)
			new_x = mok + start_xy[0]
			new_y = namuji + start_xy[1]
			self.write_value_in_cell("", [new_x, new_y], all_data_set[no][0])

	def move_yyline(self, sheet_name="", yy_list="입력필요"):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param yy_list: 세로줄의 사작과 끝 => [3,7]
		:return:
		"""
		self.move_yyline_in_sheet(sheet_name, yy_list)

	def move_yyline_in_sheet(self, sheet_name="", yy_list="입력필요"):
		"""
		같은 시트안에서 y라인을 이동시키는것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param yy_list: 세로줄의 사작과 끝 => [3,7]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		y1, y2 = self.check_yy_address(yy_list[0])
		sheet_object.Columns(y1 + ':' + y2).Cut()

		y1_new, y2_new = self.check_yy_address(yy_list[1])
		sheet_object.Columns(y1_new + ':' + y2_new).Insert()

	def move_yyline_to_another_sheet(self, sheet_name_list, yy_list):
		"""
		세로의 값을 이동시킵니다
		메뉴에서 제외

		:param sheet_name_list:
		:param yy_list: 세로줄의 사작과 끝 => [3,7]
		:return:
		"""
		sheet_object_1 = self.check_sheet_name(sheet_name_list[0])
		y1, y2 = self.check_yy_address(yy_list[0])
		sheet_object_1.Columns(y1 + ':' + y2).Cut()

		sheet_object_2 = self.check_sheet_name(sheet_name_list[1])
		y1_new, y2_new = self.check_yy_address(yy_list[1])
		sheet_object_2.Columns(y1_new + ':' + y2_new).Insert()

	def new_sheet(self, input_name=""):
		"""
		시트하나 추가하기
		위치는 자동으로 제일 뒤에 추가되는것이며, 시트이름이 없어 자동으로 만들어지는 이름입니다
		메뉴에서 제외

		:param input_name:
		:return:
		"""
		self.xlbook.Worksheets.Add()
		Sheet = self.xlbook.ActiveSheet
		try:
			if input_name != "":
				Sheet.Name = input_name
		except:
			pass

	def new_sheet_name_with_checking(self, sheet_name=""):
		"""
		시트하나 추가
		단, 이름을 확인해서 같은것이 있으면, 그냥 넘어간다

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		if sheet_name == "":
			pass
		else:
			all_sheet_names = self.read_sheet_name_all()
			if sheet_name in all_sheet_names:
				pass
			else:
				self.xlbook.Worksheets.Add()
				old_name = self.xlbook.ActiveSheet
				self.xlbook.Worksheets(old_name).Name = sheet_name

	def new_workbook(self, filename=""):
		"""
		1. 새로운 엑셀화일을 엽니다
		2. path가 없다면, Document폴더를 지정하도록 합니다
		3. 같은 화일이름이 있으면 message로 알려줍니다
		메뉴에서 제외

		:param filename:
		:return:
		"""
		if filename == "":
			self.xlbook = self.xlapp.WorkBooks.Add()
		else:
			# 경로와 화일이름을 분리
			path, file_name_only = self.split_path_n_file_name(filename)

			if str(path).strip() == "":
				# 경로가 없다면 기본 저장 경로를 설정
				path = "C:/Users/Administrator/Documents"

			# 경로가 있으면, 혹시 같은 화일이름이 기존에 있는지 확인하는 것
			old_file_is = self.check_file_in_folder(path, file_name_only)
			if old_file_is:
				self.write_messagebox_value("화일이름을 다시 확인 바랍니다")
			else:
				self.xlapp.WindowState = -4137
				try:
					self.xlbook = self.xlapp.Workbooks.Open(filename)
				except:
					self.xlbook = self.xlapp.WorkBooks.Add()
					self.save(filename)

	def open_file(self, filename=""):
		"""
		메뉴에서 제외

		:param filename:
		:return:
		"""
		self.path_full = self.check_filepath(filename)
		self.file_name_only = self.path_full.split("/")[-1]
		if filename.lower() == 'new' or filename == "":
			# 빈것으로 된 경우는 새로운 workbook < 연다는 뜻으로 해석
			try:
				self.xlapp.Windowstate = -4137
				self.xlbook = self.xlapp.WorkBooks.Add()
			except:
				win32gui.MessageBox(0, "There is no Activeworkbook", "www.xython.co.kr", 0)
		else:
			#	열린 화일중에 같은것이 있는지 확인하는 것
			file_name_list = self.read_opened_workbook_filename_all()
			if self.file_name_only in file_name_list:
				pass
			else:
				try:
					self.xlbook = self.xlapp.Workbooks.Open(self.path_full)
				except:
					win32gui.MessageBox(0, "화일이름이나 경로를 다시한번 확인해 보시기 바랍니다", "www.xython.co.kr", 0)

	def open_workbook(self, input_file_name):
		"""
		열려진 워드 화일중 이름으로 선택하는것
		메뉴에서 제외

		:param input_file_name:
		:return:
		"""
		self.xlapp.Visible = True
		win32gui.SetForegroundWindow(self.xlapp.hwnd)
		self.xlapp.WorkBooks(input_file_name).Activate()
		self.xlapp.WindowState = win32com.client.constants.xlMaximized

	def paint_cell_by_excel_colorno(self, sheet_name, xy, excel_color_no="입력필요"):
		"""
		paint_color(sheet_name, xyxy, input_data="입력필요")
		선택 셀에 색깔을 넣는다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xy: [가로번호, 세로번호]
		:param excel_color_no:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		self.check_address_value(xy)

		rgbvalue = self.var_common["dic_colorindex_rgblist"][excel_color_no]

		rgb_to_int = (int(rgbvalue[2])) * (256 ** 2) + (int(rgbvalue[1])) * 256 + int(rgbvalue[0])
		sheet_object.Cells(xy[0], xy[1]).Interior.Color = int(rgb_to_int)

	def paint_cell_by_rgb(self, sheet_name, xy, input_color="입력필요"):
		"""
		paint_color(sheet_name, xyxy, input_data="입력필요")
		선택 셀에 색깔을 넣는다

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xy: [가로번호, 세로번호]
		:param input_color: 색이름
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		self.check_address_value(xy)
		rgb_value = self.check_input_color_rgb(input_color)

		rgb_to_int = self.color.change_rgb_to_rgbint(rgb_value)
		sheet_object.Cells(xy[0], xy[1]).Interior.Color = int(rgb_to_int)

	def paint_cell_by_scolor(self, sheet_name, xy, input_color="입력필요"):
		"""
		paint_color(sheet_name, xyxy, input_data="입력필요")
		선택 셀에 색깔을 넣는다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xy: [가로번호, 세로번호]
		:param input_color: 색이름
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		self.check_address_value(xy)

		rgbvalue = self.color.change_scolor_to_rgb(input_color)
		rgb_to_int = (int(rgbvalue[2])) * (256 ** 2) + (int(rgbvalue[1])) * 256 + int(rgbvalue[0])
		sheet_object.Cells(xy[0], xy[1]).Interior.Color = int(rgb_to_int)

	def paint_cell_in_range_by_specific_text(self, sheet_name="", xyxy="", input_text="입력필요", input_color="입력필요"):
		"""
		영역안에 입력받은 글자와 같은것이 있으면 색칠하는것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_text: 입력되는 text형식의 자료
		:param input_color: 색이름
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_object.Cells(x, y).Value
				if input_text in value:
					self.paint_cell_by_scolor(sheet_name, [x, y], input_color)

	def paint_color_in_cell(self, sheet_name, xy, input_color="입력필요"):
		"""
		메뉴에서 제외
		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xy: [가로번호, 세로번호]
		:param input_color: 색이름
		:return:
		"""
		excel_no = self.paint_cell_by_excel_colorno(sheet_name, xy, input_color)

	# self.paint_cell_by_scolor(sheet_name, xy, excel_no)
	def paint_color_in_cell(self, sheet_name, xyxy, input_color):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_color: 색이름
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		input_data = self.color.check_input_color(input_color)
		rgb_to_int = (int(input_data[2])) * (256 ** 2) + (int(input_data[1])) * 256 + int(input_data[0])
		my_range.Interior.Color = rgb_to_int

	def paint_color_in_range(self, sheet_name, xyxy, input_color="입력필요"):
		"""
		paint_color(sheet_name, xyxy, input_data="입력필요")
		선택 영역에 색깔을 넣는다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_color: 색이름
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		rgbvalue = self.color.change_scolor_to_rgb(input_color)
		rgb_to_int = (int(rgbvalue[2])) * (256 ** 2) + (int(rgbvalue[1])) * 256 + int(rgbvalue[0])
		my_range.Interior.Color = rgb_to_int

	def paint_color_in_range_bywords(self, sheet_name="", xyxy=""):
		"""
		입력값을 받는데
		영역안에 입력받은 글자가 있으면 색칠하는것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		bbb = self.read_messagebox_for_input("Please input text : in, to, his, with")
		basic_list = []
		for one_data in bbb.split(","):
			basic_list.append(one_data.strip())
		total_no = len(basic_list)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				cell_value = sheet_object.Cells(x, y).Value
				temp_int = 0
				for one_word in basic_list:
					if re.match('(.*)' + one_word + '(.*)', str(cell_value)):
						temp_int = temp_int + 1
				if temp_int == total_no:
					self.paint_color_in_range(sheet_name, [x, y], "yel")

	def paint_font_color(self, sheet_name, xyxy, input_color):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_color: 색이름
		:return:
		"""
		self.paint_font_in_range_by_scolor(sheet_name, xyxy, input_color)

	def paint_font_color_in_cell(self, sheet_name="", xy="", font_color=""):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xy: [가로번호, 세로번호]
		:param font_color:
		:return:
		"""
		self.set_font_color_in_cell(sheet_name, xy, font_color)

	def paint_font_color_in_range(self, sheet_name="", xyxy="", font_color=""):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param font_color:
		:return:
		"""
		self.set_font_color_in_range(sheet_name, xyxy, font_color)

	def paint_font_in_cell_by_rgb(self, sheet_name="", xyxy="", rgb=""):
		"""
		셀안의 폰트 색깔을 넣는 것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param rgb:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.Font.Color = int(rgb[0]) + int(rgb[1]) * 256 + int(rgb[2]) * 65536

	def paint_font_in_range_by_scolor(self, sheet_name="", xyxy="", font_color=""):
		"""
		영역안의 폰트 색깔을 넣는 것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param font_color:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		input_data = self.color.change_scolor_to_rgb(font_color)
		rgb_to_int = (int(input_data[2])) * (256 ** 2) + (int(input_data[1])) * 256 + int(input_data[0])
		my_range.Font.Color = rgb_to_int

	def paint_maxvalue_in_range_in_each_xline(self, sheet_name="", xyxy=""):
		"""
		각 x라인별로 최대값에 색칠하는 것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		all_data = self.read_value_in_range(sheet_name, [x1, y1, x2, y2])
		if not (x1 == x2 and y1 == y2):
			for line_no in range(len(all_data)):
				line_data = all_data[line_no]
				filteredList = list(filter(lambda x: type(x) == type(1) or type(x) == type(1.0), line_data))
				if filteredList == []:
					pass
				else:
					max_value = max(filteredList)
					x_location = x1 + line_no
					for no in range(len(line_data)):
						y_location = y1 + no
						if (line_data[no]) == max_value:
							self.paint_cell_by_scolor(sheet_name, [x_location, y_location], "yel")
		else:
			print("Please re-check selection area")

	def paint_minvalue_in_range_in_each_xline(self, sheet_name="", xyxy=""):
		"""
		각 x라인별로 최소값에 색칠하는 것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		all_data = self.read_value_in_range(sheet_name, [x1, y1, x2, y2])
		if not (x1 == x2 and y1 == y2):
			for line_no in range(len(all_data)):
				line_data = all_data[line_no]
				filteredList = list(filter(lambda x: type(x) == type(1) or type(x) == type(1.0), line_data))
				if filteredList == []:
					pass
				else:
					max_value = min(filteredList)
					x_location = x1 + line_no
					for no in range(len(line_data)):
						y_location = y1 + no
						if (line_data[no]) == max_value:
							self.paint_cell_by_scolor(sheet_name, [x_location, y_location], "red")
		else:
			print("Please re-check selection area")

	def paint_range_by_rgb(self, sheet_name="", xyxy="", input_data=""):
		"""
		영역에 색깔을 입힌다
		엑셀에서의 색깔의 번호는 아래의 공식처럼 만들어 진다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_data: 입력자료
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		rgb_value = self.check_input_color_rgb(input_data)
		rgb_to_int = (int(rgb_value[2])) * (256 ** 2) + (int(rgb_value[1])) * 256 + int(rgb_value[0])
		my_range.Interior.Color = rgb_to_int

	def paint_range_by_scolor(self, sheet_name, xyxy, input_color="입력필요"):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_color: 색이름
		:return:
		"""
		self.paint_color_in_range(sheet_name, xyxy, input_color)

	def paint_range_for_empty_cell(self, sheet_name="", xyxy=""):
		"""
		빈셀일때 색칠하는 것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		temp_result = 0
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				cell_value = sheet_object.Cells(x, y).Value
				if cell_value == None:
					self.paint_cell_by_scolor(sheet_name, [x, y], "yel")
					temp_result = temp_result + 1
		return temp_result

	def paint_range_for_samevalue_by_excel_colorno(self, sheet_name="", xyxy="", excelcolorno=4):
		"""
		영역에서 같은 값을 색칠하는 것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param excelcolorno:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		set_a = set([])
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = str(sheet_object.Cells(x, y).Value)
				if value == "" or value == None:
					pass
				else:
					len_old = len(set_a)
					set_a.add(value)
					len_new = len(set_a)
					if len_old == len_new:
						self.paint_cell_by_excel_colorno(sheet_name, [x, y], excelcolorno)

	def paint_rgb_in_cell(self, sheet_name, xyxy, input_rgb):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_rgb: rgb형식의 입력값
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		# RGB값을 색칠하는 방법
		rgb_to_int = (int(input_rgb[2])) * (256 ** 2) + (int(input_rgb[1])) * 256 + int(input_rgb[0])
		my_range.Interior.Color = rgb_to_int

	def paint_samevalue_in_range_by_scolor(self, sheet_name="", xyxy="", input_color="gray"):
		"""
		선택한 영역에서 2번이상 반복된것만 색칠하기

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_color: 색이름
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		set_a = set([])
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = str(sheet_object.Cells(x, y).Value)
				if value == "" or value == None:
					pass
				else:
					len_old = len(set_a)
					set_a.add(value)
					len_new = len(set_a)
					if len_old == len_new:
						self.paint_cell_by_scolor(sheet_name, [x, y], input_color)

	def paint_scolor_in_cell(self, sheet_name, xyxy, input_color):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_color: 색이름
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		rgbvalue = self.color.change_scolor_to_rgb(input_color)
		rgb_to_int = (int(rgbvalue[2])) * (256 ** 2) + (int(rgbvalue[1])) * 256 + int(rgbvalue[0])
		my_range.Interior.Color = rgb_to_int

	def paint_sheet_tab_by_scolor(self, sheet_name, input_color="입력필요"):
		"""
		시트탭의 색을 넣는것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param input_color: 색이름
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		rgbvalue = self.color.change_scolor_to_rgb(input_color)
		rgb_to_int = (int(rgbvalue[2])) * (256 ** 2) + (int(rgbvalue[1])) * 256 + int(rgbvalue[0])
		sheet_object.Tab.Color = rgb_to_int

	def paint_spacecell(self, sheet_name="", xyxy="", input_color="red"):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_color: 색이름
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				cell_value = sheet_object.Cells(y, x).Value
				com = re.compile("^\s+")
				if cell_value != None:
					if com.search(cell_value):
						input_data = self.color.check_input_color(input_color)
						rgb_to_int = (int(input_data[2])) * (256 ** 2) + (int(input_data[1])) * 256 + int(
							input_data[0])
						sheet_object.Cells(y, x).Interior.Color = rgb_to_int

	def paint_spacecell_in_range_by_scolor(self, sheet_name="", xyxy="", input_color="입력필요"):
		"""
		빈셀처럼 보이는데 space문자가 들어가 있는것 찾기
		선택한 영역의 셀을 하나씩 읽어와서 re모듈을 이용해서 공백만 있는지 확인한다

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_color: 색이름
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				cell_value = sheet_object.Cells(x, y).Value
				com = re.compile("^\s+")
				if cell_value != None:
					if com.search(cell_value):
						self.paint_cell_by_scolor(sheet_name, [x, y], input_color)

	def paint_text_in_range_by_scolor(self, sheet_name="", xyxy="", input_color="입력필요"):
		"""
		영역에 글자색을 넣는다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_color: 색이름
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		rgbvalue = self.color.change_scolor_to_rgb(input_color)
		rgb_to_int = (int(rgbvalue[2])) * (256 ** 2) + (int(rgbvalue[1])) * 256 + int(rgbvalue[0])
		my_range.Font.Color = rgb_to_int

	def paint_textcolor(self, sheet_name, xyxy, input_color):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_color: 색이름
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		rgbvalue = self.color.change_scolor_to_rgb(input_color)
		rgb_to_int = (int(rgbvalue[2])) * (256 ** 2) + (int(rgbvalue[1])) * 256 + int(rgbvalue[0])

		my_range.Font.Color = rgb_to_int

	def paste_range(self, sheet_name="", xyxy=""):
		"""
		영역에 붙여넣기 하는것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		sheet_object.Cells(x1, y1).Select()
		sheet_object.Paste()

	def print_as_pdf(self, sheet_name, area, file_name):
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.ExportAsFixedFormat(0, file_name)

	def print_page(self, sheet_name, **var_dic):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param var_dic:
		:return:
		"""
		self.set_print_page(sheet_name, **var_dic)

	def print_preview(self, sheet_name=""):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.PrintPreview()

	def quit_excel(self):
		"""
		엑셀 프로그램을 끄는것

		:return:
		"""
		self.xlapp.Quit()

	def read_activesheet_name(self):
		"""
		메뉴에서 제외

		:return:
		"""
		sheet_name = self.xlapp.ActiveSheet.Name
		return sheet_name

	def read_activeworkbook_filename(self):
		"""
		현재 활성화된 엑셀화일의 이름을 갖고읍니다
		메뉴에서 제외

		:return:
		"""
		result = self.xlapp.ActiveWorkbook.Name
		return result

	def read_address_for_rangename(self, sheet_name="", range_name="입력필요"):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param range_name: 영역이름
		:return:
		"""
		result = self.read_address_rangename(sheet_name, range_name)
		return result

	def read_address_for_selection(self):
		"""
		:return:

		현재선택된 영역의 주소값을 돌려준다
		메뉴에서 제외
		"""
		result = ""
		temp_address = self.xlapp.Selection.Address
		temp_list = temp_address.split(",")
		if len(temp_list) == 1:
			result = self.check_address_value(temp_address)
		if len(temp_list) > 1:
			result = []
			for one_address in temp_list:
				result.append(self.check_address_value(one_address))
		return result

	def read_address_for_usedrange(self, sheet_name=""):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		result = self.read_address_usedrange(sheet_name)
		return result

	def read_address_in_activecell(self):
		"""
		현재 활성화된 셀의 주소를 돌려준다
		메뉴에서 제외

		:return:
		"""
		result = self.check_address_value(self.xlapp.ActiveCell.Address)
		return result

	def read_address_in_currentregion(self, sheet_name="", xy=""):
		"""
		이것은 현재의 셀에서 공백과 공백열로 둘러싸인 활성셀영역을 돌려준다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xy: [가로번호, 세로번호]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		my_range = sheet_object.Cells(xy[0], xy[1])
		# self.select_cell(sheet_name, xy)
		result = self.check_address_value(my_range.CurrentRegion.Address)
		return result

	def read_address_in_selection(self):
		"""
		예전자료를 위해서 남겨 놓음
		메뉴에서 제외

		:return:
		"""
		result = self.read_address_for_selection()
		return result

	def read_address_rangename(self, sheet_name="", range_name="입력필요"):
		"""
		rangename의 주소를 돌려주는것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param range_name: 영역이름
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		temp = sheet_object.Range(range_name).Address
		result = self.check_address_value(temp)
		return result

	def read_address_usedrange(self, sheet_name=""):
		"""
		사용자영역을 돌려주는것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		result = self.check_address_value(sheet_object.UsedRange.address)
		return result

	def read_all_property_in_cell(self, sheet_name="", xy=[7, 7]):
		"""
		셀의 모든 속성을 돌려주는것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xy: [가로번호, 세로번호]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		one_cell = sheet_object.Cells(xy[0], xy[1])
		result = {}
		result["y"] = xy[0]
		result["x"] = xy[1]
		result["value"] = one_cell.Value
		result["value2"] = one_cell.Value2
		result["formular"] = one_cell.Formula
		result["formularr1c1"] = one_cell.FormulaR1C1
		result["text"] = one_cell.Text
		result["font_background"] = one_cell.Font.Background
		result["font_bold"] = one_cell.Font.Bold
		result["font_color"] = one_cell.Font.Color
		result["font_colorindex"] = one_cell.Font.ColorIndex
		result["font_creator"] = one_cell.Font.Creator
		result["font_style"] = one_cell.Font.FontStyle
		result["font_italic"] = one_cell.Font.Italic
		result["font_name"] = one_cell.Font.Name
		result["font_size"] = one_cell.Font.Size
		result["font_strikethrough"] = one_cell.Font.Strikethrough
		result["font_subscript"] = one_cell.Font.Subscript
		result["font_superscript"] = one_cell.Font.Superscript
		result["font_themecolor"] = one_cell.Font.ThemeColor
		result["font_themefont"] = one_cell.Font.ThemeFont
		result["font_tintandshade"] = one_cell.Font.TintAndShade
		result["font_underline"] = one_cell.Font.Underline
		try:
			result["memo"] = one_cell.Comment.Text()
		except:
			result["memo"] = ""
		result["background_color"] = one_cell.Interior.Color
		result["background_colorindex"] = one_cell.Interior.ColorIndex
		result["numberformat"] = one_cell.NumberFormat
		# linestyle이 없으면 라인이 없는것으로 생각하고 나머지를 확인하지 않으면서 시간을 줄이는 것이다
		result["line_top_style"] = one_cell.Borders(7).LineStyle
		result["line_top_color"] = one_cell.Borders(7).Color
		result["line_top_colorindex"] = one_cell.Borders(7).ColorIndex
		result["line_top_thick"] = one_cell.Borders(7).Weight
		result["line_top_tintandshade"] = one_cell.Borders(7).TintAndShade
		result["line_bottom_style"] = one_cell.Borders(8).LineStyle
		result["line_bottom_color"] = one_cell.Borders(8).Color
		result["line_bottom_colorindex"] = one_cell.Borders(8).ColorIndex
		result["line_bottom_thick"] = one_cell.Borders(8).Weight
		result["line_bottom_tintandshade"] = one_cell.Borders(8).TintAndShade
		result["line_left_style"] = one_cell.Borders(9).LineStyle
		result["line_left_color"] = one_cell.Borders(9).Color
		result["line_left_colorindex"] = one_cell.Borders(9).ColorIndex
		result["line_left_thick"] = one_cell.Borders(9).Weight
		result["line_left_tintandshade"] = one_cell.Borders(9).TintAndShade
		result["line_right_style"] = one_cell.Borders(10).LineStyle
		result["line_right_color"] = one_cell.Borders(10).Color
		result["line_right_colorindex"] = one_cell.Borders(10).ColorIndex
		result["line_right_thick"] = one_cell.Borders(10).Weight
		result["line_right_tintandshade"] = one_cell.Borders(10).TintAndShade
		result["line_x1_style"] = one_cell.Borders(11).LineStyle
		result["line_x1_color"] = one_cell.Borders(11).Color
		result["line_x1_colorindex"] = one_cell.Borders(11).ColorIndex
		result["line_x1_thick"] = one_cell.Borders(11).Weight
		result["line_x1_tintandshade"] = one_cell.Borders(11).TintAndShade
		result["line_x2_style"] = one_cell.Borders(12).LineStyle
		result["line_x2_color"] = one_cell.Borders(12).Color
		result["line_x2_colorindex"] = one_cell.Borders(12).ColorIndex
		result["line_x2_thick"] = one_cell.Borders(12).Weight
		result["line_x2_tintandshade"] = one_cell.Borders(12).TintAndShade
		return result

	def read_all_property_in_cell_except_none(self, sheet_name="", xy=[7, 7]):
		"""
		셀의 모든 속성을 돌려주는것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xy: [가로번호, 세로번호]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		one_cell = sheet_object.Cells(xy[0], xy[1])
		result = {}
		result["y"] = xy[0]
		result["x"] = xy[1]
		result["value"] = one_cell.Value
		result["value2"] = one_cell.Value2
		result["formular"] = one_cell.Formula
		result["formularr1c1"] = one_cell.FormulaR1C1
		result["text"] = one_cell.Text
		if result["value"] != "" and result["value"] != None:
			# 값이 없으면 font에 대한 것을 읽지 않는다
			result["font_background"] = one_cell.Font.Background
			result["font_bold"] = one_cell.Font.Bold
			result["font_color"] = one_cell.Font.Color
			result["font_colorindex"] = one_cell.Font.ColorIndex
			result["font_creator"] = one_cell.Font.Creator
			result["font_style"] = one_cell.Font.FontStyle
			result["font_italic"] = one_cell.Font.Italic
			result["font_name"] = one_cell.Font.Name
			result["font_size"] = one_cell.Font.Size
			result["font_strikethrough"] = one_cell.Font.Strikethrough
			result["font_subscript"] = one_cell.Font.Subscript
			result["font_superscript"] = one_cell.Font.Superscript
			result["font_themecolor"] = one_cell.Font.ThemeColor
			result["font_themefont"] = one_cell.Font.ThemeFont
			result["font_tintandshade"] = one_cell.Font.TintAndShade
			result["font_underline"] = one_cell.Font.Underline
		try:
			result["memo"] = one_cell.Comment.Text()
		except:
			result["memo"] = ""
		result["background_color"] = one_cell.Interior.Color
		result["background_colorindex"] = one_cell.Interior.ColorIndex
		result["numberformat"] = one_cell.NumberFormat
		if one_cell.Borders.LineStyle != -4142:
			if one_cell.Borders(7).LineStyle != -4142:
				# linestyle이 없으면 라인이 없는것으로 생각하고 나머지를 확인하지 않으면서 시간을 줄이는 것이다
				result["line_top_style"] = one_cell.Borders(7).LineStyle
				result["line_top_color"] = one_cell.Borders(7).Color
				result["line_top_colorindex"] = one_cell.Borders(7).ColorIndex
				result["line_top_thick"] = one_cell.Borders(7).Weight
				result["line_top_tintandshade"] = one_cell.Borders(7).TintAndShade
			if one_cell.Borders(8).LineStyle != -4142:
				result["line_bottom_style"] = one_cell.Borders(8).LineStyle
				result["line_bottom_color"] = one_cell.Borders(8).Color
				result["line_bottom_colorindex"] = one_cell.Borders(8).ColorIndex
				result["line_bottom_thick"] = one_cell.Borders(8).Weight
				result["line_bottom_tintandshade"] = one_cell.Borders(8).TintAndShade
			if one_cell.Borders(9).LineStyle != -4142:
				result["line_left_style"] = one_cell.Borders(9).LineStyle
				result["line_left_color"] = one_cell.Borders(9).Color
				result["line_left_colorindex"] = one_cell.Borders(9).ColorIndex
				result["line_left_thick"] = one_cell.Borders(9).Weight
				result["line_left_tintandshade"] = one_cell.Borders(9).TintAndShade
			if one_cell.Borders(10).LineStyle != -4142:
				result["line_right_style"] = one_cell.Borders(10).LineStyle
				result["line_right_color"] = one_cell.Borders(10).Color
				result["line_right_colorindex"] = one_cell.Borders(10).ColorIndex
				result["line_right_thick"] = one_cell.Borders(10).Weight
				result["line_right_tintandshade"] = one_cell.Borders(10).TintAndShade
			if one_cell.Borders(11).LineStyle != -4142:
				result["line_x1_style"] = one_cell.Borders(11).LineStyle
				result["line_x1_color"] = one_cell.Borders(11).Color
				result["line_x1_colorindex"] = one_cell.Borders(11).ColorIndex
				result["line_x1_thick"] = one_cell.Borders(11).Weight
				result["line_x1_tintandshade"] = one_cell.Borders(11).TintAndShade
			if one_cell.Borders(12).LineStyle != -4142:
				result["line_x2_style"] = one_cell.Borders(12).LineStyle
				result["line_x2_color"] = one_cell.Borders(12).Color
				result["line_x2_colorindex"] = one_cell.Borders(12).ColorIndex
				result["line_x2_thick"] = one_cell.Borders(12).Weight
				result["line_x2_tintandshade"] = one_cell.Borders(12).TintAndShade

		for one in list(result.keys()):
			if result[one] == None:
				del result[one]

		return result

	def read_all_shape_names(self, sheet_name=""):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		drawings_nos = sheet_object.Shapes.count
		result = []
		if drawings_nos > 0:
			for num in range(sheet_object.Shapes.count, 0, -1):
				# Range를 앞에서부터하니 삭제하자마자 번호가 다시 매겨져서, 뒤에서부터 삭제하니 잘된다
				result.append(sheet_object.Shapes(num).Name)
		return result

	def read_cell(self, sheet_name="", xyxy=""):
		"""
		많이 사용하는 곳이라 짧게 만듦

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		self.read_value_in_cell(sheet_name, xyxy)

	def read_cell_value(self, sheet_name="", xyxy=""):
		"""
		메뉴에서 제외
		보관용 : 예전에 사용했던 코드

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		result = self.read_value_in_cell(sheet_name, xyxy)
		return result

	def read_color_in_cell(self, sheet_name="", xyxy=""):
		"""
		셀의 색을 돌려주는것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		# rgb값으로 출력
		result = my_range.Interior.Color
		return result

	def read_color_in_cell_by_excel_56_color_no(self, sheet_name="", xyxy=""):
		"""
		셀의 색을 돌려주는것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		# rgb값으로 출력
		result = my_range.Interior.ColorIndex
		return result

	def read_coord_in_cell(self, sheet_name, xyxy):
		"""
		셀의 픽셀 좌표를 갖고온다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		rng_x_coord = my_range.Left
		rng_y_coord = my_range.Top
		rng_width = my_range.Width
		rng_height = my_range.Height
		return [rng_x_coord, rng_y_coord, rng_width, rng_height]

	def read_excel_color_no_as_rgb(self, color_no):
		"""
		:param color_no:
		:return:
		"""
		result = self.var_common["dic_colorindex_rgblist"][color_no]
		return result

	def read_filename_for_activeworkbook(self):
		"""
		메뉴에서 제외

		:return:
		"""
		result = self.read_activeworkbook_filename()
		return result

	def read_folder_filename_all(self, directory):
		"""
		폴더 안의 화일을 읽어오는것
		메뉴에서 제외

		:param directory:
		:return:
		"""
		result = []
		filenames = os.listdir(directory)
		for filename in filenames:
			full_filename = os.path.join(directory, filename)
			result.append(filename)
		return result

	def read_font_color_in_cell(self, sheet_name="", xyxy=""):
		"""
		셀의 폰트 색을 돌려주는것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Cells(x1, y1)
		result = my_range.Font.Color
		return result

	def read_fullname_for_workbook(self):
		"""
		메뉴에서 제외

		:return:
		"""
		return self.xlapp.FullName

	def read_general_inform_for_excel(self):
		"""
		몇가지 엑셀에서 자주사용하는 것들정의
		엑셀의 사용자, 현재의 경로, 화일이름, 현재시트의 이름
		메뉴에서 제외

		:return:
		"""
		result = []
		result.append(self.xlapp.ActiveWorkbook.Name)
		result.append(self.xlapp.Username)
		result.append(self.xlapp.ActiveWorkbook.ActiveSheet.Name)
		return result

	def read_general_value(self):
		"""
		몇가지 엑셀에서 자주사용하는 것들정의
		엑셀의 사용자, 현재의 경로, 화일이름, 현재시트의 이름
		메뉴에서 제외

		:return:
		"""
		result = []
		result.append(self.xlapp.ActiveWorkbook.Name)
		result.append(self.xlapp.Username)
		result.append(self.xlapp.ActiveWorkbook.ActiveSheet.Name)
		return result

	def read_inputbox_value(self, title="Please Input Value"):
		"""
		inputbox를 사용하고 싶을때
		메뉴에서 제외

		:param title:
		:return:
		"""
		result = self.xlapp.Application.InputBox(title)
		return result

	def read_memo_in_cell(self, sheet_name="", xyxy=""):
		"""
		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:

		셀의 메모를 돌려주는것
		메뉴에서 제외
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		result = my_range.Comment.Text()
		return result

	def read_messagebox_for_input(self, text_01="xython"):
		"""
		입력창을 만들어서 입력값을 받는것
		메뉴에서 제외

		:param text_01:
		:return:
		"""
		result = self.xlapp.InputBox(text_01)
		return result

	def read_name_for_workbook(self):
		"""
		워크북의 이름을 읽어온다
		메뉴에서 제외

		:return:
		"""
		return self.xlbook.Name

	def read_opened_workbook_filename_all(self):
		"""
		모든 열려있는 엑셀화일의 이름을 갖고옵니다
		메뉴에서 제외

		:return:
		"""
		result = []
		for one in self.xlapp.Workbooks:
			result.append(one.Name)
		return result

	def read_path_for_workbook(self):
		"""
		메뉴에서 제외

		:return:
		"""
		return self.xlapp.Path

	def read_pixel_size_in_cell(self, sheet_name, xyxy):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		rng_x_coord = my_range.Left
		rng_y_coord = my_range.Top
		rng_width = my_range.Width
		rng_height = my_range.Height
		return [rng_x_coord, rng_y_coord, rng_width, rng_height]

	def read_range(self, sheet_name="", xyxy=""):
		"""
		많이 사용하는 곳이라 짧게 만듦

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		self.read_value_in_range(sheet_name, xyxy)

	def read_range_select(self):
		"""
		예전자료를 위해서 남겨 놓음
		메뉴에서 제외

		:return:
		"""
		result = self.read_address_for_selection()
		return result

	def read_range_value(self, sheet_name="", xyxy=""):
		"""
		예전자료를 위해서 남겨 놓음
		메뉴에서 제외

		:param sheet_name:
		:param xyxy:
		:return:
		"""
		result = self.read_value_in_range(sheet_name, xyxy)
		return result

	def read_rangename_all(self):
		"""
		모든 rangename을 돌려주는것
		메뉴에서 제외

		:return:
		"""
		names_count = self.xlbook.Names.Count
		result = []
		if names_count > 0:
			for aaa in range(1, names_count + 1):
				name_name = self.xlbook.Names(aaa).Name
				name_range = self.xlbook.Names(aaa)
				result.append([aaa, str(name_name), str(name_range)])
		return result

	def read_selection_address(self):
		"""
		예전자료를 위해서 남겨 놓음
		메뉴에서 제외

		:return:
		"""
		result = self.read_address_for_selection()
		return result

	def read_shape_name_by_shape_no(self, sheet_name, shape_no=""):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param shape_no:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		result = sheet_object.Shapes(shape_no).Name
		return result

	def read_shape_name_in_sheet_by_no(self, sheet_name="", shape_no="입력필요"):
		"""
		번호로 객체의 이름을 갖고오는것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param shape_no:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		result = sheet_object.Shapes(shape_no).Name
		return result

	def read_sheet_name_all(self):
		"""
		워크시트의 모든 이름을 읽어온다
		메뉴에서 제외

		:return:
		"""
		result = []
		for a in range(1, self.xlbook.Worksheets.Count + 1):
			result.append(self.xlbook.Worksheets(a).Name)
		return result

	def read_username(self):
		"""
		사용자 이름을 읽어온다
		메뉴에서 제외

		:return:
		"""
		return self.xlapp.Username

	def read_value2_in_cell(self, sheet_name, xyxy):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		result = self.read_value_in_cell_as_value2(sheet_name, xyxy)
		return result

	def read_value2_in_range(self, sheet_name, xyxy):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		result = self.read_value_in_range_as_value2(sheet_name, xyxy)
		return result

	def read_value_in_activecell(self):
		"""
		현재셀의 값을 돌려주는것
		메뉴에서 제외

		:return:
		"""
		result = [self.xlapp.ActiveCell.Row, self.xlapp.ActiveCell.Column, self.xlapp.ActiveCell.Value]
		return result

	def read_value_in_cell(self, sheet_name="", xyxy=""):
		"""
		값을 일정한 영역에서 갖고온다
		만약 영역을 두개만 주면 처음과 끝의 영역을 받은것으로 간주해서 알아서 처리하도록 변경하였다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		result = sheet_object.Cells(x1, y1).Value

		if type(result) == type(123):
			result = int(result)
		elif result == None:
			result = ""
		return result

	def read_value_in_cell_as_text(self, sheet_name="", xyxy=""):
		"""
		읽어온값 자체를 변경하지 않고 그대로 읽어오는 것
		그자체로 text형태로 돌려주는것
		만약 스캔을 한 숫자가 ,를 잘못 .으로 읽었다면
		48,100 => 48.1로 엑셀이 바로 인식을 하는데
		이럴때 48.100으로 읽어와서 바꾸는 방법을 하기위해 사용하는 방법
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		result = sheet_object.Cells(x1, y1).Text
		if result == None:
			result = ""
		return result

	def read_value_in_cell_as_value2(self, sheet_name="", xyxy=""):
		"""
		값을 일정한 영역에서 갖고온다
		만약 영역을 두개만 주면 처음과 끝의 영역을 받은것으로 간주해서 알아서 처리하도록 변경하였다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		result = sheet_object.Cells(x1, y1).Value2
		if result == None:
			result = ""
		return result

	def read_value_in_continuous_range(self, sheet_name="", xyxy=""):
		"""
		현재선택된 셀을 기준으로 연속된 영역을 가지고 오는 것입니다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		address = my_range.CurrentRegion()
		result = self.read_value_in_range(sheet_name, address)
		return result

	def read_value_in_currentregion(self, sheet_name="", xyxy=""):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		result = self.read_value_in_continuous_range(sheet_name, xyxy)
		return result

	def read_value_in_range(self, sheet_name, xyxy):
		"""
		영역의 값을 갖고온다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		if x1 == -1:
			return sheet_object.Range(x1, y1).Value
		return my_range.Value

	def read_value_in_range_as_value2(self, sheet_name, xyxy):
		"""
		영역의 값을 갖고온다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		if x1 == -1:
			return sheet_object.Range(x1, y1).Value2
		return my_range.Value2

	def read_value_in_range_speed_up(self, xyxy):
		"""
		영역의 값을 갖고온다
		메뉴에서 제외

		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		x1, y1, x2, y2 = xyxy
		my_range = self.var_pcell["sheet_object"].Range(self.var_pcell["sheet_object"].Cells(x1, y1),
		                                                self.var_pcell["sheet_object"].Cells(x2, y2))
		if x1 == -1:
			return self.var_pcell["sheet_object"].Range(x1, y1).Value
		return my_range.Value

	def read_value_in_range_with_numberformat(self, sheet_name, xyxy):
		"""
		:param sheet_name:
		:param xyxy:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		result = []

		for x in range(x1, x2+1):
			temp = []
			for y in range(y1, y2 + 1):
				one_dic = {}
				one_cell = sheet_object.Cells(x, y)
				one_dic["y"] = x
				one_dic["x"] = y
				one_dic["value"] = one_cell.Value
				one_dic["value2"] = one_cell.Value2
				one_dic["text"] = one_cell.Text
				one_dic["formular"] = one_cell.Formula
				one_dic["formularr1c1"] = one_cell.FormulaR1C1
				one_dic["numberformat"] = one_cell.NumberFormat
				temp.append(one_dic)
			result.append(temp)
		return result


	def read_value_in_range_with_xy_headers(self, sheet_name, xyxy):
		"""
		영역의 값을 갖고온다. 맨앞과 위에 번호로 행과열을 추가한다
		가끔은 자료중에서 필요없는것을 삭제했더니, 원래 있었던 자료의 위치를 알수가 없어서, 만들어 본것임
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		top_line = list(range(y1 - 1, y2 + 1))
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		all_data = list(my_range.Value)
		result = []
		for x in range(0, x2 - x1 + 1):
			temp = [+x1]
			temp.extend(list(all_data[x]))
			result.append(temp)
		result.insert(0, top_line)
		return result

	def read_value_in_selection(self, sheet_name="", xyxy=""):
		"""
		값을 일정한 영역에서 갖고온다
		만약 영역을 두개만 주면 처음과 끝의 영역을 받은것으로 간주해서 알아서 처리하도록 변경하였다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		self.get_activesheet_object()
		self.check_address_value(self.xlapp.Selection.Address)
		result = my_range.Value
		return result

	def read_value_in_usedrange(self, sheet_name=""):
		"""
		usedrange 안의 값을 갖고온다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		xyxy = self.check_address_value(sheet_object.UsedRange.address)
		result = self.read_value_in_range(sheet_name, xyxy)
		return result

	def read_value_in_xline(self, sheet_name="", xx="입력필요"):
		"""
		한줄인 x라인 의 모든값을 읽어온다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xx: 가로줄의 시작과 끝 => [3,5]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, x2 = self.check_xx_address(xx)
		return sheet_object.Range(sheet_object.Cells(x1, 1), sheet_object.Cells(x1, 1)).EntireRow.Value

	def read_value_in_xxline(self, sheet_name="", xx="입력필요"):
		"""
		xx라인의 모든값을 읽어온다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xx: 가로줄의 시작과 끝 => [3,5]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		return sheet_object.Range(sheet_object.Cells(xx[0], 1), sheet_object.Cells(xx[1], 1)).EntireRow.Value

	def read_value_in_yline(self, sheet_name="", yy="입력필요"):
		"""
		한줄인 y라인의 모든값을 읽어온다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param yy: 세로줄의 사작과 끝 => [3,7]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		y1, y2 = self.check_yy_address(yy)
		return sheet_object.Range(sheet_object.Cells(1, y1), sheet_object.Cells(1, y1)).EntireColumn.Value

	def read_value_in_yyline(self, sheet_name="", yy="입력필요"):
		"""
		yy라인의 모든값을 읽어온다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param yy: 세로줄의 사작과 끝 => [3,7]
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		return sheet_object.Range(sheet_object.Cells(1, yy[0]), sheet_object.Cells(1, yy[1])).EntireColumn.Value

	def read_workbook_fullname(self):
		"""
		워크북의 전체 경로와 이름을 읽어온다
		메뉴에서 제외

		:return:
		"""
		return self.xlbook.FullName

	def read_workbook_path(self):
		"""
		워크북의 경로를 읽어온다
		메뉴에서 제외

		:return:
		"""
		return self.xlbook.Path

	def read_workbook_username(self):
		"""
		사용자 이름을 읽어온다
		메뉴에서 제외

		:return:
		"""
		return self.xlapp.Username

	def read_worksheet_count(self):
		"""
		워크시트의 갯수를 읽어온다
		메뉴에서 제외

		:return:
		"""
		return self.xlbook.Worksheets.Count

	def read_worksheet_numbers(self):
		"""
		메뉴에서 제외

		:return:
		"""
		result = self.read_worksheet_count()
		return result

	def replace_word_in_range_by_list2d_style(self, sheet_name="", xyxy="", from_to_list2d=[]):
		"""
		영역안의 글자들을 바꾸기 한다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param from_to_list2d:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		for list1d in from_to_list2d:
			my_range.Replace(list1d[0], list1d[1])

	def replace_word_many_in_range(self, sheet_name="", xyxy="", input_list="입력필요"):
		"""
		한번에 여러 갯수를 바꾸는 것이다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_list: list type
		:return:
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for y in range(y1, y2 + 1):
			for x in range(x1, x2 + 1):
				cell_value = str(self.read_cell_value(sheet_name, [x, y]))
				for one_list in input_list:
					cell_value = cell_value.replace(one_list[0], one_list[1])
				self.write_cell_value(sheet_name, [y, x + 1], cell_value)

	def return_sheet_object(self, sheet_name=""):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		result = self.check_sheet_name(sheet_name)
		return result

	def run_vba_module(self, macro_name):
		"""
		텍스트로 만든 매크로 코드를 실행하는 코드이다
		메뉴에서 제외

		:param macro_name:
		:return:
		"""
		self.xlapp.Run(macro_name)

	def save(self, newfilename=""):
		"""
		엑셀화일을 저장하는것
		메뉴에서 제외

		:param newfilename:
		:return:
		"""
		if newfilename == "":
			self.xlbook.Save()
		else:
			# wb.SaveAs(Filename="C:\\NewFileName.xlsx")
			self.xlbook.SaveAs(newfilename, 6)

	def select_cell(self, sheet_name="", xyxy=""):
		"""
		영역을 선택한다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		sheet_object.Cells(x1, y1).Select()

	def select_range(self, sheet_name="", xyxy=""):
		"""
		영역을 선택한다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.Select()

	def select_sheet(self, sheet_name=""):
		"""
		현재의 엑셀중에서 활성화된 시트의 이름을 돌려준다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		if sheet_name == None or sheet_name == "":
			self.show_messagebox_with_value("시트이름을 다시한번 확인 해 주십시요")
		elif sheet_name in self.read_sheet_name_all():
			self.xlbook.Worksheets(sheet_name).Select()

	def select_top_line_in_range(self, sheet_name="", xyxy=""):
		"""
		영역의 제일 위로 이동
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		sheet_object.Cells(x1, y1).Select()

	def select_workbook(self, filename=""):
		"""
		워크북을 선정
		메뉴에서 제외

		:param filename:
		:return:
		"""
		if filename == None or filename == "":
			self.show_messagebox_with_value("워크북이름을 다시한번 확인 해 주십시요")
		else:
			self.xlbook = self.xlapp.Workbooks.Open(self.filename)

	def set_autofilter(self, sheet_name, xyxy):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.Columns.AutoFilter(1)

	def set_autofit_in_range(self, sheet_name="", xyxy="all"):
		"""
		자동 맞춤을 실시
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		new_y1 = self.change_num_to_char(y1)
		new_y2 = self.change_num_to_char(y2)
		if xyxy == "" or xyxy == "all":
			sheet_object.Columns.AutoFit()
		else:
			sheet_object.Columns(new_y1 + ':' + new_y2).AutoFit()

	def set_bold_in_range(self, sheet_name="", xyxy=""):
		"""
		영역안의 글씨체를 진하게 만든다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.Font.Bold = True

	def set_color_bar_by_no(self, sheet_name, xyxy, color_value=255):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param color_value:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		my_range.FormatConditions.AddDatabar
		my_range.FormatConditions(1).NegativeBarFormat.ColorType = 0  # xlDataBarColor =0
		my_range.FormatConditions(1).NegativeBarFormat.Color.Color = color_value
		my_range.FormatConditions(1).NegativeBarFormat.Color.TintAndShade = 0

	def set_conditional_in_range(self):
		"""
		조건부서식을 좀더 사용하기 쉽도록 변경이 필요
		메뉴에서 제외

		:return:
		"""
		sheet_object = self.check_sheet_name("")
		my_range = sheet_object.Range(sheet_object.Cells(1, 1), sheet_object.Cells(20, 20))
		formula1 = ' = IF($A1 = "", TRUE, FALSE)'
		# win32com.client.constants.xlCellValue = > 1
		# win32com.client.constants.xlGreaterEqual = > 7
		my_range.FormatConditions.Add(1, 7, formula1)
		my_range.FormatConditions(my_range.FormatConditions.Count).SetFirstPriority()
		my_range.FormatConditions(1).Font.Bold = True
		my_range.FormatConditions(1).Font.Strikethrough = False
		my_range.FormatConditions(1).Font.TintAndShade = 0
		my_range.FormatConditions(1).Interior.PatternColorIndex = 1
		my_range.FormatConditions(1).Interior.Color = 5296274
		my_range.FormatConditions(1).Interior.TintAndShade = 0
		my_range.FormatConditions(1).StopIfTrue = False

	def set_font_color_in_cell(self, sheet_name="", xy="", font_color=""):
		"""
		셀에 글씨체를 설정한다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xy: [가로번호, 세로번호]
		:param font_color:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xy)
		rgb_value = self.check_input_color_rgb(font_color)
		rgb_int = self.color.change_rgb_to_rgbint(rgb_value)
		my_range = sheet_object.Cells(x1, y1)
		my_range.Font.Color = rgb_int

	def set_font_color_in_range(self, sheet_name="", xyxy="", font_color=""):
		"""
		영역에 글씨체를 설정한다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param font_color:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		rgb_value = self.check_input_color_rgb(font_color)
		rgb_int = self.color.change_rgb_to_rgbint(rgb_value)
		# my_range = sheet_object.Cells(x1, y1)
		my_range.Font.Color = rgb_int

	def set_font_in_range(self, sheet_name="", xyxy="", font="입력필요"):
		"""
		영역에 글씨체를 설정한다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param font:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.Font.Name = font

	def set_font_size_in_range(self, sheet_name="", xyxy="", size="+"):
		"""
		영역에 글씨크기를 설정한다
		2023-07-24 : +-도 가능하게 변경
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param size:
		:return:
 		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		if str(size)[0] == "+":
			size_up = 2 * len(size)
			for one in my_range:
				basic_size = one.Font.Size
				one.Font.size = int(basic_size) + size_up
		elif str(size)[0] == "-":
			size_down = -2 * len(size)
			for one in my_range:
				new_size = one.Font.Size + size_down
				if new_size <= 0:
					one.Font.Size = 3
				else:
					one.Font.Size = new_size
		else:
			my_range.Font.Size = size

	def set_formula_in_range(self, sheet_name="", xyxy="", input_data="=Now()"):
		"""
		set_formula_in_range(sheet_name="", xyxy="", input_data="=Now()")
		영역에 수식을 넣는것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_data: 입력자료
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.Formula = input_data

	def set_fullscreen(self, fullscreen=1):
		"""
		전체화면으로 보기
		메뉴에서 제외

		:param fullscreen:
		:return:
		"""
		self.xlapp.DisplayFullScreen = fullscreen

	def set_fullscreen_for_workbook(self, fullscreen=1):
		"""
		전체화면으로 보이게 하는 것
		메뉴에서 제외

		:param fullscreen:
		:return:
		"""
		self.xlapp.DisplayFullScreen = fullscreen

	def set_gridline_off(self):
		"""
		그리드라인을 없애는것
		메뉴에서 제외

		:return:
		"""
		self.xlapp.ActiveWindow.DisplayGridlines = 0

	def set_gridline_on(self):
		"""
		그리드라인을 나탄게 하는것
		메뉴에서 제외

		:return:
		"""
		self.xlapp.ActiveWindow.DisplayGridlines = 1

	def set_gridline_onoff(self):
		"""
		그리드라인을 껏다 켰다하는 것
		메뉴에서 제외

		:return:
		"""
		if self.xlapp.ActiveWindow.DisplayGridlines == 0:
			self.xlapp.ActiveWindow.DisplayGridlines = 1
		else:
			self.xlapp.ActiveWindow.DisplayGridlines = 0

	def set_height_in_range(self, sheet_name, xyxy, height=13.5):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param height: 높이설정
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.RowHeight = height

	def set_height_in_xxline(self, sheet_name, xx, height=13.5):
		"""
		가로줄의 높이를 설정
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xx: 가로줄의 시작과 끝 => [3,5]
		:param height: 높이설정
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		my_range = sheet_object.Range(sheet_object.Cells(xx[0], 1), sheet_object.Cells(xx[1], 1))
		my_range.RowHeight = height

	def set_interactive_flase(self):
		"""
		:return:
		"""
		self.xlapp.Interactive = False

	def set_interactive_true(self):
		"""
		:return:
		"""
		self.xlapp.Interactive = True

	def set_lower_in_range(self, sheet_name, xyxy):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_object.Cells(y, x).Value
				sheet_object.Cells(y, x).Value = str(value.lower())

	def set_ltrim_in_range(self, sheet_name, xyxy):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_object.Cells(y, x).Value
				sheet_object.Cells(y, x).Value = str(value.lstrip())

	def set_merge_in_range(self, sheet_name="", xyxy=""):
		"""
		셀들을 병합하는 것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.Merge(0)

	def set_name_in_range(self, name):
		"""
		메뉴에서 제외

		:param name:
		:return:
		"""
		self.xlbook.Names.Add(name, vars["range"])

	def set_numberformat(self, sheet_name, xyxy, numberformat):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param numberformat:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		my_range.NumberFormat = numberformat

	def set_numberformat_in_cell(self, sheet_name="", xyxy="", numberformat="#,##0.00_ "):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param numberformat: 숫자의 형식
		:return:
		"""
		self.set_numberformat_in_range(sheet_name, xyxy, numberformat)

	def set_numberformat_in_range(self, sheet_name="", xyxy="", numberformat="#,##0.00_ "):
		"""
		영역에 숫자형식을 지정하는 것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param numberformat: 숫자의 형식
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.NumberFormat = numberformat

	def set_numberproperty_in_range(self, sheet_name="", xyxy="", type1="입력필요"):
		"""
		좀더 사용하기 쉽도록 변경이 필요
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param type1:
		:return:
		"""
		if type1 == 'general':
			result = "#,##0.00_ "
		elif type1 == 'number':
			result = "US$""#,##0.00"
		elif type1 == 'account':
			result = "_-""US$""* #,##0.00_ ;_-""US$""* -#,##0.00 ;_-""US$""* ""-""??_ ;_-@_ "
		elif type1 == 'date':
			result = "mm""/""dd""/""xx"
		elif type1 == 'datetime':
			result = "xxxx""-""m""-""d h:mm AM/PM"
		elif type1 == 'percent':
			result = "0.00%"
		elif type1 == 'bunsu':
			result = "# ?/?"
		elif type1 == 'jisu':
			result = "0.00E+00"
		elif type1 == 'text':
			result = "@"
		elif type1 == 'etc':
			result = "000-000"
		elif type1 == 'other':
			result = "$#,##0.00_);[빨강]($#,##0.00)"
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.NumberFormat = result

	def set_picture_in_cell(self, sheet_name, xy, full_path):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xy: [가로번호, 세로번호]
		:param full_path: 화일의 전체 경로
		:return:
		"""
		self.insert_image_in_xyxy(sheet_name, xy, full_path)

	def set_print_area(self, sheet_name, area, fit_wide=1):
		"""
		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param area:
		:param fit_wide:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		new_area = self.change_xyxy_to_r1c1(area)
		sheet_object.PageSetup.PrintArea = new_area

		sheet_object.PageSetup.Orientation = 1
		sheet_object.PageSetup.Zoom = False
		sheet_object.PageSetup.FitToPagesTall = False
		sheet_object.PageSetup.FitToPagesWide = fit_wide

	def set_print_page(self, sheet_name="", **var_dic):
		"""
		좀더 사용하기 쉽도록 변경이 필요
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param var_dic:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.PageSetup.Zoom = False
		sheet_object.PageSetup.FitToPagesTall = 1
		sheet_object.PageSetup.FitToPagesWide = 1
		# sheet_object.PageSetup.PrintArea = print_area
		sheet_object.PageSetup.LeftMargin = 25
		sheet_object.PageSetup.RightMargin = 25
		sheet_object.PageSetup.TopMargin = 50
		sheet_object.PageSetup.BottomMargin = 50
		# sheet_object.ExportAsFixedFormat(0, path_to_pdf)
		sheet_object.PageSetup.LeftFooter = "&D"  # 날짜
		sheet_object.PageSetup.LeftHeader = "&T"  # 시간
		sheet_object.PageSetup.CenterHeader = "&F"  # 화일명
		sheet_object.PageSetup.CenterFooter = "&P/&N"  # 현 page/ 총 page
		sheet_object.PageSetup.RightHeader = "&Z"  # 화일 경로
		sheet_object.PageSetup.RightFooter = "&P+33"  # 현재 페이지 + 33

	def set_range_nocolor(self, sheet_name, xyxy):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		self.delete_color_in_range(sheet_name, xyxy)

	def set_rangename(self, sheet_name="", xyxy="", name=""):
		"""
		rangename을 설정하는 것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param name:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		self.xlbook.Names.Add(name, my_range)

	def set_rtrim_in_range(self, sheet_name, xyxy):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_object.Cells(y, x).Value
				sheet_object.Cells(y, x).Value = str(value.rstrip())

	def get_xlines_when_same_yline_with_input_data_in_range(self, sheet_name, xyxy, filter_line, input_value,
	                                                        first_line_is_title=True):
		"""
		선택한 영역의 특정 y값이 입력값과 같은 x라인들을 돌려 주는것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param filter_line:
		:param input_value:
		:param first_line_is_title:
		:return:
		"""
		list_2d = self.read_value_in_range(sheet_name, xyxy)
		result = []

		if first_line_is_title:
			result.append(list_2d[0])

		for list_1d in list_2d:
			if input_value in list_1d[int(filter_line)]:
				result.append(list_1d)

		return result

	def split_xline_as_per_input_word_in_yline(self, sheet_name, xyxy, yline_index, input_value,
	                                           first_line_is_title=True):
		"""
		선택한 영역에서 특정 y값이 입력값을 갖고있을때, 입력값들에 따라서 x라인들을 저장한후 돌려준다

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param yline_index:
		:param input_value:
		:param first_line_is_title:
		:return:
		"""
		list_2d = self.read_value_in_range(sheet_name, xyxy)
		result = {"_main_data": []}
		for one_value in input_value:
			result[one_value] = []

		if first_line_is_title:
			for one_key in result.keys():
				result[one_key].append(list_2d[0])
			list_2d = list_2d[1:]

		for list_1d in list_2d:
			found = False
			for one_key in result.keys():
				if one_key in list_1d[int(yline_index)]:
					result[one_key].append(list_1d)
					found = True
			if found == False:
				result["_main_data"].append(list_1d)

		return result

	def set_screen_update_off(self):
		"""
		화면 변화를 잠시 멈추는것
		메뉴에서 제외

		:return:
		"""
		self.xlapp.ScreenUpdating = False

	def set_screen_update_on(self):
		"""
		화면 변화를 시작
		메뉴에서 제외

		:return:
		"""
		self.xlapp.ScreenUpdating = True

	def set_sheet(self, sheet_name):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		self.var_pcell["sheet"] = self.check_sheet_name(sheet_name)

	def set_sheet_as_hide(self, sheet_name, hide=0):
		"""
		시트 숨기기
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param hide:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Visible = hide

	def set_sheet_lock_off(self, sheet_name, password="1234"):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param password:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Unprotect(password)

	def set_sheet_lock_on(self, sheet_name, password="1234"):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param password:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)

		sheet_object.protect(password)

	def set_strikethrough_in_range(self, sheet_name, xyxy):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		my_range.Font.Strikethrough = True

	def set_swapcase_in_range(self, sheet_name, xyxy):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_object.Cells(y, x).Value
				sheet_object.Cells(y, x).Value = str(value.swapcase())

	def set_trim_in_range(self, sheet_name, xyxy):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_object.Cells(y, x).Value
				sheet_object.Cells(y, x).Value = str(value.strip())

	def set_underline_in_range(self, sheet_name, xyxy):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))

		my_range.Font.Underline = True

	def set_unmerge_in_range(self, sheet_name="", xyxy=""):
		"""
		영역안의 병합된 것을 푸는 것이다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.UnMerge()

	def set_unmerge_in_sheet(self, sheet_name=""):
		"""
		시트안의 모든 영역의 병합된 것을 푸는 것이다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.UnMerge()

	def set_upper_in_range(self, sheet_name, xyxy):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				value = sheet_object.Cells(y, x).Value
				sheet_object.Cells(y, x).Value = str(value.upper())

	def set_use_same_sheet_obj_off(self, sheet_name=""):
		"""
		같은 시트를 사용할때, 속도를 높이기도 하면서, activesheet가 여러개의 엑셀에서 왔다갔다하는것을 방지할 목적이다

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		self.var_pcell["sheet_object"] = False

	def set_use_same_sheet_obj_on(self, sheet_name=""):
		"""
		같은 시트를 사용할때, 속도를 높이기도 하면서, activesheet가 여러개의 엑셀에서 왔다갔다하는것을 방지할 목적이다

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트 sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:return:
		"""
		self.var_pcell["sheet_object"] = self.check_sheet_name(sheet_name)

	def set_visible_for_sheet(self, input_data=0):
		"""
		시트를 감추는것
		메뉴에서 제외

		:param input_data: 입력자료
		:return:
		"""
		self.xlapp.Visible = input_data

	def set_visible_for_workbook(self, value=1):
		"""
		실행되어있는 엑셀을 화면에 보이지 않도록 설정합니다
		기본설정은 보이는 것으로 되너 있읍니다
		메뉴에서 제외

		:param value:
		:return:
		"""
		self.xlapp.Visible = value

	def set_width_in_yyline(self, sheet_name, yy, width=5):
		"""
		가로줄의 넓이를 설정
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param yy: 세로줄의 사작과 끝 => [3,7]
		:param width:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		my_range = sheet_object.Range(sheet_object.Cells(1, yy[0]), sheet_object.Cells(1, yy[1]))
		my_range.ColumnWidth = width

	def set_workbook_as_hide(self):
		"""
		실행되어있는 엑셀을 화면에 보이지 않도록 설정합니다
		메뉴에서 제외

		:return:
		"""
		self.xlapp.Visible = 0

	def set_wrap_in_range(self, sheet_name="", xyxy="", input_data=""):
		"""
		셀의 줄바꿈을 설정할때 사용한다
		만약 status를 false로 하면 줄바꿈이 실행되지 않는다.
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_data: 입력자료
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		sheet_object.Range(xyxy).WrapText = input_data

	def sort_2_excel_files_001(self):
		"""
		두개시트의 자료를 기준으로 정렬한다선택한
		단 두개의 자료는 각각 정렬이되어있어야 한다
		빈칸은 없어야 한다
		메뉴에서 제외

		:return:
		"""
		# 1. 두개의 시트의 첫번째 열을 읽어온다
		sheet_names = self.read_sheet_name_all()

		# 첫번째 시트의 첫번째 행의 자료를 갖고오는 것이다
		sheet1_name = sheet_names[0]
		sheet1_usedrange = self.read_address_usedrange(sheet1_name)
		y_start, x_start, y_end, x_end = self.change_address_type(sheet1_usedrange[2])[1]
		datas1 = self.read_range_value(sheet1_name, [1, x_start, 1, x_end])

		# 두번째 시트의 첫번째 행의 자료를 갖고오는 것이다
		sheet2_name = sheet_names[1]
		sheet2_usedrange = self.read_address_usedrange(sheet2_name)
		y_start, x_start, y_end, x_end = self.change_address_type(sheet2_usedrange[2])[1]
		datas2 = self.read_range_value(sheet2_name, [1, x_start, 1, x_end])

		# 첫번째것과 두번째것을 비교하여 컬럼을 추가한다
		all_dic = {}
		for data1 in datas1:
			if data1[0] in all_dic:
				all_dic[data1[0]] = all_dic[data1[0]] + 1
			else:
				all_dic[data1[0]] = 1

		for data2 in datas2:
			if data2[0] in all_dic:
				all_dic[data2[0]] = all_dic[data2[0]] + 1
			else:
				all_dic[data2[0]] = 1

		# 각각 시트를 돌아가며 칸을 넣는다
		# 딕셔너리의 키를 리스트로 만든다
		all_dic_list = list(all_dic.keys())

		try:
			all_dic_list.remove(None)
		except:
			pass

		all_dic_list_sorted = sorted(all_dic_list)

		# 딕셔너리의 값들을 리스트로 만들어서 값을 만든다
		all_dic_values_list = list(all_dic.values())
		temp_1 = 0
		for one in all_dic_values_list:
			temp_1 = temp_1 + int(one)

		# 첫번째 시트를 맞도록 칸을 넣는다
		temp_2 = []
		for one in all_dic_list_sorted:
			for two in range(int(all_dic.get(one))):
				temp_2.append(one)

		temp_3 = 0
		for one in range(len(temp_2)):
			print(temp_2[one], datas1[temp_3][0])
			try:
				if temp_2[one] == datas1[temp_3][0]:
					temp_3 = temp_3 + 1
				else:
					self.insert_xxline_in_range(sheet1_name, one + 1)
			except:
				self.insert_xxline_in_range(sheet1_name, one + 1)

		temp_4 = 0
		for one in range(len(temp_2)):
			try:
				if temp_2[one] == datas2[temp_4][0]:
					temp_4 = temp_4 + 1
				else:
					self.insert_xxline_in_range(sheet2_name, one + 1)
			except:
				self.insert_xxline_in_range(sheet2_name, one + 1)

	def sort_with_two_range(self, sheet_name, xyxy1, xyxy2):
		"""
		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy1:
		:param xyxy2:
		:return:
		"""
		list2d_1 = self.read_value_in_range(sheet_name, xyxy1)
		list2d_2 = self.read_value_in_range(sheet_name, xyxy2)
		list2d_3 = list(list2d_2)
		self.new_sheet()
		line = 1
		len_width = len(list2d_1[0])
		total_line_no = 1
		current_x = 0

		for index, one in enumerate(list2d_1):
			current_x = current_x + 1
			self.write_value_in_range("", [current_x, 1], one)
			temp = 0
			for index2, one_2 in enumerate(list2d_2):
				if one[0] == one_2[0] and (one[0] != "" or one[0] != None):
					temp = temp + 1
					if temp > 1:
						current_x = current_x + 1
					self.write_value_in_range("", [current_x, len_width + 1], one_2)
					list2d_3[index2] = ["", ""]

		# print(list2d_3)

		total_line_no = line + len(list2d_1)
		for one in list2d_3:
			if one[0] != "" and one[0] != None:
				current_x = current_x + 1
				self.write_value_in_range("", [current_x, len_width + 1], one)

	def sound_beep(self, sec=1000, hz=500):
		"""
		beep 음을 내는 것
		메뉴에서 제외

		:param sec:
		:param hz:
		:return:
		"""
		win32api.Beep(hz, sec)

	def split_partial_value_in_range_by_step_from_start(self, sheet_name, xyxy, n_char):
		"""
		어떤 자료중에 앞에서 몇번째것들만 갖고오고 싶을때
		예:시군구 자료에서 앞의 2글자만 분리해서 얻어오는 코드

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param n_char:
		:return:
		"""
		list_2d = self.read_value_in_range(sheet_name, xyxy)
		result = set()
		for list_1d in list_2d:
			for one in list_1d:
				try:
					result.add(one[0:n_char])
				except:
					pass
		return list(result)

	def split_path_n_file_name(self, filename=""):
		"""
		화일 이름을 경로와 이름으로 구분하는 것이다
		메뉴에서 제외

		:param filename:
		:return:
		"""
		path = ""
		changed_filename = filename.replace("\\", "/")
		split_list = changed_filename.split("/")
		file_name_only = split_list[-1]
		if len(changed_filename) == len(file_name_only):
			path = ""
		else:
			path = changed_filename[:len(file_name_only)]

		return [path, file_name_only]

	def split_value_as_engnum(self, data):
		"""
    	단어중에 나와있는 숫자, 영어를 분리하는기능

		:param data:
		:return:
		"""
		re_compile = re.compile(r"[a-zA-Z0-9]+")
		result = re_compile.findall(data)

		new_result = []
		for dim1_data in result:
			for dim2_data in dim1_data:
				new_result.append(dim2_data)
		return new_result

	def split_value_by_special_string(self, sheet_name="", input_text="입력필요"):
		"""
		split_inputvalue_as_special_string( input_text="입력필요"):
		선택한 1줄의 영역에서 원하는 문자나 글자를 기준으로 분리할때
		2개의 세로행을 추가해서 결과값을 쓴다

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param input_text: 입력되는 text형식의 자료
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		rng_select = self.read_address_in_selection()
		rng_used = self.read_address_usedrange()
		[x1, y1, x2, y2] = self.intersect_range1_range2(rng_select, rng_used)
		self.insert_xline("", x1 + 1)
		self.insert_xline("", x1 + 1)
		result = []
		length = 2
		# 자료를 분리하여 리스트에 집어 넣는다
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				cell_value = sheet_object.Cells(x, y).Value
				list_data = cell_value.split(input_text)
				result.append(list_data)
		# 집어넣은 자료를 다시 새로운 세로줄에 넣는다
		for y_no in range(len(result)):
			if len(result[x_no]) > length:
				for a in range(len(result[x_no]) - length):
					self.insert_xline("", x1 + length)
				length = len(result[x_no])
			for x_no in range(len(result[x_no])):
				sheet_object.Cells(x1 + x_no, y1 + y_no + 1).Value = result[x_no][y_no]

	def split_value_to_str_num(self, input_text):
		"""
		문자와 숫자를 분리하는것

		:param input_text: 입력되는 text형식의 자료
		:return:
		"""
		re_com_num = re.compile("[a-zA-Z]+|\d+")
		result = re_com_num.findall(input_text)
		return result

	def terms(self):
		"""
		용어들에 대한 정리
		메뉴에서 제외

		:return:
		"""
		result = """
			"""
		return result

	def test_1(self, sheet_name="", xyxy=""):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		sheet_object = self.check_sheet_name(sheet_name)
		result = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		return result

	def test_2(self, sheet_name="", xyxy=""):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		r1c1 = self.change_xyxy_to_r1r1([x1, y1, x2, y2])
		sheet_object = self.check_sheet_name(sheet_name)
		result = sheet_object.Range(r1c1)
		return result

	def vlookup_with_multi_line(self, input_data1, input_data2):
		"""
		보통 vlookup은 한줄을 비교해서 다른 자료를 찾는데
		이것은 여러항목이 같은 값을 기준으로 원하는 것을 찾는 것이다
		input_datal = [자료의영역, 같은것이있는위치, 결과값의위치]
		메뉴에서 제외

		:param input_data1:
		:param input_data2:
		:return:
		"""
		base_data2d = self.read_value_in_range("", input_data1[0])
		compare_data2d = self.read_value_in_range("", input_data2[0])
		result = ""
		for one_data_1 in base_data2d:
			gijun = []
			one_data_1 = list(one_data_1)
			for no in input_data1[1]:
				gijun.append(one_data_1[no - 1])
			x = 0

			for value_1d in compare_data2d:
				value_1d = list(value_1d)
				x = x + 1
				bikyo = []

				for no in input_data2[1]:
					bikyo.append(value_1d[no - 1])

				if gijun == bikyo:
					result = one_data_1[input_data1[2] - 1]
				self.write_value_in_cell("", [x, input_data2[2]], result)

	def write_cell(self, sheet_name="", xyxy="", input_datas="입력필요"):
		"""
		많이 사용하는 것이라 짧게 만듦

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_datas:
		:return:
		"""
		self.write_value_in_cell(sheet_name, xyxy, input_datas)

	def write_cell_value(self, sheet_name="", xyxy="", value="입력필요"):
		"""
		예전자료를 위한것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param value:
		:return:
		"""
		self.write_value_in_cell(sheet_name, xyxy, value)

	def write_df_to_excel(self, sheet_name="", df_obj="입력필요", xyxy=[1, 1]):
		"""
		dataframe의 자료를 엑셀로 넘기는 것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param df_obj:
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		col_list = df_obj.columns.values.tolist()
		value_list = df_obj.values.tolist()
		self.write_value_in_range(sheet_name, xyxy, [col_list])
		self.write_value_in_range(sheet_name, [x1 + 1, y1], value_list)

	def write_dic_key_in_cell(self, sheet_name="", xyxy="", input_dic="입력필요"):
		"""
		사전으로 입력된 키값을 엑셀에 쓰는것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_dic:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		changed_input_datas = list(input_dic.keys())

		for x in range(0, len(changed_input_datas)):
			sheet_object.Cells(x + x1, y1).Value = changed_input_datas[x]

	def write_emptycell_as_uppercell_in_range(self, sheet_name="", xyxy=""):
		"""
		빈셀을 위의것으로 채우는 것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		list2d_data = self.read_value_in_range(sheet_name, xyxy)

		old_data = ""
		upper_value = ""
		for ix, list1d in enumerate(list2d_data):
			for iy, one_value in enumerate(list1d):
				if one_value == "" or one_value == None:
					self.write_value_in_cell("", [ix + x1, iy + y1], upper_value)
				else:
					upper_value = one_value

	def write_emptycell_in_range_as_uppercell(self, sheet_name="", xyxy=""):
		"""
		문제가 있어서, 아랫것으로 변경

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:return:
		"""
		self.fill_emptycell_as_uppercell_in_range(sheet_name, xyxy)

	def write_formula_in_range(self, sheet_name, xyxy, input_data="=Now()"):
		"""
		수식을 넣는 것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_data: 입력자료
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		my_range = sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x2, y2))
		my_range.Formula = input_data

	def write_list1d_at_cell_as_down(self, sheet_name="", xy="", input_list1d="입력 필요"):
		"""
		1차원자료를 시작셀을 기준으로 아래로 값을 넣는 것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xy: [가로번호, 세로번호]
		:param input_list1d: list type, 1차원 리스트형
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xy)
		for index, value in enumerate(input_list1d):
			sheet_object.Cells(x1 + index, y1).Value = value

	def write_list1d_at_cell_as_group(self, sheet_name="", xy="", input_list1d="입력 필요"):
		"""
		1차원자료를 시작셀을 기준으로 아래로 값을 넣는 것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xy: [가로번호, 세로번호]
		:param input_list1d: list type, 1차원 리스트형
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xy)
		for index, value in enumerate(input_list1d):
			sheet_object.Cells(x1 + index, y1).Value = value

	def write_list1d_from_cell_as_yline(self, sheet_name="", xyxy="", input_list1d=""):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_list1d: list type, 1차원 리스트형
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x, value in enumerate(input_list1d):
			sheet_object.Cells(x1 + x, y1).Value = input_list1d[x]

	def write_list1d_in_range(self, sheet_name="", xyxy="", input_list="입력필요"):
		"""
		1줄의 리스트는 가로로 나열된다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_list: list type
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		if x1 == x2 and y1 == y2:
			min_y = len(input_list)
		else:
			min_y = min(len(input_list), y2 - y1 + 1)
		for y in range(min_y):
			sheet_object.Cells(x1, y1 + y).Value = input_list[y]

	def write_list1d_in_yline(self, sheet_name="", xyxy="", input_datas="입력 필요"):
		"""
		아래의 예제는 엑셀의 값중에서 y라인으로 자동으로 한줄을 넣는 기능이 없어서，만들어 보았다
		영역에 값는 넣기
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_datas:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		for x in range(0, len(input_datas)):
			sheet_object.Cells(x + x1, y1).Value = input_datas[x]

	def write_list1d_in_yline_speed_up(self, xyxy="", input_datas="입력 필요"):
		"""
		아래의 예제는 엑셀의 값중에서 y라인으로 자동으로 한줄을 넣는 기능이 없어서，만들어 보았다
		영역에 값는 넣기
		메뉴에서 제외

		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_datas:
		:return:
		"""
		x1, y1, x2, y2 = xyxy
		for x in range(0, len(input_datas)):
			self.var_pcell["sheet_object"].Cells(x + x1, y1).Value = input_datas[x]

	def write_list2d_from_cell(self, sheet_name="", xyxy="", input_list2d=""):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_list2d: list type 2dimension, 2차원의 리스트형
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, yl, x2, y2 = self.check_address_value(xyxy)
		for x, list_ld in enumerate(input_list2d):
			for y, value in enumerate(list_ld):
				sheet_object.Cells(x1 + x, yl + y).Value = input_list2d[x][y]

	def write_list2d_from_start_cell_by_mixed_types(self, sheet_name="", xyxy="", input_mixed=""):
		"""
		여러가지 자료가 쉬여있는 자료를 쓰는것
		아래의 자료를 쓰기위한것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_mixed:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		for x, list_1d in enumerate(input_mixed):
			shift_y = 0
			for y, one_data in enumerate(list_1d):
				if type(one_data) == type("abc") or type(one_data) == type(1):
					# 문자나 숫자일때
					sheet_object.Cells(x1 + x, y1 + shift_y).Value = one_data
					shift_y = shift_y + 1
				elif type(one_data) == type([]) or type(one_data) == type((1)):
					# 리스트나 튜플일때
					for num, value in enumerate(one_data):
						sheet_object.Cells(x1 + x, y1 + shift_y).value = value
						shift_y = shift_y + 1
				elif type(one_data) == type(()):
					# 사전형식일때
					changed_list = list(one_data.items())
					for num, value in enumerate(changed_list):
						sheet_object.Cells(x1 + x, y1 + shift_y).value = value[0]
						shift_y = shift_y + 1
						sheet_object.cel1s(x1 + x, y1 + shift_y).value = value[1]
						shift_y = shift_y + 1

	def write_list2d_in_range(self, sheet_name="", xyxy="", input_list="입력필요"):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_list: list type
		:return:
		"""
		self.write_list_in_range(sheet_name, xyxy, input_list)

	def write_list_in_range(self, sheet_name="", xyxy="", input_list="입력필요"):
		"""
		2차원의 값만 입력할 수 있다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_list: list type
		:return:
		"""
		if type(input_list[0]) == type([]):
			self.write_value_in_range(sheet_name, xyxy, input_list)
		else:
			self.write_value_in_range(sheet_name, xyxy, [input_list])

	def write_memo_in_cell(self, sheet_name="", xyxy="", text="입력필요"):
		"""
		셀에 메모를 넣는것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param text:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		r1c1 = self.change_xyxy_to_r1c1(xyxy)
		my_range = sheet_object.Range(r1c1)

		my_range.AddComment(text)

	def write_message_in_statusbar(self, input_text="test"):
		"""
		메뉴에서 제외

		:param input_text: 입력되는 text형식의 자료
		:return:
		"""
		self.xlapp.StatusBar = input_text

	def write_messagebox_value(self, input_text, input_title="pcell"):
		"""
		메뉴에서 제외

		:param input_text: 입력되는 text형식의 자료
		:param input_title:
		:return:
		"""
		win32gui.MessageBox(0, input_text, input_title, 0)

	def write_messagebox_value(self, input_text="입력필요", input_title="pcell"):
		"""
		보관용
		메뉴에서 제외

		:param input_text: 입력되는 text형식의 자료
		:param input_title:
		:return:
		"""
		win32gui.MessageBox(0, input_text, input_title, 0)

	def write_nansu_in_range(self, sheet_name="", xyxy="", input_list=[1, 100]):
		"""
		입력한 숫자범위에서 난수를 만들어서 영역에 써주는것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_list: list type
		:return:
		"""
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		no_start, no_end = input_list
		basic_data = list(range(no_start, no_end + 1))
		random.shuffle(basic_data)
		temp_no = 0
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				self.write_cell_value(sheet_name, [x, y], basic_data[temp_no])
				if temp_no >= no_end - no_start:
					random.shuffle(basic_data)
					temp_no = 0
				else:
					temp_no = temp_no + 1

	def write_range(self, sheet_name="", xyxy="", input_datas="입력필요"):
		"""
		많이 사용하는 것이라 짧게 만듦

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_datas:
		:return:
		"""
		self.write_value_in_range(sheet_name, xyxy, input_datas)

	def write_serial_no(self, sheet_name, xyxy, start_no=1, step=1):
		"""
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param start_no:
		:param step: n번째마다 반복되는것
		:return:
		"""
		new_no = start_no
		for no in range(0, xyxy[2] - xyxy[0] + 1):
			self.write_value_in_cell(sheet_name, [xyxy[0] + no, xyxy[1]], new_no)
			new_no = new_no + step

	def write_serial_no_by_step(self, xyxy, start_no=1, step=1):
		"""
		선택한 영역에 시작번호, 간격으로 이루어진 연속된 숫자를 쓰는것
		메뉴에서 제외

		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param start_no:
		:param step: n번째마다 반복되는것
		:return:
		"""
		new_no = start_no
		for no in range(0, xyxy[2] - xyxy[0] + 1):
			self.write_value_in_cell("", [xyxy[0] + no, xyxy[1]], new_no)
			new_no = new_no + step

	# print([xyxy[0]+no, xyxy[1]], new_no)

	def write_serial_no_by_step_to_yline(self, xyxy, start_no=1, step=1):
		"""
		선택한 영역에 시작번호, 간격으로 이루어진 연속된 숫자를 쓰는것
		예 :  0,2,4,6,8....

		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param start_no:
		:param step: n번째마다 반복되는것
		:return:
		"""
		new_no = start_no
		for no in range(0, xyxy[2] - xyxy[0] + 1):
			self.write_value_in_cell("", [xyxy[0], xyxy[1] + no], new_no)
			new_no = new_no + step

	def write_value_in_activecell(self, value="입력필요"):
		"""
		활성화된 셀에 값는 넣기
		메뉴에서 제외

		:param value:
		:return:
		"""
		xy = self.read_address_in_activecell()
		self.write_value_in_cell("", [xy[0], xy[1]], value)

	def write_value_in_cell(self, sheet_name="", xyxy="", value="입력필요"):
		"""
		셀에 값는 넣기
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param value:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		# 문자형식의 숫자인지를 확인하는 것
		# 숫자와 문자가 모두 숫자형으로 인식하여서 첨가해야하는 것
		if type(value) == type("abc"):
			re_com = re.compile("^[0-9.]+$")
			check_type = re_com.search(value)
			if check_type != None:
				changed_value = "'" + value
			else:
				changed_value = value
		else:
			changed_value = value
		sheet_object.Cells(x1, y1).Value = changed_value

	def write_value_in_cell_speed(self, xy, value):
		"""
		먼저 set_sheet함수를 이용해서 sheet를 설정하여야 한다
		문자형식의 숫자인지를 확인하는 것
		숫자와 문자가 모두 숫자형으로 인식하여서 첨가해야하는 것
		메뉴에서 제외

		:param xy: [가로번호, 세로번호]
		:param value:
		:return:
		"""
		if type(value) == type("abc"):
			re_com = re.compile("^[0-9.]+$")
			check_type = re_com.search(value)
			if check_type != None:
				changed_value = "'" + value
			else:
				changed_value = value
		else:
			changed_value = value
		self.var_pcell["sheet"].Cells(xy[0], xy[1]).Value = changed_value

	def write_value_in_range(self, sheet_name="", xyxy="", input_datas="입력필요"):
		"""
		영역에 값는 넣기
		이것은 하나하나 입력이 되는 모습을 보여주며서, 실행되는 것이다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_datas:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)
		changed_input_datas = self.change_input_data_to_list2d(input_datas)

		for x in range(0, len(changed_input_datas)):
			for y in range(0, len(changed_input_datas[x])):
				sheet_object.Cells(x + x1, y + y1).Value = changed_input_datas[x][y]

	def write_value_in_range_as_speedy(self, sheet_name="", xyxy="", input_datas="입력필요"):
		"""
		2022-12-23 : x1, y1이 잘못되어서 변경함
		영역과 자료의 갯수중에서 작은것을 기준으로 값을 쓰는데
		만약 영역이 셀하나이면 자료를 전부 쓴다
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_datas:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		min_x = min(x2 - x1 + 1, len(input_datas))
		min_y = min(y2 - y1 + 1, len(input_datas[0]))

		if x1 == x2 and y1 == y2:
			# 셀이 영역을 선택하지 않았다면, 전체 자료를 전부 넣는다
			changed_datas = input_datas
			sheet_object.Range(sheet_object.Cells(x1, y1), sheet_object.Cells(x1 + len(input_datas) - 1, y1 + len(
				input_datas[0]) - 1)).Value = changed_datas
		else:
			# 영역을 선택하면, 두 영역중에 작은 부분을 기준으로 자료를 넣는다
			changed_datas = []
			for x in range(min_x):
				changed_datas.append(input_datas[x][:min_y])
			sheet_object.Range(sheet_object.Cells(x1, y1),
			                   sheet_object.Cells(x1 + min_x - 1, y1 + min_y - 1)).Value = changed_datas

	def write_value_in_range_at_newsheet(self, input_datas):
		"""
		메뉴에서 제외

		:param input_datas:
		:return:
		"""
		self.add_sheet_new()
		self.write_value_in_range("", [1, 1], input_datas)

	def write_value_in_range_by_range_priority(self, sheet_name="", xyxy="", input_datas="입력필요"):
		"""
		영역이 더 우선하는 것
		메뉴에서 제외

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_datas:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		checked_datas = self.change_input_data_to_list2d(input_datas)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		address_list = self.check_intersect_address(xyxy, input_datas)

		x_len = len(checked_datas)
		if (x2 - x1) <= x_len:
			x_len = x2 - x1

		y_len = len(checked_datas[0])
		if (y2 - y1) <= y_len:
			y_len = y2 - y1

		for x in range(0, x_len):
			for y in range(0, y_len):
				sheet_object.Cells(x + x1, y + y1).Value = input_datas[x][y]

	def write_value_in_range_by_trans(self, sheet_name="", xyxy="", input_list2d=""):
		"""
		입력자료의 xy를 바꿔서 입력하는 것

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_list2d: list type 2dimension, 2차원의 리스트형
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				sheet_object.Cells(y, x).Value = input_list2d[x][y]

	def write_value_in_range_xystep(self, sheet_name="", xyxy="", input_text="", xystep=[1, 1]):
		"""
		선택한 영역의 시작점부터 x,y 번째 셀마다 값을 넣기

		:param sheet_name: sheet name, 시트이름, ""을 시용하면, 현재활성화된 시트
		:param xyxy: range as like [1,1,2,2] = a1:b2, 4가지 꼭지점의 숫자 번호
		:param input_text: 입력되는 text형식의 자료
		:param xystep:
		:return:
		"""
		sheet_object = self.check_sheet_name(sheet_name)
		x1, y1, x2, y2 = self.check_address_value(xyxy)

		for x in range(x1, x2 + 1):
			if divmod(x, xystep[0])[1] == 0:
				for y in range(y1, y2 + 1):
					if divmod(y, xystep[1])[1] == 0:
						sheet_object.Cells(x, y).Value = str(input_text)

	def write_vba_module(self, vba_code, macro_name):
		"""
		텍스트로 만든 매크로 코드를 실행하는 코드이다
		메뉴에서 제외

		:param vba_code:
		:param macro_name:
		:return:
		"""
		new_vba_code = "Sub " + macro_name + "()" + vba_code + "End Sub"
		mod = self.xlbook.VBProject.VBComponents.Add(1)
		mod.CodeModule.AddFromString(new_vba_code)

	def z_sample_print_letter_cover_01(self):
		"""
		메뉴에서 제외
		봉투인쇄

		:return:
		"""
		# 기본적인 자료 설정
		data_from = [["sheet1", [1, 2]], ["sheet1", [1, 4]], ["sheet1", [1, 6]], ["sheet1", [1, 8]]]
		data_to = [["sheet2", [1, 2]], ["sheet2", [2, 2]], ["sheet2", [3, 2]], ["sheet2", [2, 3]]]

		no_start = 1
		no_end = 200
		step = 5

		# 실행되는 구간
		for no in range(no_start, no_end):
			for one in range(len(data_from)):
				value = self.read_cell_value(data_from[one][0], data_from[one][1])
				self.write_cell_value(data_to[one][0], [data_to[one][1][0] + (step * no), data_to[one][1][1]], value)

	def z_sample_switch_datas_01(self):
		"""
		메뉴에서 제외

		:return:
		"""
		sheet_name = self.read_activesheet_name()
		[x1, y1, x2, y2] = self.read_address_for_selection()

		# 새로운 세로행을 만든후 그곳에 두열을 서로 하나씩 포개어서 값넣기
		# a 1   ==> a
		# b 2       1
		#           b
		#           2

		new_x = 1

		self.insert_yline("", 1)
		for x in range(x1, x2 + 1):
			for y in range(y1, y2 + 1):
				cell_value = str(self.read_cell_value(sheet_name, [x, y + 1]))
				self.write_cell_value(sheet_name, [new_x, 1], cell_value)
				new_x = new_x + 1
