<html>
<head>
<title> CL crawled </title>
</head>
<body>
<pre>fuck yo couch craig.</pre><br/><hr/>
<?php
$contents = file_get_contents("/var/local/rooms.txt",1,NULL,0x0);
$listents = explode("\n", $contents); 
foreach ($listents as $link) {
	if (strlen($link) == 0 || strlen($link) == 1) {
		continue;
	}
	preg_match_all("/\/roo\/[a-z]\/(\w[\-\w]*)/", $link, $matches);
	// print_r($matches);
	print "<a href=\"" . $link . "\">" . array_shift($matches[1]) . "</a><br/>";
}
?>
</body
</html>

