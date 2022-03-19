<html>
<head>
  <meta http-equiv="refresh" content="10">
</head>
<body>
<?php

	$myfile = fopen("testfile.txt", "r");
	$i = 0;
	while(!feof($myfile)){
		$whole_line = fgets($myfile);
		$split_array = explode(" = ", $whole_line);
		$save_array[$i] = $split_array[1];
		$i++;
	}
?>

<div align="center" style="background-color:white;">
<span style="color: green; font-size: 50px;"><head>Indoor Temperature: <?php echo $save_array[5]; ?>°F</span><br>
<span style="color: green; font-size: 50px;"><head>Current Mode: <?php echo $save_array[9]; ?></span><br>
Outdoor Temperature: <?php echo $save_array[0]; ?>°F<br>
Humidity: <?php echo $save_array[1]; ?>%<br>
Condition: <?php echo $save_array[2]; ?><br><br>
Current upper limit: <?php echo $save_array[3]; ?>°F<br>
Current lower limit: <?php echo $save_array[4]; ?> °F<br><br>
Last send_data.py call: <?php echo $save_array[6]; ?><br>
Last get_data.py update: <?php echo $save_array[7]; ?><br>
Last weather_scraper.py update: <?php echo $save_array[8]; ?><br>
</div>

</body>
</html>