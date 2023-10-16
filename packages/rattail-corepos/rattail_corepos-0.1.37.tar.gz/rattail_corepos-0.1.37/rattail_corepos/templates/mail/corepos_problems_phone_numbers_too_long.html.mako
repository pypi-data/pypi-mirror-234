## -*- coding: utf-8; -*-
<%inherit file="/base_problems.html.mako" />

<%def name="summary()">
  <p>
    There are ${len(problems)} member records which have a phone
    number that is too long to properly fit in the `Customers`
    table.&nbsp; Please investigate and fix at your convenience.
  </p>
</%def>

<%def name="simple_row(member, i)">
  <tr>
    <td>${member.card_number}</td>
    <td>${member.phone}</td>
  </tr>
</%def>

${self.simple_table(["Card #", "Phone Number"])}
