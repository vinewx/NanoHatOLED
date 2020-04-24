#!/usr/bin/env python
# -*- encoding:utf8 -*-
#
#   apt-get install fonts-takao-pgothic
#   apt-get install python-mutagen python3-mutagen

import os
import sys
import commands
import re
import time
import signal
import socket
import subprocess
import smbus
import math
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import RPi.GPIO as GPIO

global pageSleep
pageSleep=60
global pageSleepCountdown
pageSleepCountdown=pageSleep

shutdownDelay   = 6
title_height    = 16
scroll_unit     = 3
gap = 4

oled_width      = 128
oled_height     =  64
cover_size      = oled_height - title_height - 2

# SSD1306 --> 0
# SH1106  --> 2
oled_offset_x   = 0

font_title      = ImageFont.truetype('/usr/share/oled/fz12.TTF', 12, encoding='unic')
#font_title     = ImageFont.truetype('aqua_pfont.ttf', title_height, encoding='unic')
#font_title     = ImageFont.truetype('MEIRYOB.TTC', int(title_height*10/12), encoding='unic')

font_info       = ImageFont.truetype('/usr/share/oled/fz12.TTF', 14, encoding='unic')
#font_info      = ImageFont.truetype('aqua_pfont.ttf', 16, encoding='unic')
#font_info      = ImageFont.truetype('MEIRYO.TTC', 14, encoding='unic')

font_audio      = ImageFont.load_default()

font_time       = ImageFont.truetype('/usr/share/oled/fz12.TTF', 28);
#font_time      = ImageFont.truetype('aqua_pfont.ttf', 32);
font_date       = ImageFont.truetype('/usr/share/oled/fz12.TTF', 16);
#font_date      = ImageFont.truetype('aqua_pfont.ttf', 18);


mpd_host        = 'localhost'
mpd_port        = 6600
mpd_bufsize     = 8192




def receive_signal(signum, stack):

	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.connect((mpd_host, mpd_port))
	soc.recv(mpd_bufsize)
	
	if signum == signal.SIGUSR1:
		print 'K1 pressed'
		soc.send('previous\n')
		soc.recv(mpd_bufsize)
	
	if signum == signal.SIGUSR2:
		print 'K2 pressed'
		soc.send('status\n')
		buff        = soc.recv(mpd_bufsize)
		state_list  = buff.splitlines()
		for line in range(0,len(state_list)):
			if state_list[line].startswith(r"state: "):
				info_state      = state_list[line].replace(r"state: ", "")
				print(info_state)
				if info_state == 'play' :
					soc.send('stop\n')
					soc.recv(mpd_bufsize)
				else:
					soc.send('play\n')
					soc.recv(mpd_bufsize)

	if signum == signal.SIGALRM:
		print 'K3 pressed'
		soc.send('next\n')
		soc.recv(mpd_bufsize)


signal.signal(signal.SIGUSR1, receive_signal)
signal.signal(signal.SIGUSR2, receive_signal)
signal.signal(signal.SIGALRM, receive_signal)


bus = smbus.SMBus(0)
OLED_address     = 0x3c
OLED_CommandMode = 0x00
OLED_DataMode    = 0x40


def oled_init():

	cmd = []

	cmd += [0xAE]   #display off

	cmd += [0x40]   #set display start line

	cmd += [0x81]   # Contrast
	cmd += [0x80]   # 0 - 255, default=0x80
	
	cmd += [0xA1]   #set segment remap

	cmd += [0xA6]   #normal / reverse

	cmd += [0xA8]   #multiplex ratio
	cmd += [0x3F]   #duty = 1/64

	cmd += [0xC8]   #Com scan direction

	cmd += [0xD3]   #set display offset
	cmd += [0x00]   
	cmd += [0xD5]   #set osc division
	cmd += [0x80]

	cmd += [0xD9]   #set pre-charge period
	cmd += [0xF1]

	cmd += [0xDA]   #set COM pins
	cmd += [0x12]

	cmd += [0xDB]   #set vcomh
	cmd += [0x40]

	cmd += [0x8D]   #set charge pump enable
	cmd += [0x14]

	cmd += [0x20]   #set addressing mode
	cmd += [0x02]   #set page addressing mode

	cmd += [0xAF]   #display ON

#   bus.write_i2c_block_data(OLED_address,OLED_CommandMode,cmd)

	for byte in cmd:
		try:
			bus.write_byte_data(OLED_address,OLED_CommandMode,byte)
		except IOError:
			print("IOError")
			return -1


def oled_drawImage(image):

	if image.mode != '1' and image.mode != 'L':
		raise ValueError('Image must be in mode 1.')

	imwidth, imheight = image.size
	if imwidth != oled_width or imheight != oled_height:
		raise ValueError('Image must be same dimensions as display ({0}x{1}).' \
		.format(oled_width, oled_height))

	# Grab all the pixels from the image, faster than getpixel.
	pix     = image.load()

	pages   = oled_height / 8;
	block   = oled_width / 32;

	for page in range(pages):

		addr    = [];
		addr    += [0xB0 | page];   # Set Page Address
		addr    += [0x10];  # Set Higher Column Address
		addr    += [0x00 | oled_offset_x];  # Set Lower Column Address

		try:
			bus.write_i2c_block_data(OLED_address,OLED_CommandMode,addr)
		except IOError:
			print("IOError")
			return -1

		for blk in range(block):
			data=[]
			for b in range(32):
				x   = blk * 32 + b;
				y   = page * 8

				data.append(
					((pix[(x, y+0)] >> 7) << 0) | \
					((pix[(x, y+1)] >> 7) << 1) | \
					((pix[(x, y+2)] >> 7) << 2) | \
					((pix[(x, y+3)] >> 7) << 3) | \
					((pix[(x, y+4)] >> 7) << 4) | \
					((pix[(x, y+5)] >> 7) << 5) | \
					((pix[(x, y+6)] >> 7) << 6) | \
					((pix[(x, y+7)] >> 7) << 7) );

			try:
				bus.write_i2c_block_data(OLED_address,OLED_DataMode,data)
			except IOError:
				print("IOError")
				return -1


def ImageHalftoning_FloydSteinberg(image):

	shift   = 20;

	cx, cy  = image.size;

	temp    = Image.new('I', (cx, cy));
	result  = Image.new('L', (cx, cy));
	
	tmp     = temp.load();
	dst     = result.load();
	
	# Setup Gamma tablw
	gamma   = [0]*256;
	for i in range(256):
		gamma[i]    = int( math.pow( i / 255.0, 2.2 ) * ((1 << shift) - 1) );
		
	# Convert to initial value
	if image.mode == 'L':
		src     = image.load();
		for y in range(cy):
			for x in range(cx):
				tmp[(x,y)]  =  gamma[ src[(x,y)] ];

	elif image.mode == 'RGB':
		src     = image.load();
		for y in range(cy):
			for x in range(cx):
				R,G,B   = src[(x,y)];
				Y       = (R * 13933 + G * 46871 + B * 4732) >> 16; # Bt.709
				tmp[(x,y)]  =  gamma[ Y ];

	elif image.mode == 'RGBA':
		src     = image.load();
		for y in range(cy):
			for x in range(cx):
				R,G,B,A = src[(x,y)];
				Y       = (R * 13933 + G * 46871 + B * 4732) >> 16; # Bt.709
				tmp[(x,y)]  =  gamma[ Y ];

	else:
		raise ValueError('Image.mode is not supported.')    

	# Error diffuse
	for y in range(cy):
		for x in range(cx):
			c   = tmp[(x,y)];
			e   = c if c < (1 << shift) else (c - ((1 << shift) - 1));
			
			dst[(x,y)]  = 0 if c < (1 << shift) else 255;

			# FloydSteinberg
			#   -       *       7/16
			#   3/16    5/16    1/16
			if  (x+1) < cx :
				tmp[(x+1,y)]    += e * 7 / 16;

			if (y+1) < cy :
				if 0 <= (x-1) :
					tmp[(x-1,y+1)]  += e * 3 / 16;

				tmp[(x,y+1)]        += e * 5 / 16;

				if (x+1) < cx :
					tmp[(x+1,y+1)]  += e * 1 / 16;

	return  result;

# initialize OLED
oled_init()

# OLED images
image           = Image.new('L', (oled_width, oled_height))
draw            = ImageDraw.Draw(image)
draw.rectangle((0,0,oled_width,oled_height), outline=0, fill=0)

profile_path    = ""
title_offset    = 0

# Draw opening image
try:
	oled_drawImage(Image.open('/usr/share/oled/opening.png').convert('L'))
	time.sleep(1)
except:
	oled_drawImage(image)


count = 0
while (count < 23):
	s = str(count).zfill(5)
	image_marvell = Image.open('/usr/share/oled/jojo/'+s+'.png').convert('1')
	oled_drawImage(image_marvell)
	count = count + 1
time.sleep(1)
print("commands:")
print("----- start ----------")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("",80))
ipaddress=(s.getsockname()[0])
s.close()

def getIP():
	ip = commands.getoutput("ubus call network.interface.lan status | grep \"address\" | grep -oE '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'")
	if bool(re.search(r'\d', ip)) is False:
		cmd = "ubus call network.interface.wwan status | grep \"address\" | grep -oE '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'"
		ip = subprocess.check_output(cmd,shell = True)
	return str(ip)

def getCPUtemperature():
	(status, output) = commands.getstatusoutput('cat /sys/class/thermal/thermal_zone0/temp')
	temp = int(output) / 1000
	return str(temp)

def getCPUuse():
	cmd = "echo -e `expr 100 - $(top -n 1 | grep 'CPU:' | awk -F '%' '{ print $4 }' | awk -F ' ' '{ print $2 }')`%"
	CPU = subprocess.check_output(cmd,shell = True)
	return str(CPU)

def getNetstat():
	cmd = "ifstat -i br-lan -q 1 1 | awk 'NR>2 {print $1}'"
	net = subprocess.check_output(cmd,shell = True).replace("\n", "")
	if float(net) > 1024:
		net = float(net) / 1024
		out = '网速:'+str(int(float(net)))+'MB/S'
	else:
		out = '网速:'+str(int(float(net)))+'KB/S'
	return out

def getProxyState():
	cmd = "uci get openclash.config.enable"
	proxystate = subprocess.check_output(cmd,shell = True)
	return int(proxystate)

def getProfileMode():
	cmd = "uci get openclash.config.proxy_mode"
	profilemode = subprocess.check_output(cmd,shell = True)
	return profilemode

def getProfilePath():
	cmd = "uci get openclash.config.config_path"
	profilepath = subprocess.check_output(cmd,shell = True)
	return profilepath

def getProfileName():
	cmd = "uci get openclash.@config_subscribe[0].name"
	profilename = subprocess.check_output(cmd,shell = True)
	return profilename

def getProfileType():
	cmd = "uci get openclash.@config_subscribe[0].type"
	profiletype = subprocess.check_output(cmd,shell = True)
	return profiletype


#switch

state = 1

SWITCH_PIN1 = 11
SWITCH_PIN2 = 13
SWITCH_PIN3 = 15
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(SWITCH_PIN1,GPIO.IN,GPIO.PUD_DOWN)
GPIO.setup(SWITCH_PIN2,GPIO.IN,GPIO.PUD_DOWN)
GPIO.setup(SWITCH_PIN3,GPIO.IN,GPIO.PUD_DOWN)

GPIO.add_event_detect(SWITCH_PIN1, GPIO.RISING,bouncetime=200)  # add rising edge detection on a channel
GPIO.add_event_detect(SWITCH_PIN2, GPIO.RISING,bouncetime=200)  # add rising edge detection on a channel
GPIO.add_event_detect(SWITCH_PIN3, GPIO.RISING,bouncetime=200)  # add rising edge detection on a channel
	
#print getCPUtemperature()
while True:
	#clear screen
	draw.rectangle((0,0,oled_width,oled_height), outline=0, fill=0)
	
	if (state == 1) and (pageSleepCountdown > 0):
		# Draw IP address
		try:
			ip_image     = Image.new('L', (oled_width, 16))
			ip_draw      = ImageDraw.Draw(ip_image)
			ip_draw.rectangle((0,0, oled_width, 16), outline=0, fill=0)
			ip_draw.text((0,0), unicode('IP:'+getIP(),'utf-8'), font=font_title, fill=255)
			image.paste(ip_image, (gap,0))
		except:
			ip_image     = Image.new('L', (oled_width, 16))
			ip_draw      = ImageDraw.Draw(ip_image)
			ip_draw.rectangle((0,0, oled_width, 16), outline=0, fill=0)
			ip_draw.text((0,0), unicode('IP地址获取中...','utf-8'), font=font_title, fill=255)
			image.paste(ip_image, (gap,0))
		# Draw Temp 
		temp_image     = Image.new('L', (oled_width, 16))
		temp_draw      = ImageDraw.Draw(temp_image)
		temp_draw.rectangle((0,0, oled_width, 16), outline=0, fill=0)
		temp_draw.text((0,0), unicode('CPU温度:'+getCPUtemperature()+'℃','utf-8'), font=font_title, fill=255)
		image.paste(temp_image, (gap,16))
		
		# Draw Cpu usage
		cpu_image     = Image.new('L', (oled_width, 16))
		cpu_draw      = ImageDraw.Draw(cpu_image)
		cpu_draw.rectangle((0,0, oled_width, 16), outline=0, fill=0)
		cpu_draw.text((0,0), unicode('CPU使用率:'+getCPUuse(),'utf-8'), font=font_title, fill=255)
		image.paste(cpu_image, (gap,32))
		
		# Draw Net stat
		try:
			net_image     = Image.new('L', (oled_width, 16))
			net_draw      = ImageDraw.Draw(net_image)
			net_draw.rectangle((0,0, oled_width, 16), outline=0, fill=0)
			net_draw.text((0,0), unicode(getNetstat(),'utf-8'), font=font_title, fill=255)
			image.paste(net_image, (gap,48))
		except:
			net_image     = Image.new('L', (oled_width, 16))
			net_draw      = ImageDraw.Draw(net_image)
			net_draw.rectangle((0,0, oled_width, 16), outline=0, fill=0)
			net_draw.text((0,0), unicode("当前无网络",'utf-8'), font=font_title, fill=255)
			image.paste(net_image, (gap,48))
	
	elif (state == 2) and (pageSleepCountdown > 0):
		proxystate = getProxyState()
		if (proxystate == 1):
			# Draw Mode
			ip_image     = Image.new('L', (oled_width, 18))
			ip_draw      = ImageDraw.Draw(ip_image)
			ip_draw.rectangle((0,0, oled_width, 18), outline=0, fill=0)
			ip_draw.text((0,0), unicode('模式:'+getProfileMode(),'utf-8'), font=font_title, fill=255)
			image.paste(ip_image, (gap,0))
			
			# Draw Path 
			propath1  = '路径:'+getProfilePath()
			propath2  = propath1.decode('utf8')[0:10].encode('utf8')
			
			if propath1 != profile_path :
				profile_path = propath1
				title_width, dmy_y   = font_title.getsize(unicode(propath1,'utf-8'))
				title_offset    = oled_width / 2;
				title_image     = Image.new('L', (title_width, title_height))
				title_draw      = ImageDraw.Draw(title_image)
				title_draw.rectangle((0,0, title_width, title_height), outline=0, fill=0)
				title_draw.text((0,0), unicode(propath1,'utf-8'), font=font_title, fill=255)

			# Title
			x   = gap
			y   = 0
			
			if oled_width < title_image.width :
				if title_image.width < -title_offset :  
					title_offset    = oled_width / 2
				
				if title_offset < gap :
					x   = title_offset
				
				title_offset    = title_offset - scroll_unit
				print x
			
			image.paste(title_image, (x,16))
			x   = gap;
			
			# Draw Sub
			try:
				# Draw Name
				ip_image     = Image.new('L', (oled_width, 18))
				ip_draw      = ImageDraw.Draw(ip_image)
				ip_draw.rectangle((0,0, oled_width, 18), outline=0, fill=0)
				ip_draw.text((0,0), unicode('配置:'+getProfileName(),'utf-8'), font=font_title, fill=255)
				image.paste(ip_image, (gap,32))
			
				# Draw Type
				type_image     = Image.new('L', (oled_width, 18))
				type_draw      = ImageDraw.Draw(type_image)
				type_draw.rectangle((0,0, oled_width, 18), outline=0, fill=0)
				type_draw.text((0,0), unicode('类型:'+getProfileType(),'utf-8'), font=font_title, fill=255)
				image.paste(type_image, (gap,48))
			except:
				ip_image     = Image.new('L', (oled_width, 18))
				ip_draw      = ImageDraw.Draw(ip_image)
				ip_draw.rectangle((0,0, oled_width, 18), outline=0, fill=0)
				ip_draw.text((0,0), unicode("当前无订阅",'utf-8'), font=font_title, fill=255)
				image.paste(ip_image, (gap,32))


		else:
			ip_image     = Image.new('L', (oled_width, 18))
			ip_draw      = ImageDraw.Draw(ip_image)
			ip_draw.rectangle((0,0, oled_width, 18), outline=0, fill=0)
			ip_draw.text((0,0), unicode('飞机当前未起飞','utf-8'), font=font_title, fill=255)
			image.paste(ip_image, (gap,0))
		

	elif (state == 3) and (pageSleepCountdown > 0):
		
		
		ip_image     = Image.new('L', (oled_width, 18))
		ip_draw      = ImageDraw.Draw(ip_image)
		ip_draw.rectangle((0,0, oled_width, 18), outline=0, fill=0)
		ip_draw.text((0,0), unicode('盒子将在'+str(shutdownDelay - 1)+'秒后关机','utf-8'), font=font_title, fill=255)
		image.paste(ip_image, (14,16))
		shutdownDelay = shutdownDelay - 1
		if shutdownDelay == 0 :
			draw.rectangle((0,0,oled_width,oled_height), outline=0, fill=0)
			oled_drawImage(image)
			time.sleep(1)
			os.system('halt')
		time.sleep(1)
	else:
		print 'hehe'
	
	oled_drawImage(image)
	#time.sleep(0.1)
	if GPIO.event_detected(SWITCH_PIN1):
		print 'Button1 pressed'
		state = 1
		pageSleepCountdown = pageSleep
	
	if GPIO.event_detected(SWITCH_PIN2):
		print 'Button2 pressed'
		state = 2
		pageSleepCountdown = pageSleep
		
	if GPIO.event_detected(SWITCH_PIN3):
		print 'Button3 pressed'
		state = 3
		pageSleepCountdown = pageSleep
	
	if pageSleepCountdown == 0:
		pageSleepCountdown = 0
	else:
		pageSleepCountdown = pageSleepCountdown - 1

	

	
