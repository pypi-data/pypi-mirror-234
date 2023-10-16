from __future__ import annotations

from typing import List

import networkx as nx
import rich_click as click
import woke.ir as ir
import woke.ir.types as types
from woke.detectors import (
    Detection,
    DetectionConfidence,
    DetectionImpact,
    Detector,
    DetectorResult,
    detector,
)


class UnusedImportDetector(Detector):
    detections = []

    def detect(self) -> List[DetectorResult]:
        return self.detections

    @detector.command(name="unused-import")
    def cli(self) -> None:
        pass

    def visit_source_unit(self, node: ir.SourceUnit):
        import itertools

        for import_directive in node.imports:
            imported_source_unit_name = import_directive.imported_source_unit_name
            found_imported_symbol = False

            for predecessor in itertools.chain(
                [imported_source_unit_name],
                (pred for pred, _, _ in nx.edge_bfs(self.imports_graph, imported_source_unit_name, "reverse")),
            ):
                if predecessor == node.source_unit_name:
                    continue

                predecessor_path = self.imports_graph.nodes[predecessor]["path"]
                source_unit = self.build.source_units[predecessor_path]

                # should not be needed to check for aliases, as there still should be original global declarations referenced

                for declaration in source_unit.declarations_iter():
                    for ref in declaration.references:
                        if isinstance(ref, ir.IdentifierPathPart):
                            ref = ref.underlying_node
                        elif isinstance(ref, ir.ExternalReference):
                            ref = ref.inline_assembly

                        if ref.source_unit.source_unit_name == node.source_unit_name:
                            found_imported_symbol = True
                            break

                    if found_imported_symbol:
                        break

                if found_imported_symbol:
                    break

            if not found_imported_symbol:
                self.detections.append(
                    DetectorResult(
                        Detection(
                            import_directive,
                            "Unused import",
                        ),
                        impact=DetectionImpact.WARNING,
                        confidence=DetectionConfidence.HIGH,
                    )
                )
