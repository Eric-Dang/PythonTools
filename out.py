# encoding: utf8

import sys,os,ftplib,socket

CONST_HOST 			= "192.168.1.250"
CONST_USERNAME 		= ""
CONST_PWD 			= ""
CONST_BUFFER_SIZE 	= 8192
CONST_UPLOAD		= False

ftpDir = "xxx/xxx"
ffserverPath = "//192.168.1.249/xx/Out/"
localOutPath = "F:/NeiOut"

def connect():
	try:
		ftp = ftplib.FTP(CONST_HOST)
		ftp.login(CONST_USERNAME,CONST_PWD)
		return ftp
	except socket.error,socket.gaierror:
		print("FTP is unavailable,please check the host,username and password!")
		sys.exit(0)

def disconnect(ftp):
	ftp.quit()

def upload(ftp, filepath):
	f = open(filepath, "rb")
	file_name = os.path.split(filepath)[-1]
	try:
		ftp.storbinary('STOR %s'%file_name, f, CONST_BUFFER_SIZE)
	except ftplib.error_perm:
		return False
	return True

def download(ftp, filename, outDir):
	outFileName = outDir + "/" + os.path.split(filename)[-1]
	f = open(outFileName, "wb").write
	try:
		ftp.retrbinary("RETR %s"%filename, f, CONST_BUFFER_SIZE)
	except ftplib.error_perm:
		return False
	return True


def updateAllFiles(ftp):
	for root, dirs, files in os.walk("./"):
		for f in files:
			fileName = root + "/" + f
			upload(ftp, fileName)


def downloadAllFiles(ftp, outDir):
	root = ftp.pwd()
	allFiles = ftp.nlst()
	for f in allFiles :
		download(ftp, root + "/" + f, outDir)


def find(ftp,filename):
	ftp_f_list = ftp.nlst()
	if filename in ftp_f_list:
		return True
	else:
		return False

ConstShaYingFiles = ["config", "DBS", "shaying"]

def main():
	ftp = connect()
	ftp.cwd(ftpDir.decode('utf8').encode('GBK'))	

	if not os.path.exists(localOutPath):
		os.mkdir(localOutPath)
		
	if CONST_UPLOAD:
		updateAllFiles(ftp)
	else:
		downloadAllFiles(ftp, localOutPath)

	disconnect(ftp)
	
	if not CONST_UPLOAD:
		for r, d, files in os.walk(localOutPath):
			for f in files:				
				if f.split('.')[0] not in ConstShaYingFiles :
					cpCmd = "\"" + r + "/" + f + "\" \"" + ffserverPath.decode('utf8').encode('GBK') + '/' + f + "\""
					print("copy /Y " + cpCmd.replace('/', '\\'))
					os.system("copy /Y " + cpCmd.replace('/', '\\'))					
					os.remove(r + "\\" + f)



if __name__ == "__main__":
	main()
