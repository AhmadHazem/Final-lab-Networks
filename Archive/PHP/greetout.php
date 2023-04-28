<!DOCTYPE html>
</head>

<body>
    <div id="bg"></div>

    <h3><?php
if (isset($_POST['Username'])) {
    $username = $_POST['Username'];
    echo "Welcome, $username!";
}
?></h3>

    <a href="greet.php">return</a>
</body>

</html>