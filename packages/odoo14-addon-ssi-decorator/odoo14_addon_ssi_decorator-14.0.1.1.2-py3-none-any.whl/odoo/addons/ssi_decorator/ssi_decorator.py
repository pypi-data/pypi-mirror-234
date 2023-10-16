# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


def attrsetter(attr, value):
    return lambda method: setattr(method, attr, value) or method


# CONFIRM
def pre_confirm_check(*args):
    return attrsetter("_pre_confirm_check", args)


def post_confirm_check(*args):
    return attrsetter("_post_confirm_check", args)


def pre_confirm_action(*args):
    return attrsetter("_pre_confirm_action", args)


def post_confirm_action(*args):
    return attrsetter("_post_confirm_action", args)


# APPROVE
def pre_approve_check(*args):
    return attrsetter("_pre_approve_check", args)


def post_approve_check(*args):
    return attrsetter("_post_approve_check", args)


def pre_approve_action(*args):
    return attrsetter("_pre_approve_action", args)


def post_approve_action(*args):
    return attrsetter("_post_approve_action", args)


# REJECT
def pre_reject_check(*args):
    return attrsetter("_pre_reject_check", args)


def post_reject_check(*args):
    return attrsetter("_post_reject_check", args)


def pre_reject_action(*args):
    return attrsetter("_pre_reject_action", args)


def post_reject_action(*args):
    return attrsetter("_post_reject_action", args)


# OPEN
def pre_open_check(*args):
    return attrsetter("_pre_open_check", args)


def post_open_check(*args):
    return attrsetter("_post_open_check", args)


def pre_open_action(*args):
    return attrsetter("_pre_open_action", args)


def post_open_action(*args):
    return attrsetter("_post_open_action", args)


# DONE
def pre_done_check(*args):
    return attrsetter("_pre_done_check", args)


def post_done_check(*args):
    return attrsetter("_post_done_check", args)


def pre_done_action(*args):
    return attrsetter("_pre_done_action", args)


def post_done_action(*args):
    return attrsetter("_post_done_action", args)


# CANCEL
def pre_cancel_check(*args):
    return attrsetter("_pre_cancel_check", args)


def post_cancel_check(*args):
    return attrsetter("_post_cancel_check", args)


def pre_cancel_action(*args):
    return attrsetter("_pre_cancel_action", args)


def post_cancel_action(*args):
    return attrsetter("_post_cancel_action", args)


# RESTART
def pre_restart_check(*args):
    return attrsetter("_pre_restart_check", args)


def post_restart_check(*args):
    return attrsetter("_post_restart_check", args)


def pre_restart_action(*args):
    return attrsetter("_pre_restart_action", args)


def post_restart_action(*args):
    return attrsetter("_post_restart_action", args)


# TERMINATE
def pre_terminate_check(*args):
    return attrsetter("_pre_terminate_check", args)


def post_terminate_check(*args):
    return attrsetter("_post_terminate_check", args)


def pre_terminate_action(*args):
    return attrsetter("_pre_terminate_action", args)


def post_terminate_action(*args):
    return attrsetter("_post_terminate_action", args)


# WIN
def pre_win_check(*args):
    return attrsetter("_pre_win_check", args)


def post_win_check(*args):
    return attrsetter("_post_win_check", args)


def pre_win_action(*args):
    return attrsetter("_pre_win_action", args)


def post_win_action(*args):
    return attrsetter("_post_win_action", args)


# LOST
def pre_lost_check(*args):
    return attrsetter("_pre_lost_check", args)


def post_lost_check(*args):
    return attrsetter("_post_lost_check", args)


def pre_lost_action(*args):
    return attrsetter("_pre_lost_action", args)


def post_lost_action(*args):
    return attrsetter("_post_lost_action", args)


# fields_view_get
def insert_on_tree_view(*args):
    return attrsetter("_insert_on_tree_view", args)


def insert_on_form_view(*args):
    return attrsetter("_insert_on_form_view", args)


def insert_on_search_view(*args):
    return attrsetter("_insert_on_tree_view", args)
