from .layer import Layer
from geopandas import GeoDataFrame

class GeoJSONLayerPolygonSelector(Layer):
    def __init__(self, mapbox, id, map_id, **kwargs):
        super().__init__(mapbox, id, map_id, **kwargs)
        pass

    def set_data(self,
                 data,
                 index):

        self.data = data
        self.index = index

        # Make sure this is not an empty GeoDataFrame
        if isinstance(data, GeoDataFrame):
            # Data is GeoDataFrame
            if len(data) == 0:
                data = GeoDataFrame()

        # Remove existing layer        
        self.mapbox.runjs("./js/main.js", "removeLayer", arglist=[self.map_id])
        # Add new layer        
        self.mapbox.runjs("./js/geojson_layer_polygon_selector.js", "addLayer", arglist=[self.map_id,
                                                                                         data,
                                                                                         index,
                                                                                         self.line_color,
                                                                                         self.line_width,
                                                                                         self.line_style,
                                                                                         self.line_opacity,
                                                                                         self.fill_color,
                                                                                         self.fill_opacity,
                                                                                         self.line_color_selected,
                                                                                         self.fill_color_selected,
                                                                                         self.selection_type])

    def set_selected_index(self, index):
        self.mapbox.runjs("/js/geojson_layer_polygon_selector.js", "setSelectedIndex", arglist=[self.map_id, index])

    def activate(self):
        self.mapbox.runjs("./js/geojson_layer_polygon_selector.js", "activate", arglist=[self.map_id,
                                                                                         self.line_color,
                                                                                         self.line_width,
                                                                                         self.line_style,
                                                                                         self.line_opacity,
                                                                                         self.fill_color,
                                                                                         self.fill_opacity,
                                                                                         self.line_color_selected,
                                                                                         self.fill_color_selected])
  
    def deactivate(self):
        self.mapbox.runjs("./js/geojson_layer_circle_selector.js", "deactivate", arglist=[self.map_id,
                                                                                          self.line_color_inactive,
                                                                                          self.line_width_inactive,
                                                                                          self.line_style_inactive,
                                                                                          self.line_opacity_inactive,
                                                                                          self.fill_color_inactive,
                                                                                          self.fill_opacity_inactive,
                                                                                          self.line_color_selected_inactive,
                                                                                          self.fill_color_selected_inactive])

    def redraw(self):
        if isinstance(self.data, GeoDataFrame):
            self.set_data(self.data, self.index)

        # self.line_color    = "dodgerblue"
        # self.line_width    = 2
        # self.line_style    = "-"
        # self.line_opacity  = 1.0
        # self.fill_color    = "dodgerblue"
        # self.fill_opacity  = 1.0
        # self.circle_radius = 4
        # self.selection_type = "single"

        # for key, value in kwargs.items():
        #     setattr(self, key, value)

        # self.line_color = mcolors.to_hex(self.line_color)
        # self.fill_color = mcolors.to_hex(self.fill_color)

#        self.type   = "geojson"
#        self.select_callback = select

        # if fill_color != "transparent":
        #     fill_color = mcolors.to_hex(fill_color)
        # if line_color != "transparent":
        #     line_color = mcolors.to_hex(line_color)

#         if isinstance(data, GeoDataFrame):
#             # Data is GeoDataFrame
#             if file_name:
# #                xxx = data.to_json()
#                 with open(os.path.join(self.mapbox.server_path, "overlays", file_name), "w") as f:
#                     if "timeseries" in data:
#                         f.write(data.drop(columns=["timeseries"]).to_crs(4326).to_json())
#                     else:
#                         f.write(data.to_crs(4326).to_json())

#                 data = "./overlays/" + file_name
#             else:
#                 data = data.to_json()
#         else:
#             data = []

        # if type == "polygon_selector":
        #     self.mapbox.runjs("./js/geojson_layer_polygon_selector.js", "addLayer", arglist=[self.map_id,
        #                                                                                      data,
        #                                                                                      fill_color,
        #                                                                                      fill_opacity,
        #                                                                                      line_width,
        #                                                                                      selection_type])

        # # elif type == "marker_selector":
        # #     self.mapbox.runjs("./js/geojson_layer_marker_selector.js", "addLayer", arglist=[self.map_id,
        # #                                                                                     data,
        # #                                                                                     fill_color,
        # #                                                                                     fill_opacity,
        # #                                                                                     line_width,
        # #                                                                                     circle_radius,
        # #                                                                                     selection_type])
        # elif type == "circle":
        #     self.mapbox.runjs("./js/geojson_layer_circle.js", "addLayer", arglist=[self.map_id,
        #                                                                            data,
        #                                                                            fill_color,
        #                                                                            fill_opacity,
        #                                                                            line_color,
        #                                                                            line_width,
        #                                                                            circle_radius,
        #                                                                            selection_type])

        # else:
        #     self.mapbox.runjs("./js/geojson_layer_polygon_selector.js", "addLayer", arglist=[self.map_id, data])

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False


    def clear(self):
        self.active = False
        self.mapbox.runjs("/js/main.js", "removeLayer", arglist=[self.map_id])

    def update(self):
        pass

    # def set_data(self,
    #              data,
    #              legend_title="",
    #              crs=None):
    #     # Make sure this is not an empty GeoDataFrame
    #     if isinstance(data, GeoDataFrame):
    #         # Data is GeoDataFrame
    #         if len(data) > 0:
    #             # Convert GDF to geojson
    #             data = data.to_json()
    #             self.mapbox.runjs("/js/geojson_layer.js", "setData", arglist=[self.map_id, data])

    def set_visibility(self, true_or_false):
        if true_or_false:
            self.mapbox.runjs("/js/main.js", "showLayer", arglist=[self.map_id + ".fill"])
            self.mapbox.runjs("/js/main.js", "showLayer", arglist=[self.map_id + ".line"])
        else:
            self.mapbox.runjs("/js/main.js", "hideLayer", arglist=[self.map_id + ".fill"])
            self.mapbox.runjs("/js/main.js", "hideLayer", arglist=[self.map_id + ".line"])
