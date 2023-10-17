import pandas as pd
import networkx as nx
from virtualitics import vip_plot, vip_dashboard, vip_annotation, vip_object
from virtualitics import exceptions


class VipResult:
    """
    Chassis for any and all responses from VIP
    """
    def __init__(self, results):
        self.data = None
        self.plot = None

        # This is weird - we take in a list of many results, and just keep the last one?
        for result in results:
            if isinstance(result, pd.DataFrame):
                self.data = result
            elif isinstance(result, vip_plot.VipPlot):
                self.plot = result
            elif isinstance(result, nx.Graph):
                self.data = result
            elif isinstance(result, str):
                self.data = result
            elif isinstance(result, vip_dashboard.VipDashboard):
                self.data = result
            elif isinstance(result, vip_dashboard.VipDashboardTile):
                self.data = result
            elif isinstance(result, vip_annotation.VipAnnotation):
                self.data = result
            elif isinstance(result, vip_object.VipObject):
                self.data = result
            elif isinstance(result, list):
                self.data = result
            elif isinstance(result, dict):
                self.data = result
            elif isinstance(result, tuple):
                self.data = result
            else:
                raise exceptions.InvalidResultTypeException("VipResult's must be pd.DataFrame, a tuple of pd.DataFrames, nx.Graph, "
                                                            "VipPlot, VipDashboard, or VipDashboardTile type.")
