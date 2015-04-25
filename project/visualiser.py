import vtk


class EuclideanVisualiser:

    def __init__(self):

        self.red = [255, 0, 0]
        self.green = [0, 255, 0]

    def visualise(self, hyperbolic_points, asn_ordered_list, aut_sys_data):

        points = self.generate_points(hyperbolic_points)
        points_poly = self.generate_point_poly_data(points)
        points_glyph_filter = self.generate_vertex_glyph_filter(points_poly)
        points_mapper = self.generate_points_mapper(points_glyph_filter)
        points_actor = self.generate_points_actor(points_mapper)

        lines, colours = self.generate_lines_and_colours(asn_ordered_list, aut_sys_data)
        lines_poly_data = self.generate_lines_poly_data(lines, points, colours)
        lines_mapper = self.generate_mapper(lines_poly_data)
        lines_actor = self.generate_actor(lines_mapper)

        self.render(points_actor)

    def generate_points(self, hyperbolic_points):

        x = self.convert_to_tuple(hyperbolic_points)

        points = vtk.vtkPoints()

        # Load the point, cell, and data attributes.
        for i in range(len(x)):
            points.InsertPoint(i, x[i])

        return points

    def convert_to_tuple(self, array_points):

        tuple_array = []

        for column in array_points:

            tuple_array.append(tuple(column))

        return tuple_array

    def generate_point_poly_data(self, points):

        poly = vtk.vtkPolyData()

        poly.SetPoints(points)

        return poly

    def generate_vertex_glyph_filter(self, poly):

        glyph_filter = vtk.vtkVertexGlyphFilter()

        glyph_filter.SetInput(poly)

        return glyph_filter

    def generate_points_mapper(self, glyph_filter):

        points_mapper = vtk.vtkPolyDataMapper()

        points_mapper.SetInputConnection(glyph_filter.GetOutputPort())

        return points_mapper

    def generate_mapper(self, poly_data):

        mapper = vtk.vtkPolyDataMapper()

        mapper.SetInput(poly_data)

        return mapper

    def generate_points_actor(self, mapper):

        actor = self.generate_actor(mapper)

        actor.GetProperty().SetPointSize(3)

        return actor

    def generate_actor(self, mapper):

        actor = vtk.vtkActor()

        actor.SetMapper(mapper)

        return actor

    def render(self, *actors):

        renderer = vtk.vtkRenderer()

        ren_win = vtk.vtkRenderWindow()

        ren_win.AddRenderer(renderer)

        iren = vtk.vtkRenderWindowInteractor()

        iren.SetRenderWindow(ren_win)

        for actor in actors:

            renderer.AddActor(actor)

        renderer.SetBackground(0, 0, 0)

        ren_win.SetSize(600, 600)

        ren_win.Render()

        iren.Start()

    def generate_lines_and_colours(self, asn_ordered_list, aut_sys_data):

        lines = vtk.vtkCellArray()

        colours = vtk.vtkUnsignedCharArray()
        colours.SetNumberOfComponents(3)
        colours.SetName("Colors")

        for asn in asn_ordered_list:

            aut_sys = aut_sys_data[asn]

            for peering in aut_sys.peers:

                line = vtk.vtkLine()

                line.GetPointIds().SetId(0, asn_ordered_list.index(asn))

                if peering.peer_asn in asn_ordered_list:

                    line.GetPointIds().SetId(1, asn_ordered_list.index(peering.peer_asn))

                    lines.InsertNextCell(line)

                    if peering.rel_type == "-1":

                        colours.InsertNextTupleValue(self.red)
                    else:

                        colours.InsertNextTupleValue(self.green)

        return lines, colours

    def generate_lines_poly_data(self, lines, points, colours):

        lines_poly_data = vtk.vtkPolyData()

        lines_poly_data.SetPoints(points)

        lines_poly_data.SetLines(lines)

        lines_poly_data.GetCellData().SetScalars(colours)

        return lines_poly_data
