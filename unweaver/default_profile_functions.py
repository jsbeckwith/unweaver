def cost_function_generator():
    def cost_function(u, v, d):
        # FIXME: "length" is not guaranteed to exist? Update `entwiner` to
        # calculate a _length attribute for all edges?
        return d.get("length", None)

    return cost_function


def directions_function(status, G, origin, destination, cost, nodes, edges):
    return {
        "status": status,
        "origin": origin,
        "destination": destination,
        "total_cost": cost,
        "edges": edges,
    }


def shortest_paths_function(status, G, origin, nodes, paths, edges):
    """Return the minimum costs to nodes in the graph."""
    # FIXME: coordinates are derived from node string, should be derived from
    # node metadata (add node coordinates upstream in entwiner).
    return {
        "status": status,
        "origin": origin,
        "paths": list(paths),
        "edges": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": edge.pop(G.network.edges.geom_column),
                    "properties": edge,
                }
                for edge in edges
            ],
        },
        "node_costs": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": n.pop(G.network.edges.geom_column),
                    "properties": {"cost": n["cost"]},
                }
                for n in nodes.values()
            ],
        },
    }


def reachable_function(status, G, origin, nodes, edges):
    """Return the total extent of reachable edges."""
    # FIXME: coordinates are derived from node string, should be derived from
    # node metadata (add node coordinates upstream in entwiner).
    unique_edges = []
    seen = set()
    for edge in edges:
        edge_id = (edge["_u"], edge["_v"])

        if edge_id in seen:
            # Skip if we've seen this edge before
            continue
        if (edge_id[1], edge_id[0]) in seen:
            # Skip if we've seen the reverse of this edge before
            continue

        unique_edges.append(edge)
        seen.add(edge_id)

    return {
        "status": status,
        "origin": origin,
        "edges": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": edge.pop(G.network.edges.geom_column),
                    "properties": edge,
                }
                for edge in unique_edges
            ],
        },
        "node_costs": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": node[G.network.nodes.geom_column],
                    "properties": {"cost": node["cost"]},
                }
                for node in nodes.values()
            ],
        },
    }
