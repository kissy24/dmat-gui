# -*- Coding: utf-8 -*-

'''
災害派遣医療チーム (DMAT) とは，
大規模な災害時に被災者の生命を守るため救急医療を行う，
専門的な訓練を受けた医療チーム

dmatdata.pyではdmat編成のための数値,テストデータを生成している
そのため一部dmatalgoの方でも流用している
'''

import random
import csv


def csv_output(output_list):
    '''
    csv形式にテストデータを出力
    '''
    f = open('dmatdata.csv', 'w')
    writer = csv.writer(f, lineterminator='\n')
    for i in output_list:
        writer.writerow(i)
    f.close()


def generator():
    '''
    テストデータ生成のmain部分
    '''
    output_list = []
    # ここに医師の人数など定数を直接代入している
    doctors_name = generate_name('d', 1463 * 2)
    nurses_name = generate_name('n', 1774 * 2)
    staff_name = generate_name('s', 1101 * 2)
    # 34は南海トラフの被災地が13県にまたがるので単純に47-13で34としている
    safe_area = generate_area('sa', 34)
    period = [True, False]
    output_list.extend(generate_data(doctors_name, 'doctor', safe_area, period))
    output_list.extend(generate_data(nurses_name, 'nurse', safe_area, period))
    output_list.extend(generate_data(staff_name, 'staff', safe_area, period))
    return output_list


def generate_data(name_list, skill, sa_list, period):
    '''
    テストデータの整形
    '''
    person_list = []
    for i in name_list:
        inner_list = []
        sa = random.choice(sa_list)
        p = random.choice(period)
        inner_list.append(i)
        inner_list.append(skill)
        inner_list.append(sa)
        inner_list.append(p)
        person_list.append(inner_list)
    return person_list


def generate_name(skill, pe_num):
    '''
    DMAT隊員の名前を作成
    今回は結果が判別しやすいように医師はdj,看護師はnj,事務職員はsjとしている
    '''
    virtual_name = []
    for i in range(pe_num):
        virtual_name.append(skill + str(i + 1))
    return virtual_name


def generate_area(area_name, area_num):
    '''
    派遣元の生成
    表記はsaj
    '''
    virtual_area = []
    for i in range(area_num):
        virtual_area.append(area_name + str(i + 1))
    return virtual_area


def generate_disaster_area():
    '''
    被災地の生成
    dmatalgo.pyで使うモジュール
    '''
    da_dict = {}
    # 例、da_dict = [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
    team_num = 50
    disaster_area = generate_area('da', 13)
    for da in disaster_area:
        da_dict[da] = team_num
    return da_dict


def main():
    csv_output(generator())


if __name__ == '__main__':
    main()
