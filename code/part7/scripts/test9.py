import cv2
import numpy as np
import speech_recognition as SRG 
import time

def overlay_transparent(background, overlay, x, y):
	# https://stackoverflow.com/a/54058766/11359097
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
	upgrade = False
	if yval_r == 10:
		upgrade = True
	if move_possible==1 and turn == 1:
		try:
			#now we will check if required position is valid : : :  This is for pawns remember destryoing condition is not given
			if xval_r == xval and yval_r == yval-70 and destroy == 0:
				if check_w_army_key(xval,yval_r) == True:
					validation = True
					print(validation,"val70")
				else:
					validation = False
					print(validation,"val700")
			elif xval_r == xval and yval==430 and yval_r == yval-140 and destroy == 0:
				if check_w_army_key(xval_r,yval_r+70) == True and check_b_army_key(xval_r,yval_r+70)==True and check_w_army_key(xval,yval_r)==True:
					validation = True
					cc = check_w_army_key(xval_r,yval_r+70)
					cd = check_b_army_key(xval_r,yval_r+70)
					ce = check_w_army_key(xval,yval_r)
					print(cc,cd,ce)
					print(validation,"val140")
				else:
					validation = False
					print(validation,"val1400")
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
	elif move_possible==1 and turn == 0:
		try:
			#now we will check if required position is valid : : :  This is for pawns remember destryoing condition is not given
			if xval_r == xval and yval_r == yval+70 and destroy == 0:
				if check_b_army_key(xval,yval_r) == True:
					validation = True
				else:
					validation = False
			elif xval_r == xval and yval==80 and yval_r == yval+140 and destroy == 0:
				if check_w_army_key(xval_r,yval_r-70) == True and check_b_army_key(xval_r,yval_r-70)==True and check_b_army_key(xval,yval_r)==True:
					validation = True
				else:
					validation = False
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
	if validation == True and upgrade == True:
		print("upgrading pawn")
	else:
		upgrade=False
	return validation,upgrade

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
		#reason="There is no one at given position"
		pass
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
		#reason="There is no one at given position"
		pass
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

def horse(move_possible,turn,xval_r,xval,yval_r,yval,destroy):
	global All_positions_x, All_positions_y
	global white_army, black_army
	print("validating")
	reason=""
	goto= ""
	print(turn)
	validation = True
	continue_traversing = True

	#checking the difference

	x_difference = xval_r - xval
	y_difference = yval_r - yval
	print("printing differences",x_difference,y_difference)

	#checking if required pos is traversable
	if x_difference == 0 and y_difference == 0:
		validation=False
	elif abs(x_difference) == 140 and abs(y_difference)==70:
		print("horse in first_category", validation)
	elif abs(x_difference) == 70 and abs(y_difference)==140:
		print("horse in second category", validation)
	else:
		validation=False

	#now if the required position is traversable
	#we check if there is any own army member at required position
	if move_possible==1 and turn == 1:
		if validation==True:
			continue_traversing = check_w_army_key(xval_r,yval_r)
	elif move_possible==1 and turn == 1:
		if validation==True:
			continue_traversing = check_b_army_key(xval_r,yval_r)
	if validation==True and continue_traversing == False:
		validation=False
	return validation

def cammel(move_possible,turn,xval_r,xval,yval_r,yval,destroy):
	global All_positions_x, All_positions_y
	global white_army, black_army
	print("validating")
	reason=""
	goto= ""
	print(turn)
	validation = True
	continue_traversing = True
	try :
		slope = (yval_r - yval)/(xval_r - xval)
	except ZeroDivisionError:
		slope=5
	print(slope)
	if abs(slope)!=1:
		validation = False
	if validation == True:
		if xval_r<xval and yval_r<yval:
			goto = "upleft"
		elif xval_r>xval and yval_r<yval:
			goto = "upright"
		elif xval_r<xval and yval_r>yval:
			goto = "downleft"
		elif xval_r>xval and yval_r>yval:
			goto = "downright"
	xval_new = xval
	yval_new = yval
	if goto == "":
		validation = False
	if validation == True:
		while xval_new!=xval_r and yval_new != yval_r:
			if goto == "upleft":
				xval_new = xval_new - 70
				yval_new = yval_new - 70
			elif goto == "upright":
				xval_new = xval_new + 70
				yval_new = yval_new - 70
			elif goto == "downleft":
				xval_new = xval_new - 70
				yval_new = yval_new + 70
			elif goto == "downright":
				xval_new = xval_new + 70
				yval_new = yval_new + 70
			if xval_new!=xval_r and yval_new!=yval_r:
				continue_traversing = check_w_army_key(xval_new,yval_new)
				if continue_traversing == False:
					validation = False
				continue_traversing1 = check_b_army_key(xval_new,yval_new)
				if continue_traversing1 == False:
					validation = False
			if xval_new == xval_r and yval_new == yval_r:
				if move_possible==1 and turn == 1:
					print("white to play cammel")
					continue_traversing = check_w_army_key(xval_new,yval_new)
					if continue_traversing == False:
						validation = False
				elif move_possible==1 and turn == 0:
					print("bloack to play cammel")
					continue_traversing1 = check_b_army_key(xval_new,yval_new)
					if continue_traversing1 == False:
						validation = False
	return validation

def queen(move_possible,turn,xval_r,xval,yval_r,yval,destroy):
	global All_positions_x, All_positions_y
	global white_army, black_army
	print("validating")
	reason=""
	goto= ""
	print(turn)
	validation = True
	cammel_val = False
	rook_val = False
	cammel_val = cammel(move_possible,turn,xval_r,xval,yval_r,yval,destroy)
	if cammel_val == False:
		 rook_val = rooks(move_possible,turn,xval_r,xval,yval_r,yval,destroy)
	if cammel_val==False and rook_val == False:
		validation = False
	return validation

def check_if_attacked(turn,xval_r,xval,yval_r,yval,left_or_right,destroy):
	global All_positions_x, All_positions_y
	global white_army, black_army
	print("checking")
	castling_k = True
	continue_traversing = True
	move_possible = 1
	yval_attack = yval
	xval_r_attack = xval_r
	yval_r_attack = yval_r
	turn1 = 0
	turn2 = 1
	if turn == 1:
		for army_mem in black_army:
			xval_attack = xval
			coordinate = black_army[army_mem]
			while xval_attack !=xval_r_attack and continue_traversing == True:
				if left_or_right == "right":
					xval_attack = xval_attack + 70
				elif left_or_right == "left":
					xval_attack = xval_attack - 70
				if army_mem in pawns_army:
					validation = pawn(move_possible,turn1,xval_attack,coordinate[0],yval_r,coordinate[1],destroy)
					if validation == True:
						continue_traversing = False
				elif army_mem in rooks_army:
					validation = rooks(move_possible,turn1,xval_attack,coordinate[0],yval_r,coordinate[1],destroy)
					if validation == True:
						continue_traversing = False
				elif army_mem in horse_army:
					validation = horse(move_possible,turn1,xval_attack,coordinate[0],yval_r,coordinate[1],destroy)
					if validation == True:
						continue_traversing = False
				elif army_mem in cammel_army:
					validation = cammel(move_possible,turn1,xval_attack,coordinate[0],yval_r,coordinate[1],destroy)
					if validation == True:
						continue_traversing = False
				elif army_mem in queens_army:
					validation = queen(move_possible,turn1,xval_attack,coordinate[0],yval_r,coordinate[1],destroy)
					if validation == True:
						continue_traversing = False
				elif army_mem in kings_army:
					validation = king(move_possible,turn1,xval_attack,coordinate[0],yval_r,coordinate[1],destroy)
					if validation == True:
						continue_traversing = False
	elif turn == 0:
		for army_mem in white_army:
			xval_attack = xval
			coordinate = white_army[army_mem]
			while xval_attack !=xval_r_attack and continue_traversing == True:
				if left_or_right == "right":
					xval_attack = xval_attack + 70
				elif left_or_right == "left":
					xval_attack = xval_attack - 70
				if army_mem in pawns_army:
					validation = pawn(move_possible,turn2,xval_attack,coordinate[0],yval_r,coordinate[1],destroy)
					if validation == True:
						continue_traversing = False
				elif army_mem in rooks_army:
					validation = rooks(move_possible,turn2,xval_attack,coordinate[0],yval_r,coordinate[1],destroy)
					if validation == True:
						continue_traversing = False
				elif army_mem in horse_army:
					validation = horse(move_possible,turn2,xval_attack,coordinate[0],yval_r,coordinate[1],destroy)
					if validation == True:
						continue_traversing = False
				elif army_mem in cammel_army:
					validation = cammel(move_possible,turn2,xval_attack,coordinate[0],yval_r,coordinate[1],destroy)
					if validation == True:
						continue_traversing = False
				elif army_mem in queens_army:
					validation = queen(move_possible,turn2,xval_attack,coordinate[0],yval_r,coordinate[1],destroy)
					if validation == True:
						continue_traversing = False
				elif army_mem in kings_army:
					validation = king(move_possible,turn2,xval_attack,coordinate[0],yval_r,coordinate[1],destroy)
					if validation == True:
						continue_traversing = False
	return continue_traversing

def check_finder(turn):
	global All_positions_x, All_positions_y
	global white_army, black_army
	print("check checking")
	continue_traversing = True
	validation = False
	move_possible = 1
	destroy=1
	if turn == 0:
		Pos = white_army["wKing"]
		for army_mem in black_army:
			coordinate = black_army[army_mem]
			if army_mem in pawns_army:
				#print("THERE ",army_mem,pawns_army)
				validation,upgrade = pawn(move_possible,turn,Pos[0],coordinate[0],Pos[1],coordinate[1],destroy)
				if validation == True:
					print("KING IN CHECK   KING IN CHECK")
					break
			elif army_mem in rooks_army:
				validation = rooks(move_possible,turn,Pos[0],coordinate[0],Pos[1],coordinate[1],destroy)
				if validation == True:
					print("KING IN CHECK   KING IN CHECK")
					break
			elif army_mem in horse_army:
				validation = horse(move_possible,turn,Pos[0],coordinate[0],Pos[1],coordinate[1],destroy)
				if validation == True:
					print("KING IN CHECK   KING IN CHECK")
					break
			elif army_mem in cammel_army:
				validation = cammel(move_possible,turn,Pos[0],coordinate[0],Pos[1],coordinate[1],destroy)
				if validation == True:
					print("KING IN CHECK   KING IN CHECK")
					break
			elif army_mem in queens_army:
				validation = queen(move_possible,turn,Pos[0],coordinate[0],Pos[1],coordinate[1],destroy)
				if validation == True:
					print("KING IN CHECK   KING IN CHECK")
					break
			elif army_mem in kings_army:
				validation = king(move_possible,turn,Pos[0],coordinate[0],Pos[1],coordinate[1],destroy)
				if validation == True:
					print("KING IN CHECK   KING IN CHECK")
					break
	elif turn == 1:
		Pos = black_army["bKing"]
		for army_mem in white_army:
			coordinate = white_army[army_mem]
			if army_mem in pawns_army:
				#print("THERE ",army_mem,pawns_army)
				validation,upgrade = pawn(move_possible,turn,Pos[0],coordinate[0],Pos[1],coordinate[1],destroy)
				if validation == True:
					print("KING IN CHECK   KING IN CHECK")
					break
			elif army_mem in rooks_army:
				validation = rooks(move_possible,turn,Pos[0],coordinate[0],Pos[1],coordinate[1],destroy)
				if validation == True:
					print("KING IN CHECK   KING IN CHECK")
					break
			elif army_mem in horse_army:
				validation = horse(move_possible,turn,Pos[0],coordinate[0],Pos[1],coordinate[1],destroy)
				if validation == True:
					print("KING IN CHECK   KING IN CHECK")
					break
			elif army_mem in cammel_army:
				validation = cammel(move_possible,turn,Pos[0],coordinate[0],Pos[1],coordinate[1],destroy)
				if validation == True:
					print("KING IN CHECK   KING IN CHECK")
					break
			elif army_mem in queens_army:
				validation = queen(move_possible,turn,Pos[0],coordinate[0],Pos[1],coordinate[1],destroy)
				if validation == True:
					print("KING IN CHECK   KING IN CHECK")
					break
			elif army_mem in kings_army:
				validation = king(move_possible,turn,Pos[0],coordinate[0],Pos[1],coordinate[1],destroy)
				if validation == True:
					print("KING IN CHECK   KING IN CHECK")
					break
	return validation

def check_finder1(turn,white_army_duplicate,black_army_duplicate):
	global All_positions_x, All_positions_y
	# global white_army, black_army
	print("check checking")
	continue_traversing = True
	validation = False
	move_possible = 1
	destroy=1
	if turn == 0:
		Pos = white_army_duplicate["wKing"]
		for army_mem in black_army_duplicate:
			coordinate = black_army_duplicate[army_mem]
			if army_mem in pawns_army:
				#print("THERE ",army_mem,pawns_army)
				validation,upgrade = pawn(move_possible,turn,Pos[0],coordinate[0],Pos[1],coordinate[1],destroy)
				if validation == True:
					print("KING IN CHECK   KING IN CHECK")
					break
			elif army_mem in rooks_army:
				validation = rooks(move_possible,turn,Pos[0],coordinate[0],Pos[1],coordinate[1],destroy)
				if validation == True:
					print("KING IN CHECK   KING IN CHECK")
					break
			elif army_mem in horse_army:
				validation = horse(move_possible,turn,Pos[0],coordinate[0],Pos[1],coordinate[1],destroy)
				if validation == True:
					print("KING IN CHECK   KING IN CHECK")
					break
			elif army_mem in cammel_army:
				validation = cammel(move_possible,turn,Pos[0],coordinate[0],Pos[1],coordinate[1],destroy)
				if validation == True:
					print("KING IN CHECK   KING IN CHECK")
					break
			elif army_mem in queens_army:
				validation = queen(move_possible,turn,Pos[0],coordinate[0],Pos[1],coordinate[1],destroy)
				if validation == True:
					print("KING IN CHECK   KING IN CHECK")
					break
			elif army_mem in kings_army:
				validation = king(move_possible,turn,Pos[0],coordinate[0],Pos[1],coordinate[1],destroy)
				if validation == True:
					print("KING IN CHECK   KING IN CHECK")
					break
	elif turn == 1:
		Pos = black_army_duplicate["bKing"]
		for army_mem in white_army_duplicate:
			coordinate = white_army_duplicate[army_mem]
			if army_mem in pawns_army:
				#print("THERE ",army_mem,pawns_army)
				validation,upgrade = pawn(move_possible,turn,Pos[0],coordinate[0],Pos[1],coordinate[1],destroy)
				if validation == True:
					print("KING IN CHECK   KING IN CHECK")
					break
			elif army_mem in rooks_army:
				validation = rooks(move_possible,turn,Pos[0],coordinate[0],Pos[1],coordinate[1],destroy)
				if validation == True:
					print("KING IN CHECK   KING IN CHECK")
					break
			elif army_mem in horse_army:
				validation = horse(move_possible,turn,Pos[0],coordinate[0],Pos[1],coordinate[1],destroy)
				if validation == True:
					print("KING IN CHECK   KING IN CHECK")
					break
			elif army_mem in cammel_army:
				validation = cammel(move_possible,turn,Pos[0],coordinate[0],Pos[1],coordinate[1],destroy)
				if validation == True:
					print("KING IN CHECK   KING IN CHECK")
					break
			elif army_mem in queens_army:
				validation = queen(move_possible,turn,Pos[0],coordinate[0],Pos[1],coordinate[1],destroy)
				if validation == True:
					print("KING IN CHECK   KING IN CHECK")
					break
			elif army_mem in kings_army:
				validation = king(move_possible,turn,Pos[0],coordinate[0],Pos[1],coordinate[1],destroy)
				if validation == True:
					print("KING IN CHECK   KING IN CHECK")
					break
	return validation
def king(move_possible,turn,xval_r,xval,yval_r,yval,destroy):
	global All_positions_x, All_positions_y
	global white_army, black_army
	global w_king_movement,w_rook_movement,w_rookR_movement,b_king_movement,b_rook_movement,b_rookR_movement
	print("validating")
	reason=""
	goto= ""
	print(turn)
	validation = True
	continue_traversing = True
	continue_traversing3 = True
	continue_traversing4 = True
	castling_k = False
	castle_clear = True
	new_xval = xval
	lastpos_castle=0
	#check for the castling :: check rooks, king and the  

	if xval_r == xval+140 or xval_r == xval - 140:
		if yval_r == yval and destroy == 0:	
			if move_possible==1 and turn == 1 and w_king_movement==0:
				if xval_r == xval + 140 and w_rookR_movement==0:
					while castle_clear == True and lastpos_castle == 0:
						new_xval = new_xval+70
						continue_traversing3 = check_w_army_key(new_xval,yval_r)
						continue_traversing4 = check_b_army_key(new_xval,yval_r)
						if new_xval == 430:
							lastpos_castle= 1
					if continue_traversing3 == True and continue_traversing4 == True:
						castling_k = check_if_attacked(turn,xval_r,xval,yval_r,yval,"right",destroy)
						if castling_k == True:
							white_army["wRookR"]=[xval_r-70,yval_r]
				elif xval_r == xval - 140 and w_rook_movement==0:
					while lastpos_castle == 0:
						new_xval = new_xval-70
						print("lastloop",lastpos_castle)
						continue_traversing3 = check_w_army_key(new_xval,yval_r)
						print(continue_traversing3)
						continue_traversing4 = check_b_army_key(new_xval,yval_r)
						print(continue_traversing4)
						if new_xval == 80:
							lastpos_castle= 1
					if continue_traversing3 == True and continue_traversing4 == True:
						castling_k = check_if_attacked(turn,xval_r,xval,yval_r,yval,"left",destroy)
						if castling_k == True:
							white_army["wRook"]=[xval_r+70,yval_r]
			elif move_possible==1 and turn == 0 and b_king_movement==0:
				if xval_r == xval + 140 and b_rookR_movement==0:
					while castle_clear == True and lastpos_castle == 0:
						new_xval = new_xval+70
						continue_traversing3 = check_w_army_key(new_xval,yval_r)
						continue_traversing4 = check_b_army_key(new_xval,yval_r)
						if new_xval == 430:
							lastpos_castle= 1
					if continue_traversing3 == True and continue_traversing4 == True:
						castling_k = check_if_attacked(turn,xval_r,xval,yval_r,yval,"right",destroy)
						if castling_k == True:
							black_army["bRookR"]=[xval_r-70,yval_r]
				elif xval_r == xval - 140 and b_rook_movement==0:
					while castle_clear == True and lastpos_castle == 0:
						new_xval = new_xval-70
						continue_traversing3 = check_w_army_key(new_xval,yval_r)
						continue_traversing4 = check_b_army_key(new_xval,yval_r)
						if new_xval == 80:
							lastpos_castle= 1
					if continue_traversing3 == True and continue_traversing4 == True:
						castling_k = check_if_attacked(turn,xval_r,xval,yval_r,yval,"left",destroy)
						if castling_k == True:
							black_army["bRook"]=[xval_r+70,yval_r]
	if castling_k == False:
		if move_possible==1 and turn == 1:
			if xval_r<=xval+70 and xval_r >=xval-70:
				if yval_r>=yval-70 and yval_r<=yval+70:
					print("king move possible")
					continue_traversing = check_w_army_key(xval_r,yval_r)
				else:
					validation = False
			else:
				validation = False
		elif move_possible==1 and turn == 0:
			if xval_r<=xval+70 and xval_r >=xval-70:
				if yval_r>=yval-70 and yval_r <= yval+70:
					print("king move possible")
					continue_traversing = check_b_army_key(xval_r,yval_r)
				else:
					validation = False
			else:
				validation = False
		if validation == True and continue_traversing == True:
			validation = True
		else:
			validation = False
	return validation

def add_upgraded_member_pawn(army_member, turn,xval_r,yval_r):
	global All_positions_x, All_positions_y
	global white_army, black_army
	global w_king_movement,w_rook_movement,w_rookR_movement,b_king_movement,b_rook_movement,b_rookR_movement
	print("adding upgraded pawn ")
	text_command1 = ""
	if turn == 1:
		while  text_command1!="A1" and text_command1!="B1" and text_command1!="C1"and text_command1!="D1":
			#text_command1 = detect_speech()
			text_command1 = input("move D7 To D6{}".format(turn))
		if text_command1=="A1":
			im2 = cv2.imread("../images/wRook.png", cv2.IMREAD_UNCHANGED)
			rooks_army.insert(0,rooks_army[0]+text_command1)
			cv2.imwrite("../images/"+rooks_army[0]+".png",im2)
			del white_army[army_member]
			white_army[rooks_army[0]]=[xval_r,yval_r]
			print(white_army)
		elif text_command1=="B1":
			horse_army.insert(0,horse_army[0]+text_command1)
			im2 = cv2.imread("../images/wHorse.png", cv2.IMREAD_UNCHANGED)
			cv2.imwrite("../images/"+horse_army[0]+".png",im2)
			del white_army[army_member]
			white_army[horse_army[0]]=[xval_r,yval_r]
		elif text_command1=="C1":
			cammel_army.insert(0,cammel_army[0]+text_command1)
			im2 = cv2.imread("../images/{}.png".format("wCammel"), cv2.IMREAD_UNCHANGED)
			cv2.imwrite("../images/"+cammel_army[0]+".png",im2)
			del white_army[army_member]
			white_army[cammel_army[0]]=[xval_r,yval_r]
		elif text_command1=="D1":
			queens_army.insert(0,queens_army[0]+text_command1)
			im2 = cv2.imread("../images/{}.png".format("wQueen"), cv2.IMREAD_UNCHANGED)
			cv2.imwrite("../images/"+queens_army[0]+".png",im2)
			del white_army[army_member]
			white_army[queens_army[0]]=[xval_r,yval_r]
	if turn == 0:
		while  text_command1!="A8" and text_command1!="B8" and text_command1!="C8"and text_command1!="D8":
			#text_command1 = detect_speech()
			text_command1 = input("move D7 To D6{}".format(turn))
		if text_command1=="A8":
			rooks_army.insert(0,rooks_army[0]+text_command1)
			im2 = cv2.imread("../images/{}.png".format("bRook"), cv2.IMREAD_UNCHANGED)
			cv2.imwrite("../images/"+rooks_army[0]+".png",im2)
			del black_army[army_member]
			black_army[rooks_army[0]]=[xval_r,yval_r]
		elif text_command1=="B8":
			horse_army.insert(0,horse_army[0]+text_command1)
			im2 = cv2.imread("../images/{}.png".format("bHorse"), cv2.IMREAD_UNCHANGED)
			cv2.imwrite("../images/"+horse_army[0]+".png",im2)
			del black_army[army_member]
			black_army[horse_army[0]]=[xval_r,yval_r]
		elif text_command1=="C8":
			cammel_army.insert(0,cammel_army[0]+text_command1)
			im2 = cv2.imread("../images/{}.png".format("bCammel"), cv2.IMREAD_UNCHANGED)
			cv2.imwrite("../images/"+cammel_army[0]+".png",im2)
			del black_army[army_member]
			black_army[cammel_army[0]]=[xval_r,yval_r]
		elif text_command1=="D8":
			queens_army.insert(0,queens_army[0]+text_command1)
			im2 = cv2.imread("../images/{}.png".format("bQueen"), cv2.IMREAD_UNCHANGED)
			cv2.imwrite("../images/"+queens_army[0]+".png",im2)
			del black_army[army_member]
			black_army[queens_army[0]]=[xval_r,yval_r]


pawns_army = ["wPawn1","wPawn2","wPawn3","wPawn4","wPawn5","wPawn6","wPawn7","wPawn8",
				"bPawn1","bPawn2","bPawn3","bPawn4","bPawn5","bPawn6","bPawn7","bPawn8"]
rooks_army = ["wRook","wRookR","bRook","bRookR"]
horse_army = ["wHorse","wHorseR","bHorse","bHorseR"]
cammel_army = ["wCammel","wCammelR","bCammel","bCammelR"]
queens_army = ["wQueen","bQueen"]
kings_army = ["wKing","bKing"]
w_king_movement = 0
w_rook_movement = 0
w_rookR_movement = 0
b_king_movement = 0
b_rook_movement = 0
b_rookR_movement = 0

def destroy_member(xval_r,yval_r):
	global back
	print("destroy")
	# boardn = cv2.imread("../images/grid1.png", cv2.IMREAD_UNCHANGED)
	im1 = cv2.imread("../images/destroy.png", cv2.IMREAD_UNCHANGED)
	im3 = cv2.imread("../images/desBattle.png", cv2.IMREAD_UNCHANGED)
	im2 = cv2.cvtColor(im1,cv2.COLOR_BGRA2RGBA)
	im4 = cv2.cvtColor(im3,cv2.COLOR_BGRA2RGBA)
	step = 10
	cv2.destroyWindow('Voice Chess')
	back1 = overlay_transparent(back.copy(), im2, xval_r-50,yval_r)
	cv2.imshow('Voice Chess',cv2.cvtColor(back1,cv2.COLOR_BGR2RGB))
	cv2.waitKey(700)
	while step <=580:
		back1 = overlay_transparent(back.copy(), im4, xval_r,yval_r)
		cv2.imshow('Voice Chess',cv2.cvtColor(back1,cv2.COLOR_BGR2RGB))
		cv2.waitKey(700)
		im4 = cv2.rotate(im4, cv2.ROTATE_90_CLOCKWISE) 
		step=step+70

def check_anim(turn):
	global back
	global white_army, black_army
	print("destroy")
	# boardn = cv2.imread("../images/grid1.png", cv2.IMREAD_UNCHANGED)
	im1 = cv2.imread("../images/check.png", cv2.IMREAD_UNCHANGED)
	im3 = cv2.imread("../images/checkk.png", cv2.IMREAD_UNCHANGED)
	im2 = cv2.cvtColor(im1,cv2.COLOR_BGRA2RGBA)
	im4 = cv2.cvtColor(im3,cv2.COLOR_BGRA2RGBA)
	step = 10
	cv2.destroyWindow('Voice Chess')
	if turn == 0:
		coordinates=white_army["wKing"]
		xval_r = coordinates[0]
		yval_r = coordinates[1]
		back1 = overlay_transparent(back.copy(), im2, xval_r-50,yval_r)
		cv2.imshow('Voice Chess',cv2.cvtColor(back1,cv2.COLOR_BGR2RGB))
		cv2.waitKey(700)
		while step <=580:
			back1 = overlay_transparent(back.copy(), im4, xval_r,yval_r)
			cv2.imshow('Voice Chess',cv2.cvtColor(back1,cv2.COLOR_BGR2RGB))
			cv2.waitKey(700)
			im4 = cv2.rotate(im4, cv2.ROTATE_90_CLOCKWISE) 
			step=step+70
	if turn == 1:
		coordinates=black_army["bKing"]
		xval_r = coordinates[0]
		yval_r = coordinates[1]
		back1 = overlay_transparent(back.copy(), im2, xval_r-50,yval_r)
		cv2.imshow('Voice Chess',cv2.cvtColor(back1,cv2.COLOR_BGR2RGB))
		cv2.waitKey(700)
		while step <=580:
			back1 = overlay_transparent(back.copy(), im4, xval_r,yval_r)
			cv2.imshow('Voice Chess',cv2.cvtColor(back1,cv2.COLOR_BGR2RGB))
			cv2.waitKey(700)
			im4 = cv2.rotate(im4, cv2.ROTATE_90_CLOCKWISE) 
			step=step+70

def possible_positions(text_command,turn):
	#here we validate positions and move accordingly
	global All_positions_x, All_positions_y
	global white_army, black_army
	global w_king_movement,w_rook_movement,w_rookR_movement,b_king_movement,b_rook_movement,b_rookR_movement
	print("validating")
	reason=""
	#
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
			print("THERE ",army_member,pawns_army)
			validation,upgrade = pawn(move_possible,turn,xval_r,xval,yval_r,yval,destroy)
		elif army_member in rooks_army:
			validation = rooks(move_possible,turn,xval_r,xval,yval_r,yval,destroy)
		elif army_member in horse_army:
			validation = horse(move_possible,turn,xval_r,xval,yval_r,yval,destroy)
		elif army_member in cammel_army:
			validation = cammel(move_possible,turn,xval_r,xval,yval_r,yval,destroy)
		elif army_member in queens_army:
			validation = queen(move_possible,turn,xval_r,xval,yval_r,yval,destroy)
		elif army_member in kings_army:
			validation = king(move_possible,turn,xval_r,xval,yval_r,yval,destroy)
	#now we check required position

	white_army_duplicate = white_army.copy()
	black_army_duplicate = black_army.copy()
	if validation == True and move_possible == 1 and turn == 1:
		if army_member =="wRook":
			w_rook_movement = 1
		elif army_member =="wRookR":
			w_rookR_movement = 1
		elif army_member =="wKing":
			w_king_movement = 1
		white_army[army_member]=[xval_r,yval_r]
		print(white_army)
		if destroy == 1:
			destroy_member(xval_r,yval_r)
			del black_army[member_to_destroy]
		checkk_self = check_finder(0 if turn == 1 else 1)
		if checkk_self == False:
			if army_member in pawns_army:
				if upgrade == True:
					add_upgraded_member_pawn(army_member,turn,xval_r,yval_r)
			checkk = check_finder(turn)
			print("printing checkk",checkk)
			if checkk == True:
				check_anim(turn)
		else:
			validation = False
			white_army = white_army_duplicate
			black_army = black_army_duplicate
	elif validation == True and move_possible == 1 and turn == 0:
		if army_member =="bRook":
			b_rook_movement = 1
		elif army_member =="bRookR":
			b_rookR_movement = 1
		elif army_member =="bKing":
			b_king_movement = 1
		black_army[army_member]=[xval_r,yval_r]
		print(black_army)
		if destroy == 1:
			destroy_member(xval_r,yval_r)
			del white_army[member_to_destroy]
		checkk_self = check_finder(0 if turn == 1 else 1)
		if checkk_self == False:
			if army_member in pawns_army:
				if upgrade == True:
					add_upgraded_member_pawn(army_member,turn,xval_r,yval_r)
			checkk = check_finder(turn)
			print("printing checkk",checkk)
			if checkk == True:
				check_anim(turn)
		else:
			validation = False
			white_army = white_army_duplicate
			black_army = black_army_duplicate
	return validation


back=[]
white_army = {"wRook":[10,500],"wHorse":[80,500],"wCammel":[150,500],"wQueen":[220,500],"wKing":[290,500],"wCammelR":[360,500],"wHorseR":[430,500],"wRookR":[500,500],
				"wPawn1":[10,430],"wPawn2":[80,430],"wPawn3":[150,430],"wPawn4":[220,430],"wPawn5":[290,430],"wPawn6":[360,430],"wPawn7":[430,430],"wPawn8":[500,430]}

black_army = {"bRook":[10,10],"bHorse":[80,10],"bCammel":[150,10],"bQueen":[220,10],"bKing":[290,10],"bCammelR":[360,10],"bHorseR":[430,10],"bRookR":[500,10],
				"bPawn1":[10,80],"bPawn2":[80,80],"bPawn3":[150,80],"bPawn4":[220,80],"bPawn5":[290,80],"bPawn6":[360,80],"bPawn7":[430,80],"bPawn8":[500,80]}
def allot_army_positions(board):
	global white_army, black_army,back
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

def detect_speech(turn):
	#https://www.journaldev.com/37873/python-speech-to-text-speechrecognition
	text_output=""
	store = SRG.Recognizer()
	with SRG.Microphone() as s:
		print("Give command to your {} army".format( "white_army" if turn == 1 else "black_army"))
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
	global white_army, black_army, back
	turn = 1   #turn 1 means white to play :: and :: turn 0 means black to play
	board = cv2.imread("../images/grid2.png", cv2.IMREAD_UNCHANGED)
	board1=board.copy()
	back = allot_army_positions(board.copy())
	move_made = False
	while True:
		text_command = detect_speech(turn)
		#text_command = input("move D7 To D6{}".format(turn))
		print(text_command)
		if text_command!="":
			print(turn)
			move_made = possible_positions(text_command,turn)
		if move_made == True and text_command!="":
			move_made = False
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

