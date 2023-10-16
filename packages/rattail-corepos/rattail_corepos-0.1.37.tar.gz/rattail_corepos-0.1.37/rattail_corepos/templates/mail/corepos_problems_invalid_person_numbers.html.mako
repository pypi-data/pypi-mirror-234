## -*- coding: utf-8; -*-
<%inherit file="/base_problems.html.mako" />

<%def name="summary()">
  <p>
    There are ${len(problems)} customer records which have unexpected
    person number sequence.&nbsp; This may throw off some logic which
    expects the sequence to be valid.&nbsp; Please investigate and fix
    at your convenience.
  </p>
</%def>

<%def name="simple_row(obj, i)">
  <% customer, expected_person_number = obj %>
  <tr>
    <td>${customer.card_number}</td>
    <td>${customer.first_name}</td>
    <td>${customer.last_name}</td>
    <td>${expected_person_number}</td>
    <td>${customer.person_number}</td>
  </tr>
</%def>

${self.simple_table(["Card #", "First Name", "Last Name", "Expected Person #", "Current Person #"])}
