# Mkdocs Strapi Plugin

This plugin is designed to fetch data from Strapi API and inject that data into the mkdocs.
## Setup

Install the plugin using pip:

`pip install  mkdocs-strapi-plugin`


Activate the plugin in `mkdocs.yml`:
```yaml
plugins:
  - search
  -  mkdocs-strapi-plugin
```

## Configuration

```yaml
plugins:
  -  mkdocs-strapi-plugin:
      url: http://localhost:1337/API_endpoint
      content_types:
        - articles
        - blog
      output_dir: ./docs
      template: ./templates/article.md
      template_dir: ./templates
      template_name: article
      template_extension: md
```
