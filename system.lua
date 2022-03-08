--[[

TR: Tüm özel sistemler, fonksiyonlar, methodlar, ve yol...
TRL : All Special Systems, funcs, method and the way to...

Geliþtirici : .. Fatihbab34™ ..
Paketler ; LuaToPython, PythonToLua, PythonIslem
Fonksiyonlar ; "split('#blabla#blabla#', '#'), systems.getinput('PythonIslem'), io funcs(open, remove, write, read, readline, readlines), table forms, pc.getqf(), pc.setqf()"

--]]

quest systems begin
	state start begin

		function uzaktanticaret_itemsil(itemTab)
			local item_yer = systems.split(itemTab, "#")[3]
			--chat(item_yer)
			item.select_cell(tonumber(item_yer))
			item.remove()
		end
		
		function uzaktanticaret_itemver(itemTab)
			pc.give_item2_select(tonumber(systems.split(itemTab, "#")[1]),tonumber(systems.split(itemTab, "#")[2]))
			local attr,socket = {},{}
			for i = 10,23 do table.insert(attr,{systems.split(itemTab, "#")[i],systems.split(itemTab,"#")[i+1]}) i = i+1 end
			for i = 4,6 do table.insert(socket,systems.split(itemTab, "#")[i]) end
			for i = 1, table.getn(attr) do 
				item2.set_attr(i-1, attr[i][1], attr[i][2]) 
			end 
			for i = 1, table.getn(socket) do if tonumber(socket[i]) > 0 then item.set_socket(i-1, socket[i]) end end
		end

		function uzaktan_ticaret_gerceklestir(benim_ad, rakip_ad)

			--syschat("benim ad : "..benim_ad.. " |||| rakip ad : "..rakip_ad)

			local item_slot = io.open('/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/'..benim_ad..'ile'..rakip_ad..'_slot.cfg', "r")
			local item_para = io.open('/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/'..benim_ad..'ile'..rakip_ad..'_para.cfg', "r")
			if item_slot then -- 45'lik slot
				for item in item_slot:lines() do
					systems.uzaktanticaret_itemsil(item)
				end
			end

			if item_para then
				local para = item_para:read()
				pc.change_money(-tonumber(para))
			end

			--cmdchat("LuaToPython DUELLO_BITTI")

			local item_slot = io.open('/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/'..rakip_ad..'ile'..benim_ad..'_slot.cfg', "r")
			local item_para = io.open('/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/'..rakip_ad..'ile'..benim_ad..'_para.cfg', "r")

			if item_slot then -- 45'lik slot
				for item in item_slot:lines() do
					local items = systems.split(item,"#")
					if items[25] == pc.get_name() then
						systems.uzaktanticaret_itemver(item)
					else
						syschat("<Ticaret> : Ticaret'te bir sorun tespit edildi!")
					end
				end
				--os.remove("/usr/game/share/locale/turkey/quest/systems/itemineduello/"..name.."ile"..pc.get_name().."_slot.cfg")
			end

			if item_para then
				local para = item_para:read()
				pc.change_money(tonumber(para))
			end

			chat('Uzaktan Ticaret baþarýyla gerçekleþti.')

		end

		when login begin
			cmdchat("PythonToLua "..q.getcurrentquestindex())
		end
	
		when button begin
			local gelen = systems.getinput("PYTHONISLEM")

			if string.find(gelen, "uzaktan_ticaret_para_ekle") then
				local bol = systems.split(gelen, "#")
				local ac_kontrol = io.open('/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/'..pc.get_name()..'ile'..bol[3]..'_para.cfg', 'r')

				local benim_name=pc.get_name()
				local adam = find_pc_by_name(bol[3])
				pc.select(tonumber(adam))
				if tonumber(bol[2])+tonumber(pc.get_money()) > 1999999999 then
					local adam2 = find_pc_by_name(benim_name)
					pc.select(tonumber(adam2))
					syschat("<Uzaktan Ticaret> : Karþý rakipte bu parayla birlikte 2T olacaðý için bu kadar parayý ticarete koyamazsýn.")
					cmdchat("LuaToPython uzaktan_ticaret_parabenim_ekle")
					return
				end
				
				local para_kontrol = io.open("/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/"..bol[3]..'ile'..pc.get_name()..'_kabul.cfg', 'r')
				if para_kontrol then
					syschat("<Uzaktan Ticaret> : Þuan'da toplamý deðiþtirmezsiniz.Karþý oyuncu ticareti kabul etmiþ, bu iþlem karþýda gözükmeyecektir.")
					return
				end

				local para_kontrol2 = io.open("/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/"..pc.get_name()..'ile'..bol[3]..'_kabul.cfg', 'r')
				if para_kontrol2 then
					syschat("<Uzaktan Ticaret> : Ticareti kabul ettin,bu yüzden þuan'da item ekliyemezsiniz. Bu iþlem karþýda gözükmeyecektir.")
					return
				end

				if pc.get_money() < tonumber(bol[2]) then
					syschat('<Uzaktan Ticaret> : Yeterli Paran Yok.')
					return
				end

				if ac_kontrol then
					syschat("<Uzaktan Ticaret> : Þuan'da toplamý deðiþtirmezsiniz.Bu iþlem karþý oyuncuda gözükmeyecektir.")
					return
				end

				local ac = io.open('/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/'..pc.get_name()..'ile'..bol[3]..'_para.cfg', 'w')
				ac:write(tostring(bol[2]))
				ac:close()

				local adam = find_pc_by_name(bol[3])
				pc.select(tonumber(adam))
				cmdchat("LuaToPython uzaktan_ticaret_para_ekle#"..bol[2])
			end

			if string.find(gelen, "uzaktan_ticaret_kabul_ediyorum") then
				local bol = systems.split(gelen, "#")
				--local ac = io.open("/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/"..pc.get_name()..'ile'..bol[2]..'_kabul.cfg', 'r')
				--if not ac then
				local ac_yaz = io.open("/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/"..pc.get_name()..'ile'..bol[2]..'_kabul.cfg', 'w')
				ac_yaz:write("1")
				ac_yaz:close()
				--end
			end

			if string.find(gelen, "uzaktan_ticaret_folder_remove") then
				--chat("sil...")
				local bol = systems.split(gelen, "#")
				local ac = io.open("/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/"..pc.get_name()..'ile'..bol[2]..'_slot.cfg', 'r')
				local ac_para = io.open("/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/"..pc.get_name()..'ile'..bol[2]..'_para.cfg', 'r')
				local ac_kabul = io.open("/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/"..pc.get_name()..'ile'..bol[2]..'_kabul.cfg', 'r')
				if ac then
					os.remove("/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/"..pc.get_name()..'ile'..bol[2]..'_slot.cfg')
				end
				if ac_para then
					os.remove("/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/"..pc.get_name()..'ile'..bol[2]..'_para.cfg')
				end
				if ac_kabul then
					os.remove("/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/"..pc.get_name()..'ile'..bol[2]..'_kabul.cfg')
				end

				local ac_x = io.open("/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/"..bol[2]..'ile'..pc.get_name()..'_slot.cfg', 'r')
				local ac_para_x = io.open("/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/"..bol[2]..'ile'..pc.get_name()..'_para.cfg', 'r')
				local ac_kabul_x = io.open("/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/"..bol[2]..'ile'..pc.get_name()..'_kabul.cfg', 'r')
				if ac_x then
					os.remove("/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/"..bol[2]..'ile'..pc.get_name()..'_slot.cfg')
				end
				if ac_para_x then
					os.remove("/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/"..bol[2]..'ile'..pc.get_name()..'_para.cfg')
				end
				if ac_kabul_x then
					os.remove("/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/"..bol[2]..'ile'..pc.get_name()..'_kabul.cfg')
				end

				local ac_rakip_ad = io.open("/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/"..pc.get_name()..'_rakip_ad.cfg', 'w')
				ac_rakip_ad:write(bol[2])
				ac_rakip_ad:close()

				local ac_rakip_ad2 = io.open("/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/"..bol[2]..'_rakip_ad.cfg', 'w')
				ac_rakip_ad2:write(pc.get_name())
				ac_rakip_ad2:close()

			end

			if string.find(gelen, "uzaktan_ticaret_gerceklestir") then
				--syschat("1 ticaret gerçekleþiyor...")
				local bol2 = systems.split(gelen, "#")
				local adam = find_pc_by_name(bol2[2])
				local kontrol_benim = 0
				local kontrol_benim_para = 0
				local kontrol_rakip = 0
				local kontrol_rakip_para = 0

				local dosya1 = 0
				local dosya2 = 0
				local dosya1_r = 0
				local dosya2_r = 0

				local iptal = 0

				--chat("ticaret gerçekleþiyor...")

				local ac_rakip_ad = io.open("/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/"..pc.get_name()..'_rakip_ad.cfg', 'r')
				if ac_rakip_ad:read() != bol2[2] then
					syschat("Uzaktan ticaret gerçekleþirken bir usülsüzlik oluþtu.")
					pc.select(tonumber(adam))
					syschat("Uzaktan ticaret gerçekleþirken bir usülsüzlik oluþtu.")
					return
				end

				local para_kontrol = io.open("/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/"..bol2[2]..'ile'..pc.get_name()..'_kabul.cfg', 'r')
				if para_kontrol then
					print "birþey yapma..."
				else
					syschat("Uzaktan ticaret gerçekleþirken bir usülsüzlik oluþtu.")
					pc.select(tonumber(adam))
					syschat("Uzaktan ticaret gerçekleþirken bir usülsüzlik oluþtu.")
					return
				end

				local item_slot = io.open('/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/'..pc.get_name()..'ile'..bol2[2]..'_slot.cfg', "r")
				local item_para = io.open('/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/'..pc.get_name()..'ile'..bol2[2]..'_para.cfg', "r")

				if item_slot then -- 45'lik slot
					
					for itemx in item_slot:lines() do
						kontrol_benim = 1
						local bol = systems.split(itemx,"#")
						local items_sec = systems.split(itemx,"#")[3]

						if bol2[2] != bol[25] then
							syschat("Uzaktan ticaret gerçekleþirken bir usülsüzlük oluþtu.")
							pc.select(tonumber(adam))
							syschat("Uzaktan ticaret gerçekleþirken bir usülsüzlik oluþtu.")
							return
						end

						--item.select_cell(0)
						item.select_cell(tonumber(items_sec))

						if tonumber(item.get_cell()) != tonumber(items_sec) then
							syschat("Uzaktan ticaret gerçekleþirken bir usülsüzlik oluþtu.")
							local adam = find_pc_by_name(bol2[2])
							pc.select(tonumber(adam))
							syschat("Uzaktan ticaret gerçekleþirken bir usülsüzlik oluþtu.")
							return
						end

						local attr = {{item2.get_attr(0)}, {item2.get_attr(1)}, {item2.get_attr(2)}, {item2.get_attr(3)},{item2.get_attr(4)},{item2.get_attr(5)}, {item2.get_attr(6)}}
						local socket, itemVnum, itemCount = {item.get_socket(0), item.get_socket(1), item.get_socket(2),item.get_socket(3),item.get_socket(4),item.get_socket(5)}, item.get_vnum(), item.get_count()
						
						if tonumber(bol[1]) == tonumber(itemVnum) and tonumber(bol[2]) == tonumber(itemCount) and tonumber(bol[4]) == tonumber(socket[1]) and tonumber(bol[5]) == tonumber(socket[2]) and tonumber(bol[6]) == tonumber(socket[3]) and tonumber(bol[7]) == tonumber(socket[4]) and tonumber(bol[8]) == tonumber(socket[5]) and tonumber(bol[9]) == tonumber(socket[6]) and tonumber(bol[10]) == tonumber(attr[1][1]) and tonumber(bol[11]) == tonumber(attr[1][2]) and tonumber(bol[12]) == tonumber(attr[2][1]) and tonumber(bol[13]) == tonumber(attr[2][2]) and tonumber(bol[14]) == tonumber(attr[3][1]) and tonumber(bol[15]) == tonumber(attr[3][2]) and tonumber(bol[16]) == tonumber(attr[4][1]) and tonumber(bol[17]) == tonumber(attr[4][2]) and tonumber(bol[18]) == tonumber(attr[5][1]) and tonumber(bol[19]) == tonumber(attr[5][2]) and tonumber(bol[20]) == tonumber(attr[6][1]) and tonumber(bol[21]) == tonumber(attr[6][2]) and tonumber(bol[22]) == tonumber(attr[7][1]) and tonumber(bol[23]) == tonumber(attr[7][2]) and tonumber(bol[27]) == tonumber(item.get_id()) then
							kontrol_benim = 0
							--print "birþey yapma..."
							--chat("item eþit.")
						else
							--chat("item eþit deðil.")
							kontrol_benim = 1
							syschat("Uzaktan ticaret gerçekleþirken bir usülsüzlik oluþtu.")
							local adam = find_pc_by_name(bol2[2])
							pc.select(tonumber(adam))
							syschat("Uzaktan ticaret gerçekleþirken bir usülsüzlik oluþtu.")
							return
						end
						--systems.uzaktanticaret_itemsil(item)
					end
				else
					dosya1 = 1
					
				end

				if item_para then
					local para = item_para:read()
					if pc.get_money() >= tonumber(para) then
						--chat("para tamam")
						print "birþey yapma..."
						--pc.change_money(-tonumber(para))
					else
						--chat("para tamam deðil")
						kontrol_benim_para = 1
						syschat("Uzaktan ticaret gerçekleþirken bir usülsüzlik oluþtu.")
						local adam = find_pc_by_name(bol2[2])
						pc.select(tonumber(adam))
						syschat("Uzaktan ticaret gerçekleþirken bir usülsüzlik oluþtu.")
						return
					end
				else
					dosya2 = 1
				end

				if kontrol_benim == 0 and kontrol_benim_para == 0 then

					pc.select(tonumber(adam))

					local ac_rakip_ad = io.open("/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/"..pc.get_name()..'_rakip_ad.cfg', 'r')
					if ac_rakip_ad:read() != bol2[3] then
						syschat("Uzaktan ticaret gerçekleþirken bir usülsüzlik oluþtu.")
						local adam = find_pc_by_name(bol2[3])
						pc.select(tonumber(adam))
						syschat("Uzaktan ticaret gerçekleþirken bir usülsüzlik oluþtu.")
						return
					end

					--syschat(pc.get_name()..'ile'..bol2[3]..'.cfg')
					local item_slot = io.open('/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/'..pc.get_name()..'ile'..bol2[3]..'_slot.cfg', "r")
					local item_para = io.open('/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/'..pc.get_name()..'ile'..bol2[3]..'_para.cfg', "r")

					if item_slot then -- 45'lik slot
						
						for itemx in item_slot:lines() do
							kontrol_rakip = 1
							local bol = systems.split(itemx,"#")
							local items_sec = systems.split(itemx,"#")[3]

							if bol2[3] != bol[25] then
								syschat("Uzaktan ticaret gerçekleþirken bir usülsüzlük oluþtu.")
								local adam = find_pc_by_name(bol2[3])
								pc.select(tonumber(adam))
								syschat("Uzaktan ticaret gerçekleþirken bir usülsüzlik oluþtu.")
								return
							end

							--item.select_cell(0)
							item.select_cell(tonumber(items_sec))

							if tonumber(item.get_cell()) != tonumber(items_sec) then
								syschat("Uzaktan ticaret gerçekleþirken bir usülsüzlik oluþtu.")
								local adam = find_pc_by_name(bol2[3])
								pc.select(tonumber(adam))
								syschat("Uzaktan ticaret gerçekleþirken bir usülsüzlik oluþtu.")
								return
							end

							local attr = {{item2.get_attr(0)}, {item2.get_attr(1)}, {item2.get_attr(2)}, {item2.get_attr(3)},{item2.get_attr(4)},{item2.get_attr(5)}, {item2.get_attr(6)}}
							local socket, itemVnum, itemCount = {item.get_socket(0), item.get_socket(1), item.get_socket(2),item.get_socket(3),item.get_socket(4),item.get_socket(5)}, item.get_vnum(), item.get_count()
							
							if tonumber(bol[1]) == tonumber(itemVnum) and tonumber(bol[2]) == tonumber(itemCount) and tonumber(bol[4]) == tonumber(socket[1]) and tonumber(bol[5]) == tonumber(socket[2]) and tonumber(bol[6]) == tonumber(socket[3]) and tonumber(bol[7]) == tonumber(socket[4]) and tonumber(bol[8]) == tonumber(socket[5]) and tonumber(bol[9]) == tonumber(socket[6]) and tonumber(bol[10]) == tonumber(attr[1][1]) and tonumber(bol[11]) == tonumber(attr[1][2]) and tonumber(bol[12]) == tonumber(attr[2][1]) and tonumber(bol[13]) == tonumber(attr[2][2]) and tonumber(bol[14]) == tonumber(attr[3][1]) and tonumber(bol[15]) == tonumber(attr[3][2]) and tonumber(bol[16]) == tonumber(attr[4][1]) and tonumber(bol[17]) == tonumber(attr[4][2]) and tonumber(bol[18]) == tonumber(attr[5][1]) and tonumber(bol[19]) == tonumber(attr[5][2]) and tonumber(bol[20]) == tonumber(attr[6][1]) and tonumber(bol[21]) == tonumber(attr[6][2]) and tonumber(bol[22]) == tonumber(attr[7][1]) and tonumber(bol[23]) == tonumber(attr[7][2]) and tonumber(bol[27]) == tonumber(item.get_id()) then
								kontrol_rakip = 0
								--print "birþey yapma..."
								--chat("item eþit.")
							else
								kontrol_rakip = 1
								syschat("Uzaktan ticaret gerçekleþirken bir usülsüzlük oluþtu.")
								local adam = find_pc_by_name(bol2[3])
								pc.select(tonumber(adam))
								syschat("Uzaktan ticaret gerçekleþirken bir usülsüzlik oluþtu.")
								return
							end
							--systems.uzaktanticaret_itemsil(item)
						end
					else
						dosya1_r = 1
					end

					if item_para then
						local para = item_para:read()
						if pc.get_money() >= tonumber(para) then
							--chat("para tamam.")
							print "birþey yapma..."
							--pc.change_money(tonumber(para))
						else
							kontrol_rakip_para = 1		
							syschat("Uzaktan ticaret gerçekleþirken bir usulsüzlük oluþtu.")
							local adam = find_pc_by_name(bol2[3])
							pc.select(tonumber(adam))
							syschat("Uzaktan ticaret gerçekleþirken bir usulsüzlük oluþtu.")
							return
						end
					else
						dosya2_r = 1
					end

					if dosya1 == 1 and dosya2 == 1 and dosya1_r == 1 and dosya2_r == 1 then
						syschat("Ticaret'e hiç birþey koyulmadýðý için ticaret iptal oldu.")
						local adam = find_pc_by_name(bol2[3])
						pc.select(tonumber(adam))
						syschat("Ticaret'e hiç birþey koyulmadýðý için ticaret iptal oldu.")
						return
					end

					if kontrol_benim == 0 and kontrol_benim_para == 0 and kontrol_rakip == 0 and kontrol_rakip_para == 0 then
						systems.uzaktan_ticaret_gerceklestir(pc.get_name(), bol2[3])
						local adam = find_pc_by_name(bol2[3])
						pc.select(tonumber(adam))
						systems.uzaktan_ticaret_gerceklestir(pc.get_name(), bol2[2])
					else
						syschat("<Uzaktan Ticaret> : Ticaret gerçekleþirken bir usulsüzlük oluþtu.")
						local adam = find_pc_by_name(bol2[3])
						pc.select(tonumber(adam))
						syschat("<Uzaktan Ticaret> : Ticaret gerçekleþirken bir usulsüzlük oluþtu.")
					end
					

				else
					syschat("<Uzaktan Ticaret> : Ticaret gerçekleþirken bir usulsüzlük oluþtu.")
					local adam = find_pc_by_name(bol2[2])
					pc.select(tonumber(adam))
					syschat("<Uzaktan Ticaret> : Ticaret gerçekleþirken bir usulsüzlük oluþtu.")
				end
			end

			if string.find(gelen, "uzaktan_ticaret_ekle") then
				local bol = systems.split(gelen, "#")
				--local pos_at = bol[2]
				local pos_sec = bol[4]
				local fxd = 0
				--local ac_fx = io.open('/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/'..pc.get_name()..'ile'..bol[3]..'_kontroltekrar.cfg', 'w')
				--ac_fx:write("byfatihbab34")
				--ac_fx:close()
				--local pos_rakip = bol[3]
				item.select_cell(bol[2])

				if tonumber(item.get_id()) == 0 then
					syschat('Ýtem ticarete konulmadý.Bu iþlem karþýda gözükmeyecektir.')
					return
				end
				
				if tonumber(item.get_vnum()) == 70011 or tonumber(item.get_vnum()) == 70042 or tonumber(item.get_vnum()) == 40001 or tonumber(item.get_vnum()) == 40004 or tonumber(item.get_vnum()) == 25041 or tonumber(item.get_vnum()) == 50125 or tonumber(item.get_vnum()) == 71135 then
					syschat("Bu nesne konulamaz.Bu iþlem karþýda gözükmeyecektir.")
					return
				end

				local para_kontrol = io.open("/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/"..bol[3]..'ile'..pc.get_name()..'_kabul.cfg', 'r')
				if para_kontrol then
					syschat("<Uzaktan Ticaret> : Þuan'da item ekliyemezsiniz.Karþý oyuncu ticareti kabul etmiþ, bu iþlem karþýda gözükmeyecektir.")
					return
				end

				local para_kontrol2 = io.open("/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/"..pc.get_name()..'ile'..bol[3]..'_kabul.cfg', 'r')
				if para_kontrol2 then
					syschat("<Uzaktan Ticaret> : Ticareti kabul ettin,bu yüzden þuan'da item ekliyemezsiniz. Bu iþlem karþýda gözükmeyecektir.")
					return
				end

				local attr = {{item2.get_attr(0)}, {item2.get_attr(1)}, {item2.get_attr(2)}, {item2.get_attr(3)},{item2.get_attr(4)},{item2.get_attr(5)}, {item2.get_attr(6)}}
				local socket, itemVnum, itemCount = {item.get_socket(0), item.get_socket(1), item.get_socket(2),item.get_socket(3),item.get_socket(4),item.get_socket(5)}, item.get_vnum(), item.get_count()
				--chat(bol[2])
				--chat(bol[4])
				local ac_kontrol = io.open('/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/'..pc.get_name()..'ile'..bol[3]..'_slot.cfg', 'r')
				if ac_kontrol then
					for fx in ac_kontrol:lines() do
						
						local bol = systems.split(fx,"#")
						if tonumber(bol[27]) == tonumber(item.get_id()) then
							chat("<Uzaktan Ticaret> : Ayný id'li itemi tekrar koyamazsýn.")
							fxd = 1
						end
						
					end
					ac_kontrol:close()
					if fxd == 0 then
						local ac = io.open('/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/'..pc.get_name()..'ile'..bol[3]..'_slot.cfg', 'a+')
						ac:write(itemVnum.."#"..itemCount.."#"..(bol[2]).."#"..socket[1].."#"..socket[2].."#"..socket[3].."#"..socket[4].."#"..socket[5].."#"..socket[6].."#"..attr[1][1].."#"..attr[1][2].."#"..attr[2][1].."#"..attr[2][2].."#"..attr[3][1].."#"..attr[3][2].."#"..attr[4][1].."#"..attr[4][2].."#"..attr[5][1].."#"..attr[5][2].."#"..attr[6][1].."#"..attr[6][2].."#"..attr[7][1].."#"..attr[7][2].."#"..pc.get_name().."#"..(bol[3]).."#"..(bol[4]).."#"..item.get_id().."#".."\\n")
						ac:close()
						local adam = find_pc_by_name(bol[3])
						pc.select(tonumber(adam))
						cmdchat("LuaToPython uzaktan_ticaret_item_ekle|#"..itemVnum.."#"..itemCount.."#"..(bol[2]).."#"..socket[1].."#"..socket[2].."#"..socket[3].."#"..socket[4].."#"..socket[5].."#"..socket[6].."#"..attr[1][1].."#"..attr[1][2].."#"..attr[2][1].."#"..attr[2][2].."#"..attr[3][1].."#"..attr[3][2].."#"..attr[4][1].."#"..attr[4][2].."#"..attr[5][1].."#"..attr[5][2].."#"..attr[6][1].."#"..attr[6][2].."#"..attr[7][1].."#"..attr[7][2].."#"..pc.get_name().."#"..(bol[3]).."#"..(bol[4]).."#"..item.get_id().."#")
					end

				else
					local ac = io.open('/usr/game/share/locale/turkey/quest/systems/uzaktan_ticaret/'..pc.get_name()..'ile'..bol[3]..'_slot.cfg', 'w')
					ac:write(itemVnum.."#"..itemCount.."#"..(bol[2]).."#"..socket[1].."#"..socket[2].."#"..socket[3].."#"..socket[4].."#"..socket[5].."#"..socket[6].."#"..attr[1][1].."#"..attr[1][2].."#"..attr[2][1].."#"..attr[2][2].."#"..attr[3][1].."#"..attr[3][2].."#"..attr[4][1].."#"..attr[4][2].."#"..attr[5][1].."#"..attr[5][2].."#"..attr[6][1].."#"..attr[6][2].."#"..attr[7][1].."#"..attr[7][2].."#"..pc.get_name().."#"..(bol[3]).."#"..(bol[4]).."#"..item.get_id().."#".."\\n")
					ac:close()

					local adam = find_pc_by_name(bol[3])
					pc.select(tonumber(adam))
					cmdchat("LuaToPython uzaktan_ticaret_item_ekle|#"..itemVnum.."#"..itemCount.."#"..(bol[2]).."#"..socket[1].."#"..socket[2].."#"..socket[3].."#"..socket[4].."#"..socket[5].."#"..socket[6].."#"..attr[1][1].."#"..attr[1][2].."#"..attr[2][1].."#"..attr[2][2].."#"..attr[3][1].."#"..attr[3][2].."#"..attr[4][1].."#"..attr[4][2].."#"..attr[5][1].."#"..attr[5][2].."#"..attr[6][1].."#"..attr[6][2].."#"..attr[7][1].."#"..attr[7][2].."#"..pc.get_name().."#"..(bol[3]).."#"..(bol[4]).."#"..item.get_id().."#")
				end
				
			end

		end


		function getinput(gelen)
			local input1 = "#quest_input#"
			local input0 = "#quest_inputbitir#"
			cmdchat("LuaToPython "..input1)
			local al = input(cmdchat("PythonIslem "..gelen))
			cmdchat("LuaToPython "..input0)
			return al
		end

		function split(command_, ne)
			return systems.split_(command_,ne)
		end
			
		function split_(string_,delimiter)
			local result = { }
			local from  = 1
			local delim_from, delim_to = string.find( string_, delimiter, from  )
			while delim_from do
				table.insert( result, string.sub( string_, from , delim_from-1 ) )
				from  = delim_to + 1
				delim_from, delim_to = string.find( string_, delimiter, from  )
			end
			table.insert( result, string.sub( string_, from  ) )
			return result
		end
	end
end