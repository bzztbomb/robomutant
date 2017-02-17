-- license:BSD-3-Clause
-- copyright-holders:bzztbomb
local exports = {}
exports.name = "mikey"
exports.version = "0.0.1"
exports.description = "Allows external programs play mame (targeting robotron)"
exports.license = "The BSD 3-Clause License"
exports.author = { name = "bzztbomb" }

require "lfs";

local mikey = exports
-- Do we wait for input before allowing play to continue?
local block_until_processed = false
local base_dir = "./snap/robotron/"
local input_file = base_dir .. "moves.csv"

function mikey.startplugin()
	emu.register_frame(function()

		if (lfs.attributes(base_dir .. "current_frame.png") == nil) then
			manager:machine():video():snapshot()
      os.rename(base_dir .. "0000.png", base_dir .. "current_frame.png")
		end

		if (block_until_processed) then
			while (lfs.attributes(input_file) == nil) do
			end
		end

		if (lfs.attributes(input_file) ~= nil) then
			for line in io.lines(input_file) do
				local x = 0
				local move = {}
				-- csv of port, field name, value
				for i in string.gmatch(line, "[^,]+") do
					move[x] = i
					x = x+1
				end
				manager:machine():ioport().ports[move[0]].fields[move[1]]:set_value(tonumber(move[2]))
			end
			os.remove(input_file)
		end
	end)
end

return exports

-- :IN0
-- Move Left	userdata: 0x7f8ed904a7c8
-- Fire Down	userdata: 0x7f8ed904aac8
-- 1 Player Start	userdata: 0x7f8ed904a908
-- Fire Up	userdata: 0x7f8ed904aa98
-- Move Up	userdata: 0x7f8ed904a048
-- 2 Players Start	userdata: 0x7f8ed904a788
-- Move Right	userdata: 0x7f8ed904a8a8
-- Move Down	userdata: 0x7f8ed904a728

-- :IN1
-- Fire Left	userdata: 0x7f8ed1ef2238
-- Fire Right	userdata: 0x7f8ed1eea4f8
