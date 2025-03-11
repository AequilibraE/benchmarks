import os
from tempfile import TemporaryDirectory
from aequilibrae.utils.create_example import create_example
from aequilibrae.paths import PathResults
from aequilibrae.paths import NetworkSkimming


class GraphBuilding:
    def setup(self):
        self.dir = TemporaryDirectory()
        self.project = create_example(os.path.join(self.dir.name, "project"), "sioux_falls")

        self.project.network.build_graphs()
        self.graph = self.project.network.graphs["c"]
        self.graph.set_graph("distance")
        self.graph.set_blocked_centroid_flows(False)

    def teardown(self):
        self.project.close()

    def time_build_graphs(self):
        self.project.network.build_graphs()

    def time_prepare_graph(self):
        graph = self.project.network.graphs["c"]
        graph.set_graph("distance")
        graph.set_blocked_centroid_flows(False)
        graph.prepare_graph()


class PathComputation:
    def setup(self):
        self.dir = TemporaryDirectory()
        self.project = create_example(os.path.join(self.dir.name, "project"), "sioux_falls")

        self.project.network.build_graphs()
        self.graph = self.project.network.graphs["c"]
        self.graph.set_graph("distance")
        self.graph.set_blocked_centroid_flows(False)

        self.res = PathResults()
        self.res.prepare(self.graph)

    def teardown(self):
        self.project.close()

    def time_compute_path(self):
        self.res.compute_path(1, 22)

    def time_compute_path_early_exit(self):
        self.res.compute_path(1, 22, early_exit=True)

    def time_compute_path_a_star_equirectangular(self):
        self.res.compute_path(1, 22, a_star=True, heuristic="equirectangular")

    def time_compute_path_a_star_haversine(self):
        self.res.compute_path(1, 22, a_star=True, heuristic="haversine")


class Skimming:
    def setup(self):
        self.dir = TemporaryDirectory()
        self.project = create_example(os.path.join(self.dir.name, "project"), "sioux_falls")

        self.project.network.build_graphs()
        self.graph = self.project.network.graphs["c"]
        self.graph.set_graph("distance")
        self.graph.set_skimming(["distance"])
        self.graph.set_blocked_centroid_flows(False)

        self.graph.prepare_graph()

    def teardown(self):
        self.project.close()

    def time_network_skimming(self):
        skm = NetworkSkimming(self.graph)
        skm.execute()
