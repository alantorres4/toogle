<html>
	<head>
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<link rel="stylesheet" href="styles.css">
		<link href="data:image/x-icon;base64,AAABAAEAEBAQAAEABAAoAQAAFgAAACgAAAAQAAAAIAAAAAEABAAAAAAAgAAAAAAAAAAAAAAAEAAAAAAAAADMwFIAAAAAALhzLgC4gy4AuJouAOjegAChZisArUCQAL06pQChSSsArUBJAL+jPQDrUM8ArUCZAK1AYQCtQIAAERERERERERERERERERERERERERjBERERERERHYEREREREREX0RERERERER9xERERERERGuEREREREREZoRERERERERaRERERERERFmEREREREREWIRERERERERIhEREREVC0MiIiIhERC0MiIiIiERERERERERERERERERERERH//wAA//8AAP5/AAD+fwAA/n8AAP5/AAD+fwAA/n8AAP5/AAD+fwAA/n8AAP5/AADAAwAAwAMAAP//AAD//wAA" rel="icon" type="image/x-icon" />
		<title>Toogle</title>
	</head>

	<body>
		<br><br>
		<section class="main-section">
			<a href="http://www.csce.uark.edu/~ajtorres/information_retrieval_project_python/toogle.php">
				<h1><span style="color:#4285F4">T</span><span style="color:#DB4437">o</span><span style="color:#F4B400">o</span><span style="color:#4285F4">g</span><span style="color:#0F9D58">l</span><span style="color:#DB4437">e</span></h1>
			</a>
			<form action="toogle.php" method="post">
				<input type="text" name="query"><br>
				<input type="submit" name="submit" value="Search">
			</form>
		</section>
	</body>
	<footer>
		<a href="http://www.csce.uark.edu/~sgauch/4553/F21/hw/hw5.html" target="_blank">About this project</a>
		&nbsp;
    <a href="https://instagram.com/alanjto/" target="_blank">Instagram<a>
	</footer>
</html>

<?php
if (isset($_POST['submit']))
{
	// grab the query string from form
	$query = $_POST[query];
	// build command to be executed
	$command = 'python3 main.py ' . $query;
	//remove dangerous characters
	$escapedCommand = escapeshellcmd($command);
	$finalCommand = $escapedCommand . ' 2>&1';
	passthru($finalCommand);
}
?>
