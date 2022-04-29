import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Variables

num_modules = 17
module = 1
last_module = 0
possible_moves = []
alive = True
won = False
power = 50
fuel = 500
locked = 0 #Locked module
queen = 0
vent_shafts = []
info_panels = []
workers = []
image_path = "map.png"

#Procedures
def load_module():
	global module, possible_moves
	check_mod(module)
	possible_moves = get_modules_from(module)
	output_module()

def get_modules_from(module):
	moves = []
	text_file = open("Charles_Darwin/module" + str(module) + ".txt","r")
	for counter in range(0,4):
		move_read = text_file.readline()
		move_read = int(move_read.strip())
		if move_read != 0:
			moves.append(move_read)
	text_file.close()
	return moves

def output_module():
	global module
	print(f"\n ---------------------------------------- \n You are in module {module} \n")

def output_moves():
	global possible_moves
	print("\n From here you can move to modues: |",end = "")
	for  move in possible_moves:
		print(move,"| ",end = "")
	print()

def get_action():
	global module,last_module,possible_moves,power
	valid_action = False
	while not valid_action:
		print("What do you want to do next ? (MOVE, SCANNER)")
		action = sanitize(input(">"))
		if action[0] == "MOVE":
			if action[1] != 0:
				move = action[1]	
			else:
				move = int(input("What module do you want to move to: "))
			if move in possible_moves:
				valid_action = True
				last_module = module
				module = move
		if action[0] == "SCANNER":
			if action[1] == "LOCK":
				print(action[2])
				lock(action[2])
		
				
		else:
			print("The module must be connected to the current module")
	power -= 1

def check_power():
	global alive
	if power <= 0:
		alive = False

def sanitize(input):
	inputs = input.split()
	if "M" in inputs[0].upper():
		inputs[0] = "MOVE"	
		try:
			inputs[1] = int(inputs[1])
		except:
			inputs.append(0)
	elif "L" in inputs[0].upper():
		try:
			mod = int(inputs[1])
		except:
			mod = 0
		inputs = ["SCANNER","LOCK",mod]
	else:
		inputs[0] = "0"
	
	return inputs


def spawn_npcs():
	global num_modules, queen, vent_shafts, info_panels, workers
	module_set =[]
	for counter in range(2,num_modules):
		module_set.append(counter)
	random.shuffle(module_set)
	print(module_set)
	i = 0
	queen = module_set[i]
	for counter in range(0,3):
		i += 1
		vent_shafts.append(module_set[i])
	for counter in range(0,2):
		i += 1
		info_panels.append(module_set[i])
	for counter in range(0,3):
		i += 1
		workers.append(module_set[i])

def check_mod(currmod):
	global queen, workers, info_panels, vent_shafts
	what = ""
	if currmod == queen:
		what = "queen"
	if currmod in workers:
		what = "worker"
	if currmod in info_panels:
		what = "info panel"
	if currmod in vent_shafts:
		what = "vent shaft"
	if what != "":
		print(f"There is a {what} in here")

def check_vent_shafts():
	global num_modules, module, vent_shafts, fuel
	if module in vent_shafts:
		print("There is a bank of fuel cells here")
		print("You load one into your flamethrower")
		fuel_gained = random.randint(2,5) * 10
		print(f"You had {fuel} but now have {fuel+fuel_gained}")
		fuel += fuel_gained
		print("The doors suddenly lock shut")
		print("What is happening to the station")
		print("Our only escape it to go into the ventillation shaft")
		print("We go though to an unkown module")
		last_module = module
		while module in vent_shafts:
			module = random.randint(1,num_modules)
		load_module()

def lock(new_lock):
	global num_modules, power, locked
	if new_lock == 0:
		new_lock = int(input("What moudule do you wish to lock"))
	if new_lock < 0 and new_lock > num_modules:
		print("Invalid Lock Failed")
	elif new_lock == queen:
		print("operation failed")
	else:
		locked = new_lock
		print(f"{locked} has been succefully locked")
		power_used = 25 + 5 * random.randint(0,5)
		power -= power_used
	
#Main

print("Do you wish to see a map? y/[n]")
want_image = input(">")
if want_image == "y":
	img = mpimg.imread('map.png')
	imgplot = plt.imshow(img)
	plt.show(block=False)

spawn_npcs()
print("Queen alien is located in module:",queen)
print("Ventilation shafts are located in modules:",vent_shafts)
print("Information panels are located in modules:",info_panels)
print("Worker aliens are located in modules:",workers)

while alive and not won:
	load_module()
	check_vent_shafts()
	check_power()
	if (not won) and alive:
		output_moves()
		get_action()

if won:
	print("The queen is trapped and you burnt it with your flamethrower \n Game over you win")
if not alive:
	print("Station has run out of power No life supprt you die")