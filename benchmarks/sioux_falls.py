import os
from tempfile import TemporaryDirectory

import numpy as np
from asv_runner.benchmarks.mark import SkipNotImplemented

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
    params = [(True, False), (None, "equirectangular", "haversine")]
    param_names = ["early_exit", "A* heuristic"]

    def setup(self, *_):
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

    def teardown(self, *_):
        self.project.close()

    def time_compute_path(self, early_exit, heuristic):
        if early_exit and heuristic is not None:
            raise SkipNotImplemented("A* not applicable when using early exit")

        self.res.compute_path(1, 22, early_exit=early_exit, a_star=heuristic is not None, heuristic=heuristic)


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
    params = [("bfsle", "lp"), (True, False), (True, False)]
    param_names = ["algorithm", "assignment", "results"]

    def setup(self, *_):
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

    def teardown(self, *_):
        self.project.close()

    def time_rc(self, algorithm, assignment, results):
        self.rc.set_choice_set_generation(algorithm, max_routes=5, seed=12345)
        self.rc.prepare()
        self.rc.execute(perform_assignment=assignment)
        if results:
            self.rc.get_results()
