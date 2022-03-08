import player
import exchange
import net
import app
import locale
import localegame
import event
import chat
import item
import constInfo
import playerSettingModule
import ui
import mouseModule
import uiPickMoney
import wndMgr
import gameInfo
import time
import os
import uiToolTip
import guild
import ime
import systemSetting

FACE_IMAGE_DICT = {
	playerSettingModule.RACE_WARRIOR_M	: "icon/face/warrior_m.tga",
	playerSettingModule.RACE_WARRIOR_W	: "icon/face/warrior_w.tga",
	playerSettingModule.RACE_ASSASSIN_M	: "icon/face/assassin_m.tga",
	playerSettingModule.RACE_ASSASSIN_W	: "icon/face/assassin_w.tga",
	playerSettingModule.RACE_SURA_M		: "icon/face/sura_m.tga",
	playerSettingModule.RACE_SURA_W		: "icon/face/sura_w.tga",
	playerSettingModule.RACE_SHAMAN_M	: "icon/face/shaman_m.tga",
	playerSettingModule.RACE_SHAMAN_W	: "icon/face/shaman_w.tga",
}

ITEMSLOT = []
ITEMSLOT_INFO = ""
ITEM_EKLE = 0

ITEMSLOT_R = {}
ITEMSLOT_R_I = {}

MONEY_SET = 0
TICARET_KAPAT = 0
TICARET_BASARILI = 0

ITEMSLOT_MY = {}

class MultiExchangeDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.isLoaded = FALSE
		self.ItemSlot = -1
		self.ItemVnum = -1

		self.Loading = 1
		self.Full = 0
		self.Zaman = 0

		self.Para = 0

		self.dlgPickMoney = MoneyDialogSET()
		self.dlgPickMoney.LoadDialog()
		self.dlgPickMoney.Hide()

	def __Initialize(self):
		self.dlgQuestion = None
		self.children = []

	def __LoadScript(self):

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/multi_exchangedialog.py")

		except:
			import exception
			exception.Abort("MultiExchangeDialog.__LoadScript.LoadObject")

		try:

			self.board = self.GetChild("board")
			self.titleBar = self.GetChild("TitleBar")
			self.wndSlot = self.GetChild("Owner_Slot")
			self.wndSlot_Target = self.GetChild("Target_Slot")

		except:
			import exception
			exception.Abort("MultiExchangeDialog.__LoadScript.BindObject")

		toolTip = uiToolTip.ItemToolTip()
		self.toolTip = toolTip

		self.wndSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.wndSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.wndSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		self.wndSlot.SetUsableItem(TRUE)
		self.wndSlot_Target.SetOverInItemEvent(ui.__mem_func__(self.OverInItem_Target))
		self.wndSlot_Target.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.CancelExchange))
		self.isLoaded = TRUE

		self.GetChild("Target_Level").SetFontColor(255, 43, 255)
		self.GetChild("My_Level").SetFontColor(255, 43, 255)
		self.GetChild("My_Name").SetFontColor(255*255, 0*255, 8*255)
		
		self.GetChild("My_Money").SetEvent(ui.__mem_func__(self.__MyMoneySet))
		self.GetChild("Owner_Accept_Button").SetToggleDownEvent(ui.__mem_func__(self.Accept))

		self.GetChild("My_Accepted").Hide()
		self.GetChild("Target_Accepted").Hide()
		self.GetChild("Successfully_Islem").Hide()
		self.GetChild("Loading_Islem").Hide()
		self.GetChild("Accepted_Close").Hide()
		self.GetChild("Accepted_Close").SetEvent(ui.__mem_func__(self.Close))

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.ClearDictionary()
		self.dlgQuestion = None
		self.board = 0
		self.successPercentage = None
		self.children = []

	def Open(self):
		global TICARET_BASARILI
		if FALSE == self.isLoaded:
			self.__LoadScript()

		self.__Initialize()

		self.SetTop()
		self.Show()

		TICARET_BASARILI = 0
		gameInfo.UZAKTAN_TICARET_DURUM = 1
		#gameInfo.PYTHONISLEM = "uzaktan_ticaret_folder_remove#"+str(gameInfo.UZAKTAN_TICARET_RAKIP)+"#"
		#event.QuestButtonClick(gameInfo.PYTHONTOLUA)

	def Close(self):
		global TICARET_KAPAT
		self.dlgQuestion = None
		if TICARET_KAPAT == 0:
			net.SendWhisperPacket(gameInfo.UZAKTAN_TICARET_RAKIP, "#uzaktan_ticaret_iptal#")
			
		TICARET_KAPAT = 0
		self.RemoveAlls()
		self.Hide()

	def RemoveAlls(self):
		global ITEMSLOT
		global ITEMSLOT_INFO
		global ITEM_EKLE
		global ITEMSLOT_R
		global ITEMSLOT_R_I
		global MONEY_SET
		global ITEMSLOT_MY

		ITEMSLOT = []
		ITEMSLOT_INFO = ""
		ITEM_EKLE = 0
		ITEMSLOT_R = {}
		ITEMSLOT_R_I = {}
		MONEY_SET = 0
		ITEMSLOT_MY = {}

		#gameInfo.UZAKTAN_TICARET_KISILER = {}
		if "kisi_"+str(gameInfo.UZAKTAN_TICARET_RAKIP) in gameInfo.UZAKTAN_TICARET_KISILER.keys():
			del gameInfo.UZAKTAN_TICARET_KISILER["kisi_"+str(gameInfo.UZAKTAN_TICARET_RAKIP)]
		gameInfo.UZAKTAN_TICARET_RAKIP = ""
		gameInfo.UZAKTAN_TICARET_DURUM = 0
		gameInfo.UZAKTAN_TICARET_PARA_TARGET = 0
		gameInfo.UZAKTAN_TICARET_PARA_MY = 0

	def ChangeToBonus(self):
		pass

	def OverInItem(self, index):
		global ITEMSLOT_MY
		self.toolTip.ClearToolTip()
		self.toolTip.Show()
		if index in ITEMSLOT_MY.keys():
			slotIndex = ITEMSLOT_MY[index]

			itemVnum = player.GetItemIndex(slotIndex)
			itemCount = player.GetItemCount(slotIndex)
			
			metinSlot = [player.GetItemMetinSocket(slotIndex, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
			attrSlot = [player.GetItemAttribute(slotIndex, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
			
			self.toolTip.AddRefineItemData(itemVnum, metinSlot, attrSlot)

	def OverInItem_Target(self, slotNumber):
		global ITEMSLOT_R
		global ITEMSLOT_R_I
		self.toolTip.ClearToolTip()
		self.toolTip.Show()
		if "slot"+str(slotNumber) in ITEMSLOT_R.keys():
			slotIndex = ITEMSLOT_R_I["slot"+str(slotNumber)].split("#")

			#metinList = {}
			#metinList["metin"] = list(eval(slotIndex[3]))
				
			#attrList = {}
			#attrList["attr"] = list(eval(slotIndex[4]))
			
			#itemVnum = player.GetItemIndex(int(slotIndex[1]))
			itemVnum = player.GetItemIndex(int(slotIndex[1]))
			#itemCount = player.GetItemCount(int(slotIndex[2]))
			itemCount = player.GetItemCount(int(slotIndex[2]))

			items = ITEMSLOT_R_I["slot"+str(slotNumber)].split("#")

			metinAttr = [int(items[4]),int(items[5]),int(items[6]),int(items[7]),int(items[8]),int(items[9])]
			slotAttr =  [(int(items[10]),int(items[11])),(int(items[12]),int(items[13])),(int(items[14]),int(items[15])),(int(items[16]),int(items[17])),(int(items[18]),int(items[19])),(int(items[20]),int(items[21])),(int(items[22]),int(items[23]))]
	
			self.toolTip.AddRefineItemData(int(slotIndex[1]), metinAttr, slotAttr)
			#self.toolTip.AddRefineItemData(int(slotIndex[1]), metinList["metin"], attrList["attr"])
			
	def OverOutItem(self):
		self.toolTip.Hide()

	def SelectEmptySlot(self, selectedSlotPos):
		global ITEMSLOT
		global ITEMSLOT_MY

		if FALSE == mouseModule.mouseController.isAttached():
			return

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()

			if player.IsEquipmentSlot(attachedSlotPos):
				return
			
			if attachedSlotPos in ITEMSLOT:
				return

			if gameInfo.UZAKTAN_TICARET_DURUM == 2 or gameInfo.UZAKTAN_TICARET_DURUM == 3 or gameInfo.UZAKTAN_TICARET_DURUM == 4:
				return	
			
			itemVnum = player.GetItemIndex(attachedSlotPos)
			if player.SLOT_TYPE_INVENTORY == attachedSlotType:

				item.SelectItem(itemVnum)
				
				if item.IsAntiFlag(item.ANTIFLAG_GIVE):
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.EXCHANGE_CANNOT_GIVE)
					mouseModule.mouseController.DeattachObject()
					return

				#if item.IsAntiFlag(item.ANTIFLAG_GIVE):
				#	chat.AppendChat(chat.CHAT_TYPE_INFO, locale.EXCHANGE_CANNOT_GIVE)
				#	mouseModule.mouseController.DeattachObject()
				#	return

				if int(player.GetItemCount(int(attachedSlotPos))) == 1:
					self.wndSlot.SetItemSlot(int(selectedSlotPos), int(player.GetItemIndex(int(attachedSlotPos))), 0)
				else:
					self.wndSlot.SetItemSlot(int(selectedSlotPos), int(player.GetItemIndex(int(attachedSlotPos))), int(player.GetItemCount(int(attachedSlotPos))))
				ITEMSLOT.append(attachedSlotPos)
				ITEMSLOT_MY[selectedSlotPos] = attachedSlotPos
	

				slotIndex = attachedSlotPos
				itemVnum = player.GetItemIndex(slotIndex)
				itemCount = player.GetItemCount(slotIndex)

				metinSlot = [player.GetItemMetinSocket(slotIndex, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
				attrSlot = [player.GetItemAttribute(slotIndex, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]

				gameInfo.PYTHONISLEM = "uzaktan_ticaret_ekle#"+str(attachedSlotPos)+"#"+str(gameInfo.UZAKTAN_TICARET_RAKIP)+"#"+str(selectedSlotPos)+"#"
				event.QuestButtonClick(gameInfo.PYTHONTOLUA)

				#net.SendWhisperPacket(gameInfo.UZAKTAN_TICARET_RAKIP, "#uzaktan_ticaret_itemekle#"+str(selectedSlotPos)+"#"+str(attachedSlotPos)+"#"+str(itemVnum)+"#"+str(itemCount)+"#"+str(metinSlot)+"#"+str(attrSlot)+"#")
				
		mouseModule.mouseController.DeattachObject()
	
	def Accept(self):
		self.GetChild("My_Accepted").Show()
		#self.GetChild("Target_Accepted").Show()
		self.GetChild("Owner_Accept_Button").Disable()

		if gameInfo.UZAKTAN_TICARET_DURUM == 3:
			gameInfo.PYTHONISLEM = "uzaktan_ticaret_gerceklestir#"+str(gameInfo.UZAKTAN_TICARET_RAKIP)+"#"+str(player.GetName())+"#"
			event.QuestButtonClick(gameInfo.PYTHONTOLUA)
			gameInfo.UZAKTAN_TICARET_DURUM = 4
			self.Full = 0
			self.Loading = 0
			self.Zaman = app.GetTime()
	
		else:
			gameInfo.UZAKTAN_TICARET_DURUM = 2
			gameInfo.PYTHONISLEM = "uzaktan_ticaret_kabul_ediyorum#"+str(gameInfo.UZAKTAN_TICARET_RAKIP)
			event.QuestButtonClick(gameInfo.PYTHONTOLUA)

		##self.GetChild("My_Accepted").Hide()# sonra sil.
	
		net.SendWhisperPacket(gameInfo.UZAKTAN_TICARET_RAKIP, "#uzaktan_ticaret_kabul#")

	def __MyMoneySet(self):
		if gameInfo.UZAKTAN_TICARET_DURUM == 2 or gameInfo.UZAKTAN_TICARET_DURUM == 3 or gameInfo.UZAKTAN_TICARET_DURUM == 4:
			chat.AppendChat(chat.CHAT_TYPE_INFO, 'Toplamý þuanda deðiþtirmezsin.')
			return
		self.dlgPickMoney.SetTitleName('Toplam')
		self.dlgPickMoney.SetAcceptText('Tamam')
		self.dlgPickMoney.Open(player.GetElk())
		self.dlgPickMoney.SetMax(10)
		self.dlgPickMoney.Show()

	def CloseTheAllsGadgets(self):
		self.GetChild("Target_Face_Slot").Hide()
		self.GetChild("Target_Character_Image").Hide()
		self.GetChild("Target_Level").Hide()
		self.GetChild("Target_Name").Hide()
		self.GetChild("Target_Guild").Hide()
		self.GetChild("Target_Money").Hide()
		self.GetChild("My_Face_Slot").Hide()
		self.GetChild("My_Character_Image").Hide()
		self.GetChild("My_Level").Hide()
		self.GetChild("My_Name").Hide()
		self.GetChild("My_Guild").Hide()
		self.GetChild("My_Money").Hide()
		self.GetChild("Target").Hide()
		self.GetChild("Owner").Hide()
		self.GetChild("Owner_Accept_Button").Hide()
		self.GetChild("My_Accepted").Hide()
		self.GetChild("Target_Accepted").Hide()
		self.GetChild("Owner_Accept_Button").Hide()
		#self.GetChild("Loading_Islem").Hide()

	def OnUpdate(self):
		global ITEMSLOT_INFO
		global ITEM_EKLE
		global ITEMSLOT_R
		global ITEMSLOT_R_I
		global TICARET_KAPAT
		global TICARET_BASARILI
		
		self.GetChild("TitleName").SetText(str(gameInfo.UZAKTAN_TICARET_RAKIP) + " adlý oyuncuyla uzaktan ticaret")
		self.GetChild("Target_Character_Image").LoadImage(FACE_IMAGE_DICT[int(gameInfo.UZAKTAN_TICARET_KISILER["kisi_"+str(gameInfo.UZAKTAN_TICARET_RAKIP)].split("#")[3])])
		self.GetChild("Target_Level").SetText("Lv. " + str(gameInfo.UZAKTAN_TICARET_KISILER["kisi_"+str(gameInfo.UZAKTAN_TICARET_RAKIP)].split("#")[1]))
		self.GetChild("Target_Name").SetText(str(gameInfo.UZAKTAN_TICARET_RAKIP))
		self.GetChild("Target_Guild").SetText(str(gameInfo.UZAKTAN_TICARET_KISILER["kisi_"+str(gameInfo.UZAKTAN_TICARET_RAKIP)].split("#")[2]))
		self.GetChild("Target_Money_Value").SetText(locale.NumberToMoneyString(str(gameInfo.UZAKTAN_TICARET_PARA_TARGET)))
		self.GetChild("My_Character_Image").LoadImage(FACE_IMAGE_DICT[net.GetMainActorRace()])
		self.GetChild("My_Level").SetText("Lv. " + str(player.GetStatus(player.LEVEL)))
		self.GetChild("My_Name").SetText("Sen")
		self.GetChild("My_Money_Value").SetText(locale.NumberToMoneyString(str(gameInfo.UZAKTAN_TICARET_PARA_MY)))
		if not guild.IsGuildEnable():
			self.GetChild("My_Guild").SetText("Lonca yok.")
		else:
			self.GetChild("My_Guild").SetText(str(player.GetGuildName()))

		if ITEM_EKLE == 1:
			bol = ITEMSLOT_INFO.split("#")
			#ITEMSLOT_R["slot"+str(bol[1])] = int(bol[2])
			ITEMSLOT_R["slot"+str(bol[26])] = int(bol[3])
			#ITEMSLOT_R_I["slot"+str(bol[1])] = "#"+str(bol[3])+"#"+str(bol[4])+"#"+str(bol[5])+"#"+str(bol[6])+"#"
			ITEMSLOT_R_I["slot"+str(bol[26])] = ITEMSLOT_INFO
			if int(bol[2]) == 1:
				self.wndSlot_Target.SetItemSlot(int(bol[26]), int(bol[1]), 0)
			else:
				self.wndSlot_Target.SetItemSlot(int(bol[26]), int(bol[1]), int(bol[2]))
			ITEM_EKLE = 0

		if gameInfo.UZAKTAN_TICARET_DURUM == 3:
			self.GetChild("Target_Accepted").Show()

		if TICARET_KAPAT == 1:
			self.Close()

		if TICARET_BASARILI == 1:
			self.Full = 0
			self.Loading = 0
			self.Zaman = app.GetTime()
			#gameInfo.PYTHONISLEM = "uzaktan_ticaret_gerceklestir#"+str(gameInfo.UZAKTAN_TICARET_RAKIP)+"#"
			#event.QuestButtonClick(gameInfo.PYTHONTOLUA)
			TICARET_BASARILI = 0

		if self.Full < 102 and self.Loading == 0:
			self.CloseTheAllsGadgets()
			self.GetChild("Loading_Islem").SetFontName("Tahoma:60")
			self.GetChild("Loading_Islem").SetText("%"+str(self.Full))
			self.Full += 1

		if self.Full == 101 and self.Loading == 0:
			self.GetChild("Loading_Islem").Hide()
			self.Loading = 1

		if app.GetTime() < self.Zaman + 2 and gameInfo.UZAKTAN_TICARET_DURUM == 4:
			self.GetChild("Loading_Islem").Show()
			self.GetChild("Successfully_Islem").Hide()
		else:
			if gameInfo.UZAKTAN_TICARET_DURUM == 4:
				self.CloseTheAllsGadgets()
				self.GetChild("Loading_Islem").Hide()
				self.SetSize(272, 435 + 37 + 20 + 9 - 207)
				self.SetPosition(systemSetting.GetWidth() - 176 - 269, systemSetting.GetHeight() - 37 - 565 + 36 + 207 - 102) 
				self.GetChild("board").SetSize(272, 435 + 37 + 20 + 9 - 207)
				self.GetChild("Accepted_Close").SetPosition(0, 329 - 107)
				self.GetChild("Accepted_Close").Show()
				self.GetChild("Successfully_Islem").SetPosition(19, 150 - 28 - 62)
				self.GetChild("Successfully_Islem").Show()
				self.GetChild("TitleName").SetText("Uzaktan ticaret baþarýyla tamamlandý!")

	def CancelExchange(self):
		self.Close()

class MoneyDialogSET(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.unitValue = 1
		self.maxValue = 0
		self.eventAccept = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/PickMoneyDialog.py")
		except:
			import exception
			exception.Abort("MoneyDialog.LoadDialog.LoadScript")

		try:
			self.board = self.GetChild("board")
			self.maxValueTextLine = self.GetChild("max_value")
			self.pickValueEditLine = self.GetChild("money_value")
			self.acceptButton = self.GetChild("accept_button")
			self.cancelButton = self.GetChild("cancel_button")
		except:
			import exception
			exception.Abort("MoneyDialog.LoadDialog.BindObject")

		self.pickValueEditLine.SetReturnEvent(ui.__mem_func__(self.OnAccept))
		self.pickValueEditLine.SetEscapeEvent(ui.__mem_func__(self.Close))
		self.acceptButton.SetEvent(ui.__mem_func__(self.OnAccept))
		self.cancelButton.SetEvent(ui.__mem_func__(self.Close))
		self.board.SetCloseEvent(ui.__mem_func__(self.Close))

	def Destroy(self):
		self.ClearDictionary()
		self.eventAccept = 0
		self.maxValue = 0
		self.pickValueEditLine = 0		
		self.acceptButton = 0
		self.cancelButton = 0
		self.board = None

	def SetTitleName(self, text):
		self.board.SetTitleName(text)

	def SetAcceptText(self, gelen):
		self.acceptButton.SetText(str(gelen))
		
	def SetAcceptEvent(self, event):
		self.eventAccept = event

	def SetMax(self, max):
		self.pickValueEditLine.SetMax(max)

	def Open(self, maxValue, unitValue=1):

		if locale.IsYMIR() or locale.IsCHEONMA() or locale.IsHONGKONG():
			unitValue = ""

		width = self.GetWidth()
		(mouseX, mouseY) = wndMgr.GetMousePosition()

		if mouseX + width/2 > wndMgr.GetScreenWidth():
			xPos = wndMgr.GetScreenWidth() - width
		elif mouseX - width/2 < 0:
			xPos = 0
		else:
			xPos = mouseX - width/2

		self.SetPosition(xPos, mouseY - self.GetHeight() - 20)

		if locale.IsARABIC():
			self.maxValueTextLine.SetText("/" + str(maxValue))
		else:
			self.maxValueTextLine.SetText(" / " + str(maxValue))

		self.pickValueEditLine.SetText(str(unitValue))
		self.pickValueEditLine.SetFocus()

		ime.SetCursorPosition(1)

		self.unitValue = unitValue
		self.maxValue = maxValue
		self.Show()
		self.SetTop()

	def Close(self):
		self.pickValueEditLine.KillFocus()
		gameInfo.MONEY_INPUT = 0
		self.Hide()

	def OnAccept(self):

		text = self.pickValueEditLine.GetText()

		if len(text) > 0 and text.isdigit():

			money = int(text)
			money = min(money, self.maxValue)

			if money > 0:
				if self.eventAccept:
					self.eventAccept(money)

			if player.GetElk() < int(text):
				chat.AppendChat(chat.CHAT_TYPE_INFO, "<Sistem> : Yeterli yang yok.")
				return

			gameInfo.PYTHONISLEM = "uzaktan_ticaret_para_ekle#"+str(text)+"#"+str(gameInfo.UZAKTAN_TICARET_RAKIP)+"#"
			event.QuestButtonClick(gameInfo.PYTHONTOLUA)
			#net.SendWhisperPacket(gameInfo.UZAKTAN_TICARET_RAKIP, "#uzaktan_ticaret_paraekle#"+str(text)+"#")
			gameInfo.UZAKTAN_TICARET_PARA_MY = int(text)
				
			#gameInfo.DUELLO_BENIM_PARA = int(text)
			#gameInfo.PYTHONISLEM = "duello_para_ekle#"+str(text)+"#"+str(gameInfo.DUELLO_RAKIP)+"#"
			#event.QuestButtonClick(gameInfo.PYTHONTOLUA)

		self.Close()

class OyuncuTeklifManager(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isLoaded = FALSE
		self.type = None
		self.yatirButton = None
		self.cekButton = None
		self.Money = None
		
	def __LoadScript(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/moneydialog.py")
		except:
			import exception
			exception.Abort("test.__LoadScript.LoadObject")

		try: 
			self.board = self.GetChild("Board")
			self.titleBar = self.GetChild("TitleBar")
			self.yatirButton = self.GetChild("yatirButton")
			self.cekButton = self.GetChild("cekButton")
			self.girilenInput = self.GetChild("Input")
			
			self.yang_text = self.GetChild("yang_girilen")
			self.yang_slot = self.GetChild("yang_resim")
			self.yang_input = self.GetChild("Input")

			self.board.SetSize(210, 90)
			self.SetPosition(210, 90)
			self.cekButton.Hide()
			self.titleBar.SetWidth(210-15)

			self.GirdiginPara = ui.TextLine_Alisveris()
			self.GirdiginPara.SetParent(self.board)
			self.GirdiginPara.SetPosition(0, 35)
			#if self.girilenInput.GetText() == "" or self.girilenInput.GetText() == 0:
			self.GirdiginPara.SetText("Oyuncu adýný girin:")
			#else:
				#self.GirdiginPara.SetText(str(locale.NumberToMoneyString(self.girilenInput.GetText())))
			self.GirdiginPara.SetWindowHorizontalAlignCenter()
			self.GirdiginPara.SetHorizontalAlignCenter()
			self.GirdiginPara.Show()

		except:
			import exception
			exception.Abort("test.__LoadScript.BindObject")
			
		self.girilenInput.SetMax(16)
		#self.girilenInput.SetNumberMode()
			
		self.yatirButton.SetEvent(self.__Gonder)
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		self.isLoaded = TRUE

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def Destroy(self):
		self.Hide()
		
	def Open(self):
		if FALSE == self.isLoaded:
			self.__LoadScript()
		self.SetTop()
		self.SetCenterPosition()
		self.Show()

		self.Islem()
		
	def GetType(self):
		return self.type
	
	def __Gonder(self):
		ad = self.girilenInput.GetText()
		race = net.GetMainActorRace()
		if ad == "":
			self.Chat('<Sistem> : Ticaret isteði yollamak istediðiniz kiþinin adýný girin!')
			return

		if not guild.IsGuildEnable():
			net.SendWhisperPacket(ad, "#uzaktan_ticaret_teklifi#"+str(player.GetStatus(player.LEVEL))+"#Lonca yok.#"+str(race))
		else:
			net.SendWhisperPacket(ad, "#uzaktan_ticaret_teklifi#"+str(player.GetStatus(player.LEVEL))+"#"+str(player.GetGuildName())+"#"+str(race))

		self.Close()
	
	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return TRUE

	def Islem(self): #islem, item sira, item kodu, item satici, fiyat
		self.GetChild("TitleName").SetText("Uzaktan Ticaret Teklifi")
		self.yatirButton.SetText("Gönder")
		self.yatirButton.SetToolTipText("Ona uzaktan ticaret için teklif gönder!")
		self.GetChild("yang_girilen").Hide()

		self.GetChild("yang_resim").LoadImage("d:/ymir work/ui/public/Parameter_Slot_04.sub")
		self.GetChild("yang_resim").SetPosition(48-36,40+19)
		self.girilenInput.SetPosition(50-36, 40+19)
		self.girilenInput.SetText("")

		self.yatirButton.SetPosition(140-6, 40+19)

	def OnUpdate(self):
		pass

	def OnPressExitKey(self):
		self.Close()
		return TRUE

class Bug_Fatihbab34(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

	def __del__(self):
		ui.ScriptWindow.__del__(self)
