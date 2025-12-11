<?php
include 'app.php';
startSession();

// Destroy session
session_unset();
session_destroy();

// Redirect to login page
header("Location: login.php");
exit;
?>


