---
layout: page
title: Photography
permalink: /photography
---

Taking pictures everywhere

<ul>
{% for page in site.photography %}
  <li><a href="{{ page.url | prepend: site.baseurl}}">{{ page.title }}</a><br>
      {{ page.description }}
 </li> 
{% endfor %}
</ul>
