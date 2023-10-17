# -*- coding: utf-8 -*-
import pandas
import matplotlib.pyplot as plt
import numpy as np

var = {}
class rgraph:
	def __init__(self):
		var["chart"] = plt
		var["marker_color"] = "k"
		var["marker_line_style"] = "-"
		var["marker_style"] = "o"
		var["chart"].rc("font", family="Malgun Gothic")
		var["chart_type"] ="plot"
		var["chart"].grid(False)

	def set_data(self, input_list):
		"""

		:param input_list:
		:return:
		"""
		#plt.axis([0, 5, 0, 20])  # X, Y축의 범위: [xmin, xmax, ymin, ymax]
		var["data"] = input_list

	def set_grid(self, input_list=False):
		"""

		:param input_list:
		:return:
		"""
		var["chart"].grid(input_list)

	def set_label(self, input_text):
		"""

		:param input_text:
		:return:
		"""
		if input_text[0] !="": var["chart"].xlabel(input_text[0])
		if input_text[1] !="": var["chart"].ylabel(input_text[1])

	def set_xtick(self, input_list):
		"""

		:param input_list:
		:return:
		"""
		var["chart"].xticks(input_list[0], input_list[1])

	def set_ytick(self, input_list):
		"""

		:param input_list:
		:return:
		"""
		var["chart"].yticks(input_list[0], input_list[1])

	def set_marker_color(self, input_text):
		"""

		:param input_text:
		:return:
		"""
		print(input_text)
		var["marker_color"] = self.check_marker_color(input_text)
		print(var["marker_color"])

	def check_marker_color(self, input_text):
		"""

		:param input_text:
		:return:
		"""
		m1_dic = {"blu":"b",
		         "gre": "g",
		         "red": "r",
		         "yel": "y",
		         "bla": "k",
		          }
		result = m1_dic[input_text]
		print(result)
		return result

	def set_line_style(self, input_text):
		"""

		:param input_text:
		:return:
		"""
		var["marker_line_style"] = self.check_line_style_dic(input_text)

	def check_line_style_dic(self, input_text=""):
		"""

		:param input_text:
		:return:
		"""
		m2_dic = {"-":"-",
		         "--": "--",
		         "-.": "-.",
		         ".": ":",
		         "": "",
		         "none": "",
		         "no": "",
		         }
		result = m2_dic[input_text]
		return result

	def set_marker_style (self, input_list):
		"""

		:param input_list:
		:return:
		"""
		var["marker_style"] = self.check_marker_style(input_list)

	def check_marker_style(self, input_text):
		"""

		:param input_text:
		:return:
		"""
		m3_dic = {".":".",
		         "o": "o",
		         "rect": "s",
		         "x": "x",
		         "": "",
		         "none": "",
		         "no": "",
		         }
		result = m3_dic[input_text]
		return result

	def set_title(self, input_text):
		"""

		:param input_text:
		:return:
		"""
		var["chart"].title(input_text)

	def check_scale(self):
		"""

		:return:
		"""
		pass

	def check_grid(self):
		"""

		:return:
		"""
		pass

	def set_chart_type(self, input_text="plot"):
		"""

		:param input_text:
		:return:
		"""
		var["chart_type"] = input_text

	def check_chart_type(self):
		"""

		:return:
		"""
		input_text = var["chart_type"]
		aaa = var["marker_color"] + var["marker_line_style"] + var["marker_style"]

		if input_text == "plot":
			var["chart"].plot(var["data"][0], var["data"][0], aaa)
		elif input_text == "bar":
			var["chart"].bar(var["data"][0], var["data"][0], aaa)
		elif input_text == "pie":
			var["chart"].pie(var["data"][0], var["data"][0], aaa)
		elif input_text == "errorbar":
			var["chart"].errorbar(var["data"][0], var["data"][0], aaa)
		elif input_text == "hist":
			var["chart"].hist(var["data"][0], var["data"][0], aaa)
		elif input_text == "scatter":
			var["chart"].scatter(var["data"][0], var["data"][0], aaa)
			#plt.scatter(x, y, s=area, c=colors, alpha=0.5, cmap='Spectral')

	def set_figure(self):
		"""

		:return:
		"""
		#figsize : (width, height)의 튜플을 전달한다. 단위는 인치이다.
		#dpi : 1인치당의 도트 수
		#facecolor : 배경색
		#edgecolor : 외곽선의 색
		pass

	def run(self):
		"""

		:return:
		"""
		self.check_chart_type()
		var["chart"].show()

x = [1, 2, 3, 4]
y = [2, 3, 5, 10]

x1 = [1, 5, 7, 4]
y1 = [2, 3, 4, 10]
aaa = rgraph()
aaa.set_data([x,y])
aaa.set_data([x1,y1])
aaa.set_marker_color("blu")
aaa.set_ytick([[1, 2, 8], ["Low", "Zero", "High"]])
aaa.set_title("title / 타이틀")
aaa.set_line_style("")
aaa.set_chart_type("plot")
aaa.set_marker_style("o")
aaa.set_grid("o")
aaa.set_label(["xxx", "yyy"])
plt.fill_between(x[1:3], y[1:3], alpha=0.5)
aaa.run()