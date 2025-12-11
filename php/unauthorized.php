<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unauthorized</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>403 - Unauthorized</h1>
        </header>

        <section class="form-section">
            <p style="font-size: 18px; color: #d32f2f;">You do not have permission to access this resource.</p>
            <p>This action requires administrator privileges.</p>
            
            <div style="margin-top: 20px;">
                <a href="index.php" class="btn btn-update">Go to Home</a>
                <?php
                include 'app.php';
                startSession();
                if (isLoggedIn()): ?>
                    <a href="logout.php" class="btn btn-delete">Logout</a>
                <?php else: ?>
                    <a href="login.php" class="btn btn-update">Login</a>
                <?php endif; ?>
            </div>
        </section>

        <footer>
            <p>&copy; 2024 Manajemen Siswa - ALH</p>
        </footer>
    </div>
</body>
</html>


