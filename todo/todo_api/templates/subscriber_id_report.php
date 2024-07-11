<?php
$host = "127.0.0.1";
$port = "5432";
$dbname = "tenant";
$user = "postgres";
$password = "password";

$conn = pg_connect("host=$host port=$port dbname=$dbname user=$user password=$password");

if (!$conn) {
    die("Connection failed: " . pg_last_error());
}

$sql = "SELECT id, plan_id, tenant_id, start_date, end_date FROM todo_api_subscriber";
$result = pg_query($conn, $sql);

if (!$result) {
    die("Query failed: " . pg_last_error());
}
?>

<!DOCTYPE HTML>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        @page {
            size: A4;
            margin: 20mm;
        }

        .content {
            width: 210mm;
            height: 297mm;
            margin: auto;
        }

        table {
            width: 70%;
            margin: 0 auto;
            box-sizing: content-box;
            border-collapse: collapse;
        }

        .attribute {
            font-weight: bold;
            text-align: right;
            box-sizing: border-box;
        }

        .separator {
            text-align: center;
            font-weight: bold;
            box-sizing: border-box;
        }

        .value {
            padding: 10px;
            box-sizing: border-box;
        }

        footer {
            bottom: 0;
            width: 80%;
            text-align: center;
            margin: 0 auto;
        }

        hr {
            display: block;
            height: 2px;
            background: transparent;
            width: 80%;
            border: none;
            border-top: solid 2px #000000;
        }
    </style>
    <script>
        function displayDateTime() {
            const now = new Date();
            const dateTimeString = now.toLocaleString();
            document.getElementById('date-time').innerText = dateTimeString;
        }

        window.onload = displayDateTime;
    </script>

</head>
<body class="content">
    <header>
        <h1 style="text-align: center;">SUBSCRIBER REPORT BY USER ID</h1>
        <hr>
    </header>

    <table>
        <!-- code in progress -->
        <div style="text-align: center"><h5>*Code in progress*</h5></div>
    </table>
    <br>

    <hr>

    <footer class="footer">
        Generated on: <span id="date-time"></span>
    </footer>
</body>
</html>
