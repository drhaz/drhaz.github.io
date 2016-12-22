---
layout: page
title: My Activities
permalink: /activities
---

Some summaries of my private activities.

<ul>
{% for page in site.myactivities %}
  <li><a href="{{ page.url | prepend: site.baseurl}}">{{ page.title }}</a><br>
      {{ page.description }}
 </li> 
{% endfor %}
</ul>
