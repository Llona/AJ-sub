import opencc


def convert_lang_select(ori_str, lang_select):
    ori_str_lv = ori_str
    conv_h = opencc.OpenCC(lang_select)  # convert
    conv_str_lv = conv_h.convert(ori_str_lv)
    return conv_str_lv


def s2tw(ori_str):
    ori_str_lv = ori_str
    conv_h = opencc.OpenCC('s2tw')  # convert from Simplified Chinese to Traditional Chinese + Taiwan phrase
    conv_str_lv = conv_h.convert(ori_str_lv)
    return conv_str_lv


def s2t(ori_str):
    ori_str_lv = ori_str
    conv_h = opencc.OpenCC('s2t')  # convert from Simplified Chinese to Traditional Chinese
    conv_str_lv = conv_h.convert(ori_str_lv)
    return conv_str_lv


def t2s(ori_str):
    ori_str_lv = ori_str
    conv_h = opencc.OpenCC('t2s')  # convert from Traditional Chinese to Simplified Chinese
    conv_str_lv = conv_h.convert(ori_str_lv)
    return conv_str_lv
