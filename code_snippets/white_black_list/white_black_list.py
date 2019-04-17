def is_acceptable(email, white_list=None, black_list=None):
    white_lst = white_list or []
    black_lst = black_list or []

    assert isinstance(white_lst, list)
    assert isinstance(black_lst, list)

    return True if not (black_lst and email in black_lst) and (not white_lst or email in white_lst) else False
