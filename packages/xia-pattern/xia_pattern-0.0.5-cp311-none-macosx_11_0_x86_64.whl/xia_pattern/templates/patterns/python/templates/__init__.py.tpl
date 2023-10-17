{% for module_name, classes in modules.items() %}
from {{ package_name }}.{{ module_name }} import {{ classes|join(", ") }}
{% endfor %}

__all__ = [
    {% for classes in modules.values() %}"{{ classes|join('", "') }}"{% if not loop.last %},{% endif %}{% endfor %}

]

__version__ = "0.0.1"
