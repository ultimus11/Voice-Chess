import cv2
import numpy as np
import matplotlib.pyplot as plt
import PIL
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
def allot_army_positions(board):
	white_army = {"wRook":[10,500],"wHorse":[80,500],"wCammel":[150,500],"wQueen":[290,500],"wKing":[220,500],"wCammelR":[360,500],"wHorseR":[430,500],"wRookR":[500,500],
					"wPawn1":[10,430],"wPawn2":[80,430],"wPawn3":[150,430],"wPawn4":[290,430],"wPawn5":[220,430],"wPawn6":[360,430],"wPawn7":[430,430],"wPawn8":[500,430]}
	firsttime=0
	for elements in white_army:
		print(elements,white_army[elements])
		im2 = cv2.imread("../images/{}.png".format(elements), cv2.IMREAD_UNCHANGED)
		#print(lable_grid(board))
		if firsttime ==0:
			back = overlay_transparent(board, im2, white_army[elements][0], white_army[elements][1])
			firsttime+=1
		elif firsttime!=0:
			back = overlay_transparent(back, im2, white_army[elements][0], white_army[elements][1])
	black_army = {"bRook":[10,10],"bHorse":[80,10],"bCammel":[150,10],"bQueen":[220,10],"bKing":[290,10],"bCammelR":[360,10],"bHorseR":[430,10],"bRookR":[500,10],
					"bPawn1":[10,80],"bPawn2":[80,80],"bPawn3":[150,80],"bPawn4":[290,80],"bPawn5":[220,80],"bPawn6":[360,80],"bPawn7":[430,80],"bPawn8":[500,80]}
	for elements in black_army:
		print(elements,black_army[elements])
		im2 = cv2.imread("../images/{}.png".format(elements), cv2.IMREAD_UNCHANGED)
		#print(lable_grid(board))
		back = overlay_transparent(back, im2, black_army[elements][0], black_army[elements][1])
	return back
def show_frames():
	board = cv2.imread("../images/grid.png", cv2.IMREAD_UNCHANGED)
	back = allot_army_positions(board)
	# back_im = board.copy()
	# back_im.paste(im2, (100, 50))
	# plt.imshow(board, cmap='gray')  # graph it
	# plt.show()
	while True:
		cv2.imshow('Voice Chess',cv2.cvtColor(back,cv2.COLOR_BGR2RGB))
		#cv2.imshow('Voice Chess',cv2.cvtColor(back_im,cv2.COLOR_BGR2RGB))
		if cv2.waitKey(25)&0xFF==('q'):
			cv2.destroyAllWindows()
			break
#print(lable_grid())
#allot_army_positions()
show_frames()