import os
import bs4
 
def _remove_h123_attrs(soup):
    tag_order = 0
    for tag in soup.find_all(['h1', 'h2', 'h3']):
        # 假如標註內容沒有字串
        #if len(tag.text) == 0:
        if len(tag.contents) ==0:
            # 且該標註為排序第一
            if tag_order == 0:
                tag.string = "First"
            else:
                # 若該標註非排序第一, 則移除無內容的標題標註
                tag.extract()
        # 針對單一元件的標題標註
        elif len(tag.contents) == 1:
            # 若內容非為純文字, 表示內容為其他標註物件
            if tag.get_text() == "":
                # 且該標註為排序第一
                if tag_order == 0:
                    # 在最前方插入標題
                    tag.insert_before(soup.new_tag('h1', 'First'))
                else:
                    # 移除 h1, h2 或 h3 標註, 只留下內容
                    tag.replaceWithChildren()
            # 表示單一元件的標題標註, 且標題為單一字串者
            else:
                # 判定若其排序第一, 則將 tag.name 為 h2 或 h3 者換為 h1
                if tag_order == 0:
                    tag.name = "h1"
            # 針對其餘單一字串內容的標註, 則保持原樣
        # 針對內容一個以上的標題標註
        #elif len(tag.contents) > 1:
        else:
            # 假如該標註內容長度大於 1
            # 且該標註為排序第一
            if tag_order == 0:
                # 先移除 h1, h2 或 h3 標註, 只留下內容
                #tag.replaceWithChildren()
                # 在最前方插入標題
                tag.insert_before(soup.new_tag('h1', 'First'))
            else:
                # 只保留標題內容,  去除 h1, h2 或 h3 標註
                # 為了與前面的內文區隔, 先在最前面插入 br 標註
                tag.insert_before(soup.new_tag('br'))
                # 再移除非排序第一的 h1, h2 或 h3 標註, 只留下內容
                tag.replaceWithChildren()
        tag_order = tag_order + 1
 
    return soup
 
def file_get_contents(filename):
    # open file in utf-8 and return file content
    with open(filename, encoding="utf-8") as file:
        return file.read()
 
def parse_content():
    """use bs4 and re module functions to parse content.htm"""
    config_dir = "./"
    # if no content.htm, generate a head 1 and content 1 file
    if not os.path.isfile(config_dir+"content.htm"):
        # create content.htm if there is no content.htm
        File = open(config_dir + "content.htm", "w", encoding="utf-8")
        File.write("<h1>head 1</h1>content 1")
        File.close()
    subject = file_get_contents(config_dir+"content.htm")
    # deal with content without content
    if subject == "":
        # create content.htm if there is no content.htm
        File = open(config_dir + "content.htm", "w", encoding="utf-8")
        File.write("<h1>head 1</h1>content 1")
        File.close()
        subject = "<h1>head 1</h1>content 1"
    # initialize the return lists
    head_list = []
    level_list = []
    page_list = []
    # make the soup out of the html content
    soup = bs4.BeautifulSoup(subject, 'html.parser')
    # 嘗試解讀各種情況下的標題
    soup = _remove_h123_attrs(soup)
    # 改寫 content.htm 後重新取 subject
    with open(config_dir + "content.htm", "wb") as f:
        f.write(soup.encode("utf-8"))
    subject = file_get_contents(config_dir+"content.htm")
    # get all h1, h2, h3 tags into list
    htag= soup.find_all(['h1', 'h2', 'h3'])
    n = len(htag)
    # get the page content to split subject using each h tag
    temp_data = subject.split(str(htag[0]))
    if len(temp_data) > 2:
        subject = str(htag[0]).join(temp_data[1:])
    else:
        subject = temp_data[1]
    if n >1:
            # i from 1 to i-1
            for i in range(1, len(htag)):
                head_list.append(htag[i-1].text.strip())
                # use name attribute of h* tag to get h1, h2 or h3
                # the number of h1, h2 or h3 is the level of page menu
                level_list.append(htag[i-1].name[1])
                temp_data = subject.split(str(htag[i]))
                if len(temp_data) > 2:
                    subject = str(htag[i]).join(temp_data[1:])
                else:
                    subject = temp_data[1]
                # cut the other page content out of htag from 1 to i-1
                cut = temp_data[0]
                # add the page content
                page_list.append(cut)
    # last i
    # add the last page title
    head_list.append(htag[n-1].text.strip())
    # add the last level
    level_list.append(htag[n-1].name[1])
    temp_data = subject.split(str(htag[n-1]))
    # the last subject
    subject = temp_data[0]
    # cut the last page content out
    cut = temp_data[0]
    # the last page content
    page_list.append(cut)
    return head_list, level_list, page_list
 
print(parse_content())