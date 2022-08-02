from __future__ import annotations

import seaborn as sns

from conflowgen.analyses.modal_split_analysis import ModalSplitAnalysis
from conflowgen.reporting import AbstractReportWithMatplotlib, modal_split_report
from conflowgen.reporting.modal_split_report import plot_modal_splits

sns.set_palette(sns.color_palette())


class ModalSplitAnalysisReport(AbstractReportWithMatplotlib):
    """
    This analysis report takes the data structure as generated by :class:`.ModalSplitAnalysis`
    and creates a comprehensible representation for the user, either as text or as a graph.
    """

    report_description = """
    Analyze the amount of containers dedicated for or coming from the hinterland compared to the amount of containers
    that are transshipment.
    """

    def __init__(self):
        super().__init__()
        self.analysis = ModalSplitAnalysis()

    def get_report_as_text(
            self
    ) -> str:
        """
        The report as a text is represented as a table suitable for logging. It uses a human-readable formatting style.
        """
        # gather data
        transshipment_and_hinterland_split = self.analysis.get_transshipment_and_hinterland_split()

        modal_split_in_hinterland_inbound_traffic = self.analysis.get_modal_split_for_hinterland_traffic(
            inbound=True, outbound=False
        )

        modal_split_in_hinterland_outbound_traffic = self.analysis.get_modal_split_for_hinterland_traffic(
            inbound=False, outbound=True
        )

        modal_split_in_hinterland_traffic_both_directions = self.analysis.get_modal_split_for_hinterland_traffic(
            inbound=True, outbound=True
        )

        report = modal_split_report.insert_values_in_template(
            transshipment_and_hinterland_split=transshipment_and_hinterland_split,
            modal_split_in_hinterland_inbound_traffic=modal_split_in_hinterland_inbound_traffic,
            modal_split_in_hinterland_outbound_traffic=modal_split_in_hinterland_outbound_traffic,
            modal_split_in_hinterland_traffic_both_directions=modal_split_in_hinterland_traffic_both_directions
        )

        return report

    def get_report_as_graph(self) -> object:
        """
        The report as a graph is represented as a set of pie charts using pandas.

        Returns:
             The matplotlib axis of the last bar chart.
        """

        # gather data
        transshipment_and_hinterland_split = self.analysis.get_transshipment_and_hinterland_split()
        modal_split_for_hinterland_inbound = self.analysis.get_modal_split_for_hinterland_traffic(
            inbound=True, outbound=False
        )
        modal_split_for_hinterland_outbound = self.analysis.get_modal_split_for_hinterland_traffic(
            inbound=False, outbound=True
        )
        modal_split_for_hinterland_both = self.analysis.get_modal_split_for_hinterland_traffic(
            inbound=True, outbound=True
        )

        axes = plot_modal_splits(
            transshipment_and_hinterland_split=transshipment_and_hinterland_split,
            modal_split_in_hinterland_both_directions=modal_split_for_hinterland_both,
            modal_split_in_hinterland_inbound_traffic=modal_split_for_hinterland_inbound,
            modal_split_in_hinterland_outbound_traffic=modal_split_for_hinterland_outbound,
        )

        return axes
