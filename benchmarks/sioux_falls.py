import os
from tempfile import TemporaryDirectory

import numpy as np

from aequilibrae.matrix import AequilibraeMatrix
from aequilibrae.paths import NetworkSkimming, PathResults, RouteChoice as RouteChoiceClass
from aequilibrae.utils.create_example import create_example


class GraphBuilding:
    def setup(self):
        self.dir = TemporaryDirectory()
        self.project = create_example(
            os.path.join(self.dir.name, "project"), "sioux_falls"
        )

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
        self.project = create_example(
            os.path.join(self.dir.name, "project"), "sioux_falls"
        )

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
        self.project = create_example(
            os.path.join(self.dir.name, "project"), "sioux_falls"
        )

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


class RouteChoice:
    def setup(self):
        self.dir = TemporaryDirectory()
        self.project = create_example(
            os.path.join(self.dir.name, "project"), "sioux_falls"
        )

        self.project.network.build_graphs()
        self.graph = self.project.network.graphs["c"]
        self.graph.set_graph("distance")
        self.graph.set_blocked_centroid_flows(False)

        self.mat = AequilibraeMatrix()
        self.mat.create_empty(
            zones=self.graph.num_zones, matrix_names=["demand"], memory_only=True
        )
        self.mat.index = self.graph.centroids[:]
        self.mat.matrices[:, :, 0] = np.full(
            (self.graph.num_zones, self.graph.num_zones), 10.0
        )
        self.mat.computational_view()

        self.rc = RouteChoiceClass(self.graph)
        try:
            self.rc.add_demand(self.mat)
        except AttributeError:
            self.rc.set_demand(self.mat)

    def teardown(self):
        self.project.close()

    def time_bfsle_with_results(self):
        self.rc.set_choice_set_generation("bfsle", max_routes=5, seed=12345)
        self.rc.prepare()
        self.rc.execute(perform_assignment=False)
        self.rc.get_results()

    def time_bfsle_without_results(self):
        self.rc.set_choice_set_generation("bfsle", max_routes=5, seed=12345)
        self.rc.prepare()
        self.rc.execute(perform_assignment=False)

    def time_bfsle_assignment_with_results(self):
        self.rc.set_choice_set_generation("bfsle", max_routes=5, seed=12345)
        self.rc.prepare()
        self.rc.execute(perform_assignment=True)
        self.rc.get_results()

    def time_bfsle_assignment_without_results(self):
        self.rc.set_choice_set_generation("bfsle", max_routes=5, seed=12345)
        self.rc.prepare()
        self.rc.execute(perform_assignment=True)

    def time_lp_with_results(self):
        self.rc.set_choice_set_generation("lp", max_routes=5, seed=12345)
        self.rc.prepare()
        self.rc.execute(perform_assignment=False)
        self.rc.get_results()

    def time_lp_without_results(self):
        self.rc.set_choice_set_generation("lp", max_routes=5, seed=12345)
        self.rc.prepare()
        self.rc.execute(perform_assignment=False)

    def time_lp_assignment_with_results(self):
        self.rc.set_choice_set_generation("lp", max_routes=5, seed=12345)
        self.rc.prepare()
        self.rc.execute(perform_assignment=True)
        self.rc.get_results()

    def time_lp_assignment_without_results(self):
        self.rc.set_choice_set_generation("lp", max_routes=5, seed=12345)
        self.rc.prepare()
        self.rc.execute(perform_assignment=True)
