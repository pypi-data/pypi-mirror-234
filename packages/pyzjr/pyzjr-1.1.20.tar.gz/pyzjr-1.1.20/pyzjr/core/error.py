from .general import is_pil

__all__=["Error_flags","Augment_Error_Message","_check_img_is_plt","_check_parameter_is_tuple_2","_check_parameter_is_tuple_and_list_2"]
Error_flags = "[pyzjr error]:"

Augment_Error_Message = "Image should be PIL image. Got {}. Use Decode() for encoded data or ToPIL() for decoded data."

def _check_img_is_plt(img):
    if not is_pil(img):
        raise TypeError(Augment_Error_Message.format(type(img)))

def _check_parameter_is_tuple_2(a):
    if not isinstance(a, tuple) or len(a) != 2:
        raise ValueError(f"{a} should be a tuple (x_para,y_para).")

def _check_parameter_is_tuple_and_list_2(a):
    if not isinstance(a, (list, tuple)) or len(a) != 2:
        raise ValueError(f"{a} should be a list or tuple of two values [x_para,y_para].")