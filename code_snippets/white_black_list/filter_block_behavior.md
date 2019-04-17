## Behavior

the Blacklist always overrides the Whitelist. The following table displays filtering and blocking behavior for all scenarios involving the Whitelist and Blacklist. [[ref]](https://github.com/IBM-Bluemix-Docs/AvailabilityMonitoring/blob/master/avmon_whitelist_blacklist.md)

<table id="avmon_whitelist_blacklist__table_gyg_vvp_fbb">

<thead>
<tr>
<th>Blacklist</th>
<th>Whitelist</th>
<th>Behavior</th>
<th>Reason</th>
</tr>
</thead>
<tbody>
<tr>
<td>Empty</td>
<td>Empty</td>
<td>Allow access</td>
<td>No filtering rules entered.</td>
</tr>
<tr>
<td>Empty</td>
<td>URL does not match list entry</td>
<td>Block access</td>
<td>URL is not in the whitelist.</td>
</tr>
<tr>
<td>Empty</td>
<td>URL matches list entry</td>
<td>Allow access</td>
<td>URL is in the whitelist. No blacklist entry to block access.</td>
</tr>
<tr>
<td>URL does not match list entry</td>
<td>Empty</td>
<td>Allow access</td>
<td>URL is not in the blacklist. No whitelist entry to block access.</td>
</tr>
<tr>
<td>URL matches list entry</td>
<td>Empty</td>
<td>Block access</td>
<td>URL is in the blacklist.</td>
</tr>
<tr>
<td>URL does not match list entry</td>
<td>URL does not match list entry</td>
<td>Block access</td>
<td>URL is not in the whitelist.</td>
</tr>
<tr>
<td>URL does not match list entry</td>
<td>URL matches list entry</td>
<td>Allow access</td>
<td>URL is in the whitelist. URL is not in the blacklist.</td>
</tr>
<tr>
<td>URL matches list entry</td>
<td>URL does not match list entry</td>
<td>Block access</td>
<td>URL is not in the whitelist. URL is in the blacklist.</td>
</tr>
<tr>
<td>URL matches list entry</td>
<td>URL matches list entry</td>
<td>Block access</td>
<td>URL is in the blacklist. The blacklist entry overrides the whitelist entry.</td>
</tr>
</tbody>
</table>

<caption>Table 1. Filtering and blocking behavior for Whitelist and Blacklist</caption>


### 化简 

真值表(Truth Table)

<table>

<tr>
<th></th>
<th>白名单（空）</th>
<th>白名单（命中）</th>
<th>白名单（Miss）</th>
</tr>
<tr>
<th>黑名单（空）</th>
<th>Allow</th>
<th>Allow</th>
<th>Block</th>
</tr>
<tr>
<th>黑名单（命中）</th>
<th>Blcok</th>
<th>Blcok</th>
<th>Blcok</th>
</tr>
<tr>
<th>黑名单（Miss）</th>
<th>Allow</th>
<th>Allow</th>
<th>Blcok</th>
</tr>

</table>

化简真值表


<table>

<tr>
<th></th>
<th>白名单（空）</th>
<th>白名单（命中）</th>
<th>白名单（Miss）</th>
</tr>
<tr>
<th>黑名单（空/Miss）</th>
<th>Allow</th>
<th>Allow</th>
<th>Block</th>
</tr>
<tr>
<th>黑名单（命中）</th>
<th>Blcok</th>
<th>Blcok</th>
<th>Blcok</th>
</tr>

</table>

进一步化简

<table>

<tr>
<th></th>
<th>白名单（空/命中）</th>
<th>白名单（Miss）</th>
</tr>
<tr>
<th>黑名单（空/Miss）</th>
<th>Allow</th>
<th>Block</th>
</tr>
<tr>
<th>黑名单（命中）</th>
<th>Blcok</th>
<th>Blcok</th>
</tr>

</table>
