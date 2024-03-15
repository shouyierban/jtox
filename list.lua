function main(splash, args)
    splash:go("https://www.foodieguide.com/iptvsearch/")
    assert(splash:wait(6))
    local f_page = splash:select("body > div:nth-child(2) > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > span:nth-child(2) > a"):info()["attributes"]["href"]
    --return f_page
  	local full_url = "https://www.foodieguide.com/iptvsearch/"..f_page
    splash:go(full_url)
    assert(splash:wait(2))
    --return splash:png()
    local charge_port = splash:select('body > div:nth-child(3) > div.tables > div > div:nth-child(3) > div'):text()
    --return charge_port
    if charge_port and string.find(charge_port, '失效') then
        return "IP无效，稍后再试"
    else
        local port_url = splash:select('body > div:nth-child(3) > div.tables > div > div.channel > a'):info()["attributes"]["href"]
        --return port_url
        local full_port_url = "https://www.foodieguide.com/iptvsearch/"..port_url
        splash:go(full_port_url)
        assert(splash:wait(15))
        --return splash:png()

        local iptv_list = {}
        while true do
            for i = 2, 21 do
                local iptv_name_element = splash:select('#content > div:nth-child(' .. i .. ') > div.channel > a > div:nth-child(1)')
                local iptv_addr_element = splash:select('#content > div:nth-child(' .. i .. ') > div.m3u8 > table > tbody > tr > td:nth-child(2)')

                if iptv_name_element and iptv_addr_element then
                    local iptv_name = iptv_name_element:text()
                    local iptv_addr = iptv_addr_element:text()

                    if iptv_name and iptv_addr then
                        local data_info = {
                            name = iptv_name,
                            addr = iptv_addr
                        }
                        table.insert(iptv_list, data_info)
                    else
                        print("数据不完整，跳过...")
                        repeat
                            break
                        until true
                    end
                else
                    print("无法找到元素，跳过...")
                    repeat
                        break
                    until true
                end
            end

            local next_bt = splash:select('#Pagination > a.next')
            if next_bt then
                next_bt: mouse_click()
            else
                break
            end
        end

        return {
            result = iptv_list
        }
    end
end

