from ortools.linear_solver import pywraplp
import numpy as np
import math
import copy
import collections
from ortools.sat.python import cp_model
import matplotlib.pyplot as plt
import time
import json
# import os
# from google.colab import drive
# drive.mount('/content/drive')
# os.chdir("/content/drive/My Drive/Colab Notebooks/sabeco3")
import random as rd

from matplotlib.pyplot import figure
import json
import codecs
import zipfile
import matplotlib.colors as mcolors
import random

"""#2 Read Json and Fake Data"""

num_priods = 5 # @param {type:"integer"}

num_products = 2 # @param {type:"slider", min:1, max:100, step:1}

num_depots = 34 # @param {type:"slider", min:1, max:1000, step:1}

num_customers = 100 # @param {type:"slider", min:1, max:1000, step:1}

num_physic_depots = 3 # @param {type:"slider", min:0, max:100, step:1}



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
        json.dump(numpy_to_list(data), json_file,default=lambda x: int(x) if x.dtype == np.int64 else x)

def get_fake_data(s, num_products, num_depots,num_customers, num_physic_depots, num_priods):

    fake_data = {}

    # create data
    # supply
    fake_data['num_priods'] = num_priods
    fake_data['num_products'] = num_products
    fake_data['num_depots'] = num_depots
    fake_data['num_customers'] = num_customers
    fake_data['num_physic_depots'] = num_physic_depots

    fake_data['inventory'] = np.random.randint(300,1000,size= (num_priods, num_depots,num_products))

    sum_S = np.sum(fake_data['inventory'], axis=1)

    # Tạo ma trận yêu cầu (demand) ngẫu nhiên cho nhiều ngày
    matrix_demand_daily = np.random.randint(30, 100, size=(num_priods, num_customers, num_products))

    for day in range(num_priods):
        sum_demand_daily = np.sum(matrix_demand_daily[day], axis=0)

        for sku_id in range(num_products):
            # Tránh chia cho 0
            if sum_demand_daily[sku_id] != 0:
                scaling_factor = 0.5 * sum_S[day, sku_id] / sum_demand_daily[sku_id]
                matrix_demand_daily[day, :, sku_id] = np.round(matrix_demand_daily[day, :, sku_id] * scaling_factor)

    fake_data['matrix_demand'] = np.copy(matrix_demand_daily)


    # capacity each physic depot
    # fake_data['capacity_physic_depots'] = [int(np.ceil(np.sum(sum_S)/num_priods*2/(num_physic_depots-1)))]*num_physic_depots
    fake_data['capacity_physic_depots'] = [np.sum(matrix_demand_daily)]*num_physic_depots

    # tồn kho theo ngày bán hàng
    # fake_data['safety_stock'] = np.random.randint(70,130,size= (num_depots, num_products))

    fake_data['safety_stock'] = np.empty( (num_priods, num_depots, num_products))
    sum_demand_F = np.sum(matrix_demand_daily, axis=1)
    for day in range(num_priods):
        for sku_id in range(num_products):
            for depot_id in range(num_depots):
                low_bound = round(sum_demand_F[day, sku_id]/num_depots)
                upper_bound = round(sum_S[day, sku_id]/num_depots)
                fake_data['safety_stock'][day][depot_id][sku_id] = np.random.randint(low_bound, upper_bound)
    # hàng có sẵn trong kho.


    # khả năng xuất nhập của kho vật lý
    low_bound = round(np.sum(fake_data['matrix_demand'])/num_physic_depots/num_priods)
    upper_bound = round(np.sum(fake_data['capacity_physic_depots'])/num_physic_depots)
    fake_data['limit_out'] = np.random.randint(low_bound, upper_bound, num_physic_depots)

    # chi phí xử lý nhập hàng mỗi pallet của mỗi kho vật lý
    fake_data['handling_cost_in'] = np.random.randint(10,30, num_depots)


    # chi phí xử lý nhập hàng mỗi pallet của mỗi kho vật lý
    # fake_data['handling_cost_out'] = np.random.randint(10,30, num_depots)
    fake_data['handling_cost_out'] = [1]*num_depots


    # location all points
    number_location = num_depots + num_customers

    loc =  np.random.randint(1,200, (number_location,2))
    loc_h = loc[: num_depots]
    loc_c = loc[num_depots:]
    fake_data['loc_h'] = np.copy(loc_h)
    fake_data['loc_c'] = np.copy(loc_c)


    # matrix distance depot - customer
    distane_h_c = np.empty((num_depots,num_customers),  np.int_)
    for i in range(num_depots):
        for j in range(num_customers):
            distane_h_c[i,j] = round(((loc_c[j][0] - loc_h[i][0] )**2 + (loc_c[j][1] - loc_h[i][1] )**2 )**0.5)
    fake_data['distane_h_c'] = np.copy(distane_h_c)


    # max distance
    max_distance = round(np.mean(distane_h_c))
    fake_data['max_distance'] = 1000_000

    # matrix config
    mat_config_DC = np.empty((num_depots, num_customers), np.int_)
    for i in range(num_depots):
        for j in range(num_customers):
            # mat_config_DC[i][j] = np.random.choice([0, 1, 2])
            mat_config_DC[i][j] = 1

    fake_data['mat_config_DC'] = np.copy(mat_config_DC)


    # map physic depots with depots
    map_physic_depots_with_depots  = np.zeros((num_physic_depots, num_depots), np.int_)

    # Đặt giá trị ngẫu nhiên thành 1 trong mỗi cột sao cho tổng mỗi cột bằng 1
    for physic_dep in range(num_depots):
        # Tạo một chỉ mục ngẫu nhiên trong mỗi cột
        idx = np.random.choice(num_physic_depots)
        # Đặt giá trị tại chỉ mục đó thành 1
        map_physic_depots_with_depots[idx, physic_dep] = 1

    fake_data['map_physic_depots_with_depots'] = np.copy(map_physic_depots_with_depots)


    fake_data['cluster_physic_depot'] = []

    for cluster_idx in range(len(fake_data['map_physic_depots_with_depots'] )):
        depot_in_cluster = []
        for dep_idx in range(num_depots):
            if fake_data['map_physic_depots_with_depots'][cluster_idx][dep_idx] == 1:
                depot_in_cluster.append(dep_idx)
        fake_data['cluster_physic_depot'].append(depot_in_cluster)

    # fake_data['cluster_physic_depot'] = [[0],[1]]
    # fake_data['fixed_cost'] = [10,10]
    # fake_data['price_product'] = np.random.randint(1,5, num_products)
    fake_data['ratio_capacity'] = [1]*num_products
    fake_data['weight_product'] = [1]*num_products
    fake_data['OB_transport_cost'] = np.copy(distane_h_c)
    # fake_data['priceByLevelService'] = [1,1]

    # Kiểm tra kiểu dữ liệu của các biến
    # for key, value in fake_data.items():
    #     print(f"{key}: {value.dtype if isinstance(value, np.ndarray) else type(value)}")

    # if s=="":
    #     named_tuple = time.localtime() # get struct_time
    #     time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    #     save_to_json(fake_data, "DRP_day"+time_string[11:]+".json")
    #     print(  "DRP_week"+time_string[8:10]+"_"+time_string[12:]+".json")
    # else:
    #     save_to_json(fake_data, s+".json")
    #     print(s+".json")


    return fake_data
# get_fake_data("test_DRP_day", num_products, num_depots,num_customers, num_physic_depots, num_priods)

filename =  '/content/drive/My Drive/Colab Notebooks/sabeco3/test_DRP_day.json'

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


# data = load_from_json(filename)
# data = convert_to_numpy(data)

"""#3 Input"""

class Input:

    def __init__(self, data_model = None, file_name = None, name=""):
        self.name =  name
        if data_model == None and file_name==None:

            self.data =  self.fake_input()
        elif file_name!=None:

            self.data= self.get_input_from_file(file_name)
        else:

            self.data = data_model


    def fake_input(self):
        # create random input from scratch
        data_model = get_fake_data("test_DRP_day", num_products, num_depots,num_customers, num_physic_depots, num_priods)
        # filename =  '/content/drive/My Drive/Colab Notebooks/sabeco3/test_DRP_day.json'
        # print("successfully create faked input")
        # data_json = load_from_json(filename)
        # data_model = convert_to_numpy(data_json)
        return data_model
        # self.input   =  Input(data_model, name = "input from faked function")


    def get_input(self, data_model):
        # get input from Data_model
        self.input  =  Input(data_model, name = "input from data_model")


    def get_input_from_file(self, file_name):
        # Gêt input from json file.
        print("file should be contained in /content/drive/My Drive/Colab Notebooks/sabeco3/")
        file_path =  "/content/drive/My Drive/Colab Notebooks/sabeco3/"+file_name
        data1 = load_from_json(file_path)
        data = convert_to_numpy(data1)
        return data
        # self.input   =  Input(data, name = "input from file")


    def visualize_input(self):

        data = self.data

        colors = list(mcolors.CSS4_COLORS.keys())
        colors =  rd.shuffle(colors)

        # visualize vị trí của kho và NPP
        location_TCO = data['loc_h']
        location_cus = data['loc_c']
        print("location_TCO", type(location_TCO), location_TCO[:, 0] )
        plt.plot( location_TCO[:, 0], location_TCO[:, 1], "rs")
        plt.plot( location_cus[:, 0], location_cus[:, 1], "bo")
            # fake_data['cluster_physic_depot'] = [[0],[1]]
        plt.show()

        figure(figsize=(8, 6), dpi=80)
        # visualize số lượng két thùng của lượng hàng tồn kho, deamnd NPP và lượng tồn kho an toàn
        X = ["SKU " +str(i) for i in range(data['num_products'])]
        for day in range(1):
            supply_list = data['inventory'][day]
            demand_list = data['matrix_demand'][day]
            safety_stock = data['safety_stock'][day] # lượng hàng tồn kho an toàn tính theo từng SKU đơn vị két thùng, và được tính bằng số ngày bán hàng, được tính bằng một module khác.
            X_axis = np.arange(data['num_products'])
            print("sum supply",  np.sum(supply_list, axis=0))
            plt.bar(X_axis - 0.2, np.sum(supply_list, axis=0) , 0.1, label = 'inventory')
            plt.bar(X_axis , np.sum(demand_list, axis=0) , 0.1, label = 'demand')
            plt.bar(X_axis + 0.2, np.sum(safety_stock, axis=0) , 0.1, label = 'safety_stock')

            plt.xticks(X_axis, X)
            plt.xlabel("Mã SKU")
            plt.ylabel("số lượng ket/thùng")
            plt.title("số lượng két/thùng từng mã của lượng hàng tồn kho và lượng hàng cần của NPP ngày "+str(day))
            plt.legend()
            plt.show()

    def visualize_capacity_physic_depot(self):

        data = self.data
        # X = ["SKU " +str(i) for i in range(data['num_products'])]
        capacity_PD = data['capacity_physic_depots']
        demand_matrix = data['matrix_demand']
        limitOut = data['limit_out']

        for day in range(num_priods):
                # creating the dataset
            data = {' Tổng capacity kho vật lý':np.sum(capacity_PD), 'Tổng năng lực xuất nhập': np.sum(limitOut),\
                    'Tổng demand NPP': np.sum(np.sum(demand_matrix[day], axis=1))}
            courses = list(data.keys())
            values = list(data.values())

            figure(figsize=(8, 5), dpi=80)

            # creating the bar plot
            plt.bar(courses, values, color ='maroon',
                    width = 0.1)

            plt.xlabel("Đối tượng")
            plt.ylabel("Số lượng két/thùng")
            plt.title("Tổng số lượng két thùng của các kho vật lý và các nhà phân phối theo tất cả các SKU ngày " + str(day))
            plt.show()

        # visulize phân phối capacity của các kho vật lý
        mylabels = ["kho vật lý " + str(i) for i in range(len(capacity_PD))]
        plt.pie(capacity_PD, labels = mylabels)
        plt.show()

    def help(self):
        s =  "visualize_input()\ndraw_limit_in()\nget_data()"
        print(s)
    def get_data(self):
        return self.data
    def print(self):
        print(self.data)




"""# Model

![image.png](data:image/png;base64,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Pde4ceMwdfLfkDp1wphzdevWDWOndOjQIYy5Uq1m45YtW+YmTpzo1y8KbNXSdsOGDa5Bgwa+zqif261bt5Zqeauwdt68eX49Wlbi+yqDBw/227F5ROuJznfttdeGMeduuummMAYAAACgIopOkDwhotHlN7t3lo8LUzC/eG69e2LZblen9al+APfveNH9r++0dv9449+EGpimPUe7A9ufCVNAxXXodefJ30873bm1vwg1FffR+19xf3zta+7V5b8MNUBuW7t2revWrVuYKv5SEQAAAEDNRYtbIA1TFq5zZzQs/VbuOk3au8ef4o30QFX462+0cscPnRWmsuP4oTNdq0tLtywEAAAAACBXENwCZViwfIv70ll13Xn1moaaYpr+4ow6/nMAlavP313tjr93+iPlFaH13fLtHmEKAAAAAIDcQnALlOGfn1znzryguG/buFqNr/CfA6hcf3/d1e6LD2u5Q384J9RUjNbz6fFz/XoBAAAAAMhFBLdACi+s3u4++vwMV6vhpaGmNNUf/+wMPx+AynPWWV9xk3/8v9xb2xq6Lz6r2D9dWv6tbQ3cxDFD/HqBfFGrVq0wVvwiMgAAAAA1G8EtkMJjT653Z1+YuLWtOa9Rezd14fowBaCy/N01HdyA71zndr9asS4Tfr/tfHdDz79xf/93p17yBOSDdu3a+ReSadi9e3eoBQAAAFBTEdwCSazc9Dt34Mgnrk6jr4eaxPT52wc/8fMDqFzjfzjEXXDu19xvN9R3n3385VCbHs2/Z/OFrvZXmrn/++MHQi0AAAAAALmJ4BZI4vEn17lzymhta9TqdtrT9HULVIVfPfWo6/PNb7v/WtHY/XHPeaE2Nc33XyuauJ5X9XS/fvrxUAsAAAAAQO4iuAUS2LD9LffbfQddvSZtQ01qmu83bx70ywGofBNGft89+4sJruj91u53L1/i3n6jlntv37klrXBValr1e9a38PPNmzbGLwcAAAAAQD4oOqGO0oCg0eU3u3eWjwtTheuOH891u49f6Go1viLUlO3QvlfdX9V718368aBQU7ia9hztDmx/JkwBletXa7a45f+50a3dsNUdPPy+e//9T12dOme7BvVquQ7tWrsbe3Z33+rWIcwNAAAAAEB+ILhFKQS3zu3Yvd/1G/GvrvnVg0NN+va+PN09Pem/u7atGoeawkRwCwAAAAAAUDF0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hZqK0Xr+ckZ9v14AAAAAAHINwS0AIC88vXidO3HuJWEqO85t0MI9v/yVMAXUDNu2bXOTJk1yS5YsCTVAMd0Tujd0jwAAACD3EdwCAPLCG3vedufWvShMZYfW99rOt8IUkBtGjx7tioqKEg69evVy06dPd3v37g1zn27EiBF+uO2220INUKxPnz7+3pgwYUKoAQAAQC4juAUA5IXDh4+4M876apjKDq3v2LFjYQrIDVu2FL80r2XLlq5nz54lg6aXL1/uhgwZ4sfVcjKRDh06+LJz586+LI8BAwb4oFghMaqfroOuh65LRXTs2NGXV155pS8BAACQ2whuAQB5o6iIf7ZQOO6++263bNmykmH37t1uz549rn///v5ztZxU69y4cePGuRMnTvhlyuvo0aO+5IuN3GDXwa5LeW3atMnfG8OHDw81AAAAyGX8BQwAyAsNG9Rzn39yPExlxxeffuDq1asbpoDc16JFCzd//nw3ceJEPz1+/Hi3du1aPw4AAACgZiG4BQDkhb9u09x9dHR/mMqOj47+0bW6tGmYAvKHWkyq+wR56KGHfGlSPVavl1JZNwgaWrVqVarLBfWhq3p1ySBq1Wvz1q9f39fJoUOH/HY0v+ptHk0neymabVf7oD56hw0bVrKs9iNVtwzanvazU6dOJdvSMlpHov5+4+vXoO1n+sK2RPts69O+RNenAN3On20vWV/ECt/1uY4hur549xea1me6DqLrYvNriL5kTMdq10jrt2PXPhk7nui5tmPS9uN03u2c87I7AACAqkdwCwDIC33+rov79OibYSo7tL7+f//NMAXklzvuuMOXCvMUsJlkj9Ur5Gvfvr1bsGBBSf+5hw8f9qGgBXnqH1f19erV89PRfnZ79Ojh66RLly6+r11t2+axPnj1AiwFh3G2P6+88orva3Xq1Km+H14tpy4gtL5EXT/o2BQ+aj83b95csj/ad61DwWOUjtPWr/DS9k3HrX1L1jdwIon22danfdH6FGhqnd26dXMbN270n4u2p2Wi10a0vwMHDvSfi+bXfFqfjjF6PM2aNSvZnui6aNqGWrVq+Xo5cuSIH3QttX6Ni4XwkqgLjPvvv9+X2n48PJ85c6av1/717t071AIAAKCqENwCAPLC3193tTvx6SH3/ru7Q03FaD1ffHzQrxfIR23atAljzu3cuTOMJTdhwgRfqpsF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)

MODEL

Biến: $X_i^j$ : biến nhị phân, có vận chuyển hàng hoá từ i đến j.

Ràng buộc:

1. Mỗi khách hàng chỉ nhận hàng từ một kho.
$$ \sum_i X_i^j \le 1 $$

2. Tổng lượng hàng xuất đi luôn bé hơn hoặc bằng lượng hàng tồn kho:
$$ \sum_j X_i^j D_j^{kt} \le \text{Inventory}_i^{kt}, \text{với mọi k,t} $$

3. Lượng hàng xuất đi luôn bé hơn hoặc bằng khả năng xuất của kho.
$$ \sum_{i \text{ in} C_d} \sum_j X_{i}^j (\sum_k D_j^{kt}) \le \text{limitOut}_d \text{ với mọi t}$$

4. Ràng buộc giữa NPP và TCO

Hàm chi phí:

$$ \text {min } \sum_t (\sum_j (1 - \sum_i X_i^j)*(\sum_k D_j^{kt}) *M + \sum_i H_i (\sum_j X_i^j \sum_k D_j^{kt}) + \sum_i \sum_j X_i^j \sum_k D_j^{kt} * \text{cost_sku}_k * \text{cost_logistic}_i^j ) $$

## SCIP model

## create the variable
"""

def create_data(model, data):

    x = {}
    for depot_idx in range(data['num_depots']): #kho
        for cus_idx in range(data['num_customers']): # khách hàng
            x[depot_idx,cus_idx] = model.NewIntVar(0, 1, '')
    return x

"""## create constraints

4. Ràng buộc giữa NPP và TCO
"""

# Kho -  NPP
def add_constraint_depot_cus(model, data,x):
    for dep_idx in range(data['num_depots']):
        for cus_idx in range(data['num_customers']):
            if data['mat_config_DC'][dep_idx][cus_idx] == 0:
                model.Add(x[dep_idx,cus_idx] == 0)

"""1. Mỗi khách hàng chỉ nhận hàng từ một kho.
$$ \sum_i X_i^j \le 1 $$
"""

def add_constraint_cus_one_depot(model, data,x):
    for cus_idx in range(data['num_customers']):
        model.Add(sum( [x[dep_idx,cus_idx] for dep_idx in range(data['num_depots'])] ) <=1)





"""3. Đối với từng kho vật lý, Lượng hàng xuất đi luôn bé hơn hoặc bằng khả năng xuất của kho đó.
$$ \sum_{i \text{ in } C_d} \sum_j X_{i}^j (\sum_k D_j^{kt}*W_k) \le \text{limitOut}_d $$
"""

def add_constraint_limitOut(model, data,x):
    for day in range(data['num_priods']):
        for physic_depot_id in range(data['num_physic_depots']):
            cluster = data['cluster_physic_depot'][physic_depot_id]

            # weight_requets = sum([data['matrix_demand'][day,:,prod_id]*data['ratio_capacity'][prod_id] for prod_id in range(data['num_products']) ])
            # print("weight_requets", weight_requets)
            demand_of_physicDepot = sum([ x[dep_idx, cus_idx]*sum([data['matrix_demand'][day,cus_idx,prod_id]*\
                                                                   data['ratio_capacity'][prod_id] for prod_id in range(data['num_products']) ]) \
                                         for cus_idx in range(data['num_customers']) for dep_idx in cluster ])

            model.Add( demand_of_physicDepot <= data['limit_out'][physic_depot_id])
            model.Add( demand_of_physicDepot <= data['capacity_physic_depots'][physic_depot_id])


"""## Cost function

$$ \text {min } \sum_t (\sum_j (1 - \sum_i X_i^j)*(\sum_k D_j^{kt}) *M + \sum_i H_i (\sum_j X_i^j \sum_k D_j^{kt}) + \sum_i \sum_j X_i^j \sum_k D_j^{kt} * \text{cost_sku}_k * \text{cost_logistic}_i^j ) $$

--> $$ min \sum_j \sum_i X_i^j *(-M*(\sum_t \sum_k D_j^{kt}) +  H_i \sum_k \sum_t D_j^{kt} + \sum_k \sum_t D_j^{kt} * \text{cost_sku}_k * \text{distance}_i^j)  $$
tương đường: hàm phạt nếu không giao được hàng + chi phi bốc dỡ tại kho + chi phí logistics
"""

def create_coefficent(data,dep_idx,cus_idx, M ):

    cost_penalty_drop = -M*float(np.sum(data['matrix_demand'][:,cus_idx,:]))

    cost_boc_xep_hang  =   float(data['handling_cost_out'][dep_idx]*np.sum(data['matrix_demand'][:,cus_idx,:]))

    cost_vanchuyen = float(sum(sum(data['matrix_demand'][:, cus_idx, sku_id])* data['weight_product'][sku_id]\
                               for sku_id in range(data['num_products']))) * data['OB_transport_cost'][dep_idx][cus_idx]

    cofficient = cost_penalty_drop + cost_boc_xep_hang + cost_vanchuyen
    return cofficient

def create_cost_function(model, data,x, M):

    coefficient_N = sum( create_coefficent(data,dep_idx,cus_idx, M )* x[dep_idx, cus_idx] \
                        for dep_idx in range(data['num_depots']) for cus_idx in range(data['num_customers']) )

    model.Minimize(coefficient_N)

"""# Visualize output

#Output
"""

class Output:

    def __init__(self, output, data):
        self.output= output
        self.data= data

    def visualize_output(self):
        data = self.data
        output =  self.output
        if output.any() == False:
            return False

        # visualize vị trí của kho và NPP
        location_TCO = data['loc_h']
        location_cus = data['loc_c']
        plt.plot(location_TCO[:, 0], location_TCO[:, 1], "rs")
        plt.plot(location_cus[:, 0], location_cus[:, 1], "bo")

        for dep_idx in range(data['num_depots']):
            for cus_idx in range(data['num_customers']):
                if output[dep_idx, cus_idx] >0:
                    plt.plot([location_TCO[dep_idx][0], location_cus[cus_idx][0]],\
                            [location_TCO[dep_idx][1], location_cus[cus_idx][1]], lw=1)

        plt.show()

    def draw_supply_TCO(self):

        data = self.data
        output =  self.output

        if output.any() == False:
            return False

        bar_width = 0.2
        X_axis = np.arange(data['num_depots'])
        color_list  = list(mcolors.CSS4_COLORS.values())

        for day in range(data['num_priods']):
            figure, axis = plt.subplots(data['num_products'])
            for sku_id in range(data['num_products']):

                bottom_data=  np.zeros((data['num_depots']))

                supply = data['inventory'][day,:,sku_id]

                for cus_idx in range(data['num_customers']):

                    axis[sku_id].bar(X_axis + 0.00, output[:,cus_idx]*data['matrix_demand'][day][cus_idx][sku_id] , bottom = bottom_data,\
                                    color = random.choice(color_list), width = bar_width, label = "KH "+str(cus_idx))

                    bottom_data = bottom_data +  output[:,cus_idx]*data['matrix_demand'][day][cus_idx][sku_id]

                axis[sku_id].bar(X_axis + bar_width, supply, color = "k", width = bar_width, label = "supply")


                axis[sku_id].set_xticks(X_axis, ["TCO "+ str(i ) for i in range(data['num_depots'])])

                axis[sku_id].plot(len(X_axis)+1,0)

                axis[sku_id].legend()
            plt.show()

    def draw_demand(self):


        data = self.data
        output =  self.output

        if output.any() == False:
            return False

        bar_width = 0.2
        X_axis = np.arange(data['num_customers'])
        color_list  = list(mcolors.CSS4_COLORS.values())

        for day in range(data['num_priods']):

            figure, axis = plt.subplots(data['num_products'])

            for sku_id in range(data['num_products']):

                bottom_data=  np.zeros((data['num_customers']))

                demand = data['matrix_demand'][day,:,sku_id]

                for dep_idx in range(data['num_depots']):

                    axis[sku_id].bar(X_axis + 0.00, output[dep_idx,:]*data['matrix_demand'][day,:,sku_id]  ,\
                                    bottom = bottom_data, color = random.choice(color_list), width = bar_width, label = "TCO "+str(dep_idx))

                    bottom_data = bottom_data +   output[dep_idx,:]*data['matrix_demand'][day,:,sku_id]

                axis[sku_id].bar(X_axis + bar_width, demand, color = "k", width = bar_width, label = "demand")


                axis[sku_id].set_xticks(X_axis, ["KH "+ str(i ) for i in range(data['num_customers'])])
                axis[sku_id].plot(len(X_axis)+1,0)

                axis[sku_id].legend()
            plt.show()

    def draw_limitOut(self):

        data = self.data
        output =  self.output

        if output.any() == False:
            return False


        # xử lý data
        capacity_N = np.empty((data['num_priods'], data['num_depots'],data['num_customers'] ,data['num_products']))

        for priod in range(data['num_priods']):
            for dep_idx in range(data['num_depots']):
                for cus_idx in range(data['num_customers']):
                    for item_idx in range(data['num_products']):
                        capacity_N[priod][dep_idx][cus_idx][item_idx] = output[dep_idx, cus_idx] *\
                                                                        data['matrix_demand'][priod][cus_idx][item_idx]*data['ratio_capacity'][item_idx]


        # vẽ
        for priod in range(data['num_priods']):
            bar_width = 0.1
            X_axis = np.arange(len(data['cluster_physic_depot']))
            print("X_axis", X_axis)
            color_list  = [ 'r',  'g', 'b', 'c','m','y', 'navy', 'lime', 'tan', 'coral', 'pink']

            luong_hang_inPD = []
            for physic_depot_id in range(len(data['cluster_physic_depot'])):

                cluster = data['cluster_physic_depot'][physic_depot_id]
                limitIn_cluster = data['limit_out'][physic_depot_id]

                luong_hang_inPD.append(np.sum([ capacity_N[priod, :,depot_idx,:] for depot_idx in cluster]))

            plt.bar(X_axis, luong_hang_inPD, width = bar_width ,edgecolor ='grey', label ='lượng hàng trong kho')
            plt.bar(X_axis + [bar_width]*len(X_axis),  data['limit_out'], width = bar_width ,edgecolor ='grey', label ='lượng hàng giới hạn')


            # axis[0].set_xticks(X_axis, ["kho vật lý "+ str(i ) for i in range(len(data['cluster_physic_depot']))])
            # axis[0].plot(len(X_axis)+1,0)
            plt.legend()
            plt.show()

    def visualize_output_detail(self):

        data = self.data
        output =  self.output

        if output.any() == False:
            return False
        # visualize vị trí của kho và NPP
        location_TCO = data['loc_h']
        location_cus = data['loc_c']
        plt.plot(location_TCO[:, 0], location_TCO[:, 1], "rs")

        # for day in range(data['num_priods']):
        for day in range(1):
            for i in range(data['num_depots']):
                s= "depot "+ str(i) +" sku: "
                for sku_id in range(data['num_products']):
                    s+= " sku "+str(sku_id) + " "+ str(data['inventory'][day][i][sku_id])
                    num_by_sku  = sum([output[i,j]*data['matrix_demand'][day][j][sku_id] for j in range(data['num_customers'])])
                    s+= "  "+ str(round(num_by_sku))
                plt.text(location_TCO[0, 0]-1930, location_TCO[0, 1]-450+150*i, s)
                plt.text(location_TCO[i, 0]+3, location_TCO[i, 1]+5, str(i))
            plt.plot(location_cus[:, 0], location_cus[:, 1], "bo")

            for dep_idx in range(data['num_depots']):
                for cus_idx in range(data['num_customers']):

                    if output[dep_idx, cus_idx] >0:
                        plt.plot([location_TCO[dep_idx][0], location_cus[cus_idx][0]],\
                                [location_TCO[dep_idx][1], location_cus[cus_idx][1]], lw=1)

            plt.title("lượng hàng ngày "+str(day))
            plt.show()

    def get_value(self):
        return self.output
    def get_data(self):
        return self.data
    def print(self):
        print(self.output)
        print(self.data)

    def help(self):
        s="List Functions:\nvisualize_output()\ndraw_supply_NM\ndraw_demand\ndraw_check_limitIn\nget_value\nget_data"

        print(s)

"""## Solver

# New Section

# New Section
"""

class VarArraySolutionPrinterWithLimit(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.__solution_limit = limit
        self.best_solution = None

    def on_solution_callback(self):
        self.__solution_count += 1
        print(f'Solution {self.__solution_count}:')
        print(f'Objective {1 - self.ObjectiveValue()}:')

        if self.best_solution is None or self.ObjectiveValue() < self.best_solution.ObjectiveValue():
            self.best_solution = self

        if self.__solution_count >= self.__solution_limit:
            print(f'Stop search after {self.__solution_limit} solutions')
            self.StopSearch()


    def solution_count(self):
        return self.__solution_count

"""#ORMODEL"""

def optimize(data, limit_time_s, num_of_solution, cost_penalty):

    # Create the mip solver with the SCIP backend.
    time1 = time.time()
    model = cp_model.CpModel()

    x = create_data(model, data)
    add_constraint_depot_cus(model, data,x)
    add_constraint_cus_one_depot(model, data,x)

    add_constraint_limitOut(model, data,x)

    #set objective function by integer variables

    create_cost_function(model, data,x, cost_penalty)

    # Create a solver and solve.
    solver = cp_model.CpSolver()

    # Thiết lập giới hạn thời gian (đơn vị là giây)
    if limit_time_s > 0:
        solver.parameters.max_time_in_seconds = limit_time_s  # Ví dụ: giới hạn 60 giây (1 phút)

    solution_printer = VarArraySolutionPrinterWithLimit(x, num_of_solution)
    # Enumerate all solutions.
    solver.parameters.enumerate_all_solutions = True

    # Solve.
    if num_of_solution > 0:
        status = solver.Solve(model, solution_printer)
    else:
        status = solver.Solve(model)

    print(f"Status = {solver.StatusName(status)}")
    print(f"Number of solutions found: {solution_printer.solution_count()}")

    output = {}
    X = np.zeros((data['num_depots'],data['num_customers']), np.int_)

    if status == cp_model.OPTIMAL :
        print(f"Minimum of objective function: {1 - solver.ObjectiveValue()}\n")
        for dep_idx in range(data['num_depots']):
            for cus_idx in range(data['num_customers']):

                if round(solver.Value(x[dep_idx, cus_idx]))  >0:
                    X[dep_idx, cus_idx] = round(solver.Value(x[dep_idx, cus_idx]))
                    # print('depots ', dep_idx, 'cus_idx ', cus_idx, round(solver.Value(x[dep_idx, cus_idx])) )
        return X

    elif solution_printer.best_solution or status == cp_model.FEASIBLE:
        print(f"Minimum of objective function: {1 - solver.ObjectiveValue()}\n")
        for dep_idx in range(data['num_depots']):
            for cus_idx in range(data['num_customers']):

                if round(solver.Value(x[dep_idx, cus_idx]))  >0:
                    X[dep_idx, cus_idx] = round(solver.Value(x[dep_idx, cus_idx]))
                    # print('depots ', dep_idx, 'cus_idx ', cus_idx, round(solver.Value(x[dep_idx, cus_idx])) )
        return X

    else:
        print('Không tìm thấy giải pháp tối ưu hoặc gần đúng.')
        return False

class ORModel:
    def __init__(self, input):
        self.data =  input.data

        self.name_congty =  input.name

        self.info ={"num_of_solution": 5}
        # -ta có thể vẽ đồ thị trong này.
        # self.model =
    def solve(self, limit_time_s, num_of_solution, cost_penalty):
        data= self.data
        self.out_put = optimize(data,  limit_time_s, num_of_solution, cost_penalty)
        result = Output( self.out_put, self.data)
        return result

    def help(self):
        s=""
        s+= "solve( limit_time_s=180, num_of_solution=5, cost_penalty=100_000)"
        print(s)
class HeuristicModel:
    def __init__(self, input):
        self.data =  input.data
        # self.model =
    def solve(self, limit_time_s, num_of_solution, cost_penalty):
        data= self.data
        self.out_put = optimize(data,  limit_time_s, num_of_solution, cost_penalty)
        result = Output( self.out_put, self.data)
        return result
    def help(self):
        s=""
        s+= "solve( limit_time_s=180, num_of_solution=5, cost_penalty=100_000)"
        print(s)

"""To do
- Cho X_ij, xác định chi phí hệ thống 1 năm.

# Tong hop
"""

# get_fake_data("test_DRP_day", num_products, num_depots,num_customers, num_physic_depots, num_priods)

class DrpNgayBackUp:
    def __init__(self, input):
        self.input =  input
        self.output="not been solved"


    def create_model(self, param= "or_model"):
        problem_sabeco = ORModel(self.input)
        self.model =  problem_sabeco

    def solve_drp_ngay(self,  param= "or_model",limit_time_s=180, num_of_solution=5, cost_penalty=100_000):
        self.create_model(param)
        if param == "or_model":
            self.output= self.model.solve(limit_time_s, num_of_solution, cost_penalty)

    def help(self):
        # numpy.sort(a, axis=-1, kind=None, order=None)
        s="\nDrpNgayBackUp.input\nDrpNgayBackUp.output\nDrpNgayBackUp.model\n"
        s+= "\nsolve_drp_ngay(self, limit_time_s, num_of_solution, cost_penalty, param= or_model)\n"
        s+= "\nmain( data_model = None, file_name = None)"
        s+="\nParameters\n data_model: kiểu dữ liệu được truyền vào. \nfile_name: đọc từ file. \n Default: create faked data"
        print(s)


input= Input()
A = DrpNgayBackUp(input)
A.solve_drp_ngay(param= "or_model",limit_time_s=20, num_of_solution=15, cost_penalty=100_000)