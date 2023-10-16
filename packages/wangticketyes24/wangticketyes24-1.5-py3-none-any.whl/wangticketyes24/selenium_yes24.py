
import datetime
import time
import traceback
from bs4 import BeautifulSoup
import requests
import random

from urllib.parse import urlencode

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import WebDriverException

class Stage(object):
	START = 0
	LOGINED = 1
	PERF_OPENED = 2


class Selenium_yes24(object):
	def __init__(self, idperf):
		self.idperf = idperf
		self.stage = Stage.START
		self.tkseat = ""

	def startChrome(self, headless=False, x=100, y=100, w=1024, h=700):
		for i in range(5):
			try:
				self.startChrome_ex(headless, x, y, w, h)
				break
			except Exception as e:
				print("[startChrome] exception.. ", str(e))
				if i == 4:
					raise Exception("chrome issue")

			time.sleep(2)

		self.driver.implicitly_wait(5)

	def startChrome_ex(self, headless, x, y, w, h):
		options = webdriver.ChromeOptions()
		options.add_argument('--no-sandbox')
		options.add_argument('--disable-dev-shm-usage')
		if headless:
			options.add_argument('--headless')
			options.add_argument('--disable-gpu')

		options.add_argument('--disable-infobars')
		options.add_argument('--window-position={},{}'.format(x,y));
		options.add_argument('--window-size={},{}'.format(w,h))
		self.driver = webdriver.Chrome('./chromedriver', options=options)

	def login2(self, userid, userpw, cookies):
		while True:
			try:
				self.login2_ex(userid, userpw, cookies)
				return
			except KeyboardInterrupt:
				raise
			except Exception as e:
				print(traceback.format_exc())
				print("Exception happen in selenium login2...", str(e))
				time.sleep(0.5)
				continue

	def login2_ex(self, userid, userpw, cookies):
		self.userid = userid

		#URL = "http://ticket.yes24.com"
		#URL = "https://www.yes24.com/Templates/FTLogin.aspx"
		URL = "http://ticket.yes24.com/Pages/Perf/Detail/Detail.aspx?IdPerf=30000"
		self.driver.get(URL)

		for cookie in cookies:
			#print(cookie.name, cookie.value, cookie.domain)
			try:
				self.driver.add_cookie({'name':cookie.name, 'value':cookie.value , 'domain':cookie.domain})
			except:
				print("exception.. ", cookie.name, cookie.value, cookie.domain)

		URL = "http://ticket.yes24.com/Pages/Perf/Detail/Detail.aspx?IdPerf={}".format(self.idperf)
		self.driver.get(URL)
		while True:
			#es = self.driver.find_elements_by_xpath("//a[contains(@href,'FTLogOut')]")
			es = self.driver.find_elements_by_xpath("//a[@id='consiceLogin']")
			if len(es) > 0:
				#LOGIN_SUCCEED = True
				logoutlink = es[0].get_attribute('href')
				logouttext = es[0].text
				print("login status:{}({})". format(logouttext, logoutlink))
				if logouttext == "로그아웃":
					break
			print("Not logined yet......(no logout button found)")
			time.sleep(1)

		## CHANGE TITLE
		self.driver.execute_script("document.title = '{}'".format(userid))


	"""
	<input name="HidPerfFanClubOption" id="HidPerfFanClubOption" type="hidden" value="1">
	<a href="javascript:;" id="pFanClubAuthButton" style="" class="rbtn rbt_fan">
	<a href="javascript:;" id="pFanClubAuthButton" style="display:none" class="rbtn rbt_fan">
	"""
	def fanclubcheck(self):
		try:
			print("Checking FAN CLUB status.........")
			soup = BeautifulSoup(self.driver.page_source, "html.parser")
			fanoption = soup.find('input', {"id": "HidPerfFanClubOption"})['value']
			if fanoption == "1":
				## FAN CLUB PERF
				authbutton = soup.find('a', {"id": "pFanClubAuthButton"})
				if authbutton['style'] == "":
					print("YOU ARE NOT FAN CLUB MEMBER???????????\n"*10)
				else:
					print("YOU ARE FAN CLUB MEMBER!!!")

		except:
			print(traceback.format_exc())
			print("failed to fanclubcheck...but not critical..\n"*10)


	def login(self, userid, userpw):
		self.userid = userid

		while True:
			URL = 'https://www.yes24.com/Templates/FTLogin.aspx?ReturnURL=http://ticket.yes24.com/Home/Perf/PerfDetailInfo.aspx&&ReturnParams=IdPerf={}'.format(self.idperf)
			self.driver.get(URL);

			es = self.driver.find_elements_by_xpath("//img[@id='yesCaptchaImage']")
			if len(es) > 0:
				print("captcha exists")
				time.sleep(15)
				continue

			print("captcha not exists. continue login....")

			## LOGIN FIRST
			#self.driver.find_element_by_name('txtLoginID').send_keys(userid)
			#self.driver.find_element_by_name('txtPassword').send_keys(userpw)
			#self.driver.find_element_by_name('imgLogin').click()
			self.driver.find_element_by_name('SMemberID').send_keys(userid)
			self.driver.find_element_by_name('SMemberPassword').send_keys(userpw)
			self.driver.find_element_by_id('btnLogin').click()

			## CHECK LOGIN FINISHED
			#self.driver.find_element_by_xpath("//a[contains(@href,'LogOutUrl')]")
			LOGIN_SUCCEED = False
			while True:
				## CAPTCHA is showing again???
				es = self.driver.find_elements_by_xpath("//img[@id='yesCaptchaImage']")
				if len(es) > 0:
					print("captcha showing again...")
					time.sleep(5)
					break

				es = self.driver.find_elements_by_xpath("//a[contains(@href,'FTLogOut')]")
				if len(es) > 0:
					LOGIN_SUCCEED = True
					break
				print("Not logined yet......(no logout button found)")
				time.sleep(1)

			if LOGIN_SUCCEED:
				print("Login succeed!!!")
				break

		## CHANGE TITLE
		self.driver.execute_script("document.title = '{}'".format(userid))

		## save stage
		self.stage = Stage.LOGINED

		"""
		executor_url = driver.command_executor._url
		session_id = driver.session_id

		print(session_id)
		print(executor_url)
		"""

	def logout(self):
		# it is for removing command_executor
		time.sleep(1)
		self.driver.quit()

	def openBlank(self, count=1):
		self.driver.execute_script("window.open()")

		## handling popup
		main_window_handle = self.driver.current_window_handle

		popup_window_handle = None
		for handle in self.driver.window_handles:
		    if handle != main_window_handle:
		        popup_window_handle = handle
		        #break

		self.driver.switch_to.window(popup_window_handle)

	def openPerf(self, idperf, idtime):
		URL = 'http://ticket.yes24.com/Pages/Perf/Sale/PerfSaleProcess.aspx?IdPerf={}&IdTime={}'.format(idperf, idtime)
		self.driver.get(URL)
		self.stage = Stage.PERF_OPENED

	def goLastPage(self):
		print("Going to last page")
		# 1 Pass Calandar
		while True:
			e = self.driver.find_element_by_xpath("//img[@id='btnSeatSelect']")
			if e.is_displayed():
				self.driver.execute_script("arguments[0].click();", e)
				break
			print("btnSeatSelect button is not showing yet...")
			time.sleep(1)

		# 2 Seat
		ret = True
		while ret:
			self.selectRandomSeat()
			ret = self.detectAlert()

		# 3 Coupon
		# 4 Deliver
		self.nextStep()

	def selectRandomSeat(self):
		self.driver.switch_to.default_content()
		retry_xpath_empty(self.driver, "//div[@id='divFlash']")

		## switch frame
		#iframe = self.driver.find_element_by_xpath("//iframe[@id='ifrmSeatFrame']")	
		iframes = self.driver.find_elements_by_tag_name("iframe")	
		self.driver.switch_to.frame(iframes[0])

		# WAIT UNTIL PAGE LOADED
		retry_xpath_empty(self.driver, "//div[@id='divSeatArray']")
		divSeatArray = self.driver.find_element_by_xpath("//div[@id='divSeatArray']")

		# parse HTML into Seats
		soup = BeautifulSoup(divSeatArray.get_attribute("innerHTML"), "html.parser")
		seats = soup.findAll('div')
		colorSeats = [seat for seat in seats if seat['class'][0] != 's13']

		# click random seat
		idx = int(random.random() * len(colorSeats))
		print("selected random idx:", idx)
		wantSeatId = colorSeats[idx]['id']
		wantSeat = divSeatArray.find_element_by_xpath("//div[@id='{}']".format(wantSeatId))
		self.driver.execute_script("arguments[0].click();", wantSeat)
		time.sleep(1)

		## complete select seat
		try:
			e = self.driver.find_element_by_xpath("//*[@class='booking']")
			self.driver.execute_script("arguments[0].click();", e)
		except NoSuchElementException as e:
			print(str(e))

	def detectAlert(self):
		try:
			WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
							"Timed out for popup to appear")
			alert = self.driver.switch_to_alert()
			alert.accept()
			print("alert appeared. Just Clicked")
			return True
		except TimeoutException:
			print("no alert. Keep going to next step")
			return False

	def nextStep(self):
		self.driver.switch_to.default_content()
		#### COUPON
		e = retry_find_element_by_xpath(self.driver, "//a[contains(@onclick,'fdc_PromotionEnd')]")
		self.driver.execute_script("arguments[0].click();", e)

		#### DELIVERY
		retry_find_element_by_xpath(self.driver, "//span[@id='deliveryPos']")
		retry_input_empty(self.driver, 'ordererUserName')

		## 티켓 수령방법을 선택하세요.
		while True:
			checked = self.driver.execute_script("var rdos = document.getElementsByName('rdoDelivery');if(rdos.length>0) return rdos[0].checked;")
			print("checked:", checked)
			if checked:
				break
			time.sleep(0.2)

		## phone number check
		m1 = self.driver.execute_script("return document.getElementById('ordererMobile1').value;")
		m2 = self.driver.execute_script("return document.getElementById('ordererMobile2').value;")
		m3 = self.driver.execute_script("return document.getElementById('ordererMobile3').value;")
		if m1 == '' or m2 == '' or m3 == '':
			print("mobile num is empty...")
			self.change_element_value_by_id('ordererMobile1', '010')
			self.change_element_value_by_id('ordererMobile2', '0000')
			self.change_element_value_by_id('ordererMobile3', '0000')
			self.change_element_value_by_id('deliveryMobile1', '010')
			self.change_element_value_by_id('deliveryMobile2', '0000')
			self.change_element_value_by_id('deliveryMobile3', '0000')

		self.change_value_by_id(self.idperf)

		## Next button
		e = retry_find_element_by_xpath(self.driver, "//a[contains(@onclick,'fdc_DeliveryEnd')]")
		self.driver.execute_script("arguments[0].click();", e)

	def prepare_lastpage(self, payment_method=1, showcaptcha=True):
		### Generating CAPTCHA if not exists
		if self.driver.execute_script("return reCAPTCHAUse;") != 'Y' and showcaptcha:
			print("Generating captcha system")
			self.driver.execute_script("reCAPTCHAUse = 'YC';")
			captchaHtml = """<li class="d_line">
                                      <em class="blu">자동주문방지</em>
                                      <div class="con">
                                        
                                        <img src="" id="captchaImg" width="180px">
                                        <div style="position:absolute;left:190px;top:15px;"> 
                                            <a href="javascript:initCaptcha();"><img src="http://tkfile.yes24.com/img/common/ic_refresh.png" alt="새로고침" width="12px">새로고침</a>
                                            <input type="text" id="captchaText" name="captchaText" style="display:block; width:160px;height:22px;margin-top:5px; padding:3px;">
                                            <input type="hidden" id="captchaKey" name="captchaKey">
                                        </div>
                                      </div>
                                    </li>
			"""

			e = self.driver.find_element_by_xpath("//ul[@class='mb']")
			self.driver.execute_script("arguments[0].innerHTML = arguments[0].innerHTML + arguments[1];", e, captchaHtml)
			self.driver.execute_script("reCAPTCHAUse = 'YC';")
			self.driver.execute_script("initCaptcha();")

		# 2 credit card / 222 kakao bank / 22 bank
		if payment_method == 1:
			e = retry_find_element_by_xpath(self.driver, "//input[@idgroup='2']")
			self.driver.execute_script("arguments[0].click();", e)
		elif payment_method == 2:
			e = retry_find_element_by_xpath(self.driver, "//input[@idgroup='222']")
			self.driver.execute_script("arguments[0].click();", e)
		elif payment_method == 3:
			e = retry_find_element_by_xpath(self.driver, "//input[@idgroup='22']")
			self.driver.execute_script("arguments[0].click();", e)
			select = Select(self.driver.find_element_by_id("selBank"))
			# 50 KB / 11631 KEB / 57 NH / 11629 SH / 49 WOORI
			# 11634 POST / 11630 HANA / 11633 SC
			select.select_by_value("50")

		e = self.driver.find_element_by_id("cbxAllAgree")
		self.driver.execute_script("arguments[0].click();", e)
		#e = self.driver.find_element_by_id("cbxCancelFeeAgree")
		#self.driver.execute_script("arguments[0].click();", e)
		#e = self.driver.find_element_by_id("chkinfoAgree")
		#self.driver.execute_script("arguments[0].click();", e)


	def newCaptcha(self):
		if self.driver.execute_script("return reCAPTCHAUse;") != 'YC':
			return

		if self.tkseat != "":
			print("newCaptcha is aborted. booking is already done")
			return

		# backup captchaKey, captchaText
		while True:
			backup_captchaKey = self.driver.find_element_by_id("captchaKey").get_attribute("value")
			if backup_captchaKey != "":
				break
			print("captchaKey not set yet")
			time.sleep(1)

		backup_captchaText = self.driver.find_element_by_name('captchaText').get_attribute('value')
		print("backup captchaKey:{}, captchaText:{}".format(backup_captchaKey, backup_captchaText))

		# fill with empty captchaKey and renew captcha
		self.change_element_value_by_id('captchaKey', "")
		self.driver.execute_script("initCaptcha();")

		## captchaKey ready??
		while True:
			captchaKey = self.driver.find_element_by_id("captchaKey").get_attribute("value")
			print("captchaKey:", captchaKey)
			if captchaKey != "":
				break
			print("captchaKey not set yet")
			time.sleep(1)

		while True:
			## get base64 from <img src ...
			script = """
			var c = document.createElement('canvas');
			var ctx = c.getContext('2d');
			var img = document.getElementById('captchaImg');
			c.height=img.naturalHeight;
			c.width=img.naturalWidth;
			ctx.drawImage(img, 0, 0,img.naturalWidth, img.naturalHeight);
			var base64String = c.toDataURL('image/jpeg', 0.5);
			return base64String;
			"""

			try:
				img_base64 = self.driver.execute_script(script)
				#print("img_base64:", img_base64)
				if len(img_base64) < 3000:
					print("captchaImg is not loaded yet")
					continue
				break
			except WebDriverException as e:
				print(traceback.format_exc())
				print("Unknown issue happening in get base64 from image ... retrying")
				continue

		## 2-1) register captchaKey
		insertURL = "http://wangticket.com/yes24/ycaptcha/new_captcha.php?captchaKey={}&idperf={}&requester={}&pcname={}&pcid={}&adminid={}".format(captchaKey, self.idperf, self.userid, self.pcname, self.pcid, self.to)
		headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
		headers["Content-Type"] = "application/x-www-form-urlencoded"
		payload = {'captchaImg': img_base64}
		r = requests.post(insertURL, headers=headers, data=urlencode(payload))

		print("[new captcha]", r.status_code, r.reason, r.headers['Date'])
		print(r.text)
		#captchaId = int(r.text)

		# restore captchaKey, captchaText
		if backup_captchaText != "":
			print("restoring captchaKey:{}, captchaText:{}".format(backup_captchaKey, backup_captchaText))
			self.change_element_value_by_id('captchaKey', backup_captchaKey)
			self.driver.find_element_by_name('captchaText').send_keys(backup_captchaText)

	def popCaptcha(self):
		## 1) pop captchaKey
		URL = "http://wangticket.com/yes24/ycaptcha/pop_captcha.php?pcid={}".format(self.pcid)
		headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
		r = requests.get(URL, headers=headers)
		print("[pop captcha]", r.status_code, r.reason, r.headers['Date'])
		if r.text != '':
			print(r.text)
			data = r.json()

			if 'captchaKey' not in data:
				return False
			captchaKey = data['captchaKey']
			captchaText = data['captchaText']
			print("[pop captcha] key:{}, text:{}".format(captchaKey, captchaText))

			self.change_element_value_by_id('captchaKey', captchaKey)
			self.driver.find_element_by_name('captchaText').send_keys(captchaText)
			return True

		return False

	def handleCaptcha(self, captcha_self=False):
		if captcha_self:
			return

		if self.driver.execute_script("return reCAPTCHAUse;") != 'YC':
			print("captcha is not needed")
			return

		## captchaKey ready??
		while True:
			captchaKey = self.driver.find_element_by_id("captchaKey").get_attribute("value")
			print("captchaKey:", captchaKey)
			if captchaKey != "":
				break
			print("captchaKey not set yet")
			time.sleep(1)

		## captchaText empty??
		captchaText = self.driver.find_element_by_name('captchaText')
		if captchaText.get_attribute('value') != "":
			return

		ret = self.popCaptcha()
		if not ret:
			self.newCaptcha()
		else:
			return

		lastcaptchanotified = datetime.datetime.now()
		## 2-2) waiting captchaText ready!
		while True:

			## notify every 50secs
			s = datetime.datetime.now()
			if (s-lastcaptchanotified).seconds > 50:
				msg = "[{}] Don't forget Captcha!!!".format(self.userid)
				print(msg)
				self.notifyTelegram(message=msg)
				lastcaptchanotified = s

			time.sleep(5)

			ret = self.popCaptcha()
			if ret:
				break

		return

	def handleDialog(self):
		ALERT1 = "자동주문방지 문자를 잘못 입력하셨습니다."
		ALERT2 = "티켓 주문처리중 오류가 발생하였습니다."
		#"예매 완료까지 허용된 제한 시간이 만료 되어 예매를 완료 할 수 없습니다. 다시 예매 하여 주십시오!"
		#"오류 내용 : 좌석선점오류[62][235]"
		#"제휴처 좌석선점에 오류가 발생하였습니다.[45][335]"
		#티켓 주문처리중 오류가 발생하였습니다.[372]<br>예매중인 공연은 고객님 1인당 2매 까지만 예매/예약이 가능 한 공연 입니다. 기존 예매/예약분을 합하여 허용 기준을 초과 합니다
		#티켓 주문처리중 오류가 발생하였습니다.[861]<br>팬클럽 인증 정보가 없습니다. 팬클럽 인증 확인 후 예매하여 주시기 바랍니다.
		#""
		ALERT3 = "자동주문방지 문자를 입력해주세요."
		ALERT4 = "결제를 취소하셨습니다."
		ALERT5 = "가상계좌 발급중 오류가 발생하였습니다."
		ALERT6 = "허용 기준을 초과 합니다"
		ALERT7 = "팬클럽 인증 정보가 없습니다."
		ALERT8 = "다른 결제 방법을 선택하여 주십시오."

		content = self.driver.find_element_by_xpath("//div[@id='dialogAlert']")
		contentHTML = content.get_attribute('innerHTML')
		print("alert is displayed.", contentHTML)

		btn_xpath = "//button[@aria-disabled='false']"
		e = self.driver.find_element_by_xpath(btn_xpath)
		self.driver.execute_script("arguments[0].click();", e)
		print("alert clicked")

		if ALERT1 in contentHTML:
			return 1
		elif ALERT5 in contentHTML:
			return 3
		elif ALERT6 in contentHTML:
			return 4
		elif ALERT7 in contentHTML:
			return 5
		elif ALERT8 in contentHTML:
			return 6
		elif ALERT2 in contentHTML or ALERT4 in contentHTML:
			return 2
		else:
			return -1

	def enterOrderPage(self, bookno):
		## handling popup
		popup_window_handle = self.driver.current_window_handle
		main_window_handle = None
		for handle in self.driver.window_handles:
		    if handle != popup_window_handle:
		        main_window_handle = handle
		        break

		self.driver.switch_to.window(main_window_handle)

		URL = "http://ticket.yes24.com/Pages/MyPage/MyOrderTicketView.aspx?IdOrder={}".format(bookno)
		self.driver.get(URL)

	def handleBookSuccess(self):
		content = self.driver.find_elements_by_xpath("//div[@id='SuccessBoard']")

		if len(content)>0 and content[0].is_displayed():
			print("SuccessBoard is displayed")

			while True:
				try:
					#OLD:<strong id="bk_bookno" class="big">Y1532880152</strong>
					#NEW:<strong id="bk_bookno" class="big">1532880152</strong>
					bookno_xpath = "//strong[@id='bk_bookno']"
					bookno_e = self.driver.find_element_by_xpath(bookno_xpath)
					bookno = bookno_e.get_attribute('innerHTML')
					if len(bookno) < 10:
						print("bookno not displayed yet.. ", bookno)
						time.sleep(1)
						continue

					if not bookno.isdigit():
						bookno = bookno[1:]
					break
				except UnexpectedAlertPresentException as e:
					print(traceback.format_exc())
					# alert text check
					# 주문이 완료되었습니다.
					# 이용해 주셔서 감사합니다.

					alert = self.driver.switch_to.alert
					alertText = alert.text

					msg = "[{}] alert:{} (seat:{})".format(self.userid, alertText, self.trying_seat)
					print(msg)
					self.notifyTelegram(message=msg)
					bookno = ""
					tkseat = self.trying_seat
					break

			if bookno != "":
				tkseat_xpath = "//div[@id='bk_tkseat']"
				tkseat_e = self.driver.find_element_by_xpath(tkseat_xpath)
				tkseat = tkseat_e.get_attribute('innerText')
				self.bookno = bookno
				self.tkseat = tkseat
				#print("seat:", tkseat)
			print("[{}][{}] {}".format(self.userid, bookno, tkseat))

			# register bookingno
			playdatetime = '{}_{}'.format(self.playdate, self.playtime)
			URL = "http://wangticket.com/yes24/new_booking.php?yes24id={}&pcid={}&bookingno={}&datetime={}&seats={}".format(self.userid, self.pcname, bookno, playdatetime, tkseat)
			headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
			r = requests.get(URL, headers=headers)
			print("[new bookingno]", r.status_code, r.reason, r.headers['Date'])
			print(r.text)

			#self.enterOrderPage(bookno)


	def fixGiftAmount(self, money):
		yesgift = self.yesgift
		giftuse = self.giftuse

		total_money = money
		usedgiftinfo = ""

		soup = BeautifulSoup(yesgift, "html.parser")
		trs = soup.findAll('tr')
		if trs is not None:
			for tr in trs:
				giftkey = tr['giftkey']
				if giftuse != '' and giftkey.split('#')[1] not in giftuse:
					print("skip using gift:", giftkey)
					continue
				amount = int(tr['limitamount'])
				if total_money > amount:
					using_money = amount
				else:
					using_money = total_money

				usedgiftinfo = usedgiftinfo + "{}#{}^".format(giftkey, using_money)
				#print(giftkey, amount, using_money)
				total_money = total_money - using_money
				if total_money == 0:
					break

		print(usedgiftinfo)
		script = "fdc_PopupYesGiftUseEnd({},'{}');".format(money-total_money, usedgiftinfo)
		print(script)
		self.driver.execute_script(script)

	def notifySeatInfo(self):
		tk_seat = self.driver.execute_script("return document.getElementById('tk_seat').innerText;")
		msg = "[{}][Lock] {}".format(self.userid, tk_seat)
		print(msg)
		self.notifyTelegram(message=msg)

	def payHyundaiCard(self):
		iframe = self.driver.find_element_by_id("iframe")
		self.driver.switch_to.frame(iframe)

		#e = retry_find_element_by_xpath(self.driver, "//a[@id='cardCode10']")
		e = retry_find_element_by_xpath(self.driver, "//a[contains(@title,'현대카드')]")
		self.driver.execute_script("arguments[0].click();", e)

		# OFF POPUP
		self.driver.execute_script("overlayPopupOnOff2(false);")

		# if agr_utilzr exist, inputAll exist
		es = self.driver.find_elements_by_xpath("//div[contains(@class,'agr_utilzr')]")
		if len(es) > 0:
			self.driver.find_element_by_id("inputAll").click()
		self.driver.find_element_by_id("CardBtn").click()

		iframe = self.driver.find_element_by_xpath("//iframe[@id='overlayFrame']")
		self.driver.switch_to.frame(iframe)

		while True:
			try:
				self.driver.find_element_by_xpath("//a[contains(@href,'ExecAppCard')]").click()
				break
			except Exception as e:
				print("Exception happen finding ExecAppCard..", str(e))
				time.sleep(1)

		li = retry_find_element_by_xpath(self.driver, "//li[@class='numcode']")
		code_number = li.find_element_by_tag_name("p")
		card_code = ''.join(code_number.text.split())
		self.driver.execute_script("setInterval(doSubmitChk, 3500);")

		msg = "[{}] [현대] code:{}".format(self.userid, card_code)
		print(msg)
		self.notifyTelegram(message=msg)

		self.driver.switch_to.default_content()
		iframe = self.driver.find_element_by_id("iframe")
		self.driver.switch_to.frame(iframe)
		retry_click_element_by_xpath(self.driver, "//a[@id='payDoneBtn']")

		# checking if checkout element is gone
		self.driver.switch_to.default_content()
		while True:
			inicis_xpath = "//div[@id='inicisModalDiv']"
			inicis = self.driver.find_elements_by_xpath(inicis_xpath)
			if len(inicis)>0 and inicis[0].is_displayed():
				print("credit card checkout is still displayed..")
				time.sleep(0.5)
				continue
			else:
				print("credit card checkout is gone!")
				break

	def checkout(self):
		while True:
			## captcha empty??
			self.handleCaptcha()

			payprice = self.driver.execute_script("return fdc_Odr_PayMoney();")
			giftuse = self.driver.execute_script("return fdc_CALC_YesGiftPrice();")
			totalprice = payprice + giftuse
			print("totalprice:", totalprice)
			print("giftuse:", giftuse)
			if giftuse > 0 and totalprice != giftuse:
				print("totalprice and giftuse is different! need to change")
				self.fixGiftAmount(money=totalprice)

			self.trying_seat = self.driver.execute_script("return document.getElementById('tk_seat').innerText;")

			## checkout button
			e = self.driver.find_element_by_xpath("//img[@id='imgPayEnd']")
			self.driver.execute_script("arguments[0].click();", e)

			self.driver.implicitly_wait(1)

			## dialog check
			while True:
				try:
					prgrs_xpath = "//div[@aria-labelledby='ui-dialog-title-dialogPayProgress']"
					alert_xpath = "//div[@aria-labelledby='ui-dialog-title-dialogAlert']"
					inicis_xpath = "//div[@id='inicisModalDiv']"
					success_xpath = "//div[@id='SuccessBoard']"

					prgrs = self.driver.find_elements_by_xpath(prgrs_xpath)
					alert = self.driver.find_elements_by_xpath(alert_xpath)
					inicis = self.driver.find_elements_by_xpath(inicis_xpath)
					success = self.driver.find_elements_by_xpath(success_xpath)

					if len(prgrs)>0 and prgrs[0].is_displayed():
						print("prgrs is displayed")
						continue
					elif len(alert)>0 and alert[0].is_displayed():
						ret = self.handleDialog()
						if ret == 2:
							print("Should find new seats")
							return False
						elif ret == 1:
							print("Should enter captcha again")
							break
						elif ret == 3:
							print("Should click Pay button again")
							break
						elif ret == 4:
							msg = "[{}] 예매가능매수 초과".format(self.userid)
							print(msg)
							self.notifyTelegram(message=msg)
							print("Should find new seats after 10seconds")
							time.sleep(10)
							return False
						elif ret == 5:
							msg = "[{}] 팬클럽 미인증 계정".format(self.userid)
							print(msg)
							self.notifyTelegram(message=msg)
							print("Should find new seats after 10seconds")
							time.sleep(10)
							return False
						elif ret == 6:
							msg = "[{}] 카드결제만 허용?".format(self.userid)
							print(msg)
							self.notifyTelegram(message=msg)
							e = retry_find_element_by_xpath(self.driver, "//input[@idgroup='2']")
							self.driver.execute_script("arguments[0].click();", e)
							print("Should click Pay button again.. after select credit card")
							break
					elif len(inicis)>0 and inicis[0].is_displayed():
						print("credit card checkout displayed")
						self.notifySeatInfo()
						self.payHyundaiCard()
						continue
					elif len(success)>0 and success[0].is_displayed():
						print("SuccessBoard is ready")
						return True
					else:
						print("nothing displayed...waiting..")
						continue
				except UnexpectedAlertPresentException as e:
					print(traceback.format_exc())
					# alert text check
					# 주문이 완료되었습니다.
					# 이용해 주셔서 감사합니다.

					alert = self.driver.switch_to.alert
					alertText = alert.text

					if '자동주문방지 문자를 잘못 입력하셨습니다' in alertText:
						alert.accept()
						print("alert accepted")
						break
					else:
						msg = "[{}] alert:{} (seat:{})".format(self.userid, alertText, self.trying_seat)
						print(msg)
						self.notifyTelegram(message=msg)
						time.sleep(10)

				except WebDriverException as e:
					print(traceback.format_exc())
					print("This error temporarily happens in Windows..")
				time.sleep(1)

			self.driver.implicitly_wait(5)

	def change_value_by_id(self, vid):
		self.driver.execute_script("jgIdPerf={}".format(vid))

	def change_element_value_by_id(self, eid, v):
		script = "document.getElementById('{}').value = '{}';".format(eid,v)
		self.driver.execute_script(script)
		while True:
			script = "return document.getElementById('{}').value;".format(eid)
			ret = self.driver.execute_script(script)
			if ret != v:
				time.sleep(0.1)
				print("value:",ret, ", changing to:", v)
			else:
				break

	def change_element_int_value_by_id(self, eid, v):
		script = "document.getElementById('{}').value = {};".format(eid,v)
		self.driver.execute_script(script)
		while True:
			script = "return document.getElementById('{}').value;".format(eid)
			ret = self.driver.execute_script(script)
			if int(ret) != v:
				time.sleep(0.1)
				print("value:",ret, ", changing to:", v)
			else:
				break

	def change_element_html_by_id(self, eid, html):
		script = "document.getElementById('{}').innerHTML = \"{}\";".format(eid,html)
		self.driver.execute_script(script)

	def notifyTelegram(self, message):
		try:
			message = "[y][{}]".format(self.pcname) + message
			URL = "http://wangticket.com/melon/send_message.php?to={}&message={}".format(self.to, message)
			headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
			r = requests.get(URL, headers=headers)
			print("[notifyTelegram]", r.status_code, r.reason, r.headers['Date'])
			#print(r.text)
		except Exception as err:
			print("Exception happen in notifyTelegram...", str(err))


def retry_click_element_by_xpath(driver, xpath):
	while True:
		try:
			element = driver.find_element_by_xpath(xpath)
			element.click()
			break
		except:
			print("failed to click.", xpath)
			time.sleep(0.2)
	return element


def retry_find_element_by_xpath(driver, xpath):
	while True:
		elements = driver.find_elements_by_xpath(xpath)
		if len(elements) == 0:
			print("length of element is 0.", xpath)
			time.sleep(0.2)
			continue

		if elements[0].is_displayed():
			break
		else:
			print("element is not displayed yet.", xpath)
			time.sleep(0.2)

	return elements[0]

def retry_input_empty(driver, inputid):
	while True:
		element = driver.find_element_by_id(inputid)
		if element.get_attribute('value') == '':
			print("input is empty yet.", inputid)
			time.sleep(0.2)
		else:
			break
	return

def retry_xpath_empty(driver, xpath):
	while True:
		elements = driver.find_elements_by_xpath(xpath)
		if len(elements) == 0:
			print("there is not xpath yet.", xpath)
			time.sleep(0.2)
			continue

		if elements[0].get_attribute('innerHTML') == '':
			print("xpath is empty yet.", xpath)
			time.sleep(0.2)
		else:
			break
	return

