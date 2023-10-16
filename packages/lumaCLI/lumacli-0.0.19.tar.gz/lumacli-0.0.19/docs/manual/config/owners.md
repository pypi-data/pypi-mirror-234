# `luma` - Owners Configuration Guide

In the directory where you run the `lumaCLI` from, a `.luma` folder can be created containing a `owners.yaml` file. Initialize this using the command:

[`luma config init`](../cli.md#luma-config-init)

This allows you to centralize and manage owner information effortlessly.

## `owners.yaml`

The `owners.yaml` file serves as a centralized location to define each owner, including their name, email, and title. You can then tag various metadata resources using only the email address of the owner, and optionally specify the type of owner.

An owner is defined with the following attributes:

- **`email`**: A unique key representing the owner's email address. This field is required.
  - **Example**: `"someone@example.com"`
- **`first_name`**: The first name of the owner, optional.
  - **Example**: `"Aaron"`
- **`last_name`**: The last name of the owner, a required field.
  - **Example**: `"Jackson"`
- **`title`**: The title or role of the owner within the organization, a required field.
  - **Example**: `"Data Analyst"`

### Example Structure

Below is an example structure of the `owners.yaml` file located at _.luma/owners.yaml_:

````yaml
owners:
  - email: "dave@example.com"
    first_name: "Dave"
    last_name: "Cotterall"
    title: "Director"
  - email: "michelle@example.com"
    first_name: "Michelle"
    last_name: "Dunne"
    title: "CTO"
  - email: "dana@example.com"
    first_name: "Dana"
    last_name: "Pawlak"
    title: "HR Manager"
````

## Tagging Metadata Items with Owners

Once the `owners.yaml` file is set up, you can tag various metadata resources with owner information through the metadata definition of that asset. Here is how you can do it:

### DBT Metadata Tagging

1. **Edit the YAML File**: Navigate to the YAML file corresponding to the resource you want to add metadata to.

2. **Add the Metadata**: Use the `meta` key to add custom key-value pairs within the YAML file. Here’s an example where a model is tagged with owner information:

   ````yaml
   models:
     - name: my_table
       description: "This is my example table"
       meta:
         owners:
           - email: "dana@example.com"
             type: "Business Owner"
           - email: "dana@example.com"
             type: "Technical Owner"
   ````

3. **Generate Metadata**

   To generate metadata, execute the following commands:
   
   - `dbt deps`
   - `dbt run`
   - `dbt test`
   - `dbt source freshness`
   - `dbt docs generate`

4. **Execute luma Ingest DBT**: Use the [`luma dbt ingest`](../cli.md#luma-dbt-ingest) command to ingest the DBT metadata into the Luma system, integrating the newly added owner information.