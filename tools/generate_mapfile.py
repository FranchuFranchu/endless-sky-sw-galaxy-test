import json
import math
from urllib.request import urlopen
from math import radians
from sys import stderr
from common import mercator_y_transform
import common

url_sys = "http://2.gusc.cartocdn.com/hbernberg/api/v1/map/6d07251cec293f14ef440bb0a2411372:1577570329193/4/{z}/{x}/{y}.grid.json"

url_hyp = "http://2.gusc.cartocdn.com/hbernberg/api/v1/map/6d07251cec293f14ef440bb0a2411372:1577570329193/3/{z}/{x}/{y}.grid.json"


systems = {}
hyper = {}

try:
	with open("systems.json") as f:
		systems = json.load(f)
	
	with open("hyper.json") as f:
		hyper = json.load(f)
		
except FileNotFoundError:
	# Reload cache
	for x in range(4):
		for y in range(4):
			for k in (
				(systems, url_sys),
				(hyper, url_hyp)
			):
				d, urlf = k
				for f in (
					urlf.format(z=x, x=1, y=y),
					urlf.format(z=y, x=1, y=x),
					#"""
					#urlf.format(x=x, y=1, z=y),
					#urlf.format(x=y, y=1, z=x),
					#urlf.format(x=x, z=1, y=y),
					#urlf.format(x=y, z=1, y=x),
					#"""
				):
					data = {}
					try:
						data = json.load(urlopen(f))
					except:
						pass
						
						
					if data.get("data") is None:
						stderr.write(str(data))
					else:
						for k, v in data["data"].items():
							d[k] = v
				stderr.write(f"{x} {y}\n")
				stderr.flush()

with open("systems.json", "w") as f:
	json.dump(systems, f)
	
with open("hyper.json", "w") as f:
	json.dump(hyper, f)
print(len(systems))		
			
from pprint import pprint

FORMATSTRING = '''
system "{name}"
	government "Uninhabited"
	habitable 600
	belt 1500
	pos {x} {y}
	object "{name}"
		sprite planet/cloud6
		distance 500
		period 180

planet "{name}"
	government "Uninhabited"
	description "{name}_DESC"
	spaceport "{name}_SPACEPORT"
'''


for i in systems.values():
	if i.get("long") is None:
		stderr.write(str(i) + "\n")
		continue
	print(FORMATSTRING.format(
		x = i["long"] * common.scale_x + common.offx,
		y = -mercator_y_transform(radians(i["lat"])) * common.scale_y * 1.3 + common.offy,
		name = i["name"],
		
	))
