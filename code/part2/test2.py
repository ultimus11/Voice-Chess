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

def possible_positions(text_command):
	#here we validate positions and move accordingly
	global All_positions_x, All_positions_y
	global white_army, black_army
	print("validating")
	reason=""
	interested_text_area = text_command[5:]
	print("Current position",interested_text_area[:2])
	print("required position:",interested_text_area[6:])
	Current_position = interested_text_area[:2]
	required_position = interested_text_area[6:]

	#we check which army member is at current position
	xval = All_positions_x[Current_position[0]]
	yval = All_positions_y[Current_position[1]]
	print(xval,yval)
	try:
		army_member = list(white_army.keys())[list(white_army.values()).index([xval,yval])]
		print(army_member)
		xval_r = All_positions_x[required_position[0]]
		yval_r = All_positions_y[required_position[1]]
		print(xval_r,yval_r)
		
		#now we will check if required position is valid : : :  This is for pawns remember destryoing condition is not given
		if xval_r == xval and yval_r == yval-70:
			validation = True
		elif xval_r == xval and yval==430 and yval_r == yval-140:
			validation = True
		else:
			validation = False

		#now we move if valid condition
		print("validation", validation)
	except ValueError:
		validation = False
		reason="There is no one at given position"
	#now we check required position


	if validation == True:
		white_army[army_member]=[xval_r,yval_r]
		print(white_army)



white_army = {"wRook":[10,500],"wHorse":[80,500],"wCammel":[150,500],"wQueen":[290,500],"wKing":[220,500],"wCammelR":[360,500],"wHorseR":[430,500],"wRookR":[500,500],
				"wPawn1":[10,430],"wPawn2":[80,430],"wPawn3":[150,430],"wPawn4":[290,430],"wPawn5":[220,430],"wPawn6":[360,430],"wPawn7":[430,430],"wPawn8":[500,430]}

black_army = {"bRook":[10,10],"bHorse":[80,10],"bCammel":[150,10],"bQueen":[290,10],"bKing":[220,10],"bCammelR":[360,10],"bHorseR":[430,10],"bRookR":[500,10],
				"bPawn1":[10,80],"bPawn2":[80,80],"bPawn3":[150,80],"bPawn4":[290,80],"bPawn5":[220,80],"bPawn6":[360,80],"bPawn7":[430,80],"bPawn8":[500,80]}
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
	board = cv2.imread("../images/grid.png", cv2.IMREAD_UNCHANGED)
	board1=board.copy()
	back = allot_army_positions(board.copy())
	while True:
		text_command = detect_speech()
		#text_command = "move D2 To D4"
		print(text_command)
		try:
			possible_positions(text_command)
		except:
			pass
		back = allot_army_positions(board.copy())
		cv2.imshow('Voice Chess',cv2.cvtColor(back,cv2.COLOR_BGR2RGB))
		#cv2.imshow('Voice Chess',cv2.cvtColor(back_im,cv2.COLOR_BGR2RGB))
		if cv2.waitKey(25)&0xFF==('q'):
			cv2.destroyAllWindows()
			break
#print(lable_grid())
#allot_army_positions()
show_frames()
