# jobby

Track new jobs from companies you like. Uses [Grist](https://www.getgrist.com/) to store and retrieve job data.

## Supported job platforms

- Greenhouse

## Schedule worker

Use fly to schedule the worker to run daily.

```bash
fly machine run . --name worker --schedule daily --env GRIST_API_KEY=xxxxx --env GRIST_DOC_ID=xxxxx
```

## Maintenance

#### Update Grist models from OpenAPI spec

```bash
datamodel-codegen --input grist/openapi-spec.yml --output grist/models.py --output-model-type=pydantic_v2.BaseModel --use-annotated
```
