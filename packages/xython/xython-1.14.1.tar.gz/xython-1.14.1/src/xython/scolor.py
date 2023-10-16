# -*- coding: utf-8 -*-
import re  #내장모듈
import math
import basic_data  # xython 모듈

class scolor:
	"""
	색을 쉽게 사용하기위해 만든 모듈
	기본색은 rgb로 한다
	"""
	def __init__(self):
		self.base_data = basic_data.basic_data()
		self.var = self.base_data.vars
		self.var_common={}

	def change_scolor_to_hsl(self, input_scolor):
		result = self.change_scolor_to_hsl(input_scolor)
		return result

	def change_scolor_to_rgb(self, input_scolor):
		hsl_value = self.change_scolor_to_hsl(input_scolor)
		result = self.change_hsl_to_rgb(hsl_value)
		return result

	def change_excel_56_color_no_to_rgb(self, input_no):
		"""
		엑셀 기본 rgb 56색의 번호를 rgb로 바꾸는 것
		"""
		result = self.var["rgb_56_for_excel"][int(input_no)]
		return result

	def change_excel_color_no_to_rgb(self, input_no):
		"""
		엑셀 기본 rgb 56색의 번호를 rgb로 바꾸는 것
		"""
		result = self.change_excel_56_color_no_to_rgb(input_no)
		return result

	def change_hsl_to_rgb(self, hsl):
		"""
		hsl을 rgb로 바꾸는 것이다
		"""
		h, s, l = hsl

		h = float(h / 360)
		s = float(s / 100)
		l = float(l / 100)

		if s == 0:
			R = l * 255
			G = l * 255
			B = l * 255

		if l < 0.5:
			temp1 = l * (1 + s)
		else:
			temp1 = l + s - l * s

		temp2 = 2 * l - temp1

		#h = h / 360

		tempR = h + 0.333
		tempG = h
		tempB = h - 0.333

		if tempR < 0: tempR = tempR + 1
		if tempR > 1: tempR = tempR - 1
		if tempG < 0: tempG = tempG + 1
		if tempG > 1: tempG = tempG - 1
		if tempB < 0: tempB = tempB + 1
		if tempB > 1: tempB = tempB - 1

		if 6 * tempR < 1:
			R = temp2 + (temp1 - temp2) * 6 * tempR
		else:
			if 2 * tempR < 1:
				R = temp1
			else:
				if 3 * tempR < 2:
					R = temp2 + (temp1 - temp2) * (0.666 - tempR) * 6
				else:
					R = temp2

		if 6 * tempG < 1:
			G = temp2 + (temp1 - temp2) * 6 * tempG
		else:
			if 2 * tempG < 1:
				G = temp1
			else:
				if 3 * tempG < 2:
					G = temp2 + (temp1 - temp2) * (0.666 - tempG) * 6
				else:
					G = temp2
		if 6 * tempB < 1:
			B = temp2 + (temp1 - temp2) * 6 * tempB
		else:
			if 2 * tempB < 1:
				B = temp1
			else:
				if 3 * tempB < 2:
					B = temp2 + (temp1 - temp2) * (0.666 - tempB) * 6
				else:
					B = temp2
		R = int(abs(round(R * 255,0)))
		G = int(abs(round(G * 255,0)))
		B = int(abs(round(B * 255,0)))

		#rgb_to_int = (int(B)) * (256 ** 2) + (int(G)) * 256 + int(R)
		return [R, G, B]

	def change_hsl_to_rgb_by_change_mode(self, hsl_value, change_mode):
		"""
		change_mode : ++, --, 70등의 값이 들어오면 변화를 시켜주는 것
		"""
		if type(change_mode) == type(123):
			#50을 기본으로 차이나는 부분을 계산하는것
			l_value = change_mode - 50
			if l_value < 0:
				l_value = 0
		elif "+" == str(change_mode)[0]:
			# 현재의 값에서 10만큼 밝아지도록 한다
			l_value = 10 * len(change_mode)
		elif "-" == str(change_mode)[0]:
			# 현재의 값에서 10만큼 어두워지도록 한다
			l_value = -10 * len(change_mode)

		final_l_value = hsl_value[2] + l_value
		if final_l_value > 100 :
			final_l_value = 100
		elif final_l_value < 0 :
			final_l_value = 0

		result = [hsl_value[0], hsl_value[1], final_l_value]
		return result

	def change_hsl_to_rgb_by_triangle_style(self, hsl):
		"""
		등간격 3색조합 : triad
		활동적인 인상과 이미지를 보인다
		"""
		h, s, l = hsl

		new_h_1 = divmod(h + 120, 360)[1]
		new_h_3 = divmod(h + 240, 360)[1]

		rgb_1 = self.change_hsl_to_rgb([new_h_1, s, l])
		rgb_2 = self.change_hsl_to_rgb(hsl)
		rgb_3 = self.change_hsl_to_rgb([new_h_3, s, l])
		result = [rgb_1, rgb_2, rgb_3]
		return result

	def change_hsl_to_rgb_for_4_tetra_style(self, hsl):
		"""
		4가지 꼭지의
		"""
		h, s, l = hsl

		new_h_1 = divmod(h + 0, 360)[1]
		new_h_2 = divmod(h + 90, 360)[1]
		new_h_3 = divmod(h + 180, 360)[1]
		new_h_4 = divmod(h + 270, 360)[1]
		rgb_1 = self.change_hsl_to_rgb([new_h_1, s, l])
		rgb_2 = self.change_hsl_to_rgb([new_h_2, s, l])
		rgb_3 = self.change_hsl_to_rgb([new_h_3, s, l])
		rgb_4 = self.change_hsl_to_rgb([new_h_4, s, l])
		result = [rgb_1, rgb_2, rgb_3, rgb_4]

		return result

	def change_hsl_to_rgb_for_bo_style(self, hsl):
		"""
		입력된 hsl의 보색을 알려주는것
		보색 : Complementary
		2차원 list의 형태로 돌려줌
		"""
		h, s, l = hsl
		new_h = divmod(h+180, 360)[1]
		result = self.change_hsl_to_rgb([new_h, s, l])
		return [result]

	def change_hsl_to_rgb_for_bo_style_1(self, hsl):
		"""
		mode : 1
		보색 : Complementary
		"""
		h, s, l = hsl

		new_h_1 = h + 180
		if new_h_1 >= 360:
			new_h_1 = 360 - new_h_1

		result_rgb = self.change_hsl_to_rgb([new_h_1, s, l])
		return result_rgb

	def change_hsl_to_rgb_with_20_hsl_by_s_step(self, hsl):
		"""
		위쪽으로 5개, 아래로 5개의 명도가 비슷한 색을 돌려준다
		"""
		h, s, l = hsl
		result = []
		for no in range(0, 21):
			temp = self.change_hsl_to_rgb([h, no*5, l])
			result.append(temp)
		return result

	def change_hsl_to_rgb_with_near_10_color_set(self, hsl, step = 10):
		"""
		위쪽으로 5개, 아래로 5개의 채도가 비슷한 색을 돌려준다
		채도의 특성상 비슷한 부분이 많아서 10단위로 만든다
		"""
		h, s, l = hsl
		result = []
		for no in range(0,100+step,step):
			#print("변경된 hsl은 s=> ", [h, no, l])
			temp = self.change_hsl_to_rgb([h, no, l])
			result.append(temp)
		return result

	def change_hsl_to_rgb_with_pccs_style(self, input_hsl, color_style="파스텔", style_step=5):
		"""
		입력된 기본 값을 스타일에 맞도록 바꾸고, 스타일을 강하게 할것인지 아닌것인지를 보는것
		color_style : pccs의 12가지 사용가능, 숫자로 사용가능, +-의 형태로도 사용가능
		입력예 : 기본색상, 적용스타일, 변화정도,("red45, 파스텔, 3)
		변화정도는 5를 기준으로 1~9까지임
		"""

		step = self.var["color_tone_12_names_vs_no"][color_style]
		step_2 = self.var["sl_big_step_vs_sl_no"][step] # 스타일을 적용하는것
		step_1 = self.var["sl_small_step_vs_sl_no"][str(style_step)] # 스타일을 얼마나 강하게 적용할것인가를 나타내는것

		h = int(input_hsl[0])
		s = int(step_1[0]) + int(step_2[0])
		l = int(step_1[1]) + int(step_2[1])

		changed_rgb = self.change_hsl_to_rgb([h, s, l])
		return changed_rgb

	def change_input_value_to_hsl(self, input_value):
		"""
		입력되는 형태에 따라서 hsl을 돌려주는것
		입력값 : rgb형식, hsl형식, scolor형식
		결과값 : hsl값
		"""
		if type(input_value) == type("string"): #문자열 형식일때 scolor형식으로 해석
			hsl = self.change_scolor_to_hsl(input_value)

		elif type(input_value) == type(123): #숫자가 입력되면 rgbint값으로 해석
			rgb = self.change_rgbint_to_rgb(input_value)
			hsl = self.change_rgb_to_hsl(rgb)

		elif type(input_value) == type([]) and len(input_value) == 3:  # 3개의 리스트형식일때는 확인해서 hsl 이나 rgb로 해석
			if input_value[0] > 255:
				hsl = input_value
			else:
				if input_value[1]>100 or input_value[2] >100:
					hsl = self.change_rgb_to_hsl(input_value)
				else: hsl = input_value
		else:
			hsl = "error"
		return hsl

	def change_rgb_to_12_pccs_rgb_list(self, rgb):
		"""
		pccs : 일본색체연구서가 빌표한 12가지 색으로 구분한것
		어떤 입력된 색의 기본적인 PCSS 12색을 돌려준다
		pccs톤, rgb로 넘어온 색을 pcss톤 12개로 만들어서 돌려준다
		"""
		result = []
		h, s, l = self.change_rgb_to_hsl(rgb)
		result4 = self.var["color_name_for_basic_12_eng"]
		for one in result4:
			result.append([h, one[0], one[1]])
		return result

	def change_rgb_to_hex(self, rgb):
		"""
		엑셀의 Cells(1, i).Interior.Color는 hex값을 사용한다
		"""
		r, g, b = rgb[2], rgb[1], rgb[0]
		result = f"#{int(round(r)):02x}{int(round(g)):02x}{int(round(b)):02x}"
		return result

	def change_rgb_to_hsl (self, rgb_list):
		"""
		rgb를 hsl로 바꾸는 것이다
		입력은 0~255사이의 값
		"""
		#r,g,b = rgb_list
		r = float(rgb_list[0] / 255)
		g = float(rgb_list[1] / 255)
		b = float(rgb_list[2] / 255)
		max1 = max(r, g, b)
		min1 = min(r, g, b)
		l = (max1 + min1) / 2

		if max1 == min1:
			s = 0
		elif l < 0.5:
			s = (max1 - min1) / (max1 + min1)
		else:
			s = (max1 - min1) / (2 - max1 - min1)

		if s ==0:
			h = 0
		elif r >= max(g, b):
			h = (g - b) / (max1 - min1)
		elif g >= max(r, b):
				h = 2+ (b - r) / (max1 - min1)
		else:
				h = 4+ (r - g) / (max1 - min1)
		h = h *60
		if h > 360 :
			h = h -360
		if h < 0 :
			h = 360 -h

		return [int(h), int(s*100), int(l*100)]

	def change_rgb_to_rgbint(self, rgb_list):
		"""
		rgb인 값을 color에서 인식이 가능한 값으로 변경하는 것이다
		엑셀에서는 rgb랑 이 정수를 사용하여 색을 지정한다
		"""
		result =  int(rgb_list[0]) + (int(rgb_list[1])) * 256 + (int(rgb_list[2])) * (256 ** 2)
		return result

	def change_rgbint_to_hsl(self, input_int):
		"""
		int값을 rgb로 바꾸는 것이다
		"""
		rgb = self.change_rgbint_to_rgb(input_int)
		hsl = self.change_rgb_to_hsl(rgb)
		return hsl

	def change_rgbint_to_rgb(self, input_int):
		"""
		int값을 rgb로 바꾸는 것이다
		"""
		mok0, namuji0 = divmod(input_int, 256*256)
		mok1, namuji1 = divmod(namuji0, 256)
		result = [namuji1, mok1, mok0]
		return result

	def change_scolor_to_hsl (self, input_scolor):
		"""
		입력형식 : scolor형식, 12, red45, red
		결과 : [h, s, l]
		입력된 자료를 기준으로 shl값을 돌려주는것
		"""
		#print("입력된 color값은 => ", input_scolor)
		if type(input_scolor) == type([]):
			if input_scolor[0] > 255:
				result = input_scolor
			else:
				if input_scolor[1]>100 or input_scolor[2] >100:
					result = self.change_rgb_to_hsl(input_scolor)
				else: result = input_scolor
		else:
			[number_only, color_name, color_step] = self.check_input_scolor(input_scolor)

			if number_only != "":
				#만약 숫자만 입력을 햇다면, 엑셀 번호로 생각하는것
				r_no, g_no, b_no = self.var["rgb_56_for_excel"][int(number_only)]
			else:
				#색을 번호로 변경하는것
				#print("색이름은 ==> ", color_name)
				color_name = self.var["check_color_name"][color_name]

				if color_name =="whi" or color_name =="bla" or color_name =="gra":
					#만약 색이 흰색, 검정, 회색일경우는 h,s는 0으로 한다
					l_code_dic = {"bla": 0, "gra": 50, "whi": 100}
					h_code = 0
					s_code = 0
					l_code = int(l_code_dic[color_name]) + int(color_step)
				elif color_name and color_step == 0:
					# 기본색 인경우
					h_code, s_code, l_code = self.var["color_name_eng_vs_hsl_no"][color_name]
				else:
					# 기타 다른 경우
					#print(color_name)
					#print(self.basic_12hsl_set)
					h_code = self.var["color_name_eng_vs_hsl_no"][color_name][0]
					s_code = 100
					l_code = int(color_step)

				if int(l_code) > 100 : l_code = 100
				if int(l_code) < 0 : l_code = 0
			#print("[h_code, s_code, l_code] ==> ", h_code, s_code, l_code)
			result = [h_code, s_code, l_code]
		return result



	def change_scolor_to_rgb_with_pccs_style(self, input_scolor="red45", color_style="파스텔", style_step=5):
		"""
		입력된 기본 값을 스타일에 맞도록 바꾸고, 스타일을 강하게 할것인지 아닌것인지를 보는것
		color_style : pccs의 12가지 사용가능, 숫자로 사용가능, +-의 형태로도 사용가능
		입력예 : 기본색상, 적용스타일, 변화정도,("red45, 파스텔, 3)
		변화정도는 5를 기준으로 1~9까지임
		"""
		# 넘어온 자료중 color값을 hsl로 변경한다
		basic_hsl = self.change_scolor_to_hsl(input_scolor)
		# 스타일을 적용하는것
		aaa = self.var["color_tone_12_names_vs_no"][color_style]
		step_2 = self.var["sl_small_step_vs_sl_no"][aaa]
		# 스타일을 얼마나 강하게 적용할것인가를 나타내는것
		step_1 = self.var["sl_big_step_vs_sl_no"][str(style_step)]

		h = int(basic_hsl[0])
		s = int(basic_hsl[1]) + int(step_1[0]) + int(step_2[0])
		l = int(basic_hsl[2]) + int(step_1[1]) + int(step_2[1])

		changed_rgb = self.change_hsl_to_rgb([h, s, l])
		return changed_rgb

	def check_change_mode(self, change_mode):

		if type(change_mode) == type([]):
			result = change_mode
		elif "+" == str(change_mode)[0]:
			#현재의 값에서 10만큼 밝아지도록 한다
			l_value = 10 * len(change_mode)
			result = [0, 0, l_value]
		elif "-" == str(change_mode)[0]:
			#현재의 값에서 10만큼 어두워지도록 한다
			l_value = -10 * len(change_mode)
			result = [0, 0, l_value]
		elif change_mode in self.var["color_tone_12_names_vs_no"].keys():
			no = self.var["color_tone_12_names_vs_no"][change_mode]
			result = self.var["sl_big_step_vs_sl_no"][no]
		return result

	def check_rgb_to_excel_color_no(self, input_rgb):
		# 입력 R6B 값중에서 엑셀의 56 가지 기본색상의 R6B 값과 가장 가까운값을 찾아내는것
		result = 0
		short_length = 255 * 255 * 255
		var_56_rgb = self.var["dic_colorindex_rgblist"]
		for excel_color_no in var_56_rgb.keys():
			excel_rgb = var_56_rgb[excel_color_no]
			differ = self.distance_two_3d_point(input_rgb, excel_rgb)
			if short_length > differ:
				short_length = differ
				result = excel_color_no
		return result

	def check_input_hsl(self, input_color):
		# 입력으로 들어온 색에 대한 hsl값을 돌려준다
		try:
			color_name = self.var["check_color_name"][input_color]
			result = self.var["color_name_eng_vs_hsl_no"][color_name]
		except:
			pass
		# 입력된 색이름을 찾을수 없을때
		return result

	def check_input_color(self, input_value):
		result = self.change_input_value_to_hsl(input_value)
		return result

	def check_input_rgb(self, input_value):
		"""
		입력값이 rgbint인지 rgb리스트인지를 확인후 돌려주는것
		"""
		if type(input_value) == type(123):
			rgb = self.change_rgbint_to_rgb(input_value)
		else:
			rgb = input_value
		return rgb

	def check_input_scolor(self, input_scolor):
		"""
		scolor형식의 입력값을 확인하는 것이다
		입력값 : "red++"
		출력값 : ["숫자만","색이름","변화정도"] ==> ["","red","60"]
		"""
		number_only = ""
		color_name =""
		color_no = 50

		#색을 나타내는 글자를 추출해서,
		# 기본색이름으로 변경하는 것이다
		re_com1 = re.compile("[a-zA-Z_가-힣]+")
		#print("input_scolor", input_scolor)
		color_str = re_com1.findall(input_scolor)
		#print("color_str", color_str)
		#print(self.var["check_color_name"])

		if color_str != []:
			if color_str[0] in self.var["check_color_name"].keys():
				color_name = self.var["check_color_name"][color_str[0]]
			else:
				color_name = "not_found_" + str(color_str[0])

		# 새롭게 정의해 보자
		#숫자로 정도를 표기한것인지를 알기위하여 숫자를 추출한다
		re_com2 = re.compile("[0-9]+")
		no_str = re_com2.findall(input_scolor)
		if no_str != []:
			color_no = int(no_str[0])
			if str(no_str[0]) == str(input_scolor):
					number_only = color_no

		#+나-를 추출하기위한 코드이다
		re_com3 = re.compile("[+]+")
		color_plus = re_com3.findall(input_scolor)
		if color_plus != []:
			color_no = 50 + 5 * len(color_plus[0])

		re_com4 = re.compile("[-]+")
		color_minus = re_com4.findall(input_scolor)
		if color_minus != []:
			color_no = 50 - 5 * len(color_minus[0])

		result = [number_only, color_name, color_no]
		#print(result)
		return result

	def control_hsl_by_scolor_style(self, input_hsl, s_step="++", l_step="++"):
		"""
		sl의값을 조정하여 채도와 명도를 조절하는것
		입력형식 : hsl값을 올리거나 내리는 것
		입력 : [[36, 50, 50], "++", "--"]
		약 5씩이동하도록 만든다
		"""
		step_no = 5  # 5단위씩 변경하도록 하였다
		h, s, l = input_hsl

		if s_step == "":
			pass
		elif s_step[0] == "+":
			s = s + len(s_step) * step_no
			if s > 100: s = 100
		elif s_step[0] == "-":
			s = s - len(s_step) * step_no
			if s < 0: s = 0

		if l_step == "":
			pass
		elif l_step[0] == "+":
			l = l + len(l_step) * step_no
			if l > 100: l = 100
		elif l_step[0] == "-":
			l = l - len(l_step) * step_no
			if l < 0: l = 0

		result = self.change_hsl_to_rgb([h, s, l])
		return result

	def control_scolor_by_bright_value(self, input_scolor, my_value=30):
		#값이 0이면 기본값으로, -100 ~ +100까지
		input_hsl = self.change_scolor_to_hsl(input_scolor)
		result = self.control_hsl_to_bright_level(input_hsl, my_value)
		return result


	def control_hsl_by_bright_level(self, input_hsl, strong_level=0.5):
		"""
		통상 level은 0~1사이의값으로 나타낸다

		입력받은 hsl값을 명도가 높은 쪽으로 이동시키는것
		bright = [100,100], sharp = [50,100], graish = [100,0], dark = [0,0], black = [50, 0]
		"""
		h, s, l = input_hsl

		changed_s = s + (100 - s) * strong_level
		changed_l = l + (100 - l) * strong_level
		return [h, changed_s, changed_l]

	def control_hsl_by_dark_level(self, input_hsl, strong_level=0.5):
		"""
		통상 level은 0~1사이의값으로 나타낸다
		입력받은 hsl값을 어두운 쪽으로 이동시키는것
		bright = [100,100], sharp = [50,100], graish = [100,0], dark = [0,0], black = [50, 0]
		"""
		h, s, l = input_hsl
		style = dark = [0,0]

		delta_s = (style[0] - s) * strong_level
		delta_l = (style[1] - l) * strong_level

		changed_s = s + delta_s
		changed_l = l + delta_l
		return [h, changed_s, changed_l]

	def control_hsl_by_gray_level(self, input_hsl, strong_level=0.5):
		"""
		입력받은 hsl값을 어두운 쪽으로 이동시키는것
		bright = [100,100], sharp = [50,100], graish = [100,0], dark = [0,0], black = [50, 0]
		"""
		h, s, l = input_hsl
		style = graish = [100,0]

		delta_s = (style[0] - s) * strong_level
		delta_l = (style[1] - l) * strong_level

		changed_s = s + delta_s
		changed_l = l + delta_l
		return [h, changed_s, changed_l]

	def control_hsl_by_pastel_level(self, input_hsl, strong_level=0.5):
		"""
		입력받은 hsl값을 파스텔톤으로 적용시키는것
		bright = [100,100], sharp = [50,100], graish = [100,0], dark = [0,0], black = [50, 0]
		"""
		h, s, l = input_hsl
		style = pastel = [0,100]

		delta_s = (style[0] - s)*strong_level
		delta_l = (style[1] - l)*strong_level

		changed_s = s + delta_s
		changed_l = l + delta_l
		return [h, changed_s, changed_l]

	def control_hsl_by_vivid_level(self, input_hsl, strong_level=0.5):
		"""
		입력받은 hsl값을 어두운 쪽으로 이동시키는것
		bright = [100,100], sharp = [50,100], graish = [100,0], dark = [0,0], black = [50, 0]
		"""
		h, s, l = input_hsl
		style = sharp = [50,100]

		delta_s = (style[0] - s) * strong_level
		delta_l = (style[1] - l) * strong_level

		changed_s = s + delta_s
		changed_l = l + delta_l
		return [h, changed_s, changed_l]

	def control_hsl_by_value(self, input_hsl, step_no):
		# +，-로 조정을 하는것이다
		s, l = self.var["+-_value_vs_sl_no"][step_no]
		result = [input_hsl[0], input_hsl[1] + s, input_hsl[2] + l]

	def control_hsl_by_color_style(self, basic_hsl, color_style="파스텔", style_step=5):
		color_style = self.var["check_color_tone"][color_style]
		#print(color_style)
		step_2 = self.var["color_tone_simple_eng_vs_sl_no"][color_style]
		step_1 = self.var["sl_small_step_vs_sl_no"][str(str(style_step))]
		h = int(basic_hsl[0])
		s = int(step_1[0]) + int(step_2[0])
		l = int(step_1[1]) + int(step_2[1])

		changed_rgb = self.change_hsl_to_rgb([h, s, l])
		return changed_rgb

	def control_rgb_by_scolor_style(self, input_rgb, s_step="++", l_step="++"):
		input_hsl = self.change_rgb_to_hsl(input_rgb)
		step_no = 5  # 5단위씩 변경하도록 하였다
		h, s, l = input_hsl

		if s_step == "":
			pass
		elif s_step[0] == "+":
			s = s + len(s_step) * step_no
			if s > 100: s = 100
		elif s_step[0] == "-":
			s = s - len(s_step) * step_no
			if s < 0: s = 0

		if l_step == "":
			pass
		elif l_step[0] == "+":
			l = l + len(l_step) * step_no
			if l > 100: l = 100
		elif l_step[0] == "-":
			l = l - len(l_step) * step_no
			if l < 0: l = 0

		result = self.change_hsl_to_rgb([h, s, l])
		return result

	def control_scolor_by_pccs_style (self, input_scolor="red45", color_style="파스텔", style_step = 5):
		"""
		입력된 기본 값을 스타일에 맞도록 바꾸고, 스타일을 강하게 할것인지 아닌것인지를 보는것
		color_style : pccs의 12가지 사용가능, 숫자로 사용가능, +-의 형태로도 사용가능
		입력예 : 기본색상, 적용스타일, 변화정도,("red45, 파스텔, 3)
		변화정도는 5를 기준으로 1~9까지임
		"""

		#넘어온 자료중 color값을 hsl로 변경한다
		basic_hsl = self.change_scolor_to_hsl(input_scolor)
		#스타일을 적용하는것
		step_2 = self.var["sl_small_step_vs_sl_no"][color_style]
		#스타일을 얼마나 강하게 적용할것인가를 나타내는것
		step_1 = self.var["sl_big_step_vs_sl_no"][str(style_step)]

		h = int(basic_hsl[0])
		s = int(basic_hsl[1]) + int(step_1[1]) + int(step_2[1])
		l = int(basic_hsl[2]) + int(step_1[2]) + int(step_2[2])

		changed_rgb = self.change_hsl_to_rgb([h,s,l])
		return changed_rgb


	def control_scolor_for_light_level(self, input_scolor, my_value=.3):
		input_hsl = self.change_scolor_to_hsl(input_scolor)
		result = self.control_hsl_by_dark_level(input_hsl, my_value)
		return result

	def control_scolor_for_pastel_level(self, input_scolor, my_value=.3):
		input_hsl = self.change_scolor_to_hsl(input_scolor)
		result = self.control_hsl_by_pastel_level(input_hsl, my_value)
		return result

	def control_scolor_for_vivid_level(self, input_scolor, my_value=.3):
		input_hsl = self.change_scolor_to_hsl(input_scolor)
		result = self.control_hsl_by_vivid_level(input_hsl, my_value)
		return result

	def data_color_name_eng_for_12set(self):
		"""
		12가지 영어 색깔이름을 돌려준다
		['rm', 'bm', 'cya', 'blu', 'gra', '유황', 'red', 'pale_pink', 'mag', 'bc', 'sca', 'yel', 'bla', 'ora', 'bro', 'gy', 'gre', 'scarlet', 'whi', 'gc', 'pin', 'sulphur_yellow']
		"""
		result = self.var["color_name_for_basic_12_eng"]
		return result

	def data_color_name_kor_for_12set(self):
		"""
		12가지 한글 색깔이름을 돌려준다
		"""
		result = self.var["color_name_for_basic_12_kor"]
		return result

	def data_pccs_style_name_eng_for_12set(self):
		result = self.var["color_tone_eng"]
		return result

	def data_pccs_style_name_kor_for_12set(self):
		result = self.var["color_tone_kor"]

		return result

	def data_46_excel_rgb_list(self):
		result = self.var["rgb_46_for_excel"]
		return result

	def data_56_excel_rgb_list(self):
		"""
		엑셀 기본 rgb 색 : 56색
		"""
		result = self.var["rgb_56_for_excel"]
		return result

	def data_color_name_eng_all(self):
		"""
		scolor에서 사용할수있는 모든 영어 색깔의 이름들
		"""
		result = self.var["list_colorname_eng"]
		return result

	def data_color_name_kor_all(self):
		"""
		scolor에서 사용할수있는 모든 한글 색깔의 이름들
		"""
		result = self.var["list_colorname_kor"]
		return result

	def data_color_name_all(self):
		"""
		모든 색깔의 이름들
		"""
		result = list(set(self.var["check_color_name"].values()))
		return result

	def data_hsl_12set(self):
		"""
		360도의 색을 30도씩 12개로 구분한 hsl분류표
		"""
		result = self.var["hsl_no_for_basic_12"]
		return result


	def data_rgb_12set(self):
		result = self.var["rgb_for_basic_12"]
		return result

	def data_12rgb_for_pccs_style(self, hsl):
		"""
		12가지 스타일의 hsl을 돌려주는 것이다
		"""
		result = []
		for one_value in self.var["hsl_no_for_basic_12"]:
			temp = self.change_hsl_to_rgb([hsl[0], one_value[0], one_value[1]])
			result.append(temp)
		return result

	def data_rgb_for_12set(self):
		"""
		기본적으로 자장된 자료에서 갖고오는 것이다
		많이 사용하는 다른 색들을 사용하기 위해
		테두리, 폰트색이나 단색으로 나타낼때 사용하면 좋다
		"""
		result = self.var["rgb_for_basic_12"]
		return result

	def data_pccs_style_name_for_12set(self):
		"""
		스타일에 대한 이름을 갖고오는 것이다
		"""
		result = list(self.var["color_tone_12_names_vs_no"].keys())
		return result

	def data_color_name_eng_for_13set(self):
		"""
		기본 13가지 색의 리스트 : 영어
		"""
		result = self.var["color_name_for_basic_12_eng"]
		return result

	def data_color_name_kor_for_13set(self):
		"""
		기본 13가지 색의 리스트 : 한글
		"""
		result = self.var["color_name_for_basic_12_kor"]
		return result

	def data_basic_36_hsl_set(self):
		"""
		기본적인 hsl로된 36색을 갖고온다
		빨간색을 0으로하여 시작한다
		결과값 : hsl
		"""
		result = []
		for one in range(0, 360, 10):
			temp = [one, 100, 50]
			result.append(temp)
		return result

	def data_basic_4356_hsl_set(self):
		"""
		h : 36가지
		s : 11단계
		l : 11단계
		총 4356개의 색집합
		"""
		result = {}
		for h in range(0, 360, 10):
			for s in range(0, 110, 10):
				for l in range(0, 110, 10):
					temp = self.change_hsl_to_rgb([h, s, l])
					result[str(h) + str("_") + str(s) + str("_") + str(l)] = temp
		return result

	def data_basic_8_pastel_rgb_set(self):
		"""
		기본적인
		자료가 있는 색들의 배경색으로 사용하면 좋은 색들
		"""
		color_set = self.var["hsl_no_for_basic_12"][:-4]
		result = []
		for hsl_value in color_set:
			rgb = self.control_hsl_with_pccs_style(hsl_value, "pastel", 4)
			result.append(rgb)
		return result

	def data_basic_color_name_list(self):
		result = self.var["color_name_for_basic_12_kor"]
		return result

	def data_basic_color_step(self):
		result = self.var["basic_color_step"]
		return result

	def data_basic_color_tone_list(self):
		result = self.var["color_tone_kor"]
		return result

	def data_basic_faber_rgb_set(self, start_color=11, code=5):
		"""
		파버 비덴의의 색체 조화론을 코드로 만든것이다
		한가지 색에대하 ㄴ조화를 다룬것
		# White(100-0) - Tone(10-50) - Color(0-0) : 색이 밝고 화사
		# Color(0-0) - Shade(0-75) - Black(0-100) : 색이 섬세하고 풍부
		# White(100-0) - GrayGray(25-75) - Black(0-100) : 무채색의 조화
		# Tint(25-0) - Tone(10-50) - Shade(0-75) 의 조화가 가장 감동적이며 세련됨
		# White(100-0) - Color(0-0) - Black(0-100) 는 기본적인 구조로 전체적으로 조화로움
		# Tint(25-0) - Tone(10-50) - Shade(0-75) - Gray(25-75) 의 조화는 빨강, 주황, 노랑, 초록, 파랑, 보라와 모두 조화를 이룬다
		"""
		h_list = self.var["hsl_no_for_basic_12"]
		sl_faber = self.var["sl_no_for_faber_style"]

		h_no = h_list[start_color][0]
		result = []
		temp_hsl = sl_faber[code]
		for one_sl in temp_hsl:
			rgb = self.change_hsl_to_rgb([h_no, one_sl[0], one_sl[1]])
			result.append(rgb)
		return result

	def data_basic_johannes_rgb_set(self, start_color=11, num_color=4, stongness=5):
		"""
		요하네스 이텐의 색체 조화론을 코드로 만든것이다
		"""
		# start_color : 처음 시작하는 색 번호, 총 색은 12색으로 한다
		# num_color : 표현할 색의 갯수(2, 3, 4, 6만 사용가능)
		# stongness : 색의 농도를 나타내는 것, 검정에서 하양까지의 11단계를 나타낸것, 중간이 5이다
		h_list = self.var["hsl_no_for_basic_12"]
		sl_list = self.var["sl_no_for_basic_11"]
		hsl_johannes = self.var["hsl_no_for_johannes_style"]
		color_set = [[], [], [0, 6], [0, 5, 9], [0, 4, 7, 10], [0, 3, 5, 8, 10], [0, 3, 5, 7, 9, 11]]

		h_no = h_list[start_color][0]
		new_color_set = []
		for temp in color_set[num_color]:
			new_color_set.append((temp + int(h_no / 30)) % 12)

		result = []
		for no in new_color_set:
			temp_hsl = hsl_johannes[no][stongness]
			rgb = self.change_hsl_to_rgb(temp_hsl)
			result.append(rgb)
		return result

	def data_color_tone_kor_list(self):
		"""
		칼라톤에대한 한글이름
		"""
		result = self.var["color_tone_kor"]
		return result

	def data_cool_color_name_list(self):
		"""
		차가운 색깔의 이름들
		"""
		result = ["파랑", "초록", "보라"]
		return result

	def data_worm_color_name_list(self):
		"""
		따뜻한 색깔의 이름들
		"""
		result = ["빨강", "주황", "노랑"]
		return result

	def get_hsl(self, input_scolor):
		result = self.change_input_value_to_hsl(input_scolor)
		return result

	def get_rgb(self, input_scolor):
		result = self.change_scolor_to_rgb(input_scolor)
		return result

	def get_rgb_by_excel_color_no(self, input_no):
		"""
		엑셀의 기본 번호를 넣으면 rgb값을 돌려주는것
		엑셀 기본 rgb 색 : 56색
		"""
		result = self.var["rgb_56_for_excel"][int(input_no)]
		return result

	def get_rgb_list_as_per_input_no (self, input_no=36):
		"""
		입력된 숫자만큼, rgt리스트를 갖고오는것
		기본적인 hsl로된 36색을 갖고온다
		빨간색을 0으로하여 시작한다
		결과값 : hsl
		"""
		result = []
		for one in range(0, 360, int(360/input_no)):
			temp=self.change_hsl_to_rgb([one, 100, 50])
			result.append(temp)
		return result

	def history(self):
		result = 	"""
			2023-03-02 : 전반적으로 이름을 수정함
			"""
		return result

	def make_20_l_step_color_by_18_degree(self, hsl):
		"""
		위쪽으로 5개, 아래로 5개의 명도가 비슷한 색을 돌려준다
		"""
		h, s, l = hsl
		result = []
		for no in range(0, 21):
			temp = [h, s, no * 5]
			result.append(temp)
		return result

	def make_2_near_bo_by_h_step(self, hsl, h_step=36):
		"""
		mode : 14
		근접보색조합 : 보색의 근처색
		분열보색조합 : Split Complementary
		근접보색조합이라고도 한다. 보색의 강한 인상이 부담스러울때 보색의 근처에 있는 색을 사용
		"""
		h, s, l = hsl

		new_h_1 = divmod(h - h_step + 180, 360)[1]
		new_h_3 = divmod(h + h_step + 180, 360)[1]

		hsl_1 = [new_h_1, s, l]
		hsl_3 = [new_h_3, s, l]
		result = [hsl_1, hsl, hsl_3]
		return result


	def make_2_side_color_by_h_step (self, hsl, h_step=36):
		"""
		근접색조합 : 양쪽 근처색
		"""
		h, s, l = hsl

		new_h_1 = divmod(h - h_step, 360)[1]
		new_h_3 = divmod(h + h_step, 360)[1]

		rgb_1 = self.change_hsl_to_rgb([new_h_1, s, l])
		rgb_2 = self.change_hsl_to_rgb(hsl)
		rgb_3 = self.change_hsl_to_rgb([new_h_3, s, l])
		result = [rgb_1, rgb_2, rgb_3]
		return result

	def make_2_side_color_by_l_step_for_hsl(self, hsl, l_step = 30):
		"""
		명도차가 큰 2가지 1가지색
		"""
		h, s, l = hsl
		rgb_1 = self.change_hsl_to_rgb([h, s, l_step])
		rgb_2 = self.change_hsl_to_rgb(hsl)
		rgb_3 = self.change_hsl_to_rgb([h, s, 100-l_step])
		result = [rgb_1, rgb_2, rgb_3]
		return result

	def make_2_side_color_by_s_step_for_hsl (self, hsl, s_step = 30):
		"""
		채도차가 큰 2가지 1가지색
		"""
		rgb_1 = self.change_hsl_to_rgb([hsl[0], s_step, hsl[2]])
		rgb_2 = self.change_hsl_to_rgb(hsl)
		rgb_3 = self.change_hsl_to_rgb([hsl[0], 100-s_step, hsl[2]])
		result = [rgb_1, rgb_2, rgb_3]
		return result

	def make_3_step_color_by_120_degree_for_hsl(self, hsl):
		"""
		mode :
		등간격 3색조합 : triad
		활동적인 인상과 이미지를 보인다
		"""
		h, s, l = hsl

		new_h_1 = divmod(h + 120, 360)[1]
		new_h_3 = divmod(h + 240, 360)[1]

		hsl_1 = [new_h_1, s, l]
		hsl_3 = [new_h_3, s, l]

		result_rgb = self.change_hsl_to_rgb([hsl_1, hsl, hsl_3])
		return result_rgb

	def make_high_bright_hsl_by_l(self, hsl, changed_l = 80):
		"""
		고명도의 hsl로 변경
		"""
		result = self.change_hsl_to_rgb([hsl[0], hsl[1], changed_l])
		return [result]

	def make_hsl_set_by_36_h_step(self, hsl):
		# hsl중에서 10도간격으로 h값을 36개 만드는것
		h, s, l = hsl
		result = []
		for no in range(0, 36):
			result.append([no*10, s, l])
		return result

	def make_low_bright_hsl_by_l(self, hsl, changed_l = 20):
		# 저명도, 20%정도의 명도를 저명도로 말하자자
		result = [hsl[0], hsl[1], changed_l]
		return [result]

	def make_low_color_hsl_by_s(self, hsl, high_s = 20):
		#저채도
		result = self.change_hsl_to_rgb([hsl[0], high_s, hsl[2]])
		return [result]

	def make_middle_bright_hsl_by_l(self, hsl, high_l = 50):
		"""
		중명도의 hsl로 변경
		"""
		result = self.change_hsl_to_rgb([hsl[0], hsl[1], high_l])
		return [result]

	def make_middle_color_hsl_by_s(self, hsl, high_s = 50):
		#중채도
		result = [hsl[0], high_s, hsl[2]]
		return [result]

	def make_n_color_set_by_h(self, hsl, n_step):
		h, s, l = hsl
		result = []
		for no in range(0, n_step):
			new_h = divmod(no * (360 / n_step) + h, 360)[0]
			temp = [new_h, s, l]
			result.append(temp)
		return result


	def make_n_color_set_by_l(self, hsl, n_step):
		h, s, l = hsl
		result = []
		for no in range(0, n_step):
			new_l = divmod(no * n_step + l, 100)[0]
			temp = [h, s, new_l]
			result.append(temp)
		return result





	def make_n_color_set_by_s(self, hsl, n_step):
		h, s, l = hsl
		result = []
		for no in range(0, n_step):
			new_s = divmod(no * n_step + s, 100)[0]
			temp = [h, new_s, l]
			result.append(temp)
		return result


	def make_one_color_to_many_colors_by_step (self, input_color = "red", step = 10):
		"""
		하나의 색을 지정하면 10가지의 단계로 색을 돌려주는 것이다
		"""
		result =[]
		for no in range(0,100,int(100/step)):
			temp = self.change_color_to_rgb(input_color+str(no))
			result.append(temp)
		return result

	def make_strong_color_hsl_by_s(self, hsl, changed_s = 80):
		#고채도
		result = [hsl[0], changed_s, hsl[2]]
		return [result]

	def manual(self):
		result = 	"""
			"""
		return result

	def mix_two_scolors_with_step(self, scolor_1, scolor_2, step=10):
		# 두가지색을 기준으로 몇단계로 색을 만들어주는 기능
		# 예를들어, 발강 ~파랑사이의 색을 10단계로 만들어 주는 기능
		rgb_1 = self.change_scolor_to_rgb(scolor_1)
		rgb_2 = self.change_scolor_to_rgb(scolor_2)
		r_step = int((rgb_2[0] - rgb_1[0]) / step)
		g_step = int((rgb_2[1] - rgb_1[1]) / step)
		b_step = int((rgb_2[2] - rgb_1[2]) / step)
		result = [rgb_1, ]
		for no in range(1, step - 1):
			new_r = int(rgb_1[0] + r_step * no)
			new_g = int(rgb_1[1] + g_step * no)
			new_b = int(rgb_1[2] + b_step * no)
			result.append([new_r, new_g, new_b])
		result.append(rgb_2)
		return result

	def terms(self):
		result = 	"""
			"""
		return result

	#def change_scolor_to_clear(self, input_scolor, my_value=30):
	#def change_scolor_to_worm(self, input_scolor, my_value=30):
	#def change_scolor_to_basic(self, input_scolor, my_value=30):
	#def change_scolor_to_strong(self, input_scolor, my_value=30):

	def data_color_style_list(self):
		style_kor = ['밝은', '기본', '파스텔', '부드러운', '검정', '연한', '탁한', '어두운', '밝은회색', '검은', '짙은', '강한', '회색', '진한', '옅은', '어두운회색', '흐린', '선명한']
		style_eng = ['white', 'vivid', 'soft', 'deep', 'pale', 'gray', 'darkgrayish', 'grayish', 'lightgrayish', 'strong', 'light', 'bright', 'black', 'dull', 'dark']
		result = style_kor + style_eng
		return result

	def change_style(self, input_scolor, style_name):
		hsl = self.change_scolor_to_hsl(input_scolor)
		change_mode = self.var["check_change_step"][style_name]
		result = self.change_hsl_to_rgb_by_change_mode(hsl, change_mode)
		return result

	def change_color_to_rgb_with_pccs_style(self, input_scolor="red45", color_style="파스텔", style_step=5):
		"""
		입력된 기본 값을 스타일에 맞도록 바꾸고, 스타일을 강하게 할것인지 아닌것인지를 보는것
		color_style : pccs의 12가지 사용가능, 숫자로 사용가능, +-의 형태로도 사용가능
		입력예 : 기본색상, 적용스타일, 변화정도,("red45, 파스텔, 3)
		변화정도는 5를 기준으로 1~9까지임
		"""
		# 넘어온 자료중 color값을 hsl로 변경한다
		basic_hsl = self.change_scolor_to_hsl(input_scolor)
		# 스타일을 적용하는것
		aaa = self.var["color_tone_12_names_vs_no"][color_style]
		step_2 = self.var["sl_small_grade_vs_sl_value"][aaa]
		# 스타일을 얼마나 강하게 적용할것인가를 나타내는것
		step_1 = self.var["sl_big_grade_vs_sl_value"][str(style_step)]

		h = int(basic_hsl[0])
		s = int(basic_hsl[1]) + int(step_1[0]) + int(step_2[0])
		l = int(basic_hsl[2]) + int(step_1[1]) + int(step_2[1])

		changed_rgb = self.change_hsl_to_rgb([h, s, l])
		return changed_rgb

	def change_excel56_to_rgb(self, input_no):
		"""
		엑셀 기본 rgb 색 : 56색
		"""
		result = self.var["rgb_56_for_excel"][int(input_no)]
		return result

	def change_hsl_by_change_mode(self, hsl_value, change_mode):
		"""
		change_mode : ++, --, 70등의 값이 들어오면 변화를 시켜주는 것
		"""
		if type(change_mode) == type(123):
			#50을 기본으로 차이나는 부분을 계산하는것
			l_value = change_mode - 50
			if l_value < 0:
				l_value = 0
		elif "+" == str(change_mode)[0]:
			# 현재의 값에서 10만큼 밝아지도록 한다
			l_value = 10 * len(change_mode)
		elif "-" == str(change_mode)[0]:
			# 현재의 값에서 10만큼 어두워지도록 한다
			l_value = -10 * len(change_mode)

		final_l_value = hsl_value[2] + l_value
		if final_l_value > 100 :
			final_l_value = 100
		elif final_l_value < 0 :
			final_l_value = 0

		result = [hsl_value[0], hsl_value[1], final_l_value]
		return result

	def change_hsl_by_high_l(self, hsl, high_l = 80):
		"""
		고명도의 hsl로 변경
		"""
		result = self.change_hsl_to_rgb([hsl[0], hsl[1], high_l])
		return [result]

	def change_hsl_by_high_s(self, hsl, high_s = 80):
		#고채도
		result = self.change_hsl_to_rgb([hsl[0], high_s, hsl[2]])
		return [result]

	def change_hsl_by_low_l(self, hsl, high_l = 20):
		"""
		저명도, 20%정도의 명도를 저명도로 말하자자
		"""
		result = self.change_hsl_to_rgb([hsl[0], hsl[1], high_l])
		return [result]

	def change_hsl_by_low_s(self, hsl, high_s = 20):
		#저채도
		result = self.change_hsl_to_rgb([hsl[0], high_s, hsl[2]])
		return [result]

	def change_hsl_by_middle_l(self, hsl, high_l = 50):
		"""
		중명도의 hsl로 변경
		"""
		result = self.change_hsl_to_rgb([hsl[0], hsl[1], high_l])
		return [result]

	def change_hsl_by_middle_s(self, hsl, high_s = 50):
		#중채도
		result = self.change_hsl_to_rgb([hsl[0], high_s, hsl[2]])
		return [result]

	def change_hsl_to_10_similar_color_set(self, hsl, step = 10):
		"""
		위쪽으로 5개, 아래로 5개의 채도가 비슷한 색을 돌려준다
		채도의 특성상 비슷한 부분이 많아서 10단위로 만든다
		"""
		h, s, l = hsl
		result = []
		for no in range(0,100+step,step):
			#print("변경된 hsl은 s=> ", [h, no, l])
			temp = self.change_hsl_to_rgb([h, no, l])
			result.append(temp)
		return result

	def change_hsl_to_20_hsl_by_l_step(self, hsl):
		"""
		위쪽으로 5개, 아래로 5개의 명도가 비슷한 색을 돌려준다
		"""
		h, s, l = hsl
		result = []
		for no in range(0, 21):
			result.append([h, s, no*5])
		return result

	def change_hsl_to_20_hsl_by_s_step(self, hsl):
		"""
		위쪽으로 5개, 아래로 5개의 명도가 비슷한 색을 돌려준다
		"""
		h, s, l = hsl
		result = []
		for no in range(0, 21):
			result.append([h, no*5, l])
		return result

	def change_hsl_to_2near_bo_style(self, hsl, h_step=36):
		"""
		근접보색조합 : 보색의 양쪽 근처색
		분열보색조합 : Split Complementary
		근접보색조합이라고도 한다. 보색의 강한 인상이 부담스러울때 보색의 근처에 있는 색을 사용
		2차원 list의 형태로 돌려줌
		"""
		h, s, l = hsl

		new_h_1 = divmod(h - h_step + 180, 360)[1]
		new_h_3 = divmod(h + h_step + 180, 360)[1]
		rgb_1 = self.change_hsl_to_rgb([new_h_1, s, l])
		rgb_2 = self.change_hsl_to_rgb(hsl)
		rgb_3 = self.change_hsl_to_rgb([new_h_3, s, l])
		result = [rgb_1, rgb_2, rgb_3]

		return result

	def change_hsl_to_2near_style (self, hsl, h_step=36):
		"""
		근접색조합 : 양쪽 근처색
		"""
		h, s, l = hsl

		new_h_1 = divmod(h - h_step, 360)[1]
		new_h_3 = divmod(h + h_step, 360)[1]

		rgb_1 = self.change_hsl_to_rgb([new_h_1, s, l])
		rgb_2 = self.change_hsl_to_rgb(hsl)
		rgb_3 = self.change_hsl_to_rgb([new_h_3, s, l])
		result = [rgb_1, rgb_2, rgb_3]
		return result

	def change_hsl_to_36_hsl_by_h_step(self, hsl):
		"""
		위쪽으로 5개, 아래로 5개의 명도가 비슷한 색을 돌려준다
		"""
		h, s, l = hsl
		result = []
		for no in range(0, 36):
			result.append([no*10, s, l])
		return result

	def change_hsl_to_3_hsl_with_big_l_gab (self, hsl, l_step = 30):
		"""
		명도차가 큰 2가지 1가지색
		"""
		h, s, l = hsl
		rgb_1 = self.change_hsl_to_rgb([hsl[0], hsl[1], l_step])
		rgb_2 = self.change_hsl_to_rgb(hsl)
		rgb_3 = self.change_hsl_to_rgb([hsl[0], hsl[1], 100-l_step])
		result = [rgb_1, rgb_2, rgb_3]
		return result

	def change_hsl_to_3_hsl_with_big_s_gab (self, hsl, s_step = 30):
		"""
		채도차가 큰 2가지 1가지색
		"""
		rgb_1 = self.change_hsl_to_rgb([hsl[0], s_step, hsl[2]])
		rgb_2 = self.change_hsl_to_rgb(hsl)
		rgb_3 = self.change_hsl_to_rgb([hsl[0], 100-s_step, hsl[2]])
		result = [rgb_1, rgb_2, rgb_3]
		return result

	def change_hsl_to_3rgb_as_like_0_120_240(self, hsl):
		"""
		mode :
		등간격 3색조합 : triad
		활동적인 인상과 이미지를 보인다
		"""
		h, s, l = hsl

		new_h_1 = divmod(h + 120, 360)[1]
		new_h_3 = divmod(h + 240, 360)[1]

		hsl_1 = [new_h_1, s, l]
		hsl_3 = [new_h_3, s, l]

		result_rgb = self.change_hsl_to_rgb([hsl_1, hsl, hsl_3])
		return result_rgb

	def change_hsl_to_3rgb_by_2near_bo(self, hsl, h_step=36):
		"""
		mode : 14
		근접보색조합 : 보색의 근처색
		분열보색조합 : Split Complementary
		근접보색조합이라고도 한다. 보색의 강한 인상이 부담스러울때 보색의 근처에 있는 색을 사용
		"""
		h, s, l = hsl

		new_h_1 = divmod(h - h_step + 180, 360)[1]
		new_h_3 = divmod(h + h_step + 180, 360)[1]

		hsl_1 = [new_h_1, s, l]
		hsl_3 = [new_h_3, s, l]
		result_rgb = self.change_hsl_to_rgb([hsl_1, hsl, hsl_3])
		return result_rgb

	def change_hsl_to_4_tetra_style(self, hsl):
		"""
		4가지 꼭지의
		"""
		h, s, l = hsl

		new_h_1 = divmod(h + 0, 360)[1]
		new_h_2 = divmod(h + 90, 360)[1]
		new_h_3 = divmod(h + 180, 360)[1]
		new_h_4 = divmod(h + 270, 360)[1]
		rgb_1 = self.change_hsl_to_rgb([new_h_1, s, l])
		rgb_2 = self.change_hsl_to_rgb([new_h_2, s, l])
		rgb_3 = self.change_hsl_to_rgb([new_h_3, s, l])
		rgb_4 = self.change_hsl_to_rgb([new_h_4, s, l])
		result = [rgb_1, rgb_2, rgb_3, rgb_4]

		return result

	def change_hsl_to_bo_style(self, hsl):
		"""
		입력된 hsl의 보색을 알려주는것
		보색 : Complementary
		2차원 list의 형태로 돌려줌
		"""
		h, s, l = hsl
		new_h = divmod(h+180, 360)[1]
		result = self.change_hsl_to_rgb([new_h, s, l])
		return [result]

	def change_hsl_to_bo_style_rgb(self, hsl):
		"""
		mode : 1
		보색 : Complementary
		"""
		h, s, l = hsl

		new_h_1 = h + 180
		if new_h_1 >= 360:
			new_h_1 = 360 - new_h_1

		result_rgb = self.change_hsl_to_rgb([new_h_1, s, l])
		return result_rgb

	def change_hsl_to_rgb_with_style_1(self, input_hsl, color_style="파스텔", style_step=5):
		"""
		입력된 기본 값을 스타일에 맞도록 바꾸고, 스타일을 강하게 할것인지 아닌것인지를 보는것
		color_style : pccs의 12가지 사용가능, 숫자로 사용가능, +-의 형태로도 사용가능
		입력예 : 기본색상, 적용스타일, 변화정도,("red45, 파스텔, 3)
		변화정도는 5를 기준으로 1~9까지임
		"""

		step = self.var["color_tone_12_names_vs_no"][color_style]
		step_2 = self.var["sl_big_grade_vs_sl_value"][step] # 스타일을 적용하는것
		step_1 = self.var["sl_small_grade_vs_sl_value"][str(style_step)] # 스타일을 얼마나 강하게 적용할것인가를 나타내는것

		h = int(input_hsl[0])
		s = int(step_1[0]) + int(step_2[0])
		l = int(step_1[1]) + int(step_2[1])

		changed_rgb = self.change_hsl_to_rgb([h, s, l])
		return changed_rgb

	def change_hsl_to_triangle_style(self, hsl):
		"""
		등간격 3색조합 : triad
		활동적인 인상과 이미지를 보인다
		"""
		h, s, l = hsl

		new_h_1 = divmod(h + 120, 360)[1]
		new_h_3 = divmod(h + 240, 360)[1]

		rgb_1 = self.change_hsl_to_rgb([new_h_1, s, l])
		rgb_2 = self.change_hsl_to_rgb(hsl)
		rgb_3 = self.change_hsl_to_rgb([new_h_3, s, l])
		result = [rgb_1, rgb_2, rgb_3]
		return result

	def change_rgb_to_12_pccs_rgb_set(self, rgb):
		"""
		pccs : 일본색체연구서가 빌표한 12가지 색으로 구분한것
		어떤 입력된 색의 기본적인 PCSS 12색을 돌려준다
		pccs톤, rgb로 넘어온 색을 pcss톤 12개로 만들어서 돌려준다
		"""
		result = []
		h, s, l = self.change_rgb_to_hsl(rgb)
		result4 = self.var["color_name_for_basic_12_eng"]
		for one in result4:
			result.append([h, one[0], one[1]])
		return result


	def check_hsl_value(self, input_color):
		# 입력으로 들어온 색에 대한 hsl값을 돌려준다
		try:
			color_name = self.var["check_color_name"][input_color]
			result = self.var["color_name_vs_hsl_value"][color_name]
		except:
			pass
		# 입력된 색이름을 찾을수 없을때
		return result

	def check_input_type(self, input_value):
		hsl = self.check_input_type(input_value)
		return hsl


	def data_12_rgb_list(self):
		result = self.var["rgb_for_basic_12"]
		return result

	def data_basic_56_excel_rgb_set(self):
		"""
		엑셀 기본 rgb 색 : 56색
		"""
		result = self.var["rgb_56_for_excel"]
		return result

	def data_excel_46_rgb_list(self):
		result = self.var["rgb_46_for_excel"]
		return result

	def data_excel_56_rgb_list(self):
		"""
		엑셀 기본 rgb 색 : 56색
		"""
		result = self.var["rgb_56_for_excel"]
		return result

	def control_hsl_to_bright_level(self, input_hsl, strong_level=0.5):
		"""
		입력받은 hsl값을 명도가 높은 쪽으로 이동시키는것
		bright = [100,100], sharp = [50,100], graish = [100,0], dark = [0,0], black = [50, 0]
		"""
		h, s, l = input_hsl
		style = bright = [100,100]

		delta_s = (style[0] - s) * strong_level
		delta_l = (style[1] - l) * strong_level

		changed_s = s + delta_s
		changed_l = l + delta_l
		return [h, changed_s, changed_l]

	def control_hsl_to_dark_level(self, input_hsl, strong_level=0.5):
		"""
		입력받은 hsl값을 어두운 쪽으로 이동시키는것
		bright = [100,100], sharp = [50,100], graish = [100,0], dark = [0,0], black = [50, 0]
		"""
		h, s, l = input_hsl
		style = dark = [0,0]

		delta_s = (style[0] - s) * strong_level
		delta_l = (style[1] - l) * strong_level

		changed_s = s + delta_s
		changed_l = l + delta_l
		return [h, changed_s, changed_l]

	def control_hsl_to_gray_level(self, input_hsl, strong_level=0.5):
		"""
		입력받은 hsl값을 어두운 쪽으로 이동시키는것
		bright = [100,100], sharp = [50,100], graish = [100,0], dark = [0,0], black = [50, 0]
		"""
		h, s, l = input_hsl
		style = graish = [100,0]

		delta_s = (style[0] - s) * strong_level
		delta_l = (style[1] - l) * strong_level

		changed_s = s + delta_s
		changed_l = l + delta_l
		return [h, changed_s, changed_l]

	def control_hsl_to_pastel_level(self, input_hsl, strong_level=0.5):
		"""
		입력받은 hsl값을 파스텔톤으로 적용시키는것
		bright = [100,100], sharp = [50,100], graish = [100,0], dark = [0,0], black = [50, 0]
		"""
		h, s, l = input_hsl
		style = pastel = [0,100]

		delta_s = (style[0] - s)*strong_level
		delta_l = (style[1] - l)*strong_level

		changed_s = s + delta_s
		changed_l = l + delta_l
		return [h, changed_s, changed_l]

	def control_hsl_to_vivid_level(self, input_hsl, strong_level=0.5):
		"""
		입력받은 hsl값을 어두운 쪽으로 이동시키는것
		bright = [100,100], sharp = [50,100], graish = [100,0], dark = [0,0], black = [50, 0]
		"""
		h, s, l = input_hsl
		style = sharp = [50,100]

		delta_s = (style[0] - s) * strong_level
		delta_l = (style[1] - l) * strong_level

		changed_s = s + delta_s
		changed_l = l + delta_l
		return [h, changed_s, changed_l]

	def check_close_excel_56_color_no_for_scolor(self, input_scolor):
		rgb_value = self.change_scolor_to_rgb(input_scolor)
		result = self.check_close_excel_56_color_no_for_rgb(rgb_value)
		return result

	def check_close_excel_56_color_no_for_rgb(self, input_rgb):
		# 입력으로 들어오는 RGB값중에서 엑셀의 56가지 기본색상의 RGB값과 가장 가까운값을 찾아내는것
		result = 0
		short_length = 255 * 255 * 255
		var_56_rgb = self.var["dic_colorindex_rgblist"]

		for excel_color_no in var_56_rgb.keys():
			excel_rgb = var_56_rgb[excel_color_no]
			differ = self.distance_two_3d_point(input_rgb, excel_rgb)
			if short_length > differ:
				short_length = differ
				result = excel_color_no
		return result

	def distance_two_3d_point(self, input_1, input_2):
		# 3 차원의 거리를 기준으로 RGB 값의 차이를 계산하는 것
		dist = math.sqrt(
			math.pow((input_1[0]-input_2[0]), 2) + math.pow((input_1[1]- input_2[1]), 2) + math.pow((input_1[2]- input_2[2]), 2))
		return dist

	def check_close_excel_color_no(self, input_rgb):
		# 입력 R6B 값중에서 엑셀의 56 가지 기본색상의 R6B 값과 가장 가까운값을 찾아내는것
		input_rgb = self.change_scolor_to_rgb(input_rgb)
		result_rgbint = 255 * 255 * 255
		result_color_no = 2

		var_56_rgb = self.var["dic_colorindex_rgblist"]
		for excel_color_no in var_56_rgb.keys():
			new_color_no = excel_color_no
			excel_rgb = var_56_rgb[excel_color_no]
			new_rgbint = self.distance_two_3d_point(input_rgb, excel_rgb)
			print(input_rgb, excel_rgb, new_rgbint)

			if min(new_rgbint, result_rgbint) ==  new_rgbint:
				result_rgbint = new_rgbint
				result_color_no = excel_color_no
		return result_color_no


