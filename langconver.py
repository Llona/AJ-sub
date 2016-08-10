import opencc

def s2tw(ori_str):
    ori_str_lv = ori_str
    conv_h = opencc.OpenCC('s2tw')  # convert from Simplified Chinese to Traditional Chinese
    conv_str_lv = conv_h.convert(ori_str_lv)
    return conv_str_lv


def tw2s(ori_str):
    ori_str_lv = ori_str
    conv_h = opencc.OpenCC('tw2s')  # convert from  Traditional Chinese to Simplified Chinese
    conv_str_lv = conv_h.convert(ori_str_lv)
    return conv_str_lv
