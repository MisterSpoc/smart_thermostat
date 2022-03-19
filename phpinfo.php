<?php
	
	if(($_POST["Upper_limit"] < $_POST["Lower_limit"]) or ($_POST["Upper_limit"] > 85) or ($_POST["Lower_limit"] < 60) or ($_POST["Outer_Tolerance"] == 0 and $_POST["Inner_Tolerance"] == 0) ) {
		exit('<form action="new_main.php" method="post"> <input type="submit" value="You fucked up"> </form>');
	}
	
	$myfile = fopen("testfile.txt", "r") or die("unable to open file");
	
	$save_array = array();
	$i = 0;	
	
	while(!feof($myfile)){
		$whole_line = fgets($myfile);
		$split_array = explode(" = ", $whole_line);
		$save_array[$i] = $split_array[1];
		$i++;
	}
	
	fclose($myfile);
	
	$save_array[3] = $_POST["Upper_limit"];
	$save_array[4] = $_POST["Lower_limit"];
	$save_array[10] = $_POST["Outer_Tolerance"];
	$save_array[11] = $_POST["Inner_Tolerance"];
	$save_array[12] = $_POST["Logging_Mode"];

	$myfile = fopen("testfile.txt", "w") or die("unable to open file");
	
	$txt .= "Current-Temperature = " . $save_array[0];
	$txt .= "Humidity = " . $save_array[1];
	$txt .= "Condition = " . $save_array[2];
	$txt .= "Upper-Limit = " . $save_array[3] . PHP_EOL;
	$txt .= "Lower-Limit = " . $save_array[4] . PHP_EOL;
	$txt .= "Indoor-Ambient = " . $save_array[5];
	$txt .= "SendData-Update = " . $save_array[6];
	$txt .= "GetData-Update = " . $save_array[7];
	$txt .= "Weather-Update = " . $save_array[8];
	$txt .= "Mode = " . $save_array[9];
	$txt .= "Outer-Tolerance = " . $save_array[10] . PHP_EOL;
	$txt .= "Inner-Tolerance = " . $save_array[11] . PHP_EOL;
	$txt .= "Logging-Mode = " . $save_array[12] . PHP_EOL;
	


	fwrite($myfile, $txt);
	
	fclose($myfile);
	
	
?>

<html><div align="center">
<form action="new_main.php" method="post">
	<input style="width:450px; height:800px; font-size: 50px" type="submit" value="Accepted">
</form>
</div></html>
