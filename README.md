# jobby

Track new jobs from companies you like. Uses [Grist](https://www.getgrist.com/) to store and retrieve job data.

See the [jobs](https://docs.getgrist.com/n9izTh6BMmma/Jobby/p/4) I am following. 

## Set up your own

1. Clone this [grist](https://docs.getgrist.com/n9izTh6BMmma/Jobby/p/4) documents so that you can customize the company list.
2. Clone this repo
3. Deploy the worker to fly with your own API keys and document ID.

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
