{# Stickies screen #}
{% extends "lizard_map/wms.html" %}
{% load workspaces %}

{% block subtitle %} Meldingen {% endblock %}

{% block css %}
  {{ block.super }}
<link rel="stylesheet"
      href="{{ STATIC_URL }}lizard_sticky/lizard_sticky.css"
      type="text/css"
      media="screen, projection" />
{% endblock css %}

{% block head-extras %}
{# this block must come after the map-javascript block, so we use head-extras #}
<script type="text/javascript"
        src="{{ STATIC_URL }}lizard_sticky/lizard_sticky.js"></script>
{% endblock %}

{% block sidebar %}
<div id="sticky"
     data-url-lizard-sticky-add="{% url lizard_sticky.add_sticky %}"
     class="sidebarbox">
  <h2>Meldingen{% block linkback %}{% endblock %}</h2>
  <form id="sticky">
    <input id="sticky_navigate" type="radio" name="sticky" value="sticky_navigate" checked><label for="sticky_navigate">Navigeren</label></input>
    <input id="sticky_add" type="radio" name="sticky" value="add_sticky"><label for="sticky_add">Melding plaatsen</label></input>
  </form>
  </ul>

  {# The add-sticky popup div #}
  <div class="popup hide"
       id="add-sticky">
    <h1>Melding</h1>
    <div>
      <strong>Nieuwe melding</strong>
      <form id="add-sticky" style="background-color: lightyellow;" method="post">{% csrf_token %}
      <fieldset>
        <div>
          <label for="reporter" id="reporter">Naam</label>
          <br />
          <input id="sticky-reporter" type="text" name="reporter" />
        </div>
        <div>
          <label for="title" id="title">Onderwerp</label>
          <br />
          <input id="sticky-title" type="text" name="title" />
        </div>
        <div>
          <label for="description" id="description">Beschrijving</label>
          <br />
          <textarea id="sticky-description" name="description" rows="2" cols="30"></textarea>
        </div>
        <div>
          <label for="tags">Kernwoorden</label>
          <br />
          <input id="sticky-tags" type="text" name="tags" />
        </div>
      </fieldset>
      <button id="submit-sticky" type="submit">Sla op</button>
      <input id="sticky-x" type="hidden" name="x" value="" />
      <input id="sticky-y" type="hidden" name="y" value="" />
      </form>
    </div>
  </div>
</div>

<div id="sticky-browser"
     class="sidebarbox sidebarbox-stretched">
  <h2>Meldingen bladeren</h2>
  <ul id="sticky-browser-list" class="automatic-tree filetree">
    <li class="workspace-acceptable file sticky-browser-item"
        data-name="Meldingen"
        data-adapter-class="adapter_sticky"
        data-adapter-layer-json='{}'>
      alle meldingen</li>
    <li class="sticky-browser-item">
      <span class="folder">op kernwoorden</span>
      <ul>
        {% for tag in tags %}
        <li class="workspace-acceptable file"
            data-name="Meldingen ({{ tag }})"
            data-adapter-class="adapter_sticky"
            data-adapter-layer-json='{"tags": ["{{ tag.slug }}"]}'>
          {{ tag }}
        </li>
        {% empty %}
        <li>geen kernwoorden</li>
        {% endfor %}
      </ul>
    </li>
  </ul>
</div>

{% for workspace in workspaces.user %}
  {% workspace workspace %}
{% empty %}
No workspace
{% endfor %}

{% endblock %}
