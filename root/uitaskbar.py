import gameInfo
import chat

	def UnselectItemQuickSlot(self, localSlotIndex):
		if gameInfo.DUELLO_DURUM == 4:
			chat.AppendChat(chat.CHAT_TYPE_INFO,"D�ello paneli a��kken item kullanamazs�n.")
			if mouseModule.mouseController.isAttached():
				mouseModule.mouseController.DeattachObject()
			return