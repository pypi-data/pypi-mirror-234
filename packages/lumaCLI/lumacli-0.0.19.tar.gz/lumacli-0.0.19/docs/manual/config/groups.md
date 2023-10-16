# `luma` - Groups Configuration Guide

In the directory where you run the `lumaCLI`, a `.luma` folder can be created containing a `config.yaml` file. Initialize this using the command:

[`luma config init`](../cli.md#luma-config-init)

You can organize your catalog into groups of metadata to facilitate easier management. For instance, you might have 'Departments' to categorize assets by organization department or 'Data Product' to group all assets under a specific product in the Luma Catalog.

The `groups` key in the `config.yaml` contains a list of objects defining specific characteristics, detailed below:

## Properties

- **`meta_key`**: A required string that represents the key identifier.
  - **Example**: `"data_product"`
- **`slug`**: A required string that yields a URL-friendly version of the label.
  - **Example**: `"data-products"`
- **`label_plural`**: A required string for the plural form of the label.
  - **Example**: `"Data Products"`
- **`label_singular`**: A required string for the singular form of the label.
  - **Example**: `"Data Product"`
- **`icon`**: A required string indicating an icon associated with the group, chosen from [HeroIcons](https://heroicons.com).
  - **Example**: `"Cube"`

## Example Configuration

### _.luma/config.yaml_

```yaml
groups:
  - meta_key: "department"
    slug: "departments"
    label_plural: "Departments"
    label_singular: "Department"
    icon: "Cube"
  - meta_key: "data_product"
    slug: "data-products"
    label_plural: "Data Products"
    label_singular: "Data Product"
    icon: "Cloud"
```

## Tagging Metadata Items with Groups

In `lumaCLI`, assets can be tagged to belong to one or more groups through the metadata definition of that asset.

### DBT

1. **Edit the YAML File**
   - Navigate to the YAML file corresponding to the resource you want to tag.

2. **Add the Metadata**
   - In the YAML file, use the `meta` key to add custom key-value pairs. Here's an example for a model:
     ```yaml
     models:
       - name: my_table
         description: "This is my example table"
         meta:
           "department": "HR"
     ```

3. **Generate Metadata**

   To generate metadata, execute the following commands:
   
   - `dbt deps`
   - `dbt run`
   - `dbt test`
   - `dbt source freshness`
   - `dbt docs generate`

4. **Ingest Data with luma**
   - Use the [`luma dbt ingest`](../cli.md#luma-dbt-ingest) command to ingest the data.
