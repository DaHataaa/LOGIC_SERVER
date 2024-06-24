import os

def load_map(map_name):
	

	f = open('data/maps/'+map_name+'.mp','r').readlines()

	field = [0]*256
	for i in range(256):
		field[i] = ['0']*256

	field_l = [0]*256
	for i in range(256):
		field_l[i] = [0]*256

	for iy in range(256):
		for ix in range(256):
			field[iy][ix] = f[iy].split()[ix].replace('\n','')
			if field[iy][ix] != '0':
				field_l[iy][ix] = int(field[iy][ix].split('_')[1][0]=='t')

	return field,field_l

def load_online_map(map_name):

	f = open('data/online_maps/'+map_name+'.mp','r').readlines()

	field = [0]*256
	for i in range(256):
		field[i] = ['0']*256

	field_l = [0]*256
	for i in range(256):
		field_l[i] = [0]*256

	for iy in range(256):
		for ix in range(256):
			field[iy][ix] = f[iy].split()[ix].replace('\n','')
			if field[iy][ix] != '0':
				field_l[iy][ix] = int(field[iy][ix].split('_')[1][0]=='t')

	return field,field_l


def save_map(field,map_name):
	f = open('data/maps/'+map_name+'.mp','w')
	mn_r = open('data/maps/maps_list.txt','r').readlines()

	mn = open('data/maps/maps_list.txt','a')
	
	for i in range(256):
		line = ''
		for i2 in range(256):
			line += field[i][i2] + ' '
		f.write(line+'\n')


	app = True
	
	for i in range(len(mn_r)):
		if mn_r[i].replace('\n','') == map_name:
			app = False
	if app:
		mn.write(map_name+'\n')


def delete_map(map_name):
	try:
		os.remove('data/maps/'+map_name+'.mp')
	except:
		1
	names = open('data/maps/maps_list.txt','r').readlines()
	mn = open('data/maps/maps_list.txt','w')
	for i in range(len(names)):
		m = names[i].replace('\n','')
		if m != map_name:
			mn.write(m+'\n')
