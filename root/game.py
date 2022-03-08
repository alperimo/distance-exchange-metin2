import uiExchange_Multi
import time
import gameInfo
import event
import guild
import localegame

	def __PressQuickSlot(self, localSlotIndex):
		if gameInfo.UZAKTAN_TICARET_DURUM == 1:
			chat.AppendChat(chat.CHAT_TYPE_INFO,"Uzaktan ticaret açıkken item kullanamazsın.")
			return

	def __ServerCommand_Build(self):
		serverCommandList={

			## New System Plugin ##
			"PythonToLua"			: self.__PythonToLua, # .python to Quest
			"PythonIslem"			: self.__PythonIslem, # .python to Quest
			"LuaToPython"			: self.__LuaToPython, # Quest to .python
			## END - New System Plugin - END ##

		}

	##replace the funtion##
	def OpenQuestWindow(self, skin, idx):
		if gameInfo.INPUT == 1:
			return
		self.interface.OpenQuestWindow(skin, idx)

	##add the new funtions##
	def __PythonToLua(self, id):
		gameInfo.PYTHONTOLUA = int(id)

	def __PythonIslem(self, PythonIslem):
		if PythonIslem == "PYTHONISLEM":
			net.SendQuestInputStringPacket(gameInfo.PYTHONISLEM)

	def __LuaToPython(self, LuaToPython):
		if LuaToPython.find("#quest_input#") != -1:
			gameInfo.INPUT = 1
		elif LuaToPython.find("#quest_inputbitir#") != -1:
			gameInfo.INPUT = 0
		elif LuaToPython.find("uzaktan_ticaret_item_ekle") != -1:
			bol_2 = LuaToPython.split("|")
			bol = LuaToPython.split("#")
			#uiExchange_Multi.ITEMSLOT_INFO = "#"+str(bol[2])+"#"+str(bol[3])+"#"+str(bol[4])+"#"+str(bol[5])+"#"+bol[6]+"#"+bol[7]+"#"
			uiExchange_Multi.ITEMSLOT_INFO = bol_2[1]
			uiExchange_Multi.ITEM_EKLE = 1

		elif LuaToPython.find("uzaktan_ticaret_para_ekle") != -1:
			bol = LuaToPython.split("#")
			gameInfo.UZAKTAN_TICARET_PARA_TARGET = int(bol[1])
			
		elif LuaToPython.find("uzaktan_ticaret_parabenim_ekle") != -1:
			gameInfo.UZAKTAN_TICARET_PARA_MY = 0


	def OnRecvWhisper(self, mode, name, line):
		if line.find("uzaktan_ticaret_teklifi") != -1:
			bol = line.split("#")
			if line.find("cevap") != -1:
				if gameInfo.UZAKTAN_TICARET_DURUM != 0:
					net.SendWhisperPacket(name, "#uzaktan_ticaret_teklifi_kap2at#")
					return
				target_level = bol[3]
				target_lonca = bol[4]
				target_sinif = bol[5]
				gameInfo.UZAKTAN_TICARET_KISILER["kisi_"+str(name)] = "#"+str(target_level)+"#"+str(target_lonca)+"#"+str(target_sinif)+"#"
				gameInfo.UZAKTAN_TICARET_RAKIP = name
				gameInfo.PYTHONISLEM = "uzaktan_ticaret_folder_remove#"+str(gameInfo.UZAKTAN_TICARET_RAKIP)+"#"
				event.QuestButtonClick(gameInfo.PYTHONTOLUA)
				self.ac = uiExchange_Multi.MultiExchangeDialog()
				self.ac.Open()
				self.interface.ToggleInventoryWindow_UzaktanTicaret()
				return
			
			if line.find("kap2at") != -1:
				uiExchange_Multi.TICARET_KAPAT = 1
				chat.AppendChat(chat.CHAT_TYPE_INFO, localegame.UZAKTAN_TICARET_RAKIP_TICARETTE)
				return
			
			if line.find("kapat") != -1:
				#uiExchange_Multi.TICARET_KAPAT = 1
				chat.AppendChat(chat.CHAT_TYPE_INFO, localegame.UZAKTAN_TICARET_RAKIP_TICARETTE)
				return

			if gameInfo.UZAKTAN_TICARET_DURUM != 0:
				net.SendWhisperPacket(name, "#uzaktan_ticaret_teklifi_kapat#")
				return

			if os.path.exists(str(gameInfo.CLIENT_YOL) + "uzaktanticaret_"+str(player.GetName())+".kf"):
				return

			target_level = bol[2]
			target_lonca = bol[3]
			target_sinif = bol[4]
			self.TicaretDialog = uiCommon.QuestionDialog()
			self.TicaretDialog.SetText(localegame.UZAKTAN_TICARET % (str(name)))
			self.TicaretDialog.SetAcceptEvent(lambda arg=TRUE: self.OnExchangeDialog(name, 1, target_level, target_lonca, target_sinif))
			self.TicaretDialog.SetCancelEvent(lambda arg=FALSE: self.OnExchangeDialog(name, 0, target_level, target_lonca, target_sinif))
			self.TicaretDialog.Open()
			return

		if line.find("uzaktan_ticaret_kabul") != -1:
			if gameInfo.UZAKTAN_TICARET_DURUM == 2:
				gameInfo.UZAKTAN_TICARET_DURUM = 4
				uiExchange_Multi.TICARET_BASARILI = 1
			else:
				gameInfo.UZAKTAN_TICARET_DURUM = 3
			return

		if line.find("uzaktan_ticaret_iptal") != -1:
			uiExchange_Multi.TICARET_KAPAT = 1
			return

	#add
	def OnExchangeDialog(self, ad, flag, target_level, target_lonca, target_sinif):
		if flag == 0:
			self.TicaretDialog.Close()
			return
			
		if player.IsOpenPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO,"Pazar'dayken ticaret yapamazsın.")
			self.TicaretDialog.Close()
			return

		self.TicaretDialog.Close()
		gameInfo.UZAKTAN_TICARET_KISILER["kisi_"+str(ad)] = "#"+str(target_level)+"#"+str(target_lonca)+"#"+str(target_sinif)+"#"
		gameInfo.UZAKTAN_TICARET_RAKIP = ad
		race = net.GetMainActorRace()
		if not guild.IsGuildEnable():
			net.SendWhisperPacket(ad, "#uzaktan_ticaret_teklifi#cevap#"+str(player.GetStatus(player.LEVEL))+"#Lonca yok.#"+str(race)+"#")
		else:
			net.SendWhisperPacket(ad, "#uzaktan_ticaret_teklifi#cevap#"+str(player.GetStatus(player.LEVEL))+"#"+str(player.GetGuildName())+"#"+str(race)+"#")
			
		gameInfo.PYTHONISLEM = "uzaktan_ticaret_folder_remove#"+str(gameInfo.UZAKTAN_TICARET_RAKIP)+"#"
		event.QuestButtonClick(gameInfo.PYTHONTOLUA)
		self.ac = uiExchange_Multi.MultiExchangeDialog()
		self.ac.Open()
		self.interface.ToggleInventoryWindow_UzaktanTicaret()

	def OnUpdate(self):
		if gameInfo.UZAKTAN_TICARET_CANSEND == 1:
			if gameInfo.UZAKTAN_TICARET_ZAMAN < app.GetTime():
				gameInfo.UZAKTAN_TICARET_CANSEND = 0
				gameInfo.UZAKTAN_TICARET_ZAMAN = 0