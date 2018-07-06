
{% for k, each in module.iteritems() %}
  {% if each.db %}
    {% if each.db.name %}
create database if not exists {{each.db.name}};
grant all on {{each.db.name}}.* to '{{each.name}}'@'localhost' identified by '{{each.password}}';
grant all on {{each.db.name}}.* to '{{each.name}}'@'%.%.int' identified by '{{each.password}}';
    {% endif %}

  {% for table in each.db.selectable %}
grant select on {{table}} to '{{each.name}}'@'localhost' identified by '{{each.password}}';
grant select on {{table}} to '{{each.name}}'@'%.%.int' identified by '{{each.password}}';
  {% endfor %}
  {% for table in each.db.writable %}
grant all on {{table}} to '{{each.name}}'@'localhost' identified by '{{each.password}}';
grant all on {{table}} to '{{each.name}}'@'%.%.int' identified by '{{each.password}}';
  {% endfor %}

  {% endif %}
{% endfor %}

flush privileges;

