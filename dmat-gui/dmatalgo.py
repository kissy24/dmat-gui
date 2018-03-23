# -*- Coding: utf-8 -*-

'''
災害派遣医療チーム (DMAT) とは，
大規模な災害時に被災者の生命を守るため救急医療を行う，
専門的な訓練を受けた医療チーム

dmatalgo.pyではdmatの編成から出力までを取り扱っている
'''

import random
import csv
import dmatdata
import dmatdb


def dmat_algorithm(data_list):
    '''
    DMAT編成アルゴリズム
    '''
    # 期間をtrueの隊員でソート
    true_list = period_divide(data_list)
    # スキルで３職に分離
    doctor_list = skill_divide('doctor', true_list)
    nurse_list = skill_divide('nurse', true_list)
    staff_list = skill_divide('staff', true_list)
    # 派遣元ごとの辞書を生成(各スキルごとに)
    doctor_dict = area_divide(doctor_list)
    nurse_dict = area_divide(nurse_list)
    staff_dict = area_divide(staff_list)
    # エリアごとの編成
    area_team_dict = area_team(doctor_dict, nurse_dict, staff_dict)
    return area_team_dict


def area_divide(skill_list):
    '''
    都道府県別に分ける
    '''
    area_skill_dict = {}
    # dmatdata.pyの派遣元の生成を利用している
    area = dmatdata.generate_area('sa', 34)
    for a in area:
        inner_list = []
        for sd in skill_list:
            if a == sd[2]:
                inner_list.append(sd[0])
        area_skill_dict[a] = inner_list
    return area_skill_dict


def dmat_team(a_dict, da_dict):
    '''
    編成したDMATを被災地に派遣
    '''
    all_list = dmat_area_include(a_dict)
    output_dmat = {}
    for da in da_dict.keys():
        da_dmat_list = []
        for d in range(da_dict[da]):
            da_dmat_list.append(all_list[0])
            all_list.remove(all_list[0])
        output_dmat[da] = da_dmat_list
    return output_dmat


def dmat_area_include(a_dict):
    '''
    dmatリスト内に派遣元の情報を格納する
    (最初から格納すれば良いのだがarea_outputerを先につくってしまったため
    ここで変換し直している。やる気がある方は修正して)
    '''
    all_dmat_list = []
    for a_k in a_dict.keys():
        for a_v in a_dict[a_k]:
            a_v.insert(0, a_k)
            all_dmat_list.append(a_v)
    return all_dmat_list


def area_team(d_dict, n_dict, s_dict):
    '''
    エリアごとにチームを最大数編成し、余剰はエリアに関係なく編成
    '''
    output_dict = {}
    # 余った医師、看護師、事務職員
    remain_d = []
    remain_n = []
    remain_s = []
    # s_dictでもn_dictでも良い
    for a in d_dict.keys():
        # エリアごとの編成
        team_list = []
        while True:
            # エリアごとに編成できなくなった時の対処として余った隊員のリストを作成
            if len(d_dict[a]) == 0 or len(n_dict[a]) <= 1 or len(s_dict[a]) == 0:
                remain_d.extend(d_dict[a])
                remain_n.extend(n_dict[a])
                remain_s.extend(s_dict[a])
                break
            else:
                dm_list = []
                dm_list.extend(dmat_choice(d_dict[a], 1))
                dm_list.extend(dmat_choice(n_dict[a], 2))
                dm_list.extend(dmat_choice(s_dict[a], 1))
                team_list.append(dm_list)
        output_dict[a] = team_list
    remain_list = []
    # 余った隊員で編成
    while True:
        # ここでさらに余った隊員を考慮する場合はbreak前に値を取ってやると取得できる
        if len(remain_d) == 0 or len(remain_n) <= 1 or len(remain_s) == 0:
            break
        else:
            dm_list = []
            dm_list.extend(dmat_choice(remain_d, 1))
            dm_list.extend(dmat_choice(remain_n, 2))
            dm_list.extend(dmat_choice(remain_s, 1))
            remain_list.append(dm_list)
    # 便宜上エリアを余りとしている
    output_dict['remain'] = remain_list
    return output_dict


def dmat_choice(dmat_list, dmat_num):
    '''
    DMATの選出
    '''
    dmat_c = random.sample(dmat_list, dmat_num)
    for dc in dmat_c:
        dmat_list.remove(dc)
    return dmat_c


def period_divide(data_list):
    '''
    急性期に出動できる隊員を選出する
    '''
    true_list = []
    for i in data_list:
        if i[3] == 'True':
            true_list.append(i)
    return true_list


def skill_divide(skill, data_list):
    '''
    スキルでリスト分け
    '''
    skill_list = []
    for i in data_list:
        if i[1] == skill:
            skill_list.append(i)
    return skill_list


def csv_read():
    '''
    csv形式のテストデータの読み込み
    guiアプリでは使わないがcsv読み込みさせたい時に使える
    '''
    data_list = []
    with open('dmatdata.csv',  newline='') as f:
        data_reader = csv.reader(f)
        for row in data_reader:
            data_list.append(row)
    return data_list


def db_read():
    '''
    dbのデータを読み込み
    '''
    dmat_data = dmatdb.getContent()
    return dmat_data

def area_outputer(output_dict):
    '''
    エリア毎のデータを綺麗に表示する
    '''
    count_team = 0  # 総チーム数のカウント
    count_area = 0  # 正常に全てのエリアで編成できているかの確認のためのカウント
    for od in output_dict.keys():
        print('エリア :' + od)
        print('編成数 : ' + str(len(output_dict[od])))
        count_team += len(output_dict[od])
        count_area += 1
        for o in output_dict[od]:
            print(o)
    print('総編成数 : ' + str(count_team))
    print('エリア数+あまり１ : ' + str(count_area))


def gui_outputer(output_dict):
    """
    GUI表示のためのデータ整形
    """
    output_str = ''
    count = 0
    for od in output_dict.keys():
        output_str = output_str + '被災地 :' + od + '\n'
        output_str = output_str + str(len(output_dict[od])) + '\n'
        count += len(output_dict[od])
        for o in output_dict[od]:
            output_str = output_str + str(o) + '\n'
    output_str = output_str + '総派遣数' + str(count)
    return output_str


def main():
    dmat_data = dmat_algorithm(db_read())
    # 被災地の設定
    disaster_dict = dmatdata.generate_disaster_area()
    dmat_dict = dmat_team(dmat_data, disaster_dict)
    output = gui_outputer(dmat_dict)
    return output


if __name__ == '__main__':
    # エリアごとの編成の結果の表示
    area_outputer(dmat_algorithm(csv_read()))
