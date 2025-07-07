from otree.api import *
import random


doc = """ """


class C(BaseConstants):
    NAME_IN_URL = "ch10_2_ultimatum"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = 600
    INSTRUCTIONS_TEMPLATE = "ch10_2_ultimatum/instructions.html"
    ADD_TIME = 180

    CHOICE_LIST_SENTE = [
        [0, "あなた0ポイント、相手600ポイント"],
        [200, "あなた200ポイント、相手400ポイント"],
        [400, "あなた400ポイント、相手200ポイント"],
        [600, "あなた600ポイント、相手0ポイント"],
    ]

    CHOICE_LIST_GOTE_TMP = [
        [600, "あなた600ポイント"],
        [400, "あなた400ポイント"],
        [200, "あなた200ポイント"],
        [0, "あなた0ポイント"],
    ]

    CHOICE_LIST_GOTE = [[0, "承諾"], [1, "拒否"]]


class Subsession(BaseSubsession):
    num_participants_p1 = models.IntegerField(initial=0)
    num_participants_p2 = models.IntegerField(initial=0)
    num_1000 = models.IntegerField(initial=0)
    num_900 = models.IntegerField(initial=0)
    num_800 = models.IntegerField(initial=0)
    num_700 = models.IntegerField(initial=0)
    num_600 = models.IntegerField(initial=0)
    num_500 = models.IntegerField(initial=0)
    num_400 = models.IntegerField(initial=0)
    num_300 = models.IntegerField(initial=0)
    num_200 = models.IntegerField(initial=0)
    num_100 = models.IntegerField(initial=0)
    num_0 = models.IntegerField(initial=0)
    num_accept = models.IntegerField(initial=0)
    num_reject = models.IntegerField(initial=0)

    #
    num_participants = models.IntegerField(initial=0)
    num_600_accept = models.IntegerField(initial=0)
    num_600_reject = models.IntegerField(initial=0)
    num_400_accept = models.IntegerField(initial=0)
    num_400_reject = models.IntegerField(initial=0)
    num_200_accept = models.IntegerField(initial=0)
    num_200_reject = models.IntegerField(initial=0)
    num_0_accept = models.IntegerField(initial=0)
    num_0_reject = models.IntegerField(initial=0)

    err_message = models.StringField()
    err_message_pair = models.StringField()


class Group(BaseGroup):
    p1_amount = models.IntegerField()
    p2_amount = models.IntegerField()

    p1_decision = models.StringField(
        choices=C.CHOICE_LIST_SENTE, widget=widgets.RadioSelect, label=""
    )

    p2_decision = models.StringField(
        choices=C.CHOICE_LIST_GOTE, widget=widgets.RadioSelect, label=""
    )

    p1_decision_why = models.LongStringField(label="なぜその選択をしましたか？")

    p2_decision_why = models.LongStringField(label="なぜその選択をしましたか？")

    flg_non_input_p1 = models.IntegerField(initial=0)
    flg_non_input_p2 = models.IntegerField(initial=0)


class Player(BasePlayer):
    # 戦略法
    tmp_first_player = models.StringField(
        choices=C.CHOICE_LIST_SENTE, widget=widgets.RadioSelect, label=""
    )
    tmp_first_player_why = models.LongStringField(label="なぜその選択をしましたか？")

    tmp_second_player = models.StringField(
        choices=C.CHOICE_LIST_GOTE_TMP, widget=widgets.RadioSelect, label=""
    )
    tmp_second_player_why = models.LongStringField(label="なぜその選択をしましたか？")


# FUNCTIONS
def set_P1(player: Player):
    sub = player.subsession
    group = player.group

    if group.p1_decision != "":
        sub.num_participants_p1 += 1
        print("++++++++++++++++", group.p1_decision)
        s = group.p1_decision
        if s == "1000":
            sub.num_1000 += 1
        elif s == "900":
            sub.num_900 += 1
        elif s == "800":
            sub.num_800 += 1
        elif s == "700":
            sub.num_700 += 1
        elif s == "600":
            sub.num_600 += 1
        elif s == "500":
            sub.num_500 += 1
        elif s == "400":
            sub.num_400 += 1
        elif s == "300":
            sub.num_300 += 1
        elif s == "200":
            sub.num_200 += 1
        elif s == "100":
            sub.num_100 += 1
        elif s == "0":
            sub.num_0 += 1
        else:
            sub.err_message = "エラーあり"
    else:
        group.flg_non_input_p1 = 1
        tmp = random.randint(0, len(C.CHOICE_LIST_SENTE) - 1)
        group.p1_decision = str(C.CHOICE_LIST_SENTE[tmp][0])
    # 先手の配分計算
    # group.p1_amount = C.ENDOWMENT - int(group.p1_decision)
    group.p1_amount = int(group.p1_decision)
    group.p2_amount = C.ENDOWMENT - int(group.p1_decision)


def set_P2(player: Player):
    sub = player.subsession
    group = player.group
    s = group.p2_decision
    if s != "":
        # グラフ用集計
        sub.num_participants_p2 += 1
        if s == "0":
            sub.num_accept += 1
        elif s == "1":
            sub.num_reject += 1
        else:
            sub.err_message = "エラーあり"
    else:
        group.flg_non_input_p2 = 1
        tmp = random.randint(0, 1)
        group.p2_decision = str(C.CHOICE_LIST_GOTE[tmp][0])


def set_pair(player: Player):
    sub = player.subsession
    group = player.group
    p1 = group.p1_decision
    p2 = group.p2_decision

    sub.num_participants += 1

    if p1 == "600" and p2 == "0":
        sub.num_600_accept += 1
    elif p1 == "600" and p2 == "1":
        sub.num_600_reject += 1
    elif p1 == "400" and p2 == "0":
        sub.num_400_accept += 1
    elif p1 == "400" and p2 == "1":
        sub.num_400_reject += 1
    elif p1 == "200" and p2 == "0":
        sub.num_200_accept += 1
    elif p1 == "200" and p2 == "1":
        sub.num_200_reject += 1
    elif p1 == "0" and p2 == "0":
        sub.num_0_accept += 1
    elif p1 == "0" and p2 == "1":
        sub.num_0_reject += 1
    else:
        sub.err_message_pair = "エラーあり"


def set_P2s(subsession: Subsession):
    for p in subsession.get_players():
        set_P2(p)


def set_P1s(subsession: Subsession):
    for p in subsession.get_players():
        set_P1(p)


def set_pairs(subsession: Subsession):
    for p in subsession.get_players():
        set_pair(p)
    graph(subsession=subsession)


def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)

    # 0：承諾
    if group.p2_decision == "0":
        # p1.payoff = C.ENDOWMENT - int(group.p1_decision)
        # p2.payoff = int(group.p1_decision)
        p1.payoff = int(group.p1_decision)
        p2.payoff = C.ENDOWMENT - int(group.p1_decision)
    # 1：拒否
    else:
        p1.payoff = 0
        p2.payoff = 0


# グラフ描画用
def graph(subsession: Subsession):
    sub = subsession
    session = sub.session
    graph_list_accept = []
    graph_list_reject = []

     # 提案額リスト（← 使ってる選択肢に合わせて）
    amount_list = [0, 200, 400, 600]

    # Reject集計
    for amt in amount_list:
        num_reject = getattr(sub, f"num_{amt}_reject", 0)
        tmp = round((num_reject / sub.num_participants) * 100, 2) if num_reject > 0 else 0
        graph_list_reject.append(tmp)

    # Accept集計
    for amt in amount_list:
        num_accept = getattr(sub, f"num_{amt}_accept", 0)
        tmp = round((num_accept / sub.num_participants) * 100, 2) if num_accept > 0 else 0
        graph_list_accept.append(tmp)

    ch10_2_result = []


    print(graph_list_accept, graph_list_reject)

    for player in subsession.get_players():
        group = player.group
        participant = player.participant

        p2_decision = ""
        if group.p2_decision == "0":
            p2_decision = "承諾"
        else:
            p2_decision = "拒否"

        participant.vars["ch10_2_result"] = (
            "++++++++++++++++++++++++++++++++++++++++++++++++++<br>"
            "最後通牒ゲーム：あなたの結果："
            "プレイヤー1（先手）は、プレイヤー1に"
            + str(group.p1_amount)
            + "ポイント、プレイヤー2に"
            + str(group.p2_amount)
            + "という提案をしました。<br>"
            "プレイヤー2（後手）は、プレイヤー1の提案を" + (p2_decision) + "しました。<br>"
            "++++++++++++++++++++++++++++++++++++++++++++++++++"
        )

    ch10_2_result.append(participant.vars["ch10_2_result"])

    # 最終結果用
    if "graph_data" not in session.vars:
        session.graph_data = {}
    session.graph_data["ch10_2"] = {
        "num_participants": sub.num_participants,
        "graph_list_accept": graph_list_accept,
        "graph_list_reject": graph_list_reject,
        "ch10_2_result": ch10_2_result,
    }


# PAGES-----
class Introduction(Page):
    timeout_seconds = 60


class Strategy(Page):
    timeout_seconds = 120 + C.ADD_TIME
    form_model = "player"
    form_fields = [
        "tmp_first_player",
        "tmp_first_player_why",
        "tmp_second_player",
        "tmp_second_player_why",
    ]


class Send(Page):
    # timeout_seconds = 60
    timeout_seconds = C.ADD_TIME
    form_model = "group"
    form_fields = ["p1_decision", "p1_decision_why"]

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class WaitForP1(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = set_P1s


class SendBack(Page):
    # timeout_seconds = 60
    timeout_seconds = C.ADD_TIME
    form_model = "group"
    form_fields = ["p2_decision", "p2_decision_why"]

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2


class WaitForP2(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = set_P2s


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class ResultWaitPair(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = set_pairs


class Results(Page):
    @staticmethod
    def js_vars(player: Player):
        print("js_vars")
        return player.session.graph_data


page_sequence = [
    Introduction,
    Strategy,
    Send,
    WaitForP1,
    SendBack,
    WaitForP2,
    ResultsWaitPage,
    ResultWaitPair,
    Results,
]
