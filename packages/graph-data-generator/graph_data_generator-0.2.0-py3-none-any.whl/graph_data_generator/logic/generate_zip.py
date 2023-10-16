from graph_data_generator.models.mapping import Mapping
# from graph_data_generator.logger import ModuleLogger
import io 
import csv
import json
import zipfile
from graph_data_generator.models.data_import import DataImporterJson
from graph_data_generator.logger import ModuleLogger

# TODO: Split the csv and zip functions out
def generate_zip(
        mapping: Mapping,
        )->tuple[io.BytesIO, str]:

    # Simple preprocess check
    if len(mapping.nodes) == 0:
        return None, f'No nodes to process from mapping: {mapping}'
    if len(mapping.relationships) == 0:
        return None, f'No relationships found from mapping: {mapping}.'

    # Prep zip file to write data to
    in_memory_data = io.BytesIO()
    in_memory_zip = zipfile.ZipFile(
        in_memory_data, "w", zipfile.ZIP_DEFLATED, False)
    in_memory_zip.debug = 3 

    # Capture generation logs into an input stream
    logs_buffer = io.StringIO()
    logs_buffer.write(f'Starting data generation...\n')

    # Process nodes
    logs_buffer.write(f'Processing {len(mapping.nodes)} node types...\n')
    successful_nodes = 0
    for nid, node in mapping.nodes.items():
        # Generate values from mappings
        try:
            values : list[dict] = node.generate_values()
            logs_buffer.write(f'Generated values for node type {nid}: {values}\n')
        except Exception as e:
            ModuleLogger().error(f'Failed to generate values for node with caption: {node.caption}. ERROR: {e}')
            logs_buffer.write(f'Node {node} value generation failed: {e}\n')
            continue

        # Generate csv from values
        if values is None or values == []:
            logs_buffer.write(f'No values generated for node {node.caption}\n')
            continue
    
        # Each node dataset will need it's own CSV file
        fieldnames = values[0].keys()
        nodes_buffer = io.StringIO()
        nodes_writer = csv.DictWriter(nodes_buffer, fieldnames=fieldnames)
        nodes_writer.writeheader()

        for row in values:
            try:
                nodes_writer.writerow(row)
                successful_nodes += 1
            except Exception as e:
                # return None, f'Node {node.caption} generation failed: {e}'
                logs_buffer.write(f'Node {node} generation failed: {e}')
                continue
        in_memory_zip.writestr(f"{node.filename()}.csv", nodes_buffer.getvalue())
    logs_buffer.write(f'Generated {successful_nodes} nodes\n')

    logs_buffer.write(f'Processing {len(mapping.relationships)} relationship types...\n')
    successful_rels = 0
    for rid, rel in mapping.relationships.items():
        # Generate values from mappings
        try:
            values : list[dict] = rel.generate_values()
        except Exception as e:
            logs_buffer.write(f'Relationship {rel} generation failed: {e}\n')
            continue

        # Generate csv from values
        if values is None or values == []:
            logs_buffer.write(f'No values generated for relationship {rel.type}\n')
            continue
        fieldnames = values[0].keys()
        rels_buffer = io.StringIO()
        writer = csv.DictWriter(rels_buffer, fieldnames=fieldnames)
        writer.writeheader()
        for row in values:
            try:
                writer.writerow(row)
                successful_rels += 1
            except Exception as e:
                logs_buffer.write(f'Relationship {rel} generation failed: {e}\n')
        in_memory_zip.writestr(f"{rel.filename()}.csv", rels_buffer.getvalue())
    logs_buffer.write(f'Generated {successful_rels} relationships\n')

    # generate data-importer.json
    dij = DataImporterJson()
    nodes = mapping.nodes
    dij.add_nodes(nodes)
    relationships = mapping.relationships
    dij.add_relationships(relationships)
    dij_dict = dij.to_dict()

    logs_buffer.write(f'Writing data-importer.json...\n')
    try:
        di_dump = json.dumps(dij_dict)
        in_memory_zip.writestr("neo4j_importer_model.json", di_dump)
        logs_buffer.write(f'Successfully wrote data-importer.json.\n')

    except Exception as e:
        # return None, f'Error adding nodes and relationships for data-importer json: predump: {dij_dict}: \n\nError: {e}'
        logs_buffer.write(f'Problem creating import model .json generation failed: {e}')

    logs_buffer.write(f'Data generation process complete.\n')
    in_memory_zip.writestr(f"logs.txt", logs_buffer.getvalue())

    return in_memory_data, None