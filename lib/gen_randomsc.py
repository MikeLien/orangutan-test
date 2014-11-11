import random
import os
import sys
from os import listdir, mkdir, chdir, getcwd
from os.path import isdir, join, exists
from argparser import Parser

class GenRandomSC(object):
	def __init__(self, dimensions=[320,480], swipe_padding=[40,40,40,40], script_repo="script", amount=1, steps=10000, deviceName="Device"):
		self.dimensions = dimensions
		self.swipe_padding = swipe_padding
		self.script_repo = script_repo
		self.amount = amount
		self.steps = steps
		self.deviceName = deviceName
		self.range_action_steps = 20
		self.short_steps_duration = 200
		self.long_steps_duration = 2000
		self.range_sleep = 5.0
		if len(sys.argv) > 1:
			options = Parser.parser(sys.argv[1:])
			if str(options.config):
				with open(options.config) as f:
					self.config = eval(f.read())
					self.dimensions = [self.config['res_x'], self.config['res_y']]
					self.deviceName = self.config['device_name']
					self.script_repo = self.config['script_repo']
					self.amount = int(self.config['script_amount'])
					self.steps = int(self.config['script_steps'])
			if int(options.gen_scripts_amount): self.amount = int(options.gen_scripts_amount)
			if int(options.gen_scripts_steps): self.steps = int(options.gen_scripts_steps)
			if str(options.gen_scripts_output): self.script_repo = str(options.gen_scripts_output)

	def gen_random_sc(self):
		cmd_list=["scroll_down", "scroll_up",
					"swipe_left", "swipe_right",
					"tap", "double_tap", "long_tap",
					"drag", "pinch",
					"tap_home", "long_tap_home",
					"vol_up", "vol_down"]
		orig_workdir = getcwd()
		for each_folder in self.script_repo.split('/'):
			if each_folder:
				if not exists(each_folder): mkdir(each_folder)
				chdir(each_folder)
		scripts_folder = self.create_folder(self.deviceName)
		if not exists(scripts_folder): mkdir(scripts_folder)
		chdir(scripts_folder)
		skip_count=0
		for num_files in range(self.amount):
			output_file = open(self.creat_file(),"w")
			for cmd_steps in range(self.steps/2):
				if skip_count > 0:
					skip_count -= skip_count
					continue
				random_cmd = random.choice(cmd_list)
				output_file.write(self.get_cmd_events(random_cmd)+'\n')
				if random_cmd is "tap_home" or random_cmd is "long_tap_home" or \
						random_cmd is "vol_up" or random_cmd is "vol_down":
					skip_count=2
				output_file.write(self.get_sleep_event(self.get_sleep_time(shortest=0.5))+'\n')
			output_file.close()
		chdir(orig_workdir)
		return scripts_folder

	def creat_file(self):
		count = len(os.listdir(os.getcwd()))
		fileName = str(count+1).zfill(4)+".sc"
		return fileName

	def create_folder(self,deviceName):		
		count = len([f for f in listdir(getcwd()) if isdir(join(getcwd(), f))])
		folderName = deviceName+"_"+str(count+1).zfill(4)
		return folderName		
	
	def get_short_latency(self):
		num_steps = random.randint(1,self.range_action_steps)
		durations = random.randint(1,self.short_steps_duration)
		return (num_steps, durations)

	def get_long_latency(self):
		num_steps = random.randint(1,self.range_action_steps)
		durations = random.randint(1,self.long_steps_duration)
		return (num_steps, durations)

	def get_coordinates(self):
		x = random.randint(0,self.dimensions[0]-1)
		y = random.randint(0,self.dimensions[1]-1)
		return (x, y)

	def get_sleep_time(self, shortest=1, longest=2):
		return round(random.uniform(shortest, longest),2)

	def get_drag_event(self, touchstart_x1, touchstart_y1, touchend_x1,
						touchend_y1, num_steps=10, duration=1000):
		return "drag %s %s %s %s %s %s" % (touchstart_x1, touchstart_y1,
										touchend_x1, touchend_y1,
										num_steps, duration)

	def get_sleep_event(self, duration=1.0):
		return "sleep %s" % int(float(duration) * 1000.0)

	def get_tap_event(self, x, y, times=1, duration=100):
		return "tap %s %s %s %s" % (x, y, times, duration)

	def get_scroll_events(self, direction, numsteps=10, duration=100):
		#Define direction against scroll
		#Scroll up: gesture is swipe down
		#Scroll down: gesture is swipe up
		x = int(self.dimensions[0] / 2)
		(y1, y2) = (self.dimensions[1] - self.swipe_padding[3], self.swipe_padding[0])
		if direction == "up":
			(y1, y2) = (y2, y1)
		return self.get_drag_event(x, y1, x ,y2, numsteps, duration)

	def get_swipe_events(self, direction, numsteps=10, duration=100):
		#Define direction against gesture swipe
		y = (self.dimensions[1] / 2)
		(x1, x2) = (self.swipe_padding[2], self.dimensions[0] - self.swipe_padding[0])
		if direction == "left":
			(x1, x2) = (x2, x1)
		return self.get_drag_event(x1, y, x2, y, numsteps, duration)

	def get_pinch_event(self, touch1_x1, touch1_y1, touch1_x2, touch1_y2,
					touch2_x1, touch2_y1, touch2_x2, touch2_y2,
					numsteps=10, duration=1000):
		return "pinch %s %s %s %s %s %s %s %s %s %s" % (touch1_x1, touch1_y1,
													touch1_x2, touch1_y2,
													touch2_x1, touch2_y1,
													touch2_x2, touch2_y2,
													numsteps,
													duration)

	def get_homekey_event(self, letency):
		return "keydown 102\n" + self.get_sleep_event(float(letency)/1000) + "\nkeyup 102"

	def get_volup_event(self, letency):
		return "keydown 115\n" + self.get_sleep_event(float(letency)/1000) + "\nkeyup 115"

	def get_voldown_event(self, letency):
		return "keydown 114\n" + self.get_sleep_event(float(letency)/1000) + "\nkeyup 114"

	def get_cmd_events(self, cmd):
		use_default = int(random.random()*10)%2
		short_latency = self.get_short_latency()
		long_latency = self.get_long_latency()
		coord_1st = self.get_coordinates()
		coord_2nd = self.get_coordinates()
		coord_3rd = self.get_coordinates()
		coord_4th = self.get_coordinates()

		if cmd == "scroll_down":
			if use_default:
				cmdevents = self.get_scroll_events("down")
			else:
				cmdevents = self.get_scroll_events("down", *short_latency)
		elif cmd == "scroll_up":
			if use_default:
				cmdevents = self.get_scroll_events("up")
			else:
				cmdevents = self.get_scroll_events("up", *short_latency)
		elif cmd == "swipe_left":
			if use_default:
				cmdevents = self.get_swipe_events("left")
			else:
				cmdevents = self.get_swipe_events("left", *short_latency)
		elif cmd == "swipe_right":
			if use_default:
				cmdevents = self.get_swipe_events("right")
			else:
				cmdevents = self.get_swipe_events("right", *short_latency)
		elif cmd == "drag":
			if use_default:
				args = coord_1st + coord_2nd
			else:
				args = coord_1st + coord_2nd + long_latency
			cmdevents = self.get_drag_event(*args)
		elif cmd == "tap":
			if use_default:
				cmdevents = self.get_tap_event(*coord_1st, times=1)
			else:
				cmdevents = self.get_tap_event(*coord_1st, times=1, duration=short_latency[1])
		elif cmd == "double_tap":
			cmdevents = self.get_tap_event(*coord_1st, times=2)
		elif cmd == "long_tap":
			cmdevents = self.get_tap_event(*coord_1st, times=1, duration=self.long_steps_duration)
		elif cmd == "pinch":
			args = coord_1st + coord_2nd + coord_3rd + coord_4th + short_latency
			cmdevents = self.get_pinch_event(*args)
		elif cmd == "sleep":
			if use_default:
				cmdevents = self.get_sleep_event()
			else:
				sleep_time = self.get_sleep_time(longest=self.range_sleep)
				cmdevents = self.get_sleep_event(sleep_time)
		elif cmd == "tap_home":
			cmdevents = self.get_homekey_event(self.short_steps_duration)
		elif cmd == "long_tap_home":
			cmdevents = self.get_homekey_event(self.long_steps_duration)
		elif cmd == "vol_up":
			cmdevents = self.get_volup_event(self.short_steps_duration)
		elif cmd == "vol_down":
			cmdevents = self.get_voldown_event(self.short_steps_duration)
		else:
			raise Exception("Unknown command")

		return cmdevents

if __name__ == '__main__':
	getrandomsc = GenRandomSC().gen_random_sc()