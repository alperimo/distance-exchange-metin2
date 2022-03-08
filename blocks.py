"Genel IMPORT"
import gameInfo
import localegame
import uiExchange_Multi

#uiInventory.py


	""" Fonksiyonlarýn içine eklenecekler!!! """
	
	def OnDetachMetinFromItem(self):
		if gameInfo.UZAKTAN_TICARET_DURUM != 0:
			self.OnCloseQuestionDialog()
			return
	
	def __DropSrcItemToDestItemInInventory(self, srcItemVID, srcItemSlotPos, dstItemSlotPos):
		if srcItemSlotPos in uiExchange_Multi.ITEMSLOT:
			#chat.AppendChat(chat.CHAT_TYPE_INFO, localegame.DUELLO_ITEMI_HAREKET_ETTIREMESSIN)
			return

	def __SendUseItemToItemPacket(self, srcSlotPos, dstSlotPos):
		if srcSlotPos in uiExchange_Multi.ITEMSLOT:
			#chat.AppendChat(chat.CHAT_TYPE_INFO, localegame.DUELLO_ITEMI_KULLANAMASSIN)
			return

	def __SendUseItemPacket(self, slotPos):
		if slotPos in uiExchange_Multi.ITEMSLOT:
			#chat.AppendChat(chat.CHAT_TYPE_INFO, localegame.DUELLO_ITEMI_KULLANAMASSIN)
			return

	def __SendMoveItemPacket(self, srcSlotPos, dstSlotPos, srcItemCount):
		if srcSlotPos in uiExchange_Multi.ITEMSLOT:
			#chat.AppendChat(chat.CHAT_TYPE_INFO, localegame.DUELLO_ITEMI_HAREKET_ETTIREMESSIN)
			return

	def OpenPickMoneyDialog(self):
		if gameInfo.UZAKTAN_TICARET_DURUM != 0:
			return

	def __SellItem(self, itemSlotPos):
	#def SellItem(self):

		if self.sellingSlotNumber in uiExchange_Multi.ITEMSLOT:
			#chat.AppendChat(chat.CHAT_TYPE_INFO, localegame.DUELLO_ITEMI_HAREKET_ETTIREMESSIN)
			return

	def SelectItemSlot(self, itemSlotIndex):
			if gameInfo.UZAKTAN_TICARET_DURUM != 0:
				mouseModule.mouseController.DeattachObject()
				return
				
			if player.GetItemIndex(attachedSlotPos) == 71084 or player.GetItemIndex(attachedSlotPos) == 71085:
				if gameInfo.UZAKTAN_TICARET_DURUM != 0:
					mouseModule.mouseController.DeattachObject()
					return
					
#uiRefine.py
import gameInfo

class RefineDialog(ui.ScriptWindow):

	#deðiþtir#
	def Accept(self):
		if gameInfo.UZAKTAN_TICARET_DURUM != 0:
			self.Close()
			return
		net.SendItemUseToItemPacket(self.scrollItemPos, self.targetItemPos)
		self.Close()
		
class RefineDialogNew(ui.ScriptWindow):
	
	#deðiþtir#
	def Accept(self):
		if gameInfo.UZAKTAN_TICARET_DURUM != 0:
			self.CancelRefine()
			return
		net.SendRefinePacket(self.targetItemPos, self.type)
		self.Close()
		
#uiAttachMetin.py
import gameInfo

class AttachMetinDialog(ui.ScriptWindow):

	def Accept(self):
		if gameInfo.UZAKTAN_TICARET_DURUM != 0:
			self.Close()
			return
			
		net.SendItemUseToItemPacket(self.metinItemPos, self.targetItemPos)
		snd.PlaySound("sound/ui/metinstone_insert.wav")
		self.Close()
		
#uiShop.py
import gameInfo

class ShopDialog...

	def UnselectItemSlot(self, selectedSlotPos):
		if shop.IsPrivateShop():
			self.AskBuyItem(selectedSlotPos)
		else:
			if gameInfo.UZAKTAN_TICARET_DURUM != 0:
				return
			net.SendShopBuyPacket(selectedSlotPos)
			
	def OnUpdate(self):
		if gameInfo.UZAKTAN_TICARET_DURUM != 0:
			self.Close()

	def AnswerBuyItem(self, flag):
		if gameInfo.UZAKTAN_TICARET_DURUM != 0:
			self.itemBuyQuestionDialog.Close()
			self.itemBuyQuestionDialog = None
			return


#uiExchange.py
DUELLO_YAPAMASSIN = 0

	def OpenDialog(self):
		global DUELLO_YAPAMASSIN
		DUELLO_YAPAMASSIN = 0

	def SelectOwnerEmptySlot(self, SlotIndex):
		if srcSlotNumber in uiExchange_Multi.ITEMSLOT:
		#if SlotIndex in uiExchange_Multi.ITEMSLOT:
			return

	def OnUpdate(self):
		global DUELLO_YAPAMASSIN
		if gameInfo.UZAKTAN_TICARET_DURUM != 0:
			if DUELLO_YAPAMASSIN == 0:
				chat.AppendChat(chat.CHAT_TYPE_INFO, '<Sistem> : Zaten ticaret yapiyorsun.')
				net.SendExchangeExitPacket()	
				DUELLO_YAPAMASSIN = 1

#uiPrivateShopBuilder.py
class PrivateShopBuild(ui.ScriptWindow):
	def Open(self, title):
		if gameInfo.UZAKTAN_TICARET_DURUM != 0:
			self.Hide()
			return
			
	def OnOk(self):
		if gameInfo.UZAKTAN_TICARET_DURUM != 0:
			self.Close()
			return

#uiSafebox.py
class SafeboxWindow(ui.ScriptWindow):
	def SelectEmptySlot(self, selectedSlotPos):

		if attachedSlotPos in uiExchange_Multi.ITEMSLOT:
			return

	def OnUpdate(self):
		if gameInfo.UZAKTAN_TICARET_DURUM != 0:
			self.Close()

class MallWindow(ui.ScriptWindow):

	def OnUpdate(self):
		if gameInfo.UZAKTAN_TICARET_DURUM != 0:
			self.Close()

#InterfaceModule.py
class InterfaceModule(ui.ScriptWindow):	
	def OpenShopDialog(self, vid):
		if gameInfo.UZAKTAN_TICARET_DURUM != 0:
			self.CloseShopDialog()
			return
		self.wndInventory.Show()
		self.wndInventory.SetTop()
		self.dlgShop.Open(vid)
		self.dlgShop.SetTop()

	##ekle boþ yere
	def ToggleInventoryWindow_UzaktanTicaret(self):
		if FALSE == player.IsObserverMode():
			if FALSE == self.wndInventory.IsShow():
				self.wndInventory.Show()
				self.wndInventory.SetTop()

#game.Py

	def RequestDropItem(self, answer):
		#if attachedItemSlotPos in uiExchange_Multi.ITEMSLOT or attachedItemIndex in uiExchange_Multi.ITEMSLOT:
		#	chat.AppendChat(chat.CHAT_TYPE_INFO, localegame.DUELLO_ITEMI_HAREKET_ETTIREMESSIN)
		#	return

		if gameInfo.UZAKTAN_TICARET_DURUM != 0:
			self.itemDropQuestionDialog.Close()
			self.itemDropQuestionDialog = None
			return