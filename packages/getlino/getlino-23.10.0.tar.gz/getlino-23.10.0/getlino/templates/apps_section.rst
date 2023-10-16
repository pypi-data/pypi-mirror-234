
.. _{{repo.nickname}}:

{{rstgen.header(2, site.verbose_name)}}

{{package.SETUP_INFO['description']}}

Source code: {{package.SETUP_INFO['url']}}

{% if public_url %}
Documentation: {{public_url}}
{% endif  %}

..
  Available features:
  {% for f in site.features.keys() -%}
  :setting:`{{f}}`
  {% endfor  %}
