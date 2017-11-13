from sqlalchemy.orm import Session

from data.model.graph_model import Event, Relationship
from data.service import BaseService
from graph.graph_creator import load_relationship_map, save_relationship_map
from settings import DUPLICATE_RELATIONSHIP_MAP_FILE


def load_edges(relationship_map, session):
    duplicate_event_map = {}

    for source_node, references in relationship_map.items():
        source_existing_events = session.query(Event).filter(Event.name == source_node).all()

        if len(source_existing_events) > 1 or len(source_existing_events) == 0:
            duplicate_event_map[source_node] = []
        else:
            source_event = source_existing_events[0]

        for destination_node in references:
            if source_event:
                destination_existing_events = session.query(Event).filter(Event.name == destination_node).all()
                if len(destination_existing_events) > 1 or len(destination_existing_events) == 0:
                    if source_node not in duplicate_event_map:
                        duplicate_event_map[source_node] = []
                    duplicate_event_map[source_node].append(destination_node)
                else:
                    destination_event = destination_existing_events[0]

                    existing_edge = session.query(Relationship)\
                        .filter(Relationship.edge_from == source_event.id, Relationship.edge_to == destination_event.id)\
                        .first()

                    if existing_edge is None:
                        edge = Relationship(edge_from=source_event.id, edge_to=destination_event.id, count=1)
                        session.add(edge)
                        session.commit()
                    else:
                        existing_edge.count += 1
                        session.add(existing_edge)
                        session.commit()
            else:
                duplicate_event_map[source_node].append(destination_node)

    save_duplicate_relationship_map(duplicate_event_map)


def save_duplicate_relationship_map(event_map, filename=DUPLICATE_RELATIONSHIP_MAP_FILE):
    save_relationship_map(event_map, filename)


if __name__ == "__main__":
    relationship_map = load_relationship_map()

    base_service = BaseService(True)
    session = Session()

    load_edges(relationship_map, session)