<?php
    include 'app.php'; 
    startSession();
    initUsersTable();
    
    // Check if user is logged in as admin
    requireAdmin();

    if (isset($_GET['id'])) {
        $id = $_GET['id'];
        deleteStudent($id);
    }

?>