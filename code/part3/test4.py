import cv2
import numpy as np
import speech_recognition as SRG 
import time

def lable_grid(board):
	grid_start_coordinates = []
	x_cord_value =10
	y_cord_value = 570
	for x_cordinates in range(1,9):
		for y_cordinates in range(1,9):
			grid_start_coordinates.append([x_cord_value,y_cord_value])
			#cv2.circle(board,(x_cord_value,y_cord_value),10,(255,0,255),2)
			y_cord_value-=70
		x_cord_value+=70
		y_cord_value=570
	return grid_start_coordinates
def overlay_transparent(background, overlay, x, y):

	background_width = background.shape[1]
	background_height = background.shape[0]

	if x >= background_width or y >= background_height:
		return background

	h, w = overlay.shape[0], overlay.shape[1]

	if x + w > background_width:
		w = background_width - x
		overlay = overlay[:, :w]

	if y + h > background_height:
		h = background_height - y
		overlay = overlay[:h]

	if overlay.shape[2] < 4:
		overlay = np.concatenate(
					[
						overlay,
						np.ones((overlay.shape[0], overlay.shape[1], 1), dtype = overlay.dtype) * 255
						],
					axis = 2,
		)

	overlay_image = overlay[..., :3]
	mask = overlay[..., 3:] / 255.0

	background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image

	return background
All_positions_x = {"A":10,"B":80,"C":150,"D":220,"E":290,"F":360,"G":430,"H":500} #these were for x cordinates
All_positions_y = {"1":500,"2":430,"3":360,"4":290,"5":220,"6":150,"7":80,"8":10} #these were for y cordinates

def pawn(move_possible,turn,xval_r,xval,yval_r,yval,destroy):
	global All_positions_x, All_positions_y
	global white_army, black_army
	print("validating")
	reason=""
	print(turn)
	validation = True
	if move_possible==1 and turn == 1:
		try:
			#now we will check if required position is valid : : :  This is for pawns remember destryoing condition is not given
			if xval_r == xval and yval_r == yval-70 and destroy == 0:
				validation = True
			elif xval_r == xval and yval==430 and yval_r == yval-140 and destroy == 0:
				validation = True
			elif (xval_r == xval+70 or xval_r == xval-70) and yval_r == yval-70 and destroy==1:
				validation = True
			else:
				validation = False

			#now we move if valid condition
			print("validation", validation)
		except ValueError:
			validation = False
			reason="There is no one at given position"
		except IndexError:
			validation = False
		except KeyError:
			validation = False
	if move_possible==1 and turn == 0:
		try:
			#now we will check if required position is valid : : :  This is for pawns remember destryoing condition is not given
			if xval_r == xval and yval_r == yval+70 and destroy == 0:
				validation = True
			elif xval_r == xval and yval==80 and yval_r == yval+140 and destroy == 0:
				validation = True
			elif (xval_r == xval+70 or xval_r == xval-70) and yval_r == yval+70 and destroy==1:
				validation = True
			else:
				validation = False

			#now we move if valid condition
			print("validation", validation)
		except ValueError:
			validation = False
			reason="There is no one at given position"
		except IndexError:
			validation = False
		except KeyError:
			validation = False
	#we need to create a function for destroy enemy
	return validation

def check_key(x,y):
	continue_traversing =True
	try:
		army_member = list(white_army.keys())[list(white_army.values()).index([x,y])]
		continue_traversing =False
		# army_member = list(black_army.keys())[list(black_army.values()).index([x,y])]
		# return continue_traversing
	except ValueError:
		# return continue_traversing
		reason="There is no one at given position"
	except IndexError:
		# return continue_traversing
		pass
	except KeyError:
		# return continue_traversing
		pass
	# now check for black army
	try:
		army_member = list(black_army.keys())[list(black_army.values()).index([x,y])]
		continue_traversing =False
		# army_member = list(black_army.keys())[list(black_army.values()).index([x,y])]
		# return continue_traversing
	except ValueError:
		# return continue_traversing
		reason="There is no one at given position"
	except IndexError:
		# return continue_traversing
		pass
	except KeyError:
		# return continue_traversing
		pass
	return continue_traversing
def check_w_army_key(x,y):
	continue_traversing =True
	try:
		army_member = list(white_army.keys())[list(white_army.values()).index([x,y])]
		continue_traversing =False
		# army_member = list(black_army.keys())[list(black_army.values()).index([x,y])]
		# return continue_traversing
	except ValueError:
		# return continue_traversing
		reason="There is no one at given position"
	except IndexError:
		# return continue_traversing
		pass
	except KeyError:
		# return continue_traversing
		pass
	return continue_traversing
def check_b_army_key(x,y):
	continue_traversing =True
	try:
		army_member = list(black_army.keys())[list(black_army.values()).index([x,y])]
		continue_traversing =False
		# army_member = list(black_army.keys())[list(black_army.values()).index([x,y])]
		# return continue_traversing
	except ValueError:
		# return continue_traversing
		reason="There is no one at given position"
	except IndexError:
		# return continue_traversing
		pass
	except KeyError:
		# return continue_traversing
		pass
	return continue_traversing
def rooks(move_possible,turn,xval_r,xval,yval_r,yval,destroy):
	global All_positions_x, All_positions_y
	global white_army, black_army
	print("validating")
	reason=""
	goto= ""
	print(turn)
	validation = True
	continue_traversing =True
	continue_traversing = True
	continue_traversing2 = True
	if move_possible==1 and turn == 1:
		print("white")
		if xval==xval_r:
			goto="vertical"
			if yval==yval_r:
				return False
			elif yval>yval_r:
				goto ="up"
			elif yval<yval_r:
				goto = "down"
		elif yval == yval_r:
			if xval==xval_r:
				return False
			elif xval>xval_r:
				goto ="left"
			elif xval<xval_r:
				goto = "right"
		print(goto)
		#now we traverse in given required directions untill we reach destination or encounter any member
	elif move_possible==1 and turn == 0:
		print("BLACK")
		if xval==xval_r:
			goto="vertical"
			if yval==yval_r:
				return False
			elif yval<yval_r:
				goto ="down"
			elif yval>yval_r:
				goto = "up"
		elif yval == yval_r:
			if xval==xval_r:
				return False
			elif xval<xval_r:
				goto ="right"
			elif xval>xval_r:
				goto = "left"
		print(goto)

	#for moving horizontal
	horizontal = []
	for elements in All_positions_x:
		horizontal.append(All_positions_x[elements])
	print(horizontal)
	if goto=="right":
		for idx, integer in enumerate(horizontal):
			# if integer == xval:
			# 	curr_idx=idx
			# if integer == xval_r:
			# 	req_idx=idx
			if integer > xval and integer<=xval_r:
				print("going right")
				if turn == 1:
					continue_traversing1 = check_w_army_key(integer,yval)
					if integer < xval_r:
						continue_traversing2 = check_b_army_key(integer,yval)
					if continue_traversing1==False or continue_traversing2 ==False:
						validation=False
				elif turn == 0:
					continue_traversing1 = check_b_army_key(integer,yval)
					if integer < xval_r:
						continue_traversing2 = check_w_army_key(integer,yval)
					if continue_traversing1==False or continue_traversing2 ==False:
						validation=False
	elif goto=="left":
		horizontal.reverse()
		for idx, integer in enumerate(horizontal):
			# if integer == xval:
			# 	curr_idx=idx
			# if integer == xval_r:
			# 	req_idx=idx
			if integer>=xval_r and integer < xval:
				print("going left")
				if turn == 1:
					continue_traversing1 = check_w_army_key(integer,yval)
					if integer > xval_r:
						continue_traversing2 = check_b_army_key(integer,yval)
					if continue_traversing1==False or continue_traversing2 ==False:
						validation=False
				elif turn == 0:
					continue_traversing1 = check_b_army_key(integer,yval)
					if integer > xval_r:
						continue_traversing2 = check_w_army_key(integer,yval)
					if continue_traversing1==False or continue_traversing2 ==False:
						validation=False

	#for moving vertical
	vertical = []
	for elements in All_positions_y:
		vertical.append(All_positions_y[elements])
	print(vertical)
	if goto=="up":
		for idx, integer in enumerate(vertical):
			# if integer == xval:
			# 	curr_idx=idx
			# if integer == xval_r:
			# 	req_idx=idx
			if integer < yval and integer>=yval_r:
				print("going up")
				if turn == 1:
					continue_traversing1 = check_w_army_key(xval,integer)
					if integer > yval_r:
						continue_traversing2 = check_b_army_key(xval,integer)
					if continue_traversing1==False or continue_traversing2 ==False:
						validation=False
				elif turn == 0:
					continue_traversing1 = check_b_army_key(xval,integer)
					if integer > yval_r:
						continue_traversing2 = check_w_army_key(xval,integer)
					if continue_traversing1==False or continue_traversing2 ==False:
						validation=False
	if goto=="down":
		vertical.reverse()
		for idx, integer in enumerate(vertical):
			# if integer == xval:
			# 	curr_idx=idx
			# if integer == xval_r:
			# 	req_idx=idx
			if integer > yval and integer<=yval_r:
				print("going up")
				if turn == 1:
					continue_traversing1 = check_w_army_key(xval,integer)
					if integer<yval_r:
						continue_traversing2 = check_b_army_key(xval,integer)
					if continue_traversing1==False or continue_traversing2 ==False:
						validation=False
				elif turn == 0:
					continue_traversing1 = check_b_army_key(xval,integer)
					if integer<yval_r:
						continue_traversing2 = check_w_army_key(xval,integer)
					if continue_traversing1==False or continue_traversing2 ==False:
						validation=False
	if goto=="":
		validation=False
	return validation


pawns_army = ["wPawn1","wPawn2","wPawn3","wPawn4","wPawn5","wPawn6""wPawn7","wPawn8",
				"bPawn1","bPawn2","bPawn3","bPawn4","bPawn5","bPawn6","bPawn7","bPawn8"]
rooks_army = ["wRook","wRookR","bRook","bRookR"]
horse_army = ["wHorse","wHorseR","bHorse","bHorseR"]
cammel_army = ["wCammel","wCammelR","bCammel","bCammelR"]
queens_army = ["wQueen","bQueen"]
kings_army = ["wKing","bKing"]
def possible_positions(text_command,turn):
	#here we validate positions and move accordingly
	global All_positions_x, All_positions_y
	global white_army, black_army
	print("validating")
	reason=""
	destroy = 0
	move_possible = 0
	print(turn)
	validation = True
	try:
		interested_text_area = text_command[5:]
		print("Current position",interested_text_area[:2])
		print("required position:",interested_text_area[6:])
		Current_position = interested_text_area[:2]
		required_position = interested_text_area[6:]

		#we check which army member is at current position
		xval = All_positions_x[Current_position[0]]
		yval = All_positions_y[Current_position[1]]
		print(xval,yval)
		xval_r = All_positions_x[required_position[0]]
		yval_r = All_positions_y[required_position[1]]
		print(xval_r,yval_r)
		
		#checking if need to destroy any one:
		if turn==1:
			print("printing turn",turn)
			army_member = list(white_army.keys())[list(white_army.values()).index([xval,yval])]
			print(army_member)
			move_possible = 1
			member_to_destroy = list(black_army.keys())[list(black_army.values()).index([xval_r,yval_r])]
			destroy = 1
		elif turn==0:
			print("printing turn",turn)
			army_member = list(black_army.keys())[list(black_army.values()).index([xval,yval])]
			print(army_member)
			move_possible = 1
			member_to_destroy = list(white_army.keys())[list(white_army.values()).index([xval_r,yval_r])]
			destroy = 1
	except ValueError:
		validation = False
		reason="There is no one at given position"
	except IndexError:
		validation = False
	except KeyError:
		validation = False

	#we need seperate try so that we can process all things
	if move_possible==1:
		if army_member in pawns_army:
			validation = pawn(move_possible,turn,xval_r,xval,yval_r,yval,destroy)
		elif army_member in rooks_army:
			validation = rooks(move_possible,turn,xval_r,xval,yval_r,yval,destroy)
	#now we check required position


	if validation == True and move_possible == 1 and turn == 1:
		white_army[army_member]=[xval_r,yval_r]
		print(white_army)
		if destroy == 1:
			del black_army[member_to_destroy]
	if validation == True and move_possible == 1 and turn == 0:
		black_army[army_member]=[xval_r,yval_r]
		print(black_army)
		if destroy == 1:
			del white_army[member_to_destroy]



white_army = {"wRook":[10,500],"wHorse":[80,500],"wCammel":[150,500],"wQueen":[290,500],"wKing":[220,500],"wCammelR":[360,500],"wHorseR":[430,500],"wRookR":[500,500],
				"wPawn1":[10,430],"wPawn2":[80,430],"wPawn3":[150,430],"wPawn4":[220,430],"wPawn5":[290,430],"wPawn6":[360,430],"wPawn7":[430,430],"wPawn8":[500,430]}

black_army = {"bRook":[10,10],"bHorse":[80,10],"bCammel":[150,10],"bQueen":[290,10],"bKing":[220,10],"bCammelR":[360,10],"bHorseR":[430,10],"bRookR":[500,10],
				"bPawn1":[10,80],"bPawn2":[80,80],"bPawn3":[150,80],"bPawn4":[220,80],"bPawn5":[290,80],"bPawn6":[360,80],"bPawn7":[430,80],"bPawn8":[500,80]}
def allot_army_positions(board):
	global white_army, black_army
	firsttime=0
	for elements in white_army:
		#print(elements,white_army[elements])
		im2 = cv2.imread("../images/{}.png".format(elements), cv2.IMREAD_UNCHANGED)
		#print(lable_grid(board))
		if firsttime ==0:
			back = overlay_transparent(board, im2, white_army[elements][0], white_army[elements][1])
			firsttime+=1
		elif firsttime!=0:
			back = overlay_transparent(back, im2, white_army[elements][0], white_army[elements][1])
	for elements in black_army:
		#print(elements,black_army[elements])
		im2 = cv2.imread("../images/{}.png".format(elements), cv2.IMREAD_UNCHANGED)
		#print(lable_grid(board))
		back = overlay_transparent(back, im2, black_army[elements][0], black_army[elements][1])
	return back

def detect_speech():
	#https://www.journaldev.com/37873/python-speech-to-text-speechrecognition
	text_output=""
	store = SRG.Recognizer()
	with SRG.Microphone() as s:
		print("Give command to your army")
		audio_input = store.record(s, duration=7)
		# print("Recording time:",time.strftime("%I:%M:%S"))
		try:
			text_output = store.recognize_google(audio_input)
			print("Text converted from audio:\n")
			print(text_output)
			print("Finished!!")
			#print("Execution time:",time.strftime("%I:%M:%S"))
		except:
			print("Couldn't process the audio input.")
	return text_output
def show_frames():
	global white_army, black_army
	turn = 1   #turn 1 means white to play :: and :: turn 0 means black to play
	board = cv2.imread("../images/grid.png", cv2.IMREAD_UNCHANGED)
	board1=board.copy()
	back = allot_army_positions(board.copy())
	while True:
		#text_command = detect_speech()
		text_command = input("move D7 To D6{}".format(turn))
		print(text_command)
		if text_command!="":
			print(turn)
			possible_positions(text_command,turn)
		if turn==1:
			turn=0
		else:
			turn=1
		back = allot_army_positions(board.copy())
		cv2.imshow('Voice Chess',cv2.cvtColor(back,cv2.COLOR_BGR2RGB))
		#cv2.imshow('Voice Chess',cv2.cvtColor(back_im,cv2.COLOR_BGR2RGB))
		if cv2.waitKey(25)&0xFF==('q'):
			cv2.destroyAllWindows()
			break
#print(lable_grid())
#allot_army_positions()
show_frames()

