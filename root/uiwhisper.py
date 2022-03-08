import gameInfo
import os
import uiCommon
import guild
import localegame

self.uzaktanticaret = GetObject("uzaktanticaretbutton")
			self.uzaktanticaret_yapabilirsin = 0



	self.uzaktanticaret.SetEvent(ui.__mem_func__(self.UzaktanTicaret))


	def OpenWithTarget(self, targetName):
		self.uzaktanticaret.Show()
		self.uzaktanticaret_yapabilirsin = 1

		if gameInfo.UZAKTAN_TICARET_CANSEND == 1:
			self.uzaktanticaret.Hide()

	def OpenWithoutTarget(self, event):
		self.uzaktanticaret.Hide()
		self.uzaktanticaret_yapabilirsin = 0

	## add

	def UzaktanTicaret(self):
		if player.IsOpenPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO,"Pazar'dayken ticaret yapamazsın.")
			return
			
		race = net.GetMainActorRace()
		if not guild.IsGuildEnable():
			net.SendWhisperPacket(self.targetName, "#uzaktan_ticaret_teklifi#"+str(player.GetStatus(player.LEVEL))+"#Lonca yok.#"+str(race))
		else:
			net.SendWhisperPacket(self.targetName, "#uzaktan_ticaret_teklifi#"+str(player.GetStatus(player.LEVEL))+"#"+str(player.GetGuildName())+"#"+str(race))	
		self.uzaktanticaret.Hide()
		gameInfo.UZAKTAN_TICARET_ZAMAN = app.GetTime() + 30
		gameInfo.UZAKTAN_TICARET_CANSEND = 1

	def OnUpdate(self):
		if gameInfo.UZAKTAN_TICARET_CANSEND == 0 and self.uzaktanticaret_yapabilirsin == 1:
			self.uzaktanticaret.Show()
		else:
			self.uzaktanticaret.Hide()