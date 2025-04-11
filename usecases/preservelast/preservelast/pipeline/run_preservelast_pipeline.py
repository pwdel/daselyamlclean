#!/usr/bin/env python3

from date_helper.date_helper import update_dates_in_data
from yaml_toplevel.yaml_toplevel import get_toplevel_inserts_keys, determine_key_contents
from yaml_list_helpers.yaml_list_helpers import get_last_list_index_for_key, get_list_item_key_values
from yaml_dict_helpers.yaml_dict_helpers import get_dict_item_key_values
from filereadwrite.file_indicies import find_yaml_block_indices_for_combined
from filereadwrite.string_write import replace_combined_updated_blocks, replace_nulls_with_tilde_in_string

def run_preservelast_pipeline(replacements_dir, manifests_file):

    inserts_file = replacements_dir + '/inserts.yaml'
    inserts_keys = get_toplevel_inserts_keys(inserts_file)

    updates_file = replacements_dir + '/updates.yaml'
    updates_keys = get_toplevel_inserts_keys(updates_file)

    # Determine key types for inserts and updates based on the manifest.
    keys_with_list_as_values_inserts, keys_with_dict_as_values_inserts = determine_key_contents(manifests_file, inserts_keys)
    keys_with_list_as_values_updates, keys_with_dict_as_values_updates = determine_key_contents(manifests_file, updates_keys)

    # Process Inserts: update dates for list-based and dict-based keys.
    counts = get_last_list_index_for_key(manifests_file, keys_with_list_as_values_inserts)
    list_item_key_values_inserts = get_list_item_key_values(manifests_file, counts)
    updated_list_dates_inserts = update_dates_in_data(list_item_key_values_inserts)
    dict_item_key_values_inserts = get_dict_item_key_values(manifests_file, keys_with_dict_as_values_inserts)
    updated_dict_dates_inserts = update_dates_in_data(dict_item_key_values_inserts)

    # Process Updates: update dates for dict-based keys (list updates not supported yet).
    dict_item_key_values_updates = get_dict_item_key_values(manifests_file, keys_with_dict_as_values_updates)
    updated_dict_dates_updates = update_dates_in_data(dict_item_key_values_updates)

    # Combine updated data for both inserts and updates.
    combined_updated_dates = {
        "inserts": {**updated_list_dates_inserts, **updated_dict_dates_inserts},
        "updates": {**updated_dict_dates_updates}
    }

    # Get the file snapshot and block indices based on the combined updated data.
    combined_lines_snapshot, combined_block_indicies = find_yaml_block_indices_for_combined(
        manifests_file, combined_updated_dates
    )

    print(f"combined_updated_dates: {combined_updated_dates}")

    # Produce and print the final updated file content.
    combined_updated_blocks_replaced = replace_combined_updated_blocks(
        combined_lines_snapshot, 
        combined_block_indicies, 
        combined_updated_dates,
        keys_with_list_as_values_inserts,
        keys_with_dict_as_values_inserts,
        keys_with_dict_as_values_updates
    )

    return replace_nulls_with_tilde_in_string(combined_updated_blocks_replaced)