ver = '1.1.0'
import pygame
import time
import os
import files_module as f_m
import threading
import urllib
import requests



def start_timer():
	global start_time
	start_time = 0
	start_time = time.time()

def stop_timer():
	global stop_time
	stop_time = time.time() - start_time

def check_timer():
	return stop_time



def start_timer2():
	global start_time2
	start_time = time.time()

def stop_timer2():
	return time.time() - start_time2

cl_white = (255,255,255)
cl_black = (0,0,0)
cl_grey = (50,50,50)
cl_lgrey = (150,150,150)
cl_red = (220,50,50)
cl_green = (50,255,50)
cl_yellow = (255,255,0)
cl_blue = (0,0,255)




#тут из файла настройки считываются
settings_f = open('settings.txt','r')

settings_s = settings_f.read()
for i in range(0,len(settings_s.split())):
	exec(settings_s.split()[i])



if resolution == '360p':
	xx = 640
	yy = 360
if resolution == '480p':
	xx = 854
	yy = 480
if resolution == '720p':
	xx = 1280
	yy = 720
if resolution == '900p':
	xx = 1600
	yy = 900
if resolution == '1080p':
	xx = 1920
	yy = 1080

screen_k = xx/854


pygame.init()
if fullscreen:
	screen = pygame.display.set_mode((xx,yy),pygame.FULLSCREEN)
else:
	screen = pygame.display.set_mode((xx,yy))
pygame.display.set_caption('LOGIC')



#переменные дял работы со стабилизацией фпс
target_fps = 60
fps_limiter = False
current_fps = target_fps
delayy = 1
physics_fps = 60
time_ratio = round(physics_fps / current_fps,4)


ver_url = 'https://raw.githubusercontent.com/DaHataaa/LOGIC_SERVER/main/version'
code_url = 'https://raw.githubusercontent.com/DaHataaa/LOGIC_SERVER/main/logic.py'
online_maps_url = 'https://raw.githubusercontent.com/DaHataaa/LOGIC_SERVER/main/online%20maps/'



#состояния клавиш
k_ctrl = False
k_shift = False
k_alt = False
k_space = False
k_space_count = 1
k_r = False
k_e = False
k_v = False
k_x = False
k_d = False
mouse_touching_l = False
mouse_touching_r = False

help_i = 0

selecting_step = 0

do_logic = 1

linee = ''


#переменные характеристики сетки и интерфейса
corner_x = 0
corner_y = 0
sq_size = 20

help_text = ['w,a,s,d - Block directions',
			 '1-8 - Block chosing',
			 'LMB - Place block',
			 'RMB (hold) - Navigation',
			 'Mouse Wheel - Scale',
			 'R - Remove block',
			 'Space - Play/Pause',
			 'ESC - Menu',
			 'E (hold) - Select and copy area to clipboard',
			 'Ctrl+V - Paste area from clipboard',
			 'Ctrl+X - Cut selected area',
			 'Ctrl+D - Clear clipboard (Deselect)',
			 'Ctrl+S - Save current map',
			 'Ctrl+Alt+S - Save as new map']



#переменные для редактора
direction = 'u'
blocks = ['arrow','getter','bridge','connector','power','not','and','xor']
blocks_i = 0

connector_i = 0
conn_x1 = 0
conn_y1 = 0

blocks_png = [0]*8
for i in range(8):
	blocks_png[i] = [['','','',''],['','','','']]

for i_b in range(8):
	for i_s in range(2):
		for i_d in range(4):
			blocks_png[i_b][i_s][i_d] = pygame.image.load('data/gfx/'+blocks[i_b]+'/'+blocks[i_b]+'_'+'ft'[i_s]+'urld'[i_d]+'.png')



pi = 3.141592653589793238462643383279




symbols = [[pygame.K_q,'q'],[pygame.K_w,'w'],[pygame.K_e,'e'],[pygame.K_r,'r'],[pygame.K_t,'t'],[pygame.K_y,'y'],
		   [pygame.K_u,'u'],[pygame.K_i,'i'],[pygame.K_o,'o'],[pygame.K_p,'p'],
		   [pygame.K_a,'a'],[pygame.K_s,'s'],[pygame.K_d,'d'],[pygame.K_f,'f'],[pygame.K_g,'g'],[pygame.K_h,'h'],
		   [pygame.K_j,'j'],[pygame.K_k,'k'],[pygame.K_l,'l'],[pygame.K_z,'z'],
		   [pygame.K_x,'x'],[pygame.K_c,'c'],[pygame.K_v,'v'],[pygame.K_b,'b'],[pygame.K_n,'n'],[pygame.K_m,'m'],
		   [pygame.K_SLASH,'/'],[pygame.K_MINUS,'-'],[pygame.K_SPACE,' '],[pygame.K_1,'1'],[pygame.K_2,'2'],[pygame.K_3,'3'],
		   [pygame.K_4,'4'],[pygame.K_5,'5'],[pygame.K_6,'6'],[pygame.K_7,'7'],[pygame.K_8,'8'],[pygame.K_9,'9'],
		   [pygame.K_0,'0']]




def deg(alpha_rad):
	return alpha_rad * (180/pi)

def rad(alpha_deg):
	return alpha_deg * (pi/180)

def dist(x1,y1,x2,y2):
	return m.sqrt((x1-x2)**2 + (y1-y2)**2)

def line(x,y,x2,y2,color,width):
	pygame.draw.line(screen,color,(x,y),(x2,y2),width)

def line_a(x,y,lenght,angle,color,width):
	x2 = x + lenght*cos(rad(angle))
	y2 = y - lenght*sin(rad(angle))
	pygame.draw.aaline(screen,color,(x,y),(x2,y2),width)


def circle(x,y,color,width):
	pygame.draw.circle(screen,color,(x,y),width)

def rect(x,y,lenght,height,color,width):
	pygame.draw.rect(screen,color,(x,y,lenght,height),width)

font = [0]*128
for i in range(2,128):
	font[i] = pygame.font.Font('data/other/fnaf.ttf',i)

def textout(x,y,size,color,text):
	out = font[size].render(text, 1, color)
	screen.blit(out,(x,y))


def get_maps_names():
	names = open('data/maps/maps_list.txt','r',encoding='utf8').readlines()
	for i in range(len(names)):
		names[i] = names[i].replace('\n','')
	return names

def get_online_maps_names():
	download_git(online_maps_url+'online_maps_list.txt','data/online_maps/online_maps_list.txt')
	
	online_names = open('data/online_maps/online_maps_list.txt','r',encoding='utf8').readlines()
	for i in range(len(online_names)):
		online_names[i] = online_names[i].replace('\n','')
	return online_names
	




def clear_field():
	global field
	global field_l
	global field_l_buf
	field = [0]*256
	for i in range(256):
		field[i] = ['0']*256

	field_l = [0]*256
	for i in range(256):
		field_l[i] = [0]*256

	field_l_buf = [0]*256
	for i in range(256):
		field_l_buf[i] = [0]*256







def download_git(url,name):
	urllib.request.urlretrieve(url,name)



class menu():
	def main():
		global field
		global field_l
		global names
		global mouse_x
		global mouse_y
		global mouse_touching_l
		global mouse_touching_r
		global menu_running
		global linee
		global names_online
		global connection

		mouse_x = xx/2 + 200
		mouse_y = yy/2

		menu_running = True
		

		

		if connection:
			try:
				os.remove('data/actual_ver.txt')
				os.remove('data/online_maps/online_maps_list.txt')
			except:
				1
			names_online = get_online_maps_names()
			download_git(ver_url,'data/actual_ver.txt')
			actual_ver = open('data/actual_ver.txt','r').readlines()[0].replace('\n','')

		names = get_maps_names()

		def menu_interface_and_events():

			global field
			global field_l
			global names
			global mouse_x
			global mouse_y
			global mouse_touching_l
			global mouse_touching_r
			global menu_running
			global linee

			line(0,0,xx,0,cl_black,2)
			textout(xx//2-50*screen_k,7,int(30*screen_k),cl_black,'LOGIC '+ver)
			line(0,50*screen_k,xx,50*screen_k,cl_black,2)



			textout(xx//2+10*screen_k,62*screen_k,int(20*screen_k),cl_black,'Local maps:')
			textout(xx//4*3+10*screen_k,62*screen_k,int(20*screen_k),cl_black,'Online maps:')
			textout(xx//2+10*screen_k,yy-14*screen_k,int(10*screen_k),cl_black,'LMC-Choose map | RMC-Delete map')
			textout(xx//4*3+10*screen_k,yy-14*screen_k,int(10*screen_k),cl_black,'LMC-Choose map')
			menu_text = ['Start empty','Continue','Quit','','','','','','','','','']
			if connection:
				if actual_ver != ver:
					menu_text[11] = ('Update to '+actual_ver)
			else:
				menu_text[11] = ('Offline mode')
			for i in range(len(menu_text)):
				if mouse_x >= 10*screen_k and mouse_x < len(menu_text[i])*14*screen_k and mouse_y >= 62*screen_k+i*34*screen_k and mouse_y < 60*screen_k+i*34*screen_k+34*screen_k:
					textout(10*screen_k,62*screen_k+i*34*screen_k,int(20*screen_k),cl_red,menu_text[i])
					if mouse_touching_l:
						if menu_text[i] == 'Quit':
							1/0
						elif menu_text[i] == 'Start empty':
							for i in range(256):
								field[i] = ['0']*256
							menu_running = False
							linee = ''
						elif menu_text[i] == 'Continue':
							menu_running = False
						elif menu_text[i].split()[0] == 'Update':
							rect(10*screen_k,62*screen_k+i*34*screen_k,(xx//2),int(25*screen_k),cl_white,0)
							textout(10*screen_k,62*screen_k+i*34*screen_k,int(20*screen_k),cl_red,'Updating...')
							pygame.display.flip()
							os.remove('logic.py')
							download_git(code_url,'logic.py')
							time.sleep(1)
							os.startfile('logic.py')
							1/0
						mouse_touching_l = False
				else:
					textout(10*screen_k,62*screen_k+i*34*screen_k,int(20*screen_k),cl_black,menu_text[i])

			line(xx//2,50*screen_k,xx//2,yy,cl_black,2)
			line(xx//4*3,50*screen_k,xx//4*3,yy,cl_black,2)

			for i in range(len(names)):
				if mouse_x >= xx//2+10*screen_k and mouse_x < xx//4*3 and mouse_y >= 95*screen_k+i*20*screen_k and mouse_y < 95*screen_k+i*20*screen_k+20*screen_k:
					textout(xx//2+10*screen_k,95*screen_k+i*20*screen_k,int(12*screen_k),cl_red,names[i])
					if mouse_touching_l:
						rect(xx//2+10*screen_k,95*screen_k,xx//4-11*screen_k,yy//3*2,cl_white,0)
						textout(xx//2+10*screen_k,95*screen_k+i*20*screen_k,int(12*screen_k),cl_red,'Loading...')
						pygame.display.flip()
						clear_field()
						field,field_l = f_m.load_map(names[i])
						menu_running = False
						linee = names[i]
					if mouse_touching_r:
						mouse_touching_r = False
						f_m.delete_map(names[i])
						names = get_maps_names()
						break
				else:
					textout(xx//2+10*screen_k,95*screen_k+i*20*screen_k,int(12*screen_k),cl_black,names[i])



			for i in range(len(names_online)):
				if mouse_x >= xx//4*3+10*screen_k and mouse_x < xx and mouse_y >= 95*screen_k+i*20*screen_k and mouse_y < 95*screen_k+i*20*screen_k+20*screen_k:
					textout(xx//4*3+10*screen_k,95*screen_k+i*20*screen_k,int(12*screen_k),cl_red,names_online[i])
					if mouse_touching_l:
						rect(xx//4*3+10*screen_k,95*screen_k,xx//4-11*screen_k,yy//3*2,cl_white,0)
						textout(xx//4*3+10*screen_k,95*screen_k+i*20*screen_k,int(12*screen_k),cl_red,'Loading...')
						pygame.display.flip()
						clear_field()
						download_git(online_maps_url+names_online[i].replace(' ','%20')+'.mp','data/online_maps/'+names_online[i]+'.mp')
						field,field_l = f_m.load_online_map(names_online[i])
						menu_running = False
						linee = names_online[i]
				else:
					textout(xx//4*3+10*screen_k,95*screen_k+i*20*screen_k,int(12*screen_k),cl_black,names_online[i])


		
		while menu_running:


			mouse_pos = pygame.mouse.get_pos()

			mouse_xl = mouse_x
			mouse_yl = mouse_y

			mouse_x = mouse_pos[0]
			mouse_y = mouse_pos[1]


			screen.fill(cl_white)

			menu_interface_and_events()



			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					1 / 0

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LCTRL:
						k_ctrl = True


				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						mouse_touching_l = True

					if event.button == 3:
						mouse_touching_r = True

				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						mouse_touching_l = False

					if event.button == 3:
						mouse_touching_r = False


				pygame.display.flip()




def main_func():
	global corner_x
	global corner_y
	global field_l
	global blocks_i
	global grid_x
	global grid_y
	global connector_i
	global conn_x1
	global conn_y1
	global mouse_touching_l


	
	grid_x = corner_x
	grid_y = corner_y
	if mouse_touching_r:
		corner_x += mouse_x - mouse_xl
		corner_y += mouse_y - mouse_yl


	
	for ix in range(256):
		for iy in range(256):
			if -sq_size < grid_x+ix*sq_size < xx-100 and -sq_size < grid_y+iy*sq_size < yy:
				calc_iy = (mouse_y-grid_y)//sq_size
				calc_ix = (mouse_x-grid_x)//sq_size
				if mouse_touching_l:
					if mouse_x < xx-100*screen_k and calc_ix < 255 and calc_iy < 255 and calc_ix >= 0 and calc_iy >= 0:
						if field[calc_iy][calc_ix].split('_')[0] == 'connector':
							if connector_i == 0:
								conn_x1 = calc_ix
								conn_y1 = calc_iy
								field[calc_iy][calc_ix] = blocks[blocks_i]+'_f'+direction
							else:
								field[calc_iy][calc_ix] = blocks[blocks_i]+'_f'+direction+'_'+str(conn_x1)+'_'+str(conn_y1)+'_'+'2'
								field[conn_y1][conn_x1] = blocks[blocks_i]+'_f'+direction+'_'+str(calc_ix)+'_'+str(calc_iy)+'_'+'1'
							connector_i ^= 1
							mouse_touching_l = False

						else:
							field[calc_iy][calc_ix] = blocks[blocks_i]+'_f'+direction
					if mouse_x > xx-78*screen_k:
						blocks_i = int((mouse_y-22*screen_k)//(55*screen_k))
				elif k_r:
					field[calc_iy][calc_ix] = '0'
					field_l[calc_iy][calc_ix] = 0

				if field[iy][ix] != '0':
					fs = field[iy][ix].split('_')
					block = blocks_png[blocks.index(fs[0])]['ft'.index(fs[1][0])]['urld'.index(fs[1][1])]
					block = pygame.transform.scale(block,(sq_size,sq_size))

					screen.blit(block,(grid_x+ix*sq_size,grid_y+iy*sq_size))
					if fs[0] == 'connector' and len(fs) == 5 and fs[4]=='1':
						circle(grid_x+ix*sq_size+sq_size/2,grid_y+iy*sq_size+sq_size/2,cl_black,sq_size//6)

	
	for i in range(256):
		if 0 < grid_x+i*sq_size <= xx-100*screen_k:
			line(grid_x+i*sq_size,grid_y,grid_x+i*sq_size,grid_y+255*sq_size,cl_black,1)
		if 0 < grid_y+i*sq_size < yy:
			line(grid_x,grid_y+i*sq_size,grid_x+255*sq_size,grid_y+i*sq_size,cl_black,1)
	


	rect(xx-99*screen_k,0,xx,yy,bg_color,0)

	line(xx-100*screen_k,0,xx-100*screen_k,yy,cl_black,2)
	rect(0,0,xx,yy,cl_black,2)



	for i in range(8):
		fs = field[iy][ix].split('_')
		block = blocks_png[i][0]['urld'.index(direction)]
		block = pygame.transform.scale(block,(50*screen_k,50*screen_k))
		screen.blit(block,(xx-75*screen_k,25*screen_k+55*screen_k*i))
		textout(xx-90*screen_k,28*screen_k+55*screen_k*i,11,cl_black,str(i+1))
		if i == blocks_i:
			rect(xx-78*screen_k,22*screen_k+55*screen_k*i,56*screen_k,56*screen_k,cl_black,2)

	if connector_i == 0:
		circle(xx-50*screen_k,215*screen_k,cl_black,8*screen_k)



	if help_i:
		rect(xx//2-170*screen_k,yy//2-140*screen_k,340*screen_k,280*screen_k,cl_white,0)
		rect(xx//2-170*screen_k,yy//2-140*screen_k,340*screen_k,280*screen_k,cl_black,2)
		for i in range(len(help_text)):
			textout(xx//2-170*screen_k+10,yy//2-135*screen_k+i*18*screen_k,int(12*screen_k),cl_black,help_text[i])
	

	textout(xx-80*screen_k,yy-20*screen_k,int(12*screen_k),cl_black,'help - h')

	textout(xx-70*screen_k,6*screen_k,int(8*screen_k),cl_black,str(current_fps)+' fps')

	rect(0,0,130*screen_k,14*screen_k,cl_white,0)
	rect(0,0,130*screen_k,14*screen_k,cl_black,2)
	textout(5*screen_k,0,int(10*screen_k),cl_black,linee)

	if not(do_logic):
		textout(xx//2-70*screen_k,yy-40*screen_k,int(22*screen_k),cl_black,'PAUSED')



def logic():
	global field
	global field_l
	global field_l_buf

	field_l_buf = [0]*256
	for i in range(256):
		field_l_buf[i] = [0]*256


	for iy in range(256):
		for ix in range(256):
			if field[iy][ix] != '0':
				field_splited = field[iy][ix].split('_')
				block = field_splited[0]
				direction = field_splited[1][1]
				value = int(field_l[iy][ix])


				if block == 'arrow':
					if direction == 'u':
						field_l_buf[iy-1][ix] += int(bool(value))
					elif direction == 'r':
						field_l_buf[iy][ix+1] += int(bool(value))
					elif direction == 'l':
						field_l_buf[iy][ix-1] += int(bool(value))
					else:
						field_l_buf[iy+1][ix] += int(bool(value))
					

				elif block == 'getter':
					if direction == 'u':
						value = field_l[iy+1][ix]
						field_l_buf[iy-1][ix] += int(bool(value))
						field_l_buf[iy][ix] = int(bool(value))
					elif direction == 'r':
						value = field_l[iy][ix-1]
						field_l_buf[iy][ix+1] += int(bool(value))
						field_l_buf[iy][ix] = int(bool(value))
					elif direction == 'l':
						value = field_l[iy][ix+1]
						field_l_buf[iy][ix-1] += int(bool(value))
						field_l_buf[iy][ix] = int(bool(value))
					else:
						value = field_l[iy-1][ix]
						field_l_buf[iy+1][ix] += int(bool(value))
						field_l_buf[iy][ix] = int(bool(value))

				elif block == 'bridge':
					if direction == 'u':
						field_l_buf[iy-2][ix] += int(bool(value))
					elif direction == 'r':
						field_l_buf[iy][ix+2] += int(bool(value))
					elif direction == 'l':
						field_l_buf[iy][ix-2] += int(bool(value))
					else:
						field_l_buf[iy+2][ix] += int(bool(value))

				elif block == 'connector':
					if len(field_splited) == 5:
						if field_splited[4] == '1':
							field_l_buf[int(field_splited[3])][int(field_splited[2])] += int(bool(value))
						else:
							if direction == 'u':
								field_l_buf[iy-1][ix] += int(bool(value))
							elif direction == 'r':
								field_l_buf[iy][ix+1] += int(bool(value))
							elif direction == 'l':
								field_l_buf[iy][ix-1] += int(bool(value))
							else:
								field_l_buf[iy+1][ix] += int(bool(value))




				elif block == 'power':
					field_l_buf[iy][ix] += 1
					field_l_buf[iy-1][ix] += 1
					field_l_buf[iy][ix+1] += 1
					field_l_buf[iy][ix-1] += 1
					field_l_buf[iy+1][ix] += 1

				


				elif block == 'not':
					if direction == 'u':
						field_l_buf[iy-1][ix] += int(bool(value)^1)
					elif direction == 'r':
						field_l_buf[iy][ix+1] += int(bool(value)^1)
					elif direction == 'l':
						field_l_buf[iy][ix-1] += int(bool(value)^1)
					else:
						field_l_buf[iy+1][ix] += int(bool(value)^1)

				else:
					if direction == 'u':
						field_l_buf[iy-1][ix] += int(bool(value))
					elif direction == 'r':
						field_l_buf[iy][ix+1] += int(bool(value))
					elif direction == 'l':
						field_l_buf[iy][ix-1] += int(bool(value))
					else:
						field_l_buf[iy+1][ix] += int(bool(value))


	#field_l = [0]*256
	#for i in range(256):
		#field_l[i] = [0]*256
	
	for iy in range(256):
		for ix in range(256):
			if field[iy][ix] != '0':
				field_splited = field[iy][ix].split('_')
				block = field_splited[0]
				direction = field_splited[1][1]
				value = field_l_buf[iy][ix]

				
				if block == 'and':
					field_l[iy][ix] = value > 1
					field[iy][ix] = block+'_'+'ft'[value > 1]+direction
				elif block == 'xor':
					field_l[iy][ix] = value % 2 == 1
					field[iy][ix] = block+'_'+'ft'[value % 2 == 1]+direction
				elif block == 'connector':
					if len(field_splited) == 5:
						field_l[iy][ix] = bool(value)
						field[iy][ix] = block+'_'+'ft'[bool(value)]+direction+'_'+str(field_splited[2])+'_'+str(field_splited[3])+'_'+field_splited[4]
				else:
					field_l[iy][ix] = bool(value)
					field[iy][ix] = block+'_'+'ft'[bool(value)]+direction


lx = 0
ly = 0
rx = 0
ry = 0
claster = []

def selecting():
	global selecting_step
	global sx1
	global sx2
	global sy1
	global sy2
	global lx
	global ly
	global rx
	global ry
	global claster

	

	if k_e:
		if selecting_step == 0:
			claster = []
			sx1 = (mouse_x-grid_x)//sq_size
			sy1 = (mouse_y-grid_y)//sq_size
			selecting_step += 1

		if selecting_step == 1:
			sx2 = (mouse_x-grid_x)//sq_size
			sy2 = (mouse_y-grid_y)//sq_size
		
		lx = min(sx1,sx2)
		rx = max(sx1,sx2)+1
		ly = min(sy1,sy2)
		ry = max(sy1,sy2)+1
		rect(lx*sq_size+grid_x,ly*sq_size+grid_y,rx*sq_size-lx*sq_size+1,ry*sq_size-ly*sq_size+1,cl_blue,3)
	else:
		if selecting_step == 1:

			claster = [0]*(ry-ly)
			for i in range(ry-ly):
				claster[i] = [0]*(rx-lx)
			for iy in range(ry-ly):
				for ix in range(rx-lx):
					claster[iy][ix] = field[ly+iy][lx+ix]



			selecting_step = 0
	if claster != []:
		for iy in range(ry-ly):
			for ix in range(rx-lx):
				if claster[iy][ix] != '0':
					fs = claster[iy][ix].split('_')
					block = blocks_png[blocks.index(fs[0])]['ft'.index(fs[1][0])]['urld'.index(fs[1][1])]
					block = pygame.transform.scale(block,(sq_size,sq_size))

					screen.blit(block,(grid_x+(ix+(mouse_x-grid_x)//sq_size)*sq_size,grid_y+(iy+(mouse_y-grid_y)//sq_size)*sq_size))

	if k_ctrl:
		if k_v:
			if claster != []:
				for iy in range(ry-ly):
					for ix in range(rx-lx):
						if claster[iy][ix] != '0':
							field[(mouse_y-grid_y)//sq_size+iy][(mouse_x-grid_x)//sq_size+ix] = claster[iy][ix]
		if k_x:
			for iy in range(ry-ly):
				for ix in range(rx-lx):
					field[ly+iy][lx+ix] = '0'

		if k_d:
			ly = ry = 0
			lx = rx = 0
			claster = []


def type_name():
	r = True
	pos = 0
	caps = False
	shift = False
	line = ''
	while r:

		rect(xx//4,yy//7*3,xx//2,yy//7,cl_white,0)
		rect(xx//4,yy//7*3,xx//2,yy//7,cl_black,2)
		textout(xx//4+10*screen_k,yy//7*3+18*screen_k,int(22*screen_k),cl_black,'Save as:   '+line)
		textout(xx//4+25*screen_k,yy//7*3+45*screen_k,int(7*screen_k),cl_black,'Max - 16 symbols')

		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				1 / 0
			if event.type == pygame.KEYDOWN:
				for i in range(len(symbols)):
					if len(line) != 16:
						if event.key == symbols[i][0]:
							if (caps ^ shift):
								s = symbols[i][1]
								line += s.upper()
							else:
								line += symbols[i][1]

				

				if event.key == pygame.K_BACKSPACE:
					line = line[:len(line)-1]

				if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
					r = False

				if event.key == pygame.K_LEFT:
					if pos > 0:
						pos -= 1
						
				if event.key == pygame.K_RIGHT:
					if pos < 2:
						pos += 1
				if event.key == pygame.K_ESCAPE:
					return -1
				if event.key == pygame.K_CAPSLOCK:
					caps ^= 1
				if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
					shift = True
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LSHIFT:
					shift = False



		pygame.display.flip()

	return line



clear_field()

mouse_x = xx/2 + 200
mouse_y = yy/2

frame_counter = 0

r_time = 0

fps_i = 0

current_fps = 1


menu.main()
running = True
world_i = 0
while running:
	start_timer()

	mouse_pos = pygame.mouse.get_pos()

	mouse_xl = mouse_x
	mouse_yl = mouse_y

	mouse_x = mouse_pos[0]
	mouse_y = mouse_pos[1]



	screen.fill(bg_color)

	
	if do_logic:
		logic()

	main_func()

	

	selecting()



	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			1 / 0

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LCTRL:
				k_ctrl = True
			if event.key == pygame.K_LALT:
				k_alt = True
			if event.key == pygame.K_LSHIFT:
				k_shift = True
			if event.key == pygame.K_SPACE:
				k_space = True
				do_logic ^= 1
			if event.key == pygame.K_e:
				k_e = True
			if event.key == pygame.K_v:
				k_v = True
			if event.key == pygame.K_x:
				k_x = True
			if event.key == pygame.K_d:
				k_d = True
			if event.key == pygame.K_l:
				if k_ctrl:
					if k_alt:
						1
						
					else:
						1
			if event.key == pygame.K_BACKSPACE:
				1
			if event.key == pygame.K_ESCAPE:
				menu.main()
			if event.key == pygame.K_w:
				direction = 'u'
			if event.key == pygame.K_a:
				direction = 'l'
			if event.key == pygame.K_d:
				if k_ctrl == False:
					direction = 'r'
			if event.key == pygame.K_s:
				if k_ctrl:
					if k_alt or linee == '':
						linee = type_name()

					if linee != -1:
						textout(xx//2-70*screen_k,yy-40*screen_k,int(22*screen_k),cl_black,'SAVING...')
						pygame.display.flip()
						f_m.save_map(field,linee)
					else:
						linee = ''
					
				else:
					direction = 'd'

			if event.key == pygame.K_r:
				k_r = True

			if event.key == pygame.K_h:
				help_i ^= 1

			if event.key == pygame.K_1:
				blocks_i = 0
			if event.key == pygame.K_2:
				blocks_i = 1
			if event.key == pygame.K_3:
				blocks_i = 2
			if event.key == pygame.K_4:
				blocks_i = 3
			if event.key == pygame.K_5:
				blocks_i = 4
			if event.key == pygame.K_6:
				blocks_i = 5
			if event.key == pygame.K_7:
				blocks_i = 6
			if event.key == pygame.K_8:
				blocks_i = 7


		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LCTRL:
				k_ctrl = False
			if event.key == pygame.K_LALT:
				k_alt = False
			if event.key == pygame.K_LSHIFT:
				k_shift = False
			if event.key == pygame.K_SPACE:
				k_space = False
			if event.key == pygame.K_e:
				k_e = False
			if event.key == pygame.K_v:
				k_v = False
			if event.key == pygame.K_x:
				k_x = False
			if event.key == pygame.K_d:
				k_d = False


			if event.key == pygame.K_r:
				k_r = False





		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				mouse_touching_l = True

				



			if event.button == 3:
				mouse_touching_r = True
				


			if event.button == 4:
				mouse_scrolling_u = True
				if sq_size < 70:
					corner_x -= (mouse_x-grid_x)//sq_size
					corner_y -= (mouse_y-grid_y)//sq_size
					sq_size += 1
				
			if event.button == 5:
				mouse_scrolling_d = True
				if sq_size > 3:
					corner_x += (mouse_x-grid_x)//sq_size
					corner_y += (mouse_y-grid_y)//sq_size
					sq_size -= 1

		if event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				mouse_touching_l = False
			if event.button == 3:
				mouse_touching_r = False


			if event.button == 4:
				mouse_scrolling_u = False
			if event.button == 5:
				mouse_scrolling_d = False


	stop_timer()
	time_per_frame = check_timer()
	
	fps_i += 1

	
	if fps_i % 5 == 0 and time_per_frame != 0:
		current_fps = round(1/time_per_frame,1)



	pygame.display.flip()
