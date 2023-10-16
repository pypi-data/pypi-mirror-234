import pandas as pd
import numpy as np
import random as rd
import matplotlib.pyplot as plt

from matplotlib.pyplot import figure

figure(figsize=(8, 6), dpi=80)

import codecs
import copy

import codecs


# Import necessary modules
import zipfile
import json



"""# Past Data"""

# def test():
#
#     past_data = {}
#     # Read the extracted JSON file
#     with open("data_NPP.json", 'r') as json_file:
#         data_NPP = json.load(json_file)
#
#     # Now you can work with the 'data' variable, which contains the JSON content
#     past_data['demand_matrix']  = np.array(data_NPP['demand_matrix'])
#     past_data['data_encode_demand'] =  data_NPP['data_encode_demand']
#
#     with open("data_NM.json", 'r') as json_file:
#         data_NM = json.load(json_file)
#     past_data['supply_matrix'] = np.array(data_NM['supply_matrix'])
#     past_data['data_encode_supply'] = data_NM['data_encode_supply']
#
#
#
#
#
#
#     data_json_plan = json.load(codecs.open('new_input.json',  'r', 'utf-8-sig'))
#


"""## supply simulation"""

def convert_to_dictionary(items, key_field):
    """
    Tạo từ điển ánh xạ cho danh sách các mục.

    Parameters:
        - items: Danh sách các mục cần ánh xạ.
        - key_field: Tên trường sẽ làm khóa trong từ điển ánh xạ.

    Returns:
        - item_dict: Từ điển ánh xạ với key là giá trị của trường key_field.
    """

    dict_index_item = {}
    dict_item_index = {}

    for item_index, item in enumerate(items):

        item_code = item[key_field]
        dict_index_item[item_index] = item_code
        dict_item_index[item_code] = item_index

    return dict_index_item, dict_item_index

def get_supply_matrix_planning_all_year(factories,products ):
    '''
    ma trận thể hiện kế hoạch sản xuất của nhà máy với từng sản phẩm, kích thước (len(factories), len(products))
    '''

    dict_index_factory, dict_factory_index = convert_to_dictionary(factories, 'factoryCode')
    dict_index_product, dict_product_index = convert_to_dictionary(products, 'productCode')

    # supply
    matrix_plan_supply_max = np.zeros((len(factories), len(products)), np.int_)
    matrix_plan_supply_min = np.zeros((len(factories), len(products)), np.int_)
    fixed_cost_sku_per_factory = np.zeros((len(factories), len(products)), np.int_)

    for fac in factories:
        fac_Code = fac['factoryCode']
        factory_idx = dict_factory_index[fac_Code]
        products = fac["products"]
        for prod in products:
            prod_c = prod['productCode']
            prod_idx = dict_product_index[prod_c]
            matrix_plan_supply_max[factory_idx][prod_idx] = prod['maxVolume']
            matrix_plan_supply_min[factory_idx][prod_idx] = prod['minVolume']
            fixed_cost_sku_per_factory[factory_idx][prod_idx] = prod['fixedCostbySkuPerFactory']
    return matrix_plan_supply_max, matrix_plan_supply_min, fixed_cost_sku_per_factory

"""## demand"""

def get_demand_matrix_planning_all_year(customers,products ):

    '''
    ma trận thể hiện kế hoạch của nhà khách hàng với từng sản phẩm, kích thước (len(customers), len(products))
    '''
    dict_index_customer, dict_customer_index = convert_to_dictionary(customers, 'customerCode')
    dict_index_product, dict_product_index = convert_to_dictionary(products, 'productCode')

    demand_matrix_planning = np.zeros((len(customers), len(products)), np.int_)

    for cus in customers:
        cus_Code = cus['customerCode']
        cus_idx = dict_customer_index[cus_Code]

        products = cus["products"]
        for prod in products:
            prod_c = prod['productCode']
            prod_idx = dict_product_index[prod_c]
            demand_matrix_planning[cus_idx][prod_idx] = prod['meanDemand']

    return demand_matrix_planning



def get_inventory_safety(depots,products,dict_index_product, safetyOrInventory ):

    safety_stock = np.zeros(( len(depots),len(products)), np.int_) # k (hàng) kho, n mặt hàng (cột)
    for index_depot in range(len(depots)):
        s_safe = depots[index_depot][safetyOrInventory]
        for each_product in  s_safe:
            for code_ix in range(len(products)):
                if each_product['productCode'] == dict_index_product[code_ix]:
                    safety_stock[index_depot, code_ix] = each_product['Capacity']

    return safety_stock

def map_PD_with_D(data_json_plan, dict_index_depot, dict_index_physic_depot):

    num_physic_depots = len(data_json_plan['physicDepots'])
    num_depots =  len(data_json_plan['depots'])
    data_map_PD_D = data_json_plan['mapPhysicDepotWithDepot']

    map_physic_depots_with_depots  = np.zeros((num_physic_depots ,num_depots), np.int_)

    for PD in range(num_physic_depots):
        for D in range(num_depots):
            for loc_pair in data_map_PD_D:
                if loc_pair['depotCode'] == dict_index_depot[D] and loc_pair['physicDepotCode'] == dict_index_physic_depot[PD]:
                    map_physic_depots_with_depots[PD,D] = loc_pair['value']

    return map_physic_depots_with_depots

def get_location(locations, dict_factory_index, dict_depot_index, dict_customer_index ):

    loc_factory = np.empty((len(dict_factory_index),2))
    loc_depot = np.empty((len(dict_depot_index),2))
    loc_customer = np.empty((len(dict_customer_index),2))

    for loc in locations:
        loc_code = loc['locationCode']

        if loc_code in dict_factory_index.keys():
            id_loc_code = dict_factory_index[loc_code]
            loc_factory[id_loc_code][0] =  loc['lat']
            loc_factory[id_loc_code][1] =  loc['lng']

        if loc_code in dict_depot_index.keys():
            id_loc_code = dict_depot_index[loc_code]
            loc_depot[id_loc_code][0] =  loc['lat']
            loc_depot[id_loc_code][1] =  loc['lng']

        if loc_code in dict_customer_index.keys():
            id_loc_code = dict_customer_index[loc_code]
            loc_customer[id_loc_code][0] =  loc['lat']
            loc_customer[id_loc_code][1] =  loc['lng']

    return loc_factory, loc_depot, loc_customer

"""# Main code

## Data model plan
"""

def process_data_plan(data_json_plan):
    '''
    lấy các thông tin trong file kế hoạch để đưa vào mô hình
    '''
    factories = data_json_plan['factories']
    customers = data_json_plan['customers']
    products = data_json_plan['products']
    physic_depots = data_json_plan['physicDepots']
    depots = data_json_plan['depots']
    locations = data_json_plan['locations']

    data_plan = {}

    # Factories
    data_plan['num_factories'] = len(factories)
    data_plan['dict_index_factory'], data_plan['dict_factory_index'] = convert_to_dictionary(factories, 'factoryCode')
    data_plan['supply_matrix_planning_max'], data_plan['supply_matrix_planning_min'], data_plan['fixedCostbySkuPerFactory'] = get_supply_matrix_planning_all_year(factories,products)


    # Customers
    data_plan['num_customers'] = len(customers)
    data_plan['dict_index_customer'], data_plan['dict_customer_index'] = convert_to_dictionary(customers, 'customerCode')
    data_plan['demand_matrix_planning'] = get_demand_matrix_planning_all_year(customers,products)

    # Products
    data_plan['num_products'] = len(products)
    data_plan['unit'] = [prod['unit'] for prod in products]
    data_plan['dict_index_product'], data_plan['dict_product_index'] = convert_to_dictionary(products, 'productCode')

    data_plan['weight_product'] = [prod["weight"] for prod in products]
    data_plan['ratio_capacity'] = [prod["ratio_capacity"] for prod in products]

    # Physics Depot
    data_plan['num_physic_depots'] = len(data_json_plan['physicDepots'])

    data_plan['dict_index_physic_depot'], data_plan['dict_physic_depot_index'] \
                                = convert_to_dictionary(physic_depots, 'depotPhysicCode')
    data_plan['capacity_physic_depots']  = []
    for index_depot in range(len(physic_depots)):
        data_plan['capacity_physic_depots'].append( physic_depots[index_depot]['storageCapacity'])

    data_plan['limit_in']  = []
    for index_depot in range(len(physic_depots)):
        data_plan['limit_in'] .append( physic_depots[index_depot]['limitOutIn']/2)
    print("limit_in", data_plan['limit_in'])

    data_plan['limit_out'] = []
    for index_depot in range(len(physic_depots)):
        data_plan['limit_out'].append( physic_depots[index_depot]['limitOutIn']/2)


    data_plan['fixed_cost'] = []
    for index_depot in range(len(physic_depots)):
        data_plan['fixed_cost'].append( physic_depots[index_depot]['fixedCost'])

    # Depot
    data_plan['num_depots'] = len(depots)
    data_plan['dict_index_depot'], data_plan['dict_depot_index'] = convert_to_dictionary(depots, 'depotCode')
    data_plan['safety_stock'] = get_inventory_safety(depots,products, data_plan['dict_index_product'], 'safetyStock' )
    data_plan['inventory'] = get_inventory_safety(depots, products, data_plan['dict_index_product'], 'inventory' )

    data_plan['handling_cost_in']  = []
    for index_depot in range(len(depots)):
        data_plan['handling_cost_in'] .append( depots[index_depot]['handlingInCost'])

    data_plan['handling_cost_out'] = []
    for index_depot in range(len(depots)):
        data_plan['handling_cost_out'].append( depots[index_depot]['handlingOutCost'])


    distane_f_h = np.empty((len(factories) , len(depots)), np.float_)
    mat_config_FD = np.empty((len(factories) , len(depots)), np.float_)
    IB_transport_cost = np.empty((len(factories) , len(depots)), np.float_)


    FD = data_json_plan['distances']['FD']
    for i in range(len(factories)):
        for j in range(len(depots)):

            for loc_pair in FD:
                if loc_pair['srcCode'] == data_plan['dict_index_factory'][i] and loc_pair['destCode'] == data_plan['dict_index_depot'][j]:
                    distane_f_h[i,j] = loc_pair['distance']
                    mat_config_FD[i,j] = loc_pair['value']


            for pair in data_json_plan['priceByLevelService']['IBtranspCost']:
                if pair['srcCode'] == data_plan['dict_index_factory'][i] and pair['destCode'] == data_plan['dict_index_depot'][j]:
                    IB_transport_cost[i,j] = pair['price']


    distane_h_c = np.empty((len(depots),len(customers)), np.float_)
    mat_config_DC = np.empty((len(depots),len(customers)), np.float_)
    OB_transport_cost = np.empty((len(depots),len(customers)), np.float_)

    DC = data_json_plan['distances']['DC']
    for i in range(len(depots)):
        for j in range(len(customers)):
            for loc_pair in DC:
                if loc_pair['srcCode'] == data_plan['dict_index_depot'][i] and loc_pair['destCode'] == data_plan['dict_index_customer'][j]:
                    distane_h_c[i,j] = loc_pair['distance']
                    mat_config_DC[i,j] = loc_pair['value']

            for pair in data_json_plan['priceByLevelService']['OBtranspCost']:
                if pair['srcCode'] == data_plan['dict_index_depot'][i] and pair['destCode'] == data_plan['dict_index_customer'][j]:
                    OB_transport_cost[i,j] = pair['price']

    data_plan['distane_f_h'] = np.copy(distane_f_h)
    data_plan['distane_h_c'] = np.copy(distane_h_c)

    data_plan['IB_transport_cost'] = np.copy(IB_transport_cost)
    data_plan['OB_transport_cost'] = np.copy(OB_transport_cost)

    data_plan['max_distance'] = data_json_plan['maxDistance']

    data_plan['mat_config_FD'] = np.copy(mat_config_FD)
    data_plan['mat_config_DC'] = np.copy(mat_config_DC)

    data_plan['mat_config_DC'] = np.copy(mat_config_DC)
    data_plan['map_physic_depots_with_depots'] = map_PD_with_D(data_json_plan, data_plan['dict_index_depot'], data_plan['dict_index_physic_depot'])

    data_plan['cluster_physic_depot'] = []

    for cluster_idx in range(len(data_plan['map_physic_depots_with_depots'] )):
        depot_in_cluster = []
        for dep_idx in range(len(depots)):
            if data_plan['map_physic_depots_with_depots'][cluster_idx][dep_idx] == 1:
                depot_in_cluster.append(dep_idx)
        data_plan['cluster_physic_depot'].append(depot_in_cluster)

    data_plan["loc_f"], data_plan['loc_h'], data_plan['loc_c'] = get_location(locations, data_plan['dict_factory_index'], data_plan['dict_depot_index'], data_plan['dict_customer_index'] )


    return data_plan
# process_data_plan(data_json_plan)# process_data_plan(data_json_plan)

def create_simulation_uniformlly(each_factory_idx, each_sku_idx, supply_matrix_planning, days_plan ):
    '''
    hàm để mô phòng phân phối năng lực sản xuất của nhà máy mỗi sản phẩm theo từng ngày với phân phối đều
    '''
    supply_max_each_day = round(supply_matrix_planning[each_factory_idx][each_sku_idx]/days_plan)
    supply_min_each_day = round(supply_matrix_planning[each_factory_idx][each_sku_idx]/days_plan)
    vector_supply_all_day = np.array([supply_max_each_day]*days_plan)
    return vector_supply_all_day

def create_simulation_past_data(total_supply_planning, supply_vector_past,days_plan):
    '''
    hàm để mô phòng phân phối năng lực sản xuất của nhà máy mỗi sản phẩm theo từng ngày với phân phối quá khứ.
    '''
    # tính tổng sản lượng của từng nhà máy, từng mã hàng
    capacity_total = sum(supply_vector_past)

    # tính tỉ lệ điều chỉnh
    scale_factor = total_supply_planning/capacity_total

    return np.round(supply_vector_past*scale_factor)

def create_database_supply( supply_matrix_past, data_encode_supply , data_json_plan, days_plan ):
    '''
    tạo database mô phỏng năng lực sản xuất của nhà máy theo từng sản phẩm theo từng ngày.
    '''
    # trong past data
    NM_code_arr = data_encode_supply['list_whseid_code']
    sku_arr = data_encode_supply['list_sku_code']


    # trong plan data
    data_plan = process_data_plan(data_json_plan)
    supply_matrix_planning_max = data_plan['supply_matrix_planning_max']
    supply_matrix_planning_min = data_plan['supply_matrix_planning_min']

    factory_code_in_json = data_plan['dict_factory_index'].keys()

    sku_code_in_json = data_plan['dict_product_index'].keys()


    supply_max_factory_forcasting = np.zeros((days_plan,  len(factory_code_in_json), len(sku_code_in_json)))
    supply_min_factory_forcasting = np.zeros((days_plan,  len(factory_code_in_json), len(sku_code_in_json)))

    for each_factory_code in factory_code_in_json:
        each_factory_idx = data_plan['dict_factory_index'][each_factory_code]

        # nếu không có nhà máy trong past data
        if each_factory_code not in NM_code_arr:
            for each_sku_code in sku_code_in_json:

                each_sku_idx = data_plan['dict_product_index'][each_sku_code]
                vector_supply_max_all_day  = create_simulation_uniformlly(each_factory_idx, \
                                                                     each_sku_idx, supply_matrix_planning_max, days_plan )
                vector_supply__min_all_day = create_simulation_uniformlly(each_factory_idx, \
                                                                     each_sku_idx, supply_matrix_planning_min, days_plan )

                supply_max_factory_forcasting[:, each_factory_idx, each_sku_idx] = np.copy(vector_supply_max_all_day)
                supply_min_factory_forcasting[:, each_factory_idx, each_sku_idx] = np.copy(vector_supply__min_all_day)


        # khi nhà máy có trong past data
        else:
            for each_sku_code in sku_code_in_json:
                each_sku_idx = data_plan['dict_product_index'][each_sku_code]

                # mã hàng không có trong past data
                if each_sku_code not in sku_arr:

                    vector_supply_max_all_day  = create_simulation_uniformlly(each_factory_idx, \
                                                                     each_sku_idx, supply_matrix_planning_max, days_plan )
                    vector_supply__min_all_day = create_simulation_uniformlly(each_factory_idx, \
                                                                     each_sku_idx, supply_matrix_planning_min, days_plan )

                    supply_max_factory_forcasting[:, each_factory_idx, each_sku_idx] = np.copy(vector_supply_max_all_day)
                    supply_min_factory_forcasting[:, each_factory_idx, each_sku_idx] = np.copy(vector_supply__min_all_day)

                # mã hàng có trong past data
                else:
                    total_supply_planning_max = supply_matrix_planning_max[each_factory_idx,each_sku_idx]
                    total_supply_planning_min = supply_matrix_planning_min[each_factory_idx,each_sku_idx]

                    factory_idx_in_past_data = data_encode_supply['dict_whseid_code'][each_factory_code]
                    sku_idx_in_past_data = data_encode_supply['dict_sku_code'][each_sku_code]
                    supply_vector_past = supply_matrix_past[:, factory_idx_in_past_data, sku_idx_in_past_data]

                    vector_supply_max = create_simulation_past_data(total_supply_planning_max, supply_vector_past,days_plan)
                    vector_supply_min = create_simulation_past_data(total_supply_planning_min, supply_vector_past,days_plan)


                    supply_max_factory_forcasting[:, each_factory_idx, each_sku_idx] = np.copy(vector_supply_max)
                    supply_min_factory_forcasting[:, each_factory_idx, each_sku_idx] = np.copy(vector_supply_min)

    return supply_max_factory_forcasting, supply_min_factory_forcasting

def visulaize_NM(data):
    for i in range(len(data[1])):
        for j in range(len(data[0,0,:])):
            if np.sum(data[:, i, j])==0:
                continue
            plt.plot(data[:, i, j], "k")
            plt.text( 0,data[0, i, j], "NM "+ str(i)+ "sku "+str(j))
        plt.show()
# visulaize_NM(supply_max_factory_forcasting)
# visulaize_NM(supply_min_factory_forcasting)

def create_database_demand( demand_matrix_past, data_encode_demand , data_json_plan, days_plan ):
    '''
    tạo database mô phỏng năng lực sản xuất của nhà máy theo từng sản phẩm theo từng ngày.
    '''
    # trong past data
    customer_code_arr = data_encode_demand['list_customercode_code']

    sku_arr = data_encode_demand['list_sku_code']


    # trong plan data
    data_plan = process_data_plan(data_json_plan)

    demand_matrix_planning = data_plan['demand_matrix_planning']
    customer_code_in_json = data_plan['dict_customer_index'].keys()
    sku_code_in_json = data_plan['dict_product_index'].keys()

    demand_customer_forcasting = np.zeros((days_plan,  len(customer_code_in_json), len(sku_code_in_json)))

    for each_customer_code in customer_code_in_json:

        each_customer_idx = data_plan['dict_customer_index'][each_customer_code]

        # nếu không có KH trong past data
        if each_customer_code not in customer_code_arr:
            for each_sku_code in sku_code_in_json:
                each_sku_idx = data_plan['dict_product_index'][each_sku_code]


                vector_demand_all_day = create_simulation_uniformlly(each_customer_idx, each_sku_idx, demand_matrix_planning, days_plan )
                demand_customer_forcasting[:, each_customer_idx, each_sku_idx] = np.copy(vector_demand_all_day)

        # khi KH có trong past data
        else:
            for each_sku_code in sku_code_in_json:
                each_sku_idx = data_plan['dict_product_index'][each_sku_code]


                # mã hàng không có trong past data
                if each_sku_code not in sku_arr:

                    vector_demand_all_day = create_simulation_uniformlly(each_customer_idx, each_sku_idx, demand_matrix_planning, days_plan )
                    demand_customer_forcasting[:, each_customer_idx, each_sku_idx] = np.copy(vector_demand_all_day)

                # mã hàng có trong past data
                else:
                    total_demand_planning = demand_matrix_planning[each_customer_idx,each_sku_idx]
                    factory_idx_in_past_data = data_encode_demand['dict_customercode_code'][each_customer_code]
                    sku_idx_in_past_data = data_encode_demand['dict_sku_code'][each_sku_code]
                    demand_vector_past = demand_matrix_past[:, factory_idx_in_past_data, sku_idx_in_past_data]



                    vector_demand = create_simulation_past_data(total_demand_planning, demand_vector_past,days_plan)
                    demand_customer_forcasting[:, each_customer_idx, each_sku_idx] = np.copy(vector_demand)

    return demand_customer_forcasting


def simulation_plan(data_json_plan, past_data,days_plan  ):

    demand_matrix = past_data['demand_matrix']
    data_encode_demand = past_data['data_encode_demand']

    supply_matrix = past_data['supply_matrix']
    data_encode_supply = past_data['data_encode_supply']


    data_simulation = {}

    data_simulation['supply_max_factory_forcasting'], data_simulation['supply_min_factory_forcasting'] = \
                    create_database_supply( supply_matrix, data_encode_supply , data_json_plan, days_plan )
    data_simulation['demand_customer_forcasting'] = create_database_demand( demand_matrix, data_encode_demand , data_json_plan, days_plan )

    data_simulation['data_model_plan'] =  process_data_plan(data_json_plan)

    data_simulation['data_model_plan']['supply_max_ver_day'] = np.copy(data_simulation['supply_max_factory_forcasting'])
    data_simulation['data_model_plan']['supply_min_ver_day'] = np.copy(data_simulation['supply_min_factory_forcasting'])
    data_simulation['data_model_plan']['demand_ver_day'] = np.copy(data_simulation['demand_customer_forcasting'])
    data_simulation['data_model_plan']['days_plan'] = days_plan

    with open("datamodel.txt", 'w') as text_file:
    # Chuyển đổi từ điển thành một chuỗi văn bản và ghi vào file
        text_content = str(data_simulation['data_model_plan'] )
        text_file.write(text_content)
    return data_simulation



