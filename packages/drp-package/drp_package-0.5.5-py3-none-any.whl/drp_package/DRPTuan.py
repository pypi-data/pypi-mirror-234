

from ortools.linear_solver import pywraplp
import numpy as np
import math
import copy
import collections
from ortools.sat.python import cp_model
import matplotlib.pyplot as plt
import time
import json
import os


import matplotlib.colors as mcolors
from matplotlib.pyplot import figure
import random
import json
import codecs



def numpy_to_list(data):
    if isinstance(data, dict):
        return {key: numpy_to_list(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [numpy_to_list(item) for item in data]
    elif isinstance(data, np.ndarray):
        return data.tolist()
    else:
        return data

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(numpy_to_list(data), json_file, indent=4, sort_keys=True)

def create_fake_data(s,num_products, num_factories, num_depots, num_physic_depots, num_days_in_priods):

    fake_data = {}

    # create data
    fake_data['num_days_in_priods'] = num_days_in_priods
    fake_data['num_products'] = num_products
    fake_data['num_factories'] = num_factories
    fake_data['num_depots'] = num_depots
    fake_data['num_physic_depots'] = num_physic_depots

    # supply
    fake_data['matrix_supply_min'] = np.random.randint(10, 50,size= (num_factories, num_products))
    fake_data['matrix_supply_max'] = np.random.randint(100, 120,size= (num_factories, num_products))

    # demand
    fake_data['matrix_demand'] = np.random.randint(100*num_factories/num_depots , 120*num_factories/num_depots , size= (num_depots, num_products))

    # khả năng nhập của kho vật lý
    fake_data['limit_in'] = np.random.randint(70*num_days_in_priods,130*num_days_in_priods, num_physic_depots) # ---> xác định bằng cách lấy lương 1 ngày x 7

    # chi phí xử lý nhập hàng mỗi pallet của mỗi kho
    fake_data['handlingCost_in'] = np.random.randint(10,30, num_depots)

    # location all points
    number_location = num_factories + num_depots
    loc =  np.random.randint(1,100, (number_location,2))
    loc_f = loc[:num_factories]
    loc_h = loc[num_factories :num_factories + num_depots]

    fake_data['loc_f'] = np.copy(loc_f)
    fake_data['loc_h'] = np.copy(loc_h)

    # matrix distance factory - depot
    distane_f_h = np.empty((num_factories,num_depots), np.int_)
    for i in range(num_factories):
        for j in range(num_depots):
            distane_f_h[i,j] = round(((loc_f[i][0] - loc_h[j][0] )**2 + (loc_f[i][1] - loc_h[j][1] )**2 )**0.5)

    fake_data['distane_f_h'] = np.copy(distane_f_h)

    # matrix config
    mat_config_FD = np.ones((num_factories, num_depots), np.int_)
    fake_data['mat_config_FD'] = np.copy(mat_config_FD)

    # map physic depots with depots
    map_physic_depots_with_depots  = np.zeros((num_physic_depots, num_depots), np.int_)

    # Đặt giá trị ngẫu nhiên thành 1 trong mỗi cột sao cho tổng mỗi cột bằng 1
    for physic_dep in range(num_depots):
        # Tạo một chỉ mục ngẫu nhiên trong mỗi cột
        idx = np.random.choice(num_physic_depots)
        # Đặt giá trị tại chỉ mục đó thành 1
        map_physic_depots_with_depots[idx, physic_dep] = 1

    fake_data['map_physic_depots_with_depots'] = np.copy(map_physic_depots_with_depots)

    # phân cụm cho các kho vật lý
    fake_data['cluster_physic_depot'] = []
    for cluster_idx in range(len(fake_data['map_physic_depots_with_depots'] )):
        depot_in_cluster = []
        for dep_idx in range(num_depots):
            if fake_data['map_physic_depots_with_depots'][cluster_idx][dep_idx] == 1:
                depot_in_cluster.append(dep_idx)
        fake_data['cluster_physic_depot'].append(depot_in_cluster)

    matrix_weight_product = np.random.randint(1, 2,  num_products)

    fake_data['fixed_cost_by_sku_per_factory'] = np.random.randint(10, 50, size= (num_factories, num_products))

    fake_data['fixed_cost_physics_depot'] =  np.random.randint(1, 2,  num_physic_depots)

    fake_data['penalty_cost'] =  np.random.randint(1_000_000, 1_000_001, size= (num_depots, num_products))

    fake_data['weight_product'] = [1]*num_products
    fake_data['ratio_capacity'] = [1]*num_products
    fake_data['IB_transport_cost'] = np.copy(distane_f_h)
    # Kiểm tra kiểu dữ liệu của các biến

    if s=="":
        named_tuple = time.localtime() # get struct_time
        time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
        save_to_json(fake_data, "DRP_week"+time_string[11:]+".json")
        print(  "DRP_week"+time_string[8:10]+"_"+time_string[12:]+".json")
    else:
        save_to_json(fake_data, s+".json")
        print(s+".json")

    return fake_data

def convert_to_numpy(data):
    if isinstance(data, dict):
        return {key: convert_to_numpy(value) for key, value in data.items()}
    elif isinstance(data, list):
        return np.array([convert_to_numpy(item) for item in data])
    else:
        return data

def load_from_json(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        return data



"""# Visualize Input

#Class Input
"""

class Input:

    def __init__(self, data_model=None, file_name=None, num_days_in_priods = 7, num_factories=4, num_depots=3, num_physic_depots=2, num_products=3):

        if data_model:
            self._initialize_from_data_model(data_model)
            self.data = data_model

        elif file_name:
            self.data = self._initialize_from_file(file_name)
        else:
            self.data = self._initialize_fake_data(num_days_in_priods = 7, num_factories=4, num_depots=3, num_physic_depots=2, num_products=3)

        self.output = "Not been solved"

    def _initialize_from_data_model(self, data_model):

        # self.data = data_model
        return data_model
        # self.problem = ORModel(self.input)

    def _initialize_from_file(self, file_name):

        full_path = file_name
        data_json = load_from_json(full_path)
        data_model = convert_to_numpy(data_json)
        self._initialize_from_data_model(data_model)
        return data_model


    def _initialize_fake_data(self, num_days_in_priods = 7, num_factories=4, num_depots=3, num_physic_depots=2, num_products=3 ):

        data_model = create_fake_data("test3009_", num_products, num_factories, num_depots, num_physic_depots, num_days_in_priods)
        # filename =  '/content/drive/My Drive/Colab Notebooks/sabeco3/test3009_.json'
        # print("successfully create faked input")
        # data_json = load_from_json(filename)
        # data_model = convert_to_numpy(data_json)
        # data_model = create_fake_data("test3009_", num_products, num_factories, num_depots, num_physic_depots, num_days_in_priods)

        self._initialize_from_data_model(data_model)
        return data_model

    def visualize_input(self):

        data= self.data

        # visualize vị trí của kho và NPP
        location_factory = data['loc_f']

        print("location_factory", type(location_factory),location_factory )
        print(location_factory[:, 0])

        location_depot = data['loc_h']
        plt.plot( location_factory[:, 0], location_factory[:, 1], "rs")
        plt.plot( location_depot[:, 0], location_depot[:, 1], "bo")

        plt.show()

        figure(figsize=(8, 6), dpi=80)

        # visualize số lượng két thùng của lượng hàng tồn kho, deamnd NPP và lượng tồn kho an toàn
        X = ["SKU " +str(i) for i in range(data['num_products'])]

        # for day in range(num_days):
        supply_max_list = data['matrix_supply_max']
        supply_min_list = data['matrix_supply_min']

        demand_list = data['matrix_demand']
        limitIn_depot = data['limit_in']

        print("demand_list", demand_list)
        # safety_stock = data['safety_stock'] # lượng hàng tồn kho an toàn tính theo từng SKU đơn vị két thùng, và được tính bằng số ngày bán hàng, được tính bằng một module khác.
        X_axis = np.arange(data['num_products'])

        plt.bar(X_axis - 0.2, np.sum(supply_max_list, axis=0) , 0.1, label = 'supply_max_list')
        plt.bar(X_axis - 0.4, np.sum(supply_min_list, axis=0) , 0.1, label = 'supply_min_list')

        plt.bar(X_axis , np.sum(demand_list, axis=0) , 0.1, label = 'demand')
        # plt.bar(X_axis + 0.2 , np.sum(limitIn_depot, axis=0) , 0.1, label = 'limit_in_depot')

        # plt.bar(X_axis + 0.2, np.sum(safety_stock, axis=0) , 0.1, label = 'safety_stock')

        plt.xticks(X_axis, X)
        plt.xlabel("Mã SKU")
        plt.ylabel("số lượng ket/thùng")
        # plt.title("số lượng két/thùng từng mã của lượng hàng tồn kho và lượng hàng cần của NPP ngày "+str(day))
        plt.legend()
        plt.show()

    def draw_limit_in(self):
        data= self.data


        # xử lý data
        capacity_N = np.empty((data['num_depots'], data['num_products']))
        print("matrix_demand", data['matrix_demand'])
        print("ratio_capacity",data['ratio_capacity'] )


        for dep_idx in range(data['num_depots']):
            for item_idx in range(data['num_products']):
                capacity_N[dep_idx][item_idx] = data['matrix_demand'][ dep_idx, item_idx] *data['ratio_capacity'][item_idx]
        print("capacity_N", capacity_N)

        # vẽ

        bar_width = 0.1
        X_axis = np.arange(len(data['cluster_physic_depot']))
        print("X_axis", X_axis)
        color_list  = [ 'r',  'g', 'b', 'c','m','y', 'navy', 'lime', 'tan', 'coral', 'pink']

        luong_hang_inPD = []
        for physic_depot_id in range(len(data['cluster_physic_depot'])):

            cluster = data['cluster_physic_depot'][physic_depot_id]
            limitIn_cluster = data['limit_in'][physic_depot_id]

            luong_hang_inPD.append(np.sum([ capacity_N[depot_idx,:] for depot_idx in cluster]))
        print("X_axis", X_axis)
        print("luong_hang_inPD", luong_hang_inPD)
        plt.bar(X_axis, luong_hang_inPD, width = bar_width ,edgecolor ='grey', label ='lượng hàng trong kho')

        plt.bar(X_axis + [bar_width]*len(X_axis),  data['limit_in'], width = bar_width ,edgecolor ='grey', label ='lượng hàng giới hạn')


        # axis[0].set_xticks(X_axis, ["kho vật lý "+ str(i ) for i in range(len(data['cluster_physic_depot']))])
        # axis[0].plot(len(X_axis)+1,0)
        plt.legend()
        plt.show()
    def help(self):
        s =  "visualize_input()\ndraw_limit_in()"
        print(s)
    def print(self):
        print(self.data)


"""# Model

![image.png](data:image/png;base64,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7dLZXXzev7kXl9yVHKkMwvnB2V/x4QohhBBCiOojAd1OYTxyLYU0454XLF2rT1aVwKN/W+beffc99/4t3kuObMrqprX+PNFx+OKxo9yoEX3dc4/dkRwpD64/+IA93VeOPyI5IoQQQgghqo0EdDunFkKa6/lk1fij5LpdCr+ZcYfr9L6WicOy2Grbt90vb/ifZE90FK6c+HV3YP+u7rlH/8e9927yofeccP4zC291B+zdxf1s0jeTo0KIQhx33HGuU6dOVV0uvfTSJHQhhBDtGQnoDkK1hLR9smrU4J3coD7bJUdFMd5++x13wy13uc02e8/ttcsA99vv3r/R8oN/vdaft8U2b7qZ/3OPP190LH426Vtu9LDd3T/u/6Vbs/LR5GhhOO+pv/zSjTpodzflR6cnR4UQxbjoootcly5dkj3n5s6d69atW1fysnTpUjd48OAkFCGEEB0BCegORqVCevYDL3ir80mjd0uOiDxMv2WO+9BuzY9bJ+f+/swi9/n/HLrR8r1fnezPe/8H3nOdu7/mzxcdj0nfP8X96r8muG3fesItf+DX7vkl89xrTc+4t994ybn33vNr9p9fOs//vvWbT7jfXDnB/dcPTk1CEELkYY899nDXXXddsufcuHHj3KpVq5K9/BDOj370o2RPCCFER0ACuoMSC+nLpj9RVEgvfeZV77p96md6JUdEXn5xw/+4rbo/k+wVZofd1rqfTbsl2RMdjRFDB7i7Zl7mpv7kDHf0wTu69695wD274Ldu4R9/5J5fOMNtsfZBN3pwF//7/950mT9fCFE6Rx55pDvnnHP8Npbkr33ta367VA4++GDXu3fvZE8IIUR7RwK6g2NCunePrQsKaVy3L7vhCf/Jqp27bpkcFXn4y0OL3T/XrHJdP5TP0s95q9Y2+etEx+WAffdy5585zovkv93zC//t98fu/rmbM+NSd9l5X/W/CyEq48ILL1zvgn3DDTe4a665xm+Xity4hRCi4yABLTyxkD7/l49vJKT1yaryuW7mLNdt16ZkLx/bfuh5N+XG25I9IYQQtQLhbOOhTz31VLdgwQK/XQrTp093Z511VrJXe4ijTV4mhBCivkhAi40wIb1v785uwuRFXkjfeNcKd++iVfpkVREYH87nvcLl+llPud//+W/ubw9t6ebe2NO98+Zm7uVVm/vtcFkwZycfxsol2/j9pxZs5265fb5b0/SyPy6EEKI2xOOhjznmmLLGQ9cCZgs/99xzk70NDBo0yF1yySWyfAshRCvQqampqfB3dRIWL17shg0bluyJjsKv7ljupv1phev34W3d2WP3lPt2xLwTurrh16/22whoXOBDunfdwl19+n41+9xXeH8hhBDlg1Bldm4YM2aMtyo3MsR3zZo17qqrrkqONCZYy/fbbz/34osvum7d5MUmhKic+fPnu/79+yd79UcWaFGQp559zY39RE83ct9u6y3S5Xz+qiMwfEDXjYQy22cet6e+lS2EEG2AeDx0awvoYi7aDz30kOvVq5c77bTT/HlYqxsRrOV88kviWQjRXpCAFpnggszkYbh1s1x37uCNXLslpFsgj+YtWu1OveIRt/VW70uOOve5kR/y48aFEEK0DcLx0AjTcsZDVwtctEePHp3sbcqsWbPctdde60455RR32223udmzZye/NA6XXnqpF/es68WTTz7pOxOsAyJvx4KNK290zwMhROsjAS1SsU9WMet2aEGVkN4AwvnxLQ5yE65a5DsbLvhSP583uG1jjda3soUQom0RjofGPfqrX/1qVcZD33PPPesF3ZAhQ5KjLZjIjMXesmXL3GGHHZbsbQzhwcyZM72F9+mnn3ajRo3yx+oJojMUq127dnVHHHGEF7FgE6sNHz7cr2sNZYUXAfHA6s1nyvbff//k18I89thjft2vXz+/FkKILCSgxSbYJ6uOHtnD9d5l6+ToxsRCGhHJRGMdAfJnwZK1Pt3ztz7KnXn8nm7SaQP8DOaA2zaLEEKItkf4fegHH3zQffe73/XblcC3osMwTWACIhPRx/LTn/40Oeq8RTlLeD766KP+fMQz3Hzzze7QQw/125WAAMUCiwg2kZ4F4pl7IlYZ34xgHT9+vLeMb7ddi/eVpZP05wXLf58+fZK9dDiH+8adGz//+c99x8d//ud/+n3c8vPOjk5HAGmwPBVCiCwkoMUm2CerEMnFMCGNxXXy755q90LahDN5NP6o3d2XVp+zXjgb5J3GPQshRNslHA89efJkd/vtt/vtSkBUMjkZ3HnnnX5tMD4Ya7eNE0Z4Ll261FtDbRZuLNXmCn3XXXdtZHFGtO6zzz5lf8ea9CEg99xzT3f33Xe78847r6jo5V6IWCYxs3h/5Stfcb17916/f//99xd0Q08Dl3TSnpXnJvK//e1vbzSumjzDpZ37hceFEKLaSECLjUD8lvPJqvYupBHOjHFGOJM3WJwH9dH4ZiGEaK+E46FPPPHEjazG5TBnzhz39a9/3QvMn/3sZ8nRFhCaBx10ULLXAvc+8MAD3Re+8AW/j0u3WXaxTo8YMcJvA2L/qKOOcrvumv+/GwuzWXKvvPJK99nPftY98cQTXhDnsRiTH5Y/Bi7wS5YsSfacF+O4oSN4i1m0DSzApOfXv/51cmRjsDIDYt2gY4F8RXjTmYA7OVb0vJgLetonw4QQIkYCWqwH12TE75ljyp85OhbSiM5ZDzyf/Nr2SBPOIwaoZ1sIIdo78Xhosx6XC8IOizLhhG7cuEITfug6zL1Xr17txSjHsboiVrHOAr/ham488MADmxxLg3shEnGRHjdunA+buNxxxx3eAl2K5ZY4cm2hSbeI89lnn+0WLlxYkhv3GWec4TswTNiGC+HF1mfctBHPwIRquGKTprxwDQwcONCvhRCiEBLQYj2Tpi/x4rAallUT0sxEjfhsa0I6FM6jBu/kzv9SXwlnIYToYMTjofNaUWO4Dqsqos8syubGzeRVxdycuQ638kpBfPKt64kTJ3pxjiBHCJcD44xJ0/HHH+9FeTweGYgzYrbUuB9++OFefNPZwPW2MMYaQuuzgRUf+vbt69el0LlzZ78eOnSoXwshRCE6NTU1rUu2C7J48WI3bNiwZE+0N5hFevaDL7hJ4wfUZPwu4hkxStiI6tFDuie/NBYI58m3PuW3Ec6jhuxUMD/mndA12Wo9hl+/OtkSQghRC3BzxkqMlbMcwYmL8dq1a9cLSSzACEQsx7hR8z3nvJNdVQIW6BtvvNFbd+HMM8/0YrVcEY1o/trXvubDQ0xj9a3W+GPyhfHnTFBGmNyLMdpYynEzj0HEcz6W+FKhfC6++OKyrhVC1J/58+e7/v37J3v1RwJa+E9WfX/KY+6Ccf0yZ92uFo0qpBHOxOuVN97JJZyFEEJ0DHBRxso6bdo0L97KgfG4uEzb9Yg9LMEIcqysP/rRj0pyca4GWMWnTp3q04fllfghpssRwEwoduqpp7qrr756vZs5hAIbsCLnBbG/3377rc93u0dWJwafByPupbhuG4Tf3B4u61ohRP1pbQEtF+4Ojo17LvTJqmqCYMa1m/HEjeDajXDmW9Z8totx21jgcT+XeBZCCIGIwxKK63C54hkY/xy6B5sbN27HuIbH3x7mvghCxvyWMhlWKSDYseRidf3GN77hbrnlFm/hJb2luqqbaGZ28BD7BBhW5FJn47bJxIgXXHbZZb4csqzl5GPWd7OLwaRs5V4rhOh4SEB3cHDd7t51Cy8a6wnjiVtTSJtwPn/K4/5b1lefvp+EsxBCiPVgPeXTUszubN8VLgfEKGGEws/EIWLVxkaHHHPMMf7ec+fOdQcccEBytHYw1htLNLNwH3LIIX6MdJaIxhJsn9MybPzz/vvv79fAMVyqv/Od75RtGbbJxIgblucJEyYkv2yMxTXru9mFoLMC9/xyrhVCdEwkoDswfGaKcc/jP7N7cqT+1FtI+zHOv3vKW5wRzr859wAJZyGEEJuA6zGijU9OlePWbPzkJz/Z5HNPgEBGuIXfcwa+f4xVGKsuVuJqTB6WF9KJpR2xm+VSjpWZ8cImWplNHEszabTJvRClfIILcMMu14puk4nR0YCre5b1+dFHH/Xr2JIfQhzS4vHyyy8nWy2dA4VmFRdCCJCA7qCY6zbiuRHEY62FNOO8TTh377KFLM5CCCEyQUhh+eQzVuHnpUoFSy3h4F4cf2MYcQjhp5MQb3xzGmGN+3Zs6a0UBGT4SahCS5YFGiszFvWRI0f687CgA2m0jgbyDCs2vzHuudyxxSboyQ++oZ0Fop44ldPRgejmWr6jzURvlbjqCyE6BppErIOC+zKu261pfS4E1nEELwK3ksnGnlv9hrt57rM+PMZ5a3IwcfgZ9yZbQgixKS//c4m77zfj3O4HnuR6jzg5OVo/Hv/T5e4DW27bKveuJvVMx72/GOM6d+/rBn7qguTIxrz9xlo37xfHuX0++T23w+5qywoh8jPjewOSrQ1IQHdAav3JqmqC8L3zgX+659a8UZKQlnAWWSCg77x8RLInhBAbsE8lYZHkE1OtAZ+4uvLKK/245LYM6cAKXWuLLi7klFehWdKx/mPpl3VZCFEKtBnTBLRcuDsYCMub5q50Z47Zs00ISly7z/9SXzf+qN3d/EVrirp2m2v6hMmL3NZbvk+u2kIIIXJzwgkn+HVrfc4IMci46759+yZH2iaWjkJjkqvFOeec4wV0IXHMOHKJZyFEtZCA7kAgLidNX1K3T1ZVk0F9tttISJ944YMbCWkTzghsE84njd5NwlkIIUQuGG/M56ZuvfXWiiYNqwQ+a8WkWVmTZbUVLB2VjB/PA2Ow+X7zzJkzkyNCCFF7JKA7ELhuIyjr/cmqamJCGgv6X5e+5E6Y+KD79rWPrhfOuKVLOAshhCgFJsw6++yz3SWXXJI5+3Q9uPvuuzeZlbstUq902ARltRbqQggRIgHdQeDzTYx7nnBcn+RI2wYLOiL53XfXuReb3nLvvrfOT4q2c9ctkzOEEEKI4uBuzAzMfCbprLPOSo6WBp+ewhpaKbNnz3aHHnpostc2IT+ZTfyzn/1sckQIIdoXEtAdAO/efGvjfLKqEkJX7edXv+n+698Hup+d9RE38cv9vUX6c+fdV9PvSAshhGhfIJy7du3qfvrTnyZHSufeeyuf3R8Rzrhh+7xVW4Q0MB55/PjxGnMshGi3SEB3APiu8qDe2/kJudoqCOdfz1q+XjhfMK6fd+U2izMW6TOP29O7cEtICyGEyAOzM/P9YsbQVjLuGcsxY37LhXjw/Wdmkm7L45+ZORy3aibtEkKI9ooEdDsHEblg6Vr3xVG7JkfaFqFwRhibcM6aBC1NSDP2WwghhAjBzfiiiy7yorWSMbTXXHONF+FDhw5NjpQOgnP16tWy2gohRBtAArodwyersD4zc3Vbc91OE86TThuQe/bwUEgvXfmq/44brt9CCCHEggUL3Gmnnea3jz/+eMf45XKXU0891YcjhBCiY9CpqalpXbJdkMWLF7thw4Yle6ItcP4vH3d79Pign5W6rYBwnv3AC/5b1Tt32dKP284rmgux9JlXfZiEzSzkhFsJCPLW5s7LRyRbohQoO+WdEB2bIUOGeKtxNRk9enSrfT9aCCFE9aHNOON7A5K9DUhAt1NwW563aLW32rYFEM64mmMlrqZwjqmWkG5tESYRWD7KOyEEluNqw8RZV111VbInhBCirZMloOXC3Q4xkdgWPlmFcL530So3YfIid/Pdz5bsql0q5tp99en7+XvzYMi1WwghOhZMdFXtReJZCCE6BhLQ7QxE4WU3POEtq438TWRvcV6ydr1wPnPMnjUVzjES0kIIIbJgjLSNcRZCCCFCJKDbGW3hk1UmnG2Cs3oK5xgJaSGEEDHMyn3JJZe4wYMHJ0eEEEKIFiSg2xG4QrM06ierEM7Mqo1wJo4I50F9tkt+bV1aQ0g/+8LqZEsIIUSjsXbtWj/ZmBBCCBEiAd1O4JNVCD5coRvtk1VpwrlRLeQmpH9z7gE1F9LX/OrWZEsIIUSj8dBDD7levXr5z13hyq1vNAshhAAJ6FbiS/8xyS/V4urfLXOjBu/UMBZdCIUzcTv/S30b2rU8hPHjaUKajopqsHrNS+7qX9/q10IIIRqPWbNmuWuvvdadcsop7rbbbnOzZ89OfhFCCNGRkYBuBcb9x2XukaUvuQf/vtad+PVLk6PlwyerEHl8lqkRMOE8+dan1gtn4tZolvE8xEL6ixc+VBWL9PRb5rhdtn7Xr4UQQjQW99xzj1/PnDnTj4d++umn3ahRo/wxIYQQHRsJ6Dpz0jcudQuefMXtsNdot3O/I/z22NMuTn4tHftkFbNut7ZA9ZODXbVovXCeNH5AmxXOMSakb554oBfSUIlF+vrp/+M+uf2T7rqptyRHhBBCNAqPPvqon0AM8Qw333yzO/TQQ/22EEKIjo0EdB058esXu0XLXnM77LmhF3vnfqPdwn+87o4fX7qIRsgh4o4e2aPVZrEGhPP5v3zcfz5r+ICu7Uo4x5AmhDSEFulShPQf737Ibf72Wndkt2fcFs1r9oUQQjQOd91110YWZ9y599lnH3fNNdckR4QQQnRUJKDrxNjTfugWP/2m67bn4cmRDezcd5R7dPkbbsypFyVH8sHY4u5dt2g1120TzudPedzt27uzn8G6vQrnNMwi3b3LFqlC+rLpT/g8ipl6w+/dRzd/3G9/dMsn/L4QQojGgfHOI0aMSPact0YfddRRbtddG/MrF0IIIeqHBHQdOG78he5vK9923fp8IjmyKd37Hu4eW/GW+/zJE5MjmzLhgh+7nQce7df2ySpct+sNohCxiMUZ4cz44I4knENIM2m/8/IRGwlp8mjeotW+c8FcvmH5My+4/71vkTus67N+n/Wf//JXf1wIIURjsHr1anfkkUcme8498MADmxwTQgjRMZGArjHH/ttE98Sz77muvT+eHMmm+96HNwvtd/01MdfP/KP7+9I/ufm/v9P9bclt7sZZi+o+7pnx1iacEYsdzeJcjFBIT5i8yAtnFqz0xtQbb3ef2Gm1e3+ndX6f9ce7vuCm3/wnvy+EEEIIIYRoXCSga8S6devc0V/5gVv2omsWz4clR4vTfe9PuCXPt1xLGMbtf7rTfXns/7ndP/yK+8oJj7kXl95et09CmXD+/pTHJJxzwDjwMG8WLF3rZ0qHac1CGbftkEO3/Ye7Xm7cQgghhBBCNDwS0DXg3Xffc5/78gVu+er3uS57lD5r5457Huae/OdmPgzCgkWP/8MduP8qv82a/VrDeF4J59JhbHrotg3k40+n3uN6bv6K67XVK8nRFtjvsdlqd/Ptc5MjQgghhBBCtC4LFixwnTp18ovYgAR0DXjf+zZzy55+1n1wp4HJkdLp/KF93ZPLn/VhwfP/fMvtvGPLBFXdd3jD79cKxB+CDzfkrbd8n4RziTC5GK7c8XLXHb9zh2zxWHLWxnxsm6fctN/+IdkTQgghhBCiPnTt2tXdfvvtyd4G+JTfJZdc4idSFBuQgK4Rwwf3d682PZPslQ7XHrh/v2SvWTTvuKV74cUt/PbzL27ZvL+5364mJpxPveKR9cL5pNG7SThXgUf/tsz9fenTbuT26ZOFcfyxx/7uzxNCCCGEEKJeFJokce3atW7IkCHJngAJ6BqBgH7v9eeSvdJ56+Vn3UcP3CfZc25A373c/Id28Nv3PdyteX8nv10NYuHMd5wlnKvL1N/+wR3aeXmyl85hXVa666f9LtkTHZlLL73Uu0uddtppyREhhBBCiOpyzz33+PbGEUcckRzZlIceesj16tXLt0k497jjjkt+6bhIQNeIoR/p695Y2zJxVDm8+fJKH4Zx5McPdj+/fqB76h/buJ9PHdi8f1TyS/mEwhlMOO/cdUu/L6rD22+/46b/7i73sW0KW5f5/Ybb7vXni47NWWed5ZYuXeq/RSuEEO2Fjt4xiEjp06dPstc6EAfKobXjIRqDgw8+2I0ePdoddlj2hMezZs1y1157rTvllFPcbbfdprZJMxLQNWKv3ru699592739+kvJkfxwzbp33/FhGCcc8wm3d5/RbtinD3d9ex/q98slFM7Pr37TC2c+iSXhXBum3TLHHbDD26775i1j2LPg90EffNGfLzom1rB58skn3ahRo9ySJUuSX2qDWbrbGtOnT1+fT4WwnnXWbQ1ERt4GruUH5Vkr8uZ5o0P8i+VVtfKynOerNeqs3bMewpavi9D4Jm8sf6hb9aKU56pahPXgjjvu8O923vW1znfSmRY2caAc6KRt9Oc5q7w4bnmaF3v261nfakGe94rVrXjBcpz2bqGtMXz48GRvY+z8mTNn+vHQTz/9tK/DHR0J6Boy7IB+ZY2D5ppBA/ZK9jYw6fvfdM8tvMld9v0zkyOlgXD+9azl64XzBeP6ufO/1FfCucZcP/UWN/L9i5K9whza+Wl33fUzkz3RHrA/u0KLncefGJN10DiotXjuCNCzPn78eDdu3LjkSO2pdyON+x1//PFu2rRp7uyzz274BrFoPEaOHOnrz+TJk1Mb19XGGuvUV+5L/e1IXHXVVV7E1jvfQ3hH9e7d2+2xxx7JkcaDPCFvpkyZkhwReeG/75xzzvHbc+fO9R0mjzzS4m1KvQv/n/jPoDOFa9J49NFH/QRiiGe4+eab3aGHlv6FofaGBHQNGT54H7eujHHQb7/ynBs1ct9kr3JC4fzXpS+tF869d9k6OUPUivseXuzWrl7lDujc8gmyYnDeS2ua/HWifYA7Nn9etgAiOTzGHxiNSRoKnE8Ds633kjcKNFahveYnnS10EmBZsM6XaoL1h8a2iRwa3dW+R7lgxWMpBQQDzxzPmWipP7hvUn8Qc/XqbOI+1FfuS/1tlDpVTayDlHe77dNRCrXKd95zdl9EEQKU7bSOtUbvpJ04caKvI2nCjve6/Z+KdLbbbju/tvxDAFM/4nf4/fff7+sin6u65ppr/DHqqdXVu+66ayOLM+7c++yzz/pzOyoS0DXEj4N+qfRx0G9F45/LJU04TzptgIRzHZk6Y5Y7dNvSvtl9yBaPu+un/U+yJzoC1qi3PzoaNjSsGg3+dPO4P+Y9r140an5WAyxZ1kmAKGS/mpB31E0a+UCj3O5XCKxHNNyLWdZo2HOeOoxaB7OGAs9IvUQV97FODOKQp041CuZVVAyeGxZEoO2Haa5FvhOW3RehROcE27GlmWONDvkTdnTlfaeIFubMmeOFcczJJ5/s1qxZsz4fO3fu7EUxHT3HHnusP7Zs2bL1ApwhFyNGjPDbgDX6qKOOcrvuumGYaUdEArqG7Degj3vlpSb3ztuvJ0eK885br7tXX17jry0XhPNNd6+UcG5l1jS97G74n7nul//o4Y7+68dyL79+tre78Y77/PWivqxatcqLP/6kEYD0yNYL7hkusaCwYzZOmiXN+ma/hUteMZsmfAs1WsK4sIS92gbh0eC0fGVJiw/HwrBsKUZ4bpxnFndb4vsSf+JlDWJbYuJ02lKuu3TePIE4DfE947jHZcCxPPUmJjw/LW5Z9YJz0+pBnA6WtPwjruE5pC/GRDeNPhY718LLkydp4caE5RPnWVo67b4xFl9b4nqaBfewa/LEN4S4Eec4P+M8r9YzEhPWn3Cx+4d5yxKmz/KLuIV5EOd3DOcSThh2nB4jTneYL2nlaHHKU3ZhnON6Y8TlYufZfeLytviyTiNOT1o8uUccH4tHmP6YQmUQp4Mli6x7xfmdJ8y0Moqxc2xZuTLdoBWewxLXBdKfVl+srGyJy6ZadTxPfUoDy3KhicEMPl1FhwodFt26dfPtoC5duvgJwyD+vNUDDzxQ8JNXHQUJ6Bpz4P593Wtr8o+Dfq3pGde/357J3sZM+P6P3c4Dj/brNBDO9y5a5YXzvEWrJZxbmS7bb+vHrJe7cL2oLzNmzPAub4Cl7ZhjjvHbtcT+SM1SwMKYJVxmwz9c4BiufpxD/BAP4Tn80Ybh0PvMUi3rBj3R5srFvcw6aQt5xx8859HLbdCzzScw7DziHjYUuIbw7HfSgPWE7ULYOSxYecgfa/zQMLG8sgXiBgpxprfdziHMsJHC+WE6Q2tSJeMHi+UJcAw3RjuHsgxd6Sj7MO6cT3rixnOxehNDPDjHwiUO5sKdl3nz5vk1XhXEx8Z7WpjkI3k9adIkfx6WM87jPjZmj4WZX61MDfPYsPpt53I8b54Ug/I55JBD1odRLM8KEdZT8oA0xo3tGPKL58iuIT7FrokhzgwLsXvH9cfKhfTZOTyHLCHFnpGYYs8Mv4d1n/JOSx9xs/hzTp5yrMZzVYwsyx5YvljYCBjiFEIawnJhsfpF/hA29T5k6tSpPt/T3Jl5Psgr8tnCO++883w6KyV+N4OVE/GNn1fe3fyfxc8smBcQ/7Mh5CfXQaEwC+VBDHlMvls45AV5FGL/vWnvpTD+XBv+l1A+nMPCbxwjjmH41arjeepTGnT+Y2UeMGBAciQ/iOgLL7ww2ROZNDU1rcuzNP8ZNpedKJUrrr5x3Uc++8N1nzj9nlwL5178k+nJ1Ru4bsad6/7l6H9Z9+Rvt1n36c8c7veNl197e909C19cd8rl/7fujJ8uXLdkxSvJL6JWUFatSWvfvy1TKO+uvvpqWgjrl+Y/yOSX6kG4zX/Syd66dc1/vKn3iY/H10HzH7lfoPmP3J/T/Cfs96G5YeCPZUF44e9pcSE8zrGF+1i4bIekHSc8wg1JSxvXGnbPOHwj7T5sx+HEcF/LLwjzz4jzhHiG+W73CfM5JE888uRJvA9p6Y6J48v5hepNGmnXxPe2MorzgftzPAwjLb0QH886L4ti6TDy5ElI2u/xvdLiyjVca8T7RqF0ZuVrsTjHED73CYnLMM4XiO+flsdZ6TLicIs9M8Dv9sxkPUOF8g3Sfo/zIU++pKXP4mRLWlqy4l0sv4A8trhbfMJ7sB+XlZEVfpwfaWUZpz0m7RojK06F4hrnv+WZpTVvmFlpNtLiHZcPcUlLW3ivtPuk5Rnx51g163jWOcXSDtaWefHFF5MjGxgzZkzR68UGaDOm6WJZoGvMgfv3c2+9/GyyVxzOHTl0n2RvA7fPvtN9ecT/ud13fMV95ZDH/D4W5wVL1roJkxe5m+9+1p05Zk9ZnIWoAMb/NP95+e3mPzL/2YZaQ093bPEBeq+b/0CTvXSwVph1mW3iTC+9Qc92cwMh2auM5oYB/7j+PsuXL/fH2A7p2bOnX2e5yhlx2ogjcTXM0hCHXwg71+IG9ORjYbCF3v1i1vjddtvNr80CgWUqtAaZ9SSPFaQU8pR3Wv5i6QjTSBhYCwtBXmXlg1lIsj5pkgeeIeqKjV8kTqQvhnofW3rSziuVcvKkGIXyrFTidOeB56HSNMT1h3zBmhXmVWylSyN+RmLyPDNY1sL7QvjsplFOvpX7XGXRLGZ83U57/nGZhaFDh/p1IbC0hunHAm1pM0utvcvtmbTxqTGFLOKVgiWbuBHH0APD4mp1IaRQXR07dqwvD7uePON88rPcMNMgzsXcl7mfpS1cqkWldbyU+hTDxF+MVcaaHIJ7Np4tzSI6OSLKRQK6xgz5SD+36oUV7r333kmOZMM5nMs1MYse/4c7sHfLTM6s//bMO144/2b20278UbtLOAtRBfizYXIXGkg0lu2zDW0JRKL9YZOGak8qVSvChkweoVuMLFfAcqDBZ3FDcBRrkNcLGmjklaWPhYZmR0Z5UhqXBG6/4VJpB1GhZwaRwPMd3q8jQQeP5YmlPxbAvKuox4CQ5vdSOhSrBfWA+NFxYJ0tsRtyKRAez6N1qtBxGg73qTfkq5VBuISTl5VDa9fxBx980A0ZMiTZ28DPf/5z79r99a9/PTkiykUCusZ84P3vc4P22cs9+scfu4WzLy+4cA7nck3M86vfcjtv94bf7t75Dbfm5XfcF0ft6oXzoD4tM+UJIdoeWZYtettLafjTqAkbZCylitA81hrIskCtWLHCr3v06OHXeTArQBz3SiH/aBxVKgRoxIYinKU1GrJpUL4IoGpiZWdlacSWk6zz0siyHhH/MC+zzssirRxqkSdplGMNNeJ0txal5ndeij0zPOuMQW5UilnYs8iyZMd5TLgI5EJ1YMKECX6NFw35WegzV4ST9q6P3+VZ5+XBZvemziDoLe5pFlXuW8iTBMGM1Rx495tlvZIwY9LqdlwuleRHMapRx/PWpxjqF/dnDocQxkXTCULds/9Fe4/RqUNdo+OZNQvH+M3GYYuNkYCuA3dM+2HqJFFpC+em0b3blu6Fl7bw28+/tKXbxj3vRgzY2DVDCNH2MJe20D3OGk2l/AGboDGrjy2l/PmZ2y73B0R5mkunuRjyB2vwR4vFt1jDMMbOpcETxps/9kqgsUXjjHiB5WmpEC/yIIwbSyNAHoWuspQHdakSKA86HihLg7yj4RXCeeRN6HpPfNLuT4OZvA8tVxZXEwqQdl4xoUoZh9QiT9LAPTSsXzy/cR4ZYX3hPOLDc18JpLPShq3ltz3vQHoIuxKKPTNxvWm0Brq5zJqVlDwhzsUw62oodinv+L3DsxMe45y4HsfPob1z00j7D0krQwQV59nzRbmHz3kaYbmRD1xvQpZ3PXU+fD6tLAtZcBHMpJf4kkb7D4Byw4yJ3yWEF/+XWb6F/2NQ7J2Th2rU8bz1KcZcv/v1a/FmRThz3X777efzN/xknHXmcYw6Rh6zZuEYv7UVL7Z6IwHdRhjQby83f8kOfvu+pd3cgL128ttCiLYNf5L8idNosIamuR4XajTFWCMktvzwBxk3ELIgLljvuD/xoMFB3NKwsC3O/NFzbfjnnBeutbGFtlQqEGgI0DgjbOLHWL5yLJPEg+vCuNEIqVRkVAMaNpSPlQGQ5kohXMs3FhqC1KsYxtLRELbz6PBJuz9lQfmGoopGIHkZNp45j7wOz6MhHJ4TYnXNzoVa5UlMXL+wqJHGGM4h7yw+POfsmwWoNbFyseedhfRUapUr9szE9YbOCO7bKFDfQpdl4pb1Howh78L6h7UwrhfU2/D5CmehDjHhlPZbCHUpjC8Lz2xc7/k/ISx7vngnpj3XIYRrYRJnrqfeAOmgnMO0kH7KuxDkL3EjvrFlvdwwY4hjmFbCi8Ow/17eRXYvFvIu652Tl2rV8Tz1KYQOA8oVEMxcc+ihh7qHH37YXxf/P/NMFuos4LdG6+BqGNJmFktbNAt368Ks25/+3CdbZuFuXoezcIv6o1m42y7tNe+aGwubzC4LHG9urCR7jUdzY4lWTbK3AY6npaeeNDc4fNyaGzDJkRbsuBCtAfWR+kc9bDT0zFSPZnHr84y1EKJ10CzcbZwTjvmE23vgaDfsgsNd3wGH+n0hhDBs/HLYm8w2vevFZiOtBFzD6OUO3W5LwcYbxtdjnSjl26y1wMagmUucQQ9/bN1pTcg7yiB0xW1UiGc9LBptKU9KhW9nU/9K8VCpF23lmWkL4NGB1bIRvBVE+0QW6PKRgG5DTLrgm36c9GU/ODM5IoQQLZjLGg0uhAML29OmTVvvcteIIAJw2Qvddlk4Frub1RtzjQxdXFkQ9hoXJloLOsVa+9nIQs9MdUC44ALMEAYhagUu4oXc1flNz206nTBDJ9sFWbx4sRs2bFiyJ0TH5vAz7nV3Xj4i2as/rX3/tozyTgghhBAdHSzQjNfOEtF05DCHSkcW0bQZZ3xvQLK3AVmghRBCCCGEEKIDIQt0+UhACyGEEEIIIUQHwsZAY2VmvgjmNGHNwjGNgc5GLtxClIFcuNsuyjshhBBCCFEMuXALIYQQQgghhBAVIAEthBBCCCFEO2TBggXrZ0MXQlQHCWghhBBCCCHaMF27dnW33357sreBQYMG+c8CDh48ODkihKgUCWghhBBCiDrAd8+xBDJZj2gM2ouFdvXq1e7II49M9jZm7dq1bsiQIcmeEKJSJKCFEEIIIaqECbJVq1YlRzbA7LYwYMCmk9KI2kLnxbnnnpvsbaCtW2jvueceX98KzZb80EMPuV69evmZlTmXvBBClI8EtBBCCCFElUCQrVu3znXr1i05sgET1X379vVr0YJZgGsp7Oi8uPDCC5O9jWnLFtqDDz7YjR492h122GHJkU2ZNWuWu/baa90pp5zibrvtNjd79uzkFyFEOUhACyGEEEJkgGXPBJ4tfD8VN+zYyswxfs9y0X7sscdcly5d3OOPP+7DYNwqFsSOzosvvujX+++/v19XGyu3LBrJQmt1iCW2mId18ZprrkmOOrdkyRI3fPjwZG9jrH7NnDnTd+48/fTTbtSoUf6YEKI8JKCFEEIIITK4/vrr/RorH5ZlxN7EiRPdxRdf7AVNKKLPOussv84SM/PmzfPr3//+91709O7d2z366KP+WDkgtgq57rYVsABDVr5VCi7alF8WlVpoEdyI72p0hlCHzJ38hhtu8GvD6uL48eN9XOHJJ590S5cu9ZboNKhfhId4hptvvtkdeuihflsIUR4S0EIIIYQQGZgrtrnIso9guuqqq9yDDz7oZsyY4Y8DYgayxMycOXO89Y9rAeFz0EEH+e2OzP333+/XWflWKcuWLct0ca6GhfanP/2pO+SQQ9y3vvUt71mA5djqQjlQx8aMGePrB2PqDauLJp6BvKNzgPPMKk3HinlB3HXXXRulh86CffbZZyMLthCiNCSghRBCCCEyMIEVW0fNzReLnmFiJgt+P+mkk/y2hWuWwXqCuMJ93NyBSQuCjzghADkWW1M5HysrcK65EyPEsMIjGjmHxfYtbGAMsv1uk6kZCxcu3GgSL8IMwzJsgrb4ej7fZPFmYTxzGH8sylnW7WpYaK1T5YEHHlhvvUa0Eg/Ln1JA5F500UV++8Ybb/RrIP0MAQjrTOfOnf35Z599tjv22GP9MToMtttuO79NfEaMGOG3gbQeddRRbtddd02OCCFKRQJaCCGEECIDc7HOYx29++67vaUTgWcCDqHJNuJnzZo17sADD/THceceOnSoPx6L1VqCoMP9HMskLum4N+Mq3NTU5KZOneruu+8+f565mwOCmbhjZYVzzjnHW9HpLPjZz37mTjjhBPeFL3zBffvb3/bC8YorrnCf/OQn14fNPXHT5lNLpNmEuIHIs0m8TBzfeuut/p6MGzdsmzAM8u9Tn/qUd6snPXPnzvWeAS+99JL/nbhjye3Xr9/6McW1tNDusccefrIyXPQvuOACH78ddtjBC2zSVkxMUxcQuYTDOnTj/stf/rJR2oFPV5HuO+64wwt5wkdkm5U6/rwVIr/QJ6+EEMXpUAL6vffWuS/++yV+YVsIIYQQohAIrNA6WgiEC5ZALKomuBFS2267rRc/hGNuuHzKCrH2wx/+0Iu7ekF6EGFmxWTMLfFmAi9EscXPLJjApGdg8UQIIvAAcXreeef58AiL3xCQln7CRjyboKODAWEcguA1cY7QDF2UyTuDfCU8uzeQr2CWbu6LsN9ll138PnANHReIfKiXhRaRSp6SR3RQHH/88Rt1CKRBx4UJ+q9+9asbuXGzLjTbNlB+WbONCyGqQ4cR0M//c4078oRz3GPPvOMW/uNtv80xIYQQQogsEFihhdIwURMKGoQL1kATMFgTsYwiLhGFWP8MsxwiOE20FoKwzEXZFsQ6Ijw+XmhiMdyTucYsvYBF0jBrOFZYY9GiRV6Ehq7DgEs6wjXLOv/www97N2ybXC0Nu1/ciWAW8PCezJYdl4WNIQ+t2lhj7TrENumjI4Nj9bTQ4lpOvJgsbvvtt3fTpk0r2lnCOHkT9Icffrhfmxs3dbFWE60JIfLTIQT0osefcp/64rlu1Ts7ui67f8ztuOeh7tk3dvDHHv3bsuQsIYQQQogNIJKxloYWSgMRCoXGPCMszTJaKYSF4A4Xm106Po6AzALhyARVWENxaY5dik24hqIYURe7DlvefPrTn06ObAqW5ZNPPjnZawHrLwLWSBPKwD3jvCXP409dcd3VV1/tJk+e7DsOik3eVWsLLfli48G///3v+/gxczsdFtSFYp0lpNG+Ex66cVNOWKOzOiuEEPWj3QvoP897xP3LSee5LXbcz22/W8u4I9hpj4Pcuu0Guk83i2jOEUIIIYQIMXdbEzQGYoZxxAi8WPi1BRBzWENNdIZgNQ6FK4IUURe7Dlve2JjuGBt7HFtMTUgaaUIZsG6H9zSLeZoFlk4Bxj5TLgjOYiK62nBfxkwzjvuYY47x7uF0HmDNJm55PAwAazzW6tBF3dy477zzztShBOSLTaBm47qFELWlXQvo3/7P/7oTv3aR22nvUe6DO21wRTK69tzX/3bCaRc2n/vn5KgQQgghRMukYLGgga997Wt+jQW4LYFYNoszItY+xRWCm3AoXCdNmuTXjNkOsbzJEoc2bjoEsYfVeuzYscmRTYUymHXbxDJxvvzyy/126AKNYMRNGrDMYqnlupUrV/pj9YL6QJyZUA1XcVzW4zqTh3D8s2Eza+MKHv9GRwGeBHyCi7oYl5EQoja0WwH945/d7M65+Ffuw/t/3nXeqU9ydFP4rdcBX3Df+eGv3FVTfpccFUIIIURHBzFpVj9EHGINKyPHmYyrrVmfEavf/e53/TbpQQSH7tQGVmhAtIVpRACbJRjrappF1GDcNNgs5lhXCY8ZvEM3ZAQv8LvNkm1wLfFklu/Pf/7zydGWeCEeiSdu0tYpgJUWwonH6gF5QmdEJfWBNFx77bWblAcdFLjck0/xUIKf//zn/jfui2jXzNpC1Id2K6D/+2c3uZ36HuE+uH2P5Eg2nNO93yfdpMm/TY4IIYQQoiODSMN1Fqsm7rF8igixhhUQq21bdN3G6oz4t/QwWRYdASF8ioo04xbM+GZckBHKJ554olu+fPl692vyIB6PHIJrNuKO7ypzv3HjxvkZx+Pxx5zDZGh/+MMf3Omnn+6Pkbe4dZ966qlePGNdxRKLuMRlnHhh4bXvNZMW7oEF+Lbbbqt72WDZ5/55Fps0LYZ0Ut/4/rNZ1Y3Pfvazfh0OJaCzgXOtfmaFK4SoPp2amppyfc9p8eLFbtiwYcle4zPum5e4R1/o6rbv0T85UpimZxe7Xtu+6H57zXeSI7WDnkpcbnhRluPiUyk0CvgDxc2oELhG8afGhCT1wu7ZWnmTl8PPuNfdefmmk8rUi9a+f1tGeSeEELUHUcfkXjbbtag+dHJceeWVsjwLUSNoM8743qZDI9qtBfpjwwa5d199JtkrzptrV7hPHfqRZK98EMf8aYQTWLDNsUKflWhEcAdifBOCu14gnpnYpJHFsxBCCCGyYTwwhJ/CEtWFtiXGhqxJ3IQQtaPdCuiDDxzoXl29PNkrzutNT/tragHuXgjRQp+VaFSwVDNLZ9ghUCsQ6uPHj99odk4hhBBCtC1shu5i3zwW5cN49kKTuAkhake7FdB9dt/FbbXlB9wbr7yYHMmGcziXa6oNVmd6CIu5SzcqWIJx4a6HRZgJOFiEEEII0XZZuHChX9ts5aL6MAFcoUnchBC1o90KaPjosEHulRxWaCzVBw+t/tT/jOfl24kI6Cxw7bbFZrYMsW/72VLsG3+czzlYc+0ajqXBhBNh2LGVmXDC34u5cnMOaQgn07BrwvjEruzm4h4uBtvxfe38tPwSQgghROvCRGF0vut/unbgIWiTqAkh6ku7FtCHDt/XvfNy8XHQ615b6UYdUvn455AZM2b48bx82D/LeovrDX8wLMwwycRioYhFJCJ+7RyEOGEWE7Kc06tXr42ui6/h2MSJE9efw2yX4fcFEc/Lli3bKAxcuYv9GZIGZtrkGtLONSaILRw6FawjgPSG+cBCXExk49JNGCHkLcjVWwghhBAdDdpOtKcOOuig5IgQop60awHNmOaXXvxHspfN6ueXVX38MyIWwm8dxvDyM+xD+YxpAROY4bhphDhCOxaUMYhOJgAz2KenMiQek43oJT4m4Lk+dKfm3lzDJywKQfxM2JJ2ruH+FhbhIJD5vIXtI5pDDjvssPUu72PHjvXrULjznUTCFEIIIYToaPD9Z9pXbfFTakK0B9q1gN6h63Zu110+5F5dsyI5sin8xjmcW01MHGe5T8eYldoEKtZfXo4xu+22m1+HlupiYI0OxXoaPXv29OuVK1f6NYRu1yyEQbyqTexKTueDxddE+JQpU/y+9bqasBZCCCGE6CgMGTLEf/t55syZyREhRL1p1wIaDjt4kHvygRvcwtmXpy78xjm1ABdmxF4xl+tGBBdqLN2ha3WaoK8ULMsjR470n66y+2DFDjn55JO92zfiGfdt4lHIsi+EEEII0R554IEHvJeerM9CtB7tXkD/4Mx/dc8tvKngwjm1AJGHMMwzdjgmy2psFmqzWNcKXs6xkK0FpAdBXGg8s7mjI55x30ZQCyGEEEIIIUS9afcCurVBGDJeN54grBg2Jjq0XuPqjHtzPYQtrueIVYN4pAn6SsElnXBJG1gaY8hDc+22vBFCCNEx4L+UIT42P4gQQgjRWkhA1wEm0MLKWooLtE2uZbNYs5irczhBWK1ggjHEqt0bmPyr2lgHA2kL0xhjY56JQ62t70IIIerPNddc48d3pmFeXAMGVP+Tk0IIIUQpdGpqatp4CuQMFi9e7IYNG5bstU1eeLHJ7bTD9smeaEtgvacDAnFdyN27Xhx+xr3uzstHJHv1p7Xv35ZR3gnR9li1apXbYYcdfMdue+tE7dq1q1uzZo2fN0Xze7R9FixY4Pbbbz+/jSFECNF2oc0443ubdtx2KAv05Cm3JFuirTFp0iS/bgTxLIQQbRWsvOZZVGypp7s0E1dyTxvOE/PYY4+5Ll26uMcff9wPMUJ0Zp3biBSyrt96661+3a9fP78WbQPq4O23357sbYDJvRhqN3jw4OSIEKK90WEE9Guvv+km/+pWvxZtD1zZ9e1nIYSojFNOOWV9w/7qq69e//UDW1588cVWedeed955fp1lgZ03b55f//73v/eTXOKR9Oijj/pjbQHyndmT03jppZd8erp165YcEVlg3aWjpdSJWWvB6tWr3ZFHHpnsbczatWszO0yqDUI+79de6HSyDjI6dYQQ5dFhBPQf737Qddmyk1+LtgcNO8aSCyGEqIyf/exnfv2d73xnk8ktEXH/+Z//meyVj1mUWWIrnR1nQRDBihUrCs6zMWfOHDdq1Kj1/wO4ch900EF+uzUI02ALgilN2BWzri9atMh3amDxRwxhYcdlXWwKngjQmtZ6E6GUaxYPPfSQ/5oKwpZza+U9x/OL+3/eT1rRQXXbbbf57dZ8foRo63QYAT17zl/cPls+72bNvjs5IoQQQnQ8aGyfc845vuGdZrlCRI8ZMybZK4/rr78+2WqxGodYA545Lazhf/fdd7vDDjvMb6dx//33u5NOOslvmxAt5Tu4iFNETLUsl5YGXHXp4EXQf/7zn/df3IjztJh1nc6B2bNn+69SPPHEEz4sOhTEplCG5HcpZV9tKEc6ewrV11mzZvkvmeB5QF2hfItBx0kxSzLnhMLdJpzlPqXAcIjWzEMh2jodxwL9vw+4T+3wjPvTvS293UIIIURH5fTTT/duwzT001w5EZqVfPHB3JER4rFo7dy5s2/Ah1Y5BMbw4cPdueeeu976iuUOsFIj9g888EC/jzv30KFD/fG846BJCwL8lltuWe/ymvfaNEgDEGdAyHAP3N8ZcmSWdShmXacMfvjDH/r84FyJm8aHYQRW9jFWr2bOnOnL8emnn/beE8U488wzfd3J8j4gXDpXrEOmXO69995c8RFCZNMhBPTdf1ngdtn6Xbf3B9f6NfutCY0JGgalfBdaCCGEqBYI3ClTpvjtNFfuSqGxj2j87Gc/68Vv6MbN2OW4AY9oPOqoo9zAgQN93IgPx+Avf/mLd3E2Uc6nrEx0luLKy3hV/n+x8iJsvvWtb3mLHqK91PTbmOzYqmyfXCR+RiHrugntY4891q+5rjXEDaLN3I1ZwnG1dLCwzxKKO+LOudZBQpmHE7yRp3QKcA5r9s2dnTAJi7xnn+sILzyHdXg/jrFwDYTXW2cMcbG4Wp0Lz4vdrokHx+Py51riZPfEPd+EMeciZLM8Cqjf1FfrBLn55pvdoYce6rcLYXVgxowZfh0zceJE/0zZfS2fSh1rjXs58QnTqPHQQpRGhxDQs/803+23RYs71L6bLfH7tSJNHLPNsfjFLYQQQrQWNMSxmGa5clcCAvOAAw5whx9+uN8P3bjvuusut//++yd7LTDBFpMymRC68847/XkQT8CFEMZtlf9bE9WlwDUWJlZCQPAgRBASsZhK4+GHHy5oVQ4pZF2POwdw5yZvSFsoHmvN1772NZ8fTCLHgohn38QxM4VTT2wMMtg23gDk2dSpU919993nz/vJT37i69RPf/pTn08INoYNMIadfUQl9/zkJz/pHnnkES9Ib7zxRn8N5+D2TGdCeD9zm6eTBa644gp/PW70N9xwg48rk3dRj/CuuPLKKzc5L+zYAEQ754afRuPYpz71KS9YqWd8XuzBBx/0k70BwwlIA+eZ8GSIgM1aT70NO0G45z777FNUpFIHeB5PPfVUXz/ihXBC67MNkyhVQBPO8uXL10/Ih5cInWhCiPx0CAH9xz/f5/bf8hm/PXjbVW72nJae43rBi5QX9B133JEcEUIIIVofJgzD0kuj2sRSNUAIjhgxwouC2I0bMZLl/mogcOvhxsw9LrzwQi+6ECKIlywLYAiimA6CPBSyrsdiizDPPvtsL3BMVNcD0sMYbu7J8vWvf923W+jQCMfXbrvttsmWcwsXLvTpQHyyIHwtzpQxAo992j6EQR0woYoI5R504lg5475MGJxjLvIhdgzBDpSbWWOJB3lmcQ3zLj4vhE4COjBC6NQA68zhWgTzLrvs4veJB88L5WRW42XLlrntttvOb5OX1H2D8Cn/XXfdNTmSjXkwxDPkUxaEY+kAS+Mhhxzi13kwKzodFjYhH2ELIUqj3QvohY895d55/WW3+1av+H3W7735mj9eD7A686Kil08IIYRoJGiEf/vb3/bb1ZzZGIFhY5ZDN27EYyH313qDFRHLMC6/iCmEi4miLLiG9IQiybBPa4UdBISbZV1HVCLwDLYRTHnHn2P1TLNWpi1mIU0DEX/xxRf7tAHlE3Z6mMt62KmBK3Ao/sGux3obitgQxDN5YXXALP7UQxPYNolaWCeJgwn2ELwB4Ctf+YpfA/eIOzjo1DHxbSD0Y/dqm5069MqgE8DSbh4QHCONeAoQLxPv8eetrPyzPnkVQp4gaG2mfED08sycccYZyZEWTAyX8txa/bzooov8GtLKUQhRmHYvoPls1eDOa5K9Fvb/4HN1+ZwVf1Y0InjxZRH+uVWz918IIYQoBo1/hBPCMY/Fl/MRP/a/lQYNe0SACajQjfvxxx/P7fpcKxBsuNMy/vOYY47xxxBSCB1EUCzQYsxCaR0EIbgmI6YKdRBwjzx5nQeEdmipLLQUEuUIKsoMMZnmaoz4jMuN9k3sim95Y2UeY50Pn/70p5MjztcJCDsuGDceurYDQjkWwIDFF9dnO5fyTevgIL7hWHQToLhXh1A2PA9YxDGCmMDPgvuGnSCVwmRi1Ee7L+7wlI11wBgmhkupS3TcUI5hHSdf8ozRFkJsoN0L6Fmz/uz2+8CyZK+F/bd61s36w5+SvdqACxjuPYydyfoz5oVof2yMzeHzF8Ve1EIIIUS1OOGEE7woMetZMb773e/6NeNks4QwlsLQooXAwI0bocM3j9Ncn80KjCg3YVNt6KRGhCDMEHKMf8Y7DPFTTDSHcG3YQWAQb8SIWfTbEqQfiypxx42d8gjBohuKT+vwj13xyZtY+IbYmOa+ffv6NTArdGxZpq7EVlGOxZOxmVi2cdFAXCHs4DDLeBhfxmxDWmcHzwPtNzqMSE8922bWkYCnAvdlfDcW/RgTw6WAMM/TiSCEKEynpqamdcl2QRYvXuyGDRuW7LUNnnn2RXfYZ05zv9zzj8mRDYz7+2Hurluvdrt8aIfkSHXgTwUhbCCOY+wcLNP2h8FLkj9kvosZ9zKKxuPwM+5NtlqPOy/f1H1QFIeyU94J0TIDMZMHMSt1luAJQUzssMMOftKnQlYvrHbjxo3b6L8M920mZkIoXXfddRu5s/KfyORITECFoLexs9UEjzAsmHzKKo8rbSGwXCPubAwpkDcINtJnrr1tBcZ+Y303cF2mTUI6APG53377eUGJ2CStlDFijI6UMK1peROCMMeyi0uzYROs2v3S2kNxHAyrV2GdJP6kJ0wTdZ2OAWuTER5WV+4Tnkc9YZZ3qyMWl/i+tYY00GFw8skn++9Jpw0DpMOJDo+87v6WFiZjs/SRXow9aW1VIURLm3HG9wYkewEI6DzLvHnzmp+vtsUvp/9h3djDD19379gumyzHH/pR/3u1aX7h8xZa1yyO/br5ZZX8soHwnBCOXXLJJcmeEKIWfOL0e5ItITouzYLD/+c0N6aTI4XhfP7PuIZl9OjRyS8bUyjcZnHpf2sWXcmRFgYPHrzu6quvTvYaG/tvt/iyz386aSMdcdoaHSsv0gCkh3SMGTPG74OdQ5pJH2VPW8XKcvz48f46tsO8SSMOG7gmbPs0i1V/jDpEvFjsGGvCt/iec845Pu9DiJ+Vhd2La7ietLBwDvGOz2MdlmN4XT2x9JK2rPzkd/KNc8kHg7SlPZ/kGdeEbc+0chRCbIA2Y5oubtcu3C3u28uTvY35yFbPuTv/WFsrYvNLzVuZw4kohBBCiNbmq1/9qh83mmWNxVJolkHAuocbabO48NYqsxbGYCUErIJYKkOwJmIBCy2WWD+xZNqne2oFljYbt11s4dw0sODZ/7nFl/TwPW2+Sd3WLM/ArNrNotGni/RQvpQJn58yKPtmQebTjIdAs+jybsZY27G6M54Zbzpzzy7kDkxZh+OmzbUaq6/BpFjE48QTT/Qza1NvOEZeM5s1n6oyyzQTYMXjovF+4D7E1T7PxJhsrqd+Yo3Gy4F4x+fZWGA8LcgPJvPCYlvKOONqgLWb+ELWpHaUG9ZjXNFPP/305Gg24azphuU75Zhn/L8QooV268L96mtvuN4HtnwOoBBL75vqtv7glsle5cTu2bY/LXBFSnPhBl7W/DHldccRQpSOXLhFRwdxzLhKXKbTBB9CEQETu4cismiAV3PCJHMrfTFyBRZClA6dVnvuuecmwySEEOWR5cLdbi3QiOLnFt5UdKmmeE4D0UwvP4KZhoIQQgjRWjBpEDMu04FrVrZ4QdAyMVMMYzLDyZqqARM+IdYlnoWonCuuuMKPP5d4FqK2tPtZuBsBXmY0SMwdRwghhGgN0mbzzQMdwIjuan4rGvhcES7DQojKwTvEvB2FELVDArrK8OJifFg8joQZFDkOWedwTO7bQgghagXjdPmvybOE/0dYinHfrvZYUKza9R5fKoQQQlSCBLQQQgghCoKlOP4ub6WYVfuggw5KjgghhBCNjwS0EEIIITJB6DL55Wc/+9nkSHWolVVbCCGEqCXtZhbueSd0Tbaqy/DrN3zsXwjR9tEs3ELk5/bbb/efpDrnnHOqOvs2swXz+SCGMjFPiBBCCNFoZM3C3a4EdLXFbi3CFEK0LhLQQrQuiGdmAOfbwnyPVzNwCyGEaEQ63GeshBBCCNF4IJiZpIwJzSSehRBCtDUkoIUQQgghhBBCiBxIQAshhBBCCCGEaBiOOOII16lTJ3fppZcmRxoHCWghhBBCCCGEEA0Dw3xg+PDhft1ISEALIUSDQ+8rvbCnnXZackQIIYRoW9xzzz3+v6xPnz7JESGKc/DBBydbjYMEtBBCNDhnnXWWW7p0qZs9e3ZypHEwcc+3goVoD9BRpUb+puBOqTwRlYAQYgJBqOQ/g3qoTuX2CZ9OtPJlPXjw4OSXxkICWgghGhQb/0NDY9SoUW7JkiXJL62HWRBouEyfPt2dffbZvkHE93zzQFq4nmvrgQn8YhAfy+tGotT8soZHLeEeba3hWkr58l1qa+RT30NIO89lOZRTx6r5vJQalj07nG/l3QjvoFpAOrPGWVazDMqF+1P3yqXQM1uPTtCwLvH80Bmc9z8jDeohncqTJ09OjhSmWBm2RudQqfWqWBztvzl+Z4XYPdPqOmHzWzWxNgxL+N60+mCLgXg+8cQT3ZQpU/w7eMyYMb7tUwgLK4S6XuvylIAWQog6Ev9xpC12Ho2ESy65xP8ZNErDdeTIkW7atGm+4dKzZ8/1QqOtc9xxx/nvErc1YRhijYbx48e36XQ0AjyHNNBb23WQcqReUj/rCY1wOsd41o8//njfqWDjEUV9QXjwTPNspwmfSrFyzitoEXzxfxZLVtziukQ9qkQ8A2H27t3bPxuVQlizZs1qSA8vo9ZxpOzsvyMUupXCd/6BsrJtwKvOLMtz5871a/jGN77h3zX23uUdPHDgQL9dCoTBtbV4XtbT1NS0Ls8yb9685nZS43Lv2C7JVvUoN8zmykCLcqOluSCTX4UQrcknTr8n2WoMeD80i+RkrwXeFxznXQLNfz7rmhsffrs1af5zXdfcYPHbxId45YVrw3ciSynXlwt5y73ywrmW742A1YVi5W//O/ZfU+10cH/CjJe28t9m8c8bX+pmtdNWahysTKsF9yW8YnUJSL+9l3h2WUIIJ35vxZRyv9amUHpaMx1WZ8DiEdafvO83yjMuQ0gr22Kk3dPilhaXYnWpHLhfKf8fhcqQcEot26z8LIVCcYrJE0d7X5T63k/77yg1PwpBeOecc06ytwHaEs0iOtlbt+6RRx7ZKB4vvvjiui5duqzfzyLrGajW+5M2Y5oulgW6ytAzZxaa5nz3S3Ph+t4XepCEEKIY9M7z7rBeWKzP9bZApRFaoYhPKVZxc4tt/jP0+7wj81xPDzLWjXoR5ntbwsYWmmWn2umgvAmThf+z5sbjRvcrBJaNPBZxLB/VtH5UAnWzUitZpViZhtCO4HmodXuC9GMlAp5dFlF/7LkD+1+oZr2sVtla3CB+1mtRl7hf2v9H3ndNCOE0wv9rIWoZx7T/jmrdy95Tn/zkJ/3aWLVqlbeop7lnv/zyy97V/Gtf+5pbs2aN22677dy5556b/JqftPdnNZGArjLnnXeeb1iElY8XBw2OqVOnJkeEEI0IL3X+fGmg8ke8YMGC5Jf6Y25xtsTjpOwYgsPOSRMf9lu4kLYswvNi9ycTs7YUCseIr1m5cmXyy8ZYvtuSlhaOcV4cZh5s7JctsQCJ3RLj+5NW7hvGMy39HAvDsSUNu2cct7isjbCs0xqJYRgshGsQd+JmAsyWYkIsPj8tboQbx8fKKI04jzg3jfi8LLg3S960hefE6YnDIA4hlEFa3QwJ6whLWjzC38M42P3ja9LyGOJ7ZeVlTLG6lBWu1VnALZftOI+A82n3AG67nGf5xm9cY2GxWF3lNzvGEodt18blFOdXHI4tafU3Dcuf8BmCUvOtUF3h3LS84xq7Ln43sBhcSxmA/ZYnfVyXFi+uJ98qAYMRw3vCfMuqS2kQtzhPwviyHee7lXVeLE/jeGQ9eyF2Dh3BpJPt8N6lpDUN0sd1lcQRLJy0MNKOkb92PktYj+w5jZ+FtHBi5s2b59dxZ+59993n1yNGjPBrGDRokB/zvN9++/l8vOiii1yXLl183L7whS8kZ+Wj0nLIRZpZOm1pCy7ctVhKpTlLU92AcFUw10chROtRyIX76quv9s+wLbhN1Zr4nYG7EsdC9zBzRQrPsziaq5VdF55D/MNwir2H0s439ymOE77tA79zLAvixu/mUmZxZAldxNLCIS4s/GZxsvPCONo5WZAfXMN5hqXFIC5xGPwe52V8LI4LYYTh8Ft43xjLnzAuFl/L5zDPLB+tPoR5GF4D8b3z5EOM3TstH8J0cyzchzAdrC2ubId5ZL9bXOw8wgzP43h8D8OuTUuv5UmevCZfwzAgTltcxjEWF4OwLcy8cWDfytqweNj5YPtG1rWG5XV4jl1j+Q5xGu268F7xfhp2XRg2WBrivLa8s7wA4sExI+3aOM8tn4vlaQi/W3rsnna9pSMMIyvfOBZCPON0GlnxsnDtviFx2Vh+FMPqD9g1YT7HeVaIQve0cCxNcXwtTZbXMfHv8b3CdBhheliHZWLEvxGnuFwIN6usYtLiwX6YrqzyNeI4ESb7RqlxtPuxEDbE5QHsh/GM02LhWLwsDAvTiMNJgzRwXtYSh1kOcR0ptRyKkeXC3W4EdKNAIaVVqPglIoRoHRpdQGf9QcbH09414XvG/pzDPw37I8wi/iM14j96I+u4kfbei6/J+nNLO54WXvznGZP2e9Y9Q7hPmBdpeZNWJmFe2H2yGglWHuHvcf5k5XFWWRkWtlFOPmTlbXzvtLjYtSyWR1nhxcfT8qUQcTkYhEHYkCev0yDssM6l1UGjWHh54pBVJqSP4yyWpjTCsGKy4heWX1adjfO4WDwg635W3oXywYiPx3UF4jyLywyIe7F843eujcPPiltavsXllnXcCMMA7hHfP4Q4huWQlh9phPex9IT5UahehxAO14ZLGE6YXtsOyxmIR5iGGEuTXR/me5xfYOezZIUbl6Hlc1gu7IdpKURaPNII7xkTxom8j+Neahwtv8LzIb4m3Ld7xIT1wc6JyzEONw3OyRr/XKgOlAJxSEtDCL9nlUMxNAa6TjRXCLds2bJkbwOMX6jmuBUhRPU59thj/RAM4FmeOXOm364nuEnFLmzQq1ev9eOHswjHhbFNGsKhI3waovmPK9nblIkTJ653SwtduMztmlm3Q+ydtnz5cr+OYYzTYYcdluyls2LFCr/u0aOHXxu2b79nsdtuu/l17F5WiLSwcfEKXb6Ie7Ew4zIhb8ljg7ynDEp59xfLU4M6EsaP7TD+uM3a8SyK5fGcOXMqnuW2uf2xvk7y30h+xMRlaGkvJd/SyPo/NtLy2twVbeF5sPgXI+s5KUTe8gbeTeSnjSeF2PUS8oQVEtYlqwvkXRgu+VBtwvIt9x0DcT0+5JBDNnp+cXflOR0+fLjfzwJ3aNJZ7D1rpOVbqe+xk08+eaOZle++++71/0FgLru2EMe88cuCPOW5vvbaa5MjLe/qcePGJXvZ8Cw0Cxa/TV2M62OYznLrkg17ZD4h8iLveNzwXVMMC9P+H80lmjZAJZTzPPKuJv/juFcrjoXegxa3MM4sxKdSLL6hm7ZB+OH4Z4bL2b2rQTXei8WQgK4yvAx5OVjFAXzxeeFNmDAhOSKEaES6devmJzixP2LG5LR1eB/ZnwhpKvQpGv6wSTsNJBu3WEiAtRd4R1vD1BqF5QpHGgaW3+R93gZdJfB/QyOJcrP4T5s2LflV5IVOFOr93Llz1+djKGYaDQQc9cviylItwmfBlnrU5Wpiws0mdi02qR7PD9ew1AvEEHltbUbeGWPHjvXbdOakTUpbDRDLdl/rLM0rVAthIiXM63LqEtdALT8txbNtYh6Ryjs/7NQplXKfR3tXc31MteOYRRhnWyr9bJ2Nfz7wwAP92rC5ZejoMmhrUbft01aVUMv3YogEdJWh54yHgZde2IiiAGtR6YUQ7QveE2mNiyzrXRY0jOKGS94GMO8x+9OZMWNGphXFxLVZEGOIb9zzHU8iZhan+Hg51rxyIR00VCp5RxMG4jnO83pg5RJagqpBVl20xq0RWuIKkeVFYY1uy/9yvArS4F7cMy/UVRqoxYRWFsWsjXkoJQzSh9dINcl6HmPyvItKeZ7KfcekgRdI2JnEklccWn3HglUK5b7HyCPqHGLDOsKs/vFcsF8o7qXkSwhhEjaijPyqVkcRHZEWVt66FEOHJnGjfrOEE0DlfdfkwYxadCDQTs9jgTfSxG4lz6OllbSHVBLHPOR515ZbjngwIYgxTIT85S9/8euhQ4f6tbF27Vo3ZMiQZK98KimHUuhwAnrC93/sdh54tF/HTDj/qpbfmteVYFaccBFCiDxgfYgbDfbnWcqfgjVIrSPPlqyGIX+gYaPALCL8wVojz9yCDVywCjXwYo8c7kHnYgiNRcKIGwacV4mYKQXSRzwN8r5UFzYTC6QlzO+0hla1sQaOWZLI57isyiGtLqalBzd98ssaYZxvswOHmOth2EikbnBuaFmz+hSeR9rixmUI8QzjZueW4u6I2A7TYc9dXtKek/i5KgZhUIfCoQBcT/pi4vNKFX1p2PMYP6eUaVgPgAZyHnBLLka575g0CIs6FT6HLPYeKgYeCNSDQvUtppL3GNfgTo2Y5Z1p8O6l3C3e9qykkTdtIfZ+Jq1m9aa+klelpN3gOvLAPlNVSl0ySAdxol5TjrwXSLM9k3nfNXmI65zVMeJAWux9mkVsHSet5T6PxAXjG2kP8yYrjtXCwos/J0X5W/qt7porOZA/hcDKTDnF8KWTyy67zG/zeaqQhx56yL+DuTfhl5vWSsqhFNqVgP7NjNluxMe/4g4+9Et+O+b6mX90f1/0Jzf/+3e6vy24ze8bbP/tb0vd3F+c7h5//ImNfhNCiHrBnxWNprAByJ8njbpSG5EQuqOyYGFJaxxxPg0quyeNHhovdk/cubAs2O8sNOwLWbWxiHINYXE+f2xpHYqEQVhh2FxXqQtZXmjwETe7N8KgHIsMYYTuliykq1Z/4AZ1hrKinhB/i0elEC7hhHWRhgkNuhDKmWOWh+Rf2v2pY+QJjUQLj7rBubH1nPNogNl5pK3Q92O5Nx1Mdj734Dmy5yAPcTr4LGUo7PNAnSUMiwdhhY25PNAwD9NOuuI8h/g8xAX3qxSexzANLFjnwzIiTXbvQvWbsrXyLibKynnHpEEjnPiHzyHxoK6Z8CqE1XviXUxEhZT7HuMdS13lfmGHD8fD96c9KyGcQ1rtnFKEtN2LOmMiKQ9mtQzTyULc4rLKU5dCSAdptvhwHvEzgRc/o1nvmrxYh0ep73veRZQZcaDModLnkbK0DoOwHMuNY154PsDizcIzZP/9QDsifG+zXyhtfIoKHnzwwY06BE444QSfbxC/N8g7OpJOOeUUd9ttt5Xtvl+r9+ImpM0slrY0+izcd89fsK7f/seum7ldz3Uzt++5rt+gz/ljIWNPPmvdzZf3XLfuz86v2TfGnnrBupnXT1/39jOL/Zp9IUT7o9As3O2J5j/b1FkuOd7cAEn2RLVobvjQCkn2NsDxtHIQ1SOrrouOR3Pj3D+HzaIqOdKCHW9u+CdHBJAnvKM6KtSHuF5kvctbi7Q4tjcsjY888ojf54soY8aM8dutTbufhXvaL2e6b/3j/9zRa1e4o5tWuNNX/NVNve7W5NcWFj3+D3dg71V+mzX7xqLHn3JDB7SMlWLNvhBCtFXoQaanN7S4sE0vMj2yorqYVSa2AGFNiN3jagm9+mYRaWTMTS+PRVCIvJjHQew2PmnSJL8uxdLaSNTCk8Usg6UMc2hv4N2BdTKsF7yzK7FqV5u0ONYC6gPv5FK8GKrFo48+6sdL28StN998szv00EP9dqPSbgT0A48udaNefi7Zc+7w5u0HH16c7LXw/Oq33M7bveG3u3d+w+8bz7+41nXvtq3f3qnrNn5fCCHaKri64fLFH6+5MrFNwyDLfU6Uj7nfmSulLRwr5HoshKgudByG7qYsuHWuS1xVRQu4y+IOXcowh/YEnXe4+objznHZJ09C9+XWJC2O7ZG77rpro45m0rzPPvu4a665JjnSeHTCDJ1sF2Tx4sVu2LBhyV7jweRfKxfd4jbz31J37p3mrZ4DPuOeW3iT34dBHxvrZp9+s+veLKKfbdrKHXHFUW7B/7aMbxl06Jfd7f99quvedVv33IsvuU9982q34K5f+t+EEO2Hw8+41915+abfJRRCCCGEEPWla9eu7rrrrnNHHnmk32c2bjrCwmOtBW3GGd8bkOxtoN1YoHftso175gNbJXvOPbP5Vm7XbbdM9loY0G8vN3/JDn77vqXd3IC9dvLbMKDv7u6+v7a4bd+/aJkbsHf+T18IIYQQQgghhCiN1atXbySUH3jggU2ONRrtRkAPGTzAzer8oWTPudnb7uwG7/3hZK+FIz9xsPv5PQPdU//cxq+PPOKo5Bd+G+Z+8T/3uaeeWeV+2bw+8vDaWqgY/9Wa49RsrEMpM0yGcB3XZ41f47diM24KIYQQQgghRFui3Qjo479whLui577upu17upu26+l+tOsgN/aUjb8neMIxn3B7Dxzthl1wuOs74FC/b7Ddd+8+buSXr3B77917o99KJU0cm+AMp3NvLZggwCZJsG/LVRPSyFhLjfsTQgghhBBCtCfajYAeedC+7jvnnequ2Oej7vJ9D3Xf+dYX/bGYSRd804+LvuwHZyZHNjDp/NP8b5PO/1pypDpgpUWoMqFPI0zewzflmNiGSRKIU2wprkTok1bEebnfbxNCCCGEEEKIRqXdCGj44rGj3D33XOfuvfvX7osnfTY5Wj/4xADik9kfGfzONgvWWAjdnV966aWNzmEp1526VPiwvQl5rMTVtBQzmyMzXXbUWR2FEK0DnjX1fpe2d2yoD4sQQgghWmhXArq1ueOOO7x4xKq7yy67+GNDhw71Aprj/A40Sq6//nrXvXt3N3fuXH8MsFJfeeWVyV4LiG5rwNiS9Y02OzduPFrD0q6z72/aYtZmczMHrMhs5xmnbdfF8bLGlxAdnfgZTMPOySP+eC6rNcdANcNKgzSV69FSCnwjk/cs3jXxN2BbA3sfV/LtVnu3hp2vIbV+x9LRSp7yWZc89VIIIYToCEhA15j777/fW3wNGkKI04MOOsg9//zz/gPpNFCskRIKaBrUiG8ahHYO45b5zmhaYwarL2FMmTIlOdLCvHnzfDg0MGko9+rVa314CHjiw71w6eYY2D3DuGdh38ubOnWqXxt8Y5DOBCFEcXgX8Lw0yvcnqwHvG9499Rq6gqDkfXbIIYckR1oP0s57lHdoPToQagUdLHyTk85gIYQQQkhA14xnnnnGr+NGx6RJk/z6Ix/5iG9YmlUaGJuMW7dZG2hQI4jDxieN6zSRbBAGjZ3QYoGQtY+w464dhoeohhUrVvh1udDwx3XdQJCTlrFjxyZHhBBZ0CGG0KrlxHvFrJnVhvvwTqj3fAg2v0NrgmC2oTK8qxH1cb7XyzJfKQhoOlo1LEcIIYRoQQK6RpgLNxbo0D2SRhTCOY2ePXv69cqVK/2aBlhao4VjWZZhazhyX+B+CNljjz3W74ON1bYFli9f7tflYkLZLOOh1VsIURie26xnui3AOyV2VeY9hRdL+A7jXZhnWEi5IFjrZe0uBHGw8jTX8rYqQOnk1XtcCCGE2IAEdI0xy6wJSxpVtWxAAvc0C/WMGTO8xdoab9ybONCgs6Ua0MBCMNt9Q6u3EGJT6Lyyd0GaddjGRNsSdsQZNgaWpdB7BXFrn6zjOeX82PpZKKw0gVzIos25FhZLWtwhPi8tLMPuZ4vF3/KJdQhpiO8bXs9S6H6ETxhxOXANS3gsvnd8DYvdy9IBpcw1AXbfuCyKxQfC31nsPymLOEyWmLhM0s4RQggh2hsS0DUGyyyClsarNaDyQqMq7RqOFWpwcU/cuGHOnDnerdvAGo1r+P9v715/5qjuBI+X/wAgBl6xxGIw0sICMuJuc5GwBpslK8QIgjFBiN2wgCFiJiFrK4BhE8x1gcyiAQNDdlEE2AygoAgIlxFI5jJgIAIBhhWXQeCdV1yc5P16/a2un318XNVd1d3P/fuRytVdT3XVqVPV7fqdW/XTVEM+CNtlv9xU5bXeknYh0OB71lTrTADEWAeMeRAFXXzv08AoukzE3/nONQWq1CKyLbAe66c1tV22VYfv/dKlS8vX/DblhXRsn6CP5txRsMb7dD2aCTftk98UfkNZJ9ankK7Lbyp5HsfOxO/ysmXLqr/WY31+P+MzFEZy3phiW2yHcxVIa37uaFbOZzh/tDZgGbqMNcGxsg3SkHb9AccR+8rTw+c4dpbHOuQj+ZkXooTYV6zPxH7TwJ3P5ueEfbCvLudFkqSZxgB6EtCvkZsRbnKYIrgdJPozpzUF3LSw7LrrrquW7Clqg2PdtD8gy9P+03lNRiDw7ir2w01VWustaRcCTL4f/YKmGP8g/e7mTWkJVtIgmPfD9jceZVv8poDPR+FZ/lmCSX6LWM56BJK8T3+LOLY8MAz83pGm9PjJvy6/MQR46foMNEZaB0nPUxRG8rnYVnRficKNSGt67jhm8ikfaLELPs926/IoTWOeHsbd4LNp/3rykW1RCFGHYyO/UhSQpPuh9pwCgPScxD5o+SRJ0mxlAD1JuHHkpuu1114r3/e7eQ7cgEVNAaX6TNy0sJ30pqUOtTysy01SinRw4xrb46YoboADN7WxTlOA3ST2l9Z6S+qJmsGmQDF0DQ7B6PptAsI2umyL9SLYirEU8rTn4zvEoIUHHHBAOR+EfZCmUURNbEz8rsbycWpKa1OLojb4jaZApc0gc5Gnkcfss67F0qBzTACe5lf834M4jgULFpTzFGn94osvqneSJM0+BtATgJuctNYYUaL/3nvvlUHmiy++uEdTat5TU5MGx7zmc+nU5saaGg/WzW+4Ih0xsR4368xDus+mG32Ce/6epyVuHNPaF0k9fL8JQroWTGk0BIMEdtFkmimatM8EUYPfpVn9KJqaoUuSJAPoKUFQy41JWrPMRK3tZAWe3CCxz2jmNy51td6SeqiJpVUJwVBT/1OMUlvZJGqBh0FBWZtWM1Ejmac9r3HOa6QH6Vermde41om/pQWFE6UprXmrAtZri8ch8n9GOiBlW03njjQ2pYGWBPyt6f+jOI66pzeMo7WAJEnTmQH0BIla3Kam1lGDm04zvdY2buyiD56kPfGbQG0ehU1NwVDd+AfUWo+jwCsecddF9BeO/ZOuaAKdit+wtKaUYJp1KViLwIs8IEBLu3qw7aaaebqkEDymxx+FDGyTbaX9qflb2jw5AvbIz0jTRKhLK/lBen7+859XS3q6jDVB3pKHpLvLdcDvMftOC2zIB9LYNKAkBSHp+WbO9ZoiLSxLC0vi/EVBBfuhoDa9jiVJmukMoOeoCOCbAvxhTMQ2pdmIACOCoby2FnyX8lYqBIqjfLf4bOyza1ATwRvNevksA2VRk16H3wBqPCPdBLcUGOTdSaJWNNZj2019fMkvthH7ZyJQjYA8H9shBmELHDufj2MnTeTvRCCtbDtNK8Eq+RLpxTBjTZA/HBfbbotjJxgm2I30kA+cP85rnfx8M8/zi7SQp+RlbJdzynFKkjSbzdu2bVur/+22bNlSLF68uHonSTPT6Ve/Vrx450nVO0mSJGlP3DM+cf0R1btdrIGWJGkCUCvrgHGSJM0uBtCSJEmSJLVgAC1J0gSgP/CgZ35LkqSZxQBakiRJkqQWDKAlSZIkSWrBAHqO4ZE5DGwTGOBmmGd08rk2g+Pw/FOeySpJkiRJM50B9AxEUBrP3eyHwDUfBTaeQ/rqq6+Wc55DeuCBB5avJwLPCuUZpLfffnu1RJIkSZJmJgPoCUKtbgS5MY3zcSYLFy4s502BKQEygWusl7rtttuKU045pUzTqlWripNPPrn6y650U1M9Lq+88kqxZs2a6p0kSZIkzUwG0BOAQHnlypVl4MgorDF9+umnZXA6LgS/DzzwQPVud+vWrSuWL19e23x69erVO9NEDfFEI0BnX5IkSZI0kxlAjxk1uDSLJnhOa3ZBAA2aYI/DBRdcUNYy532YqT0mDdddd121ZHdRIx5T1DZH4A9qrvnboKbXeU17Lm1uzpRuL/pjU1sezc2Z8vyJ9fJpnDX6kiRJkjSIAfSYPfTQQ2XwmQfPgVrj9evXV+9Gwz6oZWafqTvuuKMxDQSeBN1RA016li1bVv6N55Vu2LChfB3rUFvdhCB906ZNO7fFPtOglkD4oIMO2vn3aMod/a8Dzck5hliH/EkLBdguzc7T/ZBun68qSRq3888/f48C21EnxwGRpNnDAHrMqGWOgLQOASXG1cf44osvLgPZdHsEoDThrkMAGgOJ4dRTTy2D5WEQvKdNwC+99NIyLYG/pQF4BPRbt24t54GgPf7GnACZwBwRbJ977rnlHOznhRdeqN5JkjQ+N998czF//vzqXW8cjyjA7TLxf+uxxx5bbUWSNFsYQI/ZoGB0wYIF1avxoKQc1Dojam5jeS5vDh1NtscR0MexpduiRjrdH7788sty3oTm3LGNCKyfeOKJcg76ffcrpJAkaVgUMj/88MPVu15B9TfffFO9a4/t/PrXv67eSZJmCwPoSTYoeBxG2iycfs+8r0Ntbt4cOppsTwQCYWrk0xL5YdH0O4JwtjsZg59JkuamM888s7jmmmvK1xSMX3nlleXrrqJVlSRp9jCAHjOaNferzf3iiy/K/0zTZtSj+vnPf17O6XPMf/TxPhdNp/v1ax7nM6FJS1NT8raoUSe/0iDcvs+SpIl200037WyC/dhjjxX3339/+borm3FL0uxiAD1mS5cu3aNPcmAZNcX04R0ngnECd7bNvCk4j+A4mnmTnmjCndu8eXP1angEvukAZ8OMmk2aCcTTZuBM4xrJXJKkJgTO0R/68ssvL957773ydRf8n9uv4HrcSGP8XylJGj8D6DHjP0kCR6Y8iI7lE/EfKX200nkdmpLRfJugmf9YSUvehJt1aAIe66SjYXfFQF8UJsR/5BQusM8uDjjggHJOEJ3WQlNY4KimkqSJlPeHPuecc4bqDz0RGOvk2muvrd7tsmjRovL/emu+JWlizNu2bVurjqlbtmwpFi9eXL3TINSQRr/kwH9ok1kKPRtErXXebJvl3NjYF1pdnX71a8WLd55UvZOkwQhUGZ0bK1asGKlweTKQ3u+++27O/R9JoQKtBrzfkjQO3DM+cf0R1btdrIGeIPynldaYMk2nH3MCUAbjmu4IktNHY4HB0FjGI7gkSZpoeX/oqQ6go2VXk3feead8bCaF+azX9GSOmSiaqNe1BIjzcsQRe97wStK4GEBrWqMggn7dcbPAdMopp5TP5ZxNNwSSpOkt7Q9NYDpMf+hxoYaV/xubUMjMIx8vu+yy4plnnim7VM0WNFGnUmK//farluwSQfWhhx5aziVpIhhAz1E0ieYRUzMBac1r8+P50JIkTYa0PzTNoy+55JKx9IemVVUUEB933HHV0h7G+oi/pYXGPNGDcUXqsD08+eSTZbD51VdfFcuWLSuXTYX0GJhStIaL5c8++2y1tCf9TBRWxLaaxkD56KOPykKOjz/+uGxlt+++++7MD0kaFwNoSZKkFtLnQ7/99tvF2rVry9ejoEA43WY6ACldv2g6znTPPfdUS3uDdC5ZsqR6t7sPP/ywXJ/gGb/73e+K0047rXw9FeIY8O6775bz8Mgjj1SviuLpp5+uXvVQcw4GO41jia5wTcf++uuvl3O2RSUBA5eSH5I0TgbQkiRJLaX9oRksNK85HcY+++xTDk6GF198sZwHmipT2x1NlgmweTLFYYcdtnMUbmpko1b25Zdf3q3Gmebchx9++NDPsR4H0p4G9SGOqW5gtr333rusTU5r3qNwoakV2ksvvVQeewyeRj6deOKJ5WtJGhcDaEmSpA7S/tAXXnjhHo+t7IrA7yc/+UlZY/rggw9WS3s2b968RxDIvk844YTivPPOK9/TpJsgHNROn3TSricNELieddZZxfe///1qyeQjiK9rRk7zavpyn3322WWz+LQwgprj/DPkRb++3/z9oosuKl9H0+08aJekURlAS5IkdZD3h47a42ERYFKjzHbSZtz0/WX7aRDIvr/99tuyiTLL6YdNQM2AYeBvNDUPb7311h7LJlMEsmlQH2hyfcwxxxSnn356+T5txk1N+tFHH12969m0aVPZ95va6tgu/ah5HXlFwQLY9vHHH18uj3UlaRwMoCVJkjrK+0MPG6TxOWqJac4cNcrRjJtBsfrVuILP0ax8nNIBvAZNg0S/5AhsU9S8E1hzDHkzbvI07+tMQcGaNWuK999/f2czbgoS9tprr+KNN97YmY/gUVYUTNxyyy1l4YQkjcu8bdu2ba9e97Vly5Zi8eLF1TtJmpl4KP6Ld+5ZEyJJw2CkZ2o+6W9L7XBX9F3+05/+tDMIZvRoAkVqjnlcFs9zjsGzZiJqiKkl53hyBOBff/11GfQSPK9cubIcPIzHUNGcnadu9EPhw9atW32spaQJwT3jE9fv+Vx5a6AlSZKGQNBH8MxI0cMEz6AW9sgjj6ze9QbUimbcBJ1NI07PFP36PxMkR41x2oybx1ANqnkHtdAGz5ImmwG0JElSR/StpYZ41apVIwVxBJj01Q3RjJsBsQik8+bH7JfnRVN7S+3uREibaA+a+olm7U39n9PAOppxMwjaBx98UPaNlqTpyABakiSpA5ok82gpalBvvPHGaml3UQub1l4zMBh9eQnO0z694Zxzzin3/corr0xYkEnT6bZTP4P6P5966qnVux5G0KYp/K233lobdEvSdGAALUmS1MGVV15ZBno8cioPcLv4h3/4h52Pw0oRINM0PG/6zGOeGFGbEbdpvjzuwcPGiUKGBx54oHq3O2rRqXnnWc8pBmYjP9LRtCVpujGAliRJaun+++8vnwPNY6xGecYwg4exHZppX3vttdXSnugPnPaNpr81z5wmuKTpNJ+fzn70ox+VhQzxOnXUUUeV8x/84AdloJ2iOXzaN1qSphtH4ZY0pzgKt6RhUXNK8Mfjq6ai9pdm3dTQTueaZ0maLRyFW5IkaUjUlJ522mllv+SpCmAZYMu+wZI0tQygJUmSBohmyM8991w5n2w81oom0TwjWZI0dQygJUmS+qC/MYNe/f73v5+yvrk81orm28M+b1qSNB4G0JIkSQ141NSaNWuK2267rRz5eqps2rRpj1G5JUmTzwBakiSpBs2mzzrrrGLFihXF6tWrq6Xd8OgpRs0eFf2f6YMtSZpaBtCSJEk1CJz33Xff4p577qmWdPfaa69Vr4ZHEE7/53i8lSRp6hhAS5IkZXg2M89ofvLJJ0fq90zNMX2Xh0U6eP7zhg0b7P8sSdOAAbQkSVJi48aNxc0331wGrYsWLaqWdnf//feXQfjxxx9fLemOR2Z9++23xfnnn18tkSRNJQNoSZKkynvvvVdcccUV5euVK1eW/ZeHnS6//PJyO5Kk2cMAWpIkqXLJJZcU3333XfVOkqTdGUBLkiRVaHI9bvZdlqTZwwBakiSpsn379rFP9957b7V1SdJMZwAtSZI0hG+++aYc3Cv6PEuSZj8DaEmSpCGsXbu2nH/99dfF8uXLy9eSpNnNAFqSJKkjap/Xr19f/OIXvyifE/3cc89Vf5EkzWYG0JIkSR3wqKsTTjihfH3UUUcVZ5xxRvlakjT7GUBLkiR1sGjRomLdunXFscceWw4SZu2zJM0dBtCSJEkdbdq0qVi2bFn1TpI0VxhAS5IkdfTCCy8URx55ZPVOkjRXGEBLkiR18PnnnxefffZZcdhhh1VLJElzhQG0JElSB5s3by7mz59f9oWWJM0tBtCSJEkd2P9ZkuYuA2hJkqSWaL69cePG4uyzz66WSJLmEgNoSZKkFp599tli4cKFxapVq4rzzz+/WipJmksMoCVJklo488wzy+c+33TTTdUSSdJcYwAtSZIkSVILBtCSJEmSJLVgAC1JkiRJUgsG0JIkSZIktWAALUmSJElSCwbQkiRpznrvvfeKefPmjX2SJM1OBtCSJGnOWrRoUXHNNddU74pi+fLl5aOqhpnuu+++aiuSpNnKAFqSJM1pPNf52GOPLV8///zzxf3331++7uqyyy4rA3BJ0uxlAC1Jkua8xx57rJg/f375+vLLLy+bdg/j4osvrl5JkmYjA2hJkjTnHXzwwcXDDz9cvSuKc845p/jmm2+qd+0ddthh1StJ0mxkAC1JkrTDmWeeubM/9GeffVZceeWV5esu6FNNf2hJ0uxkAC1JklRJ+0PTrHvY/tBzzauvvjqjRiA/44wzyrTefvvt1RJJascAWpIkKTGu/tDTwfnnnz8pgeLJJ59c3HbbbTNmELXnnnuunC9ZsqScS1JbBtCSJEmJvD/0JZdcMlR/6MkSz7KuS+PGjRvL+RFHHFHOJ9rSpUurVzMDgb8kdWEALUmSlEn7Q7/99tvF2rVry9fTUfS73m+//aolu0RQfeihh5bzcWLbV1xxRRm877vvvsWtt946aYH6MJ599tnikEMOKdPLPJrqS1IXBtCSJEk10v7Q69ev31mbOyoCuJjyptXRN5eJgC+Vfi6alfN53jc10f7oo4/K5ugff/xxGTQS6NJfuYt0v+l+SCu+/vrr4pNPPim+++674oQTTiiXTbQ47phC2hebKY6VvLzwwguLhx56qCxsWLFiRbFs2bLyb5LUhQG0JElSg7Q/NLWt4+gP/cwzz5RzgrjVq1eXr8MjjzxSvSqKp59+unrVE5/bsGFDWeuM+HxTX97XX3+9nLOtTz/9tFi4cGHx4YcflsvaqksvhQkEzPfee29Z871169Zy23W14F19/vnn5eBtBPxNSEcUbrz77rvlHDTJjpYD9MmOJtpXXXVVmdZ4zyjrRx55ZPlakrowgJYkSWqQ9ocmYKQ/9Kj23nvvcn7RRReV81QEoASreY03nyOYZ2CwQLCJpr68L730UlnTSvAIAscTTzyxfN1WXXqfeuqp3Wpwn3/++ZFqdGkOzvEed9xx5Xa+/PLL4oUXXqj+Wo+8IoiOwoSwzz77lPMf//jH5ZxCD477+OOPL9+zL7Yd7yWpCwNoSZKkPvL+0Ndee235elhRK1zX3Jkmx4xkffbZZ5cBe9qMm5rjPEjdvHlz35Gv+XsEvtGcOQ84B2lK77ffflvOqS1+4IEHioMOOqgMgrs0EWd9CgT233//YtOmTcUvf/nLsqac5vMUXvRD0P7DH/6werfL448/XgbWeW34X/7yl7LAged7k7cE2qOeS0lzjwG0JEnSAGl/6JtvvnmP/sldUCtcF+CBYPWYY44pTj/99PJ92oz75ZdfLo4++ujqXQ9BJyNfp4ErfZN5Tc1r2i+ZbVPryvIuQW5den/yk5+Utbj0qSYQvfTSS4s1a9aUNceDRrYm72gOz2fpk0xhAf2oqSWnsKKNSH/edJ3aZQo50oIGCgyo0T/qqKPK/XL+qMknn84777xqLUlqxwBakiSphbQ/9N13313Oh9GvuTPB6kknnVQGq3kzbgLDPGAkPQSu77///s7AlRrcvfbaq3jjjTd2C3wZIZt933LLLcVhhx1WLmujLr3sixpoJmqQ6ZPM4Fx5n+46P/jBD8rg+/e//335PGY+X1eY0E/Uip9yyim7DRpGTTby/s3kI+ljf9Rsk+633nqrc228JBlAS5IktUDgRfAZr4cRNacEyXUIVqPGOG3GTdNj+vHmtbvUjBMYMgfbX7duXRkYXnbZZWWQGKjdZV2CybYB66D0DoNByQjIzzrrrLIWmPTE47bailpxjiedGDgM9m+WNFEMoCVJklogyHvwwQfLwO3GG2+slnYzqP9zOpJ12oybx1D16+scCLDTQcZG1S+9wyKQp7k2tcAXX3xxOSAZNcc0r27bNL6pFp/AmjxMCzhoKp4+0kqSRmEALUmS1MLatWvLWmCC6K5NjsOg/s9pUMg6NOOmufMHH3xQ9o2ebE3pZeAwRsweFcE+NdD0gT711FOLG264oXx8FYN7xQjjuX614gyalgfWNBVHl2brktTEAFqSJGkAgrz169eXNaej9Jsd1P+ZIDLFCNoE7bfeeutYm1G31ZTevHn4qAjQCabZJgUGCxYsaMynplrxGDQtz8M///nPY3tGtSQZQEuSJPVBYLZy5cpi1apVIzWPpta2CfsgWI1nLgeaOzNQWDqa9jhRm0vz5ttvv71asktTeum3PJFNoml+TYDOYGg5mtHzyKw60T89z0Nq76lF5xhpzk0Nd9c+15IUDKAlSZIaEGidc845ZQBG7fOwCDYvv/zy8jWPUcqDTx6xBEaozoM7gvbJrkHtl97rrruunA96XFWTGDG7zZT70Y9+VNbIx+tAcMwo6cjzkJr9qNX+5JNPys9v3bq1+qskdTNv27Zt26vXfW3ZsqVYvHhx9U6SZqbTr36tePHOyW8GKWlmIngl+OIRUsOOvD3b0Jyd5zfzSKiZgED8vvvuK2u1qek/7bTTygHMJKkf7hmfuP6I6t0u1kBLkiTViFrNhx9+2OA5sWnTpmLp0qXVu+mNgBnnnntuOe/XB12S2jCAliRJytBkec2aNeVzhemHrF2okV+yZEk5UvZ070v8xhtv7DaKOM25jz766KGePS1JMICWJElKEFidddZZ5XOXV69eXS1VYFAz8ufII4+c9iNbv/zyy7vVOPMoMApGvvzyS0flljQU+0BLmlPsAy1pEEaZ5nnCDDhlkCVJc5N9oCVJkgagWTL9ZKm5HDZ4Pu6442ofCyVJmvkMoCVJknZ49tlny0c2MWLzokWLqqXd0PybEbslSbOTAbQkSZrzPv/88+LCCy8sVqxYUT7uaFhvvvlmOd9nn33KuSRpdjGAliRJcxq1xgTOCxcuLO65555qaXcE4TfccEP5+vDDDy/nkqTZxQBakiTNaWvXri2bXTPtv//+xbx584aaCMBtvi1Js5sBtCRJmrPo97x+/frqnSRJ/RlAS5KkOeuDDz6oXo3XAQccUL2SJM0mBtCSJGnOWr16dbF9+/axTwcffHC1B0nSbGIALUmSJElSCwbQkiRJLbz33nvlYGGM2i1JmpsMoCVJklpYtGhR2Tx7v/32q5ZIkuYaA2hJkqQBbr/99rL2mbkkae4ygJYkSRqAwcawZMmSci5JmpsMoCVJkgb4/PPPy/nJJ59cziVJc5MBtCRJ0gCbN28uli9fXr2TJM1VBtCSJEkDbNq0qVi6dGmxcePG4tVXX62WSpLmGgNoSZKkAebPn1+sWbOmeP/9923GLUlzmAG0JEnSADfddFP5CCvmkqS5ywBakiRJkqQWDKAlSZIkSWrBAFqSJEmSpBYMoCVpRIzIO2/evHJ0XkmSJM1eBtCSNIQ0aGZE3s8++6xYuXJlufyMM84o//b5559Xaw+PbfQLzlnO3/PH6sTnSMs4xPHm+8nx90MOOaR6V5SvB31morRNc7jiiis6rT+qpnMnSZKmLwNoSUpE8JtPg4Lhgw8+uByh9/XXXy8+/fTT4rbbbisDsqnCvkkDabn99turpRPvgAMOKAsTyC8mXrNsuiOIXb9+fbFhw4bilFNOqZZKkiTtzgBakhIEnKtWrSqD4ZgIRBcuXLhbQEytM387//zzqyW9Wl+eE/vQQw8Vq1evLrc10c262T/pSJ9LS8DMvkkDaSFNgwoAxoWChMgvJl6zbKJR0z1KgQVBM8Ez+bl8+fJJKfyoO3eSJGl6M4CWpAEIRAmuqKHs19w2aqEjICKITQPsyRLBOyLQn4wgNrB/9snE65mAtMa5eu6554p77723fC1JkpQygJakFgiuqFFdt25d+Z4aXZp25zXM1ISmTb/TgJuaYZalmrbTT+wDbD/fD1iWTmkNNOmIvsnpOv0KB1LpMeY1tXE86ZRifZrJR//fmPIactZL/x5TnsY4BpqKU8AR6+XSNNc1ac+b7ufHxef5XJouluXS/aRTnUh7HFO8z/OwLr2SJGlqGEBLUksER1GzW4dg59JLL91Z+xr9afOgbxSkgWCR7deJ4It9RzqiSXUapLKNiy++eOc6NFtv0/eXdWgWzmciaI0Aj+2zn9gmE82h84HMnn/++Z3biHWWLVtW/bUX4LPd+DvHAvaXN3eOGnb2mza9T5HmF154Yee2aNKenpM4r/FZJvafp5vPHXTQQTvXIT1poM36bCv+TnoiP7rgM3GO69IrSZKmjgG0JO0QtX8RFEbtXxp09msGTdBH4JM2WY5a60cffbRaMpoI6PoFZHfccUcZkKZNxyNNTzzxRDkPaWHABRdcUM4HBWqvvPLKziCW/CBIfOCBB3a+z9O2dOnSPQodyBOaSQcCefI98vqll14qtxviWDZv3lzOuyLNce5iWwz2BmrC2TcBdorAlUA/Pf+kKT2/vE8/x/ocSyBP0+Nqq196JUnS1DKAlqQdmmoy06C5XyD0xRdflMFSBN4xsWwceEQWAVq/GnCQRtbL0zFIjJS9devWct4WNbLpMUZBREzUng7KgwMPPLCc/9u//Vs5J+imECNE8/bjjz++nI+Kc8z5wpdfflnO0/OMPE118mOn4IKa9UDBCfvKt91Vml5JkjS1DKAlqSWC17SpcY5AJwLvdBrHgFTRjJkmwoMQyNWlY6IH9CLQjdGsY580Hx9WBOEUHqS1stNZWnhBIcCgAg9JkjSzGEBLUgvR1DeaOufy2sg6CxYsKOddm/QGts+UD3CVIsiczKCNmlEKDkBtLq/T5uPDoEl4GoQz5X2fc20KFuo0nZOoiW/7DOuo+ef8pOmWJEmziwG0JA1A8EwtKLWpTYHcueeeW87zgad4H/2Kowly9EUm6Irgsw2CYwJLajabRmaOfrd1o0gPG7in0kHRmJMWBk4DwSj7Tv9OE+6uSCv5HTW5MQ1Kf96PuY0I9tP8Yj/sn6b8bWu9Yz3OZ5rmYQP7JqSN7fYrRJEkSRPHAFqSEgQ86SBiTART1Cb2awJNAMU6ef9jBpVKB90iACao5G8EWwScXRDwEcg3jczMvthmfgz0zW0bDPbDMRJEs03mpCXyhbQRdKZ/j6bnXZDOtB86U4wk3oRm8hw3++0atLJ9au0jr9gP++va9J7P5TXnpCUvVJEkSTPXvG3btrVqY7Zly5Zi8eLF1TtJmplOv/q14sU7T6reabqhUIDAOx3tG7GcIHkcBQHjRosACjUImlMsp0m6faElSZpZuGd84vojqne7WAMtSbMUNZ/UqM4k0ec4f2zTunXryhre6Rg8I/pS560CCKr7DTwnSZJmFgNoSdK0QYBM7XM0c48J07kWN5rWR/P1mIZpCi5JkqYvm3BLmlNswi1JkqRBbMItSZIkSdIIDKAlSZIkSWrBAFqSJEmSpBYMoCVJ0pzEqOnpQHWSJA1iAC1JkuYknjXOSOnLly+vlkg9PMOdghUeByhJKQNoSZJU2nfffXfWyA6aZpOlS5dWr6Se1atXlwUrXhuScgbQkiSp9PDDD5fzhQsXFl9//XWxffv23Sae0T1//vxynZnqm2++Ka644oqyEIACg1tvvbU44og9H1MyE91///3lcX3++efVktnnvffeK49x48aN1ZKJtWTJkurV1IgCK541L2l6MICWJEmlM888s1ixYkXx2WefFXfddVe1dBeaPK9atap6Nz1EgMFEs9tA09tYnjbDjdcUEHzyySfFd999V5xwwgnlsqmSpjUmgnsCfQL+tgguKeA4+OCDqyWzz0cffVTODzvssHI+TuRfnItDDjmkeP755ydkP11wneLoo48u55KmngG0JEna6eabby6DMOYMspU777zzqlfTwzPPPFPOCfxpdhseeeSRcs6xxGtqLQmY77333mK//fYrtm7dWta283rcCMauvfbaVjWHkT6aDEdtP2lcv359sXbt2vJvbfCZb7/9tno3tWKAti4FAG2Qn+TPokWLqiXjQa39aaedVvzN3/xNuf277767OPbYY4e+NrjWOP5+rQFinbrvWW6qa8Il7WIALUmSdqL28pZbbilfX3zxxXsEQAQuBBjTxd57713OL7roonIeIvChxjxeP/XUU8WyZcvK16CGMX0/KoIlasGpvbzkkkuKBQsWFPfcc0/112aRvrS/LYEiAfVMbI7NNfPTn/50pAB0st1xxx1lnl922WXl+6+++qo47rjjytfDYFsU3vzmN7+pluzpoYceKs8xLTuavPnmm+V8qmvCJe1iAC1JknZDEMGNfVNT7unk9ddfL+c0P089++yz5fykk04q5yFqaOkv/MADDxQHHXRQWRPYphawDsEi2yLYImD805/+VDz55JPFW2+9VeZjmwAy9p3XMratvY3aXqY4bgLvaI5M+kCNOO8J8CMwH7QeNelgH7xneZ5X0dwcbGP//fcv3n777XJi/brPNKEAIh3MjkA00hrLSF+qrgl83XqcZ84Tf2MfvA+8PvXUU6t3RfG73/1ut/fDoPCGVgR1yA8KcK677rpqSQ/5F/nMcf32t79tXRDBZzkuPs+1w7mLbeV5IWkE27Zt295m2vEf1HZJmun++mevVq8k9bMjeKaauZxeeeWVaun0syPQL6fcNddcU6b966+/rpZsL49j/vz55bRhw4btt912W7kO8y7YJp9fsWJF+fkdgdL2Z555pvprd5GO1Lvvvlsu4zjaiOPlvIG08Tryh79z/KQ9PeZ8PY4l1iOf4u8szz+LuE7Ij1C3rI377ruv3CfHjsiXOIfkcd128zSR1h1B587PgWVsO67lON7A39g/nyGvYl1ep9vpIvKhaUr3j9hvHB9z1iPtg7Au6SfNfIbXcc4iHyNfJbXDPWNdXGwALWlO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)

0. Ràng buộc mối quan hệ giữa nhà máy và kho
"""

# Nhà máy - kho TCO

    # add_constraint_factory_TCO(model, data,a)

def add_constraint_factory_TCO(model, data,a):

    for fac_idx in range(data['num_factories']):
        for depot_idx in range(data['num_depots']):

            # không được phép đưa hàng tới
            if data['mat_config_FD'][fac_idx][depot_idx] == 0:
                model.Add(a[fac_idx,depot_idx] == 0)
            # bắt buộc phải nhận hàng từ kho
            if data['mat_config_FD'][fac_idx][depot_idx] == 2:
                model.Add(a[fac_idx,depot_idx] == 1)

"""1. Mối quan hệ giữa các biến

"""

def add_constraint_mqh_bien(model,data, a, N):

    for fac_idx in range(data['num_factories']):
        for depot_idx in range(data['num_depots']):
            for prod_idx in range(data['num_products']):

                # Ràng buộc khi a = 1: N > 0
                model.Add(N[fac_idx, depot_idx, prod_idx] > 0).OnlyEnforceIf(a[fac_idx, depot_idx])
                # Ràng buộc khi a = 0: N = 0
                model.Add(N[fac_idx, depot_idx, prod_idx] == 0).OnlyEnforceIf(a[fac_idx, depot_idx].Not())

"""1. Tổng lượng hàng vận chuyển từ nhà máy bằng tổng lượng nhà máy cung cấp:
$$ \sum_h N_f^{ih} \le  Smax_f^i , \text{ với mọi f,i}$$
$$ \sum_h N_f^{ih} \ge  Smin_f^i , \text{ với mọi f,i}$$
"""

def add_constraint_for_supply_factory(model, data, N):
    for fac_idx in range(data['num_factories']):
        for product_idx in range(data['num_products']):
            model.Add(sum([N[fac_idx,depot_idx,product_idx] for depot_idx in range(data['num_depots'])]) <= data['matrix_supply_max'][fac_idx][product_idx])
            model.Add(sum([N[fac_idx,depot_idx,product_idx] for depot_idx in range(data['num_depots'])]) >= data['matrix_supply_min'][fac_idx][product_idx])

"""2. tổng lượng hàng nhận được từ kho bằng lượng demand.
$$ \sum_f N_f^{hi} <= D^{hi} , \text{ với mọi i,h} $$
$$ \sum_f N_f^{hi} >= D^{hi} - \text{surplus}^{ih}, \text{ với mọi i,h}  $$
"""

def add_constraint_for_demand(model, data, N, surplus):

    for dep_idx in range(data['num_depots']):
        for product_idx in range(data['num_products']):

            model.Add(sum([N[fac_idx,dep_idx,product_idx] for fac_idx in range(data['num_factories'])]) \
                    <= data['matrix_demand'][dep_idx][product_idx])

            model.Add(sum([N[fac_idx,dep_idx,product_idx] for fac_idx in range(data['num_factories'])]) \
                    >= data['matrix_demand'][dep_idx][product_idx] - surplus[dep_idx,product_idx] )

"""3. Điều kiện băng thông

$$  \sum_{h \in d} \sum_f \sum_i N_f^{hi}. I_i \le limitIn_d ,\text{với mọi d} $$
"""

def add_constraint_limitIn(model, data, N):

    for physic_depot_id in range(len(data['cluster_physic_depot'])):
        cluster = data['cluster_physic_depot'][physic_depot_id]
        capacity_luong_hang = sum([N[fac_idx, dep_idx, item_idx]*data['ratio_capacity'][item_idx] for item_idx in range(data['num_products']) \
                        for dep_idx in cluster for fac_idx in range(data['num_factories'])])
        model.Add( capacity_luong_hang  <= int(data['limit_in'][physic_depot_id]))

"""# cost function

$$ \min \sum_{f,h,i} N_f^{hi}*(d_{fh}*weightRateProduct_i + handlingCost_h + deployProduct_{fh} )+ \sum_{h,i}  surplus_{hi}*{penalty}_{hi}   $$
"""

# objective = model.Objective()

def create_coefficent(data, product_idx,fac_idx, dep_idx ):

    cost_vanchuyen = data['weight_product'][product_idx]*float(data['IB_transport_cost'][fac_idx][dep_idx])
    cost_xephang =  data['handlingCost_in'][dep_idx]
    cost_deployProduct = data['fixed_cost_by_sku_per_factory'][fac_idx][product_idx]

    coefficient = cost_vanchuyen + cost_xephang + cost_deployProduct
    return coefficient

def create_cost_function(model, data,a, N, surplus):
    coefficient_N = sum(  create_coefficent(data, product_idx,fac_idx, dep_idx)*N[fac_idx,dep_idx,product_idx] \
                           for product_idx in range(data['num_products']) for fac_idx in range(data['num_factories']) \
                             for dep_idx in range(data['num_depots']) ) + \
                    sum( surplus[dep_idx,product_idx]*data['penalty_cost'][dep_idx][product_idx] for product_idx in range(data['num_products']) \
                             for dep_idx in range(data['num_depots']))



    model.Minimize(coefficient_N)


    # for dep_idx in range(data['num_depots']):
    #     for product_idx in range(data['num_products']):
    #         model.Minimize(surplus[dep_idx,product_idx]* data['penalty_cost'][dep_idx][product_idx])

"""# Main"""

class VarArraySolutionPrinterWithLimit(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions with a limit."""

    def __init__(self, N, a,surplus, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__N = N
        self.__a = a
        self.__surplus = surplus
        self.__solution_count = 0
        self.__solution_limit = limit
        self.best_solution = None

    def on_solution_callback(self):

        self.__solution_count += 1
        print(f'Solution {self.__solution_count}:')
        print(f'Objective {self.ObjectiveValue()}:')

        if self.best_solution is None or self.ObjectiveValue() < self.best_solution.ObjectiveValue():
            self.best_solution = self



        if self.__solution_count >= self.__solution_limit:
            print(f'Stop search after {self.__solution_limit} solutions')
            self.StopSearch()




    def solution_count(self):
        return self.__solution_count

"""# class output"""

class Output:
    def __init__(self, output, data):
        self.output= output
        self.data= data
    def visualize_output(self):
        data = self.data
        output =  self.output
        if output == False:
            return False

        X_all = output["vehicle_used"]
        # visualize vị trí của nhà máy và kho
        location_factory = data['loc_f']
        location_depot = data['loc_h']
        plt.plot( location_factory[:, 0], location_factory[:, 1], "rs")
        plt.plot( location_depot[:, 0], location_depot[:, 1], "bo")

        for fac_idx in range(data['num_factories']):
            for dep_idx in range(data['num_depots']):
                if X_all[fac_idx][dep_idx] >0:
                    plt.plot([location_factory[fac_idx][0], location_depot[dep_idx][0]],\
                            [location_factory[fac_idx][1], location_depot[dep_idx][1]], lw=1)
    def draw_supply_NM(self):
        data = self.data
        output =  self.output

        if output == False:
            return False

        N_all = output['number_weight_from_factory2depot']
        print("N_all", N_all.shape)
        figure, axis = plt.subplots(2)
        bar_width = 0.2
        X_axis = np.arange(len(N_all))
        color_list  = list(mcolors.CSS4_COLORS.values())

        for sku_id in range(data['num_products']):

            print("sku_id", sku_id)

            # n_x, n_n, n_d)
            bottom_data=  np.zeros((len(N_all)))

            supply_max_each_sku = data['matrix_supply_max'][:,sku_id]
            supply_min_each_sku = data['matrix_supply_min'][:,sku_id]

            for dep_idx in range(data['num_depots']):

                print("N", N_all[:, dep_idx, sku_id ])

                axis[sku_id].bar(X_axis + 0.00, N_all[:, dep_idx, sku_id ] , bottom = bottom_data,\
                                color = random.choice(color_list), width = bar_width, label = "TCO "+str(dep_idx))

                print("dep_idx", dep_idx)
                bottom_data = bottom_data +  N_all[:, dep_idx, sku_id ]



            axis[sku_id].bar(X_axis + bar_width, supply_max_each_sku, color = "k", width = bar_width, label = "supply_max")
            axis[sku_id].bar(X_axis - bar_width, supply_min_each_sku, color = "silver", width = bar_width, label = "supply_min")

            axis[sku_id].set_xticks(X_axis, ["nhà máy "+ str(i ) for i in range(len(N_all))])
            axis[sku_id].plot(len(X_axis)+1,0)
            # axis[sku_id].legend(labels=["TCO "+ str(dep_idx)  for dep_idx in range(data['num_depots'])])
            # axis[sku_id].legend(labels=["supply_min", "supply_max"])
            axis[sku_id].legend()
        plt.show()
    def draw_demand(self):
        data = self.data
        output =  self.output
        if output == False:
            return False
        N_all =  output['number_weight_from_factory2depot']

        figure, axis = plt.subplots(2)
        bar_width = 0.2
        X_axis = np.arange(len(N_all[0]))
        color_list  = [ 'r',  'g', 'b', 'c','m','y', 'navy', 'lime', 'tan', 'coral', 'pink']

        for sku_id in range(data['num_products']):

            print("sku_id", sku_id)

            bottom_data=  np.zeros((len(N_all[0])))

            demand_each_sku =  data['matrix_demand'][:,sku_id]

            for fac_idx in range(data['num_factories']):

                axis[sku_id].bar(X_axis + 0.00, N_all[fac_idx, :, sku_id ] , bottom = bottom_data, color = color_list[fac_idx], \
                                width = bar_width, label = "NM "+str(fac_idx))
                bottom_data = bottom_data +  N_all[fac_idx, :, sku_id ]


            axis[sku_id].bar(X_axis + bar_width, demand_each_sku, color = "k", width = bar_width, label = "demand")


            axis[sku_id].set_xticks(X_axis, ["TCO "+ str(i ) for i in range(len(N_all[0]))])
            axis[sku_id].plot(len(X_axis)+1,0)
            # axis[sku_id].legend(labels=["TCO "+ str(dep_idx)  for dep_idx in range(data['num_depots'])])
            # axis[sku_id].legend(labels=["supply_min", "supply_max"])
            axis[sku_id].legend()
        plt.show()
    def get_value(self):
        return self.output
    def get_data(self):
        return self.data
    def draw_check_limitIn(self):
        data = self.data
        output =  self.output
        if output == False:
            return False
        N_all =  output['number_weight_from_factory2depot']

        # xử lý data
        capacity_N = np.empty((data['num_factories'],data['num_depots'], data['num_products']))
        for fac_idx in range(data['num_factories']):
            for dep_idx in range(data['num_depots']):
                for item_idx in range(data['num_products']):
                    capacity_N[fac_idx][dep_idx][item_idx] = N_all[fac_idx, dep_idx, item_idx] *data['ratio_capacity'][item_idx]


        # vẽ

        bar_width = 0.1
        X_axis = np.arange(len(data['cluster_physic_depot']))
        print("X_axis", X_axis)
        color_list  = [ 'r',  'g', 'b', 'c','m','y', 'navy', 'lime', 'tan', 'coral', 'pink']

        luong_hang_inPD = []
        for physic_depot_id in range(len(data['cluster_physic_depot'])):

            cluster = data['cluster_physic_depot'][physic_depot_id]
            limitIn_cluster = data['limit_in'][physic_depot_id]

            luong_hang_inPD.append(np.sum([ capacity_N[:,depot_idx,:] for depot_idx in cluster]))

        plt.bar(X_axis, luong_hang_inPD, width = bar_width ,edgecolor ='grey', label ='lượng hàng trong kho')
        plt.bar(X_axis + [bar_width]*len(X_axis),  data['limit_in'], width = bar_width ,edgecolor ='grey', label ='lượng hàng giới hạn')


        # axis[0].set_xticks(X_axis, ["kho vật lý "+ str(i ) for i in range(len(data['cluster_physic_depot']))])
        # axis[0].plot(len(X_axis)+1,0)
        plt.legend()
        plt.show()



    def print(self):
        print(self.output)
        print(self.data)

    def help(self):
        s="List Functions:\nvisualize_output()\ndraw_supply_NM\ndraw_demand\ndraw_check_limitIn\nget_value\n_get_data"

        print(s)

"""# class ORModel

# New Section
"""

def optimize(data, limit_time_s , num_of_solution):

    # Create the mip solver with the SCIP backend.
    time1 = time.time()
    model = cp_model.CpModel()

    # create variables
    N = {}
    for fac_idx in range(data['num_factories']): # nhà máy
        for dep_idx in range(data['num_depots']): # kho
            for product_idx in range(data['num_products']): # sản phẩm
                N[fac_idx,dep_idx,product_idx] = model.NewIntVar(0, 100_000_000, '')

    a = {}
    for fac_idx in range(data['num_factories']): # nhà máy
        for dep_idx in range(data['num_depots']): # kho
            a[fac_idx,dep_idx] = model.NewIntVar(0, 1, '')

    surplus = {}
    for dep_idx in range(data['num_depots']): # kho
        for product_idx in range(data['num_products']): # sản phẩm
            surplus[dep_idx,product_idx] = model.NewIntVar(0, 100_000_000, '')

    # Thêm các ràng buộc
    add_constraint_factory_TCO(model, data,a)
    add_constraint_mqh_bien(model, data,a, N)
    add_constraint_for_supply_factory(model, data, N)
    add_constraint_for_demand(model, data, N, surplus)
    add_constraint_limitIn(model, data, N)
    create_cost_function(model, data,a, N, surplus)


    # Creates a solver and solves the model.
    # solver = cp_model.CpSolver()
    # status = solver.Solve(model)

    # Create a solver and solve.
    solver = cp_model.CpSolver()

    # Thiết lập giới hạn thời gian (đơn vị là giây)
    if limit_time_s > 0:
        solver.parameters.max_time_in_seconds = limit_time_s  # Ví dụ: giới hạn 60 giây (1 phút)

    solution_printer = VarArraySolutionPrinterWithLimit(N, a, surplus, num_of_solution)
    # Enumerate all solutions.
    solver.parameters.enumerate_all_solutions = True

    # Solve.
    if num_of_solution > 0:
        status = solver.Solve(model, solution_printer)
    else:
        status = solver.Solve(model)

    print(f"Status = {solver.StatusName(status)}")
    print(f"Number of solutions found: {solution_printer.solution_count()}")
    # assert solution_printer.solution_count() == 5


    output = {}

    N_all = np.zeros((data['num_factories'],data['num_depots'], data['num_products']), np.int_)
    X_all = np.zeros((data['num_factories'],data['num_depots']), np.int_)
    surplus_all = np.zeros((data['num_depots'], data['num_products']), np.int_)


    if status == cp_model.OPTIMAL :
        print(f"Minimum of objective function: {solver.ObjectiveValue()}\n")

        for i in range(data['num_factories']):
            for j in range(data['num_depots']):
                for h in range(data['num_products']):

                    X_all[i][j] = round(solver.Value(a[i,j]))
                    N_all[i][j][h]  = round(solver.Value(N[i,j,h]))
                    surplus_all[j][h] = round(solver.Value(surplus[j, h]))

        output["number_weight_from_factory2depot"] = np.copy(N_all)
        output["vehicle_used"] = np.copy(X_all)
        output["surplus"] = np.copy(surplus_all)

        return output


    elif solution_printer.best_solution or status == cp_model.FEASIBLE:

        print('FEASIBLE Objective value =', solver.ObjectiveValue())
        for i in range(data['num_factories']):
            for j in range(data['num_depots']):
                for h in range(data['num_products']):
                    if round(solver.Value(N[i,j,h])) > 0:

                        X_all[i][j] = round(solver.Value(a[i,j]))
                        N_all[i][j][h]  = round(solver.Value(N[i,j,h]))
                        surplus_all[j][h] = round(solver.Value(surplus[j, h]))

        output["number_weight_from_factory2depot"] = np.copy(N_all)
        output["vehicle_used"] = np.copy(X_all)
        output["surplus"] = np.copy(surplus_all)

        return output
    else:
        print('Không tìm thấy giải pháp tối ưu hoặc gần đúng.')
        return False

class ORModel:
    def __init__(self, input):
        self.data =  input.data
        # self.model =
    def solve(self, limit_time_s , num_of_solution):
        data= self.data
        self.out_put = optimize(data, limit_time_s , num_of_solution)
        return Output( self.out_put, self.data)
    def help(self):
        s=""
        s+= "solve(limit_time_s = 180, num_of_solution=11000)"
        print(s)

"""# Visualize"""


class DrpTuan:
    # BASE_PATH = "/content/drive/My Drive/Colab Notebooks/sabeco3/"

    def __init__(self, input):

        self.input =  input
        self.output="not been solved"

    def create_model(self, param= "or_model"):
        problem_sabeco = ORModel(self.input)
        self.model =  problem_sabeco

    def solve_drp_ngay(self, param= "or_model", limit_time_s = 300, num_of_solution=11000):
        self.create_model(param)
        if param == "or_model":
            self.output= self.model.solve(limit_time_s , num_of_solution)

    def help(self):
        s=""
        s+= "main( data_model = None, file_name = None)"
        s+="\nParameters\n data_model: kiểu dữ liệu được truyền vào. \nfile_name: đọc từ file. \n Default: create faked data"
        print(s)


input= Input()
problem= DrpTuan(input)
my_output = problem.solve_drp_ngay(param= "or_model", limit_time_s =-1, num_of_solution=-1)

problem.output.get_value()
