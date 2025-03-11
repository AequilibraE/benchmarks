import os
from tempfile import TemporaryDirectory
from aequilibrae.utils.create_example import create_example
from aequilibrae.paths import PathResults
from .benchmarks import benchmark


# class Sequential:
#     def setup_cache(self):
#         dir = TemporaryDirectory()
#         project = create_example(os.path.join(dir.name, "project"), "coquimbo")

#         perf_results = {}

#         with benchmark(perf_results, "build_graphs"):
#             project.network.build_graphs()

#         graph = project.network.graphs["c"]

#         with benchmark(perf_results, "set_graph"):
#             graph.set_graph("distance")

#         with benchmark(perf_results, "set_skimming_travel_time)"):
#             graph.set_skimming(["travel_time"])

#         with benchmark(perf_results, "set_skimming_travel_time_distance)"):
#             graph.set_skimming(["travel_time", "distance"])

#         graph.set_blocked_centroid_flows(False)

#         res = PathResults()
#         res.prepare(graph)

#         with benchmark(perf_results, "compute_path"):
#             res.compute_path(32343, 22041)

#         with benchmark(perf_results, "compute_path_early_exit)"):
#             res.compute_path(32343, 22041, early_exit=True)

#         with benchmark(perf_results, "compute_path_a_star_equirectangular)"):
#             res.compute_path(32343, 22041, a_star=True, heuristic="equirectangular")

#         with benchmark(perf_results, "compute_path_a_star_haversine)"):
#             res.compute_path(32343, 22041, a_star=True, heuristic="haversine")

#         project.close()

#         return perf_results

#     def track_set_graph(self, perf_results):
#         return perf_results["set_graph"]

#     def track_build_graphs(self, perf_results):
#         return perf_results["build_graphs"]

#     def track_set_skimming_travel_time(self, perf_results):
#         return perf_results["set_skimming_travel_time)"]

#     def track_set_skimming_travel_time_distance(self, perf_results):
#         return perf_results["set_skimming_travel_time_distance)"]

#     def track_compute_path(self, perf_results):
#         return perf_results["compute_path"]

#     def track_compute_path_early_exit(self, perf_results):
#         return perf_results["compute_path_early_exit)"]

#     def track_compute_path_a_star_equirectangular(self, perf_results):
#         return perf_results["compute_path_a_star_equirectangular)"]

#     def track_compute_path_a_star_haversine(self, perf_results):
#         return perf_results["compute_path_a_star_haversine)"]


class PathComputation:
    def setup(self):
        self.dir = TemporaryDirectory()
        self.project = create_example(os.path.join(self.dir.name, "project"), "coquimbo")

        self.project.network.build_graphs()
        self.graph = self.project.network.graphs["c"]
        self.graph.set_graph("distance")
        self.graph.set_blocked_centroid_flows(False)

        self.res = PathResults()
        self.res.prepare(self.graph)

    def teardown(self):
        self.project.close()

    def time_compute_path(self):
        self.res.compute_path(32343, 22041)

    def time_compute_path_early_exit(self):
        self.res.compute_path(32343, 22041, early_exit=True)

    def time_compute_path_a_star_equirectangular(self):
        self.res.compute_path(32343, 22041, a_star=True, heuristic="equirectangular")

    def time_compute_path_a_star_haversine(self):
        self.res.compute_path(32343, 22041, a_star=True, heuristic="haversine")
