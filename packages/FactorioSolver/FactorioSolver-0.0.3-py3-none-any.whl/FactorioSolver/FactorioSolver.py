import pandas as pd
import json
import igraph as ig
import numpy as np
import matplotlib.pyplot as plt
import importlib.resources

class Model:
    """
    Main class of the library. This contains an internal model of the Factorio data, with utility functions to gather informations about products, recipes and production
    """

    sSpaceAssemblyCategories = [
        "advanced-crafting",
        "basic-crafting",
        "crafting",
        "crafting-or-electromagnetics",
        "crafting-with-fluid",
        "space-crafting"
        ]

    sAsm3Categories = [
        "advanced-crafting",
        "basic-crafting",
        "crafting",
        "crafting-or-electromagnetics",
        "crafting-with-fluid"
        ]

    def __init__(self, recipes_path:str="", choice_map_path:str="", items_path:str="", categories_filter:list=sSpaceAssemblyCategories):
        """
        Instance of FactorioSolver
        
        :param recipes_path:           path to the dataset file.
        :param choice_map_path:     path to the choice map json file
        :param items_path:          path to the items file
        :param categories_filter:   list of names of the product categories you want to include in the model. Categories used in the space assembly by default
        """
    
        self.mRawRecipes = None
        self.mRawItems = None
        self.mRecipes = None
        self.mProducts = None
        self.mDefaultDeliveryDeltaTime = 30.0
        
        recipes_path_or_buffer = recipes_path
        if recipes_path_or_buffer == "":
            recipes_path_or_buffer = importlib.resources.files('data').joinpath('recipes.csv')

        items_path_or_buffer = items_path
        if items_path_or_buffer == "":
            items_path_or_buffer = importlib.resources.files('data').joinpath('items.csv')

        choice_map_path_or_buffer = choice_map_path
        if choice_map_path_or_buffer == "":
            choice_map_path_or_buffer = importlib.resources.files('data').joinpath('default_choice_map.json')

        self._load_data(recipes_path_or_buffer, choice_map_path_or_buffer, items_path_or_buffer, categories_filter)
        
    def _get_amount(self, x,key):
        return 1 if (not key in x) or (type(x[key]) == float and np.isnan(x[key])) else x[key]
    
    def _link_line(self, x):
        return pd.Series({ 
            "out": self.mProducts.loc[x["products"]["name"]]["index"], 
            "in": self.mProducts.loc[x["ingredients"]["name"]]["index"], 
            "name":     x.name,  
            "category": x["category"], 
            "group":    x["group"], 
            "subgroup": x["subgroup"],
            "time":     x["time"], 
            "in.amount": self._get_amount(x["ingredients"], "amount"), 
            "out.amount": self._get_amount(x["products"], "amount") 
        })

    def _load_data(self, recipes_path_or_buffer:str, choice_map_path_or_buffer:str, items_path_or_buffer:str, categories_filter:list=sAsm3Categories):

        # Load the data file
        self.mRawRecipes = pd.read_csv(recipes_path_or_buffer, sep='|')
        self.mRawItems  = pd.read_csv(items_path_or_buffer)
        self.mChoiceMap = pd.read_json(choice_map_path_or_buffer)

        # Setup recipe data set
        recipes = self.mRawRecipes
        recipes["ingredients"] = recipes["ingredients"].apply(json.loads)
        recipes["products"] = recipes["products"].apply(lambda x : x.replace(',"amount":}', '}')).apply(json.loads)
        recipes = recipes.set_index("name")
        recipes = recipes[recipes["category"].apply(lambda x : x in categories_filter)]
        recipes['index'] = recipes.reset_index().index
        recipes["ingredients"] = recipes.apply(lambda x: [i for i in x["ingredients"] if (x.name != i["name"])], axis=1)

        recipes = recipes.drop(labels=recipes[recipes.index.str.contains('barrel', case=False, regex=True)][1:].index)

        self.mRecipes = recipes

        # Setup product data set
        unrolled_recipes = recipes.explode("ingredients").explode("products")
        products = pd.DataFrame({"name":pd.concat([unrolled_recipes["ingredients"], unrolled_recipes["products"]]).dropna().apply(lambda x : x["name"]), "type" : pd.concat([unrolled_recipes["ingredients"], unrolled_recipes["products"]]).dropna().apply(lambda x : x["type"])})
        products = products.drop_duplicates().set_index("name")

        assert not products["type"].hasnans
        products = pd.concat([products, self.mRawItems.set_index("name")], axis=1)
        products.loc[products["type"].isna(), "type"] = "item"

        products["index"] = products.reset_index().index
        products["name"] = products.index

        self.mProducts = products

        links = unrolled_recipes.dropna(subset=["ingredients", "products"]).apply(self._link_line, axis=1)
        vertices = products.set_index("index")
        graph = ig.Graph.DataFrame(vertices=vertices, directed=True, edges=links)
        #graph.es["width"] = 0.3
        graph.es["prod_ratio"] = [e["in.amount"] / e["out.amount"] for e in graph.es]
        
        self.mDataGraph = graph

    def get_products(self):
        """
        Get the products known by the model
        """
        return self.mProducts
    
    def get_recipes(self):
        """
        Get the recipes known by the model
        """
        return self.mRecipes

    def get_data_graph(self):
        """
        Get the data graph
        """
        return self.mDataGraph
    
    def get_product_usage_graph(self, product_name:str):
        """
        Get the a DAG representing the recipes using the specified product.
        
        :param product_name: name of the product
        """
        base_graph = self.mDataGraph
        sub = base_graph.subgraph(base_graph.subcomponent(base_graph.vs.select(name_eq=product_name)[0], mode="in"))
        return sub

    def get_products_info(self, search_name:str):
        """
        Get information about all the products which contain the search_name. returned as a Pandas data frame
        
        :param search_name: the name to search
        """
        return self.mProducts[self.mProducts.index.str.contains(search_name)]

    def _compute_subgraph(self, products:dict):
        graph = self.mDataGraph.copy()
        graph.vs["output_amount"] = 0
        for key, val in products.items():
            graph.vs.select(name_eq=key)["output_amount"] = val

        return graph.subgraph(list(set([v for i in graph.vs.select(output_amount_gt=0.1) for v in graph.subcomponent(i, mode="out")])))

    def get_choice_list(self, product_name = None, choice_map = None):
        """
        Get the list of choices to solve before being able to display a production graph. They correspond to the multiple ways a product can be created
        You can specify a choice map to specify the choices already made

        :param product_name: the name of a product for which to get the choice list
        :param choice_map: to specify the choices already made, see get_choice_map
        """
        graph = self.mDataGraph
        if product_name is not None:
            if type(product_name) == str:
                graph = self._compute_subgraph({product_name:1})
            if type(product_name) == dict:
                graph = self._compute_subgraph(product_name)

        if type(choice_map) is not type(None):
            graph = graph.copy()
            self._apply_choice_map(graph, self.mChoiceMap)

        choices_verts = graph.vs.select(lambda x : len(set([e["name"] for e in x.out_edges()])) > 1)
        l = [list(set([e["name"] for e in x.out_edges()])) for x in choices_verts]
        return [v for v in l if (len(v) > 1)]
    
    def get_choice_map(self):
        """
        Get the map of the choices currently made, which is a data frame containing a column "Possibilities" with the list of recipes possible, and a column "Choices" with the name of the selected recipe
        """
        return self.mChoiceMap
    
    def set_choice_map(self, choice_map:pd.DataFrame):
        """
        Set the choice map
        :param choice_map: a Panda DataFrame representing the choices, see get_choice_map
        """
        self.mChoiceMap = choice_map

    def get_default_delivery_delta_time(self):
        return self.mDefaultDeliveryDeltaTime

    def set_default_delivery_delta_time(self, delivery_delta_time:float):
        """
        Set the default delivery delta_time, used to estimate the quantity to transport in the production graph
        :param delivery_delta_time: The delta_time at which a product will be delivered
        """
        self.mDefaultDeliveryDeltaTime = delivery_delta_time

    def _in_notebook():
        try:
            from IPython import get_ipython
            if 'IPKernelApp' not in get_ipython().config:  # pragma: no cover
                return False
        except ImportError:
            return False
        except AttributeError:
            return False
        return True

    def print_product_usage(self, product_name:str, figsize=(30, 10), show_fig:bool=not _in_notebook(), file_name:str=""):
        """
        Print the product usage graph, which is a DAG representing the recipes using the specified product.
        :param product_name:    The name of the product to verify the usage from
        :param figsize:         The size of the figure to print
        :param show_fig:        Should we show automatically the figure? You can also set it to false and call plt.show() manually. By default it will show only if not in a jupyter notebook
        :param file_name:       Save the file with file_name. If this is used, the figure will not be shown
        """
        plt.clf()
        fig,ax = plt.subplots(figsize=figsize)
        sub = self.get_product_usage_graph(product_name)
        ig.plot(sub, layout="sugiyama", edge_align_label=False, vertex_label=sub.vs["name"], vertex_size=0.2, edge_background="white", edge_label_size=10, edge_label=sub.es["in.amount"], target=ax, margin=100, bbox=[0,0,600, 500])
        if file_name != "":
            plt.savefig(file_name)
            plt.clf()            
        elif show_fig:
            plt.show()

    def print_production_single(self, product_name:str, product_num:int, delivery_delta_times:dict={}, figsize=(30, 17), show_fig:bool=not _in_notebook(), edge_label_background:bool=True, file_name:str = ""):
        """
        Print production graph, which is a DAG representing the resource necessary to create a product

        :param product_name:            The name of the product to create
        :param product_num:             The amount of product to create
        :param delivery_delta_times:    Products delivery times in a dictionary with the name of the items as the key and the time as the value. eg. {"ItemA":time_a, "ItemB":time_b}
        :param figsize:                 The size of the figure to print
        :param show_fig:                Should we show automatically the figure? You can also set it to false and call plt.show() manually. By default it will show only if not in a jupyter notebook
        :param edge_label_background:   If true, will draw a background behind the edges label
        :param file_name:               Save the file with file_name. If this is used, the figure will not be shown
        """
        self.print_production({product_name:product_num}, delivery_delta_times, figsize, show_fig, edge_label_background, file_name)
    
    def print_production(self, produced_items:dict, delivery_delta_times:dict={}, figsize=(30, 20), show_fig:bool=not _in_notebook(), edge_label_background:bool=True, file_name:str = ""):
        """
        Print production graph, which is a DAG representing all the resources necessary to create a set of products

        :param produced_items:          All the products to output shown in a dictionary with the name of the items as the key and the quantity required as the value. eg. {"ItemA":quantity_a, "ItemB":quantity_b}
        :param delivery_delta_times:    Products delivery times in a dictionary with the name of the items as the key and the time as the value. eg. {"ItemA":time_a, "ItemB":time_b}
        :param figsize:                 The size of the figure to print
        :param show_fig:                Should we show automatically the figure? You can also set it to false and call plt.show() manually. By default it will show only if not in a jupyter notebook
        :param edge_label_background:   If true, will draw a background behind the edges label
        :param file_name:               Save the file with file_name. If this is used, the figure will not be shown
        """
        fig, ax = plt.subplots(figsize=figsize)
        plt.margins(0.04, 0.04)
        
        assert len(self.get_choice_list(produced_items, self.mChoiceMap)) == 0, "Multiple possible recipes to choose from, please check the choices left via print_choice_list and choose which recipe to use via the choice map"

        draw = self.compute_prod_graph(produced_items, delivery_delta_times)

        title = ""
        if len(produced_items) == 1:
            title += '"' + [key for key in produced_items][0] + '" '

        sub_max_time = max(draw.vs["prod.time"])
        title += "Production Graph"
        title += f"\n Minimal Production Time : {sub_max_time} s"
        plt.title(title)

        item_color          = "lightblue"
        base_product_color  = {"fluid":"Aqua", "item":"Burlywood"}
        needed_color        = "LightCoral"

        draw.vs["desc"]     = [f'{v["name"]}'
                            + f'\n ---------------' 
                            + f'\n Tot: {v["total"]:.1f}'
                            + f'\n y/2={v["belt_count.y"]:.1f},s={v["del_stacks"]}x{v["stack_size"]:.0f}'
                            + (f'\n Final {v["output_amount"]}' if v["output_amount"] else "")
                            + f'\n Prod speed: {v["prod_per_s"]:.1f} / s'
                            + f'\n Factories count: {v["factory_count"]}'
                            + f'\n Time: {v["prod.time"]} s'
                            for v in draw.vs]

        labels = [f'  in:{e["in.amount"]}\n(y/2:{e["belt_count.y"]:.1f})\n  out:{e["out.amount"]}' for e in draw.es]

        draw.vs["color"]    = [needed_color if v["output_amount"] > 0 else (base_product_color[v["type"]] if v.outdegree() == 0 else item_color) for v in draw.vs]
        ig.plot(draw, layout="sugiyama", edge_align_label=False, vertex_label=draw.vs["desc"], vertex_shape="square", vertex_label_size=10, vertex_label_color="black", vertex_size=0.7, edge_background="white" if edge_label_background else "#FFF0", edge_width=0.3, edge_label_size=10, edge_label=labels, target=ax, margin=100, bbox=[0,0,1000, 500])

        if file_name != "":
            plt.savefig(file_name)
            plt.clf()
        elif show_fig:
            plt.show()

    def _apply_choice_map(self, graph, choice_map):
        ex = choice_map.explode("Possibilities")
        edges_to_del = ex.set_index("Possibilities").drop(ex["Choice"]).index

        for name in edges_to_del:
            graph.delete_edges(graph.es.select(name_eq=name))

        return graph

    def compute_prod_graph(self, item_list:dict, delivery_delta_times:dict={}):
        graph = self.mDataGraph.copy()
        graph.vs["output_amount"] = 0
        for key, val in item_list.items():
            graph.vs.select(name_eq=key)["output_amount"] = val

        self._apply_choice_map(graph, self.mChoiceMap)

        graph.vs["prod.time"] = 1
        graph.vs["prod.amount"] = 1
        for i, v in enumerate(graph.vs):
            for j, e in enumerate(v.out_edges()):
                if j == 0:
                    v["prod.time"] = e["time"]
                    v["prod.amount"] = e["out.amount"]
                else:
                    assert v["prod.time"] == e["time"], "Error multiple times in out edges: multiple recipes?"
                    assert v["prod.amount"] == e["out.amount"], "Error multiple production amounts in out edges: multiple recipes? Please check there is no choices left via print_choice_list and choose one recipe via the choice map"
        
        graph = graph.subgraph(list(set([v for i in graph.vs.select(output_amount_gt=0.1) for v in graph.subcomponent(i, mode="out")])))
        graph.vs["total"] = 0
        graph.vs["prod_time"] = 0
        graph.vs["prod_per_s"] = 1
        graph.vs["factory_count"] = 0
        graph.vs["del_dt"] = self.mDefaultDeliveryDeltaTime
        for key, val in delivery_delta_times.items():
            graph.vs.select(name_eq=key)["del_dt"] = val

        for v in graph.vs[graph.topological_sorting(mode='out')] :
            v["total"] = v["output_amount"]
            for e in v.in_edges():
                v["total"] += (graph.vs[e.source]["total"] * e["prod_ratio"])
            v["prod_per_s"]      = v["prod.amount"] / v["prod.time"]
            v["factory_count"]   = int(np.ceil(v["total"] / v["prod_per_s"]))
            v["del_stacks"]      = int(np.ceil((v["total"] * v["del_dt"]) / v["stack_size"]))

        belt_item_per_s = {"y":15, "r":30, "b":45}
        graph.es["belt_count.y"]   = [graph.vs[e.source]["total"] * e["prod_ratio"] / (belt_item_per_s["y"] * 0.5) for e in graph.es]
        graph.vs["belt_count.y"]   = [v["total"] / (belt_item_per_s["y"] * 0.5) for v in graph.vs]

        return graph

def get_products_info(*args, **kwargs):
    """
    Get information about all the products which contain the search_name. returned as a Pandas data frame
       
    :param search_name: the name to search
    """
    model = Model()
    model.get_products_info(*args, **kwargs)

def print_production(*args, **kwargs):
    """
    Print production graph, which is a DAG representing all the resources necessary to create a set of products

    :param produced_items:          All the products to output shown in a dictionary with the name of the items as the key and the quantity required as the value. eg. {"ItemA":quantity_a, "ItemB":quantity_b}
    :param delivery_delta_times:    Products delivery times in a dictionary with the name of the items as the key and the time as the value. eg. {"ItemA":time_a, "ItemB":time_b}
    :param figsize:                 The size of the figure to print
    :param show_fig:                Should we show automatically the figure? You can also set it to false and call plt.show() manually. By default it will show only if not in a jupyter notebook
    :param edge_label_background:   If true, will draw a background behind the edges label
    :param file_name:               Save the file with file_name. If this is used, the figure will not be shown
    """
    model = Model()
    model.print_production(*args, **kwargs)

def print_production_single(*args, **kwargs):
    """
    Print production graph, which is a DAG representing the resource necessary to create a product

    :param product_name:            The name of the product to create
    :param product_num:             The amount of product to create
    :param delivery_delta_times:    Products delivery times in a dictionary with the name of the items as the key and the time as the value. eg. {"ItemA":time_a, "ItemB":time_b}
    :param figsize:                 The size of the figure to print
    :param show_fig:                Should we show automatically the figure? You can also set it to false and call plt.show() manually. By default it will show only if not in a jupyter notebook
    :param edge_label_background:   If true, will draw a background behind the edges label
    :param file_name:               Save the file with file_name. If this is used, the figure will not be shown
    """
    model = Model()
    model.print_production_single(*args, **kwargs)

def print_product_usage(*args, **kwargs):
    """
    Print the product usage graph, which is a DAG representing the recipes using the specified product.
    :param product_name:    The name of the product to verify the usage from
    :param figsize:         The size of the figure to print
    :param show_fig:        Should we show automatically the figure? You can also set it to false and call plt.show() manually. By default it will show only if not in a jupyter notebook
    :param file_name:       Save the file with file_name. If this is used, the figure will not be shown
    """
    model = Model()
    model.print_product_usage(*args, **kwargs)
    
if __name__ == "__main__":
   print(__name__, type(__name__))