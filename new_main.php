<html>
<head>
<title>Thermostatinator</title>
<body background="ac.jpg">
<link rel="shortcut icon" href="favicon.ico" />
</head>

<?php

	$myfile = fopen("testfile.txt", "r");
	$i = 0;
	while(!feof($myfile)){
		$whole_line = fgets($myfile);
		$split_array = explode(" = ", $whole_line);
		$save_array[$i] = $split_array[1];
		$i++;
	}

	$value1 = $save_array[3];
	$value2 = $save_array[4];
	$value3 = $save_array[10];
	$value4 = $save_array[11];
	$value5 = $save_array[12];
?>


<div align="center" style="background-color:white;"><form action="phpinfo.php" method="post">
    Upper Limit: <input type="number" max="85" min="70" step="0.25" name="Upper_limit" style="color: blue; width:200px; height:100px; font-size: 60px;" value=<?php echo $value1; ?>><br>
    Lower Limit: <input type="number" max="75" min="60" step="0.25" name="Lower_limit" style="color: red; width:200px; height:100px; font-size: 60px;" value=<?php echo $value2; ?>><br>
	Outer Tolerance: <input type="number" max="3" min="0" step="0.25" name="Outer_Tolerance" style="color: gray; width:150px; height:75px; font-size: 45px;" value=<?php echo $value3; ?>><br>
    Inner Tolerance: <input type="number" max="3" min="0" step="0.25" name="Inner_Tolerance" style="color: gray; width:150px; height:75px; font-size: 45px;" value=<?php echo $value4; ?>><br>
	Logging Mode: <input type="number" max="2" min="0" step="1" name="Logging_Mode" style="color: black; width:50px; height:25px; font-size: 15px;" value=<?php echo $value5; ?>><br>
	<input type="submit" style="width:250px; height:125px; font-size: 40px">
</form>

<iframe id="dynamic-content" src="refreshing_content.php" width="800" height="450" frameborder="0" />

</div>



<script>
function upperFunction() {
	document.getElementById("Upper_Limit").stepUp();
}

function lowerFunction() {
	document.getElementById("Lower_Limit").stepUp();
}

function outerFunction() {
	document.getElementById("Outer_Tolerance").stepUp();
}

function innerFunction() {
	document.getElementById("Inner_Tolerance").stepUp();
}

function loggingFunction() {
	document.getElementById("Logging_Mode").stepUp();
}

</script>

</body>
</html>
