import json
from urllib.request import urlopen

urlf = "http://2.gusc.cartocdn.com/hbernberg/api/v1/map/6d07251cec293f14ef440bb0a2411372:1577570329193/4/{z}/{x}/{y}.grid.json"

systems = {}

for x in range(4):
	for y in range(4):
		try:
			data = json.load(urlopen(urlf.format(z=x, x=1, y=y)))
		except:
			print(x, y)
		
		systems = {**systems, **data["data"]}
		try:
			data = json.load(urlopen(urlf.format(z=1, x=x, y=y)))
		except:
			print(x, y)
		
		systems = {**systems, **data["data"]}
		try:
			data = json.load(urlopen(urlf.format(z=y, x=x, y=1)))
		except:
			print(x, y)
		
		systems = {**systems, **data["data"]}
		
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
	print(FORMATSTRING.format(
		x = i["long"] * 20 + 197700,
		y = -i["lat"] * 20 + 250500,
		name = i["name"],
		
	))

print(len(systems))