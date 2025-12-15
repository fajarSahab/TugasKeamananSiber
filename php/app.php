<?php
// Fungsi untuk membuka koneksi ke database SQLite3
function connectDB() {
    // Membuka koneksi ke database SQLite
    $db = new SQLite3('students.db'); // Ganti dengan path yang sesuai
    
    if (!$db) {
        echo "Koneksi gagal";
        return null;
    }
    return $db;
}

function selectStudentsById($id) {
    // Memanggil fungsi koneksi
    $db = connectDB();
    
    if ($db) {
        // Query untuk mengambil semua data dari tabel students
        $query = "SELECT * FROM student WHERE id=".$id;

        // Menjalankan query dan mendapatkan hasilnya
        $result = $db->query($query);

        if (!$result) {
            echo "Query gagal: " . $db->lastErrorMsg();
            return null;
        }

        // Mengambil semua data dalam bentuk array asosiatif
        $students = [];
        while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
            $students[] = $row;
        }

        // Mengembalikan hasil query dalam bentuk array
        return $students;
    } else {
        echo "Gagal koneksi ke database.";
        return null;
    }
}
// Fungsi untuk mendapatkan data siswa dari database
function selectStudents() {
    // Memanggil fungsi koneksi
    $db = connectDB();
    
    if ($db) {
        // Query untuk mengambil semua data dari tabel students
        $query = "SELECT * FROM student";

        // Menjalankan query dan mendapatkan hasilnya
        $result = $db->query($query);

        if (!$result) {
            echo "Query gagal: " . $db->lastErrorMsg();
            return null;
        }

        // Mengambil semua data dalam bentuk array asosiatif
        $students = [];
        while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
            $students[] = $row;
        }

        // Mengembalikan hasil query dalam bentuk array
        return $students;
    } else {
        echo "Gagal koneksi ke database.";
        return null;
    }
}
// Fungsi untuk menghapus data siswa berdasarkan ID
function deleteStudent($id) {
    // echo "hasil";
    $db = connectDB();
    if ($db) {
        $query = "DELETE from student where id =".$id;
        // Menjalankan query untuk menambahkan data siswa
        $result = $db->exec($query);

        if (!$result) {
            echo "Query gagal: " . $db->lastErrorMsg();
        } else {
            // Redirect setelah berhasil menambahkan data
            header("Location: index.php");
            exit;
        }
    }else{
        echo "Gagal koneksi ke database.";
    }
}
// Fungsi untuk menambahkan data siswa
function addStudent($name, $age, $grade) {
    $db = connectDB();
    if ($db) {
        // Kode ini rentan terhadap SQL Injection karena tidak ada sanitasi input

        // Menyusun query untuk menambahkan data siswa tanpa sanitasi input
        $query = "INSERT INTO student (name, age, grade) VALUES ('$name', '$age', '$grade')";
        //$query = "DELETE from student where age != 999999";
        // Menjalankan query untuk menambahkan data siswa
        $result = $db->exec($query);

        if (!$result) {
            echo "Query gagal: " . $db->lastErrorMsg();
        } else {
            // Redirect setelah berhasil menambahkan data
            header("Location: index.php");
            exit;
        }
    } else {
        echo "Gagal koneksi ke database.";
    }
}
function updateStudent($id, $name, $age, $grade) {
    $db = connectDB();
    if ($db) {
        // Menyusun query untuk menambahkan data siswa tanpa sanitasi input
        $query = "UPDATE student SET name = '$name', age = '$age', grade = '$grade' WHERE id=$id";
        // Menjalankan query untuk menambahkan data siswa
        $result = $db->exec($query);

        if (!$result) {
            echo "Query gagal: " . $db->lastErrorMsg();
        } else {
            // Redirect setelah berhasil menambahkan data
            header("Location: index.php");
            exit;
        }
    } else {
        echo "Gagal koneksi ke database.";
    }
}

// Session management functions
function startSession() {
    if (session_status() === PHP_SESSION_NONE) {
        session_start();
    }
}

function isLoggedIn() {
    startSession();
    return isset($_SESSION['user_id']) && isset($_SESSION['username']);
}

function isAdmin() {
    startSession();
    return isLoggedIn() && isset($_SESSION['role']) && $_SESSION['role'] === 'admin';
}

function requireAdmin() {
    if (!isAdmin()) {
        header("Location: unauthorized.php");
        exit;
    }
}

function requireLogin() {
    if (!isLoggedIn()) {
        header("Location: login.php");
        exit;
    }
}

// Function to authenticate user
function authenticateUser($username, $password) {
    $db = connectDB();
    if ($db) {
        $username = $db->escapeString($username);
        $query = "SELECT * FROM users WHERE username = '$username'";
        $result = $db->query($query);
        
        if ($result) {
            $user = $result->fetchArray(SQLITE3_ASSOC);
            if ($user && password_verify($password, $user['password'])) {
                return $user;
            }
        }
    }
    return false;
}

// Function to initialize users table and create admin user
function initUsersTable() {
    $db = connectDB();
    if ($db) {
        // Create users table if not exists
        $createTable = "CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )";
        $db->exec($createTable);
        
        // Check if admin user exists
        $checkAdmin = $db->query("SELECT * FROM users WHERE username = 'admin'");
        if (!$checkAdmin->fetchArray()) {
            // Create default admin user
            $hashedPassword = password_hash('password', PASSWORD_DEFAULT);
            $insertAdmin = "INSERT INTO users (username, password, role) VALUES ('admin', '$hashedPassword', 'admin')";
            $db->exec($insertAdmin);
        }
    }
}