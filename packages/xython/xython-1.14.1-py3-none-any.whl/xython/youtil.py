# -*- coding: utf-8 -*-
import shutil  # 내장모듈
import pickle  # 내장모듈
import inspect  # 내장모듈
import re  # 내장모듈
import os  # 내장모듈
import random  # 내장모듈
import collections  # 내장모듈
import sys  # 내장모듈
from difflib import SequenceMatcher  # 내장모듈

import basic_data  # xython 모듈

class youtil():
	"""
	여러가지 사무용에 사용할 만한 메소드들을 만들어 놓은것이며,
	좀더 특이한 것은 youtil2로 만들어서 사용할 예정입니다 
	"""

	def __init__(self):
		self.base_data = basic_data.basic_data()
		self.var = self.base_data.vars
		self.var_youtil = {}  # youtil에서 공통으로 사용할 변수들을 설정하는 것

	def add_serial_value(self, input_list2d, start_no=1, special_char=""):
		"""
		2 차원값의 값의 제일 처음값에만 순서가있는 값을 넣기
		값의 맨앞에 1), 2), 3)과같은 순서의 값을 넣고 싶을때
		"""
		for x in range(len(input_list2d)):
			if not start_no == "":
				add_value = str(start_no + x) + special_char
			else:
				add_value = special_char
			input_list2d[x][0] = add_value + input_list2d[x][0]
		return input_list2d

	def append_input_value_at_each_list1d_in_list2d(self, input_list2d, input_value):
		"""
		같은 항목으로 되어있는 자료를 제일 처음의 자료를 기준으로 합치는것
		2차원 리스트의 모든 자료끝에 값 추가하기
		"""
		result = []
		for list1d in input_list2d:
			result.append(list1d.append(input_value))
		return result

	def append_input_value_in_list2d(self, input_list2d, input_value):
		"""
		같은 항목으로 되어있는 자료를 제일 처음의 자료를 기준으로 합치는것
		2차원 리스트의 모든 자료끝에 값 추가하기
		"""
		result = []
		for list1d in input_list2d:
			result.append(list1d.append(input_value))
		return result

	def change_binary_to_int(self, bits):
		"""
		0과 1의 바이너리를 숫자로 만들어 주는것
		"""
		return int(bits, 2)

	def change_binary_to_string(self, bits):
		"""
		0과 1의 바이너리를 문자로 만들어 주는것
		"""
		return ''.join([chr(int(i, 2)) for i in bits])

	def change_10jinsu_to_base_letter_jinsu(self, input_num, show_letter="가나다라마바사아자차카타파하"):
		"""
		10진수값을 내가원하는 형식으로 변경하는것
		기본형을 예로들면 14진수이면서, 표현된,모양은 "0123456789abcd"가
		아니고 "가나다라마바사아자차카타파하"로 표현되는것
		"""
		jinsu = int(len(show_letter))
		q, r = divmod(input_num, jinsu)
		if q == 0:
			return show_letter[r]
		else:
			return self.change_10jinsu_to_base_letter_jinsu(q) + show_letter[r]

	def change_10jinsu_to_njinsu(self, input_num, jinsu=10):
		"""
		10진수값을 34진수까지의 진수형태로 변환
		진수값을 바꾸면 다른 진수형태로 변경된다
		"""
		base_letter = "0123456789abcdefghijklmnopqrstuvwxyz"
		q, r = divmod(input_num, jinsu)
		if q == 0:
			return base_letter[r]
		else:
			return self.change_10jinsu_to_njinsu(q, jinsu) + base_letter[r]

	def change_alpha_to_jamo(self, input_alpha_list):
		"""
		알파벳으로 바꾼 자음과 모음을 다시 자음과 모음으로 바꾸는 것
		"""
		changed_value = input_alpha_list
		data_set = self.var["eng_vs_jamo_list"]
		for one_list in data_set:
			for one_data in one_list:
				changed_value = changed_value.replace(one_data[0], one_data[1])
		result = changed_value.split("_")[:-1]
		# 자모를 한글로 만드는 방법
		return result

	def change_alpha_to_jamo_old(self, input_alpha_list):
		"""
		알파벳을 한글의 자음이나 모음으로 변경
		"""
		import jfinder
		jf = jfinder.jfinder()
		words = str(input_alpha_list).replace("y", "")
		words = str(input_alpha_list).split("z")
		# print(input_alpha_list, words)
		result = []
		sql = "[o-x]+"
		for letter in words[:-1]:
			temp = []
			dd = jf.search_all_by_jfsql(sql, letter)
			jamo_1 = letter[0:dd[0][1]]
			jamo_1_changed = self.var["eng_vs_jamo"][jamo_1]
			jamo_2 = letter[dd[0][1]: dd[0][2]]
			jamo_2_changed = self.var["eng_vs_jamo"][jamo_2]
			jamo_3 = letter[dd[0][2]:]
			if jamo_3:
				jamo_3_changed = self.var["eng_vs_jamo"][jamo_3]
			else:
				jamo_3_changed = ""
			temp = [jamo_1_changed, jamo_2_changed, jamo_3_changed]
			result.append(temp)
		return result

	def change_alpha_to_korean(self, input_alpha):
		"""
		한글을 자음과 모음으로 분리해서, 알파벳으로 변경하는 것
		알파벳으로 바꾸면, 영문의 문자열 다루는 것을 사용할수도 있을것 같아 만들어 보았으며
		동시에 자음과 모음을 한번에 바꿀수있게 되는 것이다
		박 ==> ["ㅂ", "ㅏ", "ㄱ"] => "abc"
		이렇게 자음과 모음으로 구분된영어단어로 바뀌는 것이다
		자음과모음의 연결로도 가능하는데, 문제는 받침이 없는 경우와 space의 구분이 어렵다는 것이다
		"""

		result = self.change_alpha_to_jamo(input_alpha)
		return result

	def change_base_letter_jinsu_to_10jinsu(self, input_num, show_letter="가나다라마바사아자차카타파하"):
		"""
		입력형식의 값을 10진수값으로 변경하는것
		10진수값을 내가원하는 형식으로 변경하는것
		기본형을 예로들면 14진수이면서, "가나다라마바사아자차카타파하"로 표현되는것
		"""
		new_dic = {}
		for no, one_value in enumerate(show_letter):
			new_dic[one_value] = no

		total = 0
		checked_input_num = reversed(input_num)
		for no, one in enumerate(checked_input_num):
			total = total + len(show_letter) ** (no) * new_dic[one]
		return total

	def change_file_to_list_by_def(self, filename):
		"""
		화일을 넣으면 def를 기준으로 리스트를 만드는것
		"""
		result = {}
		def_text = ""
		def_name = ""
		f = open(filename, "r", encoding="UTF8")
		lines = f.readlines()
		for one_text in lines:
			if str(one_text).strip()[0:3] == "def":
				if not def_name == "":
					result[def_name] = def_text
				def_name = str(one_text).strip()[3:].split("(")[0]
				def_text = def_text + one_text
		return result

	def change_filename(self, old_path, new_path):
		"""
		화일이름 변경
		"""
		old_path = self.check_filepath(old_path)
		new_path = self.check_filepath(new_path)
		os.rename(old_path, new_path)

	def change_folder_name(self, old_path, new_path):
		"""
		폴더이름 변경
		"""
		os.rename(old_path, new_path)

	def change_jamo_to_alpha(self, input_jamo_list):
		"""
		한글의 자음과 모음의 한글자를 알파벳으로 바꾸는것
		"""
		result = ""
		for one_list in input_jamo_list:
			for jamo in one_list:
				eng_one = self.var["jamo_vs_eng"][jamo]
				result = result + eng_one
			result = result + "z"
		return result

	def change_jamo_to_korea(self, input_jamo_list):
		"""
		한글의 자음과 모음을 한글의 글자로 바꾸는것
		"""
		result = ""
		for one_list in input_jamo_list:
			for jamo in one_list:
				eng_one = self.var["jamo_vs_eng"][jamo]
				result = result + eng_one
			result = result + "z"
		return result

	def change_jamo_to_korean(self, input_list):
		"""
		한글을 자음과 모음으로 분리해서, 알파벳으로 변경하는 것
		"""
		result = self.change_jamo_to_korea(input_list)
		return result

	def change_jamo_to_korean_1(self, input_jamo_list):
		"""
		모든 한글은 유니코드에 U+AC00(가)부터 U+D7A3(힣)까지 사전순으로 올라가 있읍니다
		초성 19자 : ㄱ,ㄲ,ㄴ,ㄷ,ㄸ,ㄹ,ㅁ,ㅂ,ㅃ,ㅅ,ㅆ,ㅇ,ㅈ,ㅉ,ㅊ,ㅋ,ㅌ,ㅍ,ㅎ
		중성 21자 : ㅏ,ㅐ,ㅑ,ㅒ,ㅓ,ㅔ,ㅕ,ㅖ,ㅗ,ㅘ,ㅙ,ㅚ,ㅛ,ㅜ,ㅝ,ㅞ,ㅟ,ㅠ,ㅡ,ㅢ,ㅣ
		종성 28자 : (없음),ㄱ,ㄲ,ㄳ,ㄴ,ㄵ,ㄶ,ㄷ,ㄹ,ㄺ,ㄻ,ㄼ,ㄽ,ㄾ,ㄿ,ㅀ,ㅁ,ㅂ,ㅄ,ㅅ,ㅆ,ㅇ,ㅈ,ㅊ,ㅋ,ㅌ,ㅍ,ㅎ
		"""
		result = []
		for one_jamo in input_jamo_list:
			# 유니코드의 순서대로 번호를 붙인것에서 순서를 읽어온다
			chosung_no = self.var["list_자음_19"][one_jamo[0]]  # 초성
			joongsung_no = self.var["list_모음_21"][one_jamo[1]]  # 중성
			try:
				jongsung_no = self.var["list_받침_28"][one_jamo[2]]  # 종성
			except:
				jongsung_no = self.var["list_받침_28"][""]  # 종성

			# 한글이 시작되는 번호 44032번째부터 몇번째인지를 계산하는것
			unicode_no = chosung_no * 21 * 28 + joongsung_no * 28 + jongsung_no + 44032
			# print(one_jamo, " ==> unicode_no ==> ", unicode_no)
			result.append(chr(unicode_no))
		return result

	def change_korean_to_alpha(self, input_han):
		"""
		한글을 자음과 모음으로 분리해서, 알파벳으로 변경하는 것
		"""
		aa = self.split_jamo_in_korean(input_han)
		result = self.change_jamo_to_alpha(aa)
		return result

	def change_list1d_to_space_by_step(self, input_list, step, start=0):
		"""
		1차원의 자료중에서 원하는 순서째의 자료를 ""으로 만드는것
		"""
		if start != 0:
			result = input_list[0:start]
		else:
			result = []

		for num in range(start, len(input_list)):
			temp_value = input_list[num]
			if divmod(num, step)[1] == 0:
				temp_value = ""
			result.append(temp_value)

		return result

	def change_list1d_to_list2d(self, input_data):
		"""
		입력된 1차원 자료를 2차원으로 만드는 것
		입력자료는 리스트나 듀플이어야 한다
		"""
		if type(input_data[0]) == type([]) or type(input_data[0]) == type(()):
			# 2차원의 자료이므로 입력값 그대로를 돌려준다
			result = input_data
		else:
			# 1차원의 자료라는 뜻으로, 이것을 2차원으로 만들어 주는 것이다
			result = []
			for one in input_data:
				result.append([one])
		return result

	def change_list1d_to_list2d_by_step(self, input_list="", xy=""):
		"""
		입력값이 1차원과 2차원의 자료가 섞여 일을때
		2차원의 자료형태로 모두 같은 크기로 만들어 주는것
		"""
		temp_result = []
		x_len, y_len = xy
		list1_max_len = len(input_list)
		list2_max_len = y_len
		count = int(list1_max_len / x_len)

		# 2차원자료중 가장 큰것을 계산한다
		for one_value in input_list:
			if type(one_value) == type([]):
				list2_max_len = max(list2_max_len, len(one_value))

		for one_value in input_list:
			temp_list = one_value
			# 모든 항목을 리스트형태로 만든다
			if type(one_value) != type([]):
				temp_list = [one_value]

			# 최대길이에 맞도록 적은것은 ""으로 갯수를 채운다
			if list2_max_len - len(temp_list) > 0:
				temp_list.extend([""] * (list2_max_len - len(temp_list)))
			temp_result.append(temp_list)

		result = []
		for no in range(count):
			start = no * x_len
			end = start + x_len
			result.append(temp_result[start:end])

		return result

	def change_list1d_to_lower(self, input_list1d):
		"""
		모든 리스트의 자료를 소문자로 만드는것이다
		"""
		for index in range(len(input_list1d)):
			try:
				input_list1d[index] = (input_list1d[index]).lower()
			except:
				pass
		return input_list1d

	def change_list1d_to_text_with_chainword(self, input_list, chain_word=" ,"):
		"""
		리스트 자료들을 중간문자를 추가하여 하나의 문자열로 만드는 것,
		“aa, bbb, ccc” 이런 식으로 만드는 방법이다
		리스트 자료들을 중간에 문자를 추가하여 한줄의 문자로 만드는 것
		입력형태 : ["aa", "bb","ccc"]
		출력형태 : “aa, bbb, ccc”
		"""
		result = ""
		for one_word in input_list:
			result = result + str(one_word) + str(chain_word)

		return result[:-len(chain_word)]

	def change_list1d_to_upper(self, input_list1d):
		"""
		1차원자료의 모든 내용물을 대문자로 만들어 주는 것이다
		"""
		for index in range(len(input_list1d)):
			try:
				input_list1d[index] = (input_list1d[index]).upper()
			except:
				pass
		return input_list1d

	def change_list2d_by_index(self, input_list2d, input_no_list):
		"""
		input_no_list.sort()
		input_no_list.reverse()
		"""
		for before, after in input_no_list:
			for no in range(len(input_list2d)):
				value1 = input_list2d[no][before]
				value2 = input_list2d[no][after]
				input_list2d[no][before] = value2
				input_list2d[no][after] = value1
		return input_list2d

	def change_list2d_to_dic(self, list_2d, list_title):
		"""
		2차원리스트를 사전형식으로 만드는 것
		제목과 연결해서 사전을 만들어서 다음에 편하게 쓰고 넣을수있도록 만들려고 한다
		"""
		result = []
		for one in list_2d:
			my_dic = {}
			for no in range(len(list_title)):
				my_dic[list_title[no]] = one[no]
			result.append(my_dic)
		return result

	def change_list2d_to_list1d(self, input_data):
		"""
		2차원의 list를 1차원으로 만들어 주는것
		항목 : ['항목1', '기본값1', '설명', {'입력형태1':'설명1', '입력형태2':'설명1',.... }]
		결과 ['항목1', '기본값1', '설명', '입력형태1:설명1', '입력형태2:설명1',.... }]
		위 형태의 자료를 한줄로 만들기위해 자료를 변경한다
		"""
		result = []
		for one_data in input_data:
			if type(one_data) == type({}):
				for key in list(one_data.Keys()):
					value = str(key) + " : " + str(one_data[key])
					result.append(value)
			elif type(one_data) == type(()) or type(one_data) == type([]) or type(one_data) == type(set()):
				for value in one_data:
					result.append(value)
			else:
				result.append(one_data)
		return result

	def change_list2d_to_samelen_list2d(self, input_data):
		"""
		길이가 다른 2dlist의 내부 값들을 길이가 같게 만들어주는 것이다
		가변적인 2차원배열을 최대크기로 모두 같이 만들어 준다
		"""
		result = []
		max_len = max(len(row) for row in input_data)
		for list_x in input_data:
			temp = list_x
			for no in range(len(list_x), max_len):
				temp.append("")
			result.append(temp)
		return result

	def change_list2d_to_set_item(self, input_set, input_list2d):
		"""
		2차원 리스트의 항목들을 set자료형으로 바꾸는 것
		input_list = [["변경전자료1", "변경후자료2"], ["변경전자료11", "변경후자료22"], ]

		"""
		for list_1d in input_list2d:
			input_set.discard(list_1d[0])
			input_set.add(list_1d[1])
		return input_set

	def change_multi_empty_lines_to_one_line_in_file(self, filename):
		"""
		화일을 읽어 내려가다가 2줄이상의 띄어쓰기가 된것을 하나만 남기는것
		텍스트로 저장된것을 사용하다가 필요해서 만듦
		"""
		self.delete_over2_emptyline_in_file(filename)

	def change_njinsu_to_10jinsu(self, input_num, input_jinsu=10):
		"""
		입력형식의 값을 10진수값으로 변경하는것
		"""
		original_letter = "0123456789abcdefghijklmnopqrstuvwxyz"
		base_letter = original_letter[0:input_jinsu]
		new_dic = {}
		for no, one_value in enumerate(base_letter):
			new_dic[one_value] = no
		total = 0
		checked_input_num = reversed(input_num)
		for no, one in enumerate(checked_input_num):
			total = total + len(base_letter) ** (no) * new_dic[one]
		return total

	def change_num_to_1000comma_num(self, input_num):
		"""
		입력된 숫자를 1000단위로 콤마를 넣는것
		"""
		temp = str(input_num).split(".")
		total_len = len(temp[0])
		result = ""
		for num in range(total_len):
			one_num = temp[0][- num - 1]
			if num % 3 == 2:
				result = "," + one_num + result
			else:
				result = one_num + result
		if len(temp) > 1:
			result = result + "." + str(temp[1])
		return result

	def change_number_to_tel_style(self, input_value):
		"""
		전화번호나 핸드폰 번호 스타일을 바꿔주는것
		전화번호를 21345678 =>02-134-5678 로 변경하는 것
		"""
		result = input_value
		value = str(int(input_value))
		if len(value) == 8 and value[0] == "2":
			# 22345678 => 02-234-5678
			result = "0" + value[0:1] + "-" + value[1:4] + "-" + value[4:]
		elif len(value) == 9:
			if value[0:2] == "2":
				# 223456789 => 02-2345-6789
				result = "0" + value[0:1] + "-" + value[1:5] + "-" + value[5:]
			elif value[0:2] == "11":
				# 113456789 => 011-345-6789
				result = "0" + value[0:2] + "-" + value[2:5] + "-" + value[5:]
			else:
				# 523456789 => 052-345-6789
				result = "0" + value[0:2] + "-" + value[2:5] + "-" + value[5:]
		elif len(value) == 10:
			# 5234567890 => 052-3456-7890
			# 1034567890 => 010-3456-7890
			result = "0" + value[0:2] + "-" + value[2:6] + "-" + value[6:]
		return result

	def change_python_file_to_list_data(self, filename):
		"""
		python 으로만든 화일을 읽어서 함수이름과 입력변수를 알아내기 위한것
		"""
		result = []
		file_pointer = open(filename, 'r', encoding='utf-8')  # 텍스트 읽어오기
		lines_list = file_pointer.readlines()  # 한번에 다 읽기
		for one_value in lines_list:
			changed_value = one_value.strip()
			if changed_value.startswith("def "):
				var_dic = {}
				split_1 = changed_value[3:].split("(")
				# 함수이름을 찾은것
				func_name = split_1[0].strip()
				if len(split_1) > 1:
					# 여러변수들을 ,로 분리하는것
					element_text = split_1[1].strip()
					element_text = element_text.replace("):", "")
					# print(element_text)
					old = ""
					flag_d = 0
					flag_dic = 0
					flag_l = 0
					flag_t = 0

					temp = []
					for one in element_text:
						if one == "=" and flag_d == 0 and flag_l == 0 and flag_t == 0 and flag_dic == 0:
							temp.append(old.strip())
							old = ""
						elif one == "," and flag_d == 0 and flag_l == 0 and flag_t == 0 and flag_dic == 0:
							if old == "''" or old == '""':
								old = ""
							temp.append(old.strip())
							old = ""
							if divmod(len(temp), 2)[1] == 1:
								temp.append("")
						elif one == "'" or one == '"':
							flag_d = not flag_d
						elif one == "[" or one == ']':
							flag_t = not flag_t
							old = old + one
						elif one == "(" or one == ')':
							flag_t = not flag_t
							old = old + one
						elif one == "(" or one == ')':
							flag_dic = not flag_dic
							old = old + one
						else:
							old = old + one
					temp.append(old.strip())
				result.append([func_name, temp])
		return result

	def change_python_file_to_sorted_by_def(self, filename):
		"""
		python으로만든 화일을 읽어서 def를 기준으로 정렬해서 돌려주는 것
		1. 프린트해서 나타냄
		2. 화일로 정렬된것을 만듦
		3. 리스트형태로 돌려주는것
		"""
		file_pointer = open(filename, 'r', encoding='utf-8')  # 텍스트 읽어오기
		file_list = file_pointer.readlines()  # 한번에 다 읽기

		all_text = ""
		temp = []
		result = {}
		title = "000"
		for one_line_text in file_list:
			# def로 시작이 되는지 알아 내는것
			if str(one_line_text).strip()[0:3] == "def" and str(one_line_text).strip()[-1] == ":":
				result[title] = temp  # def나오기 전까지의 자료를 저장합니다
				temp = []
				title = str(one_line_text).strip()  # 사전의 key를 def의 이름으로 만드는 것이다
			temp.append(one_line_text)
		result[title] = temp

		sorted_keys = list(result.keys())
		sorted_keys.sort()  # key인 제목을 기준으로 정렬을 하도록 만든것
		write_file = open("output_output_33.txt", 'w', encoding='utf-8')  # 텍스트 읽어오기

		for one_key in sorted_keys:
			for one_line in result[one_key]:
				one_line = one_line.replace("\n", "")
				print(one_line)  # 별도로 화일로 만들지 않고, 터미널에 나타나는것을 복사해서 사용하는 방법으로 만듦
				all_text = all_text + one_line
				write_file.write(one_line + "\n")
		write_file.close()
		return result

	def change_set_item_by_list(self, input_set, input_list2d):
		"""
		input_list = [["변경전자료1", "변경후자료2"], ["변경전자료11", "변경후자료22"], ]
		"""
		for list_1d in input_list2d:
			input_set.discard(list_1d[0])
			input_set.add(list_1d[1])
		return input_set

	def change_xylist_to_yxlist(self, input_list2d="입력필요"):
		"""
		trans_list( input_list2d="입력필요")
		2차원자료를 행과열을 바꿔서 만드는것
		단, 길이가 같아야 한다
		"""
		checked_input_list2d = self.change_list2d_to_samelen_list2d(input_list2d)
		result = [list(x) for x in zip(*checked_input_list2d)]
		return result

	def check_col_name(self, col_name):
		"""
		각 제목으로 들어가는 글자에 대해서 변경해야 하는것을 변경하는 것이다
		커럼의제목으로 사용 못하는것을 제외
		"""
		for temp_01 in [[" ", "_"], ["(", "_"], [")", "_"], ["/", "_per_"], ["%", ""], ["'", ""], ['"', ""], ["$", ""],
		                ["__", "_"], ["__", "_"]]:
			col_name = col_name.replace(temp_01[0], temp_01[1])
		if col_name[-1] == "_": col_name = col_name[:-2]
		return col_name

	def check_filename(self, temp_title):
		"""
		화일의 제목으로 사용이 불가능한것을 제거한다
		"""
		for temp_01 in [[" ", "_"], ["(", "_"], [")", "_"], ["/", "_per_"], ["%", ""], ["'", ""], ['"', ""], ["$", ""],
		                ["__", "_"], ["__", "_"]]:
			temp_title = temp_title.replace(temp_01[0], temp_01[1])
		if temp_title[-1] == "_": temp_title = temp_title[:-2]
		return

	def check_filepath(self, file):
		"""
		입력자료가 폴더를 갖고있지 않으면 현재 폴더를 포함해서 돌려준다
		"""
		if len(file.split(".")) > 1:
			result = file
		else:
			cur_dir = self.read_current_path()
			result = cur_dir + "\\" + file
		return result

	def check_list_maxsize(self, list_2d_data):
		"""
		2차원 배열의 제일 큰 갯수를 확인한다
		"""
		max_length = max(len(row) for row in list_2d_data)

		an_array = [[1, 2], [3, 4, 5]]
		print("2차배열 요소의 최대 갯수는 ==>", self.check_list_maxsize(an_array))

		return max_length

	def check_price(self, input_price):
		"""
		백만원단위, 전만원단위, 억단위로 구분
		"""
		input_price = int(input_price)
		if input_price > 100000000:
			result = str('{:.If}'.format(input_price / 100000000)) + "억원"
		elif input_price > 10000000:
			result = str('{: .0f}'.format(input_price / 1000000)) + "백만원"
		elif input_price > 1000000:
			result = str('{:.If}'.format(input_price / 1000000)) + "백만원"
		return result

	def copy_file(self, old_path, new_path, meta=""):
		"""
		화일복사
		"""
		old_path = self.check_filepath(old_path)
		new_path = self.check_filepath(new_path)
		if meta == "":
			shutil.copy(old_path, new_path)
		else:
			shutil.copy2(old_path, new_path)

	def copy_folder(self, old_path, new_path):
		"""
		폴더복사
		"""
		shutil.copy(old_path, new_path)

	def count_function_num_in_python_file(self, python_file_list, path=""):
		"""
		원하는 python화일안에 몇개의 def로 정의된 메소드가 있는지 확인하는 것이다
		"""
		result = []
		num = 0
		for one in python_file_list:
			aaa = self.change_python_file_to_sorted_by_def(path+one)
			num = num + len(aaa)
			result.append([one, len(aaa)])
		result.append(["총갯수는 ===>", num])
		return result

	def count_same_value_for_ordered_list(self, input_list):
		"""
		2개이상 반복되는것중 높은 갯수 기준으로 돌려주는것
		"""
		result_dic = {}
		# 리스트안의 자료가 몇번나오는지 갯수를 센후에
		# 1번이상의 자료만 남기고 다 삭제하는것
		for one in input_list:
			if one in result_dic.keys():
				result_dic[one] = result_dic[one] + 1
			else:
				result_dic[one] = 1

		# 1번이상의 자료만 남기고 다 삭제하는것
		for one in list(result_dic.keys()):
			if result_dic[one] == 1:
				del result_dic[one]

		# 사전자료를 2차원리스트로 만든것
		new_list = []
		for key, val in result_dic.items():
			new_list.append([key, val])

		# 사전자료를 2차원리스트로 만든것을 역순으로 정렬한것
		new_list = sorted(new_list, key=lambda x: x[1], reverse=True)
		return new_list

	def data_make_name_list(self, input_no=5):
		"""
		입력한 갯수만큼 이름의 갯수를 만들어 주는것
		"""
		sung = "김이박최정강조윤장"
		name = "가나다라마바사아자차카"
		last = "진원일이삼사오구원송국한"
		if input_no > len(sung) * len(name) * len(last) / 2:
			result = []
			pass
		else:
			total_name = set()
			num = 0
			while True:
				one_sung = random.choice(sung)
				one_name = random.choice(name)
				one_last = random.choice(last)
				new_name = one_sung + one_name + one_last
				total_name.add(new_name)
				num = num + 1
				if len(total_name) == input_no:
					print(input_no, num)
					break
			result = list(total_name)
		return result

	def delete_set_item_as_same_list_data(self, input_set, input_list):
		"""
		list의 항목으로 들어간것을 하나씩 꺼내어서
		set안에 같은것이 있으면 지운다
		"""
		for one in input_list:
			input_set.remove(one)
		return input_set


	def delete_set_item_same_with_input_list(self, input_set, input_list):
		"""
		list의 항목으로 들어간것을 하나씩 꺼내어서
		set안에 같은것이 있으면 지운다
		"""
		for one in input_list:
			input_set.remove(one)
		return input_set

	def delete_all_explanation_in_input_text(self, input_text):
		"""
		넘어온 text 에서 주석으로 사용되는 것들을 지우는것
		"""
		input_text = re.sub(re.compile(r"[\s]*#.*[\n]"), "\n", input_text)
		input_text = re.sub(re.compile(r"[\s]*''',*?'''", re.DOTALL | re.MULTILINE), "", input_text)
		input_text = re.sub(re.compile(r'[\s]*""".*?"""', re.DOTALL | re.MULTILINE), "", input_text)
		input_text = re.sub(re.compile(r"[\n][\s]*?[\n]"), "\n", input_text)
		return input_text

	def delete_contineous_same_data_in_list1d(self, input_datas):
		"""
		입력된 자료중에서 연속으로 같은값만 나오면 삭제하는 것이다
		"""
		if len(input_datas) == 0:
			pass
		else:
			a = 0
			while a != len(input_datas) - 1:
				if input_datas[a] == input_datas[a + 1]: input_datas[a] = []
				a = a + 1
		return input_datas

	def delete_continious_same_data(self, input_list):
		"""
		연속된 같은 자료만 지우는 것
		"""
		result = []
		for no in range(len(input_list) - 1):
			if input_list[no] == input_list[no + 1]:
				pass
			else:
				result.append(input_list[no])
		return result

	def delete_empty_value_in_list(self, input_list, condition=["", None, [], ()]):
		"""
		넘어온 리스트 형태의 자료중 조건에 맞는것이 있으면 제거하는 것
		입력형태 : ["aaa", "", None, "", "bbb"], [["aaa", "", None, "", "bbb"],"werw", 31231, [], ["aaa", "", None, "", "bbb"]]
		출력형태 : ["aaa", "bbb"], [['aaa', 'bbb'], 'werw', 31231, [], ['aaa', 'bbb']]
		"""
		for x in range(len(input_list) - 1, -1, -1):
			if input_list[x] in condition:
				del (input_list[x])
			else:
				if type(input_list[x]) == type([]):
					for y in range(len(input_list[x]) - 1, -1, -1):
						if input_list[x][y] in condition:
							del (input_list[x][y])
				else:
					if input_list[x] in condition:
						del (input_list[x])
		return input_list

	def delete_empty_line(self, input_list2d):
		"""
		가로나 세로열을 기준으로 값이 없는것을 삭제하기
		입력으로 들어온 2차원의 자료중에서, 가로행이 완전히 빈것을 삭제하는 기능
		"""
		base_no = len(input_list2d[0])
		result = []
		for list_1d in input_list2d:
			check_no = 0
			for value in list_1d:
				if value in [[], (), "", None]:
					check_no = check_no + 1
			if check_no != base_no:
				result.append(list_1d)
		return result

	def delete_empty_yline(self, input_list2d):
		"""
		입력으로 들어온 2차원의 자료중에서, 세로행이 처음부터 끝까지 빈Y열을 삭제하는 기능
		"""
		changed_list_2d = self.change_xylist_to_yxlist(input_list2d)
		temp = self.delete_empty_line(changed_list_2d)
		result = self.change_xylist_to_yxlist(temp)
		return result

	def delete_file(self, old_path):
		"""
		화일삭제
		"""
		old_path = self.check_filepath(old_path)
		os.remove(old_path)

	def delete_folder(self, old_dir, empty="no"):
		"""
		폴더삭제
		폴더안에 자료가 있어도 삭제
		"""
		if empty == "no":
			shutil.rmtree(old_dir)
		else:
			os.rmdir(old_dir)

	def delete_line_in_list2d_by_index(self, input_list2d, no_list):
		"""
		2차원자료를 기준으로 index번호를 기준으로 삭제하는것
		입력형태 : 2차원리스트, [2,5,7]
		"""
		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_list2d)):
				del input_list2d[x][one]
		return input_list2d

	def delete_list1d_by_even_no(self, data):
		"""
		홀수의 자료만 삭제
		"""
		result = []
		for no in range(len(data)):
			if divmod(no, 2)[1] != 1:
				result.append(data[no])
		return result

	def delete_list1d_by_odd_no(self, data):
		"""
		짝수의 자료만 삭제
		"""
		result = []
		for no in range(len(data)):
			if divmod(no, 2)[1] != 0:
				result.append(data[no])
		return result

	def delete_list2d_by_index(self, input_list2d, no_list):
		"""
		2차원 자료에서
		원하는 순서들의 자료를 삭제하는 것
		입력형태 : 2차원리스트, [2,5,7]
		"""
		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_list2d)):
				del input_list2d[x][one]
		return input_list2d

	def delete_over2_emptyline_in_file(self, filename):
		"""
		화일을 읽어 내려가다가 2줄이상의 띄어쓰기가 된것을 하나만 남기는것
		텍스트로 저장된것을 사용하다가 필요해서 만듦
		"""
		f = open(filename, 'r', encoding='UTF8')
		lines = f.readlines()
		num = 0
		result = ""
		for one_line in lines:
			if one_line == "\n":
				num = num + 1
				if num == 1:
					result = result + str(one_line)
				elif num > 1:
					# print("2줄발견")
					pass
			else:
				num = 0
				result = result + str(one_line)
		return result

	def delete_same_value_in_list2d_by_index(self, input_list2d, base_index):
		"""
		2차원자료중에서 몇번째의 자료가 같은것만 삭제하는것
		"""
		waste_letters = [" ", ',', '.', '"', "'", ',', '?', '-']
		result = []
		only_one = set()
		for one_list in input_list2d:
			new_value = str(one_list[base_index])
			for one in waste_letters:
				new_value = new_value.replace(one, "")

			if new_value in only_one:
				print("같은것 찾음")
			else:
				result.append(one_list)
				only_one.add(new_value)
		return result

	def delete_same_value_in_list1d(self, input_datas, status=0):
		"""
		입력자료에서 같은것만 삭제
		"""
		if status == 0:
			result = []
			# 계속해서 pop으로 하나씩 없애므로 하나도 없으면 그만 실행한다
			while len(input_datas) != 0:
				gijun = input_datas.pop()
				sjpark = 0
				result.append(gijun)
				for number in range(len(input_datas)):
					if input_datas[int(number)] == []:  # 빈자료일때는 그냥 통과한다
						pass
					if input_datas[int(number)] == gijun:  # 자료가 같은것이 있으면 []으로 변경한다
						sjpark = sjpark + 1
						input_datas[int(number)] = []
			else:
				# 중복된것중에서 아무것도없는 []마저 없애는 것이다. 위의 only_one을 이용하여 사용한다
				# 같은것중에서 하나만 남기고 나머지는 []으로 고친다
				# 이것은 연속된 자료만 기준으로 삭제를 하는 것입니다
				# 만약 연속이 되지않은 같은자료는 삭제가 되지를 않읍니다
				result = list(set(input_datas))
				for a in range(len(result) - 1, 0, -1):
					if result[a] == []:
						del result[int(a)]
		return result



	def delete_set_item_by_list(self, input_set, input_list):
		"""
		list의 항목으로 들어간것을 하나씩 꺼내어서
		set안에 같은것이 있으면 지운다
		"""
		for one in input_list:
			input_set.remove(one)
		return input_set

	def delete_all_char_except_num_eng_in_input_value(self, input_value):
		"""
		숫자와 영어만 남기는것, 나머지것은 다 삭제하는것
		result = []
		입력형태 :
		출력형태 :
		"""
		result = []
		for one_data in input_value:
			temp = ""
			for one in one_data:
				if str(one) in ' 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
					temp = temp + str(one)
			result.append(temp)
		return result

	def draw_as_triangle(self, xyxy, per=100, reverse=1, size=100):
		"""
		삼각형을 만드는것
		# 정삼각형
		# 정삼각형에서 오른쪽이나 왼쪽으로 얼마나 더 간것인지
		# 100이나 -100이면 직삼각형이다
		# 사각형은 왼쪽위에서 오른쪽 아래로 만들어 진다
		"""
		x1, y1, x2, y2 = xyxy
		width = x2 - x1
		height = y2 - y1
		lt = [x1, y1]  # left top
		lb = [x2, y1]  # left bottom
		rt = [x1, y1]  # right top
		rb = [x2, y2]  # right bottom
		tm = [x1, int(y1 + width / 2)]  # 윗쪽의 중간
		lm = [int(x1 + height / 2), y1]  # 윗쪽의 중간
		rm = [int(x1 + height / 2), y1]  # 윗쪽의 중간
		bm = [x2, int(y1 + width / 2)]  # 윗쪽의 중간
		center = [int(x1 + width / 2), int(y1 + height / 2)]

		result = [lb, rb, tm]
		return result

	def get_partial_list_by_index(self, input_list, position_list):
		"""
		리스트로 넘오온 자료를 원하는 열만 추출하는것
		"""
		result = []
		for one_list in input_list:
			temp = []
			for one in position_list:
				temp.append(one_list[one - 1])
			result.append(temp)
		return result

	def get_not_empty_value_in_list2d_by_index(self, input_list2d, index_no=4):
		"""
		index 번호의 Y열의 값이 빈것이 아닌것만 돌려주는 것
		"""
		result = []
		for index, one in enumerate(input_list2d):
			if one[index_no]:
				result.append(one)
		return result

	def get_same_value_in_list2d(self, input_lisd1d_1, input_lisd1d_2):
		"""
		2차원의 자료안에서 입력값이 같은것을 찾아내기
		"""
		result = []
		for one in input_lisd1d_1:
			if one in input_lisd1d_2:
				result.append(one)
		return result

	def get_list_1d_with_float_range(self, start, end, step):
		"""
		실수형으로 가능한 range 형태
		"""
		result = []
		value = start
		while value <= end:
			yield value
			value = step + value
			result.append(value)
		return result

	def get_all_doc_of_method_name_for_input_object(self, object):
		"""
		입력 : 원하는 객체
		출력 : 모든 객체의 메소드이름을 사전형식으로 doc를 갖고오는것
		"""
		result = {}
		aaa = self.get_all_method_name_with_argument_for_input_object(object)

		# 만들어진 자료를 정렬한다
		all_methods_name = list(aaa.keys())
		all_methods_name.sort()

		# 위에서 만들어진 자료를 기준으로 윗부분에 나타난 형식으로 만드는 것이다
		for method_name in all_methods_name:
			if not method_name.startswith("_"):
				exec(f"bbb = excel.{method_name}.__doc__")
				result[method_name]["manual"] = str(bbb)
		return result

	def get_all_help_of_method_name_for_input_object(self, input_object):
		"""
		객체를 주면 메소드의 help를 돌려 주는것
		"""
		result = {}
		for method_name in dir(input_object):
			temp = []
			# 이중언더 메소드는 제외시키는것
			if not method_name.startswith('__'):
				try:
					temp.append(method_name)
					temp.append(getattr(input_object, method_name).__doc__)
				except:
					pass
			result[method_name] = temp
		return result

	def get_all_method_name_for_input_object(self, object):
		"""
		원하는 객체를 넣으면, 객체의 함수와 각 함수의 인자를 사전형식으로 돌려준다
		"""
		result = []
		for obj_method in dir(object):
			result.append(obj_method)
		return result

	def get_all_properties_for_input_object(self, object):
		"""
		원하는 객체를 넣으면, 객체의 함수와 각 함수의 인자를 사전형식으로 돌려준다
		"""
		result = []
		#for obj_method in dir(object.__dict__):
		#	result.append(obj_method)

		for att in dir(object):
			#print(att, getattr(object, att))
			result.append(att)

		return result


	def get_all_method_name_for_input_object_except_dunder_methods(self, object):
		"""
		원하는 객체를 넣으면, 객체의 함수와 각 함수의 인자를 사전형식으로 돌려준다
		"""
		result = []
		for obj_method in dir(object):
			if obj_method.startswith("__"):
				pass
			else:
				result.append(obj_method)

		return result

	def get_all_method_name_with_argument_for_input_object(self, object):
		"""
		원하는 객체를 넣으면, 객체의 함수와 각 함수의 인자를 사전형식으로 돌려준다
		"""
		result = {}
		for obj_method in dir(object):
			try:
				method_data = inspect.signature(getattr(object, obj_method))
				dic_fun_var = {}
				if not obj_method.startswith("_"):
					for one in method_data.parameters:
						value_default = method_data.parameters[one].default
						value_data = str(method_data.parameters[one])

						if value_default == inspect._empty:
							dic_fun_var[value_data] = None
						else:
							value_key, value_value = value_data.split("=")
							if "remove" in obj_method:
								print(value_key, value_value)
							if value_value == "''" or value_value == '""':
								value_value = ''
							# 변수값중 ''가 들어간것이 없어져서, 아래의 것을 주석처리를 함
							# value_value = str(value_value).replace("'", "")
							# print(value_data, "키값==>", value_key, "입력값==>", value_value)
							dic_fun_var[str(value_key)] = value_value
						result[obj_method] = dic_fun_var

			except:
				pass
		return result

	def get_all_source_code_of_methods_for_input_object(self, input_obj):
		"""
		입력객체에 대해서, 메소드를 기준으로 소스코드를 읽어오는것
		"""
		result = {}
		for obj_method in dir(input_obj):
			if not obj_method.startswith("_"):
				try:
					exec(f"method_object = {input_obj}.{obj_method}")
					ddd = inspect.getsource(method_object)
					result[obj_method] = ddd
				except:
					pass
		return result

	def get_cho_sung_for_korean(self, input_kor):
		"""
		초성의 글자만 갖고오는것
		"""
		result = []
		for one in input_kor:
			try:
				aa = self.split_jamo_in_korean(one)
				result.append(aa[0][0])
			except:
				pass
		return result

	def get_file_list_from_directory(self, directory):
		"""
		입력폴더안의 화일들을 리스트형태로 돌려주는것
		"""
		result = os.listdir(directory)
		return result

	def get_jaum_xy_list(self, size=[1, 2], input_data="ㄱ"):
		"""
		자음의 xy값을 갖고온다
		"""
		x, y = size
		# x, y는 글자의 크기
		ja_01 = [["ㄱ"], [1, 1, 1, y], [1, y, x, y]]
		ja_02 = [["ㄴ"], [1, 1, x, 1], [x, 1, x, y]]
		ja_03 = [["ㄷ"], [1, y, 1, 1], [1, 1, x, 1], [x, 1, x, y]]
		ja_04 = [["ㄹ"], [1, 1, 1, y], [1, y, 0.5 * x, y], [0.5 * x, y, 0.5 * x, 1], [0.5 * x, 1, x, 1], [x, 1, x, y]]
		ja_05 = [["ㅁ"], [1, 1, 1, y], [1, y, x, y], [x, y, x, 1], [x, 1, 1, 1]]
		ja_06 = [["ㅂ"], [1, 1, x, 1], [x, 1, x, y], [x, y, 1, y], [0.5 * x, 1, 0.5 * x, y]]
		ja_07 = [["ㅅ"], [1, 0.5 * y, 0.3 * x, 0.5 * y], [0.3 * x, 0.5 * y, x, 1], [0.3 * x, 0.5 * y, x, y]]
		ja_08 = [["ㅇ"], [0.8 * x, 0.2 * y, 0.8 * x, 0.8 * y], [0.8 * x, 0.8 * y, 0.6 * x, y, ""],
		         [0.6 * x, y, 0.2 * x, y], [0.2 * x, y, 1, 0.8 * y, "/"], [1, 0.8 * y, 1, 0.2 * y],
		         [1, 0.2 * y, 0.2 * x, 1, ""], [0.2 * x, 1, 0.6 * x, 1], [0.6 * x, 1, 0.8 * x, 0.2 * y, "/"]]
		ja_09 = [["ㅈ"], [1, 1, 1, y], [1, 0.5 * y, 0.5 * x, 0.5 * y], [0.5 * x, 0.5 * y, x, 1, "/"],
		         [0.5 * x, 0.5 * y, x, y, ""]]
		ja_10 = [["ㅊ"], [0.2 * x, 0.5 * y, 1, 0.5 * y], [0.2 * x, 1, 0.2 * x, y], [0.2 * x, 0.5 * y, 0.4 * x, 0.5 * y],
		         [1, 0.5 * y, 0.5 * x, 0.5 * y], [0.5 * x, 0.5 * y, x, 1], [0.5 * x, 0.5 * y, x, y, ""]]
		ja_11 = [["ㅋ"], [1, 1, 1, y], [1, y, x, y], [0.5 * x, 1, 0.5 * x, y]]
		ja_12 = [["ㅌ"], [1, y, 1, 1], [1, 1, x, 1], [x, 1, x, y], [0.5 * x, 1, 0.5 * x, y]]
		ja_13 = [["ㅍ"], [1, 1, 1, y], [x, 1, x, y], [1, 0.2 * y, x, 0.2 * y], [1, 0.8 * y, x, 0.8 * y]]
		ja_14 = [["ㅎ"], [1, 0.5 * y, 0.2 * x, 0.5 * y], [0.2 * x, 1, 0.2 * x, y], [0.4 * x, 0.3 * y, 0.4 * x, 0.8 * y],
		         [0.4 * x, 0.8 * y, 0.6 * x, y], [0.6 * x, y, 0.8 * x, y], [0.8 * x, y, x, 0.8 * y],
		         [x, 0.8 * y, x, 0.3 * y], [x, 0.3 * y, 0.8 * x, 1], [0.8 * x, 1, 0.6 * x, 1],
		         [0.6 * x, 1, 0.4 * x, 0.3 * y]]
		ja_31 = [["ㄲ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, y, x, y], ]
		ja_32 = [["ㄸ"], [1, 1, 1, 0.4 * y], [1, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y],
		         [1, 0.7 * y, x, 0.7 * y], [x, 0.7 * y, x, y], ]
		ja_33 = [["ㅃ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [x, 0.4 * y, 1, 0.4 * y], [0.5 * x, 1, 0.5 * x, 0.4 * y],
		         [1, 0.7 * y, x, 0.7 * y], [x, 0.7 * y, x, y], [x, y, 1, y], [0.5 * x, 0.7 * y, 0.5 * x, y], ]
		ja_34 = [["ㅆ"], [1, 0.3 * y, 0.4 * x, 0.3 * y], [0.4 * x, 0.3 * y, x, 1], [0.4 * x, 0.3 * y, x, 0.5 * y],
		         [1, 0.8 * y, 0.4 * x, 0.8 * y], [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
		ja_35 = [["ㅉ"], [1, 1, 1, 0.5 * y], [1, 0.3 * y, 0.4 * x, 0.3 * y], [0.4 * x, 0.3 * y, x, 1],
		         [0.4 * x, 0.3 * y, x, 0.5 * y], [1, 0.6 * y, 1, y], [1, 0.8 * y, 0.4 * x, 0.8 * y],
		         [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
		ja_36 = [["ㄳ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, x, 0.4 * y], [1, 0.8 * y, 0.4 * x, 0.8 * y],
		         [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
		ja_37 = [["ㄵ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.6 * y, 1, y], [1, 0.8 * y, 0.4 * x, 0.8 * y],
		         [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
		ja_38 = [["ㄶ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [0.1 * x, 0.8 * y, 1, 0.8 * y],
		         [0.2 * x, 0.6 * y, 0.2 * x, y], [0.4 * x, 0.7 * y, 0.4 * x, 0.9 * y], [0.4 * x, 0.9 * y, 0.6 * x, y],
		         [0.6 * x, y, x, 0.9 * y], [x, 0.9 * y, x, 0.7 * y], [x, 0.7 * y, 0.8 * x, 0.6 * y],
		         [0.8 * x, 0.6 * y, 0.6 * x, 0.6 * y], [0.6 * x, 0.6 * y, 0.4 * x, 0.7 * y]]
		ja_39 = [["ㄺ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
		         [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, y, x, y], ]
		ja_40 = [["ㄻ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
		         [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, y, x, y], [x, y, x, 0.7 * y],
		         [x, 0.7 * y, 1, 0.7 * y], ]
		ja_41 = [["ㄼ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
		         [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, x, 0.7 * y], [x, 0.7 * y, x, y], [x, y, 1, y],
		         [0.5 * x, 0.7 * y, 0.5 * x, y], ]
		ja_42 = [["ㄽ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
		         [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.8 * y, 0.4 * x, 0.8 * y], [0.4 * x, 0.8 * y, x, 0.6 * y],
		         [0.4 * x, 0.8 * y, x, y], ]
		ja_43 = [["ㄾ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
		         [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, 0.7 * y, x, 0.7 * y],
		         [x, 0.7 * y, x, y], [0.5 * x, 0.7 * y, 0.5 * x, y], ]
		ja_44 = [["ㄿ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
		         [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.6 * y, 1, y], [x, 0.6 * y, x, y],
		         [1, 0.7 * y, x, 0.7 * y], [1, 0.9 * y, x, 0.9 * y], ]
		ja_45 = [["ㅀ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
		         [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [0.1 * x, 0.8 * y, 1, 0.8 * y], [0.2 * x, 0.6 * y, 0.2 * x, y],
		         [0.4 * x, 0.7 * y, 0.4 * x, 0.9 * y], [0.4 * x, 0.9 * y, 0.6 * x, y], [0.6 * x, y, x, 0.9 * y],
		         [x, 0.9 * y, x, 0.7 * y], [x, 0.7 * y, 0.8 * x, 0.6 * y], [0.8 * x, 0.6 * y, 0.6 * x, 0.6 * y],
		         [0.6 * x, 0.6 * y, 0.4 * x, 0.7 * y]]
		ja_46 = [["ㅄ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [x, 0.4 * y, 1, 0.4 * y], [0.5 * x, 1, 0.5 * x, 0.4 * y],
		         [1, 0.8 * y, 0.4 * x, 0.8 * y], [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]

		jamo1_dic = {"ㄱ": ja_01, "ㄴ": ja_02, "ㄷ": ja_03, "ㄹ": ja_04, "ㅁ": ja_05,
		             "ㅂ": ja_06, "ㅅ": ja_07, "ㅇ": ja_08, "ㅈ": ja_09, "ㅊ": ja_10,
		             "ㅋ": ja_11, "ㅌ": ja_12, "ㅍ": ja_13, "ㅎ": ja_14,
		             "ㄲ": ja_31, "ㄸ": ja_32, "ㅃ": ja_33, "ㅆ": ja_34, "ㅉ": ja_35,
		             "ㄳ": ja_36, "ㄵ": ja_37, "ㄶ": ja_38, "ㄺ": ja_39, "ㄻ": ja_40,
		             "ㄼ": ja_41, "ㄽ": ja_42, "ㄾ": ja_43, "ㄿ": ja_44, "ㅀ": ja_45, "ㅄ": ja_46,
		             }

		result = jamo1_dic[input_data]
		return result

	def get_max_length_for_list2d(self, input_list2d):
		"""
		2차원 배열의 제일 큰 갯수를 확인한다
		"""
		max_length = max(len(row) for row in input_list2d)
		return max_length

	def get_method_text_name_for_input_object(self, object):
		"""
		원하는 객체를 넣으면, 객체의 함수와 각 함수의 인자를 사전형식으로 돌려준다
		"""
		result = []
		for obj_method in dir(object)[:1]:
			aaa = inspect.getmembers(obj_method)
			print(aaa)
		return result

	def get_moum_xy_list(self, size=[1, 2], input_data="ㅏ"):
		"""
		모음을 엑셀에 나타내기 위한 좌표를 주는 것이다
		x, y는 글자의 크기
		"""
		x, y = size
		mo_01 = [["ㅏ"], [1, 0.6 * y, x, 0.6 * y],
		         [0.4 * x, 0.6 * y, 0.4 * x, 0.8 * y]]
		mo_02 = [["ㅑ"], [1, 0.6 * y, x, 0.6 * y],
		         [0.4 * x, 0.6 * y, 0.4 * x, 0.8 * y],
		         [0.6 * x, 0.6 * y, 0.6 * x, 0.8 * y]]
		mo_03 = [["ㅓ"], [1, 0.6 * y, x, 0.6 * y],
		         [0.4 * x, 0.4 * y, 0.4 * x, 0.6 * y]]
		mo_04 = [["ㅕ"], [1, 0.6 * y, x, 0.6 * y],
		         [0.4 * x, 0.4 * y, 0.4 * x, 0.6 * y],
		         [0.6 * x, 0.4 * y, 0.6 * x, 0.6 * y]]
		mo_10 = [["ㅣ"], [1, 0.6 * y, x, 0.6 * y]]
		mo_05 = [["ㅗ"], [x, 1, x, y],
		         [x, 0.5 * y, 0.8 * x, 0.5 * y]]
		mo_06 = [["ㅛ"], [x, 1, x, y],
		         [x, 0.3 * y, 0.8 * x, 0.3 * y],
		         [x, 0.7 * y, 0.8 * x, 0.7 * y]]
		mo_07 = [["ㅜ"], [1, 1, 1, y],
		         [1, 0.5 * y, 0.5 * x, 0.5 * y]]
		mo_08 = [["ㅠ"], [1, 1, 1, y],
		         [1, 0.3 * y, 0.8 * x, 0.3 * y],
		         [1, 0.7 * y, 0.8 * x, 0.7 * y]]
		mo_09 = [["ㅡ"], [0.5 * x, 1, 0.5 * x, y]]

		mo_21 = [["ㅐ"], [1, 0.6 * y, x, 0.6 * y],
		         [1, 0.8 * y, x, 0.8 * y],
		         [0.4 * x, 0.6 * y, 0.4 * x, 0.8 * y]]
		mo_22 = [["ㅒ"], [1, 0.6 * y, x, 0.6 * y],
		         [1, 0.8 * y, x, 0.8 * y],
		         [0.4 * x, 0.6 * y, 0.4 * x, 0.6 * y],
		         [0.6 * x, 0.8 * y, 0.6 * x, 0.8 * y]]
		mo_23 = [["ㅔ"], [1, 0.6 * y, x, 0.6 * y],
		         [1, 0.8 * y, x, 0.8 * y],
		         [0.4 * x, 0.4 * y, 0.4 * x, 0.6 * y]]
		mo_24 = [["ㅖ"], [1, 0.6 * y, x, 0.6 * y],
		         [1, 0.8 * y, x, 0.8 * y],
		         [0.4 * x, 0.4 * y, 0.4 * x, 0.6 * y],
		         [0.6 * x, 0.4 * y, 0.6 * x, 0.6 * y]]

		jamo2_dic = {
			"ㅏ": mo_01, "ㅑ": mo_02, "ㅓ": mo_03, "ㅕ": mo_04, "ㅗ": mo_05,
			"ㅛ": mo_06, "ㅜ": mo_07, "ㅠ": mo_08, "ㅡ": mo_09, "ㅣ": mo_10,
			"ㅐ": mo_21, "ㅒ": mo_22, "ㅔ": mo_23, "ㅖ": mo_24,
		}
		result = jamo2_dic[input_data]
		return result

	def get_one_line_as_searched_word_in_file(self, file_name="pcell.py", input_text="menu_dic["):
		"""
		화일안에서 원하는 단어가 들어간 줄을 리스트로 만들어서 돌려주는것
		메뉴를 만들 목적으로 한것
		"""
		aa = open(file_name, 'r', encoding="UTF-8")
		result = []
		for one in aa.readlines():
			if input_text in str(one).strip():
				# print(str(one).strip())
				result.append(str(one).strip())
		return result

	def get_random_data_set_on_base_letter(self, digit=2, total_no=1, letters="가나다라마바사아자차카타파하"):
		"""
		입력으로들어오는 것을 랜덤하여 갯수만큼 자료를 만드는것
		"""
		result = []
		for no in range(total_no):
			temp = ""
			for one in range(digit):
				number = random.choice(letters)
				temp = temp + str(number)
			result.append(temp)
		return result

	def get_random_number(self, digit=2, total_no=1):
		"""
		정수로된 원하는 자릿수의 랜덤한 갯수를 갖고오는것
		"""
		result = []
		for no in range(total_no):
			temp = ""
			for one in range(digit):
				number = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
				temp = temp + str(number)
			result.append(temp)
		return result

	def get_same_value_for_list2d(self, input_lisd2d_1, input_lisd2d_2, index_list=[1, 2]):
		"""
		2 차원의 자료들이 서로 같은것을 삭제하는 것인데,
		모두 같은것이 아니고, 일부분이 같은것을
		골라내는 기능을 만든 것이다
		"""
		semi_result_1 = {}
		for num, value in enumerate(input_lisd2d_1):
			temp_1 = []
			for one in index_list:
				temp_1.append(value[one])
				semi_result_1[num] = [temp_1, value]
		semi_result_2 = {}
		for num, value in enumerate(input_lisd2d_2):
			temp_2 = []
			for one in index_list:
				temp_2.append(value[one])
				semi_result_2[num] = [temp_2, value]
		result = []
		for key, value in semi_result_1.items():
			for key2, value2 in semi_result_2.items():
				if value[0] == value2[0]:
					if value[1] in result:
						pass
					else:
						result.append(value[1])
		return list(result)

	def get_same_value_list(self, input_list1d_1, input_list1d_2):
		"""
		기준값에서 1 차원의 같은 값을 찾는 것이다
		"""
		result = []
		for one in input_list1d_1:
			if one in input_list1d_2:
				result.append(one)
		return result

	def get_unique_function_between_two_python_file(self, file_a, file_b):
		"""
		두 파이썬 화일중에서 다른 함수만 갖고오는것
		"""
		a_file = self.change_file_to_list_by_def(file_a)
		b_file = self.change_file_to_list_by_def(file_b)
		a_file_keys = a_file.keys()
		b_file_keys = b_file.keys()
		unique_a = []
		for one_key in a_file_keys:
			if not one_key in b_file_keys:
				unique_a.append([a_file_keys])
		return unique_a

	def get_unique_random_data_set_on_base_letter(self, digit=2, total_no=1, letters="가나다라마바사아자차카타파하"):
		"""
		입력으로들어오는 것을 랜덤하여 갯수만큼 자료를 만드는것
		동일한것은 제외하는 조건으로 만드는 것이다
		"""
		unique = set()
		while True:
			if len(unique) >= total_no:
				result = list(unique)
				return result
			else:
				temp = ""
				for one in range(digit):
					number = random.choice(letters)
					temp = temp + str(number)
					unique.add(temp)

	def change_list2d_to_list1d_by_grouping_count(self, input_list2d, index_no=4):
		"""
		index번호를 기준으로 그룹화를 만드는 것
		"""
		result = []
		print(input_list2d)
		sorted_input_list2d = self.sort_list2d_by_index(input_list2d, index_no)
		print(sorted_input_list2d)
		check_value = sorted_input_list2d[0][index_no]
		temp = []
		for one_list in sorted_input_list2d:
			if one_list[index_no] == check_value:
				temp.append(one_list)
			else:
				result.append(temp)
				temp = [one_list]
				check_value = one_list[index_no]
		if temp:
			result.append(temp)
		return result

	def change_list32d_to_list1d_by_grouping_count(self, input_list3d, index_no=4):
		"""
		index번호를 기준으로 그룹화를 만드는 것
		"""
		result = []
		for input_list2d in input_list3d:
			sorted_input_list2d = self.sort_list2d_by_index(input_list2d, index_no)
			grouped_list3d = self.change_list2d_to_list1d_by_grouping_count(sorted_input_list2d, index_no)
			result = result + grouped_list3d
		return result

	def history(self):
		"""
		이화일의 변경 기록
		"""
		result = """
			"""
		return result

	def insert_input_data_in_list1d_by_step(self, input_list, insert_value, step):
		"""
		기존자료에 n번째마다 자료를 추가하는 기능
		raw_data = ['qweqw','qweqweqw','rterert','gdgdfgd',23,534534,'박상진']
		added_data = "new_data"
		step=3, 각 3번째 마다 자료를 추가한다면
		"""
		var_1, var_2 = divmod(len(input_list), int(step))
		for num in range(var_1, 0, -1):
			input_list.insert(num * int(step) - var_2 + 1, insert_value)
		return input_list

	def insert_line_in_list(self, data, number=1, input_data=[]):
		"""
		리스트에 일정한 간격으로 자료삽입
		"""
		total_number = len(data)
		dd = 0
		for a in range(len(data)):
			if a % number == 0 and a != 0:
				if total_number != a:
					data.insert(dd, input_data)
					dd = dd + 1
			dd = dd + 1
		return data

	def insert_list2d_blank_by_index(self, input_list2d, no_list):
		"""
		입력형태 : 2차원리스트, [2,5,7]
		"""
		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_list2d)):
				input_list2d[x].insert(int(one), "")
		return input_list2d

	def is_number(self, input_data):
		"""
		들어온 자료가 맞는지 확인하는것
		"""
		temp = self.is_number_only(input_data)
		if temp:
			result = True
		else:
			result = False
		return result
	def is_number_only(self, input_text):
		"""
		소슷점까지는 포함한것이다
		"""
		result = False
		temp = re.match("^[0-9.]+$", input_text)
		if temp: result = True

		return result

	def make_dic_for_2list(self, key_list, value_list):
		"""
		두개의 리스트를 받으면 사전으로 만들어 주는 코드
		"""
		result = dict(zip(key_list, value_list))
		return result

	def make_dic_with_count(self, input_text):
		"""
		갯수만큼의 문자열을 사전으로 만드는 것
		"""
		input_text = input_text.replace(" ", "")
		input_text = input_text.upper()
		result = {}
		for one_letter in input_text:
			if one_letter in list(result.keys()):
				result[one_letter] = result[one_letter] + 1
			else:
				result[one_letter] = 1
		return result

	def make_folder(self, input_folder_name):
		"""
		폴더 만들기
		"""
		os.mkdir(input_folder_name)

	def make_html_table(self, table_title_list, table_value_list):
		"""
		html용으로 사용되는 table을 만드는 것
		"""
		body_top = """
		수고합니다<br>
		<br>
		구매 요청건에 대하여 아래와 같이 TBE요청합니다"<br>
		<br>
		"""

		body_tail = """
		<br>
		-----------------------------------------------------------------------------------<br>
		롯데정밀화학 / 구매2팀 / 박상진 수석<br>
		06181 서울 강남구 테헤란로 534 글라스타워 27층<br>
		SangJin Park / Procurement 2 Team / Senior Manager<br>
		LOTTE Fine Chemical Co., LTD<br>
		27F, Glasstower Bldg., / 534, Teheran-ro, Gangnam-gu, Seoul, 06181, Korea<br>
		Tel	 : 82-2-6974-4539			   C.P	: 010-3334-0053<br>
		e-mail : sjp@lotte.net<br>
		<br>
		"""

		table_style = """
		<html>
		<style>
		body {
			  font-family:'Malgun Gothic';
			  font-size:10pt;
			}
		table {
			width: 70%;
			padding: 11px;
			font-family:'Malgun Gothic';
			font-size:10pt;
		  }
		  tr, td {
			border-bottom: 1px solid #444444;
			padding: 3px;
			text-align: center;
		  }
		  tr, th {
			padding: 13px;
			background-color: #bbdefb;
		  }
		  td {
			background-color: #e3f2fd;
		  }
			</style>
			<body>"""

		temp = table_style + body_top + "<table>"

		temp = temp + "<tr>"
		for x in range(len(table_title_list)):
			temp = temp + "<th>" + str(table_title_list[x]) + "</th>"
		temp = temp + "</tr>"

		for x in range(len(table_value_list)):
			temp = temp + "<tr>"
			for y in range(len(table_value_list[0])):
				temp = temp + "<td>" + str(table_value_list[x][y]) + "<br></td>"
			temp = temp + "</tr>"
		temp = temp + "</table>" + body_tail + "</body></html>"
		return temp

	def make_random_list(self, input_list, input_limit, input_times=1):
		"""
		입력된 자료를 랜덤으로 리스트를 만드는 것
		"""
		result_set = []
		if len(input_list) == 2:
			input_list = list(range(input_list[0], input_list[1]))
		for no in range(input_times):
			result = []
			for num in range(input_limit):
				dd = random.choice(input_list)
				result.append(dd)
				input_list.remove(dd)
			result_set.append(result)
		return result_set

	def make_serial_no(self, start_no=1, style="####"):
		"""
		1000으로 시작되는 연속된 번호를 만드는 것이다
		"""
		length = len(style)
		value = 10 ** (length - 1) + start_no
		return value

	def make_text_basic(self, input_value, total_len):
		"""
		f-string처럼 문자를 변경하는것
		"""
		result = ""
		if type(input_value) == type(123.45):
			result = self.make_text_for_float(input_value, total_len, 2, " ", "right", True)
		elif type(input_value) == type(123):
			result = self.make_text_for_integer(input_value, total_len, " ", "right", True)
		elif type(input_value) == type("123.45"):
			result = self.make_text_for_string(input_value, total_len, " ", "right")
		return result

	def make_text_file_for_input_text(self, file_full_name, input_text):
		"""
		텍스트자료를 화일로 저장하는것
		"""
		new_file = open(file_full_name, "w", encoding="UTF-8")
		for one_line in input_text:
			new_file.write(one_line)

	def make_text_for_float(self, input_value, big_digit, small_digit, fill_empty=" ", align="right", comma1000=True):
		"""
		f-string처럼 실수를 원하는 형태로 변경하는것
		"""
		if comma1000:
			changed_input_value = f"{round(float(input_value), small_digit):,}"
		else:
			changed_input_value = str(round(float(input_value), small_digit))

		repeat_no = big_digit - len(changed_input_value)

		repeat_char = fill_empty * (repeat_no)
		repeat_char_start = fill_empty * int(repeat_no / 2)
		repeat_char_end = fill_empty * int(repeat_no - int(repeat_no / 2))

		if align == "left":
			result = changed_input_value + repeat_char
		elif align == "right":
			result = repeat_char + changed_input_value
		elif align == "middle":
			result = repeat_char_start + changed_input_value + repeat_char_end
		else:
			result = repeat_char + changed_input_value
		return result

	def make_text_for_integer(self, input_value, big_digit, fill_empty=" ", align="right", comma1000=True):
		"""
		f-string처럼 숫자를 원하는 형태로 변경하는것
		"""

		if comma1000:
			changed_input_value = f"{input_value:,}"
		else:
			changed_input_value = str(input_value)

		repeat_no = big_digit - len(changed_input_value)

		repeat_char = fill_empty * (repeat_no)
		repeat_char_start = fill_empty * int(repeat_no / 2)
		repeat_char_end = fill_empty * int(repeat_no - int(repeat_no / 2))

		if align == "left":
			result = changed_input_value + repeat_char
		elif align == "right":
			result = repeat_char + changed_input_value
		elif align == "middle":
			result = repeat_char_start + changed_input_value + repeat_char_end
		else:
			result = repeat_char + changed_input_value
		return result

	def make_text_for_list1d(self, input_list2d, input_len):
		"""
		1차원리스트의 자료들을 정렬해서 텍스트로 만드는 것
		"""
		result_text = ""
		result = []
		len_list = {}
		for index, one in enumerate(input_list2d[0]):
			len_list[index] = 0

		for list1d in input_list2d:
			for index, one in enumerate(list1d):
				len_list[index] = max(len(str(one)), len_list[index])

		for list1d in input_list2d:
			temp = ""
			for index, one in enumerate(list1d):
				len_list[index] = max(len(str(one)), len_list[index])

		print(len_list)

		for list1d in input_list2d:
			temp = ""
			for index, one in enumerate(list1d):
				temp = temp + self.make_text_basic(one, len_list[index]+input_len)

			result_text = result_text + temp + '\n'
		return result_text

	def make_text_for_string(self, input_value, big_digit, fill_empty=" ", align="right"):
		"""
		f-string처럼 문자를 원하는 형태로 변경하는것
		"""
		changed_input_value = str(input_value)
		repeat_no = big_digit - len(changed_input_value)

		repeat_char = fill_empty * (repeat_no)
		repeat_char_start = fill_empty * int(repeat_no / 2)
		repeat_char_end = fill_empty * int(repeat_no - int(repeat_no / 2))

		if align == "left":
			result = changed_input_value + repeat_char
		elif align == "right":
			result = repeat_char + changed_input_value
		elif align == "middle":
			result = repeat_char_start + changed_input_value + repeat_char_end
		else:
			result = repeat_char + changed_input_value
		return result

	def manual(self):
		"""
		이화일의 설명
		"""
		result = """
		여기저기 사용이 가능한것을 하나로 모아놓은 것이다
		"""
		return result

	def delta_two_list1d(self, list1d_a, list1d_b):
		"""
		두개 리스트중에서，앞과 동일한것만 삭제하기 위한 것
		앞의 리스트에서 뒤에 갈은것만 삭제하는것
		예 : [1,2,3,4,5] - [3,4,5,6,7] ==> [1,2]
		"""
		result = [x for x in list1d_a if x not in list1d_b]
		return result


	def move_data_to_right_by_step(self, input_list1d, step_no):
		"""
		1차원으로 들어온 자료를 갯수에 맞도록  분리해서 2차원의 자료로 만들어 주는것
		"""
		result = []
		for partial_list in input_list1d[::step_no]:
			result.append(partial_list)
		return result

	def move_file(self, old_file, new_file):
		"""
		화일을 이동시키는것
		"""
		old_file = self.check_filepath(old_file)
		shutil.move(old_file, new_file)

	def move_folder(self, old_dir, new_dir):
		"""
		폴더를 이동시키는것
		"""
		shutil.move(old_dir, new_dir)

	def move_list2d_by_index(self, input_list2d, input_no_list):
		"""
		입력형태 : 2차원리스트, [[옮길것, 옮기고싶은자리].....]
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

	def pcell_util_change_encodeing_type_001_success(self, ):
		"""
		기본적인 시스템에서의 인코딩을 읽어온다
		"""
		system_in_basic_incoding = sys.stdin.encoding
		system_out_basic_incoding = sys.stdout.encoding
		print("시스템의 기본적인 입력시의 인코딩 ====> ", system_in_basic_incoding)
		print("시스템의 기본적인 출력시의 인코딩 ====> ", system_out_basic_incoding)

	def get_unique_col_name_compare_table_col_name(self, table_name, data2):
		"""
		고유한 컬럼만 골라낸다
		"""
		result = []
		columns = self.read_all_filename_in_folder(table_name)
		update_data2 = self.delete_all_char_except_num_eng_in_input_value(data2)
		for temp_3 in update_data2:
			if not temp_3.lower() in columns:
				result.append(temp_3)
		return result

	def get_unique_data(self, input_2dlist):
		"""
		입력된 값중에서 고유한 값만을 골라내는것
		"""
		result = set()
		if type(input_2dlist[0]) != type([]):
			input_2dlist = [input_2dlist]
		for x in range(len(input_2dlist)):
			for y in range(len(input_2dlist[x])):
				value = input_2dlist[x][y]
				if value == "" or value == None:
					pass
				else:
					result.add(value)
		return list(result)

	def get_unique_data_in_list1d(self, input_data):
		"""
		리스트의 값중 고유한것만 골라내기
		"""
		temp = set()
		for one in input_data:
			temp.add(one)
		result = list(temp)
		return result

	def change_two_list2d_to_one_list2d_with_samelen(self, input_list2d_1, input_list2d_2):
		"""
		선택한 영역이 2개를 서로 같은것을 기준으로 묶을려고하는것이다
		제일앞의 한줄이 같은것이다
		만약 묶을려고 할때 자료가 없을때는 그 기준자료만큼 빈자료를 넣어서 다음자료를 추가하는 것이다
		"""
		no_of_list2d_1 = len(input_list2d_1[0]) - 1
		no_of_list2d_2 = len(input_list2d_2[0]) - 1
		empty_list2d_1 = [""] * no_of_list2d_1
		empty_list2d_2 = [""] * no_of_list2d_2
		# 리스트형태로는 코드가 더 길어질것으로 보여서 입력자료를 사전으로 변경 한것
		temp_dic = {}
		for one in input_list2d_1:
			temp_dic[one[0]] = one[1:]
		checked_list = []
		# 기준이 되는 자료에 항목이 있을때
		for one in input_list2d_2:
			if one[0] in temp_dic.keys():
				temp_dic[one[0]] = list(temp_dic[one[0]]) + list(one[1:])
			else:
				temp_dic[one[0]] = empty_list2d_1 + list(one[1:])
			checked_list.append(one[0])
		# 기준자료에 항목이 없는것에 대한것
		for one in temp_dic.keys():
			if not one in checked_list:
				temp_dic[one] = list(temp_dic[one]) + empty_list2d_2
		# 사전형식을 리스트로 다시 만드는것
		result = []
		for one in temp_dic:
			result.append([one] + list(temp_dic[one]))
		return result

	def print_one_by_one(self, input_list):
		"""
		리스트를 하나씩 출력하는것
		"""
		for one in input_list:
			print(one)

	def read_all_filename_in_folder(self, directory=""):
		"""
		폴더안의 모든 화일이름을 읽오오는것
		단, 폴더안의 폴더이름은 제외시킨다
		"""
		if directory == "":
			directory = self.read_current_path()
		result = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
		return result

	def read_code(self, file_name):
		"""
		같은 코드를 찾는것
		1. 기본이 되는 코드를 읽는다
		2. def 로 시작되는 코드의 시작과 끝을 읽어온다
		py로 만들어진 화일을 불러온다
		"""
		temp_list = []
		result = []
		f = open(file_name, 'r', encoding='UTF8')
		lines = f.readlines()
		original = lines
		lines = list(map(lambda s: s.strip(), lines))
		start_no = 0
		for no in range(len(lines)):
			line = lines[no]

			changed_line = line.strip()
			changed_line = changed_line.replace("\n", "")
			if changed_line[0:3] == "def" and temp_list != []:
				print("처음은 ===> ", start_no)
				print("끝은 ===> ", no)
				result.append(temp_list)
				start_no = no
				temp_list = []
			if changed_line != "" and changed_line[0] != "#":
				temp_list.append(changed_line)
		f.close()
		return [result, original]

	def read_current_path(self):
		"""
		현재의 경로를 돌려주는것
		"""
		result = os.getcwd()
		return result

	def read_file(self, filename):
		"""
		화일 읽기
		"""
		try:
			f = open(filename, 'r', encoding='UTF-8')
			result = f.readlines()
			f.close()
		except:
			f = open(filename, 'r')
			result = f.readlines()
			f.close()

		return result

	def read_file_as_list1d(self, file_full_name):
		"""
		화일을 리스트형태와 text형태로 2개로 돌려준다
		"""
		file_object = open(file_full_name, "r", encoding="UTF-8")
		file_as_list = file_object.readlines()
		file_object.close()
		return file_as_list

	def read_file_by_filename(self, filename):
		"""
		화일을 읽어오는 것
		"""
		try:
			f = open(filename, 'r', encoding='UTF-8')
			result = f.readlines()
			f.close()
		except:
			f = open(filename, 'r')
			result = f.readlines()
			f.close()
		return result

	def read_filenames_in_folder_by_extension_name(self, directory="./", filter="pickle"):
		"""
		pickle로 만든 자료를 저장하는것
		"""
		result = []
		all_files = os.listdir(directory)
		if filter == "*" or filter == "":
			filter = ""
			result = all_files
		else:
			filter = "." + filter
			for x in all_files:
				if x.endswith(filter):
					result.append(x)
		return result

	def read_filenames_in_folder_with_all_properties(self, directory="./"):
		"""
		폴더안의 파일을 이름, 작성한날, 크기, 총경로를 리스트로 만들어서 주는것
		"""
		result = []
		all_files = os.scandir(directory)
		for one in all_files:
			info = one.stat()
			try:
				if one.is_dir():
					#	print(directory+,,\\"+one.name)
					temp = self.read_filenames_in_folder_with_all_properties(directory + "\\" + one.name)
					result.extend(temp)
				else:
					# result.append(one)
					result.append([one.name, info.st_mtime, info.st_size, one.path])
			except:
				pass
		return result


	def read_filenames_in_folder_with_all_properties_except_sub_folder(self, directory="./"):
		"""
		폴더안의 파일을 이름, 작성한날, 크기, 총경로를 리스트로 만들어서 주는것
		"""
		result = []
		all_files = os.scandir(directory)
		for one in all_files:
			info = one.stat()
			try:
				if one.is_dir():
					#	print(directory+,,\\"+one.name)
					pass
				else:
					# result.append(one)
					result.append([one.name, info.st_mtime, info.st_size, one.path])
			except:
				pass
		return result


	def read_folder_filename_all(self, directory):
		"""
		폴더 안의 화일을 읽어오는것
		"""
		result = []
		filenames = os.listdir(directory)
		for filename in filenames:
			full_filename = os.path.join(directory, filename)
			result.append(filename)
		return result

	def read_method_code_by_method_name(self, str_method_name):
		"""
		메소드의 코드를 읽어오는것
		문자로 넣을수있도록 만든 것이다
		"""
		# method_name = eval(str_method_name)
		code_text = inspect.getsource(str_method_name)
		return code_text

	def read_pickle_file(self, path_n_name=""):
		"""
		pickle로 자료를 만든것을 읽어오는 것이다
		"""
		with open(path_n_name, "rb") as fr:
			result = pickle.load(fr)
		return result

	def read_size_for_list2d(self, input_list2d):
		"""
		입력값으로 온것의 크기를 돌려주는것
		"""
		len_x = len(input_list2d)
		len_y = len(input_list2d[0])
		return [len_x, len_y]

	def save_input_data_to_pickle_file(self, source_data="", file_name="", path="D:\\"):
		"""
		자료를 pickle 로 저장하는것
		"""
		if not "." in file_name:
			file_name = file_name + ".pickle"
		with open(path + file_name, "wb") as fr:
			pickle.dump(source_data, fr)

	def similar(self, a, b):
		"""
		두개의 유사도를 측정
		"""
		return SequenceMatcher(None, a, b).ratio()

	def sort_by_index_list(self, source, sort_index):
		"""
		sort_index는 정렬되는 순서
		[1,-2,3] ==> 1,2,3으로 정렬을 하는데, 2번째는 역순으로 정렬한다
		"""
		temp = ""
		for one in sort_index:
			if "-" in str(one):
				temp = temp + ("-x[%s], " % (abs(one)))
			else:
				temp = temp + ("x[%s], " % (one))

		lam = ("lambda x : (%s)" % temp[:-2])

		result = sorted(source, key=eval(lam))
		return result

	def sort_list1d(self, input_list1d):
		"""
		1차원 리스트를 정렬하는 것
		"""

		str_temp = []
		int_temp = []
		for one in input_list1d:
			if type(one) == type("str"):
				str_temp.append(one)
			else:
				int_temp.append(one)

		result_int = sorted(int_temp)
		result_str = sorted(str_temp)
		result = result_int + result_str
		return result

	def sort_list1d_by_str_len(self, input_list):
		"""
		일반적인 정렬이 아니고,	문자의 길이에 따라서 정렬
		"""
		input_list.sort(key=lambda x: len(str(x)))
		return input_list

	def sort_list2d(self, input_list2d):
		"""
		2차원 리스트를 정렬하는 것
		"""
		result = self.sort_list2d_by_index(input_list2d, 0)
		return result

	def sort_list2d_by_index(self, input_list2d, index_no):
		"""
		입력 :  리스트자료
		리스트자료를 몇번째 순서를 기준으로 정렬하는것
		숫자와 문자가 같이 섞여 있어도, 정렬이 가능
		aa = [[111, 'abc'], [222, 222],['333', 333], ['777', 'sjpark'], ['aaa', 123],['zzz', 'sang'], ['jjj', 987], ['ppp', 'park']]
		value=sort_list(리스트자료, 정렬기준번호)
		"""
		print("========>", input_list2d)
		none_temp = []
		str_temp = []
		int_temp = []

		for list1d in input_list2d:

			if type(list1d[index_no]) == type(None):
				none_temp.append(list1d)
			elif type(list1d[index_no]) == type("str"):
				str_temp.append(list1d)
			else:
				int_temp.append(list1d)

		result_int = sorted(int_temp, key=lambda x: x[index_no])
		result_str = sorted(str_temp, key=lambda x: x[index_no])
		result = none_temp + result_int + result_str
		return result

	def sort_list2d_by_index_1(self, input_list2d, index_no):
		"""
		입력 :  리스트자료
		리스트자료를 몇번째 순서를 기준으로 정렬하는것
		숫자와 문자가 같이 섞여 있어도, 정렬이 가능
		aa = [[111, 'abc'], [222, 222],['333', 333], ['777', 'sjpark'], ['aaa', 123],['zzz', 'sang'], ['jjj', 987], ['ppp', 'park']]
		value=sort_list(리스트자료, 정렬기준번호)
		"""
		print("========>", input_list2d)
		none_temp = []
		str_temp = []
		int_temp = []

		for list1d in input_list2d:

			if type(list1d[index_no]) == type(None):
				none_temp.append(list1d)
			elif type(list1d[index_no]) == type("str"):
				str_temp.append(list1d)
			else:
				int_temp.append(list1d)

		result_int = sorted(int_temp, key=lambda x: x[index_no])
		result_str = sorted(str_temp, key=lambda x: x[index_no])
		result = none_temp + result_int + result_str
		return result

	def sort_list2d_by_yy_list(self, input_data, input_list=[0, 2, 3]):
		"""
		2차원리스트를 몇번째를 기준으로 정렬하는것
		"""
		text = ""
		for one in input_list:
			text = text + "row[" + str(one * -1) + "],"
		text = text[:-1]
		exec("global sorted_list2d; sorted_list2d = sorted(input_data, key=lambda row: (%s))" % text)
		global sorted_list2d
		return sorted_list2d

	def sort_list3d_by_index(self, input_list3d, index_no=0):
		"""
		3차원자료를 정렬하는것
		"""
		result = []
		for input_list2d in input_list3d:
			if len(input_list2d) == 1:
				result.append(input_list2d)
			else:
				sorted_list2d = self.sort_list2d_by_index(input_list2d, index_no)
				result.append(sorted_list2d)
		return result

	def sort_mixed_list1d(self, input_list1d):
		"""
		1, 2차원의 자료가 섞여서 저장된 자료를 정렬하는 것
		"""
		int_list = sorted([i for i in input_list1d if type(i) is float or type(i) is int])
		str_list = sorted([i for i in input_list1d if type(i) is str])
		return int_list + str_list

	def split_all_list1d_to_list2d_by_input_text(self, input_list, input_text):
		"""
		리스트로 들어온 자료들을 한번에 분리해서 2차원리스트로 만드는 것
		"""

		result = []
		for one_value in input_list:
			temp_result = str(one_value).split(input_text)
			result.append(temp_result)
		return result

	def split_as_num_list(self, input_list1d, num_list1d):
		"""
		넘어온 자료를 원하는 숫자만큼씩 자르는것
		입력값 : "ㅁㄴㅇㄹㄴㅇㄹㄴㅇㄹㄴㅇㄹㄴㄹ"
		분리기준 = [2,4,5]
		결과값 :["ㅁㄴ", "ㅇㄹㄴㅇ", "ㄹㄴㅇㄹㄴ", "ㅇㄹㄴㄹ"]
		"""
		result = []

		for one_text in input_list1d:
			temp = []
			text_len = len(one_text)
			remain_text =one_text
			for x in num_list1d:
				if x <= len(remain_text):
					temp.append(remain_text[0:x])
					remain_text = remain_text[x:]
				elif len(remain_text):
					temp.append(remain_text)
					break
			result.append(temp)
		return result

	def split_double_moum(self, double_moum):
		"""
		이중모음을 분리시키는것
		"""
		result = self.split_double_moum(double_moum)
		return result

	def split_double_moum_to_two_simple_moum(self, double_moum):
		"""
		이중모음을 단모음으로 바꿔주는것
		"""
		mo2_dic = {"ㅘ": ["ㅗ", "ㅏ"], "ㅙ": ["ㅗ", "ㅐ"], "ㅚ": ["ㅗ", "ㅣ"], "ㅝ": ["ㅜ", "ㅓ"], "ㅞ": ["ㅜ", "ㅔ"], "ㅟ": ["ㅜ", "ㅣ"],
		           "ㅢ": ["ㅡ", "ㅣ"], }
		result = mo2_dic[double_moum]
		return result

	def split_file_by_def(self, filename, base_text="def"):
		"""
		화일안의 def를 기준으로 문서를 분리하는것
		같은 함수의 코드를 찾기위해 def로 나누는것
		맨앞의 시작글자에 따라서 나눌수도 있다
		"""
		temp_list = []
		result = []
		# 화일을 읽어온다
		f = open(filename, 'r', encoding='UTF8')
		lines = f.readlines()
		original = lines
		# 빈 줄을 제거한다
		lines = list(map(lambda s: s.strip(), lines))
		start_no = 0
		for no in range(len(lines)):
			line = lines[no]

			# 각줄의 공백을 제거한다
			one_line = line.strip()
			# 혹시 있을수 있는 줄바꿈을 제거한다
			one_line = one_line.replace("\n", "")
			# 맨 앞에서 def가 발견이되면 여태저장한것을 최종result리스트에 저장 하고 새로이 시작한다
			if one_line[0:(len(base_text) + 1)] == base_text and temp_list != []:
				# print("처음은 ===> ", start_no)
				# print("끝은 ===> ", no)
				result.append(temp_list, start_no, no)
				start_no = no
				temp_list = []
			# 빈행이나 주석으로된 열을 제외한다
			if one_line != "" and one_line[0] != "#":
				temp_list.append(one_line)
		f.close()
		return result

	def split_file_path_by_path_and_name(self, input_value=""):
		"""
		입력값을 경로와 이름으로 분리
		"""
		filename = ""
		path = ""
		input_value = input_value.replace("/", "\\")
		temp_1 = input_value.split("\\")
		if "." in temp_1[-1]:
			filename = temp_1[-1]
		if len(temp_1) > 1 and "\\" in temp_1[:len(temp_1[-1])]:
			path = input_value[:len(temp_1[-1])]
		result = [filename, path]
		return result

	def split_hangul_to_jamo(self, one_text):
		"""
		한글자의 한글을 자음과 모음으로 구분해 주는것
		"""
		one_byte_data = one_text.encode("utf-8")

		new_no_1 = (int(one_byte_data[0]) - 234) * 64 * 64
		new_no_2 = (int(one_byte_data[1]) - 128) * 64
		new_no_3 = (int(one_byte_data[2]) - 128)

		value = new_no_1 + new_no_2 + new_no_3 - 3072

		temp_num_1 = divmod(value, 588)  # 초성이 몇번째 자리인지를 알아내는것
		temp_num_2 = divmod(divmod(value, 588)[1], 28)  # 중성과 종성의 자릿수를 알아내는것것

		chosung = self.var["list_자음_19"][divmod(value, 588)[0]]  # 초성
		joongsung = self.var["list_모음_21"][divmod(divmod(value, 588)[1], 28)[0]]  # 중성
		jongsung = self.var["list_받침_28"][divmod(divmod(value, 588)[1], 28)[1]]  # 종성

		return [chosung, joongsung, jongsung]

	def split_input_file_by_method_name_with_delete_empty_line(self, filename):
		"""
		py화일을 다를려고 만든것이며
		화일의 메소드를 기준으로 나누면서 동시에 빈라인은 삭제하는것
		"""
		def_list = []
		result = []
		total_code = ""
		total = ""
		# 화일을 읽어온다
		f = open(filename, 'r', encoding='UTF8')
		original_lines = f.readlines()
		f.close()
		# print(len(original_lines))
		num = 1
		temp = ""
		exp_start = ""
		exp_end = ""
		exp_mid = ""
		for one_line in original_lines:
			total = total + one_line
			changed_one_line = one_line.strip()
			if changed_one_line == "":
				one_line = ""
			elif changed_one_line[0] == "#":
				one_line = ""
			elif changed_one_line[0:3] == "def":
				def_list.append(temp)
				temp = one_line
			elif '"""' in changed_one_line:
				if changed_one_line[0:3] == '"""':
					exp_end = "no"
					exp_start = "yes"
					one_line = ""
				elif changed_one_line[:-3] == '"""':
					if exp_mid == "yes":
						exp_mid = "no"
					else:
						exp_end = "yes"
						exp_start = "no"
						one_line = ""
				else:
					if exp_mid == "yes":
						exp_mid = "no"
					else:
						exp_mid = "yes"

				num = num + 1

			if exp_start == "yes" and exp_end == "no":
				one_line = ""

			temp = temp + one_line
			total_code = total_code + one_line
		# print(num)

		return [def_list, total_code, total]

	def split_input_text_as_eng_vs_num(self, data):
		"""
		단어중에 나와있는 숫자, 영어를 분리하는기능
		"""
		re_compile = re.compile(r"([a-zA-Z]+)([0-9]+)")
		result = re_compile.findall(data)
		new_result = []
		for dim1_data in result:
			for dim2_data in dim1_data:
				new_result.append(dim2_data)
		return new_result

	def split_input_text_by_newline_tab(self, input_text, number):
		"""
		문자열을 \n, tab으로 구분해서 분리한다
		"""
		result = []
		temp_list = str(input_text).split("\n")
		for one_value_1 in temp_list:
			temp = []
			tab_list = str(one_value_1).split("\t")
			for one_value_2 in tab_list:
				temp.append(one_value_2)
			result.append(temp)

		return result

	def split_input_text_by_step(self, input_text, number):
		"""
		문자열을 몇개씩 숫자만큼 분리하기
		['123456'] => ['12','34','56']
		"""
		input_text = str(input_text)
		result = []
		for i in range(0, len(input_text), number):
			result.append(input_text[i:i + number])
		return result

	def split_inputdata_as_num_vs_char(self, raw_data):
		"""
		문자와숫자를 분리해서 리스트로 돌려주는 것이다
		123wer -> ['123','wer']
		"""
		temp = ""
		int_temp = ""
		result = []
		datas = str(raw_data)
		for num in range(len(datas)):
			if num == 0:
				temp = str(datas[num])
			else:
				try:
					fore_var = int(datas[num])
					fore_var_status = "integer"
				except:
					fore_var = datas[num]
					fore_var_status = "string"
				try:
					back_var = int(datas[num - 1])
					back_var_status = "integer"
				except:
					back_var = datas[num - 1]
					back_var_status = "string"

				if fore_var_status == back_var_status:
					temp = temp + datas[num]
				else:
					result.append(temp)
					temp = datas[num]
		if len(temp) > 0:
			result.append(temp)
		return result

	def split_jamo_in_korean(self, input_text):
		"""
		한글의 자음과 모음을 분리
		"""
		result = []
		for one_text in input_text:
			one_byte_data = one_text.encode("utf-8")
			# print("one_byte_data", one_byte_data)
			new_no_1 = (int(one_byte_data[0]) - 234) * 64 * 64
			new_no_2 = (int(one_byte_data[1]) - 128) * 64
			new_no_3 = (int(one_byte_data[2]) - 128)
			# 유니코드의 번호로 바꾼다
			# 한글의 경우는 44032번째부터 순서대로 표시되어있다
			value = new_no_1 + new_no_2 + new_no_3 - 3072

			# print("value", value)
			chosung = self.var["list_자음_19"][divmod(value, 588)[0]]  # 초성
			joongsung = self.var["list_모음_21"][divmod(divmod(value, 588)[1], 28)[0]]  # 중성
			jongsung = self.var["list_받침_28"][divmod(divmod(value, 588)[1], 28)[1]]  # 종성
			result.append(([chosung, joongsung, jongsung]))
		# print(divmod(value, 588), divmod(divmod(value, 588)[1], 28))
		return result

	def split_list1d_by_group_no(self, input_list1d, step_no):
		"""
		12개의 리스트를
		입력 : [ [1,2,3,4,5,6,7,8,9,10,11,12], 4]를 받으면
				총 4개의 묶읆으로 순서를 섞어서 만들어 주는것
			   [[1,5,9],  [2,6,10],  [3,7,11],  [4,8,12]] 로 만들어 주는것
		"""
		count_no = int(len(input_list1d) / step_no)
		group_no = divmod(len(input_list1d), int(step_no))[0]
		namuji = len(input_list1d) - step_no * group_no
		result = []

		for no in range(count_no):
			temp = input_list1d[no * count_no: no * count_no + count_no]
			result.append(temp)
		if namuji > 0:
			result.append(input_list1d[-namuji:])
		return result

	def split_list1d_by_step(self, input_list1d, step_no):
		"""
		1차원 리스트를 원하는 개수만 큼 자르는 것
		"""
		count_no = int(len(input_list1d) / step_no)
		# group_no = divmod(len(input_list1d), int(step_no))[0]
		namuji = len(input_list1d) - step_no * count_no
		result = []

		for no in range(count_no):
			temp = input_list1d[no * step_no: no * step_no + step_no]
			result.append(temp)
		if namuji > 0:
			result.append(input_list1d[-namuji:])
		return result

	def split_name_and_title(self, input_name):
		"""
		이름과 직함이 같이 있는 입력값을 이름과 직함으로 분리하는 것
		"""
		name = ""
		title = ""
		title_list = ["부장", "이사", "프로", "사원", "대리", "과장", "사장", "차장", "대표", "대표이사", "전무", "전무이사", "공장장"]
		input_name = input_name.strip()  # 공백을 없애는 것
		if len(input_name) > 3:
			for one in title_list:
				title_len = len(one)
				if input_name[-title_len:] == one:
					name = input_name[:-title_len]
					title = input_name[-title_len:]
					break
		return [name, title]

	def split_sentence(self, input_list1d, base_words):
		"""
		문장으로 된것을 의미있는 단어들로 분리하는 것
		"""
		aaa = collections.Counter()
		for one in input_list1d:
			value = str(one).lower().strip()
			if len(value) == 1 or value == None or value == " ":
				pass
			else:
				for l1 in base_words:
					value = value.replace(l1[0], l1[1])
				value = value.replace(",", " ")
				value = value.replace("(", " ")
				value = value.replace(")", " ")
				value = value.replace("  ", " ")
				value = value.replace("  ", " ")
				values = value.split(" ")
				aaa.update(values)
		return aaa

	def split_text_as_serial_no(self, input_data, input_list):
		"""
		입력문자를 숫자만큼씨 짤라서 리스트로 만드는 것
		"""
		result = []
		total_len = 0
		start_no = 0
		for no in range(len(input_list)):
			if no != 0:
				start_no = total_len
			end_len = input_list[no]
			result.append(input_data[start_no:start_no + end_len])
			total_len = total_len + end_len
		return result

	def split_text_line(self, input_text):
		"""
		csv 형식의 자료를 읽어오는 것
		""로 들러쌓인것은 숫자나 문자이며, 아닌것은 전부 문자이다
		"""
		result = []
		temp = ""
		num = 0
		my_type = ""
		for no in range(len(input_text)):
			one_char = input_text[no]
			if one_char == '"' and num == 0:
				my_type = "type_2"
			if one_char == '"': num = num + 1
			if one_char == ',':
				if divmod(num, 2)[1] == 0 and my_type == "type_2":
					temp = temp.replace(",", "")
					try:
						temp = int(temp[1:-1])
					except:
						temp = float(temp[1:-1])
					result.append(temp)
					temp = ""
					num = 0
					my_type = ""
				elif my_type == "":
					result.append(temp)
					temp = ""
					num = 0
				else:
					temp = temp + one_char
			else:
				temp = temp + one_char
		return result

	def split_value_as_engnum(self, data):
		"""
		단어중에 나와있는 숫자, 영어를 분리하는기능
		"""
		re_compile = re.compile(r"[a-zA-Z0-9]+")
		result = re_compile.findall(data)

		new_result = []
		for dim1_data in result:
			for dim2_data in dim1_data:
				new_result.append(dim2_data)
		return new_result

	def split_value_to_str_num(self, input_text):
		"""
		문자와 숫자를 분리하는 것
		"""
		re_com_num = re.compile("[a-zA-Z]+|\d+")
		result = re_com_num.findall(input_text)
		return result

	def change_string_to_binary(self, st):
		"""
		문자를 바이너리로 만드는것
		"""
		temp = [bin(ord(i))[2:].zfill(8) for i in st]
		result = "".join(temp)
		return result

	def change_string_to_binary_list(self, st):
		"""
		문자열을 바이너리 리스트로 만드는것
		"""
		result = [bin(ord(i))[2:].zfill(8) for i in st]
		return result

	def swap(self, a, b):
		"""
		a,b를 바꾸는 함수이다
		"""
		t = a
		a = b
		b = t
		return [a, b]

	def change_2_data_position_for_list1d(self, input_data):
		"""
		input_data : [a, b, c, d]
		result : [b, a, d, c]
		두개의 자료들에 대해서만 자리를 바꾸는 것이다
		"""
		result = []
		for one_data in range(int(len(input_data) / 2)):
			result.append(input_data[one_data * 2 + 1])
			result.append(input_data[one_data * 2])
		return result

	def terms(self):
		"""
		용어정리 : 아래와같은 형태로 용어를 사용한다
		"""

		result = """
		pxy : 커서의 픽셀 좌표
		pwh: 넓이, 높이의 길이를 픽셀단위로 나타낸것
		mouse_click = mouse_down + mouse_up film
		date	 : 2000-01-01
		datelist : [2000, 01, 01]
		ymdlist : [2000, 01, 01]
		time	 : 시간의 여러형태로 입력을 하면, 이에 맞도록 알아서 조정한다
		dhms	 : 2일3시간10분30초, day-hour-minute-sec
		hmslist  : [시, 분, 초]
		utftime  : 1640995200.0 또는 "", 1648037614.4801838 (의미 : 2022-03-23T21:13:34.480183+09:00)
		move	 : 입력값에 더하거나 빼서 다른 값으로 바꾸는것, 입력값과 출력값이 다를때 (출력값을 입력의 형태로 바꾸면 값이 다른것)
		change   : 형태를 바꾼것
		read	 : 입력값을 원하는 형태로 변경해서 갖고오는것
		get	  : 입력값에서 원하는 형태의 값을 갖고오는것
		shift	: 현재의 값을 같은 형태에서 값을 이동시키는것
		index : 0부터 시작되는 번호들
		no : 1부터 시작되는 번호들
		"""
		return result

	def check_text_encoding_data(self, text, encoding_type):
		"""
		인코딩 상태를 확인하는 것
		사용법 : check_text_encoding_data("Hello", "utf-8")
		"""
		byte_data = text.encode(encoding_type)
		hex_data_as_str = "".join("{0}".format(hex(c)) for c in byte_data)
		int_data_as_str = "".join(" {0}".format(int(c)) for c in byte_data)
		# print("\"" + text + "\" 전체 문자 길이: {0}".format(len(text)))
		# print("\"" + text + "\" 전체 문자를 표현하는 데 사용한 바이트 수: {0}	바이트".format(len(byte_data)))
		# print("\"" + text + "\" 16 진수 값: {0}".format(hex_data_as_str))
		# print("\"" + text + "\" 10진수 값: {0}".format(int_data_as_str))
		return int_data_as_str

	def write_hangul_cjj(self, letters="박상진", canvas_size=[50, 50], stary_xy=[1, 1]):
		"""
		"""
		# 입력받은 한글을 크기가 50 x 50의 엑셀 시트에 글씨를 색칠하여 나타내는 것이다

		# 기본 설정부분
		size_x = canvas_size[0]
		size_y = canvas_size[1]
		# 문자 하나의 기본크기
		# 기본문자는 10을 기준으로 만들었으며, 이것을 얼마만큼 크게 만들것인지 한글자의 배수를 정하는것
		h_mm = int(canvas_size[0] / 10)
		w_mm = int(canvas_size[1] / 10)
		# 시작위치
		h_start = stary_xy[0]
		w_start = stary_xy[1]

		check_han = re.compile("[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]")
		for one_char in letters:
			# 한글을 초성, 중성, 종성으로 나누는 것이다
			if check_han.match(one_char):
				jamo123 = self.split_hangul_to_jamo(one_char)
				if jamo123[0][2] == "":
					# 가, 나, 다
					if jamo123[0][1] in ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅣ"]:
						# 기본설정은 시작점은 [1,1]이며, 캔버스의 크기는 [50, 50]인것이다

						start_xy = [1, 1]
						size = [10, 5]  # 위에서 배수를 5,5를 기본으로 해서 50x50되는 것이다
						# 자음의 시작점은 1,1이며, 크기는 50 x 25의 사이즈의 자음을 만드는 것이다
						self.draw_jaum_color(jamo123[0][0],
						                     [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
						                     [h_mm * size[0], w_mm * size[1]])
						# 모음의 시작점은 자음의 끝점에서 5를 이동한 1,30이며, 크기는 자음보다 가로의 크기를 좀 줄인
						# 50 x 20의 사이즈의 자음을 만드는 것이다

						start_xy = [1, 7]
						size = [10, 4]
						self.draw_moum_color(jamo123[0][1],
						                     [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
						                     [h_mm * size[0], w_mm * size[1]])

					# 구, 누, 루
					if jamo123[0][1] in ["ㅗ", "ㅛ", "ㅜ", "ㅡ"]:
						start_xy = [1, 1]
						size = [4, 10]
						self.draw_jaum_color(jamo123[0][0],
						                     [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
						                     [h_mm * size[0], w_mm * size[1]])
						start_xy = [6, 1]
						size = [5, 10]
						self.draw_moum_color(jamo123[0][1],
						                     [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
						                     [h_mm * size[0], w_mm * size[1]])

					# 와, 왜, 궈
					if jamo123[0][1] in ["ㅘ", "ㅙ", "ㅚ", "ㅝ", "ㅞ", "ㅟ", "ㅢ"]:
						# lists = self.div_mo2_mo1(jamo123[0][1])

						start_xy = [1, 1]
						size = [10, 5]
						self.draw_jaum_color(jamo123[0][0],
						                     [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
						                     [h_mm * size[0], w_mm * size[1]])
						start_xy = [8, 1]
						size = [3, 8]
						self.draw_moum_color(jamo123[0][1],
						                     [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
						                     [h_mm * size[0], w_mm * size[1]])
						start_xy = [1, 8]
						size = [6, 3]
						self.draw_moum_color(jamo123[0][1],
						                     [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
						                     [h_mm * size[0], w_mm * size[1]])

				if jamo123[0][2] != "":
					# 왕, 웍, 윔
					if jamo123[0][1] in ["ㅘ", "ㅙ", "ㅚ", "ㅝ", "ㅞ", "ㅟ", "ㅢ"]:
						hangul_type = "23자음+1332-2중모음+24자음"
						# lists = div_mo2_mo1(jamo123[0][1])

						start_xy = [1, 1]
						size = [4, 5]
						self.draw_jaum_color(jamo123[0][0],
						                     [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
						                     [h_mm * size[0], w_mm * size[1]])
						start_xy = [4, 1]
						size = [3, 7]
						self.draw_moum_color(jamo123[0][1],
						                     [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
						                     [h_mm * size[0], w_mm * size[1]])
						start_xy = [1, 7]
						size = [6, 3]
						self.draw_moum_color(jamo123[0][1],
						                     [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
						                     [h_mm * size[0], w_mm * size[1]])
						start_xy = [8, 1]
						size = [3, 6]
						self.draw_jaum_color(jamo123[0][0],
						                     [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
						                     [h_mm * size[0], w_mm * size[1]])

					# 앙, 양, 건
					if jamo123[0][1] in ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅣ"]:
						start_xy = [1, 1]
						size = [3, 5]
						self.draw_jaum_color(jamo123[0][0],
						                     [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
						                     [h_mm * size[0], w_mm * size[1]])
						start_xy = [1, 6]
						size = [5, 4]
						self.draw_moum_color(jamo123[0][1],
						                     [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
						                     [h_mm * size[0], w_mm * size[1]])
						start_xy = [7, 2]
						size = [3, 6]
						self.draw_jaum_color(jamo123[0][0],
						                     [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
						                     [h_mm * size[0], w_mm * size[1]])

					# 곡, 는
					if jamo123[0][1] in ["ㅗ", "ㅛ", "ㅜ", "ㅡ"]:
						start_xy = [1, 1]
						size = [3, 10]
						self.draw_jaum_color(jamo123[0][0],
						                     [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
						                     [h_mm * size[0], w_mm * size[1]])
						start_xy = [4, 1]
						size = [3, 10]
						self.draw_moum_color(jamo123[0][1],
						                     [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
						                     [h_mm * size[0], w_mm * size[1]])
						start_xy = [8, 1]
						size = [3, 10]
						self.draw_jaum_color(jamo123[0][0],
						                     [h_start + h_mm * (start_xy[0] - 1), w_start + w_mm * (start_xy[1] - 1)],
						                     [h_mm * size[0], w_mm * size[1]])

	def zzz_sample_1(self):
		"""
		자주 사용하는 함수의 갯수를 알아내는 것이다
		"""
		num = 0
		result = []
		for one in ["pcell.py", "youtil.py", "jfinder.py", "anydb.py", "ganada.py", "mailmail.py", "pynal.py",
		            "pyclick.py", "scolor.py"]:
			aaa = self.change_python_file_to_sorted_by_def(one)
			num = num + len(aaa)
			result.append([one, len(aaa)])
		print(num)
		print(result)

	def check_similar_word(self, basic_list, input_value):
		"""
		앞에서부터 가장 많이 같은 글자가 있는 자료를 돌려준다
		"""
		result_no = 0
		result_value = ""
		# 공백이 없도록 만든다, 가끔 공백을 2개를 넣거나 하는경우가 있어서 넣은것이다
		checked_input_value = str(input_value).replace(" ", "")
		# 비교할것중에 작은것을 기준으로 한글짜식 비교하기 위해 길이를 계산한것
		a_len = len(input_value)

		# 폴더의 자료를 하나씩 돌려서 비교한다
		for one_word in basic_list:
			temp_no = 0
			# 공백이 없도록 만든다, 가끔 공백을 2개를 넣거나 하는경우가 있어서 넣은것이다
			checked_one_word = str(one_word).replace(" ", "")
			b_len = len(checked_one_word)
			min_len = min(a_len, b_len)

			# 길이만큼 하나씩 비교를 한다
			for index in range(min_len):
				# 만약 위치마다 한글짜식 비교해서 계속 같은것이 나오면 갯수를 더한다
				if checked_input_value[index] == checked_one_word[index]:
					temp_no = temp_no + 1
				else:
					# 만약 다른 글자가 나타나면, 제일 긴것인지를 확인한후, 다음 단어로 넘어가도록 한다
					if temp_no > result_no:
						result_no = temp_no
						result_value = one_word
					print("앞에서부터 같은 갯수 ==> ", temp_no, checked_one_word)
					break
		return result_value